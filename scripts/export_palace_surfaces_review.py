"""Export labeled, unaltered emulator frame comparisons and palette samples."""
from pathlib import Path
import argparse,io,json
from PIL import Image,ImageDraw,ImageFont
import numpy as np
p=argparse.ArgumentParser();p.add_argument('--captures',required=True);p.add_argument('--out',required=True);a=p.parse_args()
root=Path(__file__).resolve().parents[1];captures=Path(a.captures);out=Path(a.out);out.mkdir(exist_ok=True,parents=True)
font=ImageFont.truetype(str(root/'art/fonts/DejaVuSerif-Bold.ttf'),22);small=ImageFont.truetype(str(root/'art/fonts/DejaVuSerif-Bold.ttf'),16)
def load(name,phase,n):return Image.open(captures/f'surface-{name}-{phase}/frames/{n:06}.png').convert('RGB')
def save(im,path):
    buffer=io.BytesIO();im.save(buffer,format='PNG');path.write_bytes(buffer.getvalue());assert np.array_equal(np.array(Image.open(path)),np.array(im))
canvas=Image.new('RGB',(1024,1090),'#141923');d=ImageDraw.Draw(canvas)
d.text((20,12),'Level 5 masonry · actual matched replay frames',font=font,fill='#e2e8ed')
for i,(phase,label)in enumerate([('before','0.31.0'),('after','0.32.0 candidate')]):
    im=load('climb',phase,2);assert im.size==(512,480);canvas.paste(im,(i*512,70));d.text((i*512+16,44),label,font=small,fill='#d3e0ee')
    assert np.array_equal(np.array(canvas)[70:550,i*512:(i+1)*512],np.array(im))
d.text((20,574),'Level 3 Overdrive pickup · actual gameplay crops',font=font,fill='#e2e8ed')
for i,(phase,label)in enumerate([('native','Original NES book'),('before','0.31.0 orb'),('after','0.32.0 book')]):
    crop=load('book',phase,4260).crop((228,244,284,300)).resize((280,280),Image.Resampling.NEAREST);x=32+i*336
    canvas.paste(crop,(x,660));d.text((x,626),label,font=small,fill='#d3e0ee')
d.text((20,990),'Opening Level 5 rooms and distant backgrounds remain unchanged.',font=small,fill='#b9c8d9')
d.text((20,1022),'The active Overdrive spell effect is unchanged.',font=small,fill='#b9c8d9')
save(canvas,out/'Holy_Diver_v0.32.0_Comparison.png')
canvas=Image.new('RGB',(1024,1060),'#141923');d=ImageDraw.Draw(canvas)
panels=[('climb',2,'Silver stair hall'),('next',2560,'Violet lava corridor'),('late',10800,'Green hall'),('book',4260,'Overdrive spell book')]
for i,(name,n,label)in enumerate(panels):
    x,y=i%2*512,i//2*530;im=load(name,'after',n);canvas.paste(im,(x,y+50));d.text((x+16,y+14),label,font=font,fill='#e2e8ed')
    assert np.array_equal(np.array(canvas)[y+50:y+530,x:x+512],np.array(im))
save(canvas,out/'Holy_Diver_v0.32.0_Palette_Preview.png')
(root/'evidence/palace_surfaces/preview_frames.json').write_text(json.dumps(dict(actual_emulator_frames=True,no_imagegen_gameplay=True,panels=panels,comparison_frame=2,book_crop_frame=4260),indent=2)+'\n')
