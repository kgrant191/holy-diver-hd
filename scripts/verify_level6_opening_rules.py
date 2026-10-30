"""Prove the Level 6 layer is removable and preserves native terrain boundaries."""
from pathlib import Path
import hashlib,json,re,tempfile,subprocess,sys,shutil
import numpy as np
from PIL import Image

NEW={'Final_Citadel_Tiles_2x.png','Final_Citadel_Exterior.png',
     'Final_Citadel_Interior.png','Final_Citadel_Exterior_Flash.png',
     'Final_Citadel_Interior_Flash.png'}

def strip(text):
 for section in ['IMAGES','CONDITIONS','MAPPINGS']:
  text,n=re.subn(r'^# BEGIN LEVEL6_OPENING '+section+r'\n.*?^# END LEVEL6_OPENING '+section+r'\n','',text,flags=re.M|re.S)
  assert n==1
 return text

def native_hull(pattern):
 a=np.array([[bool((pattern[y]|pattern[y+8])>>(7-x)&1)for x in range(8)]for y in range(8)])
 for y in range(8):
  xs=np.flatnonzero(a[y])
  if len(xs):a[y,xs[0]:xs[-1]+1]=True
 for x in range(8):
  ys=np.flatnonzero(a[:,x])
  if len(ys):a[ys[0]:ys[-1]+1,x]=True
 return np.repeat(np.repeat(a,2,0),2,1)

def verify(root,pack):
 previous=json.loads((root/'evidence/0.24.0-pack-sha256.json').read_text())
 text=(pack/'hires.txt').read_text();old=strip(text);lines=set(text.splitlines());oldlines=set(old.splitlines())
 assert hashlib.sha256(old.encode()).hexdigest()==previous['hires.txt']
 assert {p.name for p in pack.iterdir()if p.is_file()}==set(previous)|NEW
 for name,digest in previous.items():
  if name not in ['hires.txt','README.txt']:assert hashlib.sha256((pack/name).read_bytes()).hexdigest()==digest,name
 art=root/'art/level6_opening';reg=json.loads((art/'registration.json').read_text())
 patterns={int(k,16):bytes.fromhex(v)for k,v in json.loads((art/'native_patterns.json').read_text()).items()}
 assert all(l in lines for l in reg['conditions']+reg['backgrounds'])
 defs={l[11:].split(',')[0]:l[11:].split(',')[1:]for l in reg['conditions']}
 olddefs={l[11:].split(',')[0]:l[11:].split(',')[1:]for l in oldlines if l.startswith('<condition>')}
 assert all(d[0]!='tileNearby'for d in defs.values())
 for name,d in defs.items():
  if name.startswith('citadelReuse'):assert d in olddefs.values(),(name,d)
 assert len(reg['backgrounds'])==3*3*256*len(reg['guard_palettes'])==23040
 for room,mode in [('9A8B','04'),('9BB7','10'),('9CA7','0C')]:
  scope=reg['scopes'][room];terms=scope.split('&')
  assert [defs[n]for n in terms]==[['memoryCheckConstant','0072','==',mode],['memoryCheckConstant','0078','==',room[2:]],['memoryCheckConstant','0079','==',room[:2]]]
 atlas=Image.open(pack/'Final_Citadel_Tiles_2x.png').convert('RGBA');assert atlas.size==(512,256)
 assert (pack/'Final_Citadel_Tiles_2x.png').read_bytes()==(art/'Final_Citadel_Tiles_2x.png').read_bytes()
 mapping={};hulls=0
 for e in reg['mappings']:
  assert e['rule']in lines
  x,y=e['xy'];cell=atlas.crop((x,y,x+16,y+16));mapping[e['tile'],e['palette'],e['scope']]=cell
  if e['kind']in ['empty native space','distant wall']:assert not cell.getchannel('A').getbbox()
  elif e['kind']in ['native structural stone','whole skull block']:
   assert np.array_equal(np.array(cell.getchannel('A'))>0,native_hull(patterns[int(e['tile'],16)])),e
   hulls+=1
  elif e['kind']=='cape menu':
   terms=e['scope'].split('&');assert len(terms)==5
   assert [defs[n][0]for n in terms[-2:]]==['originPositionCheckX','originPositionCheckY']
  else:raise AssertionError(e['kind'])
 for name,layout in reg['groups'].items():
  im=Image.open(art/(name+'.png')).convert('RGBA');pal='0F081030'if name=='skull'else'0F061636'
  for y,row in enumerate(layout):
   for x,t in enumerate(row):assert im.crop((x*16,y*16,x*16+16,y*16+16)).tobytes()==mapping[f'{t:04X}',pal,reg['scopes']['9A8B']].tobytes()
 cape=Image.open(art/'cape_menu.png').convert('RGBA');assert cape.size==(32,32)
 for y,row in enumerate([[0x955,0x954],[0x952,0x951]]):
  for x,t in enumerate(row):
   entries=[e for e in reg['mappings']if e['kind']=='cape menu'and int(e['tile'],16)==t];assert len(entries)==1
   e=entries[0];assert cape.crop((x*16,y*16,x*16+16,y*16+16)).tobytes()==mapping[e['tile'],e['palette'],e['scope']].tobytes()
   terms=e['scope'].split('&');assert defs[terms[-2]][1:]==['==',str(72+x*8)]and defs[terms[-1]][1:]==['==',str(104+y*8)]
 for e in reg['clones']:
  assert e['source_rule']in oldlines and e['rule']in lines
  a=e['source_rule'].split('<tile>')[1].split(',');b=e['rule'].split('<tile>')[1].split(',')
  assert a[0]==b[0]and a[3:]==b[3:]
  assert patterns[int(a[1],16)]==patterns[int(b[1],16)],e
  head=e['rule'].split(']')[0][1:].split('&');assert '&'.join(head[:3])in reg['scopes'].values()
  if e['kind']=='approved lava and ice':
   original=e['source_rule'].split(']')[0][1:].split('&')[3:]
   assert [defs[n.lstrip('!')]for n in head[3:]]==[olddefs[n.lstrip('!')]for n in original]
   assert [n.startswith('!')for n in head[3:]]==[n.startswith('!')for n in original]
 for style in ['Exterior','Interior']:
  normal=np.array(Image.open(pack/f'Final_Citadel_{style}.png').convert('RGBA'))
  flash=np.array(Image.open(pack/f'Final_Citadel_{style}_Flash.png').convert('RGBA'))
  assert normal.shape==(480,512,4)and np.all(normal[:,:,3]==255)
  assert np.array_equal(flash[:,:,:3],normal[:,:,:3])and np.all(flash[:,:,3]==176)
 return dict(prior_assets_exact=len(previous)-2,exact_0240_mapping_recovery=True,
  native_terrain_masks_exact=hulls,whole_stone_skull_and_cape_sources_exact=True,
  background_rules=len(reg['backgrounds']),clone_rules=len(reg['clones']),
  new_background_neighbor_probes=0,new_files=sorted(NEW))

def legacy_projection(root,pack):
 previous=json.loads((root/'evidence/0.24.0-pack-sha256.json').read_text())
 with tempfile.TemporaryDirectory(prefix='citadel-0240-')as directory:
  target=Path(directory)
  for name,digest in previous.items():
   if name=='hires.txt':(target/name).write_text(strip((pack/name).read_text()))
   elif name=='README.txt':(target/name).write_bytes((root/'evidence/level6_opening/baseline_README.txt').read_bytes())
   else:shutil.copyfile(pack/name,target/name)
   assert hashlib.sha256((target/name).read_bytes()).hexdigest()==digest,name
  subprocess.run([sys.executable,str(root/'scripts/validate_pack.py'),str(target)],check=True)

if __name__=='__main__':
 root=Path(__file__).resolve().parents[1]
 print(json.dumps(verify(root,root/'build/Holy_Diver_(Tr)'),indent=2))
