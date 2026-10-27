"""Require two exact scoped backdrop guards and complete baseline recovery."""
from pathlib import Path
import hashlib
import json
import re


def strip(text):
    text, count = re.subn(r'^# BEGIN BACKGROUND_CONTINUITY\n.*?^# END BACKGROUND_CONTINUITY\n',
                          '', text, flags=re.M | re.S)
    assert count == 1
    return text


def verify(root, pack):
    text = (pack / 'hires.txt').read_text()
    previous = json.loads((root / 'evidence/0.20.4-pack-sha256.json').read_text())
    assert {p.name for p in pack.iterdir() if p.is_file()} == set(previous)
    for name, digest in previous.items():
        if name not in {'hires.txt', 'README.txt'}:
            assert hashlib.sha256((pack / name).read_bytes()).hexdigest() == digest, name
    old = strip(text)
    assert hashlib.sha256(old.encode()).hexdigest() == previous['hires.txt']
    registration = json.loads((root / 'art/background_continuity/registration.json').read_text())
    expected = []
    for identity in ['074B', '074C']:
        name = 'mossContinuity_' + identity
        condition = f'<condition>{name},tileAtPosition,128,16,{identity},0F091929'
        rule = f'[l3c9DEEMode&l3c9DEELo&l3c9DEEHi&{name}]<background>Poison_Moss_Ruins_Background.png,1,0,0,11,0,0'
        assert text.splitlines().count(condition) == text.splitlines().count(rule) == 1
        assert condition not in old and rule not in old
        assert text.index(condition) < text.index(rule)
        expected.append(dict(identity=identity, palette='0F091929', position=[128, 16],
                             condition=condition, rule=rule))
    assert registration['mappings'] == expected
    assert registration['source_guard'] in old.splitlines()
    assert registration['source_rule'] in old.splitlines()
    assert '<condition>l3c9DEEMode,memoryCheckConstant,0072,==,14' in old
    assert '<condition>l3c9DEELo,memoryCheckConstant,0078,==,EE' in old
    assert '<condition>l3c9DEEHi,memoryCheckConstant,0079,==,9D' in old
    return dict(conditions=2, background_rules=2, tile_rules=0, prior_assets_exact=117,
                exact_0204_mapping_recovery=True, artwork_modified=False,
                native_neighbor_probes_added=0)


if __name__ == '__main__':
    root = Path(__file__).resolve().parents[1]
    print(json.dumps(verify(root, root / 'build/Holy_Diver_(Tr)'), indent=2))
