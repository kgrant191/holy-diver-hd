"""Verify a mapping-only repair and retain the exact historical validator chain."""
from pathlib import Path
import hashlib,json,re,tempfile,subprocess,sys,shutil
from PIL import Image

def strip(text):
 text,n=re.subn(r'^# BEGIN PALACE_ONE_UP MAPPINGS\n.*?^# END PALACE_ONE_UP MAPPINGS\n','',text,flags=re.M|re.S);assert n==1
 return text

def verify(root,pack):
 previous=json.loads((root/'evidence/0.22.1-pack-sha256.json').read_text());text=(pack/'hires.txt').read_text();old=strip(text)
 assert hashlib.sha256(old.encode()).hexdigest()==previous['hires.txt']
 assert {p.name for p in pack.iterdir()if p.is_file()}==set(previous)
 for name,h in previous.items():
  if name not in ['hires.txt','README.txt']:assert hashlib.sha256((pack/name).read_bytes()).hexdigest()==h,name
 reg=json.loads((root/'art/level5_one_up/registration.json').read_text());patterns=json.loads((root/'art/level5_one_up/native_patterns.json').read_text());assert len(reg['mappings'])==12
 expected={(f'{bank+offset:04X}',pal)for bank in [0x1000,0x1200]for offset in [0x4e,0x4f]for pal in ['FF300036','FF221136','FF190927']}
 atlas=Image.open(pack/'Tree_Court_Tiles_2x.png').convert('RGBA')
 for e in reg['mappings']:
  assert e['source_rule']in old.splitlines()and text.splitlines().count(e['rule'])==1
  a=e['source_rule'][6:].split(',');b=e['rule'][6:].split(',');expected.remove((b[1],b[2]))
  assert a[0]==b[0]=='29'and a[3:]==b[3:]and patterns[a[1]]==patterns[b[1]]
  assert a[2]==('FF221136'if b[2]=='FF221136'else'FF300036')
  figurine=Image.open(root/f'art/screen1_4/one_up_{a[2]}.png').convert('RGBA');row=(int(b[1],16)&1)*16
  assert atlas.crop((int(b[3]),int(b[4]),int(b[3])+16,int(b[4])+16)).tobytes()==figurine.crop((0,row,16,row+16)).tobytes()
 assert not expected
 return dict(prior_assets_exact=124,exact_0221_mapping_recovery=True,aliases=12,banks=['1000','1200'],palettes=['FF300036','FF221136','FF190927'],complete_approved_figurines_exact=True,new_artwork=False,new_conditions=False)

def legacy_projection(root,pack):
 previous=json.loads((root/'evidence/0.22.1-pack-sha256.json').read_text())
 with tempfile.TemporaryDirectory(prefix='palace-0221-')as directory:
  target=Path(directory)
  for name,h in previous.items():
   if name=='hires.txt':(target/name).write_text(strip((pack/name).read_text()))
   elif name=='README.txt':(target/name).write_bytes((root/'evidence/level5_one_up/baseline_README.txt').read_bytes())
   else:shutil.copyfile(pack/name,target/name)
   assert hashlib.sha256((target/name).read_bytes()).hexdigest()==h,name
  subprocess.run([sys.executable,str(root/'scripts/validate_pack.py'),str(target)],check=True)

if __name__=='__main__':
 root=Path(__file__).resolve().parents[1];print(json.dumps(verify(root,root/'build/Holy_Diver_(Tr)'),indent=2))
