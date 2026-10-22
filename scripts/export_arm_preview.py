"""Before/after contact sheet from actual emulator captures, plus current video."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import argparse, subprocess, shutil
p=argparse.ArgumentParser();p.add_argument('--work',required=True);p.add_argument('--title',required=True);p.add_argument('--out',required=True);a=p.parse_args()
w=Path(a.work).resolve();out=Path(a.out).resolve();out.mkdir(parents=True,exist_ok=True)
font='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
title=ImageFont.truetype(font,28);label=ImageFont.truetype(font,18);small=ImageFont.truetype(font,15)
canvas=Image.new('RGB',(1368,744),'#111b29');d=ImageDraw.Draw(canvas)
d.text((20,14),'Holy Diver HD v15.1 — Randy arm repair',font=title,fill='#f4dfb8')
d.text((20,56),'A connected forearm, wrist guard and fist in both costumes',font=label,fill='#bdcfe3')
for row,mode in enumerate(['normal','twin']):
 y=98+row*304;d.text((20,y),'Normal costume' if row==0 else 'Twin Fire costume',font=label,fill='#f4dfb8')
 for col,(f,name)in enumerate([(20,'Idle'),(190,'Casting left'),(104,'Airborne cast')]):
  x=20+col*448;d.text((x,y+28),name+'  ·  Before / Repaired',font=small,fill='white')
  for side,version in enumerate(['before','after']):
   src=w/version/mode;o=(src/f'dumps/{f:04}.oam').read_bytes()
   sprites=[(o[i+3],o[i])for i in range(0,256,4)if o[i]<240 and 0<o[i+1]<0x43 and(o[i+2]&3)==3]
   sx=min(x for x,y in sprites)*2;sy=min(y for x,y in sprites)*2
   crop=Image.open(src/f'frames/{f:04}.png').convert('RGB').crop((sx-8,sy-4,sx+62,sy+72)).resize((210,228),Image.Resampling.NEAREST)
   canvas.paste(crop,(x+side*216,y+54))
d.text((20,716),'Actual Mesen captures, enlarged with nearest-neighbor scaling. Original face, costume and native animation retained.',font=small,fill='#bdcfe3')
canvas.save(out/'Holy_Diver_v15_Comparison.png')
clips=[]
specs=[('normal',w/'after/normal',10,270,2,'v15.1 - repaired arm - normal costume'),('twin',w/'after/twin',10,270,2,'v15.1 - repaired arm - Twin Fire costume'),('stage',Path(a.title).resolve(),540,730,2,'Stage introduction - fresh start / reset'),('enemy',w/'room2/enemy',100,270,1,'Screen 2 - combat and defeat effects'),('randy',w/'room2/normal',50,450,1,'Randy defeat and remaining lives')]
for name,src,start,end,step,text in specs:
 seq=out/(name+'_frames');seq.mkdir(exist_ok=True);frames=list(range(start,end+1,step))
 for i,n in enumerate(frames,1):shutil.copy2(src/f'frames/{n:04}.png',seq/f'{i:04}.png')
 dest=out/(name+'.mp4');clips.append(dest)
 vf=f"scale=1024:960:flags=neighbor,pad=1024:1016:0:56:black,drawtext=fontfile={font}:text='{text}':x=24:y=15:fontsize=26:fontcolor=white"
 subprocess.run(['ffmpeg','-y','-v','error','-framerate',str(60.0988/step),'-i',str(seq/'%04d.png'),'-ss',str((start-1)/60.0988),'-i',str(src/'full.wav'),'-t',str(len(frames)/(60.0988/step)),'-vf',vf,'-r','60','-c:v','libx264','-preset','fast','-crf','18','-pix_fmt','yuv420p','-c:a','aac','-b:a','160k','-shortest',str(dest)],check=True)
 concat=out/'clips.txt';concat.write_text(''.join("file '"+str(f)+"'\n"for f in clips))
subprocess.run(['ffmpeg','-y','-v','error','-f','concat','-safe','0','-i',str(concat),'-c','copy','-movflags','+faststart',str(out/'Holy_Diver_v15_Gameplay.mp4')],check=True)
print('Exported v15.1 comparison and live gameplay video')
