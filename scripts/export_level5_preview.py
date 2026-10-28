"""Export selected actual Mesen captures at native speed, with native audio."""
from pathlib import Path
import argparse,subprocess,wave,json
from PIL import Image,ImageDraw,ImageFont
p=argparse.ArgumentParser();p.add_argument('--capture',required=True);p.add_argument('--out',required=True);a=p.parse_args();c=Path(a.capture);out=Path(a.out);out.parent.mkdir(parents=True,exist_ok=True)
root=Path(__file__).resolve().parents[1];font=ImageFont.truetype(str(root/'art/fonts/DejaVuSerif-Bold.ttf'),17);small=ImageFont.truetype(str(root/'art/fonts/DejaVuSerif-Bold.ttf'),12)
clips=[(300,900,'Demonic Palace • Lava cavern'),(2650,3160,'Blizzard • Native lava freeze / thaw'),(5030,5320,'Crimson column chamber'),(6090,6630,'Column climb • Skeletons and boulders'),(8190,8470,'The next palace hall'),(8790,9100,'Thunder • Two native casts'),(9210,9530,'Dragon flight • Segmented serpent'),(9598,9642,'Stair hall • First entry only'),(9700,9840,'Start menu • THUNDER spelling restored')]
with wave.open(str(c/'full.wav'),'rb')as f:params=f.getparams();pcm=f.readframes(f.getnframes())
# Captures occur every other 60 Hz game frame. Movie audio is the unchanged
# native emulator stream; concatenate exactly the same selected time intervals.
rate=params.framerate;block=params.nchannels*params.sampwidth;audio=bytearray();sequence=[]
for first,last,label in clips:
 for n in range(first,last,2):sequence.append((n,label))
 audio+=pcm[round(first/60*rate)*block:round(last/60*rate)*block]
# Hold the final actual menu capture for a readable ending, with silence.
sequence += [(9838,'Start menu • THUNDER spelling restored')]*45;audio+=bytes(round(1.5*rate)*block)
wav=out.with_suffix('.preview.wav')
with wave.open(str(wav),'wb')as f:f.setparams(params);f.writeframes(audio)
cmd=['ffmpeg','-y','-loglevel','error','-f','rawvideo','-pixel_format','rgb24','-video_size','768x768','-framerate','30','-i','pipe:0','-i',str(wav),'-c:v','libx264','-preset','fast','-crf','20','-pix_fmt','yuv420p','-c:a','aac','-b:a','128k','-shortest','-movflags','+faststart',str(out)]
proc=subprocess.Popen(cmd,stdin=subprocess.PIPE)
for n,label in sequence:
 im=Image.new('RGB',(768,768),'#10121b');im.paste(Image.open(c/'frames'/f'{n:06}.png').convert('RGB').resize((768,720),Image.Resampling.NEAREST),(0,30));d=ImageDraw.Draw(im);d.text((12,5),label,font=font,fill='#f3dfbd');d.text((12,752),'0.21.0 review • Actual MesenCE 2.2.1 replay • Native gameplay and audio',font=small,fill='#b7bdc9');proc.stdin.write(im.tobytes())
proc.stdin.close();assert proc.wait()==0;wav.unlink();out.with_suffix('.json').write_text(json.dumps(dict(actual_gameplay=True,fps=30,stride=2,clips=clips,ending_hold_seconds=1.5),indent=2)+'\n');print(out)
