"""Show the reported scrolling dropouts using paired real Mesen captures."""
from pathlib import Path
import argparse
import subprocess
from PIL import Image, ImageDraw, ImageFont

parser = argparse.ArgumentParser()
for key in ['before', 'after', 'work', 'out']:
    parser.add_argument('--' + key, required=True)
args = parser.parse_args()
root = Path(__file__).resolve().parents[1]
work = Path(args.work)
work.mkdir(parents=True, exist_ok=True)
font = ImageFont.truetype(str(root / 'art/fonts/DejaVuSerif-Bold.ttf'), 15)
fps = 60.0988138974405
clips = []
for name, start, end, speed in [('scroll', 230, 510, 1), ('return', 1130, 1220, .5)]:
    folder = work / name
    folder.mkdir(exist_ok=True)
    for index, n in enumerate(range(start, end)):
        image = Image.new('RGB', (1024, 512), '#10131a')
        draw = ImageDraw.Draw(image)
        for col, (capture, label) in enumerate([(args.before, '0.20.4 before'), (args.after, '0.20.5 repaired')]):
            image.paste(Image.open(Path(capture) / 'frames' / f'{n:06}.png'), (col*512, 32))
            rate = 'normal speed' if speed == 1 else 'half speed'
            draw.text((col*512+10, 8), f'{label} — actual replay, {rate}', font=font, fill='#ead7ac')
        image.save(folder / f'{index:06}.png', compress_level=1)
    clip = work / (name + '.mp4')
    subprocess.run([
        'ffmpeg', '-y', '-hide_banner', '-loglevel', 'error',
        '-framerate', str(fps*speed), '-i', str(folder / '%06d.png'),
        '-ss', str((start-1)/fps), '-i', str(Path(args.after) / 'full.wav'),
        '-t', str((end-start)/(fps*speed)), '-af', f'atempo={speed}',
        '-c:v', 'libx264', '-preset', 'fast', '-crf', '19', '-pix_fmt', 'yuv420p',
        '-r', '60', '-threads', '2', '-c:a', 'aac', '-ar', '48000', '-b:a', '128k', str(clip)
    ], check=True)
    clips.append(clip)
listing = work / 'concat.txt'
listing.write_text(''.join("file '" + str(clip) + "'\n" for clip in clips))
subprocess.run(['ffmpeg', '-y', '-hide_banner', '-loglevel', 'error', '-f', 'concat',
                '-safe', '0', '-i', str(listing), '-c', 'copy', '-movflags', '+faststart', args.out], check=True)
print(args.out)
