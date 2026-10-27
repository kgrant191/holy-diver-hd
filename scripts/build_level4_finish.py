"""Restore the boss portal and smooth the reported descending stair underside."""
from pathlib import Path
import hashlib, json, re
import numpy as np
from PIL import Image

r = Path(__file__).resolve().parents[1]
p = r / 'build/Holy_Diver_(Tr)'
a = r / 'art/level4_finish'
a.mkdir(exist_ok=True)
text = (p / 'hires.txt').read_text()
prior = json.loads((r / 'evidence/0.20.0-pack-sha256.json').read_text())
assert hashlib.sha256(text.encode()).hexdigest() == prior['hires.txt']
assert text.count('<img>') == 54
atlas = Image.new('RGBA', (128, 64))
old = np.array(Image.open(r / 'art/level4_stairs/descending_step.png').convert('RGBA'))
step = old.copy()
# The standing surface and upper half are unchanged. Replace coarse native
# cutouts and the dangling bottom pixel with one continuous lower diagonal.
for x in range(32):
    bottom = 19 + (12*x + 15)//31
    step[16:, x, 3] = 0
    step[16:bottom+1, x, 3] = 255
assert np.array_equal(step[:16], old[:16])
assert np.array_equal(step[:, :, :3], old[:, :, :3])
im = Image.fromarray(step)
im.save(a / 'descending_step.png')
atlas.paste(im, (0, 0))
rules, early, conditions, records = [], [], [], []
for line in text.splitlines():
    m = re.fullmatch(r'\[([^]]+)\]<tile>49,(0[BD]7[CDEF]),([^,]+),(\d+),(\d+),1,N', line)
    if not m:
        continue
    # Only replace rules already using the restored physical stair source.
    new = line.replace(']<tile>49,', ']<tile>54,')
    if new not in rules+early:
        (early if text.index(line) < text.index('# BEGIN TEMPLE_FINALE CONDITIONS') else rules).append(new)
        records.append(dict(kind='smooth descending step', source_rule=line, rule=new))
assert rules and len(early)==24

# The native boss doorway has a four-by-four ornamental crown followed by
# six rows of blank opening. Reuse the accepted entrance crown and its dark
# opening cell; do not reinstate the removed decorative foreground columns.
scope = json.loads((r / 'art/level4_finale/registration.json').read_text())['scopes']['AEF5']
source = json.loads((r / 'art/level4/registration.json').read_text())['mappings']
layout = [[0xbdf, 0xbe0, 0xbe1, 0xbe2], [0xb5b, 0xb5c, 0xb63, 0xb64],
          [0xb5d, 0xb5e, 0xb65, 0xb66], [0xb5f, 0xb60, 0xb67, 0xb68]]
portal = Image.new('RGBA', (64, 160))
original = Image.open(p / 'Golden_Temple_Tiles_2x.png').convert('RGBA')
for y, row in enumerate(layout):
    for x, tile in enumerate(row):
        src = next(m for m in source if int(m['tile'],16) == tile and m['kind'] == 'temple entrance facade')
        xx, yy = src['xy']
        portal.paste(original.crop((xx, yy, xx+16, yy+16)), (x*16, y*16))
        new = f'[{scope}]<tile>47,{tile+0x200:04X},0F172737,{xx},{yy},1,N'
        rules.append(new)
        records.append(dict(kind='boss entrance crown', source_rule=src['rule'], rule=new))
dark = next(m for m in source if m['kind'] == 'dark entrance')
xx, yy = dark['xy']
for row in range(6):
    distance = (row+1)*8
    bound = f'finishDoorY{row}'
    conditions.append(f'<condition>{bound},positionCheckY,>=,{distance}')
    for col, tile in enumerate(layout[-1]):
        name = f'finishDoorAbove{row}_{col}'
        conditions.append(f'<condition>{name},tileNearby,0,{-distance},{tile+0x200:04X},0F172737')
        for pal in ['0F172737', '0F071723']:
            new = f'[{scope}&{bound}&{name}]<tile>47,0D00,{pal},{xx},{yy},1,N'
            rules.append(new)
            records.append(dict(kind='boss entrance opening', row=row, column=col, rule=new))
        portal.paste(original.crop((xx, yy, xx+16, yy+16)), (col*16, 64+row*16))
portal.save(a / 'boss_portal.png')

def block(name, lines):
    return '# BEGIN TEMPLE_FINISH '+name+'\n'+'\n'.join(lines)+'\n# END TEMPLE_FINISH '+name+'\n'
end = text.index('\n', text.rfind('<img>'))+1
text = text[:end]+block('IMAGES', ['<img>Golden_Temple_Finish_2x.png'])+text[end:]
# Existing scopes must be declared first. This is immediately before the
# first finale tile replacement, ahead of all older shared scenery rules.
text = text.replace('# BEGIN TEMPLE_STAIRS MAPPINGS', block('EARLY_STAIRS', early)+'# BEGIN TEMPLE_STAIRS MAPPINGS')
mark = '# BEGIN TEMPLE_FINALE MAPPINGS'
text = text.replace(mark, block('CONDITIONS', conditions)+block('MAPPINGS', rules)+mark)
(p / 'hires.txt').write_text(text)
atlas.save(p / 'Golden_Temple_Finish_2x.png')
(a / 'registration.json').write_text(json.dumps(dict(mappings=records, tile_rules=len(rules)+len(early),
    conditions=len(conditions), stair_rules=sum(m['kind']=='smooth descending step' for m in records),
    portal_scope=scope, portal_layout=[[f'{t+0x200:04X}' for t in row] for row in layout],
    standing_surface_unchanged=True, prior_assets_unchanged=True, native_gameplay_modified=False), indent=2)+'\n')
print('Temple finishing repair:', len(rules)+len(early), 'tile rules;', len(conditions), 'bounded conditions')
