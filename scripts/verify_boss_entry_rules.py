"""Check exact recovery, complete boss coverage and unchanged installed assets."""
from pathlib import Path
import hashlib
import json
import re


def strip(text):
    text, count = re.subn(
        r'^# BEGIN BOSS_ENTRY_REPAIR MAPPINGS\n.*?^# END BOSS_ENTRY_REPAIR MAPPINGS\n',
        '', text, flags=re.M | re.S)
    assert count == 1
    return text


def verify(root, pack, content=None):
    text = content if content is not None else (pack / 'hires.txt').read_text()
    prior = json.loads((root / 'evidence/0.20.3-pack-sha256.json').read_text())
    assert {p.name for p in pack.iterdir() if p.is_file()} == set(prior)
    for name, digest in prior.items():
        if name not in {'hires.txt', 'README.txt'}:
            assert hashlib.sha256((pack / name).read_bytes()).hexdigest() == digest, name
    old = strip(text)
    assert hashlib.sha256(old.encode()).hexdigest() == prior['hires.txt']
    registration = json.loads((root / 'art/boss_entry_repair/registration.json').read_text())
    layout = json.loads((root / 'art/boss2/wall_layout.json').read_text())
    expected = {'0F271027': '0F270027', '0F271006': '0F270027', '0F020627': '0F121626'}
    assert registration['palettes'] == expected
    lines, old_lines = text.splitlines(), old.splitlines()
    for palette, source_palette in expected.items():
        cells = [m for m in registration['mappings'] if m['palette'] == palette]
        assert len(cells) == len(layout)
        assert {m['identity'] for m in cells} == set(layout)
        for cell in cells:
            rule, source = cell['rule'], cell['source_rule']
            assert rule.startswith('[b2Room&b2Lo&b2Hi]<tile>39,')
            assert cell['source_palette'] == source_palette
            assert rule == source.replace(',' + source_palette + ',', ',' + palette + ',')
            assert source in old_lines and lines.count(rule) == 1
            assert lines.index(rule) < lines.index(source)
    assert registration['tile_rules'] == len(layout) * 3
    return dict(tile_rules=len(layout) * 3, palettes=list(expected),
                prior_assets_exact=len(prior) - 2, exact_0203_mapping_recovery=True,
                artwork_modified=False, new_conditions=0)


if __name__ == '__main__':
    root = Path(__file__).resolve().parents[1]
    print(json.dumps(verify(root, root / 'build/Holy_Diver_(Tr)'), indent=2))
