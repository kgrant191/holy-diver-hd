"""Reveal scenery behind the unmapped ornamental F8 tile in the dragon arena."""
from pathlib import Path
import hashlib,json
from PIL import Image
r=Path(__file__).resolve().parents[1];p=r/'build/Holy_Diver_(Tr)';f=p/'hires.txt';text=f.read_text()
prior=json.loads((r/'evidence/0.19.0-pack-sha256.json').read_text());assert hashlib.sha256(text.encode()).hexdigest()==prior['hires.txt']
images=[l[5:]for l in text.splitlines()if l.startswith('<img>')];assert images[50]=='Golden_Temple_Courtyard_2x.png'
assert Image.open(p/images[50]).convert('RGBA').crop((0,0,16,16)).getchannel('A').getbbox()is None
scope='staffArenaMode&staffArenaLo&staffArenaHi'
rules=[f'[{scope}]<tile>50,0DF8,{pal},0,0,1,N'for pal in ['0F073703','31073703']]
block='# BEGIN TEMPLE_RESIDUE MAPPINGS\n'+'\n'.join(rules)+'\n# END TEMPLE_RESIDUE MAPPINGS\n'
f.write_text(text.replace('# BEGIN TEMPLE_DRAGON MAPPINGS',block+'# BEGIN TEMPLE_DRAGON MAPPINGS'))
print('Arena residue: two scoped F8 mappings; existing transparent cell; no artwork changes')
