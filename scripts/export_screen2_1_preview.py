"""Export labeled, unretouched runtime comparisons from the paired replays."""
from pathlib import Path
import argparse
from PIL import Image, ImageDraw, ImageFont
import json

p=argparse.ArgumentParser()
for n in ['before','after','out']:p.add_argument('--'+n,required=True)
a=p.parse_args();out=Path(a.out);out.mkdir(parents=True,exist_ok=True)
root=Path(__file__).resolve().parents[1]
font=ImageFont.truetype(str(root/'art/fonts/DejaVuSerif-Bold.ttf'),18)
small=ImageFont.truetype(str(root/'art/fonts/DejaVuSerif-Bold.ttf'),14)
samples=[('Volcanic exterior / flying enemy','entry_combat',300),
         ('Hot lava','cast_thaw',10),('Blizzard ice','cast_thaw',300),
         ('Lava creature / normal Randy','red_combat',40),
         ('Breakable blocks','crossing',1120),('Exit cliff','crossing',2220)]
canvas=Image.new('RGB',(1056,80+len(samples)*524),'#0b101b');d=ImageDraw.Draw(canvas)
d.text((16,14),'HOLY DIVER HD 0.4.0 — STAGE 2 / SCREEN 1',font=font,fill='#ecd4a5')
d.text((16,47),'Actual Mesen captures · approved 0.3.5 at left · candidate at right',font=small,fill='#b7c2d4')
metadata=[]
for i,(label,case,n) in enumerate(samples):
    y=80+i*524;d.text((16,y+4),label,font=font,fill='#d5ba82')
    for j,base in enumerate([a.before,a.after]):
        src=Path(base)/case/f'frames/{n:04}.png';im=Image.open(src).convert('RGB')
        assert im.size==(512,480);canvas.paste(im,(16+j*512,y+32))
    metadata.append(dict(label=label,case=case,frame=n,retouched=False))
canvas.save(out/'comparison.png')
(out/'comparison_sources.json').write_text(json.dumps(metadata,indent=2)+'\n')
# Compact review image of the key state change, using full original frames.
pair=Image.new('RGB',(1024,520),'#0b101b');pd=ImageDraw.Draw(pair)
for i,(n,label) in enumerate([(10,'LAVA'),(300,'BLIZZARD ICE')]):
    pd.text((i*512+16,12),label,font=font,fill='#ecd4a5')
    pair.paste(Image.open(Path(a.after)/'cast_thaw'/f'frames/{n:04}.png').convert('RGB'),(i*512,40))
pair.save(out/'lava_and_ice.png')
print(out/'comparison.png')
