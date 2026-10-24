"""Register the second horizontal cave using approved Stage 2 artwork."""
from pathlib import Path
import hashlib
import json
import numpy as np
from PIL import Image

root = Path(__file__).resolve().parents[1]
pack = root / 'build/Holy_Diver_(Tr)'
art = root / 'art/screen2_4'
text = (pack / 'hires.txt').read_text()
assert text.count('<img>') == 35
scope = 's24Room&s24DataLo&s24DataHi'
conditions = [
    '<condition>s24Room,memoryCheckConstant,0072,==,10',
    '<condition>s24DataLo,memoryCheckConstant,0078,==,AD',
    '<condition>s24DataHi,memoryCheckConstant,0079,==,8C',
    '<condition>s24WallPalette0,ppuMemoryCheckConstant,3F09,==,06',
    '<condition>s24WallPalette1,ppuMemoryCheckConstant,3F0A,==,18',
    '<condition>s24WallPalette2,ppuMemoryCheckConstant,3F0B,==,28',
]
aliases, rules, metadata = [], [], []
patterns = json.loads((art / 'native_patterns.json').read_text())
prior = json.loads((root / 'art/screen2_1/registration.json').read_text())['scope']

# All 512 native patterns are byte-identical to the approved exterior bank.
# Reuse terrain, pools/ice, breakable blocks, demons/arrows and pulsing rocks.
# Distant exterior sky and doorway-specific black fills do not belong here.
for line in text.splitlines():
    if not line.startswith('[' + prior + ']<tile>'):
        continue
    fields = line.split('<tile>')[1].split(',')
    t = int(fields[1], 16)
    if t < 0x300 or t == 0x300 or 0x32E <= t <= 0x34A:
        aliases.append(line.replace(prior, scope, 1))

cave_scope = json.loads((root / 'art/screen2_2/registration.json').read_text())['scope']
for line in text.splitlines():
    if not line.startswith('[' + cave_scope) or '<tile>' not in line:
        continue
    t = int(line.split('<tile>')[1].split(',')[1], 16)
    if 0x35B <= t <= 0x35E or 0x389 <= t <= 0x38E or t in [0x3A1, 0x3A2]:
        aliases.append(line.replace(cave_scope, scope, 1))

# Re-register the accepted gold texture within the new native ceiling edges.
# No new painted scenery or enemy source is introduced.
gold = Image.open(root / 'art/layers/50_floor.png').convert('RGBA').crop((256,880,320,912))
gold = gold.resize((32,32), Image.Resampling.LANCZOS)
alpha = gold.getchannel('A').point(lambda v:255 if v >= 120 else 0)
gold = gold.convert('RGB').quantize(colors=48).convert('RGBA')
gold.putalpha(alpha)
atlas = Image.new('RGBA', (128,64))
cache = {}

def tile(t, palette, image, kind):
    digest = hashlib.sha256(image.tobytes()).hexdigest()
    if digest not in cache:
        n = len(cache)
        xy = (n % 8 * 16, n // 8 * 16)
        assert xy[1] + 16 <= atlas.height
        atlas.paste(image, xy)
        cache[digest] = xy
    x, y = cache[digest]
    rules.append(f'[{scope}]<tile>35,{t:04X},{palette},{x},{y},1,N')
    metadata.append(dict(identity=f'{t:04X}', palette=palette, atlas=[x,y], kind=kind))

solid = [*range(0x350,0x35B), *range(0x369,0x36D), *range(0x381,0x389), *range(0x38F,0x397)]
for t in solid:
    x, y = (t & 1)*16, ((t >> 1) & 1)*16
    tile(t, '0F071737', gold.crop((x,y,x+16,y+16)), 'shared gold ceiling texture')

for t in range(0x397,0x39B):
    b = bytes.fromhex(patterns[f'{t:04X}'])
    mask = np.array([[255 if ((b[y] | b[y+8]) >> (7-x)) & 1 else 0
                      for x in range(8)] for y in range(8)], dtype=np.uint8)
    # Fill the rock above its native lower contour; retain every tooth edge.
    for x in range(8):
        ys = np.flatnonzero(mask[:,x])
        if len(ys):
            mask[:ys[-1]+1,x] = 255
    x, y = (t & 1)*16, ((t >> 1) & 1)*16
    cell = gold.crop((x,y,x+16,y+16))
    cell.putalpha(Image.fromarray(mask).resize((16,16), Image.Resampling.NEAREST))
    tile(t, '0F071737', cell, 'native ceiling lower contour')

# The red/ochre repeating wall motif is nonsolid scenery, as in screen 2-3.
for t in [0x300, 0x36E, 0x36F, *range(0x39B,0x3A1)]:
    tile(t, '0F061828', Image.new('RGBA',(16,16)), 'cave backdrop reveal')

backgrounds = []
guards = [(t, '0F071737') for t in [*range(0x32E,0x334), *range(0x350,0x35F),
                                               *range(0x381,0x389), *range(0x38F,0x39B)]]
guards += [(t, '0F061828') for t in range(0x39B,0x3A1)]
for i, (t,palette) in enumerate(guards):
    name = f's24Rendered{i}'
    conditions.append(f'<condition>{name},tileAtPosition,128,16,{t:04X},{palette}')
    background_scope = scope+'&s24WallPalette0&s24WallPalette1&s24WallPalette2'
    backgrounds.append(f'[{background_scope}&{name}]<background>Stage2_Cave_Background.png,1,1,1,11,0,0')

atlas.save(art / 'Stage2_Second_Cave_Tiles_2x.png')
atlas.save(pack / 'Stage2_Second_Cave_Tiles_2x.png')

def section(kind, lines):
    return '# BEGIN SCREEN2_4 '+kind+'\n'+'\n'.join(lines)+'\n# END SCREEN2_4 '+kind+'\n'

end = text.index('\n', text.rfind('<img>')) + 1
text = text[:end] + section('IMAGES',['<img>Stage2_Second_Cave_Tiles_2x.png']) + text[end:]
lines = text.splitlines(keepends=True)
first = next(i for i,line in enumerate(lines) if '<tile>' in line or '<background>' in line)
lines[first:first] = [section('CONDITIONS',conditions), section('MAPPINGS',aliases+rules+backgrounds)]
(pack/'hires.txt').write_text(''.join(lines))
(art/'registration.json').write_text(json.dumps(dict(scope=scope, shared_aliases=len(aliases),
    new_tile_rules=len(rules), atlas_cells=len(cache), mappings=metadata,
    background_rules=len(backgrounds), reused_background='Stage2_Cave_Background.png',
    new_painted_sources=0, native_collision_modified=False, previous_artwork_modified=False),indent=2)+'\n')
print('Stage 2 second horizontal cave:',len(aliases),'shared aliases,',len(rules),'new tile mappings')
