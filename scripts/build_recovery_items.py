"""Register large HP/Magic flasks to their identical native CHR copies."""
from pathlib import Path
import hashlib
import json
import re
from PIL import Image

root = Path(__file__).resolve().parents[1]
art = root / 'art/pickups'
pack = root / 'build/Holy_Diver_(Tr)'
text = (pack / 'hires.txt').read_text()
assert text.count('<img>') == 31
atlas = Image.new('RGBA', (32, 32))
items = []
rules = []
# The ROM contains sixteen byte-identical copies of each native flask tile.
# Exact CHR identity plus the native pickup palette avoids room-specific scope.
patterns = {'49': '000000007e3c3c3c0000000000001818',
            '4A': '3c7afdfdfdb9423c18387c7c7c380000',
            '4B': '000000007e3c24240000000000001818',
            '4C': '42818181818181ff3c7c7c7c7c7c4000'}
for i, (name, top) in enumerate([('hp', 0x49), ('magic', 0x4b)]):
    source = root / f'art/generated/{name}_flask_generated.png'
    im = Image.open(source).convert('RGBA')
    bounds = im.getchannel('A').point(lambda v: 255 if v >= 128 else 0).getbbox()
    # Four transparent native rows above each bottle stay transparent. The
    # whole generated shape fits below them and ends at the native base.
    scaled = im.crop(bounds).resize((14, 24), Image.Resampling.LANCZOS)
    alpha = scaled.getchannel('A').point(lambda v: 255 if v >= 128 else 0)
    scaled = scaled.convert('RGB').quantize(colors=32).convert('RGBA')
    scaled.putalpha(alpha)
    sprite = Image.new('RGBA', (16, 32))
    sprite.paste(scaled, (1, 8))
    sprite.save(art / f'{name}_flask.png')
    atlas.paste(sprite, (i * 16, 0))
    aliases = []
    for bank in range(0, 0x2000, 0x200):
        pair = [f'{bank + top:04X}', f'{bank + top + 1:04X}']
        aliases.append(pair)
        for row, identity in enumerate(pair):
            assert not re.search(r'<tile>\d+,0*' + identity.lstrip('0') + r',FF301116,', text)
            rules.append(f'<tile>31,{identity},FF301116,{i * 16},{row * 16},1,N')
    items.append({'name': name, 'source': str(source.relative_to(root)),
                  'source_sha256': hashlib.sha256(source.read_bytes()).hexdigest(),
                  'source_crop': list(bounds), 'target_rectangle': [1, 8, 15, 32],
                  'native_tiles': [f'{top:02X}', f'{top+1:02X}'],
                  'palette': 'FF301116', 'identical_chr_aliases': aliases})
atlas.save(art / 'Recovery_Items_2x.png')
atlas.save(pack / 'Recovery_Items_2x.png')
last = text.rfind('<img>')
end = text.index('\n', last) + 1
text = text[:end] + '# BEGIN RECOVERY_ITEMS IMAGES\n<img>Recovery_Items_2x.png\n# END RECOVERY_ITEMS IMAGES\n' + text[end:]
text += '# BEGIN RECOVERY_ITEMS MAPPINGS\n' + '\n'.join(rules) + '\n# END RECOVERY_ITEMS MAPPINGS\n'
(pack / 'hires.txt').write_text(text)
(art / 'registration.json').write_text(json.dumps({
    'items': items, 'native_chr_patterns': patterns, 'tile_rules': len(rules),
    'atlas_index': 31, 'native_geometry_changed': False,
    'existing_rules_modified': False, 'later_bank_live_coverage': 'Base-bank pickups tested in supplied chapel/tree states; matching copies are mapped but not all live-tested.'
}, indent=2) + '\n')
print('Recovery flasks: 64 shared CHR mappings; existing assets and rules preserved.')
