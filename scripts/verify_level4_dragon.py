"""Pair native state/audio and bound visual changes to requested artwork."""
from pathlib import Path
from collections import Counter
import argparse,json,hashlib,wave
import numpy as np
from PIL import Image,ImageOps
p=argparse.ArgumentParser()
for k in ['before','after','out']:p.add_argument('--'+k,required=True)
a=p.parse_args();r=Path(__file__).resolve().parents[1];b,c=Path(a.before),Path(a.after)
bi,ci=[json.loads((d/'result.json').read_text())for d in [b,c]]
for k in ['movie_sha256','rom_sha1','core_sha256','movie_frames','captured_frames','stride']:assert bi[k]==ci[k],k
assert bi['movie_completed']and ci['movie_completed'];stride=ci['stride']
for folder,version in [(b,'0.18.0'),(c,'0.19.0')]:assert json.loads((folder/'installed_pack.json').read_text())==json.loads((r/f'evidence/{version}-pack-sha256.json').read_text())
frames=sorted(int(f.stem)for f in(c/'frames').glob('*.png'));data={k:{}for k in ['ram','ppu','oam','view']}
for n in frames:
 for k in data:
  name=f'{n:06}'+('.json'if k=='view'else'.bin');raw=(c/k/name).read_bytes();assert raw==(b/k/name).read_bytes(),(n,k);data[k][n]=json.loads(raw)if k=='view'else raw
apu=(b/'apu.tsv').read_bytes();assert apu==(c/'apu.tsv').read_bytes()
with wave.open(str(b/'full.wav'),'rb')as f:pcm=f.readframes(f.getnframes());params=f.getparams()
with wave.open(str(c/'full.wav'),'rb')as f:assert f.getparams()==params;assert f.readframes(f.getnframes())==pcm
rooms={n:int.from_bytes(v[0x78:0x7a],'little')for n,v in data['ram'].items()};temple={0xa865,0xaa09,0xaa81,0xaaf9,0xab71,0xac61,0xacd9}
reg=json.loads((r/'art/level4_dragon/registration.json').read_text());columns={int(m['tile'],16)&255 for m in reg['mappings']if 'column reveal'in m['kind']}

def allowed(n):
 mask=np.zeros((480,512),bool);pad=stride*2+2
 for j in [n-stride,n,n+stride]:
  if j not in data['ram']:continue
  room=rooms[j];pp,v,ram=[data[k][j]for k in ['ppu','view','ram']]
  if room==0xffff:mask[208:240,80:112]=True;continue
  if room not in temple:continue
  vv=v['vram'];sx=(vv&31)*8+v['xscroll']+(256 if vv&0x400 else 0);sy=((vv>>5)&31)*8+((vv>>12)&7)+(240 if vv&0x800 else 0)
  for yy in range(sy//8,(sy+239)//8+1):
   for xx in range(sx//8,(sx+255)//8+1):
    tx,ty=xx%32,yy%30;nt=0x2000+xx//32%2*0x400+yy//30%2*0x800
    if pp[nt+ty*32+tx]not in columns and not(room==0xacd9 and pp[0x3f00]==0x31):continue
    X,Y=(xx*8-sx)*2,(yy*8-sy)*2;mask[max(0,Y-pad):min(480,Y+16+pad),max(0,X-pad):min(512,X+16+pad)]=True
  oam=data['oam'][j]
  for offset in range(0,256,4):
   y,t,attr,x=oam[offset:offset+4]
   changed=t in [0x47,0x48,0x95,0x96]or(room==0xacd9 and (0x94<=t<=0xb4 or t==0x74))
   if y>=239 or not changed:continue
   X,Y=x*2,(y+1)*2;mask[max(0,Y-pad):min(480,Y+16+pad),max(0,X-pad):min(512,X+16+pad)]=True
 return mask

def source(im):
 src=np.array(im.convert('RGBA'));mask=src[:,:,3]==255;colors,counts=np.unique(src[mask,:3],axis=0,return_counts=True);color=colors[np.argmax(colors.sum(1)/(1+counts))];yy,xx=np.where(mask&np.all(src[:,:,:3]==color,2));return src,mask,int(yy[0]),int(xx[0])
def matches(im,item):
 src,mask,ay,ax=item;h,w=mask.shape;ys,xs=np.where(np.all(im==src[ay,ax,:3],2));hits=[]
 for y,x in zip(ys-ay,xs-ax):
  if y<0 or x<0 or y+h>480 or x+w>512:continue
  if np.array_equal(im[y:y+h,x:x+w][mask],src[:,:,:3][mask]):hits.append([int(x),int(y)])
 return hits
art=r/'art/level4_dragon';assets={name:source(Image.open(art/(name+'.png')))for name in ['staff','heart','magic','dragon_pickup','dragon_shot','transform_star']}
for i in range(3):
 for flip in [False,True]:
  im=Image.open(art/f'pose_{i}.png');assets[f'dragon_{i}_'+('left'if flip else'right')]=source(ImageOps.mirror(im)if flip else im)
bgs={room:np.array(Image.open(c/f'mesen_home/HdPacks/Holy_Diver_(Tr)/Golden_Temple_{style}.png').convert('RGB'))[:,:512]for room,style in [(x,'Exterior'if x in {0xa865,0xab71,0xacd9}else'Interior')for x in temple]}
counts=Counter();hits=Counter();examples={};background=Counter();flash=0
for n in frames:
 paths=[d/'frames'/f'{n:06}.png'for d in [b,c]]
 if not all(f.stat().st_size for f in paths):assert paths[0].stat().st_size==paths[1].stat().st_size;counts['empty_initial']+=1;continue
 old,im=[np.array(Image.open(f).convert('RGB'))for f in paths];diff=np.any(old!=im,2)
 if diff.any():
  bad=diff&~allowed(n)
  assert not bad.any(),('outside requested artwork',n,int(bad.sum()),np.argwhere(bad).min(0).tolist(),np.argwhere(bad).max(0).tolist())
  counts['scoped_changes']+=1
 else:counts['identical']+=1
 if not old.any():assert not im.any();counts['native_black']+=1
 room=rooms[n]
 if room in bgs and not data['view'][n]['grayscale']and data['ppu'][n][0x3f00]==0x0f:
  was=int(np.all(old==bgs[room],2)[112:].sum());now=int(np.all(im==bgs[room],2)[112:].sum())
  if was>40000:assert now>35000,('panorama vanished',n,was,now);background[f'{room:04X}']+=1
 if room==0xacd9 and data['ppu'][n][0x3f00]==0x31:flash+=1
 if n%10==0:
  for name,item in assets.items():
   if name.startswith(('dragon','transform'))and room!=0xacd9:continue
   found=matches(im,item)
   if found:
    hits[name]+=len(found);examples.setdefault(name,[])
    if len(examples[name])<3:examples[name].append(dict(frame=n,positions=found))
report=dict(movie_sha256=ci['movie_sha256'],movie_frames=ci['movie_frames'],native_samples_per_type=len(frames),native_exact=True,apu_exact=True,pcm_exact=True,pcm_bytes=len(pcm),pcm_sha256=hashlib.sha256(pcm).hexdigest(),apu_sha256=hashlib.sha256(apu).hexdigest(),image_checks=counts,changes_confined_to_requested_artwork=True,panorama_samples=background,native_flash_samples=flash,complete_source_matches=hits,source_examples=examples,neighbor_diagnostic='Enabled during replay; no invalid read reported')
Path(a.out).write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
