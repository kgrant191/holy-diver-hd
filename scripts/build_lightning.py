"""Register a generated lightning strike to the ROM's actual thunder event.

The title routine at bank 6:$BBEE queues sound $26, advances $04AF to $08,
then counts frames in $009F. The effect follows this state, including resets,
skipped intros and subsequent title loops. It has no free-running trigger.
"""
from pathlib import Path
from PIL import Image,ImageOps
import numpy as np
root=Path(__file__).resolve().parents[1];art=root/'art';out=root/'build/Holy_Diver_(Tr)'
fx=art/'title_fx';fx.mkdir(exist_ok=True)
title=Image.open(art/'Title_HD.png').convert('RGBA')
bolt=Image.open(art/'generated/lightning_generated.png').convert('RGBA')
bolt=bolt.crop(bolt.getbbox())
bolt=ImageOps.mirror(bolt).resize((100,282),Image.Resampling.LANCZOS)
layer=Image.new('RGBA',title.size);layer.alpha_composite(bolt,(420,-4))
b=np.asarray(layer).astype(float);scene=np.asarray(title).astype(float)
yy,xx=np.mgrid[:480,:512]
# Keep warm lettering and the bright moon in front of the distant strike.
warm=(scene[:,:,0]>scene[:,:,2]*1.15)&(scene[:,:,0]>60)
moon=(xx>415)&(xx<477)&(yy>45)&(yy<155)&(scene[:,:,:3].min(axis=2)>65)
b[:,:,3][warm|moon]=0
# Restrained local sky illumination rather than a full-screen white strobe.
falloff=np.exp(-(((xx-471)/145)**2+((yy-139)/235)**2))
sky=(scene[:,:,2]>scene[:,:,0]*1.25)&(scene[:,:,2]>scene[:,:,1]*1.03)
wash=np.zeros_like(b);wash[:,:,:3]=(164,193,255);wash[:,:,3]=falloff*sky*34
for phase,strength in enumerate([1,.52,.20,.07]):
 ambient=wash.copy();ambient[:,:,3]*=strength
 strike=b.copy();strike[:,:,3]*=strength*.94
 result=Image.alpha_composite(Image.fromarray(ambient.astype('uint8')),Image.fromarray(strike.astype('uint8')))
 result.save(out/f'Title_Lightning_{phase}.png');result.save(fx/f'Title_Lightning_{phase}.png')
conditions=['<condition>titleThunder,memoryCheckConstant,04AF,==,08',
            '<condition>titleThunderSound,memoryCheckConstant,01BC,==,26']
edges=[1,6,9,13,17,23,33,49]
conditions += [f'<condition>thunderTime{n},memoryCheckConstant,009F,>=,{n:02X}' for n in edges]
rules=[]
for start,end,asset in [(1,6,0),(6,9,1),(9,13,2),(13,17,0),(17,23,1),(23,33,2),(33,49,3)]:
 cond=f'titleScreen&titleLogoB&titleThunder&titleThunderSound&thunderTime{start}&!thunderTime{end}'
 rules.append(f'[{cond}]<background>Title_Lightning_{asset}.png,1,0,0,32,0,0')
p=out/'hires.txt';s=p.read_text();pos=s.index('#Chr_00_0.png')
s=s[:pos]+'\n'.join(conditions+rules)+'\n'+s[pos:];p.write_text(s)
