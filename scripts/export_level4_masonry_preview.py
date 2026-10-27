"""Export paired real Mesen pictures, with labels outside the unchanged frames."""
from pathlib import Path
import argparse,json,subprocess
from PIL import Image,ImageDraw,ImageFont
p=argparse.ArgumentParser()
for k in ['before','after','out']:p.add_argument('--'+k,required=True)
a=p.parse_args();out=Path(a.out);out.mkdir(parents=True,exist_ok=True);r=Path(__file__).resolve().parents[1]
font=ImageFont.truetype(str(r/'art/fonts/DejaVuSerif-Bold.ttf'),18);small=ImageFont.truetype(str(r/'art/fonts/DejaVuSerif-Bold.ttf'),14)
def pair(n,label):
 im=Image.new('RGB',(1024,552),'#101522');d=ImageDraw.Draw(im);d.text((16,8),label,font=font,fill='#f2d997')
 for x,c,version in [(0,a.before,'Previous 0.16.0'),(512,a.after,'Revised 0.16.1')]:
  d.text((x+16,34),version,font=small,fill='white');im.paste(Image.open(Path(c)/'frames'/f'{n:06}.png').convert('RGB'),(x,56))
 d.text((16,536),'Actual MesenCE 2.2.1 playback | native 2x capture | silent comparison',font=small,fill='#c8d0e0');return im
segments=[('Distinct breakable blocks',range(300,540,4)),('Worn stone; outdoor columns preserved',range(800,1040,4)),('Carved indoor supports',range(4160,4400,4)),('Hanging column and upper platform',range(6400,6640,4)),('Indoor pillars from the reported scene',range(7440,7800,4))]
video=out/'Holy_Diver_HD_v0.16.1_Preview.mp4';cmd=['ffmpeg','-y','-loglevel','error','-f','rawvideo','-pix_fmt','rgb24','-s','1024x552','-r','15','-i','-','-an','-c:v','libx264','-crf','18','-pix_fmt','yuv420p','-movflags','+faststart',str(video)]
proc=subprocess.Popen(cmd,stdin=subprocess.PIPE);count=0
for label,ns in segments:
 for n in ns:proc.stdin.write(pair(n,label).tobytes());count+=1
proc.stdin.close();assert proc.wait()==0
sheet=Image.new('RGB',(1024,1104))
for j,(n,label)in enumerate([(300,'Solid stone and distinct breakable blocks'),(7680,'Carved indoor columns; background preserved')]):sheet.paste(pair(n,label),(0,552*j))
sheet.save(out/'Holy_Diver_HD_v0.16.1_Comparison.png')
report=dict(frames=count,fps=15,seconds=count/15,silent=True,game_images_unretouched=True,segments=[dict(label=l,first=list(ns)[0],last=list(ns)[-1],frames=len(ns))for l,ns in segments])
(r/'evidence/level4_masonry/preview.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
