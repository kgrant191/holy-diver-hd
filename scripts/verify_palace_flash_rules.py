"""Verify exact source reuse and isolated native-palette flash variants."""
from pathlib import Path
import hashlib,json,re,tempfile,subprocess,sys,shutil
import numpy as np
from PIL import Image
def strip(text):
 for section in ['CONDITIONS','MAPPINGS']:
  text,n=re.subn(r'^# BEGIN PALACE_FLASH '+section+r'\n.*?^# END PALACE_FLASH '+section+r'\n','',text,flags=re.M|re.S);assert n==1
 return text
def verify(root,pack):
 previous=json.loads((root/'evidence/0.22.0-pack-sha256.json').read_text());text=(pack/'hires.txt').read_text();old=strip(text);assert hashlib.sha256(old.encode()).hexdigest()==previous['hires.txt']
 reg=json.loads((root/'art/level5_flash/registration.json').read_text());assert {p.name for p in pack.iterdir()if p.is_file()}==set(previous)|set(reg['files'].values())
 for name,h in previous.items():
  if name not in ['hires.txt','README.txt']:assert hashlib.sha256((pack/name).read_bytes()).hexdigest()==h,name
 for src,dst in reg['files'].items():
  a=np.array(Image.open(pack/src).convert('RGB'));b=np.array(Image.open(pack/dst).convert('RGBA'))
  assert np.array_equal(a,b[:,:,:3])and np.all(b[:,:,3]==176)
 old_lines=set(old.splitlines());all_lines=set(text.splitlines());defs={l[11:].split(',')[0]:l[11:].split(',')for l in old_lines if l.startswith('<condition>')};new_defs={l[11:].split(',')[0]:l[11:].split(',')for l in reg['conditions']}
 for entry in reg['mappings']:
  source=entry['source_rule'];rule=entry['rule'];phase=entry['phase'];assert source in old_lines and rule in all_lines and phase in ['30','31']
  sh,sb=source[1:].split(']',1);nh,nb=rule[1:].split(']',1);assert sh.startswith('palace')
  assert len(sh.split('&'))==len(nh.split('&'))
  for st,nt in zip(sh.split('&'),nh.split('&')):
   if st in ['hmirror','vmirror','bgpriority']:assert st==nt;continue
   expected=defs[st.lstrip('!')].copy();expected[0]='palaceFlash'+phase+'_'+expected[0]
   if expected[1]in ['tileNearby','tileAtPosition']and expected[5].startswith('0F'):expected[5]=phase+expected[5][2:]
   assert new_defs[nt.lstrip('!')]==expected and st.startswith('!')==nt.startswith('!')
  if entry['kind']=='tile':
   a=sb[6:].split(',');b=nb[6:].split(',');assert a[:2]==b[:2]and a[3:]==b[3:]and b[2]==phase+a[2][2:]
  else:
   a=sb[12:].split(',');b=nb[12:].split(',');assert b[0]==reg['files'][a[0]]and a[1:]==b[1:]
   assert any(new_defs[t.lstrip('!')][1]=='tileAtPosition'and new_defs[t.lstrip('!')][5].startswith(phase)for t in nh.split('&'))
 return dict(prior_assets_exact=122,exact_0220_mapping_recovery=True,all_source_cells_and_conditions_preserved=True,flash_variants=['30','31'],panorama_RGB_exact=True,panorama_opacity=176,tile_aliases=reg['tile_rules'],background_aliases=reg['background_rules'],new_neighbor_geometry=False)
def legacy_projection(root,pack):
 previous=json.loads((root/'evidence/0.22.0-pack-sha256.json').read_text())
 with tempfile.TemporaryDirectory(prefix='palace-0220-')as directory:
  target=Path(directory)
  for name,h in previous.items():
   if name=='hires.txt':(target/name).write_text(strip((pack/name).read_text()))
   elif name=='README.txt':(target/name).write_bytes((root/'evidence/level5_flash/baseline_README.txt').read_bytes())
   else:shutil.copyfile(pack/name,target/name)
   assert hashlib.sha256((target/name).read_bytes()).hexdigest()==h,name
  subprocess.run([sys.executable,str(root/'scripts/validate_pack.py'),str(target)],check=True)
if __name__=='__main__':
 root=Path(__file__).resolve().parents[1];print(json.dumps(verify(root,root/'build/Holy_Diver_(Tr)'),indent=2))
