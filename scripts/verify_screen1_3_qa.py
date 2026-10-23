"""Compare the three controller-driven chapel replays against approved 0.0.2."""
from pathlib import Path
import argparse
import hashlib
import json
import struct

p = argparse.ArgumentParser()
for name in ['before', 'after', 'out']:
    p.add_argument('--'+name, required=True)
a = p.parse_args()
result = {'emulator': 'MesenCE 2.2.1', 'ram_writes': False, 'cases': {}}

def pcm(path):
    data = path.read_bytes()
    assert data[:4] == b'RIFF' and data[8:16] == b'WAVEfmt ' and data[36:40] == b'data'
    assert struct.unpack('<IHHIIHH', data[16:36]) == (16, 1, 2, 48000, 192000, 4, 16)
    length = struct.unpack('<I', data[40:44])[0]
    assert length in (0, len(data)-44) and (len(data)-44)%4 == 0
    return data[44:]

for case in ['state1', 'state2', 'state3']:
    before, after = Path(a.before)/case, Path(a.after)/case
    assert (before/'completed.txt').read_text() == (after/'completed.txt').read_text() == '720'
    assert (before/'input.json').read_bytes() == (after/'input.json').read_bytes()
    report = {'emulated_frames': 720, **json.loads((after/'input.json').read_text())}
    bh = json.loads((before/'installed_pack_sha256.json').read_text())
    ah = json.loads((after/'installed_pack_sha256.json').read_text())
    assert bh.keys() <= ah.keys()
    added = sorted(ah.keys()-bh.keys())
    changed = sorted(k for k in bh if bh[k] != ah[k])
    assert added == ['Nave_Background.png', 'Nave_Tiles_2x.png']
    assert changed == ['README.txt', 'hires.txt']
    report.update(added_installed_files=added, changed_installed_files=changed,
                  unchanged_approved_files=len(bh)-len(changed))
    for ext in ['ram', 'ppu', 'oam']:
        paths = sorted((before/'dumps').glob('*.'+ext))
        assert len(paths) == 360
        assert all(v.read_bytes() == (after/'dumps'/v.name).read_bytes() for v in paths), (case, ext)
        report[ext+'_identical_samples'] = len(paths)
    apu = (before/'apu.tsv').read_bytes()
    assert apu == (after/'apu.tsv').read_bytes()
    report['apu_sha256'] = hashlib.sha256(apu).hexdigest()
    bp, ap = pcm(before/'full.wav'), pcm(after/'full.wav')
    common = min(len(bp), len(ap))
    assert common > 0 and bp[:common] == ap[:common], case+' PCM mismatch'
    report.update(identical_pcm_bytes=common, before_pcm_bytes=len(bp), after_pcm_bytes=len(ap))
    result['cases'][case] = report
result['total_emulated_frames_per_build'] = 2160
result['paired_samples_per_memory_type'] = 1080
out = Path(a.out)
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(json.dumps(result, indent=2)+'\n')
print(json.dumps(result, indent=2))
