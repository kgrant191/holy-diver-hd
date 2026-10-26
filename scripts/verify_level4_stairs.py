"""Pair native state/audio; restrict all visual changes to restored stair cells."""
from pathlib import Path
from collections import Counter
import argparse,json,hashlib,wave
import numpy as np
from PIL import Image
p=argparse.ArgumentParser()
for k in ['before','after','out']:p.add_argument('--'+k,required=True)
a=p.parse_args();r=Path(__file__).resolve().parents[1];b,c=Path(a.before),Path(a.after)
bi,ci=[json.loads((d/'result.json').read_text())for d in[b,c]]
for k in ['movie_sha256','rom_sha1','core_sha256','movie_frames','captured_frames','stride']:assert bi[k]==ci[k],k
assert bi['movie_completed']and ci['movie_completed'];stride=ci['stride']
for folder,version in [(b,'0.16.2'),(c,'0.16.3')]:
 assert json.loads((folder/'installed_pack.json').read_text())==json.loads((r/f'evidence/{version}-pack-sha256.json').read_text())
frames=sorted(int(f.stem)for f in(c/'frames').glob('*.png'));data={k:{}for k in ['ram','ppu','oam','view']}
for n in frames:
 for k in data:
  name=f'{n:06}'+('.json'if k=='view'else'.bin');raw=(c/k/name).read_bytes()
  assert raw==(b/k/name).read_bytes(),(n,k);data[k][n]=json.loads(raw)if k=='view'else raw
apu=(b/'apu.tsv').read_bytes();assert apu==(c/'apu.tsv').read_bytes()
with wave.open(str(b/'full.wav'),'rb')as f:pcm=f.readframes(f.getnframes());params=f.getparams()
with wave.open(str(c/'full.wav'),'rb')as f:assert f.getparams()==params;assert f.readframes(f.getnframes())==pcm
def allowed(n):
 mask=np.zeros((480,512),bool)
 for j in [n-stride,n,n+stride]:
  if j not in data['ram']:continue
  ram,pp,v=[data[k][j]for k in ['ram','ppu','view']]
  if int.from_bytes(ram[0x78:0x7a],'little')not in [0xa865,0xaa09,0xaa81]:continue
  vv=v['vram'];sx=(vv&31)*8+v['xscroll']+(256 if vv&0x400 else 0)
  sy=((vv>>5)&31)*8+((vv>>12)&7)+(240 if vv&0x800 else 0)
  for yy in range(sy//8,(sy+239)//8+1):
   for xx in range(sx//8,(sx+255)//8+1):
    tx,ty=xx%32,yy%30;nt=0x2000+xx//32%2*0x400+yy//30%2*0x800
    if pp[nt+ty*32+tx]not in range(0x7c,0x80):continue
    X,Y=(xx*8-sx)*2,(yy*8-sy)*2
    # endFrame scroll metadata can describe the next submitted image.
    pad=stride*2+2
    mask[max(0,Y-pad):min(480,Y+16+pad),max(0,X-pad):min(512,X+16+pad)]=True
 return mask
src=np.array(Image.open(r/'art/level4_stairs/descending_step.png').convert('RGBA'))
alpha=src[:,:,3]==255;ys,xs=np.where(alpha);k=np.argmax(src[ys,xs,:3].sum(1));ay,ax=int(ys[k]),int(xs[k])
counts=Counter();examples=[];hits=0
for n in frames:
 paths=[f/'frames'/f'{n:06}.png'for f in[b,c]]
 if not all(p.stat().st_size for p in paths):assert paths[0].stat().st_size==paths[1].stat().st_size;counts['empty_initial']+=1;continue
 old,im=[np.array(Image.open(p).convert('RGB'))for p in paths];diff=np.any(old!=im,2)
 if diff.any():
  assert not diff[~allowed(n)].any(),('outside restored stairs',n,int(diff[~allowed(n)].sum()))
  counts['stair_only']+=1
 else:counts['identical']+=1
 if not old.any():assert not im.any();counts['native_black']+=1
 if n%10:continue
 ys,xs=np.where(np.all(im==src[ay,ax,:3],2));positions=[]
 for y,x in zip(ys-ay,xs-ax):
  if y<0 or x<0 or y+32>480 or x+32>512:continue
  if np.array_equal(im[y:y+32,x:x+32][alpha],src[:,:,:3][alpha]):positions.append([int(x),int(y)])
 if positions:
  hits+=len(positions)
  if len(examples)<10:examples.append(dict(frame=n,positions=positions))
assert hits,'No complete restored step matched actual playback'
report=dict(movie_frames=ci['movie_frames'],native_samples_per_type=len(frames),movie_sha256=ci['movie_sha256'],
 native_exact=True,apu_exact=True,pcm_exact=True,pcm_bytes=len(pcm),pcm_sha256=hashlib.sha256(pcm).hexdigest(),
 apu_sha256=hashlib.sha256(apu).hexdigest(),image_checks=counts,changes_confined_to_stair_cells=True,
 complete_step_source_matches=hits,examples=examples)
Path(a.out).write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
