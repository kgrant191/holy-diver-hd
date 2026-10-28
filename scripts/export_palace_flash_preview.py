"""Show every captured native frame of the corrected spell and pickup flashes."""
from pathlib import Path
import argparse,subprocess,wave,json
from PIL import Image,ImageDraw,ImageFont
p=argparse.ArgumentParser();p.add_argument('--captures',required=True);p.add_argument('--out',required=True);a=p.parse_args();c=Path(a.captures);out=Path(a.out);out.parent.mkdir(parents=True,exist_ok=True);root=Path(__file__).resolve().parents[1]
font=ImageFont.truetype(str(root/'art/fonts/DejaVuSerif-Bold.ttf'),16);small=ImageFont.truetype(str(root/'art/fonts/DejaVuSerif-Bold.ttf'),12)
clips=[('opening_after',8760,9221,'Column hall • Thunder casts and dragon pickup'),('hall_after',280,701,'Stair hall • Thunder casts and dragon pickup')]
sequence=[];audio=bytearray();params=None
for name,first,last,label in clips:
 capture=c/name
 with wave.open(str(capture/'full.wav'),'rb')as f:
  if params is None:params=f.getparams()
  else:assert f.getparams()[:3]==params[:3]and f.getparams()[4:]==params[4:]
  f.setpos(round(first/60*params.framerate));audio+=f.readframes(round((last-first)/60*params.framerate))
 sequence += [(capture,n,label)for n in range(first,last)]
wav=out.with_suffix('.wav')
with wave.open(str(wav),'wb')as f:f.setparams(params);f.writeframes(audio)
proc=subprocess.Popen(['ffmpeg','-y','-loglevel','error','-f','rawvideo','-pixel_format','rgb24','-video_size','768x768','-framerate','60','-i','pipe:0','-i',str(wav),'-c:v','libx264','-preset','fast','-crf','18','-pix_fmt','yuv420p','-c:a','aac','-b:a','128k','-shortest','-movflags','+faststart',str(out)],stdin=subprocess.PIPE)
for capture,n,label in sequence:
 im=Image.new('RGB',(768,768),'#10121b');im.paste(Image.open(capture/'frames'/f'{n:06}.png').convert('RGB').resize((768,720),Image.Resampling.NEAREST),(0,30));d=ImageDraw.Draw(im);d.text((12,5),label,font=font,fill='#f3dfbd');d.text((12,752),'0.22.1 review • Actual Mesen capture at 60 fps • Native gameplay and audio',font=small,fill='#b7bdc9');proc.stdin.write(im.tobytes())
proc.stdin.close();assert proc.wait()==0;wav.unlink();out.with_suffix('.json').write_text(json.dumps(dict(actual_gameplay=True,fps=60,consecutive_frames=True,clips=[dict(capture=x[0],first=x[1],last_exclusive=x[2],label=x[3])for x in clips]),indent=2)+'\n');print(out)
