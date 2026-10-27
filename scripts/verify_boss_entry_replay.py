"""Verify actual wall-boss entrance frames and unchanged native state/audio."""
from pathlib import Path
from collections import Counter
import argparse
import hashlib
import json
import wave
import numpy as np
from PIL import Image

parser = argparse.ArgumentParser()
for key in ['before', 'after', 'out']:
    parser.add_argument('--' + key, required=True)
args = parser.parse_args()
root = Path(__file__).resolve().parents[1]
before, after = Path(args.before), Path(args.after)
infos = [json.loads((p / 'result.json').read_text()) for p in [before, after]]
for key in ['movie_sha256', 'rom_sha1', 'core_sha256', 'movie_frames', 'captured_frames', 'stride']:
    assert infos[0][key] == infos[1][key], key
assert all(i['movie_completed'] and i['stride'] == 1 for i in infos)
for p, version in [(before, '0.20.3'), (after, '0.20.4')]:
    assert json.loads((p / 'installed_pack.json').read_text()) == json.loads(
        (root / f'evidence/{version}-pack-sha256.json').read_text())
frames = sorted(int(p.stem) for p in (after / 'frames').glob('*.png'))
data = {key: {} for key in ['ram', 'ppu', 'oam', 'view']}
for n in frames:
    for key in data:
        name = f'{n:06}' + ('.json' if key == 'view' else '.bin')
        raw = (after / key / name).read_bytes()
        assert raw == (before / key / name).read_bytes(), (n, key)
        data[key][n] = json.loads(raw) if key == 'view' else raw
apu = (before / 'apu.tsv').read_bytes()
assert apu == (after / 'apu.tsv').read_bytes()
with wave.open(str(before / 'full.wav'), 'rb') as f:
    pcm, params = f.readframes(f.getnframes()), f.getparams()
with wave.open(str(after / 'full.wav'), 'rb') as f:
    assert f.getparams() == params
    assert f.readframes(f.getnframes()) == pcm
palettes = {'0F271027': '0F270027', '0F271006': '0F270027', '0F020627': '0F121626'}
sources = {p: np.array(Image.open(root / f'art/boss2/wall_{s}.png').convert('RGBA'))
           for p, s in palettes.items()}
layout = json.loads((root / 'art/boss2/wall_layout.json').read_text())
cover = np.zeros((256, 192), bool)
for x, y in layout.values():
    cover[y:y+16, x:x+16] = True
background = np.array(Image.open(root / 'build/Holy_Diver_(Tr)/Stage2_Crimson_Cave_Background.png').convert('RGB'))
counts, palette_matches, examples = Counter(), Counter(), {}
changed_frames, changed_pixels = [], 0
for n in frames:
    paths = [p / 'frames' / f'{n:06}.png' for p in [before, after]]
    if not all(p.stat().st_size for p in paths):
        assert paths[0].stat().st_size == paths[1].stat().st_size
        counts['empty_initial'] += 1
        continue
    old, new = [np.array(Image.open(p).convert('RGB')) for p in paths]
    diff = np.any(old != new, axis=2)
    if not old.any():
        assert not new.any()
        counts['native_black_exact'] += 1
    if not diff.any():
        counts['identical'] += 1
        continue
    counts['changed'] += 1
    changed_frames.append(n)
    changed_pixels += int(diff.sum())
    assert data['ram'][n][0x78:0x7a] == b'\x7d\x8f'
    assert data['ram'][n][0x72] == 8
    scrolls, rendered_palettes = set(), set()
    sprites = np.zeros((480, 512), bool)
    for j in [n-1, n, n+1]:
        if j not in data['ppu']:
            continue
        pp, view, oam = (data[k][j] for k in ['ppu', 'view', 'oam'])
        scrolls.add((view['vram'] & 31) * 8 + view['xscroll'] + ((view['vram'] >> 10) & 1) * 256)
        rendered_palettes.add((pp[0x3f00:0x3f01] + pp[0x3f0d:0x3f10]).hex().upper())
        for k in range(0, 256, 4):
            x, y = oam[k+3] * 2, (oam[k] + 1) * 2
            if y < 480:
                sprites[max(0, y-2):min(480, y+18), max(0, x-2):min(512, x+18)] = True
    applicable = rendered_palettes & palettes.keys()
    assert applicable, (n, rendered_palettes)
    # End-frame view can describe the following camera position.
    if max(scrolls) - min(scrolls) <= 8:
        scrolls.update(range(min(scrolls), max(scrolls)+1))
    allowed = np.zeros((480, 512), bool)
    matches = []
    for scroll in scrolls:
        origin = 2 * (208 - scroll)
        left, right = max(0, origin), min(512, origin+192)
        if left >= right:
            continue
        visible = cover[:, left-origin:right-origin] & ~sprites[64:320, left:right]
        allowed[64:320, left:right] |= cover[:, left-origin:right-origin]
        actual = new[64:320, left:right]
        for palette in applicable:
            source = sources[palette][:, left-origin:right-origin]
            opaque = visible & (source[:, :, 3] == 255)
            if opaque.sum() < 1000 or not np.array_equal(actual[opaque], source[:, :, :3][opaque]):
                continue
            transparent = visible & (source[:, :, 3] == 0)
            bx = (np.arange(left, right) + scroll * 2) % background.shape[1]
            bg = background[64:320][:, bx]
            clear = np.all(actual == 0, axis=2) | np.all(actual == bg, axis=2)
            assert clear[transparent].all(), (n, palette, 'transparent boss remnants')
            matches.append((palette, scroll, int(opaque.sum()), int(transparent.sum())))
    assert not (diff & ~allowed).any(), (n, 'changed outside boss')
    assert matches, (n, 'complete visible boss source mismatch')
    palette, scroll, opaque, transparent = matches[0]
    palette_matches[palette] += 1
    examples.setdefault(palette, dict(frame=n, scroll=scroll, opaque_pixels=opaque,
                                     transparent_pixels=transparent))
assert set(palette_matches) == set(palettes)
report = dict(movie_frames=infos[1]['movie_frames'], native_samples_per_type=len(frames),
              native_state_exact=True, apu_exact=True, pcm_exact=True,
              pcm_bytes=len(pcm), pcm_sha256=hashlib.sha256(pcm).hexdigest(),
              movie_sha256=infos[1]['movie_sha256'], image_checks=dict(counts),
              changed_frames=changed_frames, changed_pixels=changed_pixels,
              complete_boss_matches=dict(palette_matches), examples=examples,
              all_changes_confined_to_missing_boss_palettes=True)
Path(args.out).write_text(json.dumps(report, indent=2) + '\n')
print(json.dumps(report, indent=2))
