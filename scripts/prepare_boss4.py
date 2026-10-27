"""Register complete rotating tower bands and the two whole ring frames."""
from pathlib import Path
import json,math
import numpy as np
from PIL import Image,ImageOps

def prepare(root):
 a=root/'art/level4_finale';g=root/'art/generated'
 raw=Image.open(g/'boss4_body.png').convert('RGB').resize((224,64),Image.Resampling.LANCZOS)
 # Move one continuous generated material around a cylinder; fixed lighting
 # avoids carrying a dark edge into the bright front as each band turns.
 src=np.array(raw,dtype=float);lum=src.mean((0,2));smooth=np.convolve(np.pad(lum,(16,16),mode='wrap'),np.ones(33)/33,mode='valid');surface=np.clip(src*(100/np.maximum(smooth,30))[None,:,None],0,255)
 opened=Image.open(g/'boss4_eye.png').convert('RGBA');closed=Image.open(g/'boss4_closed.png').convert('RGBA');box=opened.getchannel('A').point(lambda v:255 if v>=180 else 0).getbbox();opened=opened.crop(box);closed=closed.crop(box)
 # Native eye bounds in the56x32 band, including partially wrapped side eyes.
 eyes={0:[('closed',(12,7,22,18))],1:[('open',(4,10,19,24)),('closed',(34,7,43,18))],2:[('closed',(12,15,22,26)),('open',(36,10,52,24))],3:[('open',(18,10,38,24)),('closed',(-6,15,4,26)),('closed',(54,7,63,18))],4:[('closed',(23,15,33,26)),('open',(47,10,65,24))],5:[('open',(-10,6,6,20)),('closed',(54,15,63,26))],6:[('open',(-5,10,15,24)),('closed',(23,7,33,18))],7:[('closed',(34,15,43,26))]}
 order=[3,2,4,7,5,0,6,1];panels=[]
 for phase in range(8):
  angle=order.index(phase)/8;x=(np.arange(112)+.5)/56-1;theta=np.arcsin(x);u=((theta/(2*math.pi)+.5+angle)*224)%224;left=np.floor(u).astype(int);frac=u-left
  rgb=surface[:,left]*(1-frac)[None,:,None]+surface[:,(left+1)%224]*frac[None,:,None];shade=.26+.77*np.sqrt(1-x*x)+.12*(-x);rgb=np.clip(rgb*shade[None,:,None],0,255).astype('uint8');im=Image.fromarray(rgb).convert('RGBA')
  for state,bounds in eyes[phase]:
   x0,y0,x1,y1=[v*2 for v in bounds];eye=(opened if state=='open'else closed).resize((x1-x0,y1-y0),Image.Resampling.LANCZOS);eye.putalpha(eye.getchannel('A').point(lambda v:255 if v>=140 else 0));im.alpha_composite(eye,(x0,y0))
  panels.append(im)
 combined=Image.new('RGB',(112,64*8))
 for i,im in enumerate(panels):combined.paste(im,(0,i*64))
 palette=combined.quantize(colors=192)
 panels=[im.convert('RGB').quantize(palette=palette,dither=Image.Dither.NONE).convert('RGBA')for im in panels]
 for i,im in enumerate(panels):im.save(a/f'tower_band_{i}.png')
 # Both frames use one scale, preserving the ring's diameter while its points
 # rotate. Tight-cropping and scaling each separately would make it breathe.
 raw=Image.open(g/'boss4_ring.png').convert('RGBA');rings=[]
 for i,cx in enumerate([455,1321]):
  im=raw.crop((cx-350,97,cx+350,797)).resize((32,32),Image.Resampling.LANCZOS);alpha=im.getchannel('A').point(lambda v:255 if v>=140 else 0);im=im.convert('RGB').quantize(colors=96).convert('RGBA');im.putalpha(alpha);im.save(a/f'ring_{i}.png');rings.append(im)
 report=dict(band_size=[112,64],native_band_size=[56,32],phase_order=order,eye_boxes_native={str(k):v for k,v in eyes.items()},eye_common_source_box=list(box),complete_band_registration=True,ring_size=[32,32],ring_common_scale=32/700,native_gameplay_modified=False)
 (a/'art_registration.json').write_text(json.dumps(report,indent=2)+'\n');return panels,rings,report
if __name__=='__main__':prepare(Path(__file__).resolve().parents[1])
