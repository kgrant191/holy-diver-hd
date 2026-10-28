"""Require an exact recoverable baseline and complete scoped Palace coverage."""
from pathlib import Path
import hashlib,json,re,tempfile,subprocess,sys,shutil
import numpy as np
from PIL import Image
NEW='Demonic_Palace_Next_2x.png'
def strip(text):
 for section in ['IMAGES','CONDITIONS','MAPPINGS','ALIASES']:
  text,n=re.subn(r'^# BEGIN PALACE_NEXT '+section+r'\n.*?^# END PALACE_NEXT '+section+r'\n','',text,flags=re.M|re.S);assert n==1
 return text
def verify(root,pack):
 previous=json.loads((root/'evidence/0.21.1-pack-sha256.json').read_text());text=(pack/'hires.txt').read_text();old=strip(text)
 assert hashlib.sha256(old.encode()).hexdigest()==previous['hires.txt'];assert {p.name for p in pack.iterdir()if p.is_file()}==set(previous)|{NEW}
 for name,h in previous.items():
  if name not in {'hires.txt','README.txt'}:assert hashlib.sha256((pack/name).read_bytes()).hexdigest()==h,name
 art=root/'art/level5_next';reg=json.loads((art/'registration.json').read_text());patterns={int(k,16):bytes.fromhex(v)for k,v in json.loads((art/'native_patterns.json').read_text()).items()}
 all_lines=set(text.splitlines());old_lines=set(old.splitlines());assert all(l in all_lines for l in reg['conditions']+reg['backgrounds'])
 assert not any('tileNearby'in l for l in reg['conditions']);assert len(reg['backgrounds'])==7168
 for room in ['888E','897E','8A6E']:
  palettes=['0F0F0717','0F001030']if room=='888E'else ['0F071727','0F040F24','0F060616','0F161606','0F122131']
  if room=='897E':palettes+=['0F0F0717','0F001030']
  for palette in palettes:
   for base in [0x1100,0x1300]:
    for t in range(base,base+256):
     name=f'palaceNextView{room}_{t:04X}_{palette}'
     assert f'<condition>{name},tileAtPosition,128,16,{t:04X},{palette}'in all_lines
     assert f'[{reg["scopes"][room]}&{name}]<background>Demonic_Palace_Interior.png,1,0,0,1,0,0'in all_lines
 atlas=Image.open(pack/NEW).convert('RGBA');assert atlas.size==(256,256);assert (pack/NEW).read_bytes()==(art/NEW).read_bytes()
 mappings={m['tile']:m for m in reg['mappings']if m['kind']=='rising armored sentry'};whole=Image.open(art/'sentry.png').convert('RGBA')
 union=np.zeros((112,64),bool)
 for key,x,y in json.loads((art/'sentry_layout.json').read_text()):
  m=mappings[key];sx,sy=m['xy'];assert atlas.crop((sx,sy,sx+16,sy+16)).tobytes()==whole.crop((x,y,x+16,y+16)).tobytes();union[y:y+16,x:x+16]=True
 assert not ((np.array(whole)[:,:,3]>0)&~union).any()
 for m in reg['mappings']:
  assert m['rule']in all_lines
  assert m['scope']in reg['scopes'].values()
  if m['kind']=='native stair stone':
   t=int(m['tile'],16);b=patterns[t];alpha=np.array([[bool((b[y]|b[y+8])>>(7-x)&1)for x in range(8)]for y in range(8)])
   for y in range(8):
    xs=np.flatnonzero(alpha[y])
    if len(xs):alpha[y,xs[0]:xs[-1]+1]=True
   for x in range(8):
    ys=np.flatnonzero(alpha[:,x])
    if len(ys):alpha[ys[0]:ys[-1]+1,x]=True
   sx,sy=m['xy'];actual=np.array(atlas.crop((sx,sy,sx+16,sy+16)))[:,:,3]>0
   assert np.array_equal(actual,np.repeat(np.repeat(alpha,2,0),2,1))
 for entry in reg['clones']:
  assert entry['source_rule']in old_lines and entry['rule']in all_lines
  f=entry['source_rule'].split('<tile>')[1].split(',');g=entry['rule'].split('<tile>')[1].split(',')
  assert f[0]==g[0]and f[3:]==g[3:]
  if entry['kind'].startswith('native byte alias:')or entry['kind']=='exact player HUD and shared effects':assert patterns[int(f[1],16)]==patterns[int(g[1],16)]
 return dict(prior_assets_exact=121,exact_0211_mapping_recovery=True,complete_background_guards=7168,new_neighbor_probes=0,whole_sentry_source_exact=True,native_stair_masks_exact=True,existing_source_aliases=len(reg['clones']),new_files=[NEW])
def legacy_projection(root,pack):
 previous=json.loads((root/'evidence/0.21.1-pack-sha256.json').read_text())
 with tempfile.TemporaryDirectory(prefix='palace-0211-')as directory:
  target=Path(directory)
  for name,h in previous.items():
   if name=='hires.txt':(target/name).write_text(strip((pack/name).read_text()))
   elif name=='README.txt':(target/name).write_bytes((root/'evidence/level5_next/baseline_README.txt').read_bytes())
   else:shutil.copyfile(pack/name,target/name)
   assert hashlib.sha256((target/name).read_bytes()).hexdigest()==h,name
  subprocess.run([sys.executable,str(root/'scripts/validate_pack.py'),str(target)],check=True)
if __name__=='__main__':
 root=Path(__file__).resolve().parents[1];print(json.dumps(verify(root,root/'build/Holy_Diver_(Tr)'),indent=2))
