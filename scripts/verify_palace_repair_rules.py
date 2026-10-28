"""Require the exact Palace baseline plus narrowly scoped repair overrides."""
from pathlib import Path
import hashlib,json,re,tempfile,subprocess,sys,shutil
import numpy as np
from PIL import Image
from prepare_level5 import reg as register_material
NEW='Demonic_Palace_Repair_2x.png'
def strip(text):
 for section in ['IMAGES','CONDITIONS','MAPPINGS']:
  text,n=re.subn(r'^# BEGIN PALACE_REPAIR '+section+r'\n.*?^# END PALACE_REPAIR '+section+r'\n','',text,flags=re.M|re.S);assert n==1
 return text

def verify(root,pack):
 previous=json.loads((root/'evidence/0.21.0-pack-sha256.json').read_text());text=(pack/'hires.txt').read_text();old=strip(text);assert hashlib.sha256(old.encode()).hexdigest()==previous['hires.txt'];assert {p.name for p in pack.iterdir()if p.is_file()}==set(previous)|{NEW}
 for name,h in previous.items():
  if name not in {'hires.txt','README.txt'}:assert hashlib.sha256((pack/name).read_bytes()).hexdigest()==h,name
 a=root/'art/level5_repair';reg=json.loads((a/'registration.json').read_text());inventory=json.loads((a/'inventory.json').read_text());images=[l[5:]for l in text.splitlines()if l.startswith('<img>')];assert images[58]==NEW
 source=Image.open(pack/NEW).convert('RGBA');assert source.size==(128,128)and (pack/NEW).read_bytes()==(a/NEW).read_bytes()
 roof=0;stair_masks=0
 oldreg=json.loads((root/'art/level5/registration.json').read_text())
 oldmaterial=np.array(register_material(Image.open(root/'art/generated/screen2_5_stair_tread_generated.png'),(64,64)))
 for m in reg['mappings']:
  assert m['rule']in text.splitlines();x,y=m['xy'];im=source.crop((x,y,x+16,y+16));t=int(m['tile'],16)
  if m['kind']=='slime cavern ceiling':
   original=m['source_rule'];assert original in old.splitlines()and text.index(m['rule'])<text.index(original)
   f=original.split('<tile>')[1].split(',');sx,sy=map(int,f[3:5]);native=Image.open(pack/images[int(f[0])]).convert('RGBA').crop((sx,sy,sx+16,sy+16))
   assert native.getchannel('A').tobytes()==im.getchannel('A').tobytes()
   assert (t&255)in [1,2,3,4,0x1d,0x1e,0x1f,0x20]and m['scope'].startswith(reg['scopes']['850A']);assert original[1:original.index(']')]==m['scope'];roof+=1
  else:
   assert m['scope']in [reg['scopes'][r]for r in ['8816','888E']]
   if m['scope']==reg['scopes']['8816']and m['palette']=='0F001030':
    candidates=[v for v in oldreg['mappings']if v['tile']==m['tile']and v['palette']==m['palette']and v['scope']==m['scope']]
    if candidates:
     previous_cell=candidates[0];ox,oy=previous_cell['xy'];previous_image=Image.open(pack/'Demonic_Palace_Tiles_2x.png').convert('RGBA').crop((ox,oy,ox+16,oy+16))
     assert previous_image.getchannel('A').tobytes()==im.getchannel('A').tobytes()
     x0,y0=t%4*16,t//4%4*16;keep=(oldmaterial[y0:y0+16,x0:x0+16,3]>0)&(np.array(im)[:,:,3]>0)
     assert np.array_equal(np.array(previous_image)[:,:,:3][keep],np.array(im)[:,:,:3][keep]);stair_masks+=1
 assert roof==48
 # All newly observed native guards are present in both physical CHR copies.
 for room,items in inventory['view_guards'].items():
  for key,pal in items:
   assert pal in ['0F0F0717','0F001030']
   for bank in [0,0x200]:
    t=int(key,16)+bank;name=f'palaceRepairView{room}_{t:04X}_{pal}'
    assert f'<condition>{name},tileAtPosition,128,16,{t:04X},{pal}'in reg['conditions']
    assert f'[{reg["scopes"][room]}&{name}]<background>Demonic_Palace_Interior.png,1,0,0,1,0,0'in reg['backgrounds']
 # Exactly thirteen normal-palette aliases; no pose, geometry or timing change.
 assert len(reg['clones'])==13
 for m in reg['clones']:
  assert m['source_rule']in old.splitlines()and m['rule']in text.splitlines()
  assert m['rule']=='['+reg['scopes']['8816']+']'+m['source_rule'].replace('FF0B2B30','FF110130')
 assert not any('tileNearby'in l for l in reg['conditions'])
 return dict(prior_assets_exact=120,exact_0210_mapping_recovery=True,roof_alpha_and_conditions_exact=roof,existing_stair_alpha_and_opaque_tread_exact=stair_masks,serpent_aliases=13,new_neighbor_probes=0,new_background_guards=len(reg['backgrounds']),new_files=[NEW])

def legacy_projection(root,pack):
 previous=json.loads((root/'evidence/0.21.0-pack-sha256.json').read_text())
 with tempfile.TemporaryDirectory(prefix='palace-0210-')as directory:
  target=Path(directory)
  for name,h in previous.items():
   if name=='hires.txt':(target/name).write_text(strip((pack/name).read_text()))
   elif name=='README.txt':(target/name).write_bytes((root/'evidence/level5_repair/baseline_README.txt').read_bytes())
   else:shutil.copyfile(pack/name,target/name)
   assert hashlib.sha256((target/name).read_bytes()).hexdigest()==h,name
  subprocess.run([sys.executable,str(root/'scripts/validate_pack.py'),str(target)],check=True)
if __name__=='__main__':
 root=Path(__file__).resolve().parents[1];print(json.dumps(verify(root,root/'build/Holy_Diver_(Tr)'),indent=2))
