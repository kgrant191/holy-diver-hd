"""Match complete registered sources against actual Mesen capture pixels."""
from pathlib import Path
from collections import Counter
import argparse,json
import numpy as np
from PIL import Image
p=argparse.ArgumentParser();p.add_argument('--capture',required=True);p.add_argument('--stairs',action='append',default=[]);p.add_argument('--out',required=True);args=p.parse_args();r=Path(__file__).resolve().parents[1];capture=Path(args.capture)/'frames'
def matches(im,src):
 mask=src[:,:,3]>0;h,w=mask.shape;colors,counts=np.unique(src[mask,:3],axis=0,return_counts=True);color=colors[np.argmin(counts)];ay,ax=np.argwhere(mask&np.all(src[:,:,:3]==color,2))[0];yy,xx=np.where(np.all(im==color,2));yy-=ay;xx-=ax;valid=(yy>=0)&(xx>=0)&(yy+h<=480)&(xx+w<=512);yy,xx=yy[valid],xx[valid];pts=np.argwhere(mask);pts=pts[np.linspace(0,len(pts)-1,16,dtype=int)]
 for py,px in pts:
  valid=np.all(im[yy+py,xx+px]==src[py,px,:3],1);yy,xx=yy[valid],xx[valid]
  if not len(yy):return []
 return [[int(x),int(y)]for y,x in zip(yy,xx)if np.array_equal(im[y:y+h,x:x+w][mask],src[:,:,:3][mask])]
report={'tower_fades':{},'white_dragon':{}}
for n,factor in [(1750,1),(1892,.65),(1900,.30),(1908,.12)]:
 im=np.array(Image.open(capture/f'{n:06}.png').convert('RGB'));hits={}
 for phase in range(8):
  src=np.array(Image.open(r/f'art/level4_finale/tower_band_{phase}_0F001030.png').convert('RGBA'))
  # Stock Mesen2.2.1 HdNesPack::AdjustBrightness, including integer rounding.
  if factor!=1:src[:,:,:3]=(((src[:,:,:3].astype(int)+1)*int(factor*255))>>8).astype('uint8')
  positions=matches(im,src)
  if positions:hits[str(phase)]=positions
 assert len(hits)>=2,(n,hits);report['tower_fades'][str(n)]=hits
for n in [3240,3300,3359,3400]:
 im=np.array(Image.open(capture/f'{n:06}.png').convert('RGB'));hits={}
 for phase in range(3):
  src=np.array(Image.open(r/f'art/level4_dragon/pose_{phase}.png').convert('RGBA'));src[:,:,:3]=255;positions=matches(im,src)
  if positions:hits[str(phase)]=positions
 assert hits,n;report['white_dragon'][str(n)]=hits
src=np.array(Image.open(r/'art/level4_transition/thunder_tome.png').convert('RGBA'));report['thunder_tome']=matches(np.array(Image.open(capture/'001750.png').convert('RGB')),src);assert report['thunder_tome']
step=np.array(Image.open(r/'art/level4_transition/ascending_step.png').convert('RGBA'));hits=Counter();examples={}
for path in args.stairs:
 c=Path(path)
 for f in sorted((c/'frames').glob('*.png')):
  n=int(f.stem)
  if n%20 or not f.stat().st_size:continue
  positions=matches(np.array(Image.open(f).convert('RGB')),step)
  if positions:
   ram=(c/'ram'/f.with_suffix('.bin').name).read_bytes();room=ram[0x78:0x7a][::-1].hex().upper();hits[room]+=len(positions);examples.setdefault(room,dict(frame=n,positions=positions))
if args.stairs:assert hits['AA81'] and hits['AAF9']
report['ascending_stairs']=dict(complete_matches=hits,examples=examples)
Path(args.out).write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
