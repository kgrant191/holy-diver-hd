"""Verify the F8 repair changes only the missing decorative cell in actual play."""
from pathlib import Path
from collections import Counter
import argparse,hashlib,json,wave
import numpy as np
from PIL import Image
p=argparse.ArgumentParser()
for k in ['before','after','out']:p.add_argument('--'+k,required=True)
a=p.parse_args();r=Path(__file__).resolve().parents[1];b,c=Path(a.before),Path(a.after)
bi,ci=[json.loads((d/'result.json').read_text())for d in [b,c]]
for k in ['movie_sha256','rom_sha1','core_sha256','movie_frames','captured_frames','stride']:assert bi[k]==ci[k],k
assert bi['movie_completed']and ci['movie_completed'];stride=ci['stride']
for folder,version in [(b,'0.19.0'),(c,'0.19.1')]:assert json.loads((folder/'installed_pack.json').read_text())==json.loads((r/f'evidence/{version}-pack-sha256.json').read_text())
frames=sorted(int(f.stem)for f in(c/'frames').glob('*.png'));data={k:{}for k in ['ram','ppu','oam','view']}
for n in frames:
 for k in data:
  name=f'{n:06}'+('.json'if k=='view'else'.bin');raw=(c/k/name).read_bytes();assert raw==(b/k/name).read_bytes(),(n,k);data[k][n]=json.loads(raw)if k=='view'else raw
apu=(b/'apu.tsv').read_bytes();assert apu==(c/'apu.tsv').read_bytes()
with wave.open(str(b/'full.wav'),'rb')as f:pcm=f.readframes(f.getnframes());params=f.getparams()
with wave.open(str(c/'full.wav'),'rb')as f:assert f.getparams()==params;assert f.readframes(f.getnframes())==pcm

def cells(n):
 ram,pp,v=[data[k][n]for k in ['ram','ppu','view']]
 if ram[0x72]!=0x18 or ram[0x78:0x7a]!=bytes.fromhex('d9ac'):return []
 vv=v['vram'];sx=(vv&31)*8+v['xscroll']+(256 if vv&0x400 else 0);sy=((vv>>5)&31)*8+((vv>>12)&7)+(240 if vv&0x800 else 0);found=[]
 for yy in range(sy//8,(sy+239)//8+1):
  for xx in range(sx//8,(sx+255)//8+1):
   tx,ty=xx%32,yy%30;nt=0x2000+xx//32%2*0x400+yy//30%2*0x800
   if pp[nt+ty*32+tx]!=0xf8:continue
   attr=pp[nt+960+ty//4*8+tx//4];pa=attr>>((ty%4)//2*4+(tx%4)//2*2)&3
   pal=(bytes([pp[0x3f00]])+pp[0x3f01+pa*4:0x3f04+pa*4]).hex().upper()
   if pal not in ['0F073703','31073703']:continue
   found.append(((xx*8-sx)*2,(yy*8-sy)*2))
 return found
positions={n:cells(n)for n in frames};counts=Counter();changed_pixels=0;examples=[]
bg=np.array(Image.open(c/'mesen_home/HdPacks/Holy_Diver_(Tr)/Golden_Temple_Exterior.png').convert('RGB'))[:,:512]
for n in frames:
 paths=[d/'frames'/f'{n:06}.png'for d in [b,c]]
 if not all(f.stat().st_size for f in paths):assert paths[0].stat().st_size==paths[1].stat().st_size;counts['empty_initial']+=1;continue
 old,im=[np.array(Image.open(f).convert('RGB'))for f in paths];diff=np.any(old!=im,2)
 if not diff.any():counts['identical']+=1;continue
 allowed=np.zeros((480,512),bool)
 for j in [n-stride,n,n+stride]:
  for x,y in positions.get(j,[]):
   pad=2*stride+2;allowed[max(0,y-pad):min(480,y+16+pad),max(0,x-pad):min(512,x+16+pad)]=True
 assert not diff[~allowed].any(),('outside F8 ornament',n,int(diff[~allowed].sum()))
 assert np.array_equal(im[diff],bg[diff]),('replacement is not exact panorama',n)
 counts['ornament_only']+=1;changed_pixels+=int(diff.sum())
 if len(examples)<8:examples.append(dict(frame=n,changed_pixels=int(diff.sum()),native_positions=positions[n]))
assert counts['ornament_only']>0
report=dict(movie_sha256=ci['movie_sha256'],movie_frames=ci['movie_frames'],native_samples_per_type=len(frames),native_exact=True,apu_exact=True,pcm_exact=True,pcm_bytes=len(pcm),pcm_sha256=hashlib.sha256(pcm).hexdigest(),apu_sha256=hashlib.sha256(apu).hexdigest(),image_checks=counts,changed_pixels=changed_pixels,changes_confined_to_F8=True,all_changed_pixels_match_existing_panorama=True,examples=examples)
Path(a.out).write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
