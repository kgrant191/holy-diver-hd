"""Register complete Demonic Palace sources before slicing native cells."""
from pathlib import Path
import json
import numpy as np
from PIL import Image,ImageOps,ImageDraw
R=Path(__file__).resolve().parents[1]; A=R/'art/level5'; G=R/'art/generated'
def reg(im,size,colors=128):
 im=im.convert('RGBA').resize(size,Image.Resampling.LANCZOS);alpha=im.getchannel('A').point(lambda x:255 if x>=160 else 0)
 out=im.convert('RGB').quantize(colors=colors,dither=Image.Dither.NONE).convert('RGBA');out.putalpha(alpha);return out
def obj(im):
 im=im.convert('RGBA');return im.crop(im.getchannel('A').point(lambda x:255 if x>=160 else 0).getbbox())
def framed(im,size,margin=1):
 raw=obj(im);raw=reg(ImageOps.contain(raw,(size[0]-margin*2,size[1]-margin*2),Image.Resampling.LANCZOS),ImageOps.contain(raw,(size[0]-margin*2,size[1]-margin*2)).size)
 out=Image.new('RGBA',size);out.paste(raw,((size[0]-raw.width)//2,(size[1]-raw.height)//2));return out

def prepare():
 A.mkdir(exist_ok=True);report={}
 layouts=json.loads((A/'skeleton_layouts.json').read_text());raw=Image.open(G/'palace_skeleton.png').convert('RGBA');panels=[raw.crop((i*512,0,(i+1)*512,760))for i in range(3)]
 # One common source coordinate system; preserve shared skull, rib cage and arm.
 box=panels[0].getchannel('A').point(lambda x:255 if x>=190 else 0).getbbox();print('skeleton source box',box)
 masks=[]
 for layout in layouts:
  im=Image.new('L',(64,64));d=ImageDraw.Draw(im)
  for t,x,y in layout:d.rectangle((x*2,y*2,x*2+15,y*2+15),fill=255)
  masks.append(np.array(im)>0)
 # Register four whole horizontal bands, never trim a limb at a tile boundary.
 def bands(panel,width,x,cuts):
  im=Image.new('RGBA',(64,64));start=box[1]
  for i,stop in enumerate(cuts+[box[3]]):
   band=reg(panel.crop((box[0],start,box[2],stop)),(width,16));im.paste(band,(x,i*16));start=stop
  return im
 fit=None
 for width in range(64,53,-1):
  for x in range(0,65-width):
   for c0 in range(335,376,5):
    for c1 in range(505,546,10):
     for c2 in range(600,641,10):
      cuts=[c0,c1,c2];im=bands(panels[0],width,x,cuts)
      if ((np.array(im.getchannel('A'))>0)&~masks[0]).any():continue
      fit=width,x,cuts,im;break
     if fit:break
    if fit:break
   if fit:break
  if fit:break
 assert fit,'Skeleton needs a complete source registration, not clipping'
 width,x,cuts,base=fit;poses=[base]
 for i in [1,2]:
  fitted=bands(panels[i],width,x,cuts);out=base.copy()
  oldkeys={v[0]for v in layouts[0]}
  for t,xx,yy in layouts[i]:
   if t not in oldkeys:out.paste(fitted.crop((xx*2,yy*2,xx*2+16,yy*2+16)),(xx*2,yy*2))
  # No native fourth row in the tucked pose.
  if i==2:out.paste(Image.new('RGBA',(64,16)),(0,48))
  assert not ((np.array(out.getchannel('A'))>0)&~masks[i]).any(),('pose outside native union',i)
  poses.append(out)
 for i,im in enumerate(poses):im.save(A/f'skeleton_{i}.png')
 bone=framed(raw.crop((690,765,810,970)),(16,32),1);bone.save(A/'bone.png')
 report['skeleton']={'source_box':box,'band_cuts':cuts,'width':width,'x':x,'shared_cells_exact':True,'clipped_pixels':0}
 rock=framed(Image.open(G/'palace_boulder.png'),(48,48),2)
 for i,angle in enumerate([0,90,180]):rock.rotate(angle,Image.Resampling.NEAREST).save(A/f'boulder_{i}.png')
 # Native three-cell initial emergence is a compressed whole boulder silhouette.
 reg(rock,(48,16)).save(A/'boulder_emerge.png')
 serpent=Image.open(G/'palace_serpent.png');w,h=serpent.size
 framed(serpent.crop((0,0,w//2,h)),(48,48),2).save(A/'serpent_head.png');framed(serpent.crop((w//2,0,w,h)),(32,32),2).save(A/'serpent_segment.png')
 report['boulder']={'size':[48,48],'rotations':[0,90,180],'native_emergence_size':[48,16]};report['serpent']={'head':[48,48],'segment':[32,32],'native_separate_segments':True}
 (A/'source_registration.json').write_text(json.dumps(report,indent=2)+'\n');return report
if __name__=='__main__':print(json.dumps(prepare(),indent=2))
