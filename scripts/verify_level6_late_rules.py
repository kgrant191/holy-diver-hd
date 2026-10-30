"""Validate exact accepted-art reuse, scoped room coverage and native ledge bounds."""
from pathlib import Path
import hashlib,json,re,tempfile,subprocess,sys,shutil
import numpy as np
from PIL import Image
from verify_level6_opening_rules import native_hull
NEW={'Final_Citadel_Late_2x.png'}|{f'Final_Citadel_{s}{f}.png'for s in ['Reliquary','Green_Shaft']for f in ['','_Flash']}
def strip(text):
 for part in ['IMAGES','CONDITIONS','MAPPINGS']:
  text,n=re.subn(r'^# BEGIN LEVEL6_LATE '+part+r'\n.*?^# END LEVEL6_LATE '+part+r'\n','',text,flags=re.M|re.S);assert n==1
 return text
def verify(root,pack):
 prior=json.loads((root/'evidence/0.27.0-pack-sha256.json').read_text());text=(pack/'hires.txt').read_text();old=strip(text)
 assert hashlib.sha256(old.encode()).hexdigest()==prior['hires.txt']
 assert{p.name for p in pack.iterdir()if p.is_file()}==set(prior)|NEW
 for name,digest in prior.items():
  if name not in ['hires.txt','README.txt']:assert hashlib.sha256((pack/name).read_bytes()).hexdigest()==digest,name
 art=root/'art/level6_late';reg=json.loads((art/'registration.json').read_text());lines=set(text.splitlines());oldlines=set(old.splitlines());defs={l[11:].split(',')[0]:l[11:].split(',')[1:]for l in reg['conditions']}
 patterns={int(k,16):bytes.fromhex(v)for k,v in json.loads((root/'art/level6_opening/native_patterns.json').read_text()).items()}
 assert all(d[0]!='tileNearby'for d in defs.values());assert all(l in lines for l in reg['conditions']+reg['backgrounds'])
 for room,mode in [('A20B','10'),('A2FB','04')]:assert[defs[k]for k in reg['scopes'][room].split('&')]==[['memoryCheckConstant','0072','==',mode],['memoryCheckConstant','0078','==',room[2:]],['memoryCheckConstant','0079','==',room[:2]]]
 atlas=Image.open(pack/'Final_Citadel_Late_2x.png').convert('RGBA');assert atlas.size==(32,48);assert(pack/'Final_Citadel_Late_2x.png').read_bytes()==(art/'Final_Citadel_Late_2x.png').read_bytes()
 assert[l[5:]for l in text.splitlines()if l.startswith('<img>')][66]=='Final_Citadel_Late_2x.png'
 ledge=Image.open(art/'floating_ledge.png').convert('RGBA');stone=Image.open(root/'art/level6_variety/green_material.png').convert('RGBA');assert np.array_equal(np.array(ledge)[:,:,:3],np.array(stone.crop((0,0,32,32)))[:,:,:3]);assert atlas.crop((0,0,32,32)).tobytes()==ledge.tobytes()
 masks=0;eye=0
 for e in reg['mappings']:
  assert e['rule']in lines;t=int(e['tile'],16);x,y=e['xy'];cell=atlas.crop((x,y,x+16,y+16))
  if e['kind']=='distant green wall':assert not cell.getchannel('A').getbbox()
  else:assert e['kind']=='whole floating ledge';assert np.array_equal(np.array(cell.getchannel('A'))>0,native_hull(patterns[t]));masks+=1
 for e in reg['clones']:
  assert e['source_rule']in oldlines and e['rule']in lines
  a=e['source_rule'].split('<tile>')[1].split(',');b=e['rule'].split('<tile>')[1].split(',');assert a[0]==b[0]and a[3:]==b[3:];assert patterns[int(a[1],16)]==patterns[int(b[1],16)]
  if e['kind']=='returning eye and tear':eye+=1;assert a[2]==b[2]
  elif e['kind']=='shaft green palette':assert a[2][2:]=='0B1B3B'and b[2][2:]=='0A1A39'and a[2][:2]==b[2][:2]
  else:assert a==b
 assert masks==144 and eye==12
 expected={(room,t,phase+suffix)for room in reg['scopes']for base in [0x1700,0x1900]for t in range(base,base+256)for phase in ['0F','30','31']for suffix in reg['guard_palettes']}
 for line in reg['backgrounds']:
  head,fields=line[1:].split(']<background>');terms=head.split('&');room=next(r for r,s in reg['scopes'].items()if s=='&'.join(terms[:3]));d=defs[terms[-1]];assert d[:3]==['tileAtPosition','128','16'];t,pal=int(d[3],16),d[4];expected.remove((room,t,pal));style=reg['styles'][room][0]
  assert fields==f'Final_Citadel_{style}'+('_Flash'if pal[:2]!='0F'else'')+'.png,1,0,0,1,0,0'
 assert not expected;assert all(s not in reg['guard_palettes']for s in ['213029','041424'])
 for style in ['Reliquary','Green_Shaft']:
  im=np.array(Image.open(pack/f'Final_Citadel_{style}.png').convert('RGBA'));flash=np.array(Image.open(pack/f'Final_Citadel_{style}_Flash.png').convert('RGBA'));assert im.shape==(480,512,4)and np.all(im[:,:,3]==255);assert np.array_equal(im[:,:,:3],flash[:,:,:3])and np.all(flash[:,:,3]==176)
 return dict(prior_assets_exact=len(prior)-2,exact_0270_mapping_recovery=True,native_ledge_masks=masks,whole_ledge_size=[32,32],native_byte_clone_rules=len(reg['clones']),eye_and_tear_aliases=eye,background_guards=len(reg['backgrounds']),background_bank_copies=['1700','1900'],new_neighbor_probes=0,death_card_palettes_excluded=True)
def legacy_projection(root,pack):
 prior=json.loads((root/'evidence/0.27.0-pack-sha256.json').read_text())
 with tempfile.TemporaryDirectory(prefix='citadel-0270-')as directory:
  target=Path(directory)
  for name,digest in prior.items():
   if name=='hires.txt':(target/name).write_text(strip((pack/name).read_text()))
   elif name=='README.txt':(target/name).write_bytes((root/'evidence/level6_late/baseline_README.txt').read_bytes())
   else:shutil.copyfile(pack/name,target/name)
   assert hashlib.sha256((target/name).read_bytes()).hexdigest()==digest,name
  subprocess.run([sys.executable,str(root/'scripts/validate_pack.py'),str(target)],check=True)
if __name__=='__main__':
 root=Path(__file__).resolve().parents[1];print(json.dumps(verify(root,root/'build/Holy_Diver_(Tr)'),indent=2))
