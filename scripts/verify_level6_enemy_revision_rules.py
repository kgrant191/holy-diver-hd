"""Check the narrow visual override and independently reversible green enemy."""
from pathlib import Path
import hashlib,json,re,tempfile,shutil,subprocess,sys
from PIL import Image

NEW='Final_Citadel_Enemy_Revision_2x.png'
def strip(text):
 for part in ['IMAGES','MAPPINGS']:
  text,n=re.subn(r'^# BEGIN LEVEL6_ENEMY_REVISION '+part+r'\n.*?^# END LEVEL6_ENEMY_REVISION '+part+r'\n','',text,flags=re.M|re.S);assert n==1
 return text
def verify(root,pack):
 prior=json.loads((root/'evidence/0.29.0-pack-sha256.json').read_text());text=(pack/'hires.txt').read_text();old=strip(text);positions={l:i for i,l in enumerate(text.splitlines())};oldlines=set(old.splitlines())
 assert hashlib.sha256(old.encode()).hexdigest()==prior['hires.txt']
 assert {p.name for p in pack.iterdir()if p.is_file()}==set(prior)|{NEW}
 for name,digest in prior.items():
  if name not in ['hires.txt','README.txt']:assert hashlib.sha256((pack/name).read_bytes()).hexdigest()==digest,name
 art=root/'art/level6_enemy_revision';reg=json.loads((art/'registration.json').read_text());original=json.loads((root/'art/level6_organic/registration.json').read_text());standby=json.loads((art/'standby.json').read_text())
 assert reg['scope']==original['scope']=='organicMode&organicLo&organicHi'
 assert reg['choice']==json.loads((art/'choice.json').read_text())['green_enemy']in ['blob','rock']
 assert [l[5:]for l in text.splitlines()if l.startswith('<img>')][68]==NEW
 assert (pack/NEW).read_bytes()==(art/NEW).read_bytes();atlas=Image.open(pack/NEW).convert('RGBA');assert atlas.size==(128,128)
 assert Image.open(art/'wall_face.png').getchannel('A').tobytes()==Image.open(root/'art/level6_organic/wall_face.png').getchannel('A').tobytes()
 face_ids={t for row in reg['face_layout']for t in row};expected={e['rule']for e in original['mappings']if e['kind']=='native organic terrain'and int(e['tile'],16)in face_ids}
 if reg['choice']=='blob':expected|={e['rule']for e in original['mappings']if e['kind']=='whole orb'}
 assert {e['source_rule']for e in reg['mappings']}==expected
 cells={};kinds={}
 for e in reg['mappings']:
  src=e['source_rule'];rule=e['rule'];assert src in oldlines and rule in positions;assert positions[rule]<positions[src]
  a=src.split('<tile>')[1].split(',');b=rule.split('<tile>')[1].split(',');assert a[1:3]==b[1:3]and a[5:]==b[5:]and b[0]=='68'
  assert rule.startswith('['+reg['scope']+']');x,y=e['xy'];assert 0<=x<=112 and 0<=y<=112
  cells[int(e['tile'],16)]=atlas.crop((x,y,x+16,y+16));kinds[e['kind']]=kinds.get(e['kind'],0)+1
 assert kinds['wall face color']==171 and kinds.get('mucus blob',0)==(8 if reg['choice']=='blob'else 0)
 whole=Image.open(art/'wall_face.png').convert('RGBA')
 for y,row in enumerate(reg['face_layout']):
  for x,t in enumerate(row):assert whole.crop((16*x,16*y,16*x+16,16*y+16)).tobytes()==cells[t].tobytes()
 for pose in reg['poses']:
  im=Image.open(art/(pose['name']+'.png')).convert('RGBA');assert im.size==(32,32);assert im.getbbox()==(0,0,32,32)
  if reg['choice']=='blob':
   for y,row in enumerate(pose['layout']):
    for x,t in enumerate(row):assert im.crop((16*x,16*y,16*x+16,16*y+16)).tobytes()==cells[t].tobytes()
 assert standby['original_orb_rules']==[e['rule']for e in original['mappings']if e['kind']=='whole orb']
 for path,digest in standby['original_files'].items():assert hashlib.sha256((root/path).read_bytes()).hexdigest()==digest
 # Omitting just the blob rules restores the exact first matching orb rule,
 # while every face override remains ahead of its original rule.
 restored=text
 for e in reg['mappings']:
  if e['kind']=='mucus blob':restored=restored.replace(e['rule']+'\n','')
 for rule in standby['original_orb_rules']:
  fields=rule.split('<tile>')[1].split(',');key=','.join(fields[1:3])
  candidates=[l for l in restored.splitlines()if l.startswith('['+reg['scope']+']<tile>')and ','.join(l.split('<tile>')[1].split(',')[1:3])==key]
  assert candidates[0]==rule
 for e in reg['mappings']:
  if e['kind']=='wall face color':assert restored.index(e['rule'])<restored.index(e['source_rule'])
 return dict(prior_assets_exact=len(prior)-2,exact_0290_mapping_recovery=True,face_cells=len(face_ids),face_native_alpha_exact=True,mappings=kinds,whole_blob_poses=2,original_orb_standby_exact=True,independent_orb_restore_verified=True,new_neighbor_probes=0)

def legacy_projection(root,pack):
 prior=json.loads((root/'evidence/0.29.0-pack-sha256.json').read_text())
 with tempfile.TemporaryDirectory(prefix='citadel-0290-')as directory:
  target=Path(directory)
  for name,digest in prior.items():
   if name=='hires.txt':(target/name).write_text(strip((pack/name).read_text()))
   elif name=='README.txt':(target/name).write_bytes((root/'evidence/level6_enemy_revision/baseline_README.txt').read_bytes())
   else:shutil.copyfile(pack/name,target/name)
   assert hashlib.sha256((target/name).read_bytes()).hexdigest()==digest,name
  subprocess.run([sys.executable,str(root/'scripts/validate_pack.py'),str(target)],check=True)

if __name__=='__main__':
 root=Path(__file__).resolve().parents[1];print(json.dumps(verify(root,root/'build/Holy_Diver_(Tr)'),indent=2))
