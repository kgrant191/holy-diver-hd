"""Export actual emulator captures; no painted or reconstructed acceptance frames."""
from pathlib import Path
import argparse,json,subprocess
from PIL import Image,ImageDraw,ImageFont
p=argparse.ArgumentParser();p.add_argument('--captures',required=True);p.add_argument('--out',required=True);a=p.parse_args()
base,out=Path(a.captures),Path(a.out);out.mkdir(exist_ok=True,parents=True)
font='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf';title=ImageFont.truetype(font,23);small=ImageFont.truetype(font,16)
def frame(case,n):return Image.open(base/case/'frames'/f'{n:06}.png').convert('RGB')
rows=[('Start / pause menu: the same boot as the collectible','before','final',2,(48,100,200,196),2),('Lava corridor and fish; Breaker charge','before','final',342,(0,0,512,480),1),('Carved steps and upward Breaker release','breaker_before','breaker_after',3936,(0,0,512,480),1)]
sheet=Image.new('RGB',(1064,1448),(19,22,28));d=ImageDraw.Draw(sheet)
d.text((16,12),'Holy Diver HD 0.12.0 - actual Mesen captures',font=title,fill='white')
d.text((16,48),'Before: approved 0.11.2',font=small,fill=(180,187,201));d.text((544,48),'After: 0.12.0 review build',font=small,fill=(180,187,201))
y=80
for label,b,c,n,box,scale in rows:
 d.text((16,y),label,font=title,fill=(229,199,137));y+=36
 for case,x in [(b,16),(c,544)]:
  im=frame(case,n).crop(box)
  if scale!=1:im=im.resize((im.width*scale,im.height*scale),Image.Resampling.NEAREST)
  sheet.paste(im,(x,y))
 y+=im.height+24
d.text((16,1420),'Unretouched captures. Crops enlarged with nearest-neighbor scaling.',font=small,fill=(180,187,201))
sheet.save(out/'Holy_Diver_HD_v0.12.0_Comparison.png')
clips=[('Menu boot','final',2,62,2,'normal'),('Fish, lava and Breaker charge','final',300,540,2,'normal'),('Across the lava corridor','final',1760,2000,2,'normal'),('Carved stairs','final',2940,3120,2,'normal'),('Breaker: left cast','breaker_after',3720,3792,1,'half speed'),('Breaker: upward cast','breaker_after',3918,3990,1,'half speed'),('Blizzard: frozen lava','blizzard_final',360,480,2,'normal')]
proc=subprocess.Popen(['ffmpeg','-y','-f','rawvideo','-pixel_format','rgb24','-video_size','512x524','-framerate','30','-i','-','-an','-c:v','libx264','-crf','18','-pix_fmt','yuv420p','-movflags','+faststart',str(out/'Holy_Diver_HD_v0.12.0_Preview.mp4')],stdin=subprocess.PIPE,stderr=subprocess.DEVNULL)
count=0
for label,case,start,end,step,speed in clips:
 for n in range(start,end,step):
  im=Image.new('RGB',(512,524),(19,22,28));dd=ImageDraw.Draw(im);dd.text((12,6),label,font=small,fill='white');dd.text((12,25),'0.12.0 | '+speed,font=ImageFont.truetype(font,12),fill=(180,187,201));im.paste(frame(case,n),(0,44));proc.stdin.write(im.tobytes());count+=1
proc.stdin.close();assert proc.wait()==0
(out/'preview.json').write_text(json.dumps(dict(source='actual unretouched Mesen captures',comparison=[dict(label=x[0],frame=x[3],crop=x[4],integer_scale=x[5])for x in rows],video_clips=clips,fps=30,video_frames=count,duration_seconds=count/30,silent=True),indent=2)+'\n')
print(f'Exported comparison and {count/30:.2f}-second preview.')
