"""Show paired real captures from the user's stair save state."""
from pathlib import Path
import argparse,json,subprocess
from PIL import Image,ImageDraw,ImageFont
p=argparse.ArgumentParser()
for k in ['before','after','out']:p.add_argument('--'+k,required=True)
a=p.parse_args();r=Path(__file__).resolve().parents[1];out=Path(a.out);out.mkdir(parents=True,exist_ok=True)
font=ImageFont.truetype(str(r/'art/fonts/DejaVuSerif-Bold.ttf'),17)
small=ImageFont.truetype(str(r/'art/fonts/DejaVuSerif-Bold.ttf'),13)
def pair(n):
 im=Image.new('RGB',(1024,552),'#101522');d=ImageDraw.Draw(im)
 d.text((16,8),'Golden Temple — restored stair flight',font=font,fill='#f2d997')
 for x,folder,label in [(0,a.before,'Previous 0.16.2'),(512,a.after,'Corrected 0.16.3')]:
  d.text((x+16,32),label,font=small,fill='white')
  im.paste(Image.open(Path(folder)/'frames'/f'{n:06}.png').convert('RGB'),(x,56))
 d.text((16,536),'Actual MesenCE 2.2.1 | supplied save state | silent, half-speed playback',font=small,fill='#c8d0e0')
 return im
video=out/'Holy_Diver_HD_v0.16.3_Preview.mp4'
proc=subprocess.Popen(['ffmpeg','-y','-loglevel','error','-f','rawvideo','-pix_fmt','rgb24','-s','1024x552','-r','15','-i','-','-an','-c:v','libx264','-crf','18','-pix_fmt','yuv420p','-movflags','+faststart',str(video)],stdin=subprocess.PIPE)
frames=list(range(2,359,2))
for n in frames:proc.stdin.write(pair(n).tobytes())
proc.stdin.close();assert proc.wait()==0
pair(30).save(r/'evidence/level4_stairs/comparison.png')
report=dict(frames=len(frames),fps=15,seconds=len(frames)/15,playback_speed=.5,
 game_images_unretouched=True,source_frames=[frames[0],frames[-1]],silent=True)
(r/'evidence/level4_stairs/preview.json').write_text(json.dumps(report,indent=2)+'\n');print(report)
