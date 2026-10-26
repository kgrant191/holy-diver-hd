"""Pair actual playback; permit only small-pickup pixels to change."""
from pathlib import Path
from collections import Counter
import argparse, hashlib, json, wave
import numpy as np
from PIL import Image

p=argparse.ArgumentParser()
for n in ['before','after','out']:p.add_argument('--'+n,required=True)
args=p.parse_args();r=Path(__file__).resolve().parents[1];b,c=Path(args.before),Path(args.after)
bi,ci=[json.loads((f/'result.json').read_text())for f in [b,c]]
for k in ['movie_sha256','rom_sha1','core_sha256','movie_frames','captured_frames','stride']:assert bi[k]==ci[k],k
assert bi['movie_completed'] and ci['movie_completed']
for folder,version in [(b,'0.16.1'),(c,'0.16.2')]:
 assert json.loads((folder/'installed_pack.json').read_text())==json.loads((r/f'evidence/{version}-pack-sha256.json').read_text())
frames=sorted(int(f.stem)for f in(c/'frames').glob('*.png'));counts=Counter();hits=Counter();examples={}
reg=json.loads((r/'art/level4_repairs/registration.json').read_text())
imgs=[l[5:]for l in(r/'build/Holy_Diver_(Tr)/hires.txt').read_text().splitlines()if l.startswith('<img>')]
sources={}
for name in ['heart','magic']:
 rec=next(x for x in reg['pickups']if x['name']==name)
 f=rec['rule'][6:].split(',');x,y=map(int,f[3:5])
 sources[name]=np.array(Image.open(r/'build/Holy_Diver_(Tr)'/imgs[int(f[0])]).convert('RGBA').crop((x,y,x+16,y+16)))
for n in frames:
 for kind in ['ram','ppu','oam','view']:
  fn=f'{n:06}'+('.json'if kind=='view'else'.bin')
  assert (b/kind/fn).read_bytes()==(c/kind/fn).read_bytes(),(n,kind)
 bp,cp=[f/'frames'/f'{n:06}.png'for f in[b,c]]
 if not bp.stat().st_size or not cp.stat().st_size:
  assert bp.stat().st_size==cp.stat().st_size;counts['empty_initial']+=1;continue
 old,new=[np.array(Image.open(f).convert('RGB'))for f in [bp,cp]]
 diff=np.any(old!=new,axis=2)
 if not diff.any():counts['identical']+=1
 else:
  allowed=np.zeros((480,512),bool)
  for j in [n-ci['stride'],n,n+ci['stride']]:
   op=c/'oam'/f'{j:06}.bin'
   if not op.exists():continue
   o=op.read_bytes()
   for i in range(0,256,4):
    y,t,at,x=o[i:i+4]
    if y>=239 or t not in [0x47,0x48]:continue
    X,Y=x*2,(y+1)*2
    # endFrame OAM can be three native pixels ahead of the submitted drop
    # image during falling/spawning (measured maximum: 6 HD pixels, f3436).
    # Adjacent captures retain the native positions on both sides of it.
    allowed[max(0,Y-6):min(480,Y+22),max(0,X-6):min(512,X+22)]=True
  assert not diff[~allowed].any(),('outside pickup cells',n,int(diff[~allowed].sum()))
  counts['pickup_only']+=1
 if not old.any():assert not new.any();counts['native_black']+=1
 if n%20:continue
 for name,src in sources.items():
  mask=src[:,:,3]==255;ys,xs=np.nonzero(mask);k=np.argmax(src[ys,xs,:3].sum(1));ay,ax=ys[k],xs[k]
  yy,xx=np.where(np.all(new==src[ay,ax,:3],axis=2))
  for y,x in zip(yy-ay,xx-ax):
   if y<0 or x<0 or y+16>480 or x+16>512:continue
   if np.array_equal(new[y:y+16,x:x+16][mask],src[:,:,:3][mask]):
    hits[name]+=1;examples.setdefault(name,dict(frame=n,xy=[int(x),int(y)]));break
apu=(b/'apu.tsv').read_bytes();assert apu==(c/'apu.tsv').read_bytes()
with wave.open(str(b/'full.wav'),'rb')as f:pcm=f.readframes(f.getnframes());params=f.getparams()
with wave.open(str(c/'full.wav'),'rb')as f:assert f.getparams()==params;assert f.readframes(f.getnframes())==pcm
assert hits['heart'] and hits['magic']
report=dict(movie_frames=ci['movie_frames'],native_samples_per_type=len(frames),native_exact=True,
 apu_exact=True,pcm_exact=True,pcm_bytes=len(pcm),pcm_sha256=hashlib.sha256(pcm).hexdigest(),
 image_checks=counts,complete_pickup_source_matches=hits,examples=examples,
 all_other_pixels_unchanged=True,oam_capture_margin_hd_pixels=6,
 movie_sha256=ci['movie_sha256'],core_sha256=ci['core_sha256'])
Path(args.out).write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
