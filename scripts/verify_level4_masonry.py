"""Pair 0.16.0/0.16.1 native playback and restrict edits to foreground cells."""
from pathlib import Path
from collections import Counter
import argparse,json,hashlib,wave
import numpy as np
from PIL import Image
p=argparse.ArgumentParser()
for key in ['before','after','out']:p.add_argument('--'+key,required=True)
a=p.parse_args();r=Path(__file__).resolve().parents[1];b,c=Path(a.before),Path(a.after)
bi,ci=[json.loads((f/'result.json').read_text())for f in[b,c]]
for k in ['movie_sha256','rom_sha1','core_sha256','movie_frames','captured_frames','stride']:assert bi[k]==ci[k],k
assert bi['movie_completed']and ci['movie_completed'];stride=ci['stride']
for path,version in [(b,'0.16.0'),(c,'0.16.1')]:assert json.loads((path/'installed_pack.json').read_text())==json.loads((r/f'evidence/{version}-pack-sha256.json').read_text())
frames=sorted(int(f.stem)for f in(c/'frames').glob('*.png'));data={k:{}for k in ['ram','ppu','oam','view']}
for n in frames:
 for k in data:
  name=f'{n:06}'+('.json'if k=='view'else'.bin');raw=(c/k/name).read_bytes();assert raw==(b/k/name).read_bytes(),(n,k);data[k][n]=json.loads(raw)if k=='view'else raw
apu=(b/'apu.tsv').read_bytes();assert apu==(c/'apu.tsv').read_bytes()
with wave.open(str(b/'full.wav'),'rb')as f:pcm=f.readframes(f.getnframes());params=f.getparams()
with wave.open(str(c/'full.wav'),'rb')as f:assert params==f.getparams();assert pcm==f.readframes(f.getnframes())
registration=json.loads((r/'art/level4_masonry/registration.json').read_text());eligible={int(m['tile'],16)&255 for m in registration['mappings']if m['tile'].startswith('0B')}
def scope_mask(n):
 mask=np.zeros((480,512),bool)
 for j in [n-stride,n,n+stride]:
  if j not in data['ram']:continue
  ram,pp,v=data['ram'][j],data['ppu'][j],data['view'][j];room=int.from_bytes(ram[0x78:0x7a],'little')
  if room not in [0xa865,0xaa09,0xaa81]:continue
  vv=v['vram'];sx=(vv&31)*8+v['xscroll']+(256 if vv&0x400 else 0);sy=((vv>>5)&31)*8+((vv>>12)&7)+(240 if vv&0x800 else 0)
  for yy in range(sy//8,(sy+239)//8+1):
   for xx in range(sx//8,(sx+255)//8+1):
    tx,ty=xx%32,yy%30;nt=0x2000+xx//32%2*0x400+yy//30%2*0x800
    if pp[nt+ty*32+tx]not in eligible:continue
    X,Y=(xx*8-sx)*2,(yy*8-sy)*2
    # The endFrame view can describe the adjacent picture's camera phase.
    pad=stride*2+2;mask[max(0,Y-pad):min(480,Y+16+pad),max(0,X-pad):min(512,X+16+pad)]=True
  o=data['oam'][j]
  for i in range(0,256,4):
   yy,t,at,xx=o[i:i+4]
   if yy<239 and 0xf8<=t<=0xfb:
    X,Y=xx*2,(yy+1)*2;pad=stride*2+2;mask[max(0,Y-pad):min(480,Y+16+pad),max(0,X-pad):min(512,X+16+pad)]=True
 return mask
sources={}
for name in ['solid','breakable','column_cap','column_base','column_shaft','moving_platform']:
 im=np.array(Image.open(r/f'art/level4_masonry/{name}.png').convert('RGBA'));ys,xs=np.where(im[:,:,3]==255);i=np.argmax(im[ys,xs,:3].sum(1));sources[name]=(im,im[:,:,3]==255,int(ys[i]),int(xs[i]))
counts=Counter();hits=Counter();examples={};background_checks=[]
for n in frames:
 paths=[f/'frames'/f'{n:06}.png'for f in[b,c]]
 if not all(p.stat().st_size for p in paths):assert paths[0].stat().st_size==paths[1].stat().st_size;counts['empty_initial']+=1;continue
 before,after=[np.array(Image.open(p).convert('RGB'))for p in paths];diff=np.any(before!=after,2)
 if not diff.any():counts['identical_images']+=1
 else:
  allowed=scope_mask(n);bad=diff&~allowed
  assert not bad.any(),('outside foreground',n,int(bad.sum()))
  counts['changed_foreground_only']+=1
 if not before.any():assert not after.any();counts['native_black_frames']+=1
 if n%20:continue
 for name,(src,mask,ay,ax)in sources.items():
  hh,ww=src.shape[:2];ys,xs=np.where(np.all(after==src[ay,ax,:3],2))
  for Y,X in zip(ys-ay,xs-ax):
   if Y<0 or X<0 or Y+hh>480 or X+ww>512:continue
   if np.array_equal(after[Y:Y+hh,X:X+ww][mask],src[:,:,:3][mask]):hits[name]+=1;examples.setdefault(name,dict(frame=n,xy=[int(X),int(Y)]));break
 if n in [400,1600,3200,4000,4200,5200,6500,7200,8000,8600]:
  room=int.from_bytes(data['ram'][n][0x78:0x7a],'little');name='Golden_Temple_Exterior.png'if room==0xa865 else'Golden_Temple_Interior.png'
  bg=np.array(Image.open(c/'mesen_home/HdPacks/Holy_Diver_(Tr)'/name).convert('RGB'))[:,:512];pixels=int(np.all(bg==after,2)[112:].sum());assert pixels>40000
  background_checks.append(dict(frame=n,source=name,exact_pixels_below_hud=pixels))
assert hits['solid']and hits['breakable']
out=dict(native_samples_per_type=len(frames),movie_frames=ci['movie_frames'],movie_sha256=ci['movie_sha256'],native_exact=True,apu_exact=True,pcm_exact=True,pcm_bytes=len(pcm),pcm_sha256=hashlib.sha256(pcm).hexdigest(),apu_sha256=hashlib.sha256(apu).hexdigest(),image_checks=counts,changes_confined_to_foreground=True,complete_source_matches=hits,examples=examples,background_checks=background_checks)
Path(a.out).write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
