"""Actual paired movie checks for the scoped Palace repair."""
from pathlib import Path
from collections import Counter
import argparse,json,hashlib,wave
import numpy as np
from PIL import Image
p=argparse.ArgumentParser()
for k in ['before','after','out']:p.add_argument('--'+k,required=True)
p.add_argument('--opening',action='store_true');a=p.parse_args();r=Path(__file__).resolve().parents[1];b,c=Path(a.before),Path(a.after)
infos=[json.loads((d/'result.json').read_text())for d in [b,c]]
for k in ['movie_sha256','rom_sha1','core_sha256','movie_frames','captured_frames','stride']:assert infos[0][k]==infos[1][k],k
assert all(v['movie_completed']for v in infos)
for d,ver in [(b,'0.21.0'),(c,'0.21.1')]:assert json.loads((d/'installed_pack.json').read_text())==json.loads((r/f'evidence/{ver}-pack-sha256.json').read_text())
frames=sorted(int(f.stem)for f in(c/'frames').glob('*.png'));data={k:{}for k in ['ram','ppu','oam','view']}
for n in frames:
 for k in data:
  name=f'{n:06}'+('.json'if k=='view'else'.bin');raw=(c/k/name).read_bytes();assert raw==(b/k/name).read_bytes(),(n,k);data[k][n]=json.loads(raw)if k=='view'else raw
apu=(c/'apu.tsv').read_bytes();assert apu==(b/'apu.tsv').read_bytes()
with wave.open(str(b/'full.wav'),'rb')as f:pcm=f.readframes(f.getnframes());params=f.getparams()
with wave.open(str(c/'full.wav'),'rb')as f:assert f.getparams()==params and f.readframes(f.getnframes())==pcm
bg=np.array(Image.open(r/'build/Holy_Diver_(Tr)/Demonic_Palace_Interior.png').convert('RGB'))[:,:512]
def roof_mask(n):
 allowed=np.zeros((480,512),bool)
 for j in [n-2,n,n+2]:
  if j not in data['ram']or data['ram'][j][0x78:0x7a]!=b'\x0a\x85':continue
  pp,v=data['ppu'][j],data['view'][j];vv=v['vram'];sx=(vv&31)*8+v['xscroll']+(256 if vv&0x400 else 0);sy=((vv>>5)&31)*8+((vv>>12)&7)+(240 if vv&0x800 else 0)
  for yy in range(sy//8,(sy+239)//8+1):
   for xx in range(sx//8,(sx+255)//8+1):
    tx,ty=xx%32,yy%30;nt=0x2000+xx//32%2*0x400+yy//30%2*0x800;t=pp[nt+ty*32+tx]
    if t not in [1,2,3,4,0x1d,0x1e,0x1f,0x20]:continue
    at=pp[nt+960+ty//4*8+tx//4];pa=at>>((ty%4)//2*4+(tx%4)//2*2)&3;pal=(pp[0x3f00:0x3f01]+pp[0x3f01+pa*4:0x3f04+pa*4]).hex()
    if pal!='0f182819':continue
    x,y=(xx*8-sx)*2,(yy*8-sy)*2;allowed[max(0,y-4):min(480,y+20),max(0,x-4):min(512,x+20)]=True
 return allowed

def source(path):
 src=np.array(Image.open(path).convert('RGBA'));mask=src[:,:,3]==255;colors,counts=np.unique(src[mask,:3],axis=0,return_counts=True);color=colors[np.argmax(colors.sum(1)/(1+counts))];yy,xx=np.where(mask&np.all(src[:,:,:3]==color,2));pts=np.argwhere(mask)
 return src,mask,int(yy[0]),int(xx[0]),pts[np.linspace(0,len(pts)-1,8,dtype=int)]
def matches(im,item):
 src,mask,ay,ax,probes=item;h,w=mask.shape;yy,xx=np.where(np.all(im==src[ay,ax,:3],2));yy-=ay;xx-=ax;v=(yy>=0)&(xx>=0)&(yy+h<=480)&(xx+w<=512);yy,xx=yy[v],xx[v]
 for py,px in probes:
  v=np.all(im[yy+py,xx+px]==src[py,px,:3],1);yy,xx=yy[v],xx[v]
  if not len(yy):return []
 return [[int(x),int(y)]for y,x in zip(yy,xx)if np.array_equal(im[y:y+h,x:x+w][mask],src[:,:,:3][mask])]
sources={name:source(r/'art/level5'/(name+'.png'))for name in ['serpent_head','serpent_segment']};hits={};counts=Counter();rooms=Counter();background_counts=[];changed=[];green=0
for n in frames:
 paths=[d/'frames'/f'{n:06}.png'for d in [b,c]]
 if not all(v.stat().st_size for v in paths):assert paths[0].stat().st_size==paths[1].stat().st_size;counts['empty_initial']+=1;continue
 old,im=[np.array(Image.open(v).convert('RGB'))for v in paths];diff=np.any(old!=im,2);counts['changed'if diff.any()else'identical']+=1
 if diff.any():changed.append(n)
 ram=data['ram'][n];room=f'{int.from_bytes(ram[0x78:0x7a],"little"):04X}';rooms[room]+=1
 if not old.any():
  assert not im.any();counts['native_black_exact']+=1
  if not a.opening:continue
 if a.opening:
  if room=='850A' or (diff.any()and any(data['ram'][j][0x78:0x7a]==b'\x0a\x85'for j in [n-2,n+2]if j in data['ram'])):
   if diff.any():
    mask=roof_mask(n);assert not diff[~mask].any(),(n,'outside roof',int(diff[~mask].sum()));counts['roof_only']+=1
    rgb=im.astype(np.int16);green+=int((diff&(rgb[:,:,1]>rgb[:,:,0]+8)&(rgb[:,:,1]>rgb[:,:,2]+5)).sum())
  elif room!='8816':assert not diff.any(),(n,room,'unrelated room changed');counts['other_room_exact']+=1
 else:
  assert room in ['8816','888E']
  pixels=int(np.all(im==bg,2).sum());background_counts.append(pixels);assert pixels>70000,(n,'background missing',pixels)
  if n%4==0 and room=='8816':
   for name,item in sources.items():
    if name in hits:continue
    pos=matches(im,item)
    if pos:hits[name]=dict(frame=n,positions=pos)
if a.opening:assert counts['roof_only']>100 and green>100000
else:assert len(hits)==2
report=dict(movie=infos[1],native_samples_per_type=len(frames),native_exact=True,apu_exact=True,pcm_exact=True,apu_sha256=hashlib.sha256(apu).hexdigest(),pcm_sha256=hashlib.sha256(pcm).hexdigest(),images=counts,rooms=rooms,green_ceiling_pixels=green,background_visible_every_nonblack_sample=True if not a.opening else None,minimum_background_pixels=min(background_counts)if background_counts else None,live_whole_serpent_matches=hits,changed_frames=changed)
Path(a.out).write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:v for k,v in report.items()if k!='changed_frames'},indent=2))
