"""Render actual revised ceiling and climb footage; keep original game audio."""
from pathlib import Path
import argparse,subprocess,wave,json
from PIL import Image,ImageDraw,ImageFont
p=argparse.ArgumentParser();p.add_argument('--opening',required=True);p.add_argument('--climb',required=True);p.add_argument('--out',required=True);a=p.parse_args();out=Path(a.out);out.parent.mkdir(parents=True,exist_ok=True);root=Path(__file__).resolve().parents[1]
font=ImageFont.truetype(str(root/'art/fonts/DejaVuSerif-Bold.ttf'),17);small=ImageFont.truetype(str(root/'art/fonts/DejaVuSerif-Bold.ttf'),12)
clips=[(Path(a.opening),300,900,'Muted green slime ceiling • Rocky floor preserved'),(Path(a.climb),2,700,'Stair climb • Continuous palace background'),(Path(a.climb),700,878,'The same serpent • Completed HD artwork'),(Path(a.climb),878,1214,'Native room transition • Next hall entrance')]
sequence=[];audio=bytearray();params=None
for capture,first,last,label in clips:
 with wave.open(str(capture/'full.wav'),'rb')as f:
  if params is None:params=f.getparams()
  else:assert f.getparams()[:3]==params[:3] and f.getparams()[4:]==params[4:]
  pcm=f.readframes(f.getnframes())
 block=params.nchannels*params.sampwidth;rate=params.framerate;audio+=pcm[round(first/60*rate)*block:round(last/60*rate)*block]
 sequence += [(capture,n,label)for n in range(first,last,2)]
wav=out.with_suffix('.wav')
with wave.open(str(wav),'wb')as f:f.setparams(params);f.writeframes(audio)
proc=subprocess.Popen(['ffmpeg','-y','-loglevel','error','-f','rawvideo','-pixel_format','rgb24','-video_size','768x768','-framerate','30','-i','pipe:0','-i',str(wav),'-c:v','libx264','-preset','fast','-crf','20','-pix_fmt','yuv420p','-c:a','aac','-b:a','128k','-shortest','-movflags','+faststart',str(out)],stdin=subprocess.PIPE)
for capture,n,label in sequence:
 im=Image.new('RGB',(768,768),'#10121b');im.paste(Image.open(capture/'frames'/f'{n:06}.png').convert('RGB').resize((768,720),Image.Resampling.NEAREST),(0,30));d=ImageDraw.Draw(im);d.text((12,5),label,font=font,fill='#f3dfbd');d.text((12,752),'0.21.1 review • Actual MesenCE 2.2.1 capture • Native gameplay and audio',font=small,fill='#b7bdc9');proc.stdin.write(im.tobytes())
proc.stdin.close();assert proc.wait()==0;wav.unlink();out.with_suffix('.json').write_text(json.dumps(dict(actual_gameplay=True,fps=30,clips=[dict(capture=x[0].name,first=x[1],last=x[2],label=x[3])for x in clips]),indent=2)+'\n');print(out)
