"""Unretouched paired Mesen frame, with nearest-neighbor detail crops."""
from pathlib import Path
import argparse,json
from PIL import Image,ImageDraw,ImageFont
p=argparse.ArgumentParser()
for k in ['before','after','out']:p.add_argument('--'+k,required=True)
a=p.parse_args();r=Path(__file__).resolve().parents[1];font=ImageFont.truetype(str(r/'art/fonts/DejaVuSerif-Bold.ttf'),18);small=ImageFont.truetype(str(r/'art/fonts/DejaVuSerif-Bold.ttf'),14)
im=Image.new('RGB',(1024,736),'#101522');d=ImageDraw.Draw(im);d.text((16,8),'Outdoor dragon area — missed ornament tile removed',font=font,fill='#f2d997');box=(432,280,480,328)
for x,folder,label in [(0,a.before,'Previous 0.19.0'),(512,a.after,'Fixed 0.19.1')]:
 frame=Image.open(Path(folder)/'frames/000650.png').convert('RGB');d.text((x+16,36),label,font=small,fill='white');im.paste(frame,(x,60));im.paste(frame.crop(box).resize((144,144),Image.Resampling.NEAREST),(x+16,572));d.text((x+176,584),'Same scene and inputs',font=small,fill='white');d.text((x+176,610),'3x detail — original pixels',font=small,fill='#c8d0e0')
d.text((16,718),'Actual MesenCE 2.2.1 capture | frame650 | no retouching',font=small,fill='#c8d0e0');out=Path(a.out);out.parent.mkdir(exist_ok=True,parents=True);im.save(out)
(r/'evidence/level4_residue/comparison.json').write_text(json.dumps(dict(frame=650,source_before=a.before,source_after=a.after,game_images_unretouched=True,detail_crop=box,detail_scale=3,detail_resampling='nearest'),indent=2)+'\n');print(out)
