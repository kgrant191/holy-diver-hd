"""Build an unretouched, normal-speed before/after preview from Mesen frames."""
from pathlib import Path
import argparse, json, subprocess
from PIL import Image, ImageDraw, ImageFont
p=argparse.ArgumentParser()
for k in ['before','after','out']:p.add_argument('--'+k,required=True)
a=p.parse_args();r=Path(__file__).resolve().parents[1];out=Path(a.out);out.mkdir(parents=True,exist_ok=True)
evidence=r/'evidence/level4_finale'
font=ImageFont.truetype(str(r/'art/fonts/DejaVuSerif-Bold.ttf'),17)
small=ImageFont.truetype(str(r/'art/fonts/DejaVuSerif-Bold.ttf'),13)
def pair(n,title):
 im=Image.new('RGB',(1024,552),'#101522');d=ImageDraw.Draw(im)
 d.text((16,8),title,font=font,fill='#f2d997')
 for x,folder,label in [(0,a.before,'Previous 0.19.1'),(512,a.after,'Updated 0.20.0')]:
  d.text((x+16,32),label,font=small,fill='white')
  im.paste(Image.open(Path(folder)/'frames'/f'{n:06}.png').convert('RGB'),(x,56))
 d.text((16,536),'Actual MesenCE 2.2.1 | supplied movie | normal-speed, silent preview',font=small,fill='#c8d0e0')
 return im
segments=[(420,660,'First indoor hall — returning sentinel and new rings'),(4500,4740,'Second indoor hall — finished scenery and stonework'),(6250,7090,'Boss encounter — rotating eyes, native hit flashes and moving platforms')]
video=out/'Holy_Diver_HD_v0.20.0_Preview.mp4'
proc=subprocess.Popen(['ffmpeg','-y','-loglevel','error','-f','rawvideo','-pix_fmt','rgb24','-s','1024x552','-r','30','-i','-','-an','-c:v','libx264','-crf','18','-pix_fmt','yuv420p','-movflags','+faststart',str(video)],stdin=subprocess.PIPE)
count=0
for start,end,title in segments:
 for n in range(start,end+1,2):proc.stdin.write(pair(n,title).tobytes());count+=1
for _ in range(60):proc.stdin.write(pair(6500,'Golden Temple boss — defeat sequence not shown in this recording').tobytes());count+=1
proc.stdin.close();assert proc.wait()==0
for n,title in [(500,'First indoor hall'),(4800,'Second indoor hall'),(6500,'Rotating eye tower'),(6300,'Native white-hit palette')]:pair(n,title).save(evidence/f'comparison_{n}.png')
report=dict(frames=count,fps=30,seconds=count/30,playback_speed=1,game_images_unretouched=True,source_segments=segments,final_still_frame=6500,final_still_seconds=2,silent=True)
(evidence/'preview.json').write_text(json.dumps(report,indent=2)+'\n');print(report)
