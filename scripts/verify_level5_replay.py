"""Paired native/audio checks, exact menu-change scope and live source matches."""
from pathlib import Path
from collections import Counter
import argparse,hashlib,json,wave
import numpy as np
from PIL import Image
p=argparse.ArgumentParser()
for key in ['before','after','out']:p.add_argument('--'+key,required=True)
p.add_argument('--regression',action='store_true');p.add_argument('--edge',action='store_true');a=p.parse_args()
r=Path(__file__).resolve().parents[1];b,c=Path(a.before),Path(a.after);infos=[json.loads((v/'result.json').read_text())for v in [b,c]]
for k in ['movie_sha256','rom_sha1','core_sha256','movie_frames','captured_frames','stride']:assert infos[0][k]==infos[1][k],k
assert all(v['movie_completed']for v in infos)
assert json.loads((b/'installed_pack.json').read_text())==json.loads((r/'evidence/0.20.5-pack-sha256.json').read_text())
assert json.loads((c/'installed_pack.json').read_text())==json.loads((r/'evidence/0.21.0-pack-sha256.json').read_text())
frames=sorted(int(v.stem)for v in(c/'frames').glob('*.png'));data={k:{}for k in ['ram','ppu','oam','view']}
for n in frames:
 for k in data:
  name=f'{n:06}'+('.json'if k=='view'else'.bin');raw=(c/k/name).read_bytes();assert raw==(b/k/name).read_bytes(),(n,k);data[k][n]=json.loads(raw)if k=='view'else raw
assert(b/'apu.tsv').read_bytes()==(c/'apu.tsv').read_bytes()
with wave.open(str(b/'full.wav'),'rb')as f:pcm=f.readframes(f.getnframes());params=f.getparams()
with wave.open(str(c/'full.wav'),'rb')as f:assert params==f.getparams();assert pcm==f.readframes(f.getnframes())
def source(path,flip):
 src=np.array(Image.open(path).convert('RGBA'))
 if flip&1:src=src[:,::-1]
 if flip&2:src=src[::-1]
 mask=src[:,:,3]==255;colors,counts=np.unique(src[mask,:3],axis=0,return_counts=True);color=colors[np.argmax(colors.sum(1)/(1+counts))];yy,xx=np.where(mask&np.all(src[:,:,:3]==color,2));pts=np.argwhere(mask)
 return src,mask,int(yy[0]),int(xx[0]),pts[np.linspace(0,len(pts)-1,8,dtype=int)]
def matches(im,item):
 src,mask,ay,ax,probes=item;h,w=mask.shape;yy,xx=np.where(np.all(im==src[ay,ax,:3],2));yy-=ay;xx-=ax;v=(yy>=0)&(xx>=0)&(yy+h<=480)&(xx+w<=512);yy,xx=yy[v],xx[v]
 for py,px in probes:
  v=np.all(im[yy+py,xx+px]==src[py,px,:3],1);yy,xx=yy[v],xx[v]
  if not len(yy):return []
 return [[int(x),int(y)]for y,x in zip(yy,xx)if np.array_equal(im[y:y+h,x:x+w][mask],src[:,:,:3][mask])]
names=['skeleton_0','skeleton_1','skeleton_2','bone','boulder_0','boulder_1','boulder_2','serpent_head','serpent_segment','thunder_0','thunder_1','thunder_2']
sources={}if(a.regression or a.edge)else{(name,f):source(r/'art/level5'/(name+'.png'),f)for name in names for f in range(4)}
hits={};counts=Counter();rooms=Counter();menubox=None;positions=[]
menu_border=np.array(Image.open(r/'evidence/level5/menu_border_reference.png').convert('RGB'))
for n in frames:
 paths=[d/'frames'/f'{n:06}.png'for d in [b,c]]
 if not all(v.stat().st_size for v in paths):assert paths[0].stat().st_size==paths[1].stat().st_size;continue
 old,im=[np.array(Image.open(v).convert('RGB'))for v in paths];diff=np.any(old!=im,2);counts['changed'if diff.any()else'identical']+=1
 ram,pp=data['ram'][n],data['ppu'][n];room=f'{int.from_bytes(ram[0x78:0x7a],"little"):04X}';rooms[room]+=1
 if not old.any():assert not im.any(),(n,'blackout');counts['native_black_exact']+=1
 menu=pp[0x20e3]==0x86 and pp[0x212f]==0x82 and pp[0x3f11]==0x0f and np.array_equal(old[:12],menu_border)
 if menu and n>frames[0] and all(data['ppu'][j][0x20e3]==0x86 for j in [n-infos[1]['stride']]if j in data['ppu']):
  if diff.any():
   yy,xx=np.where(diff);box=[int(xx.min()),int(yy.min()),int(xx.max()+1),int(yy.max()+1)]
   # The H is one native cell. No unrelated menu pixel may change.
   assert box[2]-box[0]<=16 and box[3]-box[1]<=16,(n,box)
   if menubox is None:menubox=box
   else:assert box==menubox,(n,box,menubox)
  counts['menu_only_H']+=1
 if a.regression:assert not diff.any(),('prior-stage change',n)
 if a.edge and n%10==0:positions.append(dict(frame=n,x=int.from_bytes(ram[0x74:0x76],'little'),y=int.from_bytes(ram[0x76:0x78],'little')))
 if sources and n%10==0 and not menu:
  for key,item in list(sources.items()):
   pos=matches(im,item)
   if pos:hits[key[0]+' flip'+str(key[1])]=dict(frame=n,positions=pos);del sources[key]
if not(a.regression or a.edge):
 for name in names:assert any(k.startswith(name+' ')for k in hits),(name,'no live complete-source match')
 assert counts['menu_only_H']>0 and menubox is not None
report=dict(movie=infos[1],native_samples_per_type=len(frames),native_exact=True,apu_exact=True,pcm_exact=True,pcm_sha256=hashlib.sha256(pcm).hexdigest(),apu_sha256=hashlib.sha256((c/'apu.tsv').read_bytes()).hexdigest(),images=counts,rooms=rooms,menu_change_bbox=menubox,live_complete_source_matches=hits)
if a.edge:report['controller_route_positions']=positions
Path(a.out).write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:v for k,v in report.items()if k not in ['live_complete_source_matches','controller_route_positions']},indent=2));print('Live whole-source variants:',len(hits))
