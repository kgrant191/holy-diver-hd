"""Export actual paired Mesen captures without interpolation or pixel edits."""
from pathlib import Path
import argparse,json,subprocess
from PIL import Image,ImageDraw,ImageFont
p=argparse.ArgumentParser()
for k in ['before','after','out']:p.add_argument('--'+k,required=True)
a=p.parse_args();before,after,out=map(Path,[a.before,a.after,a.out]);out.parent.mkdir(parents=True,exist_ok=True)
r=Path(__file__).resolve().parents[1];font=ImageFont.truetype(str(r/'art/fonts/DejaVuSerif-Bold.ttf'),17)
clips=[('Final moss climb',500,900),('Upper platforms and exit',1180,1420),('Boss emerging from the ceiling',1720,1960),('Boss emerging from the floor',2480,2720),('Defeat and native flashes',3400,3600),('Living growths disappear',3860,4100),('Overdrive pickup and fade',4206,4380),('Overdrive acquired',4400,4490),('Golden Temple title card',4600,4720)]
proc=subprocess.Popen(['ffmpeg','-y','-f','rawvideo','-pixel_format','rgb24','-video_size','1040x544','-framerate','60','-i','-','-an','-c:v','libx264','-crf','18','-pix_fmt','yuv420p','-movflags','+faststart',str(out)],stdin=subprocess.PIPE,stderr=subprocess.DEVNULL)
count=0
for label,start,end in clips:
 for n in range(start,end,2):
  im=Image.new('RGB',(1040,544),(14,25,21));d=ImageDraw.Draw(im);d.text((8,6),'Before: approved 0.14.0',font=font,fill='white');d.text((528,6),'Poison Moss Land finale: 0.15.0',font=font,fill='white');d.text((8,33),label+' | actual Mesen playback, normal speed',font=font,fill=(200,220,204))
  for folder,x in [(before,8),(after,528)]:im.paste(Image.open(folder/'frames'/f'{n:06}.png').convert('RGB'),(x,64))
  for _ in range(2):proc.stdin.write(im.tobytes());count+=1
proc.stdin.close();assert proc.wait()==0
e=r/'evidence/level3_finale';e.mkdir(exist_ok=True)
report=dict(source='Actual paired Mesen captures; no pixel editing or motion interpolation',silent=True,fps=60,capture_stride=2,frames=count,seconds=count/60,clips=[dict(label=l,start=s,end=t)for l,s,t in clips])
(e/'preview.json').write_text(json.dumps(report,indent=2)+'\n')
gallery=Image.new('RGB',(1040,1080),(14,25,21));d=ImageDraw.Draw(gallery)
for i,(label,n)in enumerate([('Final moss climb',800),('Ceiling boss',1800),('Floor boss',2600),('Overdrive reward',4240)]):
 x,y=i%2*520,i//2*540;d.text((x+8,y+10),label+' | actual 0.15.0 capture',font=font,fill='white');gallery.paste(Image.open(after/'frames'/f'{n:06}.png'),(x+4,y+48))
gallery.save(e/'preview.png');print(out,count/60,'seconds')
