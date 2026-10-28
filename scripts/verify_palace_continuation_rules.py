"""Validate exact baseline recovery, native geometry and complete flash aliases."""
from pathlib import Path
import hashlib,json,re,tempfile,subprocess,sys,shutil
import numpy as np
from PIL import Image
NEW='Demonic_Palace_Continuation_2x.png'
def strip(text):
 for section in ['IMAGES','CONDITIONS','MAPPINGS']:
  text,n=re.subn(r'^# BEGIN PALACE_CONTINUATION '+section+r'\n.*?^# END PALACE_CONTINUATION '+section+r'\n','',text,flags=re.M|re.S);assert n==1
 return text
def verify(root,pack):
 previous=json.loads((root/'evidence/0.22.2-pack-sha256.json').read_text());text=(pack/'hires.txt').read_text();old=strip(text)
 assert hashlib.sha256(old.encode()).hexdigest()==previous['hires.txt']
 assert {p.name for p in pack.iterdir()if p.is_file()}==set(previous)|{NEW}
 for name,h in previous.items():
  if name not in ['hires.txt','README.txt']:assert hashlib.sha256((pack/name).read_bytes()).hexdigest()==h,name
 art=root/'art/level5_continuation';reg=json.loads((art/'registration.json').read_text());patterns={int(k,16):bytes.fromhex(v)for k,v in json.loads((art/'native_patterns.json').read_text()).items()}
 ls=set(text.splitlines());prior_ls=set(old.splitlines());assert all(l in ls for l in reg['conditions']+reg['backgrounds'])
 assert not any('Nearby'in l for l in reg['conditions'])
 assert len(reg['backgrounds'])==sum(map(len,reg['guard_palettes'].values()))*512
 for room,pals in reg['guard_palettes'].items():
  for pal in pals:
   for base in [0x1100,0x1300]:
    for t in range(base,base+256):
     name=f'palaceContinueView{room}_{t:04X}_{pal}'
     assert f'<condition>{name},tileAtPosition,128,16,{t:04X},{pal}'in ls
     assert f'[{reg["scopes"][room]}&{name}]<background>Demonic_Palace_Interior.png,1,0,0,1,0,0'in ls
 atlas=Image.open(pack/NEW).convert('RGBA');assert atlas.size==(256,256)and (pack/NEW).read_bytes()==(art/NEW).read_bytes()
 for e in reg['mappings']:
  assert e['rule']in ls and e['scope']in reg['scopes'].values();t=int(e['tile'],16);x,y=e['xy'];actual=np.array(atlas.crop((x,y,x+16,y+16)))[:,:,3]
  if e['kind']=='distant palace wall':assert not actual.any();continue
  b=patterns[t];mask=np.array([[bool((b[y]|b[y+8])>>(7-x)&1)for x in range(8)]for y in range(8)])
  for yy in range(8):
   xs=np.flatnonzero(mask[yy])
   if len(xs):mask[yy,xs[0]:xs[-1]+1]=True
  for xx in range(8):
   ys=np.flatnonzero(mask[:,xx])
   if len(ys):mask[ys[0]:ys[-1]+1,xx]=True
  assert np.array_equal(actual>0,np.repeat(np.repeat(mask,2,0),2,1)),e
 for e in reg['clones']:
  assert e['source_rule']in prior_ls and e['rule']in ls
  a=e['source_rule'].split('<tile>')[1].split(',');b=e['rule'].split('<tile>')[1].split(',');assert a[0]==b[0]and a[3:]==b[3:]
  if e['kind'].startswith('byte-identical')or e['kind'].startswith('existing visible'):assert patterns[int(a[1],16)]==patterns[int(b[1],16)]
 defs={l[11:].split(',')[0]:l[11:].split(',')for l in reg['conditions']}
 for e in reg['flash']:
  assert e['rule']in ls and e['source_rule']in ls
  kind=e['kind'];a=e['source_rule'].split(']')[1].split('>')[1].split(',');b=e['rule'].split(']')[1].split('>')[1].split(',')
  if kind=='tile':assert b[2]==e['phase']+a[2][2:]and a[:2]==b[:2]and a[3:]==b[3:]
  else:assert a[0]=='Demonic_Palace_Interior.png'and b[0]=='Demonic_Palace_Interior_Flash.png'and a[1:]==b[1:]
  before=e['source_rule'][1:].split(']')[0].split('&');after=e['rule'][1:].split(']')[0].split('&');assert len(before)==len(after)
  for src,dst in zip(before,after):
   if src in ['hmirror','vmirror','bgpriority']:assert src==dst;continue
   a=defs[src.lstrip('!')][1:];b=defs[dst.lstrip('!')][1:];expect=a.copy()
   if expect[0]in ['tileNearby','tileAtPosition']and expect[4].startswith('0F'):expect[4]=e['phase']+expect[4][2:]
   assert expect==b
 return dict(prior_assets_exact=124,exact_0222_mapping_recovery=True,native_terrain_and_lift_masks_exact=True,normal_background_rules=len(reg['backgrounds']),flash_rules=len(reg['flash']),source_reuse_aliases=len(reg['clones']),new_neighbor_probes=0,new_files=[NEW])
def legacy_projection(root,pack):
 previous=json.loads((root/'evidence/0.22.2-pack-sha256.json').read_text())
 with tempfile.TemporaryDirectory(prefix='palace-0222-')as directory:
  target=Path(directory)
  for name,h in previous.items():
   if name=='hires.txt':(target/name).write_text(strip((pack/name).read_text()))
   elif name=='README.txt':(target/name).write_bytes((root/'evidence/level5_continuation/baseline_README.txt').read_bytes())
   else:shutil.copyfile(pack/name,target/name)
   assert hashlib.sha256((target/name).read_bytes()).hexdigest()==h,name
  subprocess.run([sys.executable,str(root/'scripts/validate_pack.py'),str(target)],check=True)
if __name__=='__main__':
 root=Path(__file__).resolve().parents[1];print(json.dumps(verify(root,root/'build/Holy_Diver_(Tr)'),indent=2))
