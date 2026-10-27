"""Paired native/audio checks and source matches in actual Mesen captures."""
from pathlib import Path
from collections import Counter
import argparse, hashlib, json, wave
import numpy as np
from PIL import Image, ImageOps

p=argparse.ArgumentParser()
for key in ['before','after','out']:p.add_argument('--'+key,required=True)
p.add_argument('--regression',action='store_true');a=p.parse_args()
r=Path(__file__).resolve().parents[1];b,c=Path(a.before),Path(a.after)
bi,ci=[json.loads((d/'result.json').read_text())for d in [b,c]]
for k in ['movie_sha256','rom_sha1','core_sha256','movie_frames','captured_frames','stride']:assert bi[k]==ci[k],k
assert bi['movie_completed'] and ci['movie_completed'] and ci['stride']==1
for d,version in [(b,'0.19.1'),(c,'0.20.0')]:
 assert json.loads((d/'installed_pack.json').read_text())==json.loads((r/f'evidence/{version}-pack-sha256.json').read_text())
frames=sorted(int(f.stem)for f in(c/'frames').glob('*.png'));data={k:{}for k in ['ram','ppu','oam','view']}
for n in frames:
 for k in data:
  name=f'{n:06}'+('.json'if k=='view'else'.bin');raw=(c/k/name).read_bytes();assert raw==(b/k/name).read_bytes(),(n,k)
  data[k][n]=json.loads(raw)if k=='view'else raw
apu=(b/'apu.tsv').read_bytes();assert apu==(c/'apu.tsv').read_bytes()
with wave.open(str(b/'full.wav'),'rb')as f:pcm=f.readframes(f.getnframes());params=f.getparams()
with wave.open(str(c/'full.wav'),'rb')as f:assert f.getparams()==params;assert f.readframes(f.getnframes())==pcm
rooms={n:int.from_bytes(d[0x78:0x7a],'little')for n,d in data['ram'].items()}

def source(im):
 src=np.array(im.convert('RGBA'));mask=src[:,:,3]==255
 colors,counts=np.unique(src[mask,:3],axis=0,return_counts=True);color=colors[np.argmax(colors.sum(1)/(1+counts))]
 yy,xx=np.where(mask&np.all(src[:,:,:3]==color,2));opaque=np.argwhere(mask);probes=opaque[np.linspace(0,len(opaque)-1,8,dtype=int)]
 return src,mask,int(yy[0]),int(xx[0]),probes

def matches(im,packed,item):
 src,mask,ay,ax,probes=item;h,w=mask.shape;color=src[ay,ax,:3].astype(np.uint32);anchor=int(color[0]<<16|color[1]<<8|color[2]);ys,xs=np.where(packed==anchor);ys-=ay;xs-=ax;hits=[]
 valid=(ys>=0)&(xs>=0)&(ys+h<=480)&(xs+w<=512);ys,xs=ys[valid],xs[valid]
 # Cheap exact rejections avoid copying a whole masked image for every
 # occurrence of a common gold pixel. Surviving candidates still require
 # every opaque source pixel to match, exactly as before.
 for py,px in probes:
  valid=np.all(im[ys+py,xs+px]==src[py,px,:3],1);ys,xs=ys[valid],xs[valid]
  if not len(ys):return hits
 for y,x in zip(ys,xs):
  if np.array_equal(im[y:y+h,x:x+w][mask],src[:,:,:3][mask]):hits.append([int(x),int(y)])
 return hits

art=r/'art/level4_finale';assets={}
for phase in range(8):
 for pal in ['0F071727','0F001030']:assets[f'band_{phase}_{pal}']=source(Image.open(art/f'tower_band_{phase}_{pal}.png'))
for phase in range(2):
 im=Image.open(art/f'ring_{phase}.png')
 for mirror in [False,True]:assets[f'ring_{phase}_{mirror}']=source(ImageOps.mirror(im)if mirror else im)
assets['platform']=source(Image.open(art/'moving_platform.png'))
for phase in range(4):
 for pal in ['FF061530','FF102030','FF122232']:
  im=Image.open(r/f'art/level4_staff/sentinel_{phase}_{pal}.png')
  for mirror in [False,True]:assets[f'sentinel_{phase}_{pal}_{mirror}']=source(ImageOps.mirror(im)if mirror else im)
bg=np.array(Image.open(r/'build/Holy_Diver_(Tr)/Golden_Temple_Interior.png').convert('RGB'))[:,:512]
dim=((bg.astype(np.uint16)+1)*127>>8).astype(np.uint8)
counts=Counter();hits=Counter();examples={};scene_counts=Counter();scene_min={};changed_pixels=0
# Cover all consecutive native death fragments, not a same-parity sample.
death=[]
for n,oam in data['oam'].items():
 if rooms[n]!=0xafa9:continue
 for off in range(0,256,4):
  y,t,attr,x=oam[off:off+4]
  if y<239 and 0x64<=t<=0x73:death.append((x*2,(y+1)*2,min(512,(x+8)*2),min(480,(y+9)*2)))
death_box=[min(v[0]for v in death),min(v[1]for v in death),max(v[2]for v in death),max(v[3]for v in death)]if death else None
for n in frames:
 paths=[d/'frames'/f'{n:06}.png'for d in [b,c]]
 if not all(f.stat().st_size for f in paths):assert paths[0].stat().st_size==paths[1].stat().st_size;counts['empty_initial']+=1;continue
 old,im=[np.array(Image.open(f).convert('RGB'))for f in paths];diff=np.any(old!=im,2);changed_pixels+=int(diff.sum())
 counts['changed'if diff.any()else'unchanged']+=1
 if a.regression:
  allowed=np.zeros((480,512),bool)
  for j in [n-1,n,n+1]:
   oam=data['oam'].get(j,bytes(256))
   for off in range(0,256,4):
    y,t,attr,x=oam[off:off+4]
    if y<239 and 0xb6<=t<=0xbd:allowed[max(0,y*2-4):min(480,(y+10)*2+4),max(0,x*2-4):min(512,(x+8)*2+4)]=True
  assert not diff[~allowed].any(),('Earlier change outside native rings',n)
 else:
  if diff.any():assert any(rooms.get(j)in {0xae41,0xaef5,0xafa9}for j in [n-1,n,n+1]),('Outside new rooms',n)
  if not old.any():assert not im.any(),('Native black frame changed',n);counts['native_black']+=1;continue
  mask=np.zeros((480,512),bool);is_death=False
  for j in [n-1,n,n+1]:
   oam=data['oam'].get(j,bytes(256))
   for off in range(0,256,4):
    y,t,attr,x=oam[off:off+4]
    if y<239:
     mask[max(0,y*2):min(480,(y+10)*2),max(0,x*2-2):min(512,(x+9)*2)]=True
     if rooms.get(j)==0xafa9 and 0x64<=t<=0x73:is_death=True
  if is_death and death_box:
   x0,y0,x1,y1=death_box;mask[y0:y1,x0:x1]=True
  if not old[~mask].any():
   assert not im[~mask].any(),('Native background disable changed',n)
   counts['native_background_disabled']+=1;continue
  room=rooms[n];stable=all(rooms.get(j)==room for j in [n-1,n+1])and not data['view'][n]['grayscale']
  pal=data['ppu'][n][0x3f00:0x3f10].hex()
  expected=(room in [0xae41,0xaef5]and pal=='0f1727370f0717230f0717370f031323')or(room==0xafa9 and pal in ['0f0717270f0717370f0313230f071727','0f0717270f0717370f0313230f001030'])
  if stable and expected:
   exact=int(np.all(im==(dim if room==0xafa9 else bg),2)[112:].sum())
   assert exact>30000,('Missing panorama',n,hex(room),exact)
   key=f'{room:04X}';scene_counts[key]+=1;scene_min[key]=min(exact,scene_min.get(key,exact))
 if n%5==0:
  rgb=im.astype(np.uint32);packed=rgb[:,:,0]<<16|rgb[:,:,1]<<8|rgb[:,:,2]
  for name,item in assets.items():
   if name.startswith('band') and rooms[n]!=0xafa9:continue
   if name=='platform' and rooms[n]!=0xafa9:continue
   if name.startswith('sentinel') and rooms[n]not in [0xae41,0xaef5]:continue
   found=matches(im,packed,item)
   if found:
    hits[name]+=len(found);examples.setdefault(name,[])
    if len(examples[name])<3:examples[name].append(dict(frame=n,positions=found))
if not a.regression:
 for phase in range(8):
  for pal in ['0F071727','0F001030']:assert hits[f'band_{phase}_{pal}'],('Missing complete boss band',phase,pal)
 assert hits['platform']
 for phase in range(4):assert any(v for k,v in hits.items()if k.startswith(f'sentinel_{phase}_'))
 for pal in ['FF061530','FF102030','FF122232']:assert any(v for k,v in hits.items()if pal in k)
 for mirror in ['False','True']:assert any(v for k,v in hits.items()if k.startswith('sentinel')and k.endswith(mirror))
for phase in range(2):assert any(v for k,v in hits.items()if k.startswith(f'ring_{phase}_'))
report=dict(movie_sha256=ci['movie_sha256'],movie_frames=ci['movie_frames'],native_samples_per_type=len(frames),native_exact=True,apu_exact=True,pcm_exact=True,pcm_bytes=len(pcm),pcm_sha256=hashlib.sha256(pcm).hexdigest(),apu_sha256=hashlib.sha256(apu).hexdigest(),image_checks=counts,changed_pixels=changed_pixels,background_samples=scene_counts,minimum_exact_panorama_pixels=scene_min,complete_source_matches=hits,source_examples=examples,death_actor_extent=death_box,earlier_changes_confined_to_rings=a.regression,neighbor_diagnostic='Enabled; no invalid read',coverage_limit='Earlier dragon pickup/flight route; changes confined to updated rings'if a.regression else'Supplied movie ends with game over; boss defeat and later rooms are untested')
Path(a.out).write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
