"""Verify 0.8.1 review scope, native behavior/audio and actual rendered artwork."""
from pathlib import Path
from collections import Counter
import argparse,hashlib,json
import numpy as np
from PIL import Image
p=argparse.ArgumentParser()
for k in ['before','after','routes','out']:p.add_argument('--'+k,required=True)
a=p.parse_args();root=Path(__file__).resolve().parents[1]
routes=json.loads(Path(a.routes).read_text());old=json.loads((root/'evidence/0.8.0-pack-sha256.json').read_text());new=json.loads((root/'evidence/0.8.1-pack-sha256.json').read_text())
assert sorted(k for k in old if old[k]!=new[k])==['README.txt','hires.txt']
assert set(new)-set(old)=={'Stage2_Cave_Review_2x.png'}
art=root/'art/screen2_5_review';sources={f'stair_{t:04X}':np.array(Image.open(art/f'stair_{t:04X}.png').convert('RGBA'))for t in [0x375,0x379,0x37d]}
sources['health_jug']=np.array(Image.open(art/'health_jug.png').convert('RGBA'))
assert set(np.unique(sources['health_jug'][:,:,3]))=={0,255}
assert np.all(sources['health_jug'][16:25,8:21,3]==255),'vessel interior must be opaque'
# Stair alpha equals the prior native contour. New art only changes material.
atlas_old=Image.open(root/'build/Holy_Diver_(Tr)/Stage2_Second_Cave_Tiles_2x.png').convert('RGBA')
prior=json.loads((root/'art/screen2_4/registration.json').read_text())['mappings']
for t in [0x375,0x379,0x37d]:
 old_step=Image.new('RGBA',(32,32))
 for i in range(4):
  m=next(m for m in prior if m['identity']==f'{t+i:04X}');x,y=m['atlas'];old_step.paste(atlas_old.crop((x,y,x+16,y+16)),(i%2*16,i//2*16))
 assert np.array_equal(np.array(old_step)[:,:,3],sources[f'stair_{t:04X}'][:,:,3])
anchors={}
for key,im in sources.items():
 mask=im[:,:,3]>0;color,counts=np.unique(im[:,:,:3][mask],axis=0,return_counts=True);color=color[counts.argmin()]
 y,x=np.argwhere(mask & np.all(im[:,:,:3]==color,axis=2))[0];anchors[key]=(mask,color,int(x),int(y))
seen=Counter();examples={}
def match(rgb,key,case,n):
 src=sources[key];mask,color,sx,sy=anchors[key];h,w=src.shape[:2]
 for y,x in np.argwhere(np.all(rgb==color,axis=2)):
  X,Y=int(x-sx),int(y-sy)
  if X<0 or Y<0 or X+w>512 or Y+h>480:continue
  if np.array_equal(rgb[Y:Y+h,X:X+w][mask],src[:,:,:3][mask]):
   seen[key]+=1;examples.setdefault(key,dict(case=case,frame=n,box=[X,Y,X+w,Y+h]));return True
 return False
def position(folder,n):
 v=(folder/f'dumps/{n:04}.view').read_text().split(',');tmp,fine=int(v[0]),int(v[1]);return (tmp&31)*8+fine+((tmp>>10)&1)*256
report=dict(baseline='0.8.0',candidate='0.8.1',controller_only=True,ram_writes=False,capture_stride=2,cases={})
for case,route in routes.items():
 b,c=Path(a.before)/case,Path(a.after)/case;frames=route['frames']
 assert (b/'completed.txt').read_text()==(c/'completed.txt').read_text()==str(frames)
 assert (b/'input.json').read_bytes()==(c/'input.json').read_bytes()
 inp=json.loads((c/'input.json').read_text());assert inp['controller_route']==route.get('input_code','emu.setInput({'+route.get('input','')+'},0)')
 for folder,expected in [(b,old),(c,new)]:
  for fname in ['installed_pack_sha256.json','installed_pack_after_sha256.json']:assert json.loads((folder/fname).read_text())==expected
 for ext in ['ram','ppu','oam','view']:
  fs=list((b/'dumps').glob('*.'+ext));assert len(fs)==frames//2
  for f in fs:assert f.read_bytes()==(c/'dumps'/f.name).read_bytes(),(case,f.name)
 apu=(b/'apu.tsv').read_bytes();assert apu==(c/'apu.tsv').read_bytes()
 bp,cp=(b/'full.wav').read_bytes()[44:],(c/'full.wav').read_bytes()[44:];common=min(len(bp),len(cp));tail=abs(len(bp)-len(cp));assert common and bp[:common]==cp[:common] and tail<=3200
 black=outside=menu=changed=exact=floor_cells=jug_frames=0;rooms=Counter();scrolls=[]
 for n in range(2,frames+1,2):
  before=np.array(Image.open(b/f'frames/{n:04}.png').convert('RGB'));after=np.array(Image.open(c/f'frames/{n:04}.png').convert('RGB'));diff=np.any(before!=after,axis=2)
  exact+=not diff.any();changed+=bool(diff.any())
  ram=(c/f'dumps/{n:04}.ram').read_bytes();ppu=(c/f'dumps/{n:04}.ppu').read_bytes();oam=(c/f'dumps/{n:04}.oam').read_bytes();room=ram[0x78:0x7a].hex();rooms[room]+=1
  neighbors=[j for j in [n-2,n,n+2]if 2<=j<=frames]
  if before.max()==0:assert after.max()==0,(case,n,'black frame');black+=1
  nearrooms={(c/f'dumps/{j:04}.ram').read_bytes()[0x78:0x7a].hex()for j in neighbors}
  if not nearrooms & {'ad8c','9d8d'}:assert not diff.any(),(case,n,'outside cave');outside+=1
  if case=='menu' and 420<=n<=530:assert not diff.any();menu+=1
  if room=='ad8c' and nearrooms=={'ad8c'}:
   allowed=np.zeros((480,512),dtype=bool)
   for j in neighbors:
    pp=(c/f'dumps/{j:04}.ppu').read_bytes();offset=position(c,j)
    for page in [0,1]:
     for ty in range(30):
      for tx in range(32):
       t=pp[0x2000+page*1024+ty*32+tx]
       if not 0x75<=t<=0x80:continue
       x=(page*256+tx*8-offset)%512
       if x<256:allowed[ty*16:ty*16+16,max(0,x*2-2):min(512,x*2+18)]=True
   assert not np.any(diff&~allowed),(case,n,'outside native stair cells')
  visible_jug=any(oam[i]<239 and oam[i+1]==0x76 and ppu[0x3f11+(oam[i+2]&3)*4:0x3f14+(oam[i+2]&3)*4]==bytes.fromhex('301116')for i in range(0,256,4))
  jug_frames+=visible_jug
  if n%20==0:
   for key in sources:
    if key!='health_jug' or visible_jug:match(after,key,case,n)
  if room=='9d8d':
   sc=int.from_bytes(ram[0x60:0x62],'little')
   if sc<768:scrolls.append(sc)
   # Compare central pixels of the original gold platform bodies. Their cap
   # lookup must preserve full bodies even though ceiling uses the same IDs.
   if n%20==0 and ppu[0x3f08:0x3f0c]==bytes.fromhex('0f061626') and before.max()>0:
    offset=position(c,n)
    for page in [0,1]:
     for tx in range(32):
      capped=False
      for ty in range(30):
       t=ppu[0x2000+page*1024+ty*32+tx]
       if t in [0x2e,0x2f]:capped=True
       if not capped or t not in [0x30,0x31,0x32,0x33,0x81,0x82,0x83,0x84]:continue
       x=(page*256+tx*8-offset)%512
       if not 2<=x<=246:continue
       X,Y=x*2+4,ty*16+4
       assert np.array_equal(before[Y:Y+8,X:X+8],after[Y:Y+8,X:X+8]),(case,n,'gold platform body',tx,ty)
       floor_cells+=1
 report['cases'][case]=dict(frames=frames,input=inp,identical_native_samples_per_type=frames//2,apu_sha256=hashlib.sha256(apu).hexdigest(),identical_pcm_bytes=common,shutdown_tail_bytes=tail,changed_images=changed,exact_images=exact,black_images=black,unchanged_outside_room_images=outside,unchanged_menu_images=menu,gold_floor_cell_checks=floor_cells,health_jug_oam_frames=jug_frames,rooms=dict(rooms),max_camera_scroll=max(scrolls)if scrolls else None)
for key in ['stair_0375','stair_0379','stair_037D']:assert seen[key],('missing complete stair match',key)
report.update(total_frames_per_build=sum(r['frames']for r in routes.values()),native_samples_per_type=sum(r['frames']//2 for r in routes.values()),complete_source_matches=dict(seen),source_examples=examples,unchanged_prior_runtime_files=86,pack_files=89)
out=Path(a.out);out.parent.mkdir(parents=True,exist_ok=True);out.write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:v for k,v in report.items()if k not in ['cases','source_examples']},indent=2))
