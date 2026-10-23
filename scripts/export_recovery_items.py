"""Export actual HP and Magic flask captures at labeled 3x pixel enlargement."""
from pathlib import Path
import argparse
from PIL import Image, ImageDraw, ImageFont

p = argparse.ArgumentParser()
for name in ['before', 'after', 'out']:
    p.add_argument('--' + name, required=True)
a = p.parse_args(); root = Path(__file__).resolve().parents[1]
font = lambda n: ImageFont.truetype(str(root/'art/fonts/DejaVuSerif-Bold.ttf'), n)
out = Image.new('RGB', (1008, 868), '#0b1421'); d = ImageDraw.Draw(out)
d.text((16, 14), 'Holy Diver HD 0.3.5 — HP and Magic flasks', font=font(25), fill='#f1d9ac')
d.text((16, 52), 'Actual Mesen captures • 3× nearest-neighbor crops', font=font(15), fill='#b7cada')
d.text((16, 84), '0.3.4 — original pickups', font=font(18), fill='#d6e2ec')
d.text((520, 84), '0.3.5 — HD pickups', font=font(18), fill='#d6e2ec')
for i, (label, case, rect) in enumerate([
        ('Red HP flask', 'hp_drop', (352, 280, 512, 392)),
        ('Blue Magic flask', 'magic_drop', (288, 288, 448, 400))]):
    y = 120 + i * 368
    d.text((16, y), label, font=font(17), fill='#f1d9ac')
    for j, folder in enumerate([a.before, a.after]):
        im = Image.open(Path(folder)/case/'frames/0020.png').convert('RGB')
        out.paste(im.crop(rect).resize((480, 336), Image.Resampling.NEAREST), (16+j*504, y+26))
path = Path(a.out); path.parent.mkdir(parents=True, exist_ok=True); out.save(path)
print(path)
