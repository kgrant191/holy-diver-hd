"""Export a labeled comparison from actual replay frames and native PCM."""
from pathlib import Path
import argparse,subprocess,json
from PIL import Image,ImageDraw,ImageFont
p=argparse.ArgumentParser();p.add_argument('--work',required=True);p.add_argument('--out',required=True);a=p.parse_args();w=Path(a.work);out=Path(a.out);tmp=w/'transition_preview';tmp.mkdir(exist_ok=True)
font=ImageFont.truetype(str(Path(__file__).resolve().parents[1]/'art/fonts/DejaVuSerif-Bold.ttf'),14);fps=60.0988138974405
segments=[('stairs7_before_r0','stairs7_after_r0',96,216,4,'Upper ascending stairs'),('stairs7_before_r0','stairs7_after_r0',1352,1472,4,'Lower ascending stairs'),('thunder_before','thunder_final_after_r0',1560,1680,1,'Boss impact and Thunder tome'),('thunder_before','thunder_final_after_r0',1720,1820,1,'Thunder pickup'),('thunder_before','thunder_final_after_r0',1820,1920,1,'Boss defeat fade'),('thunder_before','thunder_final_after_r0',1924,2044,1,'Thunder acquired'),('thunder_before','thunder_final_after_r0',3200,3420,1,'Dragon travel flash')]
clips=[]
for i,(before,after,start,end,stride,label)in enumerate(segments):
 folder=tmp/str(i);folder.mkdir(exist_ok=True)
 for j,n in enumerate(range(start,end,stride)):
  im=Image.new('RGB',(1024,512),'#10131a');draw=ImageDraw.Draw(im)
  for col,(capture,title)in enumerate([(before,'0.20.1'),(after,'0.20.2')]):
   im.paste(Image.open(w/capture/'frames'/f'{n:06}.png').convert('RGB'),(col*512,32));draw.text((col*512+12,8),title+' — '+label,font=font,fill='#ead7ac')
  im.save(folder/f'{j:06}.png',compress_level=1)
 clip=tmp/f'{i}.mp4';duration=(end-start)/fps
 subprocess.run(['ffmpeg','-y','-hide_banner','-loglevel','error','-framerate',str(fps/stride),'-i',str(folder/'%06d.png'),'-ss',str((start-1)/fps),'-i',str(w/after/'full.wav'),'-t',str(duration),'-c:v','libx264','-preset','fast','-crf','19','-pix_fmt','yuv420p','-r','60','-threads','2','-c:a','aac','-ar','48000','-b:a','128k',str(clip)],check=True);clips.append(clip)
listing=tmp/'concat.txt';listing.write_text(''.join("file '"+str(p)+"'\n"for p in clips))
subprocess.run(['ffmpeg','-y','-hide_banner','-loglevel','error','-f','concat','-safe','0','-i',str(listing),'-c','copy','-movflags','+faststart',str(out)],check=True)
print(json.dumps({'preview':str(out),'segments':len(segments),'actual_replay_frames':True,'native_audio':True}))
