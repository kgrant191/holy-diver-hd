"""Export unretouched paired emulator crops at the left stop and right walk-off."""
from pathlib import Path
import argparse
import json
import shutil
from PIL import Image, ImageDraw, ImageFont

p = argparse.ArgumentParser()
for name in ['before', 'after', 'out']:
    p.add_argument('--'+name, required=True)
a = p.parse_args()
out = Path(a.out)
out.mkdir(parents=True, exist_ok=True)
font_path = str(Path(__file__).resolve().parents[1]/'art/fonts/DejaVuSerif-Bold.ttf')
font, title = ImageFont.truetype(font_path, 16), ImageFont.truetype(font_path, 22)
rows = [('Upper: far-left standing position', 'upper', 140, 96),
        ('Upper: falling beyond the right edge', 'upper', 361, 96),
        ('Lower: far-left standing position', 'lower', 140, 272),
        ('Lower: falling beyond the right edge', 'lower', 425, 272)]
canvas = Image.new('RGB', (956, 1376), '#101827')
draw = ImageDraw.Draw(canvas)
draw.text((20, 14), 'Ledge boundary correction — actual Mesen captures', font=title, fill='#f0dfbd')
draw.text((20, 50), 'Previous 0.0.2 candidate', font=font, fill='#b5bdce')
draw.text((488, 50), 'Revised 0.0.2 candidate', font=font, fill='#b5bdce')
y = 86
for label, case, frame, surface in rows:
    draw.text((20, y), label, font=font, fill='#f0dfbd')
    y += 28
    for source, x in [(Path(a.before), 20), (Path(a.after), 488)]:
        d = source/case
        camera = (d/f'dumps/{frame:04}.ram').read_bytes()[0x3cf]
        top = (surface-camera)*2-100
        im = Image.open(d/f'frames/{frame:04}.png').convert('RGB')
        canvas.paste(im.crop((0, top, 224, top+136)).resize((448, 272), Image.Resampling.NEAREST), (x, y))
    shutil.copyfile(Path(a.after)/case/f'frames/{frame:04}.png', out/f'{case}_{frame:04}.png')
    y += 292
canvas.crop((0, 0, 956, y)).save(out/'comparison.png')
for case in ['upper', 'lower']:
    for variant in ['before', 'after']:
        source = Path(getattr(a, variant))/case/'installed_pack_sha256.json'
        shutil.copyfile(source, out/f'{variant}_{case}_installed_pack_sha256.json')
