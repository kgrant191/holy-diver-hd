"""Restore the original brown ceiling by reusing its exact existing atlas cells."""
from pathlib import Path
import json

root = Path(__file__).resolve().parents[1]
pack = root / 'build/Holy_Diver_(Tr)'
# Builds may reuse the output directory from the rejected 0.8.2 candidate.
(pack / 'Stage2_Crimson_Ceiling_2x.png').unlink(missing_ok=True)
text = (pack / 'hires.txt').read_text()
images = [line[5:] for line in text.splitlines() if line.startswith('<img>')]
assert len(images) == 38
geometry = json.loads((root / 'art/screen2_5_roof/previous_geometry.json').read_text())
assert len(geometry) == 46
rules = []
for identity, source in sorted(geometry.items()):
    x, y = source['xy']
    index = images.index(source['image'])
    rules.append(f'[s25Room&s25DataLo&s25DataHi]<tile>{index},{identity},0F071737,{x},{y},1,N')
block = '# BEGIN SCREEN2_5_BROWN_ROOF\n' + '\n'.join(rules) + '\n# END SCREEN2_5_BROWN_ROOF\n'
lines = text.splitlines(keepends=True)
first = next(i for i, line in enumerate(lines) if '<tile>' in line or '<background>' in line)
lines.insert(first, block)
(pack / 'hires.txt').write_text(''.join(lines))
print('Original brown ceiling: 46 exact original cell references; no new or modified artwork.')
