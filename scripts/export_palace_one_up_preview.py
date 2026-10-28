"""Show actual before/after gameplay with nearest-neighbor pickup enlargements."""
from pathlib import Path
import argparse,json
from PIL import Image,ImageDraw,ImageFont
p=argparse.ArgumentParser();p.add_argument('--captures',required=True);p.add_argument('--out',required=True);a=p.parse_args();c=Path(a.captures);root=Path(__file__).resolve().parents[1]
font=ImageFont.truetype(str(root/'art/fonts/DejaVuSerif-Bold.ttf'),18);small=ImageFont.truetype(str(root/'art/fonts/DejaVuSerif-Bold.ttf'),13)
cases=[('dragon',1420,'Upper hall / dragon-form palette'),('next',4750,'Lava room / normal palette')]
canvas=Image.new('RGB',(1040,1300),'#10121b');draw=ImageDraw.Draw(canvas)
for row,(case,n,label)in enumerate(cases):
 top=row*650;draw.text((12,top+8),label,font=font,fill='#f0ddba')
 o=(c/f'{case}_after/oam/{n:06}.bin').read_bytes();cells=[(x*2,(y+1)*2)for y,t,at,x in zip(o[::4],o[1::4],o[2::4],o[3::4])if y<239 and t==0x4e];assert len(cells)==1;x,y=cells[0]
 for col,phase in enumerate(['before','after']):
  left=8+col*520;im=Image.open(c/f'{case}_{phase}/frames/{n:06}.png').convert('RGB');canvas.paste(im,(left,top+58));draw.text((left,top+35),'0.22.1 / reported sprite'if phase=='before'else'0.22.2 / restored HD figurine',font=small,fill='#dce2eb')
  crop=im.crop((x-8,y-4,x+24,y+36));canvas.paste(crop.resize((80,100),Image.Resampling.NEAREST),(left,top+544));draw.text((left+92,top+551),'Actual gameplay crop',font=small,fill='#c9d0dc');draw.text((left+92,top+573),'2.5x nearest-neighbor enlargement',font=small,fill='#c9d0dc');draw.text((left+92,top+595),'Artwork, scenery and effects otherwise unchanged',font=small,fill='#c9d0dc')
out=Path(a.out);out.parent.mkdir(parents=True,exist_ok=True);canvas.save(out)
out.with_suffix('.json').write_text(json.dumps(dict(actual_gameplay=True,postprocessed_game_pixels=False,source_frames=[dict(case=c,frame=n,label=l)for c,n,l in cases],crop_enlargement=2.5),indent=2)+'\n');print(out)
