"""Compare unretouched live knee/boot joins against the dark entrance backdrop."""
from pathlib import Path
import argparse
from PIL import Image, ImageDraw, ImageFont

p = argparse.ArgumentParser()
for name in ['before', 'after', 'out']:
    p.add_argument('--' + name, required=True)
a = p.parse_args()
root = Path(__file__).resolve().parents[1]
font = lambda n: ImageFont.truetype(str(root / 'art/fonts/DejaVuSerif-Bold.ttf'), n)
out = Image.new('RGB', (816, 1570), '#0b1421')
d = ImageDraw.Draw(out)
d.text((16, 15), 'Holy Diver HD 0.3.4 — connected standing leg', font=font(22), fill='#f1d9ac')
d.text((16, 51), 'Live Mesen captures • 4× nearest-neighbor crops', font=font(14), fill='#b7cada')
d.text((16, 82), '0.3.3 — broken knee join', font=font(16), fill='#d6e2ec')
d.text((416, 82), '0.3.4 — continuous leg', font=font(16), fill='#d6e2ec')
rows = [('Standing right — normal', 'clear_normal', 120),
        ('Standing left — normal', 'clear_normal', 160),
        ('Standing right — Twin Fire', 'clear_twin', 120),
        ('Crouching — unchanged', 'clear_normal', 190)]
for i, (label, case, frame) in enumerate(rows):
    y = 116 + i * 360
    d.text((16, y), label, font=font(15), fill='#f1d9ac')
    for j, folder in enumerate([a.before, a.after]):
        im = Image.open(Path(folder) / case / 'frames' / f'{frame:04}.png').convert('RGB')
        assert im.size == (512, 480)
        crop = im.crop((176, 248, 272, 328)).resize((384, 320), Image.Resampling.NEAREST)
        out.paste(crop, (16 + j * 400, y + 25))
path = Path(a.out)
path.parent.mkdir(parents=True, exist_ok=True)
out.save(path)
print(path)
