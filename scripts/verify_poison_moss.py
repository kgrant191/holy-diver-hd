"""Pair native state/audio and unchanged actor source pixels for the green retheme."""
from pathlib import Path
from collections import Counter
import argparse,json,wave
import numpy as np
from PIL import Image
p=argparse.ArgumentParser()
for k in ('before','after','out'):p.add_argument('--'+k,required=True)
a=p.parse_args();b,c=Path(a.before),Path(a.after);r=Path(__file__).resolve().parents[1]
bi=json.loads((b/'result.json').read_text());ci=json.loads((c/'result.json').read_text())
for k in ('movie_sha256','rom_sha1','core_sha256','movie_frames','captured_frames','stride'):assert bi[k]==ci[k],k
assert bi['movie_completed'] and ci['movie_completed'];stride=ci['stride']
assert json.loads((c/'installed_pack.json').read_text())==json.loads((r/'evidence/0.14.0-pack-sha256.json').read_text()),'Capture is not the final candidate'
assert json.loads((b/'installed_pack.json').read_text())==json.loads((r/'evidence/0.13.0-pack-sha256.json').read_text()),'Baseline pack differs'
frames=sorted(int(f.stem)for f in(c/'frames').glob('*.png'));ram={}
for n in frames:
 for k in ['ram','ppu','oam','view']:
  f=f'{n:06}'+('.json'if k=='view'else'.bin');raw=(c/k/f).read_bytes();assert raw==(b/k/f).read_bytes(),(n,k)
  if k=='ram':ram[n]=raw
apu=(b/'apu.tsv').read_bytes();assert apu==(c/'apu.tsv').read_bytes()
with wave.open(str(b/'full.wav'),'rb')as f:bp=f.readframes(f.getnframes());params=f.getparams()
with wave.open(str(c/'full.wav'),'rb')as f:cp=f.readframes(f.getnframes());assert f.getparams()==params
assert bp==cp
sources={}
for name,path in [('fish0','art/level3_lava/fish_0.png'),('fish1','art/level3_lava/fish_1.png'),('green_creature','art/level3_caves/green_creature.png')]:
 src=np.array(Image.open(r/path).convert('RGBA'))
 for flip in [False,True]:
  im=src[:,::-1]if flip else src;mask=im[:,:,3]==255;ys,xs=np.nonzero(mask);j=len(ys)//2
  sources[name+'/'+str(flip)]=(im,mask,int(ys[j]),int(xs[j]))
counts=Counter();rooms=Counter();matches=Counter();examples=[]
target={0x988a,0x997a,0x99f2,0x9aa6,0x9b96,0x9c86,0x9cfe,0x9dee}
def room(n):return int.from_bytes(ram[n][0x78:0x7a],'little')
for n in frames:
 f=f'{n:06}.png';pb,pc=b/'frames'/f,c/'frames'/f
 if not pb.stat().st_size or not pc.stat().st_size:assert n in[1,2,4]and pb.stat().st_size==pc.stat().st_size;counts['initial_empty']+=1;continue
 before=np.array(Image.open(pb).convert('RGB'));after=np.array(Image.open(pc).convert('RGB'));eq=np.array_equal(before,after)
 counts['exact_images'if eq else'changed_images']+=1;rooms[f'{room(n):04X}']+=1
 near=[j for j in[n-stride,n,n+stride]if j in ram]
 if all(room(j)not in target for j in near):assert eq,('outside Level 3 scenery',n);counts['exact_outside_images']+=1
 if all(room(j)==0xffff for j in near):assert eq,('menu',n);counts['exact_menu_images']+=1
 if not before.any():assert not after.any(),('blackout',n);counts['exact_blackouts']+=1
 if n%24:continue
 for key,(src,mask,sy,sx)in sources.items():
  h,w=mask.shape
  for y,x in np.argwhere(np.all(before==src[sy,sx,:3],axis=2)):
   X,Y=int(x-sx),int(y-sy)
   if X<0 or Y<0 or X+w>512 or Y+h>480:continue
   if not np.array_equal(before[Y:Y+h,X:X+w][mask],src[:,:,:3][mask]):continue
   assert np.array_equal(after[Y:Y+h,X:X+w][mask],src[:,:,:3][mask]),('actor changed',n,key,X,Y)
   matches[key]+=1
   if len(examples)<12:examples.append(dict(frame=n,source=key,xy=[X,Y],opaque_pixels=int(mask.sum())))
out=Path(a.out);out.parent.mkdir(parents=True,exist_ok=True)
report=dict(version='0.14.0',movie_sha256=ci['movie_sha256'],movie_frames=ci['movie_frames'],capture_stride=stride,paired_native_samples_per_type=len(frames),identical_apu_writes=len(apu.splitlines()),identical_pcm_bytes=len(bp),counts=dict(counts),rooms=dict(rooms),preserved_source_matches=dict(matches),examples=examples,native_gameplay_unchanged=True)
out.write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
