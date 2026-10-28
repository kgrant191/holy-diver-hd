"""Pair native state/audio and inspect actual rendered Palace movie samples."""
from pathlib import Path
from collections import Counter
import argparse,json,hashlib,wave
import numpy as np
from PIL import Image
p=argparse.ArgumentParser()
for key in ['before','after','out']:p.add_argument('--'+key,required=True)
a=p.parse_args();r=Path(__file__).resolve().parents[1];b,c=Path(a.before),Path(a.after)
infos=[json.loads((d/'result.json').read_text())for d in [b,c]]
for k in ['movie_sha256','rom_sha1','core_sha256','movie_frames','captured_frames','stride']:assert infos[0][k]==infos[1][k],k
assert all(v['movie_completed']for v in infos)
for d,ver in [(b,'0.21.1'),(c,'0.22.0')]:assert json.loads((d/'installed_pack.json').read_text())==json.loads((r/f'evidence/{ver}-pack-sha256.json').read_text())
frames=sorted(int(f.stem)for f in(c/'frames').glob('*.png'));data={k:{}for k in ['ram','ppu','oam','view']}
for n in frames:
 for k in data:
  name=f'{n:06}'+('.json'if k=='view'else'.bin');raw=(c/k/name).read_bytes();assert raw==(b/k/name).read_bytes(),(n,k);data[k][n]=json.loads(raw)if k=='view'else raw
apu=(c/'apu.tsv').read_bytes();assert apu==(b/'apu.tsv').read_bytes()
with wave.open(str(b/'full.wav'),'rb')as f:pcm=f.readframes(f.getnframes());params=f.getparams()
with wave.open(str(c/'full.wav'),'rb')as f:assert f.getparams()==params and f.readframes(f.getnframes())==pcm
bg=np.array(Image.open(r/'build/Holy_Diver_(Tr)/Demonic_Palace_Interior.png').convert('RGB'))[:,:512]
# Match native scanline grayscale/emphasis, including the between-samples
# death flash. This is the exact HdNesPack::ProcessGrayscaleAndEmphasis math.
filtered=[]
for gray in [False,True]:
 base=np.repeat((bg.astype(np.uint16).sum(2)//3)[:,:,None],3,2)if gray else bg
 for bits in range(8):
  if not gray and not bits:continue
  factors=np.ones(3)
  for bit in range(3):
   if bits&(1<<bit):factors*=np.array([1.1 if channel==bit else .9 for channel in range(3)])
  filtered.append((gray,bits,np.minimum(base.astype(float)*factors,255).astype(np.uint8)))
def source(path,mirror=False):
 src=np.array(Image.open(path).convert('RGBA'))
 if mirror:src=src[:,::-1]
 mask=src[:,:,3]==255;colors,counts=np.unique(src[mask,:3],axis=0,return_counts=True);color=colors[np.argmax(colors.sum(1)/(1+counts))];yy,xx=np.where(mask&np.all(src[:,:,:3]==color,2));pts=np.argwhere(mask)
 return src,mask,int(yy[0]),int(xx[0]),pts[np.linspace(0,len(pts)-1,8,dtype=int)]
def matches(im,item):
 src,mask,ay,ax,probes=item;h,w=mask.shape;yy,xx=np.where(np.all(im==src[ay,ax,:3],2));yy-=ay;xx-=ax;v=(yy>=0)&(xx>=0)&(yy+h<=480)&(xx+w<=512);yy,xx=yy[v],xx[v]
 for py,px in probes:
  v=np.all(im[yy+py,xx+px]==src[py,px,:3],1);yy,xx=yy[v],xx[v]
  if not len(yy):return []
 return [[int(x),int(y)]for y,x in zip(yy,xx)if np.array_equal(im[y:y+h,x:x+w][mask],src[:,:,:3][mask])]
paths={'sentry':'level5_next/sentry.png','guardian':'level4/guardian.png','walking_dragon_0':'screen2_6/dragon_pose_0.png','walking_dragon_1':'screen2_6/dragon_pose_1.png'}
sources={name:[source(r/'art'/path,mirror)for mirror in [False,True]]for name,path in paths.items()};hits={};counts=Counter();rooms=Counter();backgrounds={};changed=[];dropout_fixes=[]
def sprite_envelope(old):
 mask=np.zeros((480,512),bool)
 # On death the submitted picture can contain the previous Randy position
 # while sampled OAM has already jumped. Bound actual native sprite pixels.
 for y,row in enumerate(np.any(old!=0,2)):
  xs=np.flatnonzero(row)
  if len(xs):mask[max(0,y-32):min(480,y+33),max(0,int(xs[0])-32):min(512,int(xs[-1])+33)]=True
 return mask
pose_frames={'walking_dragon_0':1988,'walking_dragon_1':1996,'sentry':2552,'guardian':5500}
for n in frames:
 paths=[d/'frames'/f'{n:06}.png'for d in [b,c]]
 if not all(v.stat().st_size for v in paths):assert paths[0].stat().st_size==paths[1].stat().st_size;counts['empty_initial']+=1;continue
 old,im=[np.array(Image.open(v).convert('RGB'))for v in paths];diff=np.any(old!=im,2);counts['changed'if diff.any()else'identical']+=1
 if diff.any():changed.append(n)
 ram=data['ram'][n];room=f'{int.from_bytes(ram[0x78:0x7a],"little"):04X}';rooms[room]+=1
 if not old.any():assert not im.any(),(n,'native blackout changed');counts['native_black_exact']+=1;continue
 if room in ['FFFF','0000']:
  # EndFrame state can lead submitted video by one frame at transitions.
  if all(f'{int.from_bytes(data["ram"][j][0x78:0x7a],"little"):04X}'==room for j in [n-2,n+2]if j in data['ram']):
   assert not diff.any(),(n,room,'stable menu/death card changed');counts['menu_and_lives_exact']+=1
  continue
 assert room in ['888E','897E','8A6E']
 pp=data['ppu'][n];pal=pp[0x3f00:0x3f04].hex();pixels=int(np.all(im==bg,2).sum());before_pixels=int(np.all(old==bg,2).sum())
 if pixels<=10000:
  # Native death/restart can disable only scenery, retaining HUD and Randy.
  # Require its black field and exclude it from panorama coverage claims.
  if np.any(old!=0,2).sum()<10000:
   envelope=sprite_envelope(old)
   assert not im[~envelope].any(),(n,'native disabled background changed')
   assert np.any(im!=0,2).sum()<15000,(n,'native sprite-only field filled')
   counts['native_background_disabled_exact']+=1;continue
 if pal in ['0f0f0717','0f071727']and pixels<=10000:
  for gray,bits,variant in filtered:
   count=int(np.all(im==variant,2).sum())
   if count>10000:
    pixels=count;before_pixels=int(np.all(old==variant,2).sum());counts[f'native_filter_gray{int(gray)}_emphasis{bits}']+=1;break
 if pal in ['0f0f0717','0f071727'] and pixels>10000:
  backgrounds.setdefault(room,[]).append(pixels)
  if before_pixels<1000:dropout_fixes.append(n)
 elif pal in ['0f0f0717','0f071727']:
  # Only transition submissions may still be native black/menu pictures.
  adjacent=[data['ppu'][j][0x3f00:0x3f04].hex()for j in [n-2,n+2]if j in data['ppu']]
  assert any(v not in ['0f0f0717','0f071727']for v in adjacent),(n,room,'missing panorama',pixels)
  counts['transition_submission']+=1
 if n in pose_frames.values():
  for name,variants in sources.items():
   if n!=pose_frames[name]:continue
   for mirror,item in enumerate(variants):
    positions=matches(im,item)
    if positions:hits[name]=dict(frame=n,mirrored=bool(mirror),positions=positions);break
assert set(hits)==set(sources),hits
assert len(dropout_fixes)>100 and all(len(backgrounds[k])>100 for k in ['888E','897E','8A6E'])
report=dict(movie=infos[1],native_samples_per_type=len(frames),native_exact=True,apu_exact=True,pcm_exact=True,apu_sha256=hashlib.sha256(apu).hexdigest(),pcm_sha256=hashlib.sha256(pcm).hexdigest(),images=counts,rooms=rooms,backgrounds={k:dict(samples=len(v),minimum_pixels=min(v))for k,v in backgrounds.items()},restored_background_samples=len(dropout_fixes),live_whole_source_matches=hits,changed_frames=changed)
Path(a.out).write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:v for k,v in report.items()if k!='changed_frames'},indent=2))
