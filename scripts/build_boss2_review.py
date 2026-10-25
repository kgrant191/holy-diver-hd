"""Keep the boss HD through gold-palette defeat, then hide its pickup echo."""
from pathlib import Path
import hashlib
import json
import numpy as np
from PIL import Image

root = Path(__file__).resolve().parents[1]
pack = root / 'build/Holy_Diver_(Tr)'
art = root / 'art/boss2_review'
art.mkdir(exist_ok=True)
atlas = Image.open(pack / 'Boss2_Tiles_2x.png').convert('RGBA')
base = np.array(atlas)
expected = json.loads((root / 'evidence/0.10.0-pack-sha256.json').read_text())
assert hashlib.sha256((pack / 'Boss2_Tiles_2x.png').read_bytes()).hexdigest() == expected['Boss2_Tiles_2x.png']
registration = json.loads((root / 'art/boss2/registration.json').read_text())
layout = json.loads((root / 'art/boss2/wall_layout.json').read_text())
empty = next(m['xy'] for m in registration['mappings']
             if m['kind'] == 'defeated boss hidden')
source = np.array(Image.open(root / 'art/boss2/wall_0F270027.png').convert('RGBA'))
scope = 'b2Room&b2Lo&b2Hi'
rules, records, cells = [], [], {}
# Append on a fresh row, preserving every existing atlas pixel/reference.
first_cell = ((registration['atlas_cells'] + 63) // 64) * 64
for palette, factor in [('0F170F17', .60), ('0F070F07', .28)]:
    pixels = source.copy()
    pixels[:, :, :3] = (pixels[:, :, :3].astype(float) * factor).astype('uint8')
    wall = Image.fromarray(pixels)
    wall.save(art / f'wall_{palette}.png')
    for identity, (x, y) in layout.items():
        cell = wall.crop((x, y, x + 16, y + 16))
        digest = hashlib.sha256(cell.tobytes()).hexdigest()
        if digest not in cells:
            number = first_cell + len(cells)
            pos = (number % 64 * 16, number // 64 * 16)
            assert pos[1] + 16 <= atlas.height
            assert not base[pos[1]:pos[1]+16, pos[0]:pos[0]+16].any()
            cells[digest] = pos
            atlas.paste(cell, pos)
        ax, ay = cells[digest]
        rules.append(f'[{scope}]<tile>39,{identity},{palette},{ax},{ay},1,N')
        records.append(dict(identity=identity, palette=palette, xy=[ax, ay]))
# The dead boss's native tiles remain in the nametable during the pickup flash.
# Keep the room flash, but use the existing transparent cell for this palette.
for identity in layout:
    rules.append(f'[{scope}]<tile>39,{identity},310F0F0F,{empty[0]},{empty[1]},1,N')
text = (pack / 'hires.txt').read_text()
marker = '# BEGIN BOSS2 MAPPINGS\n'
block = '# BEGIN BOSS2_REVIEW\n' + '\n'.join(rules) + '\n# END BOSS2_REVIEW\n'
assert text.count(marker) == 1
(pack / 'hires.txt').write_text(text.replace(marker, block + marker))
atlas.save(pack / 'Boss2_Tiles_2x.png')
atlas.save(art / 'Boss2_Tiles_2x.png')
(art / 'registration.json').write_text(json.dumps(dict(
    tile_rules=len(rules), first_cell=first_cell, added_cells=len(cells),
    palettes=['0F170F17', '0F070F07'], hidden_palette='310F0F0F',
    empty_cell=empty, mappings=records, source='art/boss2/wall_0F270027.png',
    native_gameplay_modified=False), indent=2) + '\n')
print(f'Boss 2 review: {len(rules)} scoped rules; gold defeat fades and hidden pickup echo.')
