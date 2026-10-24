"""Create unretouched 0.5.0/0.5.1 cave comparisons and moving-fall evidence."""
from pathlib import Path
import argparse,json,subprocess
from PIL import Image,ImageDraw,ImageFont
p=argparse.ArgumentParser()
for n in ['before','after','out']:p.add_argument('--'+n,required=True)
a=p.parse_args();root=Path(__file__).resolve().parents[1];out=Path(a.out);out.mkdir(parents=True,exist_ok=True)
font=ImageFont.truetype(str(root/'art/fonts/DejaVuSerif-Bold.ttf'),18)
small=ImageFont.truetype(str(root/'art/fonts/DejaVuSerif-Bold.ttf'),14)
samples=[('Removed red decoration / continuous cave backdrop','entry_combat',20),
         ('Hot fall / downward flow shown in the video','crossing',2300),
         ('Blizzard ice / stationary frozen fall','crossing',1700)]
canvas=Image.new('RGB',(1056,80+len(samples)*524),'#0b101b');d=ImageDraw.Draw(canvas)
d.text((16,14),'HOLY DIVER HD 0.5.1 — CAVE REVIEW FIXES',font=font,fill='#ecd4a5')
d.text((16,47),'Actual Mesen captures · previous 0.5.0 at left · revised 0.5.1 at right',font=small,fill='#b7c2d4')
for i,(label,case,n) in enumerate(samples):
    y=80+i*524;d.text((16,y+4),label,font=font,fill='#d5ba82')
    for j,base in enumerate([a.before,a.after]):
        im=Image.open(Path(base)/case/f'frames/{n:04}.png').convert('RGB')
        assert im.size==(512,480);canvas.paste(im,(16+j*512,y+32))
canvas.save(out/'comparison.png')
clips=[('entry_combat',2,180,'Cave backdrop revealed'),('crossing',2240,2480,'Hot fall flows downward'),
       ('crossing',1600,1840,'Blizzard ice stays still'),('crossing',2080,2240,'Native thaw restores the hot flow')]
proc=subprocess.Popen(['ffmpeg','-y','-loglevel','error','-f','rawvideo','-pix_fmt','rgb24','-s','1024x528','-r','30','-i','-',
                       '-an','-c:v','libx264','-preset','medium','-crf','19','-pix_fmt','yuv420p','-movflags','+faststart',str(out/'review.mp4')],stdin=subprocess.PIPE)
for case,start,end,label in clips:
    for n in range(start,end+1,2):
        im=Image.new('RGB',(1024,528),'#0b101b');d=ImageDraw.Draw(im)
        d.text((16,5),label,font=small,fill='#ecd4a5')
        d.text((16,26),'Previous 0.5.0',font=small,fill='#aebbd0');d.text((528,26),'Revised 0.5.1',font=small,fill='#aebbd0')
        for j,base in enumerate([a.before,a.after]):im.paste(Image.open(Path(base)/case/f'frames/{n:04}.png').convert('RGB'),(j*512,48))
        proc.stdin.write(im.tobytes())
proc.stdin.close();assert proc.wait()==0
(out/'preview_sources.json').write_text(json.dumps(dict(stills=samples,clips=clips,capture_stride=2,fps=30,retouched=False,audio=False),indent=2)+'\n')
print(out/'comparison.png');print(out/'review.mp4')
