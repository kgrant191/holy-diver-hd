"""Export actual replay crops; nearest-neighbor scaling only, no retouching."""
from pathlib import Path
import argparse
from PIL import Image,ImageDraw,ImageFont
p=argparse.ArgumentParser();p.add_argument('--root',required=True);p.add_argument('--out',required=True);a=p.parse_args()
w=Path(a.root);out=Path(a.out);out.mkdir(parents=True,exist_ok=True)
font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',12)
canvas=Image.new('RGB',(736,1112),'#111b2a');d=ImageDraw.Draw(canvas)
d.text((12,10),'Holy Diver HD 0.1.1 — live Mesen comparisons',font=font,fill='white')
d.text((12,30),'Each pair: 0.1.0 before / 0.1.1 after. Crops enlarged 2x without smoothing.',font=font,fill='#b8c7dc')
for i,(mode,frame,label) in enumerate([
 ('normal',44,'Normal / right wind-up'),('normal',48,'Normal / right release'),
 ('normal',154,'Normal / left wind-up'),('normal',158,'Normal / left release'),
 ('twin',44,'Twin Fire / right wind-up'),('twin',48,'Twin Fire / right release'),
 ('twin',154,'Twin Fire / left wind-up'),('twin',158,'Twin Fire / left release')]):
 x=i%2*368;y=60+i//2*176
 d.text((x+10,y),label,font=font,fill='white')
 for col,build in enumerate(['before','after']):
  image=Image.open(w/build/mode/f'frames/{frame:04}.png').crop((388,324,472,388))
  canvas.paste(image.resize((168,128),Image.Resampling.NEAREST),(x+10+col*180,y+24))
for i,frame in enumerate([20,28,180,300]):
 x=i%2*368;y=780+i//2*160
 d.text((x+10,y),f'Ghoul standing / frame {frame}',font=font,fill='white')
 for col,build in enumerate(['ghoul_before','ghoul_after']):
  r=w/build/'state2';b=(r/f'dumps/{frame-2:04}.oam').read_bytes()
  sprites=[(x,y)for y,t,a,x in[b[k:k+4]for k in range(0,256,4)]if y<239 and a&3==1 and 0x94<=t<=0xab]
  cx=min(x for x,y in sprites)*2;cy=(min(y for x,y in sprites)+1)*2
  image=Image.open(r/f'frames/{frame:04}.png').crop((cx-10,cy-4,cx+50,cy+52))
  canvas.paste(image.resize((120,112),Image.Resampling.NEAREST),(x+30+col*180,y+24))
canvas.save(out/'comparison.png')
# Also preserve one full unretouched screenshot for spatial context.
Image.open(w/'after/twin/frames/0158.png').save(out/'crouch_full_frame.png')
Image.open(w/'ghoul_after/state2/frames/0020.png').save(out/'ghoul_full_frame.png')
print(out/'comparison.png')
