"""Export unretouched big-fish hover before/after captures."""
from pathlib import Path
import argparse,subprocess,json
from PIL import Image,ImageDraw,ImageFont
p=argparse.ArgumentParser()
for k in ('before','after','out'):p.add_argument('--'+k,required=True)
a=p.parse_args();b,c=Path(a.before),Path(a.after);out=Path(a.out);out.parent.mkdir(parents=True,exist_ok=True)
font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',18);small=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',14)
# Static viewport crops: the fish is not tracked or stabilized in the video.
clips=[('Left-facing hover',300,450,(184,64,440,256),1),('Left-facing hover',300,450,(184,64,440,256),4),('Right-facing hover',780,840,(0,64,256,256),1),('Right-facing hover',780,840,(0,64,256,256),4),('Dive and turn: original movement',470,620,(0,48,256,240),1)]
proc=subprocess.Popen(['ffmpeg','-y','-f','rawvideo','-pixel_format','rgb24','-video_size','1040x448','-framerate','60','-i','-','-an','-c:v','libx264','-crf','16','-pix_fmt','yuv420p','-movflags','+faststart',str(out)],stdin=subprocess.PIPE,stderr=subprocess.DEVNULL)
count=0
for label,start,end,box,repeats in clips:
 for n in range(start,end):
  im=Image.new('RGB',(1040,448),(18,22,29));d=ImageDraw.Draw(im)
  d.text((8,7),'Before: 0.12.1',font=font,fill='white');d.text((528,7),'After: 0.12.2',font=font,fill='white')
  d.text((8,34),label+' | '+('normal speed'if repeats==1 else'quarter speed')+' | 2x nearest-neighbor crop',font=small,fill=(200,205,215))
  for folder,x in ((b,8),(c,528)):
   f=Image.open(folder/'frames'/f'{n:06}.png').convert('RGB').crop(box).resize((512,384),Image.Resampling.NEAREST);im.paste(f,(x,64))
  for _ in range(repeats):proc.stdin.write(im.tobytes());count+=1
proc.stdin.close();assert proc.wait()==0
out.with_suffix('.json').write_text(json.dumps(dict(source='consecutive actual Mesen captures; static crop; no tracking or postprocessing',fps=60,frames=count,duration_seconds=count/60,clips=clips,interpolation=False,silent=True),indent=2)+'\n');print('Exported',out,count/60,'seconds')
