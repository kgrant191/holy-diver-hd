"""Export unretouched game captures with captions outside the game image."""
from pathlib import Path
import argparse,json,subprocess
from PIL import Image,ImageDraw,ImageFont
p=argparse.ArgumentParser();p.add_argument('--capture',required=True);p.add_argument('--out',required=True)
a=p.parse_args();r=Path(__file__).resolve().parents[1];out=Path(a.out);out.mkdir(parents=True,exist_ok=True)
font=ImageFont.truetype(str(r/'art/fonts/DejaVuSerif-Bold.ttf'),15)
small=ImageFont.truetype(str(r/'art/fonts/DejaVuSerif-Bold.ttf'),12)
def frame(n,label):
 im=Image.new('RGB',(512,536),'#101522');d=ImageDraw.Draw(im)
 d.text((12,7),'Holy Diver HD 0.16.2 | '+label,font=font,fill='#f2d997')
 im.paste(Image.open(Path(a.capture)/'frames'/f'{n:06}.png').convert('RGB'),(0,32))
 d.text((12,516),'Actual MesenCE 2.2.1 playback | silent | 2x capture',font=small,fill='#c8d0e0')
 return im
segments=[('HD recovery drops',range(480,720,4)),('Temple entry',range(3780,4440,4))]
video=out/'Holy_Diver_HD_v0.16.2_Preview.mp4'
proc=subprocess.Popen(['ffmpeg','-y','-loglevel','error','-f','rawvideo','-pix_fmt','rgb24','-s','512x536','-r','15','-i','-','-an','-c:v','libx264','-crf','18','-pix_fmt','yuv420p','-movflags','+faststart',str(video)],stdin=subprocess.PIPE)
count=0
for label,ns in segments:
 for n in ns:proc.stdin.write(frame(n,label).tobytes());count+=1
proc.stdin.close();assert proc.wait()==0
sheet=Image.new('RGB',(1024,536))
sheet.paste(frame(600,'HD recovery drops'),(0,0));sheet.paste(frame(4060,'Inside the temple'),(512,0))
sheet.save(r/'evidence/level4_repairs/preview.png')
report=dict(frames=count,fps=15,seconds=count/15,unretouched_game_images=True,silent=True,
 segments=[dict(label=l,first=ns[0],last=ns[-1])for l,ns in segments])
(r/'evidence/level4_repairs/preview.json').write_text(json.dumps(report,indent=2)+'\n');print(report)
