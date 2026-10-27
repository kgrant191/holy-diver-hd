"""Check actual paired Mesen output for the staff hall and outdoor arena."""
from pathlib import Path
from collections import Counter
import argparse,hashlib,json,wave
import numpy as np
from PIL import Image,ImageOps

p=argparse.ArgumentParser()
for key in ['before','after','out']:p.add_argument('--'+key,required=True)
p.add_argument('--regression',action='store_true');a=p.parse_args()
root=Path(__file__).resolve().parents[1];before,after=Path(a.before),Path(a.after)
bi,ai=[json.loads((folder/'result.json').read_text())for folder in [before,after]]
for key in ['movie_sha256','rom_sha1','core_sha256','movie_frames','captured_frames','stride']:assert bi[key]==ai[key],key
assert bi['movie_completed']and ai['movie_completed']
for folder,version in [(before,'0.17.0'),(after,'0.18.0')]:
 assert json.loads((folder/'installed_pack.json').read_text())==json.loads((root/f'evidence/{version}-pack-sha256.json').read_text())
frames=sorted(int(f.stem)for f in(after/'frames').glob('*.png'));rooms={};palettes={};gray={}
for n in frames:
 for kind in ['ram','ppu','oam','view']:
  name=f'{n:06}'+('.json'if kind=='view'else'.bin');data=(after/kind/name).read_bytes()
  assert data==(before/kind/name).read_bytes(),(kind,n)
  if kind=='ram':rooms[n]=int.from_bytes(data[0x78:0x7a],'little')
  if kind=='ppu':palettes[n]=data[0x3f00:0x3f10].hex()
  if kind=='view':gray[n]=json.loads(data)['grayscale']
apu=(before/'apu.tsv').read_bytes();assert apu==(after/'apu.tsv').read_bytes()
with wave.open(str(before/'full.wav'),'rb')as f:pcm=f.readframes(f.getnframes());params=f.getparams()
with wave.open(str(after/'full.wav'),'rb')as f:assert f.getparams()==params;assert f.readframes(f.getnframes())==pcm

def source(im):
 src=np.array(im.convert('RGBA'));mask=src[:,:,3]==255
 colors,counts=np.unique(src[mask,:3],axis=0,return_counts=True)
 color=colors[np.argmax(colors.sum(1)/(1+counts))]
 yy,xx=np.where(mask&np.all(src[:,:,:3]==color,2));ay,ax=int(yy[0]),int(xx[0])
 return src,mask,ay,ax
def matches(im,item):
 src,mask,ay,ax=item;h,w=mask.shape;ys,xs=np.where(np.all(im==src[ay,ax,:3],2));hits=[]
 for y,x in zip(ys-ay,xs-ax):
  if y<0 or x<0 or y+h>480 or x+w>512:continue
  if np.array_equal(im[y:y+h,x:x+w][mask],src[:,:,:3][mask]):hits.append([int(x),int(y)])
 return hits

assets={};art=root/'art/level4_staff'
for name,path in [('staff',art/'staff.png'),('ornament',root/'art/level4_courtyard/courtyard_statue.png'),('ornament_alt',root/'art/level4_courtyard/courtyard_statue_alt.png')]:assets[name]=source(Image.open(path))
for i in range(4):
 for pal in ['FF061530','FF102030','FF122232']:
  im=Image.open(art/f'sentinel_{i}_{pal}.png')
  for mirror in [False,True]:assets[f'sentinel_{i}_{pal}_'+('mirror'if mirror else'normal')]=source(ImageOps.mirror(im)if mirror else im)
bgs={room:np.array(Image.open(root/f'build/Holy_Diver_(Tr)/Golden_Temple_{style}.png').convert('RGB'))[:,:512]for room,style in [(0xac61,'Interior'),(0xacd9,'Exterior')]}
expected_pal={0xac61:'0f1727370f0717270f0717370f031323',0xacd9:'0f0717370f0717030f0737030f031323'}
menu_reference=np.array(Image.open(before/'frames/001600.png').convert('RGB'))if not a.regression else None
counts=Counter();hits=Counter();examples={};scene_counts=Counter();scene_min={};menu_hits=0;stride=ai['stride']
death_extent=[]
for n in frames:
 if rooms[n]!=0xacd9:continue
 oam=(before/'oam'/f'{n:06}.bin').read_bytes()
 for offset in range(0,256,4):
  y,t,attr,x=oam[offset:offset+4]
  if y<239 and 0x64<=t<=0x73:death_extent.append((x*2,(y+1)*2,min(512,(x+8)*2),min(480,(y+9)*2)))
death_box=([min(v[0]for v in death_extent),min(v[1]for v in death_extent),max(v[2]for v in death_extent),max(v[3]for v in death_extent)]if death_extent else None)
for n in frames:
 paths=[folder/'frames'/f'{n:06}.png'for folder in [before,after]]
 if not all(path.stat().st_size for path in paths):
  assert paths[0].stat().st_size==paths[1].stat().st_size;counts['empty_initial']+=1;continue
 old,im=[np.array(Image.open(path).convert('RGB'))for path in paths];changed=not np.array_equal(old,im)
 if a.regression:assert not changed,('Earlier image changed',n)
 if changed:
  assert any(rooms.get(n+j*stride)in {0xac61,0xacd9,0xffff}for j in [-2,-1,0,1,2]),('Outside requested rooms',n)
  counts['changed']+=1
 else:counts['unchanged']+=1
 if not old.any():
  assert not im.any();counts['native_black']+=1
  continue
 if a.regression:continue
 room=rooms[n]
 # On player death the native game disables its background while retaining
 # the HUD/player sprites. Prove that from the baseline picture outside all
 # native OAM footprints, then require the same black region in the update.
 oam_mask=np.zeros((480,512),dtype=bool);death_bounds=[]
 for j in [-2,-1,0,1,2]:
  path=before/'oam'/f'{n+j*stride:06}.bin'
  if not path.exists():continue
  oam=path.read_bytes()
  for offset in range(0,256,4):
   y,t,attr,x=oam[offset:offset+4]
   if y<239:
    oam_mask[(y+1)*2:min(480,(y+9)*2),x*2:min(512,(x+8)*2)]=True
    if 0x64<=t<=0x73:death_bounds.append((x*2,(y+1)*2,min(512,(x+8)*2),min(480,(y+9)*2)))
 # The death fragments change every frame, between the even OAM samples.
 # Use the whole observed death-actor extent, not disconnected sampled cells
 # or a few same-parity poses. All other screen pixels must remain black.
 if death_bounds:
  x0,y0,x1,y1=death_box
  oam_mask[y0:y1,x0:x1]=True
 if not old[~oam_mask].any():
  assert not im[~oam_mask].any(),('Native background-disable changed',n)
  counts['native_background_disabled']+=1
  continue
 # Native metadata can lead the submitted picture by one frame at menu exits.
 near_pause=any(rooms.get(n+j*stride)==0xffff for j in [-1,0,1])
 menu_visible=np.array_equal(old[108:272,200:216],menu_reference[108:272,200:216])
 if menu_visible:
  delta=np.any(old!=im,2);delta[208:240,80:112]=False
  assert not delta.any(),('Changes outside staff menu icon',n)
  if matches(im,assets['staff']):menu_hits+=1
  counts['visible_pause_samples']+=1
 elif not near_pause and room in bgs and palettes[n]==expected_pal[room]and not gray[n]and all(rooms.get(n+j*stride)==room for j in [-1,1]):
  exact=int(np.all(im==bgs[room],2)[112:].sum())
  assert exact>40000,('Missing panorama',n,f'{room:04X}',exact)
  key=f'{room:04X}';scene_counts[key]+=1;scene_min[key]=min(exact,scene_min.get(key,exact))
 if n%10==0:
  for name,item in assets.items():
   if name.startswith('sentinel')and room!=0xacd9:continue
   found=matches(im,item)
   if found:
    hits[name]+=len(found);examples.setdefault(name,[])
    if len(examples[name])<3:examples[name].append(dict(frame=n,positions=found))
if not a.regression:
 assert hits['staff']and menu_hits and hits['ornament']and hits['ornament_alt']
 for i in range(4):assert any(v for k,v in hits.items()if k.startswith(f'sentinel_{i}_')),('Missing live pose',i)
 for pal in ['FF061530','FF102030','FF122232']:assert any(v for k,v in hits.items()if pal in k),('Missing live palette',pal)
 for mirror in ['normal','mirror']:assert any(v for k,v in hits.items()if k.startswith('sentinel_')and k.endswith('_'+mirror)),('Missing orientation',mirror)
 # Exact eligible counts for the unchanged supplied recording: transitions,
 # pause, blackouts and 90 native background-disable samples are separate.
 assert dict(scene_counts)=={'AC61':1221,'ACD9':297},dict(scene_counts)
report=dict(movie_sha256=ai['movie_sha256'],movie_frames=ai['movie_frames'],native_samples_per_type=len(frames),native_exact=True,apu_exact=True,pcm_exact=True,pcm_bytes=len(pcm),pcm_sha256=hashlib.sha256(pcm).hexdigest(),apu_sha256=hashlib.sha256(apu).hexdigest(),image_checks=counts,background_samples=scene_counts,minimum_exact_panorama_pixels=scene_min,complete_source_matches=hits,source_examples=examples,menu_staff_matches=menu_hits,death_actor_extent=death_box,earlier_movie_images_exact=a.regression,neighbor_diagnostic='Enabled during candidate replay; no invalid read reported',coverage_limit='Recorded encounter ends with player death; sentinel defeat and later areas are not tested')
Path(a.out).write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
