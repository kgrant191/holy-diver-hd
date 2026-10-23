"""Arrange unretouched paired Mesen captures for the user's visual review."""
from pathlib import Path
import argparse
from PIL import Image, ImageDraw, ImageFont

p=argparse.ArgumentParser()
for name in ['before','after','out']:p.add_argument('--'+name,required=True)
a=p.parse_args();root=Path(__file__).resolve().parents[1]
font=lambda size:ImageFont.truetype(str(root/'art/fonts/DejaVuSerif-Bold.ttf'),size)
cases=[('Boss standing','entry',320),('Crouched fire','entry',422),
       ('White hit flash','hit',285),('Progressive defeat','pickup',180),
       ('Blizzard chamber','pickup',720),('Spell announcement','pickup',1400)]
im=Image.new('RGB',(1056,144+len(cases)*520),'#081223');d=ImageDraw.Draw(im)
d.text((24,22),'HOLY DIVER HD · FIRST BOSS',font=font(27),fill='#f3ddb1')
d.text((24,66),'Approved 0.2.1',font=font(18),fill='#bec7d8')
d.text((544,66),'0.3.0 review candidate',font=font(18),fill='#b9e8fa')
for i,(label,case,frame)in enumerate(cases):
    y=108+i*520;d.text((24,y),label,font=font(16),fill='#d9b779')
    for x,directory in [(16,Path(a.before)),(536,Path(a.after))]:
        shot=Image.open(directory/case/'frames'/f'{frame:04}.png').convert('RGB')
        assert shot.size==(512,480)
        im.paste(shot,(x,y+28))
d.text((24,im.height-25),'Actual Mesen captures · original 2× output · controller input only',font=font(12),fill='#b0bccf')
out=Path(a.out);out.parent.mkdir(parents=True,exist_ok=True);im.save(out)
print(out)
