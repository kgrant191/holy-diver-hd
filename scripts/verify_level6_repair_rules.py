"""Validate the removable upper-ceiling and 1-up repair, preserving 0.25.0."""
from pathlib import Path
import hashlib,json,re,tempfile,subprocess,sys,shutil
import numpy as np
from PIL import Image
from verify_level6_opening_rules import native_hull
NEW={'Final_Citadel_Repair_2x.png'}
def strip(text):
 for section in ['IMAGES','CONDITIONS','MAPPINGS','ALIASES']:
  text,n=re.subn(r'^# BEGIN LEVEL6_REPAIR '+section+r'\n.*?^# END LEVEL6_REPAIR '+section+r'\n','',text,flags=re.M|re.S);assert n==1
 return text
def verify(root,pack):
 previous=json.loads((root/'evidence/0.25.0-pack-sha256.json').read_text());text=(pack/'hires.txt').read_text();old=strip(text)
 assert hashlib.sha256(old.encode()).hexdigest()==previous['hires.txt']
 assert {p.name for p in pack.iterdir()if p.is_file()}==set(previous)|NEW
 for name,digest in previous.items():
  if name not in ['hires.txt','README.txt']:assert hashlib.sha256((pack/name).read_bytes()).hexdigest()==digest,name
 art=root/'art/level6_repair';reg=json.loads((art/'registration.json').read_text());patterns={k:bytes.fromhex(v)for k,v in json.loads((root/'art/level6_opening/native_patterns.json').read_text()).items()}
 lines=text.splitlines();oldlines=old.splitlines();assert len(reg['conditions'])==9 and len(reg['mappings'])==72 and len(reg['clones'])==6
 assert all(l in lines for l in reg['conditions']);assert all(',memoryCheckConstant,'in l for l in reg['conditions'])
 defs={l[11:].split(',')[0]:l[11:].split(',')[1:]for l in reg['conditions']}
 for room,mode in [('9A8B','04'),('9BB7','10'),('9CA7','0C')]:
  assert [defs[k]for k in reg['scopes'][room].split('&')]==[['memoryCheckConstant','0072','==',mode],['memoryCheckConstant','0078','==',room[2:]],['memoryCheckConstant','0079','==',room[:2]]]
 atlas=Image.open(pack/'Final_Citadel_Repair_2x.png').convert('RGBA');assert atlas.size==(32,32)
 assert (pack/'Final_Citadel_Repair_2x.png').read_bytes()==(art/'ceiling_unit.png').read_bytes()
 source=Image.open(root/reg['ceiling_source']).convert('RGBA').crop(reg['source_crop']);assert np.array_equal(np.array(atlas)[:,:,:3],np.array(source)[:,:,:3])
 expected={(f'{t:04X}',phase+suffix,scope)for t in range(0x17b4,0x17b8)for phase in ['0F','30','31']for suffix in ['061636','072830']for scope in reg['scopes'].values()}
 for e in reg['mappings']:
  assert e['rule']in lines;expected.remove((e['tile'],e['palette'],e['scope']));x,y=e['xy']
  assert np.array_equal(np.array(atlas.crop((x,y,x+16,y+16)).getchannel('A'))>0,native_hull(patterns[e['tile']]))
  old_matches=[i for i,l in enumerate(oldlines)if '<tile>'in l and f",{e['tile']},{e['palette']},"in l]
  if e['palette']=='0F061636':assert old_matches
  assert all(lines.index(e['rule'])<lines.index(oldlines[i])for i in old_matches)
 assert not expected
 donor=Image.open(pack/'Tree_Court_Tiles_2x.png').convert('RGBA')
 for e in reg['clones']:
  assert e['source_rule']in oldlines and lines.count(e['rule'])==1
  a=e['source_rule'][6:].split(',');b=e['rule'][6:].split(',');assert a[0]==b[0]=='29'and a[3:]==b[3:]
  assert patterns[a[1]]==patterns[b[1]];assert a[2]==('FF221136'if b[2]=='FF221136'else'FF300036')
  figurine=Image.open(root/f'art/screen1_4/one_up_{a[2]}.png').convert('RGBA');y=(int(b[1],16)&1)*16
  x0,y0=map(int,a[3:5]);assert donor.crop((x0,y0,x0+16,y0+16)).tobytes()==figurine.crop((0,y,16,y+16)).tobytes()
 return dict(prior_assets_exact=len(previous)-2,exact_0250_mapping_recovery=True,ceiling_rules=72,one_up_aliases=6,ceiling_RGB_reuses_existing_stone=True,native_hulls_exact=True,complete_approved_figurines_exact=True,new_backgrounds=False,new_neighbor_probes=0)
def legacy_projection(root,pack):
 previous=json.loads((root/'evidence/0.25.0-pack-sha256.json').read_text())
 with tempfile.TemporaryDirectory(prefix='citadel-0250-')as directory:
  target=Path(directory)
  for name,digest in previous.items():
   if name=='hires.txt':(target/name).write_text(strip((pack/name).read_text()))
   elif name=='README.txt':(target/name).write_bytes((root/'evidence/level6_repair/baseline_README.txt').read_bytes())
   else:shutil.copyfile(pack/name,target/name)
   assert hashlib.sha256((target/name).read_bytes()).hexdigest()==digest,name
  subprocess.run([sys.executable,str(root/'scripts/validate_pack.py'),str(target)],check=True)
if __name__=='__main__':
 root=Path(__file__).resolve().parents[1];print(json.dumps(verify(root,root/'build/Holy_Diver_(Tr)'),indent=2))
