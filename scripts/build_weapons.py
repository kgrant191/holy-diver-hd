"""Slice eight generated projectile frames into the existing 8×8 NES footprint."""
from pathlib import Path
from PIL import Image,ImageDraw
import numpy as np
root=Path(__file__).resolve().parents[1];art=root/'art';out=root/'build/Holy_Diver_(Tr)'
src=Image.open(art/'generated/weapons_generated.png').convert('RGBA')
atlas=Image.new('RGBA',(64,32))
for row in range(2):
 for col in range(4):
  cell=src.crop((round(col*src.width/4),round(row*src.height/2),round((col+1)*src.width/4),round((row+1)*src.height/2)))
  mask=cell.getchannel('A').point(lambda v:255 if v>=150 else 0)
  cell=cell.crop(mask.getbbox())
  # Fixed leading-core/center registration and enough height for flicker.
  cell=cell.resize((16,12),Image.Resampling.LANCZOS)
  a=cell.getchannel('A').point(lambda v:255 if v>=100 else 0)
  cell=cell.convert('RGB').quantize(colors=18,method=Image.Quantize.MEDIANCUT).convert('RGBA');cell.putalpha(a)
  atlas.alpha_composite(cell,(col*16,row*16+2))
atlas.save(art/'Weapon_Effects_2x.png');atlas.save(out/'Weapon_Effects_2x.png')
preview=Image.new('RGB',(512,256),'#101e38');big=atlas.resize((512,256),Image.Resampling.NEAREST);preview.paste(big,(0,0),big);preview.save(art/'weapon_effects_preview.png')
scope='gameplay&entranceLowerA&entranceLowerB&entrancePillar&litPalette'
conditions=['<condition>twinFireEquipped,ppuMemoryCheckConstant,3F1D,==,22']
for i in range(1,4):conditions.append(f'<condition>firePhase{i},frameRange,16,{i*4}')
rules=[]
for row in range(2):
 for i in [3,2,1,0]:
  condition=scope+('&twinFireEquipped' if row else '&!twinFireEquipped')+(f'&firePhase{i}' if i else '')
  rules.append(f'[{condition}]<tile>20,43,FF301116,{i*16},{row*16},1,N')
base=(out/'hires.txt').read_text();pos=base.index('#Chr_00_0.png')
base=base[:pos]+'<img>Weapon_Effects_2x.png\n'+'\n'.join(conditions+rules)+'\n'+base[pos:]
(out/'hires.txt').write_text(base)
