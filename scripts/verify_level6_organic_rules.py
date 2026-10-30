"""Validate complete source registration and the exact removable 0.28.0 baseline."""
from pathlib import Path
import hashlib,json,re,tempfile,shutil,subprocess,sys
import numpy as np
from PIL import Image
from verify_level6_opening_rules import native_hull
NEW={'Final_Citadel_Organic_2x.png','Final_Citadel_Organic.png','Final_Citadel_Organic_Flash.png'}
def strip(text):
 for part in ['IMAGES','CONDITIONS','MAPPINGS']:
  text,n=re.subn(r'^# BEGIN LEVEL6_ORGANIC '+part+r'\n.*?^# END LEVEL6_ORGANIC '+part+r'\n','',text,flags=re.M|re.S);assert n==1
 return text
def verify(root,pack):
 prior=json.loads((root/'evidence/0.28.0-pack-sha256.json').read_text());text=(pack/'hires.txt').read_text();old=strip(text);assert hashlib.sha256(old.encode()).hexdigest()==prior['hires.txt']
 assert{p.name for p in pack.iterdir()if p.is_file()}==set(prior)|NEW
 for name,digest in prior.items():
  if name not in ['hires.txt','README.txt']:assert hashlib.sha256((pack/name).read_bytes()).hexdigest()==digest,name
 art=root/'art/level6_organic';reg=json.loads((art/'registration.json').read_text());lines=set(text.splitlines());oldlines=set(old.splitlines());defs={l[11:].split(',')[0]:l[11:].split(',')[1:]for l in reg['conditions']};olddefs={l[11:].split(',')[0]:l[11:].split(',')[1:]for l in oldlines if l.startswith('<condition>')}
 patterns={int(k,16):bytes.fromhex(v)for k,v in json.loads((root/'art/level6_opening/native_patterns.json').read_text()).items()}
 assert[defs[k]for k in reg['scope'].split('&')]==[['memoryCheckConstant','0072','==','10'],['memoryCheckConstant','0078','==','AF'],['memoryCheckConstant','0079','==','A3']]
 assert all(d[0]!='tileNearby'for d in defs.values());assert all(l in lines for l in reg['conditions']+reg['backgrounds'])
 atlas=Image.open(pack/'Final_Citadel_Organic_2x.png').convert('RGBA');assert atlas.size==(256,256);assert (pack/'Final_Citadel_Organic_2x.png').read_bytes()==(art/'Final_Citadel_Organic_2x.png').read_bytes()
 assert[l[5:]for l in text.splitlines()if l.startswith('<img>')][67]=='Final_Citadel_Organic_2x.png'
 cells={};masks=0
 for e in reg['mappings']:
  assert e['rule']in lines;t=int(e['tile'],16);x,y=e['xy'];cell=atlas.crop((x,y,x+16,y+16));cells.setdefault((t,e['palette']),cell)
  if e['kind']=='native organic terrain':assert np.array_equal(np.array(cell.getchannel('A'))>0,native_hull(patterns[t]));masks+=1
  elif e['kind']!='whole orb':assert not cell.getchannel('A').getbbox()
 for name,layout in reg['groups'].items():
  whole=Image.open(art/(name+'.png')).convert('RGBA')
  for y,row in enumerate(layout):
   for x,t in enumerate(row):
    if t is not None:assert whole.crop((x*16,y*16,x*16+16,y*16+16)).tobytes()==cells[t,'0F162638'].tobytes()
 for pose in reg['poses']:
  whole=Image.open(art/(pose['name']+'.png')).convert('RGBA');assert whole.size==(32,32)
  for y,row in enumerate(pose['layout']):
   for x,t in enumerate(row):assert whole.crop((x*16,y*16,x*16+16,y*16+16)).tobytes()==cells[t,'FF0A1930'].tobytes()
 kinds={}
 for e in reg['clones']:
  assert e['source_rule']in oldlines and e['rule']in lines;a=e['source_rule'].split('<tile>')[1].split(',');b=e['rule'].split('<tile>')[1].split(',');assert a[0]==b[0]and a[3:]==b[3:];assert patterns[int(a[1],16)]==patterns[int(b[1],16)];kinds[e['kind']]=kinds.get(e['kind'],0)+1
  oldhead=e['source_rule'].split(']')[0][1:].split('&')if e['source_rule'].startswith('[')else[];newhead=e['rule'].split(']')[0][1:].split('&')[3:]
  if e['kind']=='approved lava ice':oldhead=oldhead[3:];assert a[2][2:]==b[2][2:]
  elif e['kind']!='accepted 1-up':assert a[2]==b[2]
  if e['kind']in ['player HUD effects','approved lava ice']:
   assert len(oldhead)==len(newhead)
   for o,n in zip(oldhead,newhead):
    if o in ['hmirror','vmirror','bgpriority']:assert n==o;continue
    assert o.startswith('!')==n.startswith('!');d=olddefs[o.lstrip('!')].copy()
    if d[0]=='spriteNearby'and e['kind']=='player HUD effects'and 0xa00<=int(d[3],16)<=0xa8d:d[3]=f'{int(d[3],16)+0x1000:04X}'
    assert defs[n.lstrip('!')]==d
 expected={(t,phase+suffix)for t in range(0x1b00,0x1c00)for phase in ['0F','30','31']for suffix in reg['guard_palettes']}
 for line in reg['backgrounds']:
  h,f=line[1:].split(']<background>');terms=h.split('&');assert '&'.join(terms[:3])==reg['scope'];d=defs[terms[-1]];assert d[:3]==['tileAtPosition','128','16'];t,pal=int(d[3],16),d[4];expected.remove((t,pal));assert f=='Final_Citadel_Organic'+('_Flash'if pal[:2]!='0F'else'')+'.png,1,0,0,1,0,0'
 assert not expected and '0F0F0F'not in reg['guard_palettes']
 im=np.array(Image.open(pack/'Final_Citadel_Organic.png').convert('RGBA'));flash=np.array(Image.open(pack/'Final_Citadel_Organic_Flash.png').convert('RGBA'));assert im.shape==(480,512,4)and np.all(im[:,:,3]==255);assert np.array_equal(im[:,:,:3],flash[:,:,:3])and np.all(flash[:,:,3]==176)
 return dict(prior_assets_exact=len(prior)-2,exact_0280_mapping_recovery=True,native_terrain_masks=masks,whole_groups=list(reg['groups']),whole_orb_poses=2,clone_counts=kinds,background_guards=len(reg['backgrounds']),new_neighbor_probes=0)
def legacy_projection(root,pack):
 prior=json.loads((root/'evidence/0.28.0-pack-sha256.json').read_text())
 with tempfile.TemporaryDirectory(prefix='citadel-0280-')as directory:
  target=Path(directory)
  for name,digest in prior.items():
   if name=='hires.txt':(target/name).write_text(strip((pack/name).read_text()))
   elif name=='README.txt':(target/name).write_bytes((root/'evidence/level6_organic/baseline_README.txt').read_bytes())
   else:shutil.copyfile(pack/name,target/name)
   assert hashlib.sha256((target/name).read_bytes()).hexdigest()==digest,name
  subprocess.run([sys.executable,str(root/'scripts/validate_pack.py'),str(target)],check=True)
if __name__=='__main__':
 root=Path(__file__).resolve().parents[1];print(json.dumps(verify(root,root/'build/Holy_Diver_(Tr)'),indent=2))
