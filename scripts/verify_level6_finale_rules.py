"""Validate the removable final-climb, boss and ending art layer."""
from pathlib import Path
import hashlib,json,re,shutil,subprocess,sys,tempfile
import numpy as np
from PIL import Image
from verify_level6_opening_rules import native_hull

def strip(text):
 for part in ['IMAGES','CONDITIONS','MAPPINGS']:
  text,n=re.subn(r'^# BEGIN LEVEL6_FINALE '+part+r'\n.*?^# END LEVEL6_FINALE '+part+r'\n','',text,flags=re.M|re.S);assert n==1
 return text

def verify(root,pack):
 prior=json.loads((root/'evidence/0.29.1-pack-sha256.json').read_text());text=(pack/'hires.txt').read_text();old=strip(text);oldlines=set(old.splitlines());lines=set(text.splitlines())
 assert hashlib.sha256(old.encode()).hexdigest()==prior['hires.txt']
 art=root/'art/level6_finale';reg=json.loads((art/'registration.json').read_text());patterns={int(k,16):v for k,v in json.loads((art/'native_patterns.json').read_text()).items()}
 assert set(p.name for p in pack.iterdir()if p.is_file())==set(prior)|set(reg['new_files'])
 for name,digest in prior.items():
  if name not in ['hires.txt','README.txt']:assert hashlib.sha256((pack/name).read_bytes()).hexdigest()==digest,name
 assert len(reg['new_files'])==13 and reg['atlas_index']==69
 images=[l[5:]for l in text.splitlines()if l.startswith('<img>')];assert images[69]=='Final_Citadel_Finale_2x.png'
 assert (pack/images[69]).read_bytes()==(art/images[69]).read_bytes()
 atlas=Image.open(pack/images[69]).convert('RGBA');assert atlas.size==(1024,512)
 assert set(reg['scopes'])=={'A49F','A553','A58F','B01C'}
 assert sum(',tileNearby,'in l for l in reg['conditions'])==len(reg['fill_sources'])
 for room,scope in reg['scopes'].items():
  terms=scope.split('&');assert len(terms)==3
  for name,addr,val in zip(terms,['0072','0078','0079'],['04',room[2:],room[:2]]):assert f'<condition>{name},memoryCheckConstant,{addr},==,{val}'in lines
 for e in reg['clones']:
  s,t=e['source_rule'],e['rule'];assert s in oldlines and t in lines
  a,b=[v.split('<tile>')[1].split(',')for v in [s,t]]
  assert patterns[int(a[1],16)]==patterns[int(b[1],16)]
  assert a[0]==b[0]and a[3:5]==b[3:5]and a[6:]==b[6:]
  assert float(b[5])<=float(a[5])
  assert any(scope in t for scope in reg['scopes'].values())
 # Specific sprite-neighbor identities must use the destination bank.
 for line in reg['conditions']:
  f=line[11:].split(',')
  if f[1]=='spriteNearby':assert not 0xA00<=int(f[4],16)<=0xA8D
 kinds={};cells={}
 for e in reg['mappings']:
  assert e['rule']in lines;assert e['palette']not in ['0F0F0F0F','FF0F0F0F']
  assert any(scope in e['scope']for scope in reg['scopes'].values())
  x,y=e['xy'];assert x%16==y%16==0 and 0<=x<=1008 and 0<=y<=496
  cells[e['tile'],e['palette'],e['kind']]=atlas.crop((x,y,x+16,y+16));kinds[e['kind']]=kinds.get(e['kind'],0)+1
 for name,layout in reg['components'].items():
  whole=Image.open(art/(name+'.png')).convert('RGBA');mask=np.zeros((whole.height,whole.width),bool)
  for t,x,y in layout:
   mask[y:y+16,x:x+16]=True;expected=whole.crop((x,y,x+16,y+16)).tobytes()
   mapped=[v for (tile,pal,kind),v in cells.items()if int(tile,16)==t and kind=='boss '+name];assert mapped and all(v.tobytes()==expected for v in mapped)
  assert not ((np.array(whole)[:,:,3]>0)&~mask).any()
 shared={}
 for i,layout in enumerate(reg['ending_layouts']):
  whole=Image.open(art/f'ending_dragon{i}.png').convert('RGBA');mask=np.zeros((whole.height,whole.width),bool)
  for t,x,y in layout:
   mask[y*2:y*2+16,x*2:x*2+16]=True;cell=whole.crop((x*2,y*2,x*2+16,y*2+16))
   assert cells[f'{0x1e00+t:04X}','FF190927','ending dragon'].tobytes()==cell.tobytes()
   if t in shared:assert shared[t]==cell.tobytes()
   shared[t]=cell.tobytes()
  assert not ((np.array(whole)[:,:,3]>0)&~mask).any()
 spec=json.loads((art/'boss_background_variants.json').read_text())
 for name in ['boss1','boss2']:
  x0,y0,x1,y1=spec[name]['box'];assert Image.open(art/(name+'_painting.png')).size==(x1-x0,y1-y0)
  legal={(p['x'],p['y'])for p in spec[name]['positions']if set(p['tiles'])=={'1D00'}}
  defs={l[11:].split(',')[0]:l[11:].split(',')for l in reg['conditions']}
  for fill in [f for f in reg['fill_sources']if f['form']==name]:
   x,y=fill['x'],fill['y'];assert (x,y)in legal
   dx,dy=fill['dx'],fill['dy'];terms=fill['terms'];assert len(terms)==5
   expected=[['positionCheckX','>=',str(max(0,-dx))],['positionCheckX','<',str(min(256,256-dx))],['positionCheckY','>=',str(max(0,-dy))],['positionCheckY','<',str(min(240,240-dy))]]
   for term,d in zip(terms[:4],expected):assert defs[term][1:]==d
   assert defs[terms[4]][1:]==['tileNearby',str(dx),str(dy),fill['anchor'],'0F063026','Y']
   anchors=[p for p in spec[name]['positions']if fill['anchor']in p['tiles']];assert len(anchors)==1 and len(anchors[0]['tiles'])==1
   assert (anchors[0]['x'],anchors[0]['y'])==(x+dx*2,y+dy*2)
   uses=[e for e in reg['mappings']if e['kind']==name+' static interior fill'and terms[4]in e['scope'].split('&')];assert uses
   for e in uses:
    tt=e['scope'].split('&');assert tt[-5:]==terms and e['tile']=='1D00'
 for line in reg['backgrounds']:assert line in lines and any(scope in line for scope in reg['scopes'].values())and ',1,0,0,1,0,0'in line
 assert not any('1F'==e['tile'][:2]for e in reg['mappings']) # Finished ending typography remains exact.
 standby=json.loads((root/'art/level6_enemy_revision/standby.json').read_text())
 for path,digest in standby['original_files'].items():assert hashlib.sha256((root/path).read_bytes()).hexdigest()==digest
 return dict(prior_assets_exact=len(prior)-2,exact_0291_mapping_recovery=True,new_install_files=13,room_scopes=reg['scopes'],mappings=kinds,alias_rules=len(reg['clones']),native_aliases_exact=True,whole_component_bounds_exact=True,ending_poses=2,ending_shared_tail_exact=True,ending_lettering_unchanged=True,static_fills_never_destroyed_parts=True,original_orb_standby_exact=True,bounded_unique_body_neighbor_probes=len(reg['fill_sources']))

def legacy_projection(root,pack):
 prior=json.loads((root/'evidence/0.29.1-pack-sha256.json').read_text())
 with tempfile.TemporaryDirectory(prefix='citadel-0291-')as directory:
  target=Path(directory)
  for name,digest in prior.items():
   if name=='hires.txt':(target/name).write_text(strip((pack/name).read_text()))
   elif name=='README.txt':(target/name).write_bytes((root/'evidence/level6_finale/baseline_README.txt').read_bytes())
   else:shutil.copyfile(pack/name,target/name)
   assert hashlib.sha256((target/name).read_bytes()).hexdigest()==digest,name
  subprocess.run([sys.executable,str(root/'scripts/validate_pack.py'),str(target)],check=True)

if __name__=='__main__':
 root=Path(__file__).resolve().parents[1];print(json.dumps(verify(root,root/'build/Holy_Diver_(Tr)'),indent=2))
