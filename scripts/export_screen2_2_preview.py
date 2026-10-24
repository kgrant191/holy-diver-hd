"""Export actual paired cave frames and a silent gameplay-speed review video."""
from pathlib import Path
import argparse,json,subprocess
from PIL import Image,ImageDraw,ImageFont
p=argparse.ArgumentParser()
for n in ['before','after','out']:p.add_argument('--'+n,required=True)
a=p.parse_args();root=Path(__file__).resolve().parents[1];out=Path(a.out);out.mkdir(parents=True,exist_ok=True)
font=ImageFont.truetype(str(root/'art/fonts/DejaVuSerif-Bold.ttf'),18)
small=ImageFont.truetype(str(root/'art/fonts/DejaVuSerif-Bold.ttf'),14)
report=json.loads((out/'verification.json').read_text())
bat=report['sprite_examples']['bat_open/native']
ghoul=report['sprite_examples']['ghoul_0/native']
samples=[('Cave entry / folded ceiling bats','entry_combat',20),
         ('Open-wing ceiling bat',bat['case'],bat['frame']),
         ('Reused approved ghoul artwork',ghoul['case'],ghoul['frame']),
         ('Hot lava fall','crossing',1400),('Blizzard ice fall','crossing',1600)]
canvas=Image.new('RGB',(1056,80+len(samples)*524),'#0b101b');d=ImageDraw.Draw(canvas)
d.text((16,14),'HOLY DIVER HD 0.5.0 — STAGE 2 / SCREEN 2',font=font,fill='#ecd4a5')
d.text((16,47),'Actual Mesen captures · approved 0.4.1 at left · review candidate at right',font=small,fill='#b7c2d4')
metadata=[]
for i,(label,case,n) in enumerate(samples):
    y=80+i*524;d.text((16,y+4),label,font=font,fill='#d5ba82')
    for j,base in enumerate([a.before,a.after]):
        src=Path(base)/case/f'frames/{n:04}.png';im=Image.open(src).convert('RGB')
        assert im.size==(512,480);canvas.paste(im,(16+j*512,y+32))
    metadata.append(dict(label=label,case=case,frame=n,retouched=False))
canvas.save(out/'comparison.png')
(out/'comparison_sources.json').write_text(json.dumps(metadata,indent=2)+'\n')
clips=[('entry_combat',2,400,'Cave entry and ceiling bats'),('entry_combat',500,900,'Shared ghoul artwork / both directions'),
       ('crossing',800,1100,'Blizzard ice / shared gold terrain'),('crossing',1320,1740,'Native hot-to-ice fall transition')]
video=out/'review.mp4'
proc=subprocess.Popen(['ffmpeg','-y','-loglevel','error','-f','rawvideo','-pix_fmt','rgb24','-s','512x512','-r','30','-i','-',
                       '-an','-c:v','libx264','-preset','medium','-crf','20','-pix_fmt','yuv420p','-movflags','+faststart',str(video)],stdin=subprocess.PIPE)
for case,start,end,label in clips:
    for n in range(start,end+1,2):
        frame=Image.new('RGB',(512,512),'#0b101b');draw=ImageDraw.Draw(frame)
        draw.text((10,8),label,font=small,fill='#ecd4a5')
        frame.paste(Image.open(Path(a.after)/case/f'frames/{n:04}.png').convert('RGB'),(0,32))
        proc.stdin.write(frame.tobytes())
proc.stdin.close();assert proc.wait()==0
(out/'video_sources.json').write_text(json.dumps(dict(clips=clips,captured_stride=2,fps=30,retouched=False,audio=False),indent=2)+'\n')
print(out/'comparison.png');print(video)
