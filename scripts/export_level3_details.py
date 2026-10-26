"""Export labeled comparisons and a silent video from untouched native captures."""
from pathlib import Path
import argparse,json,subprocess
from PIL import Image,ImageDraw,ImageFont
p=argparse.ArgumentParser()
for k in ['before','after','out']:p.add_argument('--'+k,required=True)
a=p.parse_args();b,c,out=Path(a.before),Path(a.after),Path(a.out);out.mkdir(exist_ok=True,parents=True)
font='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf';title=ImageFont.truetype(font,24);small=ImageFont.truetype(font,17)
rows=[('Round enemy shot',400,(150,100,370,320)),('Solid oak branches',1696,(148,0,512,392)),('Boot collectible',2256,(130,360,250,480))]
sheet=Image.new('RGB',(1064,1476),(19,22,28));d=ImageDraw.Draw(sheet)
d.text((20,14),'Holy Diver HD 0.11.2 - actual Mesen captures',font=title,fill='white')
d.text((20,51),'Before: 0.11.1',font=small,fill=(175,182,194));d.text((552,51),'After: 0.11.2',font=small,fill=(175,182,194))
y=86
for label,n,box in rows:
 d.text((20,y),label,font=title,fill=(225,193,130));y+=38
 for path,x in [(b,20),(c,552)]:
  im=Image.open(path/'frames'/f'{n:06}.png').convert('RGB').crop(box)
  scale=min(492/im.width,392/im.height);im=im.resize((round(im.width*scale),round(im.height*scale)),Image.Resampling.NEAREST)
  sheet.paste(im,(x,y))
 y+=420
d.text((20,1445),'Cropped and enlarged without retouching. Gameplay and audio unchanged.',font=small,fill=(175,182,194))
sheet.save(out/'Holy_Diver_HD_v0.11.2_Comparison.png')
clips=[(360,552),(1460,1640),(1660,1840),(2232,2360)]
video=out/'Holy_Diver_HD_v0.11.2_Preview.mp4'
proc=subprocess.Popen(['ffmpeg','-y','-f','rawvideo','-pixel_format','rgb24','-video_size','512x480','-framerate','15','-i','-','-an','-c:v','libx264','-crf','18','-pix_fmt','yuv420p','-movflags','+faststart',str(video)],stdin=subprocess.PIPE,stderr=subprocess.DEVNULL)
count=0
for start,end in clips:
 for n in range(start,end,4):
  im=Image.open(c/'frames'/f'{n:06}.png').convert('RGB');proc.stdin.write(im.tobytes());count+=1
proc.stdin.close();assert proc.wait()==0
(out/'preview.json').write_text(json.dumps(dict(source='unretouched actual Mesen screenshots',comparison_frames=[x[1]for x in rows],video_clips=clips,fps=15,video_frames=count,duration_seconds=count/15,silent=True,speed='original gameplay speed'),indent=2)+'\n')
print('Exported comparison and',count/15,'second silent actual-gameplay preview.')
