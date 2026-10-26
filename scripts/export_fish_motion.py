"""Side-by-side video of consecutive unretouched emulator frames."""
from pathlib import Path
import argparse, subprocess, json
from PIL import Image,ImageDraw,ImageFont
p=argparse.ArgumentParser()
for name in ('before','after','out'):p.add_argument('--'+name,required=True)
a=p.parse_args();before=Path(a.before);after=Path(a.after);out=Path(a.out);out.parent.mkdir(parents=True,exist_ok=True)
font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',18)
small=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',14)
# Each source interval is shown first at normal speed and then in slow motion.
# Static crops preserve world motion; no frame blending or interpolation.
clips=[('Left-facing small fish',290,370,(112,88,368,280),1),('Left-facing small fish',290,370,(112,88,368,280),4),('Right-facing small fish',2470,2580,(256,104,512,296),1),('Right-facing small fish',2470,2580,(256,104,512,296),4)]
proc=subprocess.Popen(['ffmpeg','-y','-f','rawvideo','-pixel_format','rgb24','-video_size','1040x448','-framerate','60','-i','-','-an','-c:v','libx264','-crf','16','-pix_fmt','yuv420p','-movflags','+faststart',str(out)],stdin=subprocess.PIPE,stderr=subprocess.DEVNULL)
count=0
for label,start,end,box,repeats in clips:
 for n in range(start,end):
  im=Image.new('RGB',(1040,448),(18,22,29));d=ImageDraw.Draw(im)
  d.text((8,7),'Before: 0.12.0',font=font,fill='white');d.text((528,7),'After: 0.12.1',font=font,fill='white')
  d.text((8,34),f'{label} | '+('normal speed'if repeats==1 else'quarter speed')+' | 2x nearest-neighbor crop',font=small,fill=(200,205,215))
  for folder,x in ((before,8),(after,528)):
   f=Image.open(folder/'frames'/f'{n:06}.png').convert('RGB').crop(box).resize((512,384),Image.Resampling.NEAREST);im.paste(f,(x,64))
  for _ in range(repeats):proc.stdin.write(im.tobytes());count+=1
proc.stdin.close();assert proc.wait()==0
out.with_suffix('.json').write_text(json.dumps(dict(source='consecutive actual Mesen captures',fps=60,frames=count,duration_seconds=count/60,clips=clips,interpolation=False,silent=True),indent=2)+'\n')
print('Exported',out,count/60,'seconds')
