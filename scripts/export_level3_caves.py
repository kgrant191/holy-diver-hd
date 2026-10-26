"""Export actual paired Mesen captures; no tracking or motion interpolation."""
from pathlib import Path
import argparse,json,subprocess
from PIL import Image,ImageDraw,ImageFont
p=argparse.ArgumentParser()
for k in['before','after','fish-before','fish-after','out']:p.add_argument('--'+k,required=True)
a=p.parse_args();b,c,fb,fc,out=map(Path,[a.before,a.after,a.fish_before,a.fish_after,a.out]);out.parent.mkdir(parents=True,exist_ok=True)
font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',18);small=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',14)
clips=[('Two fish, opposite hover phases',fb,fc,1960,2030,1,1,(0,48,256,288)),('Same frames at quarter speed',fb,fc,1960,2030,1,4,(0,48,256,288)),('Green creature and frozen lava',b,c,2700,3000,2,2,None),('Vertical cave and blade rings',b,c,4460,4820,2,2,None),('Stone platforms and native edges',b,c,5480,5720,2,2,None),('Frozen pools and thawing',b,c,6140,6500,2,2,None),('Beginning of the bat descent',b,c,6870,6980,2,2,None)]
proc=subprocess.Popen(['ffmpeg','-y','-f','rawvideo','-pixel_format','rgb24','-video_size','1040x544','-framerate','60','-i','-','-an','-c:v','libx264','-crf','17','-pix_fmt','yuv420p','-movflags','+faststart',str(out)],stdin=subprocess.PIPE,stderr=subprocess.DEVNULL)
count=0
for label,left,right,start,end,step,repeats,box in clips:
 for n in range(start,end,step):
  im=Image.new('RGB',(1040,544),(18,22,29));d=ImageDraw.Draw(im);d.text((8,7),'Before: 0.12.2',font=font,fill='white');d.text((528,7),'Review: 0.13.0',font=font,fill='white');d.text((8,35),label+(' | fixed crop, 2x nearest-neighbor'if box else' | normal speed, actual captures'),font=small,fill=(205,210,220))
  for folder,x in[(left,8),(right,528)]:
   f=Image.open(folder/'frames'/f'{n:06}.png').convert('RGB')
   if box:f=f.crop(box).resize((512,480),Image.Resampling.NEAREST)
   im.paste(f,(x,64))
  for _ in range(repeats):proc.stdin.write(im.tobytes());count+=1
proc.stdin.close();assert proc.wait()==0
out.with_suffix('.json').write_text(json.dumps(dict(source='Actual Mesen captures, fixed crops only, no interpolation or tracking',silent=True,fps=60,frames=count,seconds=count/60,clips=[dict(label=v[0],start=v[3],end=v[4],stride=v[5],repeats=v[6],crop=v[7])for v in clips]),indent=2)+'\n')
print(out,count/60,'seconds')
