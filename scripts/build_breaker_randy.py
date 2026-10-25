"""Reuse every existing Randy pose during the Breaker room's native fade."""
from pathlib import Path
import json
import re

root = Path(__file__).resolve().parents[1]
pack = root / 'build/Holy_Diver_(Tr)'
text = (pack / 'hires.txt').read_text()
definitions = {line.split('>')[1].split(',')[0]: line
               for line in text.splitlines() if line.startswith('<condition>')}
source = text.split('# BEGIN BOSS2 ALIASES\n')[1].split('# END BOSS2 ALIASES')[0]
phases = {
    'FF300036': [('FF200F26', '.65'), ('FF100F16', '.30'), ('FF000F06', '.12')],
    'FF221136': [('FF120126', '.65'), ('FF020F16', '.30'), ('FF0F0F06', '.12')],
}
conditions, rules = {}, []
sources = 0
for line in source.splitlines():
    match = re.fullmatch(r'(?:\[([^]]+)\])?<tile>(.*)', line)
    if not match:
        continue
    scope, fields = match[1] or '', match[2].split(',')
    if fields[0] not in {'18', '19', '22'} or fields[2] not in phases:
        continue
    sources += 1
    for palette, brightness in phases[fields[2]]:
        terms = ['b2Room', 'b2Lo', 'b2Hi']
        for term in scope.split('&') if scope else []:
            name = term.lstrip('!')
            definition = definitions.get(name, '').split('>')[-1].split(',')
            if len(definition) > 1 and definition[1] == 'spriteNearby':
                assert definition[5] == fields[2]
                replacement = f'breakerFade_{palette}_{name}'
                definition[0], definition[5] = replacement, palette
                conditions[replacement] = '<condition>' + ','.join(definition)
                term = ('!' if term.startswith('!') else '') + replacement
            terms.append(term)
        result = fields.copy()
        result[2], result[5] = palette, brightness
        rules.append('[' + '&'.join(terms) + ']<tile>' + ','.join(result))

# Copy in source order: crouch/standing-leg/pose-specific rules precede fallback
# rules. Only palettes and brightness change; native CHR aliases and mirrors stay.
assert sources == 314 and len(rules) == 942
block = '# BEGIN BREAKER_RANDY\n' + '\n'.join([*conditions.values(), *rules]) + '\n# END BREAKER_RANDY\n'
marker = '# BEGIN BOSS2_REVIEW\n'
assert text.count(marker) == 1
(pack / 'hires.txt').write_text(text.replace(marker, block + marker))
out = root / 'art/breaker_randy'
out.mkdir(exist_ok=True)
(out / 'registration.json').write_text(json.dumps(dict(
    source_rules=sources, tile_rules=len(rules), conditions=len(conditions),
    palette_phases=phases, source_atlases=['Randy_Entrance_2x.png',
    'Randy_Equipped_2x.png', 'Randy_Upward_2x.png'], new_artwork=False,
    scope='b2Room&b2Lo&b2Hi', pose_order_preserved=True), indent=2) + '\n')
print(f'Breaker Randy: {len(rules)} fade aliases; all existing artwork unchanged.')
