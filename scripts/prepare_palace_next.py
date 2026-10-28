"""Register the complete rising sentry within its native row geometry."""
from pathlib import Path
import json
import numpy as np
from PIL import Image,ImageDraw
from prepare_level5 import reg
R=Path(__file__).resolve().parents[1];A=R/'art/level5_next'
def prepare():
 raw=Image.open(R/'art/generated/palace_sentry.png').convert('RGBA')
 # One source coordinate system and connected horizontal bands. The native
 # lower body repeats BE/BF, so its repeated row must be byte identical.
 cuts=[14,120,330,375,720,1050];im=Image.new('RGBA',(64,112))
 for row,(top,bottom)in enumerate(zip(cuts,cuts[1:])):
  im.paste(reg(raw.crop((160,top,788,bottom)),(64,16)),(0,row*16))
 im.paste(im.crop((16,64,48,80)),(16,80))
 im.paste(reg(raw.crop((160,1050,788,1635)),(64,16)),(0,96))
 layout=[('12B1',0,0),('12B2',48,0)]
 for first,y,xs in [(0x12b3,16,[0,16,32,48]),(0x12b7,32,[16,32]),(0x12b9,48,[0,16,32,48]),(0x12bd,64,[0,16,32,48]),(0x12be,80,[16,32]),(0x12c1,96,[16,32])]:
  layout += [(f'{first+j:04X}',x,y)for j,x in enumerate(xs)]
 mask=Image.new('L',im.size);d=ImageDraw.Draw(mask)
 for _,x,y in layout:d.rectangle((x,y,x+15,y+15),fill=255)
 outside=(np.array(im.getchannel('A'))>0)&(np.array(mask)==0)
 assert not outside.any(),f'{outside.sum()} source pixels outside native footprint'
 im.save(A/'sentry.png');(A/'sentry_layout.json').write_text(json.dumps(layout,indent=2)+'\n')
 (A/'source_registration.json').write_text(json.dumps(dict(source='art/generated/palace_sentry.png',method='whole horizontal bands before native slicing',source_x=[160,788],source_y_cuts=cuts,size=[64,112],repeated_body_cells=['12BE','12BF'],clipped_pixels=0,built_in_imagegen=True),indent=2)+'\n')
 return im
if __name__=='__main__':prepare()
