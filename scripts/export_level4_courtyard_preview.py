"""Export a compact before/after cut from unretouched actual Mesen frames."""
from pathlib import Path
import argparse,json,subprocess
from PIL import Image,ImageDraw,ImageFont
p=argparse.ArgumentParser()
for k in ['before','after','out']:p.add_argument('--'+k,required=True)
a=p.parse_args();r=Path(__file__).resolve().parents[1];out=Path(a.out);out.mkdir(parents=True,exist_ok=True)
font=ImageFont.truetype(str(r/'art/fonts/DejaVuSerif-Bold.ttf'),17)
small=ImageFont.truetype(str(r/'art/fonts/DejaVuSerif-Bold.ttf'),13)
def pair(n,title):
 im=Image.new('RGB',(1024,552),'#101522');d=ImageDraw.Draw(im)
 d.text((16,8),title,font=font,fill='#f2d997')
 for x,folder,label in [(0,a.before,'Previous 0.16.3'),(512,a.after,'Updated 0.17.0')]:
  d.text((x+16,32),label,font=small,fill='white')
  im.paste(Image.open(Path(folder)/'frames'/f'{n:06}.png').convert('RGB'),(x,56))
 d.text((16,536),'Actual MesenCE 2.2.1 | supplied recording | normal-speed, silent preview',font=small,fill='#c8d0e0')
 return im
segments=[(400,700,'Next indoor hall'),(2200,2598,'Stairs and wings pickup'),(2760,3140,'Outdoor courtyard and fire chain'),(3400,3700,'Courtyard columns and fire-chain movement'),(3780,4040,'Temple entrance and return indoors')]
video=out/'Holy_Diver_HD_v0.17.0_Preview.mp4'
proc=subprocess.Popen(['ffmpeg','-y','-loglevel','error','-f','rawvideo','-pix_fmt','rgb24','-s','1024x552','-r','30','-i','-','-an','-c:v','libx264','-crf','18','-pix_fmt','yuv420p','-movflags','+faststart',str(video)],stdin=subprocess.PIPE)
count=0
for start,end,title in segments:
 for n in range(start,end+1,2):proc.stdin.write(pair(n,title).tobytes());count+=1
for _ in range(60):proc.stdin.write(pair(4020,'Return indoors — recorded temple re-entry').tobytes());count+=1
proc.stdin.close();assert proc.wait()==0
for n,title in [(500,'Next indoor hall'),(2400,'Stairs and wings pickup'),(3500,'Outdoor courtyard'),(3880,'Temple entrance'),(4020,'Return indoors')]:pair(n,title).save(r/f'evidence/level4_courtyard/comparison_{n}.png')
report=dict(frames=count,fps=30,seconds=count/30,playback_speed=1,game_images_unretouched=True,source_segments=segments,final_still_frame=4020,final_still_seconds=2,silent=True)
(r/'evidence/level4_courtyard/preview.json').write_text(json.dumps(report,indent=2)+'\n');print(report)
