"""Actual paired ceiling review captures, with a slowed native head-bump clip."""
from pathlib import Path
import argparse,json,subprocess,tempfile
from PIL import Image,ImageDraw,ImageFont
p=argparse.ArgumentParser()
for k in ['before','after','out']:p.add_argument('--'+k,required=True)
p.add_argument('--before-version',default='0.8.1')
p.add_argument('--after-version',default='0.8.2')
p.add_argument('--title',default='READABLE CAVE CEILING')
a=p.parse_args();b,c,out=Path(a.before),Path(a.after),Path(a.out);out.mkdir(parents=True,exist_ok=True)
font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',17);title=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',20)
stills=[('Solid foreground ceiling / visible bat attachment','traversal',200),('Low overhang / native head-bump position','extended_traversal',624)]
sheet=Image.new('RGB',(1056,1128),'#0b101b');d=ImageDraw.Draw(sheet)
d.text((16,14),f'HOLY DIVER HD {a.after_version} — {a.title}',font=title,fill='#ecd4a0');d.text((16,47),f'Actual Mesen captures • left: {a.before_version} • right: {a.after_version}',font=font,fill='#b8c4d4')
for i,(label,case,n)in enumerate(stills):
 y=88+i*524;d.text((16,y),label,font=title,fill='#ddc186')
 for ext in ['ram','ppu','oam']:assert(b/case/f'dumps/{n:04}.{ext}').read_bytes()==(c/case/f'dumps/{n:04}.{ext}').read_bytes()
 for x,folder in [(16,b),(528,c)]:sheet.paste(Image.open(folder/case/f'frames/{n:04}.png').convert('RGB'),(x,y+28))
sheet.save(out/'comparison.png')
clips=[('traversal',100,240,'Bats hang from a solid foreground ceiling',1),('extended_traversal',540,650,'Low ceiling and head bumps / half speed',2),('extended_traversal',700,840,'Ceiling silhouette at the lava-fall approach',1),('stair_walk',20,180,'Approved stairs remain unchanged',1),('freeze_thaw',340,500,'Native Blizzard flashes preserved',1)]
with tempfile.TemporaryDirectory()as td:
 td=Path(td);index=0
 for case,start,end,label,repeats in clips:
  for n in range(start,end+1,2):
   im=Image.new('RGB',(1024,528),'#0b101b');draw=ImageDraw.Draw(im);draw.text((12,6),f'{a.before_version}  →  {a.after_version}  |  '+label,font=font,fill='#ecd4a0')
   for x,folder in [(0,b),(512,c)]:im.paste(Image.open(folder/case/f'frames/{n:04}.png').convert('RGB'),(x,48))
   for _ in range(repeats):im.save(td/f'{index:05}.png');index+=1
 subprocess.run(['ffmpeg','-v','error','-y','-framerate','30','-i',str(td/'%05d.png'),'-c:v','libx264','-crf','19','-pix_fmt','yuv420p','-movflags','+faststart',str(out/'review.mp4')],check=True)
(out/'preview_sources.json').write_text(json.dumps(dict(baseline=a.before_version,candidate=a.after_version,stills=stills,clips=clips,fps=30,capture_stride=2,retouched=False,audio=False,head_bump_clip_speed=0.5),indent=2)+'\n')
print('Wrote',out/'comparison.png','and',out/'review.mp4')
