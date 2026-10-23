"""Export paired live standing/crouching crops with labeled pixel enlargement."""
from pathlib import Path
import argparse
from PIL import Image,ImageDraw,ImageFont

p=argparse.ArgumentParser()
for name in ['before','after','out']:p.add_argument('--'+name,required=True)
a=p.parse_args();root=Path(__file__).resolve().parents[1]
font=lambda n:ImageFont.truetype(str(root/'art/fonts/DejaVuSerif-Bold.ttf'),n)
out=Image.new('RGB',(808,1410),'#0b1421');d=ImageDraw.Draw(out)
d.text((16,15),'Holy Diver HD 0.3.3 — standing boot',font=font(23),fill='#f1d9ac')
d.text((16,52),'Actual Mesen captures • 3× nearest-neighbor crops',font=font(14),fill='#b7cada')
d.text((16,83),'0.3.2 — before',font=font(17),fill='#d6e2ec')
d.text((416,83),'0.3.3 — corrected',font=font(17),fill='#d6e2ec')
rows=[('Standing right — normal','normal',110),('Standing left — normal','normal',85),
      ('Standing right — Twin Fire','twin',110),('Crouching — unchanged','normal',155)]
for i,(label,case,frame) in enumerate(rows):
    y=116+i*320;d.text((16,y),label,font=font(15),fill='#f1d9ac')
    for j,folder in enumerate([a.before,a.after]):
        im=Image.open(Path(folder)/case/'frames'/f'{frame:04}.png').convert('RGB')
        assert im.size==(512,480)
        im=im.crop((0,120,128,216)).resize((384,288),Image.Resampling.NEAREST)
        out.paste(im,(12+j*400,y+24))
path=Path(a.out);path.parent.mkdir(parents=True,exist_ok=True);out.save(path)
print(path)
