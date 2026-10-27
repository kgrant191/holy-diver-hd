"""Require exact native/audio replay and replacement only of missing scenery."""
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
for capture, version in [(before, '0.20.4'), (after, '0.20.5')]:
    assert json.loads((capture / 'installed_pack.json').read_text()) == json.loads(
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
background = np.array(Image.open(root / 'build/Holy_Diver_(Tr)/Poison_Moss_Ruins_Background.png').convert('RGB'))[:, :512]
nonblack_background = np.any(background != 0, axis=2)
pack = root / 'build/Holy_Diver_(Tr)'
lines = (pack / 'hires.txt').read_text().splitlines()
images = [line[5:] for line in lines if line.startswith('<img>')]
ui = np.array(Image.open(pack / images[21]).convert('RGBA'))
hud = {}
for line in lines:
    if not line.startswith('<tile>21,06'):
        continue
    fields = line[6:].split(',')
    tile = int(fields[1], 16)
    if 0x650 <= tile < 0x660 and fields[2] == 'FF301116':
        x, y = int(fields[3]), int(fields[4])
        assert fields[5:] == ['1', 'N']
        hud[tile & 255] = ui[y:y+16, x:x+16]


def probe(n):
    pp, view = data['ppu'][n], data['view'][n]
    v = view['vram']
    sx = (v & 31)*8 + view['xscroll'] + (256 if v & 0x400 else 0)
    sy = ((v >> 5) & 31)*8 + ((v >> 12) & 7) + (240 if v & 0x800 else 0)
    x, y = (sx+128)//8, (sy+16)//8
    nt = 0x2000 + (x//32 % 2)*0x400 + (y//30 % 2)*0x800
    x, y = x % 32, y % 30
    tile = pp[nt + y*32 + x]
    attr = pp[nt + 960 + (y//4)*8 + x//4]
    pal = (attr >> ((y % 4//2)*4 + (x % 4//2)*2)) & 3
    palette = (pp[0x3f00:0x3f01] + pp[0x3f01+pal*4:0x3f04+pal*4]).hex().upper()
    return f'{tile+0x700:04X}', palette


counts, guards, examples, changed_frames = Counter(), Counter(), {}, []
restored_pixels = 0
blended_hud_pixels = 0
for n in frames:
    paths = [capture / 'frames' / f'{n:06}.png' for capture in [before, after]]
    if not all(p.stat().st_size for p in paths):
        assert paths[0].stat().st_size == paths[1].stat().st_size
        counts['empty_initial'] += 1
        continue
    old, new = [np.array(Image.open(p).convert('RGB')) for p in paths]
    diff = np.any(old != new, axis=2)
    room = data['ram'][n][0x78:0x7a]
    if not old.any():
        assert not new.any(), (n, 'native blackout changed')
        counts['native_black_exact'] += 1
    if room != b'\xee\x9d':
        assert not diff.any(), (n, 'outside room changed')
        counts['other_room_or_menu_exact'] += 1
    if not diff.any():
        counts['identical'] += 1
        continue
    assert room == b'\xee\x9d' and data['ram'][n][0x72] == 0x14
    near = [j for j in [n-1, n, n+1] if j in data['ppu']]
    observed = {probe(j) for j in near} & {('074B', '0F091929'), ('074C', '0F091929')}
    assert observed, (n, 'missing rendered ceiling signature')
    # The old HUD has translucent glyph edges. Require the exact stock-Mesen
    # integer alpha blend there, using the unchanged source and native OAM.
    direct = np.all(old == 0, axis=2) & np.all(new == background, axis=2)
    blended = np.zeros((480, 512), bool)
    for j in near:
        oam, pp = data['oam'][j], data['ppu'][j]
        for k in range(0, 256, 4):
            y, tile, attr, x = oam[k:k+4]
            if tile not in hud or y >= 48:
                continue
            if pp[0x3f11+(attr & 3)*4:0x3f14+(attr & 3)*4] != b'\x30\x11\x16':
                continue
            x, y = x*2, (y+1)*2
            if x+16 > 512 or y+16 > 480:
                continue
            source = hud[tile]
            if attr & 0x40:
                source = source[:, ::-1]
            if attr & 0x80:
                source = source[::-1]
            source = source.astype(np.uint16)
            alpha = source[:, :, 3:4]
            premultiplied = source[:, :, :3]*(alpha+1) >> 8
            expected = premultiplied + (background[y:y+16, x:x+16].astype(np.uint16)*(256-alpha) >> 8)
            valid = ((alpha[:, :, 0] > 0) & (alpha[:, :, 0] < 255)
                     & np.all(old[y:y+16, x:x+16] == premultiplied, axis=2)
                     & np.all(new[y:y+16, x:x+16] == expected, axis=2))
            blended[y:y+16, x:x+16] |= valid
    assert not (diff & ~direct & ~blended).any(), (n, 'unexpected foreground/panorama change')
    blended_hud_pixels += int((diff & ~direct & blended).sum())
    matches = int((np.all(new == background, axis=2) & nonblack_background).sum())
    assert matches > 50000, (n, 'incomplete background restoration', matches)
    counts['changed'] += 1
    changed_frames.append(n)
    restored_pixels += int(diff.sum())
    for tile, palette in observed:
        guards[tile] += 1
        examples.setdefault(tile, dict(frame=n, panorama_pixels=matches,
                                      restored_pixels=int(diff.sum())))
assert set(guards) == {'074B', '074C'}
report = dict(movie_frames=infos[1]['movie_frames'], native_samples_per_type=len(frames),
              movie_sha256=infos[1]['movie_sha256'], native_state_exact=True,
              apu_exact=True, pcm_exact=True, pcm_bytes=len(pcm),
              pcm_sha256=hashlib.sha256(pcm).hexdigest(), image_checks=dict(counts),
              changed_frames=changed_frames, restored_pixels=restored_pixels,
              observed_guard_matches=dict(guards), examples=examples,
              panorama_pixels_exact=True, translucent_hud_blends_exact=True,
              blended_hud_pixels=blended_hud_pixels,
              all_opaque_foreground_pixels_unchanged=True)
Path(args.out).write_text(json.dumps(report, indent=2) + '\n')
print(json.dumps(report, indent=2))
