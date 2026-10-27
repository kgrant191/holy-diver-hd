"""Export unretouched paired Mesen pictures with labels outside the game image."""
from pathlib import Path
import argparse,json,subprocess
from PIL import Image,ImageDraw,ImageFont
p=argparse.ArgumentParser()
for k in ['before','after','spell-before','spell-after','out']:p.add_argument('--'+k,required=True)
a=p.parse_args();out=Path(a.out);out.mkdir(parents=True,exist_ok=True)
r=Path(__file__).resolve().parents[1];font=ImageFont.truetype(str(r/'art/fonts/DejaVuSerif-Bold.ttf'),18)
small=ImageFont.truetype(str(r/'art/fonts/DejaVuSerif-Bold.ttf'),14)
def pair(before,after,n,label):
 im=Image.new('RGB',(1024,552),'#101522');d=ImageDraw.Draw(im)
 d.text((16,8),label,font=font,fill='#f2d997')
 for x,c,version in [(0,before,'Approved 0.15.0'),(512,after,'Golden Temple 0.16.0')]:
  d.text((x+16,34),version,font=small,fill='white');im.paste(Image.open(Path(c)/'frames'/f'{n:06}.png').convert('RGB'),(x,56))
 d.text((16,536),'Actual MesenCE 2.2.1 playback | native 2x capture | silent comparison',font=small,fill='#c8d0e0')
 return im
segments=[('Overdrive menu',a.before,a.after,[160]*30),('Outdoor temple approach',a.before,a.after,range(300,540,4)),('Entering the temple',a.before,a.after,range(3900,4260,4)),('Enclosed golden hall',a.before,a.after,range(5100,5340,4)),('Overdrive: orbiting energy orbs',a.spell_before,a.spell_after,range(236,476,4)),('Second recorded interior',a.before,a.after,range(7460,7700,4))]
video=out/'Holy_Diver_HD_v0.16.0_Preview.mp4'
cmd=['ffmpeg','-y','-loglevel','error','-f','rawvideo','-pix_fmt','rgb24','-s','1024x552','-r','15','-i','-','-an','-c:v','libx264','-crf','18','-pix_fmt','yuv420p','-movflags','+faststart',str(video)]
proc=subprocess.Popen(cmd,stdin=subprocess.PIPE);count=0
for label,b,c,frames in segments:
 for n in frames:proc.stdin.write(pair(b,c,n,label).tobytes());count+=1
proc.stdin.close();assert proc.wait()==0
sheet=Image.new('RGB',(1024,1656))
for j,(n,label)in enumerate([(400,'Outdoor temple approach'),(4200,'Inside the Golden Temple'),(8000,'Second recorded interior')]):sheet.paste(pair(a.before,a.after,n,label),(0,552*j))
sheet.save(out/'Holy_Diver_HD_v0.16.0_Comparison.png')
report=dict(frames=count,fps=15,seconds=count/15,silent=True,game_images_unretouched=True,segments=[dict(label=l,first=list(ns)[0],last=list(ns)[-1],frames=len(ns))for l,b,c,ns in segments])
(r/'evidence/level4/preview.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
