"""Export actual late-Palace captures with their original game audio."""
from pathlib import Path
import argparse,subprocess,wave,json
from PIL import Image,ImageDraw,ImageFont
p=argparse.ArgumentParser();p.add_argument('--capture',required=True);p.add_argument('--out',required=True);a=p.parse_args();out=Path(a.out);out.parent.mkdir(parents=True,exist_ok=True);root=Path(__file__).resolve().parents[1];capture=Path(a.capture)
font=ImageFont.truetype(str(root/'art/fonts/DejaVuSerif-Bold.ttf'),17);small=ImageFont.truetype(str(root/'art/fonts/DejaVuSerif-Bold.ttf'),12)
clips=[(320,800,'Lava corridor • Returning skeleton and guardian'),(1480,1900,'Blizzard • Frozen lava and small platforms'),(3260,3680,'Lava corridor • Continuous palace scenery'),(8940,9500,'Platform shaft • Moving stone lift'),(11680,12200,'Next hall • Returning rising sentry'),(13990,14590,'Skull shaft entrance • Recorded final chamber')]
# NES NTSC frame clock; preserve original PCM without time stretching.
fps=60.0988138974405
with wave.open(str(capture/'full.wav'),'rb')as f:params=f.getparams();pcm=f.readframes(f.getnframes())
block=params.nchannels*params.sampwidth;rate=params.framerate;audio=bytearray();sequence=[]
for first,last,label in clips:
 audio+=pcm[round(first/fps*rate)*block:round(last/fps*rate)*block];sequence.extend((n,label)for n in range(first,last,2))
wav=out.with_suffix('.wav')
with wave.open(str(wav),'wb')as f:f.setparams(params);f.writeframes(audio)
proc=subprocess.Popen(['ffmpeg','-y','-loglevel','error','-f','rawvideo','-pixel_format','rgb24','-video_size','768x768','-framerate',str(fps/2),'-i','pipe:0','-i',str(wav),'-c:v','libx264','-preset','fast','-crf','20','-pix_fmt','yuv420p','-c:a','aac','-b:a','128k','-shortest','-movflags','+faststart',str(out)],stdin=subprocess.PIPE)
for n,label in sequence:
 im=Image.new('RGB',(768,768),'#10121b');im.paste(Image.open(capture/'frames'/f'{n:06}.png').convert('RGB').resize((768,720),Image.Resampling.NEAREST),(0,30));d=ImageDraw.Draw(im);d.text((12,5),label,font=font,fill='#f3dfbd');d.text((12,752),'0.23.0 review • Actual MesenCE 2.2.1 capture • Native gameplay and audio',font=small,fill='#b7bdc9');proc.stdin.write(im.tobytes())
proc.stdin.close();assert proc.wait()==0;wav.unlink();out.with_suffix('.json').write_text(json.dumps(dict(actual_gameplay=True,fps=fps/2,native_audio=True,clips=[dict(first=x[0],last=x[1],label=x[2])for x in clips]),indent=2)+'\n');print(out)
