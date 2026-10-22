from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import argparse,subprocess,shutil
p=argparse.ArgumentParser();p.add_argument('--before',required=True);p.add_argument('--release',required=True);p.add_argument('--motion',required=True);p.add_argument('--out',required=True);a=p.parse_args();before=Path(a.before).resolve();release=Path(a.release).resolve();motion=Path(a.motion).resolve();out=Path(a.out).resolve();out.mkdir(parents=True,exist_ok=True)
font='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf';title=ImageFont.truetype(font,26);label=ImageFont.truetype(font,18);small=ImageFont.truetype(font,16)
c=Image.new('RGB',(1088,930),'#111b29');d=ImageDraw.Draw(c)
d.text((24,16),'Holy Diver HD v15',font=title,fill='#f4dfb8');d.text((24,55),'Stage introductions, lives cards and matching defeat effects',font=label,fill='white')
for x,text,path in [(24,'Fresh start / reset',release/'title/frames/0580.png'),(552,'After losing a life',release/'normal/frames/0280.png')]:
 d.text((x,88),text,font=label,fill='#b6c9dd');c.paste(Image.open(path).convert('RGB'),(x,115))
items=[('Previous ring',before/'enemy/frames/0154.png',(398,236,502,340)),('HD compact phase',motion/'enemy/frames/0154.png',(398,236,502,340)),('HD expanded phase',motion/'enemy/frames/0158.png',(398,236,502,340)),("Randy's explosion",motion/'normal/frames/0078.png',(212,330,316,434))]
for i,(text,path,box)in enumerate(items):
 x=24+i*264;d.text((x,626),text,font=small,fill='white');crop=Image.open(path).convert('RGB').crop(box).resize((208,208),Image.Resampling.NEAREST);c.paste(crop,(x,657))
d.text((24,892),'Actual Mesen captures. Effect details enlarged; native timing and game values retained.',font=small,fill='#b6c9dd');c.save(out/'Holy_Diver_v15_Comparison.png')
clips=[]
for name,src,start,end,step,text in [('stage',release/'title',540,730,2,'Stage introduction - fresh start / reset'),('enemy',motion/'enemy',100,270,1,'Enemy defeat - both HD phases'),('randy',motion/'normal',50,450,1,'Randy defeat and remaining lives')]:
 seq=out/(name+'_frames');seq.mkdir(exist_ok=True);frames=list(range(start,end+1,step))
 for i,n in enumerate(frames,1):shutil.copy2(src/f'frames/{n:04}.png',seq/f'{i:04}.png')
 dest=out/(name+'.mp4');clips.append(dest)
 vf=f"scale=1024:960:flags=neighbor,pad=1024:1016:0:56:black,drawtext=fontfile={font}:text='{text}':x=24:y=15:fontsize=26:fontcolor=white"
 subprocess.run(['ffmpeg','-y','-v','error','-framerate',str(60.0988/step),'-i',str(seq/'%04d.png'),'-ss',str((start-1)/60.0988),'-i',str(src/'full.wav'),'-t',str(len(frames)/(60.0988/step)),'-vf',vf,'-r','60','-c:v','libx264','-preset','fast','-crf','18','-pix_fmt','yuv420p','-c:a','aac','-b:a','160k','-shortest',str(dest)],check=True)
concat=out/'clips.txt';concat.write_text(''.join("file '"+str(f)+"'\n"for f in clips))
subprocess.run(['ffmpeg','-y','-v','error','-f','concat','-safe','0','-i',str(concat),'-c','copy','-movflags','+faststart',str(out/'Holy_Diver_v15_Gameplay.mp4')],check=True)
print('Exported live comparison and motion video')
