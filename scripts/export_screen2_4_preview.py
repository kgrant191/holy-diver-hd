"""Export unretouched paired Mesen captures and a gameplay-speed review video."""
from pathlib import Path
import argparse
import json
import subprocess
from PIL import Image,ImageDraw,ImageFont

p=argparse.ArgumentParser()
for n in ['before','after','out']:
    p.add_argument('--'+n,required=True)
a=p.parse_args()
root=Path(__file__).resolve().parents[1]
out=Path(a.out)
out.mkdir(parents=True,exist_ok=True)
font=ImageFont.truetype(str(root/'art/fonts/DejaVuSerif-Bold.ttf'),18)
small=ImageFont.truetype(str(root/'art/fonts/DejaVuSerif-Bold.ttf'),14)
samples=[('Cave entrance / reused winged demon and downward arrow','combat_respawn',200),
         ('Reused faceless pulsing rock and gold terrain','combat_respawn',440),
         ('Hot lava falls / approved downward flow','hot_falls',1600),
         ('Blizzard / approved frozen falls and pool','traversal',1600)]
canvas=Image.new('RGB',(1056,80+len(samples)*524),'#0b101b')
d=ImageDraw.Draw(canvas)
d.text((16,14),'HOLY DIVER HD 0.7.0 — STAGE 2 / SCREEN 4',font=font,fill='#ecd4a5')
d.text((16,47),'Actual Mesen captures · approved 0.6.1 at left · review 0.7.0 at right',font=small,fill='#b7c2d4')
for i,(label,case,n) in enumerate(samples):
    y=80+i*524
    d.text((16,y+4),label,font=font,fill='#d5ba82')
    for j,base in enumerate([a.before,a.after]):
        im=Image.open(Path(base)/case/f'frames/{n:04}.png').convert('RGB')
        assert im.size==(512,480)
        canvas.paste(im,(16+j*512,y+32))
canvas.save(out/'comparison.png')
clips=[('combat_respawn',40,440,'Shared demons, arrows and pulsing rocks'),
       ('traversal',700,1240,'Gold ceiling and platforms / scrolling cave'),
       ('hot_falls',1400,1800,'Downward lava flow'),
       ('traversal',1400,1840,'Frozen falls / native Blizzard behavior')]
proc=subprocess.Popen(['ffmpeg','-y','-loglevel','error','-f','rawvideo','-pix_fmt','rgb24','-s','1024x528','-r','30','-i','-',
                       '-an','-c:v','libx264','-preset','medium','-crf','19','-pix_fmt','yuv420p','-movflags','+faststart',str(out/'review.mp4')],stdin=subprocess.PIPE)
for case,start,end,label in clips:
    for n in range(start,end+1,2):
        im=Image.new('RGB',(1024,528),'#0b101b')
        d=ImageDraw.Draw(im)
        d.text((16,5),label,font=small,fill='#ecd4a5')
        d.text((16,26),'Approved 0.6.1',font=small,fill='#aebbd0')
        d.text((528,26),'Review 0.7.0',font=small,fill='#aebbd0')
        for j,base in enumerate([a.before,a.after]):
            im.paste(Image.open(Path(base)/case/f'frames/{n:04}.png').convert('RGB'),(j*512,48))
        proc.stdin.write(im.tobytes())
proc.stdin.close()
assert proc.wait()==0
(out/'preview_sources.json').write_text(json.dumps(dict(stills=samples,clips=clips,capture_stride=2,fps=30,retouched=False,audio=False),indent=2)+'\n')
print(out/'comparison.png')
print(out/'review.mp4')
