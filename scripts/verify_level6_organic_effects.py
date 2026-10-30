"""Check exact accepted lava, ice and projectile source pixels in the new room."""
from pathlib import Path
import argparse,json,tempfile
import numpy as np
from PIL import Image
from verify_level6_opening_replay import source,matches
p=argparse.ArgumentParser();p.add_argument('--capture',required=True);p.add_argument('--out',required=True);a=p.parse_args();root=Path(__file__).resolve().parents[1];cap=Path(a.capture);pack=cap/'mesen_home/HdPacks/Holy_Diver_(Tr)';images=[l[5:]for l in(pack/'hires.txt').read_text().splitlines()if l.startswith('<img>')];reg=json.loads((root/'art/level6_organic/registration.json').read_text());entries={};atlases={}
for e in reg['clones']:
 if e['kind']in ['approved lava ice','returning projectile']:
  f=e['rule'].split('<tile>')[1].split(',');entries[int(f[1],16),f[2]]=f
def cell(t,pal):
 f=entries[t,pal];i,x,y=int(f[0]),int(f[3]),int(f[4])
 if i not in atlases:atlases[i]=Image.open(pack/images[i]).convert('RGBA')
 return atlases[i].crop((x,y,x+16,y+16))
hits={}
with tempfile.TemporaryDirectory()as tmp:
 sources={}
 for name,pal in [('lava_a','0F060616'),('lava_b','0F161606'),('Blizzard_ice','0F122131')]:
  im=Image.new('RGBA',(32,48))
  for i,t in enumerate(range(0x1b6f,0x1b75)):im.paste(cell(t,pal),(i%2*16,i//2*16))
  path=Path(tmp)/(name+'.png');im.save(path);sources[name]=source(path)
 path=Path(tmp)/'shot.png';cell(0x1acd,'FF301116').save(path);sources['wall_projectile']=source(path)
 for n in range(220,4050,4):
  im=np.array(Image.open(cap/'frames'/f'{n:06}.png').convert('RGB'))
  for name,item in sources.items():
   if name in hits:continue
   found=matches(im,item)
   if found:hits[name]=dict(frame=n,positions=found)
  if len(hits)==len(sources):break
assert set(hits)==set(sources),set(sources)-set(hits)
Path(a.out).write_text(json.dumps(dict(actual_complete_source_matches=hits),indent=2)+'\n');print('Accepted whole source matches:',sorted(hits))
