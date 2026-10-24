"""Paired, unretouched Mesen boss fight and Breaker review captures."""
from pathlib import Path
import argparse,json,subprocess,tempfile
from PIL import Image,ImageDraw,ImageFont
p=argparse.ArgumentParser()
for k in ['before','after','out']:p.add_argument('--'+k,required=True)
a=p.parse_args();b,c,out=Path(a.before),Path(a.after),Path(a.out);out.mkdir(parents=True,exist_ok=True)
font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',17);title=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',20)
stills=[('Complete wall boss / reused cave and terrain','arena',200),('Breaker tome / native collection position','victory',1100)]
sheet=Image.new('RGB',(1056,1128),'#0b101b');d=ImageDraw.Draw(sheet)
d.text((16,14),'HOLY DIVER HD 0.10.0 — LEVEL 2 BOSS',font=title,fill='#ecd4a0');d.text((16,47),'Actual Mesen captures • left: approved 0.9.0 • right: 0.10.0',font=font,fill='#b8c4d4')
for i,(label,case,n)in enumerate(stills):
 y=88+i*524;d.text((16,y),label,font=title,fill='#ddc186')
 for ext in ['ram','ppu','oam','view']:assert(b/case/f'dumps/{n:04}.{ext}').read_bytes()==(c/case/f'dumps/{n:04}.{ext}').read_bytes()
 for x,folder in [(16,b),(528,c)]:sheet.paste(Image.open(folder/case/f'frames/{n:04}.png').convert('RGB'),(x,y+28))
sheet.save(out/'comparison.png')
clips=[('arena',150,240,'Full boss and native room movement'),('victory',180,440,'Combat, reused fireballs and native hit flashes'),('victory',640,960,'Native boss defeat and disappearance'),('victory',1060,1220,'Breaker pickup, victory flash and announcement'),('victory',1360,1620,'Existing Stage 3 title card and arrival')]
with tempfile.TemporaryDirectory()as td:
 td=Path(td);index=0
 for case,start,end,label in clips:
  for n in range(start,end+1,2):
   im=Image.new('RGB',(1024,528),'#0b101b');draw=ImageDraw.Draw(im);draw.text((12,6),'0.9.0 → 0.10.0 | '+label,font=font,fill='#ecd4a0')
   for x,folder in [(0,b),(512,c)]:im.paste(Image.open(folder/case/f'frames/{n:04}.png').convert('RGB'),(x,48))
   im.save(td/f'{index:05}.png');index+=1
 subprocess.run(['ffmpeg','-v','error','-y','-framerate','30','-i',str(td/'%05d.png'),'-c:v','libx264','-crf','19','-pix_fmt','yuv420p','-movflags','+faststart',str(out/'review.mp4')],check=True)
(out/'preview_sources.json').write_text(json.dumps(dict(baseline='0.9.0',candidate='0.10.0',stills=stills,clips=clips,fps=30,capture_stride=2,retouched=False,audio=False,normal_speed=True),indent=2)+'\n');print('Exported actual paired boss review.')
