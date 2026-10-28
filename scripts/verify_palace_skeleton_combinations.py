"""Verify all four complete native skeleton combinations in actual captures."""
from pathlib import Path
import argparse,json,tempfile
import numpy as np
from PIL import Image
p=argparse.ArgumentParser();p.add_argument('--capture',required=True);p.add_argument('--out',required=True);a=p.parse_args();r=Path(__file__).resolve().parents[1];c=Path(a.capture)
def source(path,mirror=False):
 src=np.array(Image.open(path).convert('RGBA'))
 if mirror:src=src[:,::-1]
 mask=src[:,:,3]==255;colors,counts=np.unique(src[mask,:3],axis=0,return_counts=True);color=colors[np.argmax(colors.sum(1)/(1+counts))];yy,xx=np.where(mask&np.all(src[:,:,:3]==color,2));pts=np.argwhere(mask)
 return src,mask,int(yy[0]),int(xx[0]),pts[np.linspace(0,len(pts)-1,8,dtype=int)]
def matches(im,item):
 src,mask,ay,ax,probes=item;h,w=mask.shape;yy,xx=np.where(np.all(im==src[ay,ax,:3],2));yy-=ay;xx-=ax;v=(yy>=0)&(xx>=0)&(yy+h<=480)&(xx+w<=512);yy,xx=yy[v],xx[v]
 for py,px in probes:
  v=np.all(im[yy+py,xx+px]==src[py,px,:3],1);yy,xx=yy[v],xx[v]
  if not len(yy):return []
 return [[int(x),int(y)]for y,x in zip(yy,xx)if np.array_equal(im[y:y+h,x:x+w][mask],src[:,:,:3][mask])]


reg=json.loads((r/'art/level5_continuation/registration.json').read_text());atlas=Image.open(c/'mesen_home/HdPacks/Holy_Diver_(Tr)/Demonic_Palace_Tiles_2x.png').convert('RGBA')
coords={e['rule'].split('<tile>')[1].split(',')[1]:list(map(int,e['rule'].split('<tile>')[1].split(',')[3:5]))for e in reg['clones']if e['kind']=='byte-identical skeleton and bone'}
hits={}
with tempfile.TemporaryDirectory()as temporary:
 for i,layout in enumerate(json.loads((r/'art/level5_continuation/skeleton_layouts.json').read_text())):
  whole=Image.new('RGBA',(64,64))
  for tile,x,y in layout['cells']:
   sx,sy=coords[tile];whole.paste(atlas.crop((sx,sy,sx+16,sy+16)),(x*2,y*2))
  path=Path(temporary)/f'pose_{i}.png';whole.save(path)
  for n in range(layout['example'],layout['example']+40,2):
   im=np.array(Image.open(c/'frames'/f'{n:06}.png').convert('RGB'))
   for mirror in [False,True]:
    positions=matches(im,source(path,mirror))
    if positions:hits[str(i)]=dict(frame=n,mirrored=mirror,positions=positions);break
   if str(i)in hits:break
assert len(hits)==4,hits
report=dict(complete_native_combinations=4,unchanged_approved_atlas=True,opaque_source_pixels_exact=True,matches=hits)
Path(a.out).write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
