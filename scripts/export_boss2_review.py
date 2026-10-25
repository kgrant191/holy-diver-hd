"""Export unretouched paired Mesen captures for the two boss repairs."""
from pathlib import Path
import hashlib
import json
import subprocess
from PIL import Image, ImageDraw, ImageFont

root = Path(__file__).resolve().parents[1]
work = root / 'work/boss2_review'
out = root / 'evidence/boss2_review'
out.mkdir(exist_ok=True)
font = '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
small, large = ImageFont.truetype(font, 18), ImageFont.truetype(font, 22)
sources = []


def frame(n, side):
    path = work / side / 'pickup/frames' / f'{n:04}.png'
    sources.append(dict(path=str(path.relative_to(root)),
                        sha256=hashlib.sha256(path.read_bytes()).hexdigest()))
    return Image.open(path).convert('RGB')


comparison = Image.new('RGB', (1056, 1128), '#0b0e19')
d = ImageDraw.Draw(comparison)
d.text((16, 14), 'HOLY DIVER HD 0.10.1 — BOSS DEFEAT / BREAKER FIXES', font=large, fill='#ebcf91')
d.text((16, 48), 'Actual Mesen captures • left: 0.10.0 • right: 0.10.1', font=small, fill='#b9c7d9')
for n, y, label in [(172, 116, 'HD boss retained throughout the gold defeat fade'),
                    (254, 640, 'Defeated boss stays hidden during the Breaker flash')]:
    d.text((16, y-30), label, font=large, fill='#ebcf91')
    comparison.paste(frame(n, 'before'), (16, y))
    comparison.paste(frame(n, 'after'), (528, y))
comparison.save(out / 'comparison.png')
cmd = ['ffmpeg', '-y', '-v', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24',
       '-s', '1024x528', '-r', '60', '-i', '-', '-an', '-c:v', 'libx264',
       '-crf', '18', '-pix_fmt', 'yuv420p', '-movflags', '+faststart', str(out/'review.mp4')]
process = subprocess.Popen(cmd, stdin=subprocess.PIPE)
for n in range(130, 761):
    picture = Image.new('RGB', (1024, 528), '#0b0e19')
    draw = ImageDraw.Draw(picture)
    draw.text((12, 10), f'0.10.0  →  0.10.1     |     Actual Mesen frame {n}', font=small, fill='#ebcf91')
    picture.paste(frame(n, 'before'), (0, 48))
    picture.paste(frame(n, 'after'), (512, 48))
    process.stdin.write(picture.tobytes())
process.stdin.close()
assert process.wait() == 0
subprocess.run(['ffmpeg', '-v', 'error', '-i', str(out/'review.mp4'), '-f', 'null', '-'], check=True)
(out/'preview_sources.json').write_text(json.dumps(dict(
    source='paired actual Mesen captures', unretouched=True,
    still_frames=[172, 254], video_frames=[130, 760], video_fps=60,
    frames=sources), indent=2)+'\n')
print('Exported paired comparison and normal-speed video; decode passed.')
