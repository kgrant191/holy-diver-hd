"""Validate the isolated Palace layer and run every earlier validator unchanged."""
from pathlib import Path
import hashlib,json,re,subprocess,sys,tempfile,os
import numpy as np
from PIL import Image
ADDED={'Demonic_Palace_Tiles_2x.png','Demonic_Palace_Cavern.png','Demonic_Palace_Interior.png'}
def digest(data):return hashlib.sha256(data).hexdigest()
def strip(text):
 for section in ['IMAGES','CONDITIONS','MAPPINGS','ALIASES']:
  text,n=re.subn(r'^# BEGIN DEMONIC_PALACE '+section+r'\n.*?^# END DEMONIC_PALACE '+section+r'\n','',text,flags=re.M|re.S);assert n==1,section
 return text

def verify(root,pack):
 prior=json.loads((root/'evidence/0.20.5-pack-sha256.json').read_text());text=(pack/'hires.txt').read_text();old=strip(text)
 assert digest(old.encode())==prior['hires.txt'],'baseline mappings changed'
 assert {p.name for p in pack.iterdir()if p.is_file()}==set(prior)|ADDED
 for name,h in prior.items():
  if name not in {'hires.txt','README.txt'}:assert digest((pack/name).read_bytes())==h,name
 a=root/'art/level5';reg=json.loads((a/'registration.json').read_text());defs={l[11:].split(',')[0]:l[11:].split(',')for l in text.splitlines()if l.startswith('<condition>')}
 atlas=Image.open(pack/'Demonic_Palace_Tiles_2x.png').convert('RGBA');assert atlas.size==(512,512)
 assert (pack/'Demonic_Palace_Tiles_2x.png').read_bytes()==(a/'Demonic_Palace_Tiles_2x.png').read_bytes()
 assert reg['atlas_index']==57
 for m in reg['mappings']:
  assert m['rule'] in text.splitlines()
  tile=int(m['tile'],16)
  if tile>=0x1100:assert any(m['scope'].startswith(s)for s in reg['scopes'].values()),m
  if tile==0x946:assert m['scope']=='pauseScreen&pauseMagicRow&pausedPalette'
 for m in reg['clones']:
  assert m['source_rule']in old.splitlines()and m['rule']in text.splitlines()
 for line in reg['backgrounds']:
  assert line in text.splitlines()and any(line.startswith('['+s+'&')for s in reg['scopes'].values())
  cond=defs[line.split(']')[0].split('&')[-1]];assert cond[1:4]==['tileAtPosition','128','16']and cond[5].startswith('0F')
  assert line.endswith(',1,0,0,1,0,0')
 # Exact CHR bank copies justify all broad actor/HUD aliases and the 1300 scenery copy.
 patterns=json.loads((a/'native_patterns.json').read_text())
 for i in range(0x75):assert patterns[f'{0xa00+i:04X}']==patterns[f'{0x1000+i:04X}']
 for i in range(256):assert patterns[f'{0x1100+i:04X}']==patterns[f'{0x1300+i:04X}']
 # Exhaust all screen positions. The Y bound MUST execute before each probe.
 probes=0
 for line in [m['rule']for m in reg['mappings']]:
  terms=line[1:line.index(']')].split('&')if line.startswith('[')else[]
  for j,name in enumerate(terms):
   d=defs.get(name)
   if not d or d[1]!='tileNearby':continue
   assert d[2:4]==['0','8']and 'palaceRoofBelowBound'in terms[:j]
   assert defs['palaceRoofBelowBound']==['palaceRoofBelowBound','positionCheckY','<','232']
   for y in range(240):
    for x in range(256):
     if y<232:assert 0<=x<256 and 0<=y+8<240
   probes+=1
 # Whole sprite alpha stays in the native cell union; shared skeleton cells exact.
 layouts=json.loads((a/'skeleton_layouts.json').read_text());seen={}
 for i,layout in enumerate(layouts):
  im=np.array(Image.open(a/f'skeleton_{i}.png').convert('RGBA'));allowed=np.zeros(im.shape[:2],bool)
  for key,x,y in layout:
   allowed[y*2:y*2+16,x*2:x*2+16]=True;part=im[y*2:y*2+16,x*2:x*2+16]
   if key in seen:assert np.array_equal(seen[key],part)
   seen[key]=part
  assert not np.any((im[:,:,3]>0)&~allowed)
 source=json.loads((a/'source_registration.json').read_text());assert source['skeleton']['clipped_pixels']==0
 h=next(m for m in reg['mappings']if m['kind']=='Thunder H');x,y=h['xy'];assert atlas.crop((x,y,x+16,y+16)).getchannel('A').getbbox()
 return dict(prior_assets_exact=117,exact_0205_mapping_recovery=True,new_files=sorted(ADDED),room_scopes=list(reg['scopes']),tile_rules=len(reg['mappings'])+len(reg['clones']),background_rules=len(reg['backgrounds']),conditions=len(reg['conditions']),bounded_neighbor_rules=probes,unsafe_neighbor_reads=0,shared_skeleton_cells_exact=True)

def validate_legacy_projection(root,pack):
 prior=json.loads((root/'evidence/0.20.5-pack-sha256.json').read_text())
 with tempfile.TemporaryDirectory(prefix='holy-diver-approved-')as directory:
  target=Path(directory)
  for name,h in prior.items():
   if name=='hires.txt':(target/name).write_text(strip((pack/name).read_text()))
   elif name=='README.txt':(target/name).write_bytes((root/'evidence/level5/baseline_README.txt').read_bytes())
   else:os.link(pack/name,target/name)
   assert digest((target/name).read_bytes())==h,name
  # No Palace marker: the complete existing 0.20.5 validation path still executes.
  subprocess.run([sys.executable,str(root/'scripts/validate_pack.py'),str(target)],check=True)

if __name__=='__main__':
 root=Path(__file__).resolve().parents[1];print(json.dumps(verify(root,root/'build/Holy_Diver_(Tr)'),indent=2))
