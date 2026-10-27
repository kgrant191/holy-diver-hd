"""Verify whole branch joins in actual movie frames."""
from pathlib import Path
import argparse,json
from collections import Counter
import numpy as np
from PIL import Image
def matches(im,src):
 mask=src[:,:,3]==255;h,w=mask.shape;colors,counts=np.unique(src[mask,:3],axis=0,return_counts=True);color=colors[np.argmin(counts)];ay,ax=np.argwhere(mask&np.all(src[:,:,:3]==color,2))[0];yy,xx=np.where(np.all(im==color,2));yy-=ay;xx-=ax;valid=(yy>=0)&(xx>=0)&(yy+h<=480)&(xx+w<=512);yy,xx=yy[valid],xx[valid];pts=np.argwhere(mask);pts=pts[np.linspace(0,len(pts)-1,16,dtype=int)]
 for py,px in pts:
  valid=np.all(im[yy+py,xx+px]==src[py,px,:3],1);yy,xx=yy[valid],xx[valid]
  if not len(yy):return []
 return [[int(x),int(y)]for y,x in zip(yy,xx)if np.array_equal(im[y:y+h,x:x+w][mask],src[:,:,:3][mask])]
p=argparse.ArgumentParser();p.add_argument('--capture',required=True);p.add_argument('--out',required=True);a=p.parse_args();r=Path(__file__).resolve().parents[1];c=Path(a.capture);sources={side:np.array(Image.open(r/f'art/tree_potion_cleanup/{side}_whole_join.png').convert('RGBA'))for side in ['left','right']};counts=Counter();examples={}
for f in sorted((c/'frames').glob('*.png')):
 n=int(f.stem)
 if n%20 or not f.stat().st_size:continue
 im=np.array(Image.open(f).convert('RGB'))
 for side,src in sources.items():
  pos=matches(im,src)
  if pos:counts[side]+=len(pos);examples.setdefault(side,dict(frame=n,positions=pos))
assert counts['left'] and counts['right'],counts
report=dict(complete_opaque_join_matches=counts,examples=examples,actual_replay_pixels=True);Path(a.out).write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
