"""Verify bounded flask replacement, paired native state/audio and pickup effects."""
from pathlib import Path
import argparse
import hashlib
import json
import re
import numpy as np
from PIL import Image

p = argparse.ArgumentParser()
for name in ['before', 'after', 'old-pack', 'out']:
    p.add_argument('--' + name, required=True)
a = p.parse_args()
root = Path(__file__).resolve().parents[1]
old_pack, pack = Path(a.old_pack), root / 'build/Holy_Diver_(Tr)'
old = json.loads((root / 'evidence/0.3.4-pack-sha256.json').read_text())
new = json.loads((root / 'evidence/approved-pack-sha256.json').read_text())
hashes = lambda folder: {f.name: hashlib.sha256(f.read_bytes()).hexdigest() for f in folder.iterdir() if f.is_file()}
assert hashes(old_pack) == old and hashes(pack) == new
assert len(old) == 79 and len(new) == 80
assert set(new) - set(old) == {'Recovery_Items_2x.png'}
assert sorted(k for k in old if old[k] != new[k]) == ['README.txt', 'hires.txt']
text = (pack / 'hires.txt').read_text()
restored = re.sub(r'^# BEGIN RECOVERY_ITEMS (IMAGES|MAPPINGS)\n.*?^# END RECOVERY_ITEMS \1\n', '', text, flags=re.M | re.S)
assert restored == (old_pack / 'hires.txt').read_text()
atlas = np.array(Image.open(pack / 'Recovery_Items_2x.png').convert('RGBA'))
assert atlas.shape == (32, 32, 4) and not atlas[:8, :, 3].any()
meta = json.loads((root / 'art/pickups/registration.json').read_text())
routes = json.loads((root / 'scripts/recovery_item_routes.json').read_text())
report = {'baseline': '0.3.4', 'candidate': '0.3.5', 'pack_files': 80,
          'new_files': ['Recovery_Items_2x.png'], 'changed_existing_files': ['README.txt', 'hires.txt'],
          'unchanged_existing_files': 77, 'previous_artwork_and_mappings_exact': True,
          'controller_only': True, 'ram_writes': False, 'cases': {}}
for case, route in routes.items():
    before, after = Path(a.before) / case, Path(a.after) / case
    frames = route['frames']
    assert (before / 'completed.txt').read_text() == (after / 'completed.txt').read_text() == str(frames)
    assert (before / 'input.json').read_bytes() == (after / 'input.json').read_bytes()
    assert (before / 'frames/0001.png').read_bytes() == (after / 'frames/0001.png').read_bytes() == b''
    for folder, expected in [(before, old), (after, new)]:
        for filename in ['installed_pack_sha256.json', 'installed_pack_after_sha256.json']:
            assert json.loads((folder / filename).read_text()) == expected
    result = {'frames': frames, **json.loads((after / 'input.json').read_text())}
    for ext in ['ram', 'ppu', 'oam']:
        files = sorted((before / 'dumps').glob('*.' + ext))
        assert len(files) == frames
        for f in files:
            assert f.read_bytes() == (after / 'dumps' / f.name).read_bytes(), (case, f.name)
        result[ext + '_identical_samples'] = frames
    apu = (before / 'apu.tsv').read_bytes()
    assert apu == (after / 'apu.tsv').read_bytes()
    bp, cp = (before / 'full.wav').read_bytes()[44:], (after / 'full.wav').read_bytes()[44:]
    common = min(len(bp), len(cp))
    assert common and bp[:common] == cp[:common] and abs(len(bp) - len(cp)) <= 3200
    result.update(apu_sha256=hashlib.sha256(apu).hexdigest(), identical_pcm_bytes=common,
                  before_pcm_bytes=len(bp), after_pcm_bytes=len(cp),
                  shutdown_tail_difference_bytes=abs(len(bp) - len(cp)))
    changed = []; exact_items = []; visible = []; unchanged = []
    item_index = 0 if case.startswith('hp_') else 1
    native_ids = {0x49, 0x4a} if item_index == 0 else {0x4b, 0x4c}
    for f in range(2, frames + 1):
        bi = np.array(Image.open(before / 'frames' / f'{f:04}.png').convert('RGB'))
        ci = np.array(Image.open(after / 'frames' / f'{f:04}.png').convert('RGB'))
        diff = np.any(bi != ci, axis=2)
        o = (after / 'dumps' / f'{f-1:04}.oam').read_bytes()
        q = (after / 'dumps' / f'{f-1:04}.ppu').read_bytes()
        sprites = [tuple(o[i:i+4]) for i in range(0, 256, 4) if o[i] < 239 and o[i+1] in native_ids and o[i+2] & 3 == 2]
        allowed = np.zeros(diff.shape, bool); exact = len(sprites) == 2
        if sprites:
            assert q[0x3f19:0x3f1c].hex() == '301116'
            visible.append(f)
        for y, tile, attr, x in sprites:
            assert q[tile*16:(tile+1)*16].hex() == meta['native_chr_patterns'][f'{tile:02X}']
            row = (tile - min(native_ids)) * 16
            source = atlas[row:row+16, item_index*16:(item_index+1)*16]
            if attr & 0x40: source = source[:, ::-1]
            if attr & 0x80: source = source[::-1]
            x0, y0 = x * 2, (y + 1) * 2
            allowed[y0:y0+16, x0:x0+16] = True
            crop = ci[y0:y0+16, x0:x0+16]; mask = source[:, :, 3] > 0
            exact &= crop.shape == source[:, :, :3].shape and np.array_equal(crop[mask], source[:, :, :3][mask])
        assert not np.any(diff & ~allowed), (case, f, 'changed outside recovery item')
        if diff.any(): changed.append(f)
        else: unchanged.append(f)
        if exact: exact_items.append(f)
    # Jumping reaches HP quickly; longer neutral cases prove the complete art
    # throughout the remaining drop/expiry interval.
    minimum = 10 if case in ['hp_collect', 'hp_normal_collect'] else 40
    assert len(exact_items) >= minimum and len(changed) >= minimum
    start = (after / 'dumps/0001.ram').read_bytes()
    end = (after / 'dumps' / f'{frames:04}.ram').read_bytes()
    if case.endswith('_collect'):
        assert max(visible) < frames - 100
        assert max(visible) == (24 if item_index == 0 else 92)
        assert all(f in unchanged for f in range(max(visible)+1, frames+1))
        if item_index == 1: assert (start[0x490], end[0x490]) == (10, 50)
        else: assert (start[0x440], end[0x440]) == (5, 6)
    else:
        assert max(visible) == (74 if item_index == 0 else 105)
        assert start[0x440] == end[0x440] and start[0x490] == end[0x490]
        assert all(f in unchanged for f in range(max(visible)+1, frames+1))
    result.update(changed_screenshots=len(changed), unchanged_screenshots=len(unchanged),
                  pixel_exact_whole_item_frames=len(exact_items), first_item_frame=min(visible),
                  last_item_frame=max(visible), life_before=start[0x440], life_after=end[0x440],
                  magic_before=start[0x490], magic_after=end[0x490],
                  disappears_by='collection' if case.endswith('_collect') else 'native expiry',
                  observed_restoration='HP 5 to 6' if item_index == 0 and case.endswith('_collect') else ('Magic 10 to 50' if case.endswith('_collect') else 'none; native expiry'))
    report['cases'][case] = result
report['total_frames_per_build'] = sum(r['frames'] for r in routes.values())
report['native_memory_and_audio_preserved'] = True
out = Path(a.out); out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(json.dumps(report, indent=2) + '\n')
print(json.dumps({k:v for k,v in report.items() if k != 'cases'}, indent=2))
