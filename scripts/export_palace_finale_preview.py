"""Export actual late-Palace captures with their original game audio."""
from pathlib import Path
import argparse,subprocess,wave,json
from PIL import Image,ImageDraw,ImageFont
p=argparse.ArgumentParser();p.add_argument('--capture',required=True);p.add_argument('--out',required=True);p.add_argument('--ending',required=True);a=p.parse_args();out=Path(a.out);out.parent.mkdir(parents=True,exist_ok=True);root=Path(__file__).resolve().parents[1];capture=Path(a.capture)
font=ImageFont.truetype(str(root/'art/fonts/DejaVuSerif-Bold.ttf'),17);small=ImageFont.truetype(str(root/'art/fonts/DejaVuSerif-Bold.ttf'),12)
clips=[(180,400,'Skull shaft • Moving stone lift'),(2900,3200,'Skull shaft • Updated masonry'),(7120,7320,'Demonic Palace • Boss chamber'),(7558,7600,'Thunder • HD scenery through the flash'),(8260,8310,'Boss fight • Skull and articulated hands'),(9470,9520,'Thunder • Second flash sequence'),(11690,11860,'Boss fight • Thunder and movement'),(13000,13400,'Demonic Palace • Final combat'),(13600,13900,'Boss defeat • Victory effigy'),(14240,14540,'Victory ascent • HD character and scenery'),(14720,14900,'Victory • Native white flash'),(15190,15374,'Stage 6 • HD title card'),(15374,15584,'Level 6 • Recorded entrance')]
# NES NTSC frame clock; preserve original PCM without time stretching.
fps=60.0988138974405
with wave.open(str(capture/'full.wav'),'rb')as f:params=f.getparams();pcm=f.readframes(f.getnframes())
block=params.nchannels*params.sampwidth;rate=params.framerate;audio=bytearray();sequence=[]
for first,last,label in clips:
 audio+=pcm[round(first/fps*rate)*block:round(last/fps*rate)*block];sequence.extend((n,label)for n in range(first,last))
wav=out.with_suffix('.wav')
with wave.open(str(wav),'wb')as f:f.setparams(params);f.writeframes(audio)
proc=subprocess.Popen(['ffmpeg','-y','-loglevel','error','-f','rawvideo','-pixel_format','rgb24','-video_size','768x768','-framerate',str(fps),'-i','pipe:0','-i',str(wav),'-c:v','libx264','-preset','fast','-crf','20','-pix_fmt','yuv420p','-c:a','aac','-b:a','128k','-shortest','-movflags','+faststart',str(out)],stdin=subprocess.PIPE)
for n,label in sequence:
 im=Image.new('RGB',(768,768),'#10121b');im.paste(Image.open((Path(a.ending)if n>=15120 else capture)/'frames'/f'{n:06}.png').convert('RGB').resize((768,720),Image.Resampling.NEAREST),(0,30));d=ImageDraw.Draw(im);d.text((12,5),label,font=font,fill='#f3dfbd');d.text((12,752),'0.24.0 review • Actual MesenCE 2.2.1 capture • Native gameplay and audio',font=small,fill='#b7bdc9');proc.stdin.write(im.tobytes())
proc.stdin.close();assert proc.wait()==0;wav.unlink();out.with_suffix('.json').write_text(json.dumps(dict(actual_gameplay=True,ending_capture='final stage-card repair',earlier_capture='identical pre-card gameplay mappings',fps=fps,native_audio=True,clips=[dict(first=x[0],last=x[1],label=x[2])for x in clips]),indent=2)+'\n');print(out)
