"""Verify paired full traversals and record the actual first falling frames."""
from pathlib import Path
import argparse
import hashlib
import json
import struct

p = argparse.ArgumentParser()
for name in ['before', 'after', 'out']:
    p.add_argument('--'+name, required=True)
a = p.parse_args()
result = {'emulator': 'MesenCE 2.2.1', 'ram_writes': False,
          'route': 'left frames 10-129; right two frames in eight from 160-439; otherwise neutral',
          'cases': {}}

def position(folder, frame):
    ram = (folder/f'dumps/{frame:04}.ram').read_bytes()
    oam = (folder/f'dumps/{frame:04}.oam').read_bytes()
    sprites = [oam[i:i+4] for i in range(0, 256, 4)
               if oam[i] < 240 and oam[i+2]&3 == 3 and 1 <= oam[i+1] < 64]
    assert sprites, frame
    return {'sprite_left': min(s[3] for s in sprites),
            'sprite_right_exclusive': max(s[3]+8 for s in sprites),
            'world_feet_y': max(s[0]+9 for s in sprites)+ram[0x3cf],
            'camera_y': ram[0x3cf]}

def pcm(path):
    data = path.read_bytes()
    assert data[:4] == b'RIFF' and data[8:16] == b'WAVEfmt ' and data[36:40] == b'data'
    assert struct.unpack('<IHHIIHH', data[16:36]) == (16, 1, 2, 48000, 192000, 4, 16)
    length = struct.unpack('<I', data[40:44])[0]
    assert length in (0, len(data)-44) and (len(data)-44)%4 == 0
    return data[44:]

for case, surface, edge_x, first_fall in [('upper', 96, 64, 353), ('lower', 272, 80, 417)]:
    before, after = Path(a.before)/case, Path(a.after)/case
    assert (before/'completed.txt').read_text() == (after/'completed.txt').read_text() == '460'
    assert (before/'input.json').read_bytes() == (after/'input.json').read_bytes()
    report = {'emulated_frames': 460, **json.loads((after/'input.json').read_text())}
    bh = json.loads((before/'installed_pack_sha256.json').read_text())
    ah = json.loads((after/'installed_pack_sha256.json').read_text())
    assert bh.keys() == ah.keys()
    changed = sorted(k for k in bh if bh[k] != ah[k])
    assert changed in [['EntranceScene.png'], ['EntranceScene.png', 'README.txt']], changed
    report['changed_installed_files'] = changed
    for ext in ['ram', 'ppu', 'oam']:
        paths = sorted((before/'dumps').glob('*.'+ext))
        assert len(paths) == 460
        assert all(p.read_bytes() == (after/'dumps'/p.name).read_bytes() for p in paths), (case, ext)
        report[ext+'_identical_samples'] = len(paths)
    apu = (before/'apu.tsv').read_bytes()
    assert apu == (after/'apu.tsv').read_bytes()
    report['apu_sha256'] = hashlib.sha256(apu).hexdigest()
    bp, ap = pcm(before/'full.wav'), pcm(after/'full.wav')
    common = min(len(bp), len(ap))
    assert common > 0 and bp[:common] == ap[:common]
    report['identical_pcm_bytes'] = common
    # The first two neutral frames still display the running OAM footprint.
    # Compare the settled idle silhouette after that native pose transition.
    left_hold = [position(after, f) for f in range(132, 160)]
    assert all(v == left_hold[0] for v in left_hold), 'Leftmost hold drifted'
    assert left_hold[0]['world_feet_y'] == surface
    route = [position(after, f) for f in range(160, first_fall+1)]
    assert all(v['world_feet_y'] == surface for v in route[:-1])
    assert route[-1]['world_feet_y'] == surface+1
    assert position(after, first_fall+8)['world_feet_y'] > surface+1
    report.update(leftmost_hold=left_hold[0], first_falling_frame=first_fall,
                  last_grounded_frame=first_fall-1,
                  first_falling_position=route[-1],
                  native_surface={'left': 0, 'right_exclusive': edge_x, 'y': surface},
                  hd_surface={'left': 0, 'right_exclusive': edge_x*2, 'y': surface*2})
    result['cases'][case] = report
result['total_emulated_frames_per_build'] = 920
result['paired_samples_per_memory_type'] = 920
out = Path(a.out)
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(json.dumps(result, indent=2)+'\n')
print(json.dumps(result, indent=2))
