"""Complete the existing rendered backdrop guards in the moss lava corridor."""
from pathlib import Path
import hashlib
import json

ROOT = Path(__file__).resolve().parents[1]
PACK = ROOT / 'build/Holy_Diver_(Tr)'
SCOPE = 'l3c9DEEMode&l3c9DEELo&l3c9DEEHi'
BACKGROUND = 'Poison_Moss_Ruins_Background.png,1,0,0,11,0,0'


def build():
    text = (PACK / 'hires.txt').read_text()
    previous = json.loads((ROOT / 'evidence/0.20.4-pack-sha256.json').read_text())
    assert hashlib.sha256(text.encode()).hexdigest() == previous['hires.txt']
    # The original guard family ends at 074A. The movie also renders 074B/C
    # beneath the same probe as the camera moves, with the same native palette.
    old_guard = '<condition>l3c9DEEView0_074A,tileAtPosition,128,16,074A,0F091929'
    old_rule = f'[{SCOPE}&l3c9DEEView0_074A]<background>{BACKGROUND}'
    assert old_guard in text.splitlines() and old_rule in text.splitlines()
    conditions, rules, records = [], [], []
    for identity in ['074B', '074C']:
        name = 'mossContinuity_' + identity
        condition = f'<condition>{name},tileAtPosition,128,16,{identity},0F091929'
        rule = f'[{SCOPE}&{name}]<background>{BACKGROUND}'
        conditions.append(condition)
        rules.append(rule)
        records.append(dict(identity=identity, palette='0F091929', position=[128, 16],
                            condition=condition, rule=rule))
    block = '# BEGIN BACKGROUND_CONTINUITY\n' + '\n'.join(conditions + rules) + '\n# END BACKGROUND_CONTINUITY\n'
    marker = '# BEGIN LEVEL3_CAVES MAPPINGS\n'
    assert text.count(marker) == 1
    (PACK / 'hires.txt').write_text(text.replace(marker, block + marker))
    art = ROOT / 'art/background_continuity'
    art.mkdir(exist_ok=True)
    (art / 'registration.json').write_text(json.dumps(dict(
        room='9DEE', mode='14', conditions=2, background_rules=2, tile_rules=0,
        source_guard=old_guard, source_rule=old_rule, mappings=records,
        artwork_modified=False, native_gameplay_modified=False), indent=2) + '\n')
    print('Background continuity: two missing ceiling guards; all artwork unchanged.')


if __name__ == '__main__':
    build()
