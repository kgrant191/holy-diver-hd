"""Register complete generated poses within the measured native sprite unions."""
from pathlib import Path
import json
import numpy as np
from PIL import Image,ImageDraw

def prepare(root):
 a=root/'art/level4_staff';g=root/'art/generated'
 layouts=json.loads((a/'native_sentinel_layouts.json').read_text())
 base=Image.open(g/'temple_sentinel.png').convert('RGBA')
 box=base.getchannel('A').point(lambda v:255 if v>=160 else 0).getbbox()
 raw=base.crop(box);step=Image.open(g/'temple_sentinel_step.png').convert('RGBA').crop(box)
 masks=[]
 for pose in layouts:
  mask=Image.new('L',(96,96));draw=ImageDraw.Draw(mask)
  for t,x,y in pose['layout']:draw.rectangle((x*2,y*2,x*2+15,y*2+15),fill=255)
  masks.append(np.array(mask)>0)
 def bands(im,width,x,cuts,heights):
  out=Image.new('RGBA',(96,96));y=1;start=0
  for stop,height in zip(cuts,heights):
   out.paste(im.crop((0,start,im.width,stop)).resize((width,height),Image.Resampling.LANCZOS),(x,y))
   start=stop;y+=height
  out.putalpha(out.getchannel('A').point(lambda v:255 if v>=128 else 0));return out
 fit=None
 for width in range(88,77,-1):
  for cut in range(350,391,2):
   for x in range(1,10):
    im=bands(raw,width,x,[cut,raw.height],[31,63])
    other=bands(step,width,x,[cut,step.height],[31,63])
    if any(((np.array(v.getchannel('A'))>0)&~masks[2]).any()for v in [im,other]):continue
    fit=(width,x,cut,im,other);break
   if fit:break
  if fit:break
 assert fit,'Cannot register whole sentinel without clipping'
 width,x,cut,base,step=fit
 palette=base.convert('RGB').quantize(colors=128)
 def quant(im):
  alpha=im.getchannel('A');out=im.convert('RGB').quantize(palette=palette,dither=Image.Dither.NONE).convert('RGBA');out.putalpha(alpha);return out
 base,step=quant(base),quant(step)
 left=step.crop((16,48,48,96));right=left.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
 pose0=base.copy();pose0.paste(left,(16,48))
 pose1=base.copy();pose1.paste(right,(48,48))
 attack=Image.open(g/'temple_sentinel_attack_corrected.png').convert('RGBA')
 abox=attack.getchannel('A').point(lambda v:255 if v>=160 else 0).getbbox();attack=attack.crop(abox)
 attack_fit=None
 # The attack's outer right hand starts in the second native tile row.
 # Register that complete row separately; never trim the hand to fit a cell.
 for aw in range(width,77,-1):
  for ax in range(1,10):
   for middlecut in range(390,431,10):
    for topcut in range(130,201,10):
     candidate=bands(attack,aw,ax,[topcut,middlecut,attack.height],[15,16,63])
     if ((np.array(candidate.getchannel('A'))>0)&~masks[3]).any():continue
     attack_fit=(aw,ax,topcut,middlecut,candidate);break
    if attack_fit:break
   if attack_fit:break
  if attack_fit:break
 assert attack_fit,'Attack cannot fit native union without clipping'
 aw,ax,topcut,middlecut,attack=attack_fit;attack=quant(attack)
 pose3=base.copy()
 for t,xx,yy in layouts[3]['layout']:
  if int(t,16)<0xce6:continue
  X,Y=xx*2,yy*2;pose3.paste(attack.crop((X,Y,X+16,Y+16)),(X,Y))
 # The missing upper-right native cell is genuinely empty in this pose.
 pose3.paste(Image.new('RGBA',(16,16)),(80,0))
 poses=[pose0,pose1,base,pose3];shared={}
 for i,(im,layout)in enumerate(zip(poses,layouts)):
  assert not ((np.array(im.getchannel('A'))>0)&~masks[i]).any()
  for t,xx,yy in layout['layout']:
   cell=im.crop((xx*2,yy*2,xx*2+16,yy*2+16)).tobytes()
   if t in shared:assert cell==shared[t],('Shared animation cell changed',i,t)
   shared[t]=cell
  im.save(a/f'sentinel_{i}.png')
 report=dict(size=[96,96],source_bbox=list(box),body_fit=dict(width=width,x=x,source_cut=cut,band_heights=[31,63],y=1),attack_bbox=list(abox),attack_fit=dict(width=aw,x=ax,source_cuts=[topcut,middlecut],band_heights=[15,16,63],y=1),clipped_pixels=0,shared_native_cells_exact=True,leg_states='standing, complete raised left leg, mirrored raised right leg; static upper body retained',native_layouts=layouts)
 (a/'sentinel_registration.json').write_text(json.dumps(report,indent=2)+'\n')
 return poses,report

if __name__=='__main__':
 poses,report=prepare(Path(__file__).resolve().parents[1]);print(json.dumps({k:v for k,v in report.items()if k!='native_layouts'},indent=2))
