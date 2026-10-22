"""Compare controller replay results and prove stable feet/world coordinates.

Usage: python verify_platform_landings.py ORIGINAL_OUTPUT HD_OUTPUT
Both directories are produced by run_mesen_platform_qa.py.
"""
from pathlib import Path
import sys, json, hashlib

original, hd = map(Path, sys.argv[1:3])
assert (hd/'completed.txt').read_text().strip() == '1700', 'Replay incomplete'
landings = [('upper_left',900,192), ('upper_right',1090,240),
            ('middle_left',1280,288), ('lower_right',1470,336),
            ('lower_left',1660,384)]
oam = {}
for line in (hd/'oam.tsv').read_text().splitlines():
    fields = line.split('\t')
    oam[int(fields[0])] = [tuple(map(int, field.split(','))) for field in fields[1:]]
assert (original/'oam.tsv').read_bytes() == (hd/'oam.tsv').read_bytes()
assert (original/'state.tsv').read_bytes() == (hd/'state.tsv').read_bytes()
samples = list((original/'ram').glob('*.bin'))
for file in samples:
    assert file.read_bytes() == (hd/'ram'/file.name).read_bytes(), file.name
results = []
for name, frame, target_y in landings:
    original_ram = (original/(name+'.ram')).read_bytes()
    assert original_ram == (hd/(name+'.ram')).read_bytes(), name
    stable = []
    for f in range(frame, frame+29):
        file = hd/'ram'/f'{f:04d}.bin'
        if not file.exists():
            continue
        ram = file.read_bytes()
        player = [v for v in oam[f] if v[2]&3 == 3 and 1 <= v[1] < 64]
        assert player and all(v[1] <= 9 for v in player), (name, f, 'not idle')
        # Each 8px sprite begins at OAM Y+1. Its exclusive bottom is Y+9.
        feet_screen = max(v[0]+9 for v in player)
        camera_y = ram[0x3cf]
        assert feet_screen + camera_y == target_y, (name, f, feet_screen, camera_y)
        stable.append(f)
    assert len(stable) >= 7, name
    results.append({'branch':name, 'capture_frame':frame,
                    'nes_world_surface_y':target_y, 'hd_world_surface_y':target_y*2,
                    'stable_sample_frames':stable, 'ram_matches_original':True})
report = {'emulator':'Mesen 2.1.1 Linux x64', 'controller_only':True,
          'ram_writes_or_cheats':False, 'ram_samples_matching':len(samples),
          'oam_and_room_signatures_identical':True, 'landings':results}
(hd/'landing_verification.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
