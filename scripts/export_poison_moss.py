"""Show the green retheme using actual paired Mesen playback frames."""
from pathlib import Path
import argparse,json,subprocess
from PIL import Image,ImageDraw,ImageFont
p=argparse.ArgumentParser()
for k in ['opening-before','opening-after','next-before','next-after','out']:p.add_argument('--'+k,required=True)
a=p.parse_args();ob,oa,nb,na,out=map(Path,[a.opening_before,a.opening_after,a.next_before,a.next_after,a.out]);out.parent.mkdir(parents=True,exist_ok=True)
font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',18);small=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',14)
clips=[('Forest approach',ob,oa,320,560,4),('Oak and moss',ob,oa,1080,1320,4),('Overgrown shaft',ob,oa,2320,2560,4),('First fish corridor',ob,oa,5800,6040,4),('Moss ruins across the scrolling wrap',nb,na,1260,1500,2),('Blade-ring climb',nb,na,4460,4700,2),('Mossy carved platforms',nb,na,5460,5700,2),('Beginning of the bat descent',nb,na,6858,6978,2)]
proc=subprocess.Popen(['ffmpeg','-y','-f','rawvideo','-pixel_format','rgb24','-video_size','1040x544','-framerate','60','-i','-','-an','-c:v','libx264','-crf','18','-pix_fmt','yuv420p','-movflags','+faststart',str(out)],stdin=subprocess.PIPE,stderr=subprocess.DEVNULL)
count=0
for label,left,right,start,end,step in clips:
 for n in range(start,end,step):
  im=Image.new('RGB',(1040,544),(14,25,21));d=ImageDraw.Draw(im);d.text((8,7),'Before: 0.13.0',font=font,fill='white');d.text((528,7),'Poison Moss Land: 0.14.0 review',font=font,fill='white');d.text((8,35),label+' | actual Mesen captures, normal speed',font=small,fill=(200,220,204))
  for folder,x in [(left,8),(right,528)]:im.paste(Image.open(folder/'frames'/f'{n:06}.png').convert('RGB'),(x,64))
  for _ in range(step):proc.stdin.write(im.tobytes());count+=1
proc.stdin.close();assert proc.wait()==0
out.with_suffix('.json').write_text(json.dumps(dict(source='Actual paired Mesen captures, no pixel editing or motion interpolation',silent=True,fps=60,frames=count,seconds=count/60,clips=[dict(label=v[0],start=v[3],end=v[4],capture_stride=v[5])for v in clips]),indent=2)+'\n')
gallery=Image.new('RGB',(1040,1100),(14,25,21));d=ImageDraw.Draw(gallery)
for j,(label,folder,n)in enumerate([('Forest approach',oa,400),('Mossy shaft',oa,2400),('Lava corridor',na,2800),('Blade-ring climb',na,4560)]):
 x,y=j%2*520,j//2*550;d.text((x+8,y+10),label+' | 0.14.0 actual capture',font=font,fill='white');gallery.paste(Image.open(folder/'frames'/f'{n:06}.png'),(x+4,y+50))
e=Path(__file__).resolve().parents[1]/'evidence/poison_moss';e.mkdir(exist_ok=True);gallery.save(e/'preview.png');(e/'preview.json').write_text(out.with_suffix('.json').read_text())
print(out,count/60,'seconds')
