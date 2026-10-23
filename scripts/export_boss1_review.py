"""Export unretouched paired Mesen screenshots for the fireball/menu repair."""
from pathlib import Path
import argparse
from PIL import Image,ImageDraw,ImageFont

p=argparse.ArgumentParser()
for name in ['before','after','out']:p.add_argument('--'+name,required=True)
a=p.parse_args()
root=Path(__file__).resolve().parents[1]
font=lambda n:ImageFont.truetype(str(root/'art/fonts/DejaVuSerif-Bold.ttf'),n)
rows=[('Fireball — boss facing left','crouch',24),
      ('Fireball — boss facing right','crouch',380),
      ('Blizzard selected in the pause menu','menu_blizzard',1980)]
out=Image.new('RGB',(1048,1660),'#0b1421');d=ImageDraw.Draw(out)
d.text((20,15),'Holy Diver HD 0.3.1 — review fixes',font=font(24),fill='#f1d9ac')
d.text((20,52),'Actual Mesen captures • original artwork and gameplay retained',font=font(14),fill='#b7cada')
d.text((16,83),'0.3.0 — before',font=font(17),fill='#d6e2ec')
d.text((536,83),'0.3.1 — corrected',font=font(17),fill='#d6e2ec')
for i,(label,case,frame) in enumerate(rows):
    y=116+i*510
    d.text((16,y),label,font=font(16),fill='#f1d9ac')
    for j,folder in enumerate([a.before,a.after]):
        im=Image.open(Path(folder)/case/'frames'/f'{frame:04}.png').convert('RGB')
        assert im.size==(512,480)
        out.paste(im,(8+j*520,y+25))
path=Path(a.out);path.parent.mkdir(parents=True,exist_ok=True);out.save(path)
print(path)
