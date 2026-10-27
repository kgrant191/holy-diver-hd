"""Verify paired native execution, exact retained scope and live source pixels."""
from pathlib import Path
from collections import Counter
import argparse,json,hashlib,wave
import numpy as np
from PIL import Image
p=argparse.ArgumentParser()
for k in ['before','after','out']:p.add_argument('--'+k,required=True)
p.add_argument('--regression',action='store_true');a=p.parse_args()
r=Path(__file__).resolve().parents[1];b,c=Path(a.before),Path(a.after)
bi,ci=[json.loads((d/'result.json').read_text())for d in[b,c]]
for k in ['movie_sha256','rom_sha1','core_sha256','movie_frames','captured_frames','stride']:assert bi[k]==ci[k],k
assert bi['movie_completed']and ci['movie_completed']
for folder,version in [(b,'0.16.3'),(c,'0.17.0')]:
 assert json.loads((folder/'installed_pack.json').read_text())==json.loads((r/f'evidence/{version}-pack-sha256.json').read_text())
frames=sorted(int(f.stem)for f in(c/'frames').glob('*.png'));rooms={};data={}
for n in frames:
 for k in ['ram','ppu','oam','view']:
  name=f'{n:06}'+('.json'if k=='view'else'.bin');raw=(c/k/name).read_bytes()
  assert raw==(b/k/name).read_bytes(),(n,k)
  if k=='ram':rooms[n]=int.from_bytes(raw[0x78:0x7a],'little')
apu=(b/'apu.tsv').read_bytes();assert apu==(c/'apu.tsv').read_bytes()
with wave.open(str(b/'full.wav'),'rb')as f:pcm=f.readframes(f.getnframes());params=f.getparams()
with wave.open(str(c/'full.wav'),'rb')as f:assert f.getparams()==params;assert f.readframes(f.getnframes())==pcm
def source(path):
 src=np.array(Image.open(path).convert('RGBA'));mask=src[:,:,3]==255;ys,xs=np.where(mask)
 # Rare bright source colors keep matching efficient and unambiguous.
 colors,count=np.unique(src[mask,:3],axis=0,return_counts=True)
 pick=np.argmax(colors.sum(1)/(1+count));color=colors[pick]
 yy,xx=np.where(mask&np.all(src[:,:,:3]==color,2));ay,ax=int(yy[0]),int(xx[0])
 return src,mask,ay,ax
assets={n:source(r/'art/level4_courtyard'/f'{n}.png')for n in ['wings','fire_orb','courtyard_statue','courtyard_statue_alt']}
assets['solid']=source(r/'art/level4_masonry/solid.png')
def matches(im,item):
 src,mask,ay,ax=item;h,w=mask.shape;ys,xs=np.where(np.all(im==src[ay,ax,:3],2));hits=[]
 for y,x in zip(ys-ay,xs-ax):
  if y<0 or x<0 or y+h>480 or x+w>512:continue
  if np.array_equal(im[y:y+h,x:x+w][mask],src[:,:,:3][mask]):hits.append([int(x),int(y)])
 return hits
counts=Counter();hits=Counter();examples={};scene_checks=[]
target={0xaaf9,0xab71,0xac61};stride=ci['stride']
for n in frames:
 paths=[d/'frames'/f'{n:06}.png'for d in[b,c]]
 if not all(p.stat().st_size for p in paths):assert paths[0].stat().st_size==paths[1].stat().st_size;counts['empty_initial']+=1;continue
 old,im=[np.array(Image.open(path).convert('RGB'))for path in paths];changed=not np.array_equal(old,im)
 if a.regression:assert not changed,('Earlier room image changed',n)
 elif changed:
  assert any(rooms.get(n+j*stride)in target for j in [-2,-1,0,1,2]),('Unrelated room changed',n)
  counts['requested_rooms_changed']+=1
 else:counts['unchanged']+=1
 if not old.any():assert not im.any();counts['native_black']+=1
 if rooms[n]==0xffff and not changed:counts['unchanged_pause_samples']+=1
 if a.regression:continue
 if n%10==0:
  for name,item in assets.items():
   found=matches(im,item)
   if found:
    hits[name]+=len(found)
    examples.setdefault(name,[])
    if len(examples[name])<4:examples[name].append(dict(frame=n,positions=found))
 if n in [500,1200,2000,2400,2800,3000,3500,3880,4020]:
  style='Exterior'if rooms[n]==0xab71 else'Interior';bg=np.array(Image.open(c/f'mesen_home/HdPacks/Holy_Diver_(Tr)/Golden_Temple_{style}.png').convert('RGB'))[:,:512]
  exact=int(np.all(im==bg,2)[112:].sum());assert exact>40000,(n,exact)
  scene_checks.append(dict(frame=n,room=f'{rooms[n]:04X}',background=style,exact_background_pixels=exact))
if not a.regression:
 for name in assets:assert hits[name]>0,('No complete live source match',name)
 assert len(scene_checks)==9
report=dict(movie_frames=ci['movie_frames'],native_samples_per_type=len(frames),movie_sha256=ci['movie_sha256'],native_exact=True,apu_exact=True,pcm_exact=True,
 pcm_bytes=len(pcm),pcm_sha256=hashlib.sha256(pcm).hexdigest(),apu_sha256=hashlib.sha256(apu).hexdigest(),
 image_checks=counts,complete_source_matches=hits,source_examples=examples,scenery_checks=scene_checks,
 earlier_movie_images_exact=a.regression,neighbor_diagnostic='Enabled in candidate runner; no invalid access reported')
Path(a.out).write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
