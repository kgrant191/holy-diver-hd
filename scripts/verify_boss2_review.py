"""Verify the two reported boss echoes using paired actual emulator captures."""
from pathlib import Path
from collections import Counter
import hashlib
import json
import numpy as np
from PIL import Image

root = Path(__file__).resolve().parents[1]
work = root / 'work/boss2_review'
old = json.loads((root / 'evidence/0.10.0-pack-sha256.json').read_text())
new = json.loads((root / 'evidence/0.10.1-pack-sha256.json').read_text())
assert set(old) == set(new)
assert sorted(k for k in old if old[k] != new[k]) == ['Boss2_Tiles_2x.png', 'README.txt', 'hires.txt']
layout = json.loads((root / 'art/boss2/wall_layout.json').read_text())
cover = np.zeros((256, 192), dtype=bool)
for x, y in layout.values():
    cover[y:y+16, x:x+16] = True
walls = {pal: np.array(Image.open(root / f'art/boss2_review/wall_{pal}.png').convert('RGBA'))
         for pal in ['0F170F17', '0F070F07']}
flash = np.array(Image.open(root / 'build/Holy_Diver_(Tr)/Boss2_Cave_Flash.png').convert('RGB'))


def rgb(path):
    return np.array(Image.open(path).convert('RGB'))


def locations(folder, n, stride, frames):
    offsets, sprites = [], np.zeros((480, 512), dtype=bool)
    for j in [max(stride, n-stride), n, min(frames, n+stride)]:
        vals = (folder / f'dumps/{j:04}.view').read_text().split(',')
        tmp, fine = int(vals[0]), int(vals[1])
        offsets.append((tmp & 31)*8 + fine + ((tmp >> 10) & 1)*256)
        oam = (folder / f'dumps/{j:04}.oam').read_bytes()
        for k in range(0, 256, 4):
            x, y = oam[k+3]*2, (oam[k]+1)*2
            if y < 480:
                sprites[y:min(y+16, 480), x:min(x+16, 512)] = True
    positions = set(offsets)
    for start, end in zip(offsets, offsets[1:]):
        if abs(end-start) <= 8:
            positions.update(range(min(start, end), max(start, end)+1))
    return positions, sprites


cases = [('pickup', work/'before/pickup', work/'after/pickup', 1600, 1,
          '6cfdc375c9620d42e989e96ce4e855babe06f3d54fd49aa28d0de9bf7a408345')]
routes = json.loads((root / 'scripts/boss2_routes.json').read_text())
for case, route in routes.items():
    baseline = work/'arena_repeat_before'/case if case == 'arena' else root/'work/boss2/after'/case
    candidate = work/'arena_repeat_after'/case if case == 'arena' else work/'regression_after'/case
    cases.append(('original_'+case, baseline, candidate, route['frames'], 2,
                  '3dc10e1f35dda26171678ca6548fc3f974635b6e9face870525398c1a658f7e6'))
report = dict(baseline='0.10.0', candidate='0.10.1', controller_only=True,
              ram_writes=False, unchanged_runtime_assets=90, pack_files=93, cases={})
for name, before, after, frames, stride, state in cases:
    assert (before/'completed.txt').read_text() == (after/'completed.txt').read_text() == str(frames)
    assert (before/'input.json').read_bytes() == (after/'input.json').read_bytes()
    inputs = json.loads((after/'input.json').read_text())
    assert inputs['state_sha256'] == state
    for folder, hashes in [(before, old), (after, new)]:
        for filename in ['installed_pack_sha256.json', 'installed_pack_after_sha256.json']:
            assert json.loads((folder/filename).read_text()) == hashes
    for ext in ['ram', 'ppu', 'oam', 'view']:
        files = list((before/'dumps').glob('*.'+ext))
        assert len(files) == frames//stride
        for file in files:
            assert file.read_bytes() == (after/'dumps'/file.name).read_bytes(), (name, file.name)
    apu = (before/'apu.tsv').read_bytes()
    assert apu == (after/'apu.tsv').read_bytes()
    left, right = (before/'full.wav').read_bytes()[44:], (after/'full.wav').read_bytes()[44:]
    common, tail = min(len(left), len(right)), abs(len(left)-len(right))
    assert left[:common] == right[:common] and tail <= 3200, (name, 'PCM', tail)
    counts, examples = Counter(), {}
    for n in range(stride, frames+1, stride):
        if n == 1 and (before/f'frames/{n:04}.png').stat().st_size == 0:
            assert (after/f'frames/{n:04}.png').stat().st_size == 0
            counts['empty_initial_capture'] += 1
            continue
        a, b = rgb(before/f'frames/{n:04}.png'), rgb(after/f'frames/{n:04}.png')
        different = np.any(a != b, axis=2)
        if not different.any():
            counts['identical_images'] += 1
            continue
        counts['changed_images'] += 1
        ram = (after/f'dumps/{n:04}.ram').read_bytes()
        assert ram[0x78:0x7a] == bytes.fromhex('7d8f'), (name, n, 'outside boss room')
        positions, sprites = locations(after, n, stride, frames)
        permitted = np.zeros((480, 512), dtype=bool)
        matched = None
        for scroll in positions:
            X = 2*(208-scroll)
            x0, x1 = max(0, X), min(512, X+192)
            if x0 >= x1:
                continue
            mask = cover[:, x0-X:x1-X]
            permitted[64:320, x0:x1] |= mask
            visible = mask & ~sprites[64:320, x0:x1]
            actual = b[64:320, x0:x1]
            # Every non-sprite pixel in every covered boss tile must match.
            # This checks transparent areas too, so native fallback remnants fail.
            if visible.sum() > 12000:
                expected_flash = flash[64:320, 2*scroll+x0:2*scroll+x1]
                if np.array_equal(actual[visible], expected_flash[visible]):
                    matched = ('hidden_pickup_echo', scroll, int(visible.sum()))
                for palette, wall in walls.items():
                    crop = wall[:, x0-X:x1-X]
                    expected_wall = np.where(crop[:, :, 3:4] > 0, crop[:, :, :3], 0)
                    if ((crop[:, :, 3] > 0) & visible).sum() > 4000 and np.array_equal(actual[visible], expected_wall[visible]):
                        matched = (palette, scroll, int(visible.sum()))
        assert not (different & ~permitted).any(), (name, n, 'changed outside boss tiles')
        assert matched is not None, (name, n, 'boss source/background mismatch')
        key, scroll, pixels = matched
        counts[key] += 1
        examples.setdefault(key, dict(frame=n, scroll=scroll, exact_pixels=pixels))
    if name in ['original_poses', 'original_arena']:
        assert counts['changed_images'] == 0
    if name == 'pickup':
        for key in ['0F170F17', '0F070F07', 'hidden_pickup_echo']:
            assert counts[key] > 0, key
    if name == 'original_victory':
        assert counts['hidden_pickup_echo'] > 0
    report['cases'][name] = dict(frames=frames, capture_stride=stride,
        before_path=str(before.relative_to(root)), after_path=str(after.relative_to(root)),
        native_samples_per_type=frames//stride, input=inputs,
        apu_sha256=hashlib.sha256(apu).hexdigest(), identical_common_pcm_bytes=common,
        shutdown_tail_bytes=tail, image_checks=dict(counts), examples=examples)
report['total_frames_per_build'] = sum(c[3] for c in cases)
report['native_samples_per_type'] = sum(c[3]//c[4] for c in cases)
out = root / 'evidence/boss2_review'
out.mkdir(exist_ok=True)
(out/'validation.json').write_text(json.dumps(report, indent=2)+'\n')
print(json.dumps(report, indent=2))
