"""Export unretouched Mesen frames with labels and nearest-neighbor crops."""
from pathlib import Path
import argparse, json
from PIL import Image, ImageDraw, ImageFont

p=argparse.ArgumentParser()
for n in ['before','after','cave-before','cave-after','out']:p.add_argument('--'+n,required=True)
a=p.parse_args();out=Path(a.out);out.mkdir(parents=True,exist_ok=True)
root=Path(__file__).resolve().parents[1]
font=ImageFont.truetype(str(root/'art/fonts/DejaVuSerif-Bold.ttf'),17)
rows=[
    ('Cave first reveal / full frame',Path(a.cave_before)/'walk_right/frames/0045.png',Path(a.cave_after)/'walk_right/frames/0045.png',None),
    ('Winged demon / 4x live crop',Path(a.before)/'entry_combat/frames/0040.png',Path(a.after)/'entry_combat/frames/0040.png',(372,206,500,302)),
    ('Pulsing rock / 4x live crop',Path(a.before)/'red_combat/frames/0010.png',Path(a.after)/'red_combat/frames/0010.png',(384,264,512,360)),
]
height=48+sum(36+(480 if crop is None else 384) for _,_,_,crop in rows)
canvas=Image.new('RGB',(1024,height),'#171923');d=ImageDraw.Draw(canvas)
d.text((12,12),'0.4.0 — reported issues',font=font,fill='#eeeeee')
d.text((524,12),'0.4.1 — review repairs',font=font,fill='#eeeeee')
y=48
for title,b,c,crop in rows:
    d.text((12,y+8),title,font=font,fill='#e0c289');y+=36
    for x,f in [(0,b),(512,c)]:
        im=Image.open(f).convert('RGB')
        if crop:im=im.crop(crop).resize((512,384),Image.Resampling.NEAREST)
        canvas.paste(im,(x,y))
    y+=480 if crop is None else 384
canvas.save(out/'comparison.png')
sources=[{'title':t,'before':str(b),'after':str(c),'crop':crop,'scale':4 if crop else 1} for t,b,c,crop in rows]
(out/'preview_sources.json').write_text(json.dumps(sources,indent=2)+'\n')
print(out/'comparison.png')
