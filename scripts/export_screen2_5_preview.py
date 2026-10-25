"""Export actual stair/cavern comparisons and a silent gameplay-speed video."""
from pathlib import Path
import argparse,json,subprocess
from PIL import Image,ImageDraw,ImageFont
p=argparse.ArgumentParser()
for k in ['before','after','stairs-before','out']:p.add_argument('--'+k,required=True)
a=p.parse_args();root=Path(__file__).resolve().parents[1];out=Path(a.out);out.mkdir(parents=True,exist_ok=True)
font=ImageFont.truetype(str(root/'art/fonts/DejaVuSerif-Bold.ttf'),18);small=ImageFont.truetype(str(root/'art/fonts/DejaVuSerif-Bold.ttf'),14)
samples=[('2-4 stairs / gold texture inside the original step edges','stair_walk',20),
         ('2-5 entrance / broad crimson formations and deep recesses','traversal',200),
         ('2-5 platforms / reused floating eyes and blue tears','traversal',600)]
def bases(case):return [Path(a.stairs_before)if case=='stair_walk'else Path(a.before),Path(a.after)]
canvas=Image.new('RGB',(1056,80+len(samples)*524),'#0b101b');d=ImageDraw.Draw(canvas)
d.text((16,14),'HOLY DIVER HD 0.8.0 — STAIRS AND CRIMSON CAVE',font=font,fill='#ecd4a5')
d.text((16,47),'Actual Mesen captures · left: 0.7.0 stairs / 0.7.1 cave · right: 0.8.0',font=small,fill='#b7c2d4')
for i,(label,case,n)in enumerate(samples):
 y=80+i*524;d.text((16,y+4),label,font=font,fill='#d5ba82')
 before,after=bases(case)
 for ext in ['ram','ppu','oam']:
  assert (before/case/f'dumps/{n:04}.{ext}').read_bytes()==(after/case/f'dumps/{n:04}.{ext}').read_bytes()
 for j,base in enumerate([before,after]):
  im=Image.open(base/case/f'frames/{n:04}.png').convert('RGB');assert im.size==(512,480);canvas.paste(im,(16+j*512,y+32))
canvas.save(out/'comparison.png')
clips=[('stair_walk',20,380,'2-4: both stair flights and landing'),
       ('traversal',60,200,'Jumping into the crimson cave'),
       ('traversal',350,660,'Crimson formations, platforms and blue tears'),
       ('combat',800,1280,'Reused bat and native combat'),
       ('freeze_thaw',340,500,'Native Blizzard cast and black flashes')]
proc=subprocess.Popen(['ffmpeg','-y','-loglevel','error','-f','rawvideo','-pix_fmt','rgb24','-s','1024x528','-r','30','-i','-',
 '-an','-c:v','libx264','-preset','medium','-crf','19','-pix_fmt','yuv420p','-movflags','+faststart',str(out/'review.mp4')],stdin=subprocess.PIPE)
for case,start,end,label in clips:
 for n in range(start,end+1,2):
  im=Image.new('RGB',(1024,528),'#0b101b');d=ImageDraw.Draw(im);d.text((16,5),label,font=small,fill='#ecd4a5')
  d.text((16,26),'Before: '+('0.7.0'if case=='stair_walk'else'0.7.1'),font=small,fill='#aebbd0');d.text((528,26),'Review: 0.8.0',font=small,fill='#aebbd0')
  for j,base in enumerate(bases(case)):im.paste(Image.open(base/case/f'frames/{n:04}.png').convert('RGB'),(j*512,48))
  proc.stdin.write(im.tobytes())
proc.stdin.close();assert proc.wait()==0
(out/'preview_sources.json').write_text(json.dumps(dict(stills=samples,clips=clips,stairs_baseline='0.7.0',cave_baseline='0.7.1',candidate='0.8.0',capture_stride=2,fps=30,retouched=False,audio=False),indent=2)+'\n')
print(out/'comparison.png');print(out/'review.mp4')
