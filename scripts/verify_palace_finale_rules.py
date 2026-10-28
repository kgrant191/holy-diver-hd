"""Validate removable finale rules, unchanged assets and whole native sources."""
from pathlib import Path
import hashlib,json,re,tempfile,subprocess,sys,shutil
import numpy as np
from PIL import Image
NEW={'Demonic_Palace_Finale_2x.png','Demonic_Palace_Boss_Flash.png'}
def strip(text):
 for section in ['IMAGES','CONDITIONS','MAPPINGS','ALIASES']:
  text,n=re.subn(r'^# BEGIN PALACE_FINALE '+section+r'\n.*?^# END PALACE_FINALE '+section+r'\n','',text,flags=re.M|re.S);assert n==1
 return text
def verify(root,pack):
 previous=json.loads((root/'evidence/0.23.0-pack-sha256.json').read_text());text=(pack/'hires.txt').read_text();old=strip(text)
 assert hashlib.sha256(old.encode()).hexdigest()==previous['hires.txt']
 assert {p.name for p in pack.iterdir()if p.is_file()}==set(previous)|NEW
 for name,h in previous.items():
  if name not in ['hires.txt','README.txt']:assert hashlib.sha256((pack/name).read_bytes()).hexdigest()==h,name
 art=root/'art/level5_finale';reg=json.loads((art/'registration.json').read_text());patterns={int(k,16):bytes.fromhex(v)for k,v in json.loads((art/'native_patterns.json').read_text()).items()};ls=set(text.splitlines());oldls=set(old.splitlines())
 assert all(l in ls for l in reg['conditions']+reg['backgrounds'])
 olddefs={l[11:].split(',')[0]:l[11:].split(',')[1:]for l in oldls if l.startswith('<condition>')}
 # Only cloned sprite-neighbor dependencies; no new background probes.
 for l in reg['conditions']:
  d=l[11:].split(',')
  assert d[1]!='tileNearby',d
  if d[1]=='spriteNearby':
   identity=d[1:].copy();tile=int(identity[3],16)
   if 0x1400<=tile<=0x148d:identity[3]=f'{tile-0xa00:04X}'
   elif 0x1600<=tile<=0x168d:identity[3]=f'{tile-0xc00:04X}'
   assert any(v[:4]==identity[:4]for v in olddefs.values()),d
 assert len(reg['backgrounds'])==sum(map(len,reg['guard_palettes'].values()))*256
 assert len(reg['card_clones'])==61
 for e in reg['card_clones']:
  assert e['source_rule']in oldls and e['rule']in ls
  expected=e['source_rule'].replace('&cardRendering','&palaceFinaleStage6Rendered')
  if '&stageNumber6'not in expected:expected=expected.replace(']','&stageNumber6]',1)
  assert e['rule']==expected
 atlas=Image.open(pack/'Demonic_Palace_Finale_2x.png').convert('RGBA');assert atlas.size==(512,512)
 assert (pack/'Demonic_Palace_Finale_2x.png').read_bytes()==(art/'Demonic_Palace_Finale_2x.png').read_bytes()
 for e in reg['clones']:
  assert e['source_rule']in oldls and e['rule']in ls
  a=e['source_rule'].split('<tile>')[1].split(',');b=e['rule'].split('<tile>')[1].split(',');assert a[:1]==b[:1]and a[3:5]==b[3:5]and a[6:]==b[6:]
  assert patterns[int(a[1],16)]==patterns[int(b[1],16)],e
 mapping={}
 for e in reg['mappings']:
  assert e['rule']in ls;x,y=e['xy'];actual=atlas.crop((x,y,x+16,y+16));mapping[e['tile'],e['palette'],e['scope']]=actual
  if e['kind'].endswith('space')or e['kind']=='exit distant wall':assert not actual.getchannel('A').getbbox()
  if e['kind']in ['shaft structural stone','Level 6 native crimson rock']:
   b=patterns[int(e['tile'],16)];mask=np.array([[bool((b[y]|b[y+8])>>(7-x)&1)for x in range(8)]for y in range(8)])
   for yy in range(8):
    xs=np.flatnonzero(mask[yy])
    if len(xs):mask[yy,xs[0]:xs[-1]+1]=True
   for xx in range(8):
    ys=np.flatnonzero(mask[:,xx])
    if len(ys):mask[ys[0]:ys[-1]+1,xx]=True
   assert np.array_equal(np.array(actual.getchannel('A'))>0,np.repeat(np.repeat(mask,2,0),2,1)),e
 for name,layout in json.loads((art/'boss_layouts.json').read_text()).items():
  im=Image.open(art/(name+'.png')).convert('RGBA');mask=Image.new('L',im.size)
  for t,x,y in layout:
   part=im.crop((x*2,y*2,x*2+16,y*2+16));assert part.tobytes()==mapping[t,'FF052730',reg['scopes']['8E6A']].tobytes();mask.paste(255,(x*2,y*2,x*2+16,y*2+16))
  assert not ((np.array(im)[:,:,3]>0)&(np.array(mask)==0)).any()
 normal=np.array(Image.open(pack/'Demonic_Palace_Interior.png').convert('RGBA'));flash=np.array(Image.open(pack/'Demonic_Palace_Boss_Flash.png').convert('RGBA'));assert np.array_equal(flash[:,:,:3],(normal[:,:,:3]*.5).astype(np.uint8))and np.all(flash[:,:,3]==176)
 return dict(prior_assets_exact=len(previous)-2,exact_0230_mapping_recovery=True,whole_boss_sources_exact=True,native_terrain_masks_exact=True,background_rules=len(reg['backgrounds']),clone_rules=len(reg['clones']),new_background_neighbor_probes=0,new_files=sorted(NEW))
def legacy_projection(root,pack):
 previous=json.loads((root/'evidence/0.23.0-pack-sha256.json').read_text())
 with tempfile.TemporaryDirectory(prefix='palace-0230-')as directory:
  target=Path(directory)
  for name,h in previous.items():
   if name=='hires.txt':(target/name).write_text(strip((pack/name).read_text()))
   elif name=='README.txt':(target/name).write_bytes((root/'evidence/level5_finale/baseline_README.txt').read_bytes())
   else:shutil.copyfile(pack/name,target/name)
   assert hashlib.sha256((target/name).read_bytes()).hexdigest()==h,name
  subprocess.run([sys.executable,str(root/'scripts/validate_pack.py'),str(target)],check=True)
if __name__=='__main__':
 root=Path(__file__).resolve().parents[1];print(json.dumps(verify(root,root/'build/Holy_Diver_(Tr)'),indent=2))
