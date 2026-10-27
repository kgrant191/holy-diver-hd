"""Reuse approved wall-boss artwork for three entrance-only native palettes."""
from pathlib import Path
import hashlib
import json

ROOT = Path(__file__).resolve().parents[1]
PACK = ROOT / 'build/Holy_Diver_(Tr)'
SCOPE = 'b2Room&b2Lo&b2Hi'
PALETTES = {
    '0F271027': '0F270027',  # warm entrance flash -> approved gold hit artwork
    '0F271006': '0F270027',
    '0F020627': '0F121626',  # colored entrance phase -> approved normal artwork
}


def build():
    text = (PACK / 'hires.txt').read_text()
    prior = json.loads((ROOT / 'evidence/0.20.3-pack-sha256.json').read_text())
    assert hashlib.sha256(text.encode()).hexdigest() == prior['hires.txt']
    layout = json.loads((ROOT / 'art/boss2/wall_layout.json').read_text())
    source = json.loads((ROOT / 'art/boss2/registration.json').read_text())
    records = []
    for palette, source_palette in PALETTES.items():
        cells = [m for m in source['mappings']
                 if m['palette'] == source_palette
                 and m['kind'] == 'wall boss / native palette phase']
        assert {m['identity'] for m in cells} == set(layout)
        for cell in cells:
            identity = cell['identity']
            x, y = cell['xy']
            original = f'[{SCOPE}]<tile>39,{identity},{source_palette},{x},{y},1,N'
            assert original in text.splitlines()
            rule = original.replace(',' + source_palette + ',', ',' + palette + ',')
            assert rule not in text
            records.append(dict(identity=identity, palette=palette,
                                source_palette=source_palette, source_rule=original,
                                rule=rule, xy=[x, y]))
    block = '# BEGIN BOSS_ENTRY_REPAIR MAPPINGS\n' + '\n'.join(
        m['rule'] for m in records) + '\n# END BOSS_ENTRY_REPAIR MAPPINGS\n'
    marker = '# BEGIN BOSS2_REVIEW\n'
    assert text.count(marker) == 1
    (PACK / 'hires.txt').write_text(text.replace(marker, block + marker))
    art = ROOT / 'art/boss_entry_repair'
    art.mkdir(exist_ok=True)
    (art / 'registration.json').write_text(json.dumps(dict(
        room='8F7D', mode='08', palettes=PALETTES, tile_rules=len(records),
        new_artwork=False, new_conditions=False, native_gameplay_modified=False,
        mappings=records), indent=2) + '\n')
    print(f'Boss entrance: {len(records)} aliases; every approved atlas unchanged.')


if __name__ == '__main__':
    build()
