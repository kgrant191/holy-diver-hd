"""Validate exact reuse, native bounds and reversible Level 6 continuation."""
from pathlib import Path
import hashlib,json,re,tempfile,subprocess,sys,shutil
import numpy as np
from PIL import Image
from verify_level6_opening_rules import native_hull
NEW={'Final_Citadel_Next_2x.png'}
def strip(text):
 for part in ['IMAGES','CONDITIONS','MAPPINGS','ALIASES']:
  text,n=re.subn(r'^# BEGIN LEVEL6_NEXT '+part+r'\n.*?^# END LEVEL6_NEXT '+part+r'\n','',text,flags=re.M|re.S);assert n==1
 return text
def verify(root,pack):
 previous=json.loads((root/'evidence/0.25.1-pack-sha256.json').read_text());text=(pack/'hires.txt').read_text();old=strip(text)
 assert hashlib.sha256(old.encode()).hexdigest()==previous['hires.txt']
 assert {p.name for p in pack.iterdir()if p.is_file()}==set(previous)|NEW
 for name,digest in previous.items():
  if name not in ['hires.txt','README.txt']:assert hashlib.sha256((pack/name).read_bytes()).hexdigest()==digest,name
 art=root/'art/level6_next';reg=json.loads((art/'registration.json').read_text())
 patterns={int(k,16):bytes.fromhex(v)for k,v in json.loads((root/'art/level6_opening/native_patterns.json').read_text()).items()}
 lines=set(text.splitlines());oldlines=set(old.splitlines());defs={l[11:].split(',')[0]:l[11:].split(',')[1:]for l in reg['conditions']}
 assert all(d[0]!='tileNearby'for d in defs.values())
 assert all(l in lines for l in reg['conditions']+reg['backgrounds'])
 for room,mode in [('9F3B','10'),('A02B','04')]:
  assert [defs[k]for k in reg['scopes'][room].split('&')]==[['memoryCheckConstant','0072','==',mode],['memoryCheckConstant','0078','==',room[2:]],['memoryCheckConstant','0079','==',room[:2]]]
 atlas=Image.open(pack/'Final_Citadel_Next_2x.png').convert('RGBA');assert atlas.size==(256,256)
 assert (pack/'Final_Citadel_Next_2x.png').read_bytes()==(art/'Final_Citadel_Next_2x.png').read_bytes()
 images=[l[5:]for l in text.splitlines()if l.startswith('<img>')];assert images[reg['atlas_index']]=='Final_Citadel_Next_2x.png'
 mapped={};hulls=0
 for e in reg['mappings']:
  assert e['rule']in lines;assert e['scope']in reg['scopes'].values()
  t=int(e['tile'],16);x,y=e['xy'];cell=atlas.crop((x,y,x+16,y+16));mapped[t,e['palette'],e['scope']]=cell
  if e['kind']in ['empty native space','distant wall']:assert not cell.getchannel('A').getbbox()
  elif e['kind']=='native structural stone':assert np.array_equal(np.array(cell.getchannel('A'))>0,native_hull(patterns[t]));hulls+=1
  else:assert e['kind'].startswith('whole crawler ')
 aliases=0;shot=0
 for e in reg['clones']:
  assert e['source_rule']in oldlines and e['rule']in lines
  a=e['source_rule'].split('<tile>')[1].split(',');b=e['rule'].split('<tile>')[1].split(',')
  assert a[0]==b[0]and a[3:]==b[3:]
  if e['kind']=='one-cell shot art reuse':assert a[1]=='0694'and b[1]=='18EB'and b[2]=='FF000F30';shot+=1
  else:assert patterns[int(a[1],16)]==patterns[int(b[1],16)];aliases+=1
 # Every native whole terrain group remains contiguous and has the old RGB.
 stone=Image.open(root/'art/level6_opening/rock_material.png').convert('RGBA')
 for name,layout in reg['groups'].items():
  im=Image.open(art/(name+'.png')).convert('RGBA');assert np.array_equal(np.array(im)[:,:,:3],np.array(stone.crop((0,0,*im.size)))[:,:,:3])
  for y,row in enumerate(layout):
   for x,t in enumerate(row):
    if t is None:continue
    expected=im.crop((16*x,16*y,16*x+16,16*y+16))
    for scope in reg['scopes'].values():
     for phase in ['0F','30','31']:
      for suffix in ['061636','162738','072830']:
       for bank in [0,0x200]:assert mapped[t+bank,phase+suffix,scope].tobytes()==expected.tobytes()
 for pose in reg['poses']:
  assert pose['clipped_native_empty_cell_pixels']==0
  im=Image.open(art/f"crawler_{pose['name']}.png").convert('RGBA');union=np.zeros((im.height,im.width),bool)
  for key,x,y in pose['layout']:
   union[y*2:y*2+16,x*2:x*2+16]=True
   assert mapped[int(key,16),'FF072630',reg['scopes']['A02B']].tobytes()==im.crop((x*2,y*2,x*2+16,y*2+16)).tobytes()
  assert not np.any((np.array(im.getchannel('A'))>0)&~union)
 # A complete explicit cross-product; no single scrolling tile is assumed.
 expected={(room,t,phase+suffix)for room in reg['scopes']for base in [0x1700,0x1900]for t in range(base,base+256)for phase in ['0F','30','31']for suffix in reg['guard_palettes']}
 for line in reg['backgrounds']:
  head,fields=line[1:].split(']<background>');terms=head.split('&');d=defs[terms[-1]]
  room=next(r for r,s in reg['scopes'].items()if '&'.join(terms[:3])==s)
  assert d[:3]==['tileAtPosition','128','16'];t,pal=int(d[3],16),d[4];expected.remove((room,t,pal))
  assert fields==('Final_Citadel_Interior'+('_Flash'if pal[:2]!='0F'else'')+'.png,1,0,0,1,0,0')
 assert not expected
 return dict(prior_assets_exact=len(previous)-2,exact_0251_mapping_recovery=True,native_byte_aliases=aliases,
  explicitly_nonidentical_projectile_art_reuses=shot,native_structural_masks=hulls,whole_terrain_groups=len(reg['groups']),
  crawler_poses=len(reg['poses']),crawler_native_cell_union_exact=True,clipped_crawler_pixels=0,
  background_guards=len(reg['backgrounds']),background_bank_copies=['1700','1900'],new_neighbor_probes=0)
def legacy_projection(root,pack):
 previous=json.loads((root/'evidence/0.25.1-pack-sha256.json').read_text())
 with tempfile.TemporaryDirectory(prefix='citadel-0251-')as directory:
  target=Path(directory)
  for name,digest in previous.items():
   if name=='hires.txt':(target/name).write_text(strip((pack/name).read_text()))
   elif name=='README.txt':(target/name).write_bytes((root/'evidence/level6_next/baseline_README.txt').read_bytes())
   else:shutil.copyfile(pack/name,target/name)
   assert hashlib.sha256((target/name).read_bytes()).hexdigest()==digest,name
  subprocess.run([sys.executable,str(root/'scripts/validate_pack.py'),str(target)],check=True)
if __name__=='__main__':
 root=Path(__file__).resolve().parents[1];print(json.dumps(verify(root,root/'build/Holy_Diver_(Tr)'),indent=2))
