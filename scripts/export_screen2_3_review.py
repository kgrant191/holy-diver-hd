"""Export actual before/after tears and labeled enlargements of live captures."""
from pathlib import Path
import argparse,json,subprocess
from PIL import Image,ImageDraw,ImageFont
p=argparse.ArgumentParser()
for n in ['before','after','out']:p.add_argument('--'+n,required=True)
a=p.parse_args();root=Path(__file__).resolve().parents[1];out=Path(a.out);out.mkdir(parents=True,exist_ok=True)
font=ImageFont.truetype(str(root/'art/fonts/DejaVuSerif-Bold.ttf'),18)
small=ImageFont.truetype(str(root/'art/fonts/DejaVuSerif-Bold.ttf'),14)
report=json.loads((out/'verification.json').read_text())
closeups=dict(report['sprite_examples'])
# A later exact match keeps Randy's unrelated fireball out of this close-up.
closeups['02DD/mirrored']=dict(case='combat_respawn',frame=180,box=[280,202,296,218])
canvas=Image.new('RGB',(1056,800),'#0b101b');d=ImageDraw.Draw(canvas)
d.text((16,14),'HOLY DIVER HD 0.6.1 — BLUE TEARS',font=font,fill='#ecd4a5')
d.text((16,48),'Actual Mesen captures · previous 0.6.0 at left · revised 0.6.1 at right',font=small,fill='#b7c2d4')
case='combat_respawn';n=240
for i,base in enumerate([a.before,a.after]):canvas.paste(Image.open(Path(base)/case/f'frames/{n:04}.png').convert('RGB'),(16+i*512,80))
d.text((16,580),'Both tear shapes and mirrors — live crops enlarged 6×',font=font,fill='#ecd4a5')
for i,key in enumerate(['02DC/native','02DC/mirrored','02DD/native','02DD/mirrored']):
    e=closeups[key]
    crop=Image.open(Path(a.after)/e['case']/f'frames/{e["frame"]:04}.png').crop(e['box']).convert('RGB').resize((96,96),Image.Resampling.NEAREST)
    x=16+i*256;canvas.paste(crop,(x+70,624));d.text((x+20,738),key,font=small,fill='#b7c2d4')
canvas.save(out/'comparison.png')
clips=[(160,480),(680,1000)]
proc=subprocess.Popen(['ffmpeg','-y','-loglevel','error','-f','rawvideo','-pix_fmt','rgb24','-s','1024x528','-r','30','-i','-',
                       '-an','-c:v','libx264','-preset','medium','-crf','19','-pix_fmt','yuv420p','-movflags','+faststart',str(out/'review.mp4')],stdin=subprocess.PIPE)
for start,end in clips:
    for n in range(start,end+1,2):
        im=Image.new('RGB',(1024,528),'#0b101b');d=ImageDraw.Draw(im)
        d.text((16,5),'Eye projectiles: blue teardrops / native movement unchanged',font=small,fill='#ecd4a5')
        d.text((16,26),'Previous 0.6.0',font=small,fill='#aebbd0');d.text((528,26),'Revised 0.6.1',font=small,fill='#aebbd0')
        for j,base in enumerate([a.before,a.after]):im.paste(Image.open(Path(base)/case/f'frames/{n:04}.png').convert('RGB'),(j*512,48))
        proc.stdin.write(im.tobytes())
proc.stdin.close();assert proc.wait()==0
(out/'preview_sources.json').write_text(json.dumps(dict(case=case,still_frame=240,clips=clips,closeups=closeups,
    closeup_scale=6,capture_stride=2,fps=30,retouched=False,audio=False),indent=2)+'\n')
print(out/'comparison.png');print(out/'review.mp4')
