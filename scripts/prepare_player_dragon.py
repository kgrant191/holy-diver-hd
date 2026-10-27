"""Register whole dragon poses, retaining exact shared native cells."""
from pathlib import Path
import json
import numpy as np
from PIL import Image,ImageDraw

def prepare(root):
 art=root/'art/level4_dragon';gen=root/'art/generated'
 layouts=json.loads((art/'native_dragon_layouts.json').read_text())
 raised=next(p for p in layouts if any(t=='0C94'for t,x,y in p['layout'])and any(t=='0CA3'for t,x,y in p['layout']))
 folded=next(p for p in layouts if any(t=='0CA4'for t,x,y in p['layout'])and any(t=='0CA3'for t,x,y in p['layout']))
 raw=[Image.open(gen/name).convert('RGBA')for name in ['player_dragon_raised.png','player_dragon_folded.png','player_dragon_firing.png']]
 # One common crop/placement keeps neck, hips and feet registered across edits.
 box=(40,60,1882,786);raw=[im.crop(box)for im in raw]
 def mask(layout):
  im=Image.new('L',(112,48));draw=ImageDraw.Draw(im)
  for t,x,y in layout:draw.rectangle((x*2,y*2,x*2+15,y*2+15),fill=255)
  return np.array(im)>0
 masks=[mask(p['layout'])for p in [raised,folded]]
 def registered(im,x,y):
  out=Image.new('RGBA',(112,48));out.paste(im,(x,y));out.putalpha(out.getchannel('A').point(lambda v:255 if v>=128 else 0));return out
 found=None
 for height in range(46,37,-1):
  for width in range(110,99,-1):
   scaled=[im.resize((width,height),Image.Resampling.LANCZOS)for im in raw]
   for y in range(1,49-height):
    for x in range(1,113-width):
     candidates=[registered(im,x,y)for im in scaled]
     if any(((np.array(im.getchannel('A'))>0)&~m).any()for im,m in zip(candidates,[masks[0],masks[1],masks[0]])):continue
     found=(width,height,x,y,candidates);break
    if found:break
   if found:break
  if found:break
 assert found,'Whole dragon cannot fit the native sprite unions without clipping'
 width,height,fit_x,fit_y,(base,fold,fire)=found
 palette=base.convert('RGB').quantize(colors=128)
 def quant(im):
  out=im.convert('RGB').quantize(palette=palette,dither=Image.Dither.NONE).convert('RGBA');out.putalpha(im.getchannel('A'));return out
 base,fold,fire=map(quant,[base,fold,fire]);base_cells={t:base.crop((x*2,y*2,x*2+16,y*2+16))for t,x,y in raised['layout']}
 cells=dict(base_cells);poses=[]
 for p in layouts:
  im=Image.new('RGBA',(112,48));is_fold=any(t=='0CA4'for t,x,y in p['layout'])
  for t,x,y in p['layout']:
   if t not in cells:
    src=fire if t=='0CAD'else fold if is_fold else base
    cells[t]=src.crop((x*2,y*2,x*2+16,y*2+16))
   im.paste(cells[t],(x*2,y*2))
  assert not ((np.array(im.getchannel('A'))>0)&~mask(p['layout'])).any()
  im.save(art/(p['name']+'.png'));poses.append(im)
 # Native mirroring and animation order remain in the game, not in the atlas.
 report=dict(size=[112,48],common_source_box=list(box),fit=dict(width=width,height=height,x=fit_x,y=fit_y),clipped_pixels=0,shared_native_cells_exact=True,pose_names=[p['name']for p in layouts],native_gameplay_modified=False)
 (art/'dragon_registration.json').write_text(json.dumps(report,indent=2)+'\n')
 return poses,report

if __name__=='__main__':
 images,report=prepare(Path(__file__).resolve().parents[1]);print(report)
