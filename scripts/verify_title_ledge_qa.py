"""Compare paired live title/ledge replays, including actual grounded edges."""
from pathlib import Path
import argparse
import hashlib
import json
import struct

parser = argparse.ArgumentParser()
parser.add_argument('--before', required=True)
parser.add_argument('--after', required=True)
parser.add_argument('--out', required=True)
args = parser.parse_args()
result = {'emulator': 'MesenCE 2.2.1', 'controller_only': True, 'ram_writes': False, 'cases': {}}

def captured_pcm(path):
    """Read Mesen's PCM stream, including a zero-size header after emu.stop()."""
    data = path.read_bytes()
    assert data[:4] == b'RIFF' and data[8:16] == b'WAVEfmt ' and data[36:40] == b'data', path
    assert struct.unpack('<I', data[16:20])[0] == 16, path
    assert struct.unpack('<HHIIHH', data[20:36]) == (1, 2, 48000, 192000, 4, 16), path
    declared = struct.unpack('<I', data[40:44])[0]
    assert declared in [0, len(data)-44] and (len(data)-44)%4 == 0, path
    return data[44:], declared == 0

for case, end in [('title', 1800), ('upper_right', 1000), ('upper_left', 1000),
                  ('lower_right', 1320), ('lower_left', 1320)]:
    before, after = Path(args.before)/case, Path(args.after)/case
    assert (before/'completed.txt').read_text() == (after/'completed.txt').read_text() == str(end)
    report = {'emulated_frames': end}
    baseline_pack = json.loads((before/'installed_pack_sha256.json').read_text())
    candidate_pack = json.loads((after/'installed_pack_sha256.json').read_text())
    assert baseline_pack.keys() == candidate_pack.keys()
    changed_pack = sorted(name for name in baseline_pack if baseline_pack[name] != candidate_pack[name])
    assert changed_pack == ['EntranceScene.png', 'README.txt', 'Title_HD.png', 'Title_Intro_HD.png']
    report['installed_pack_hashes_verified'] = True
    for ext in ['ram', 'ppu', 'oam']:
        paths = sorted((before/'dumps').glob('*.'+ext))
        assert len(paths) == end//4, (case, ext, len(paths))
        assert all(p.read_bytes() == (after/'dumps'/p.name).read_bytes() for p in paths), (case, ext)
        report[ext+'_identical_samples'] = len(paths)
    apu = (before/'apu.tsv').read_bytes()
    assert apu == (after/'apu.tsv').read_bytes(), (case, 'APU writes')
    report['apu_sha256'] = hashlib.sha256(apu).hexdigest()
    audio_before, unfinished_before = captured_pcm(before/'full.wav')
    audio_after, unfinished_after = captured_pcm(after/'full.wav')
    common = min(len(audio_before), len(audio_after))
    assert common > 0 and audio_before[:common] == audio_after[:common], (case, 'PCM audio')
    report['identical_pcm_bytes'] = common
    report['audio_capture_header_unfinalized'] = {'before': unfinished_before, 'after': unfinished_after}
    if case == 'title':
        ready_values = {}
        for frame, expected in [(240, 0x40), (420, 1), (1140, 0x40), (1320, 1)]:
            ram = (after/f'dumps/{frame:04d}.ram').read_bytes()
            assert ram[0x4af] == expected, (frame, ram[0x4af])
            ready_values[str(frame)] = expected
            assert (before/f'frames/{frame:04d}.png').read_bytes() != (after/f'frames/{frame:04d}.png').read_bytes(), 'Title repair not visible'
        report['native_title_ready_states'] = ready_values
        for frame in [580, 1480]:
            assert (before/f'frames/{frame:04d}.png').read_bytes() == (after/f'frames/{frame:04d}.png').read_bytes()
        report['stage_cards_unchanged'] = True
    else:
        target = 96 if case.startswith('upper') else 272
        checkpoint = 840 if case.startswith('upper') else 1200
        grounded = []
        for frame in range(checkpoint-20, checkpoint+21, 4):
            ram = (after/f'dumps/{frame:04d}.ram').read_bytes()
            data = (after/f'dumps/{frame:04d}.oam').read_bytes()
            sprites = [tuple(data[i:i+4]) for i in range(0, 256, 4)
                       if data[i] < 240 and data[i+2]&3 == 3 and 1 <= data[i+1] < 64]
            assert sprites and all(s[1] <= 9 for s in sprites), (case, frame, 'not idle')
            assert max(s[0]+9 for s in sprites)+ram[0x3cf] == target, (case, frame, 'not grounded')
            grounded.append(frame)
        report.update(checkpoint_frame=checkpoint, native_world_surface_y=target,
                      hd_world_surface_y=target*2, stationary_samples=grounded)
        assert (before/f'frames/{checkpoint:04d}.png').read_bytes() != (after/f'frames/{checkpoint:04d}.png').read_bytes(), 'Ledge repair not visible'
    result['cases'][case] = report
result['total_emulated_frames_per_build'] = sum(c['emulated_frames'] for c in result['cases'].values())
result['paired_state_samples'] = sum(c['ram_identical_samples'] for c in result['cases'].values())
out = Path(args.out)
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(json.dumps(result, indent=2)+'\n')
print(json.dumps(result, indent=2))
