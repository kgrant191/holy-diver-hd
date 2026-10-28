"""Register complete boss/altar paintings to native component unions.

Horizontal scanlines are fitted only when the native union is narrower. The
source is never clipped at an OAM boundary. Shared animation cells are exact.
"""
from pathlib import Path
import json
import numpy as np
from PIL import Image, ImageDraw
R=Path(__file__).resolve().parents[1]; A=R/'art/level5_finale'; G=R/'art/generated'

def opaque(im):
 im=im.convert('RGBA');im.putalpha(im.getchannel('A').point(lambda x:255 if x>=192 else 0));return im

def union(layout,size,scale=1):
 out=Image.new('L',size);d=ImageDraw.Draw(out)
 for _,x,y in layout:d.rectangle((x*scale,y*scale,x*scale+15,y*scale+15),fill=255)
 return np.array(out)>0

def fit(im,size,mask):
 im=opaque(im);im=im.crop(im.getchannel('A').getbbox()).resize(size,Image.Resampling.LANCZOS);im=opaque(im)
 # Preserve the entire silhouette where a native component has a narrow cap.
 a=np.array(im);rows=0
 for y in range(size[1]):
  xs=np.flatnonzero(a[y,:,3]);allowed=np.flatnonzero(mask[y])
  if not len(xs):continue
  assert len(allowed)
  if xs[0]<allowed[0]or xs[-1]>allowed[-1]:
   left=max(xs[0],allowed[0]);right=min(xs[-1],allowed[-1]);width=right-left+1
   row=Image.fromarray(a[y:y+1,xs[0]:xs[-1]+1]).resize((width,1),Image.Resampling.LANCZOS)
   a[y]=0;a[y,left:right+1]=np.array(opaque(row))[0];rows+=1
 result=Image.fromarray(a);rgb=result.convert('RGB').quantize(colors=128,dither=Image.Dither.NONE).convert('RGBA');rgb.putalpha(result.getchannel('A'))
 assert not ((np.array(rgb)[:,:,3]>0)&~mask).any()
 return rgb,rows

def prepare():
 layouts=json.loads((A/'boss_layouts.json').read_text());sheet=Image.open(G/'palace_boss5.png').convert('RGBA');report={};whole={};shared={}
 for col,(name,size)in enumerate([('skull',(48,64)),('claw',(64,64)),('fist',(32,32))]):
  for phase in range(2):
   key=name+str(phase);raw=sheet.crop((col*512+(96 if name=='fist'else 0),phase*512,(col+1)*512,(phase+1)*512));mask=union(layouts[key],size,2)
   im,rows=fit(raw,size,mask)
   if phase:
    # A native shared ID cannot change between phases. Copy complete 16px cells.
    for tile,x,y in layouts[key]:
     if tile in shared:im.paste(shared[tile],(x*2,y*2))
   for tile,x,y in layouts[key]:
    cell=im.crop((x*2,y*2,x*2+16,y*2+16))
    if tile in shared:assert shared[tile].tobytes()==cell.tobytes()
    shared[tile]=cell
   im.save(A/(key+'.png'));whole[key]=im;report[key]=dict(size=size,fitted_scanlines=rows,clipped_pixels=0)
 ornaments=json.loads((A/'ornament_layouts.json').read_text())
 for name,size in [('idol',(64,96)),('effigy',(96,128))]:
  im,rows=fit(Image.open(G/f'palace_boss5_{name}.png'),size,union(ornaments[name],size));im.save(A/(name+'.png'));whole[name]=im;report[name]=dict(size=size,fitted_scanlines=rows,clipped_pixels=0)
 # The native victory actor has one fewer lower row. Keep the crossbar and
 # upper figure exact, compressing the entire lower figure together.
 moving=Image.new('RGBA',(96,112));moving.paste(whole['effigy'].crop((0,0,96,48)),(0,0));moving.paste(opaque(whole['effigy'].crop((0,48,96,128)).resize((96,64),Image.Resampling.LANCZOS)),(0,48))
 layout=json.loads((A/'effigy_sprite_layout.json').read_text());moving,rows=fit(moving,(96,112),union(layout,(96,112)));moving.save(A/'effigy_sprite.png');report['effigy_sprite']=dict(size=[96,112],fitted_scanlines=rows,clipped_pixels=0)
 report['shared_cells_exact']=True;(A/'source_registration.json').write_text(json.dumps(report,indent=2)+'\n')
 preview=Image.new('RGBA',(520,180),'#152030');d=ImageDraw.Draw(preview)
 for k,(name,im)in enumerate(whole.items()):
  x=[4,62,125,195,270,310,352,420][k];preview.alpha_composite(im,(x,22));d.text((x,5),name,fill='white')
 preview.convert('RGB').resize((1040,360),Image.Resampling.NEAREST).save(A/'source_review.png');return report
if __name__=='__main__':print(json.dumps(prepare(),indent=2))
