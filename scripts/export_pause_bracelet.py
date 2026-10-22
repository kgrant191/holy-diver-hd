from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import argparse,subprocess,shutil
p=argparse.ArgumentParser();p.add_argument('--capture',required=True);p.add_argument('--out',required=True);a=p.parse_args();src=Path(a.capture).resolve();out=Path(a.out).resolve();out.mkdir(parents=True,exist_ok=True)
font='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf';h=ImageFont.truetype(font,25);f=ImageFont.truetype(font,18)
c=Image.new('RGB',(1088,610),'#111b29');d=ImageDraw.Draw(c)
d.text((24,16),'Same bracelet in gameplay and the Start menu',font=h,fill='#f4dfb8')
for x,label,frame in [(24,'Gameplay pickup',2),(552,'Start / pause — after collection',780)]:
 d.text((x,58),label,font=f,fill='white');im=Image.open(src/f'frames/{frame:04}.png').convert('RGB');c.paste(im,(x,88))
d.text((24,580),'Actual Mesen captures · the menu uses the same approved bracelet artwork',font=f,fill='#b6c9dd')
c.save(out/'Holy_Diver_v14_Comparison.png')
sequence=out/'video_frames';sequence.mkdir(exist_ok=True)
for i,frame in enumerate(range(600,846,2),1):shutil.copy2(src/f'frames/{frame:04}.png',sequence/f'{i:04}.png')
vf=f"scale=1024:960:flags=neighbor,pad=1024:1016:0:56:black,drawtext=fontfile={font}:text='Collect bracelet, then press START':x=24:y=15:fontsize=26:fontcolor=white"
subprocess.run(['ffmpeg','-y','-v','error','-framerate','30.0494','-i',str(sequence/'%04d.png'),'-ss',str(599/60.0988),'-i',str(src/'full.wav'),'-frames:v','123','-vf',vf,'-c:v','libx264','-preset','fast','-crf','18','-pix_fmt','yuv420p','-c:a','aac','-b:a','160k','-shortest','-movflags','+faststart',str(out/'Holy_Diver_v14_Gameplay.mp4')],check=True)
print('Exported live menu comparison and video')
