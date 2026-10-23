"""Export actual paired Mesen captures, with labeled nearest-neighbor crops."""
from pathlib import Path
import argparse
from PIL import Image,ImageDraw,ImageFont

p=argparse.ArgumentParser()
for name in ['before','after','out']:p.add_argument('--'+name,required=True)
a=p.parse_args();root=Path(__file__).resolve().parents[1]
font=lambda n:ImageFont.truetype(str(root/'art/fonts/DejaVuSerif-Bold.ttf'),n)
out=Image.new('RGB',(1048,1410),'#0b1421');d=ImageDraw.Draw(out)
d.text((20,15),'Holy Diver HD 0.3.2 — Blizzard transition',font=font(23),fill='#f1d9ac')
d.text((20,52),'Actual Mesen captures • native timing, foreground and audio retained',font=font(14),fill='#b7cada')
d.text((16,83),'0.3.1 — before',font=font(17),fill='#d6e2ec')
d.text((536,83),'0.3.2 — corrected',font=font(17),fill='#d6e2ec')
rows=[('Ascent: wall continues behind the native bell and ornaments','menu_blizzard',1000,None,116),
      ('Final fade: facing left • 3× nearest-neighbor crop','menu_blizzard',1315,(192,232,352,344),635),
      ('Final fade: facing right • 3× nearest-neighbor crop','reverse_blizzard',1587,(160,232,320,344),1020)]
for label,case,frame,crop,y in rows:
    d.text((16,y),label,font=font(15),fill='#f1d9ac')
    for j,folder in enumerate([a.before,a.after]):
        im=Image.open(Path(folder)/case/'frames'/f'{frame:04}.png').convert('RGB')
        assert im.size==(512,480)
        if crop:im=im.crop(crop).resize((480,336),Image.Resampling.NEAREST)
        out.paste(im,(8+j*520+(512-im.width)//2,y+25))
path=Path(a.out);path.parent.mkdir(parents=True,exist_ok=True);out.save(path)
print(path)
