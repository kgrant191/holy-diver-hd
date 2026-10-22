"""Lay out paired real emulator captures; do not fabricate gameplay scenes."""
from pathlib import Path
import argparse
from PIL import Image, ImageDraw, ImageFont

parser = argparse.ArgumentParser()
parser.add_argument('--before', required=True)
parser.add_argument('--after', required=True)
parser.add_argument('--out', required=True)
args = parser.parse_args()
root = Path(__file__).resolve().parents[1]
font_path = str(root/'art/fonts/DejaVuSerif-Bold.ttf')
small, large = ImageFont.truetype(font_path, 16), ImageFont.truetype(font_path, 22)
rows = [('Title before Start', 'title', 240, (0, 368, 512, 472), (512, 208)),
        ('Title after first Start', 'title', 420, (0, 368, 512, 472), (512, 208)),
        ('Upper rock ledge', 'upper_left', 840, (72, 120, 200, 224), (384, 312)),
        ('Lower rock ledge', 'lower_left', 1200, (104, 246, 232, 350), (384, 312))]
height = 94 + sum(size[1]+49 for _, _, _, _, size in rows)
canvas = Image.new('RGB', (1060, height), '#101827')
draw = ImageDraw.Draw(canvas)
draw.text((20, 14), 'Title and entrance fixes — actual Mesen captures', font=large, fill='#f0dfbd')
draw.text((20, 52), 'Before: 0.0.1', font=small, fill='#a9b5c8')
draw.text((548, 52), 'After: 0.0.2 candidate', font=small, fill='#a9b5c8')
y = 84
for label, case, frame, box, size in rows:
    draw.text((20, y), label, font=small, fill='#f0dfbd')
    y += 29
    for source, x in [(Path(args.before), 20), (Path(args.after), 548)]:
        capture = Image.open(source/case/'frames'/f'{frame:04}.png').convert('RGB')
        canvas.paste(capture.crop(box).resize(size, Image.Resampling.NEAREST), (x, y))
    y += size[1]+20
out = Path(args.out)
out.parent.mkdir(parents=True, exist_ok=True)
canvas.save(out)
