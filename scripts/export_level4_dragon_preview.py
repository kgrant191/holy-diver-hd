"""Labeled before/after preview from unretouched stock-Mesen captures."""
from pathlib import Path
import argparse,json,subprocess
from PIL import Image,ImageDraw,ImageFont
p=argparse.ArgumentParser();p.add_argument('--captures',required=True);p.add_argument('--out',required=True);a=p.parse_args();r=Path(__file__).resolve().parents[1];base=Path(a.captures);out=Path(a.out);out.mkdir(parents=True,exist_ok=True)
font=ImageFont.truetype(str(r/'art/fonts/DejaVuSerif-Bold.ttf'),17);small=ImageFont.truetype(str(r/'art/fonts/DejaVuSerif-Bold.ttf'),13)
pairs={'flight':('dragon_flight_before','dragon_flight_after'),'hall':('staff_0180_final','dragon_hall_after'),'opening':('dragon_opening_before','dragon_opening_after'),'courtyard':('staff_0180_regression','dragon_courtyard_after')}
def pair(case,n,title):
 im=Image.new('RGB',(1024,552),'#101522');d=ImageDraw.Draw(im);d.text((16,8),title,font=font,fill='#f2d997')
 for x,folder,label in [(0,pairs[case][0],'Previous 0.18.0'),(512,pairs[case][1],'Updated 0.19.0')]:
  d.text((x+16,32),label,font=small,fill='white');im.paste(Image.open(base/folder/'frames'/f'{n:06}.png').convert('RGB'),(x,56))
 d.text((16,536),'Actual MesenCE 2.2.1 | unchanged saves / controller inputs | normal-speed, silent preview',font=small,fill='#c8d0e0');return im
segments=[('flight',2,360,2,'Dragon pickup, transformation and fire breath'),('flight',460,800,2,'Raised / folded wings, both directions and native damage blinking'),('hall',900,1200,2,'Brighter staff and small recovery drops'),('hall',1540,1640,2,'The same staff in the Start menu'),('opening',520,760,4,'Decorative columns removed — background revealed'),('courtyard',2620,2720,2,'Earlier outdoor courtyard — physical stonework retained')]
video=out/'Holy_Diver_HD_v0.19.0_Preview.mp4';proc=subprocess.Popen(['ffmpeg','-y','-loglevel','error','-f','rawvideo','-pix_fmt','rgb24','-s','1024x552','-r','30','-i','-','-an','-c:v','libx264','-crf','18','-pix_fmt','yuv420p','-movflags','+faststart',str(video)],stdin=subprocess.PIPE);count=0
for case,start,end,stride,title in segments:
 for n in range(start,end+1,stride):
  frame=pair(case,n,title).tobytes()
  for _ in range(stride//2):proc.stdin.write(frame);count+=1
for _ in range(60):proc.stdin.write(pair('flight',650,'Golden Temple — updated dragon and clear scenery').tobytes());count+=1
proc.stdin.close();assert proc.wait()==0
for case,n,title in [('flight',20,'Dragon pickup and clear foreground'),('flight',300,'Dragon flying and firing'),('hall',1000,'Brighter staff pickup'),('opening',560,'Outdoor approach without decorative foreground columns'),('courtyard',2660,'Outdoor courtyard without decorative foreground columns')]:pair(case,n,title).save(r/f'evidence/level4_dragon/comparison_{case}.png')
(r/'evidence/level4_dragon/preview.json').write_text(json.dumps(dict(frames=count,fps=30,seconds=count/30,playback_speed=1,game_images_unretouched=True,segments=segments,final_still_seconds=2,silent=True),indent=2)+'\n');print(video,count/30)
