"""Export labeled live captures; never composite new art into screenshots."""
from pathlib import Path
import argparse
import json
from PIL import Image, ImageDraw, ImageFont

p=argparse.ArgumentParser()
for name in ['before','after','out']:
    p.add_argument('--'+name,required=True)
a=p.parse_args()
root=Path(__file__).resolve().parents[1]
out=Path(a.out);out.mkdir(parents=True,exist_ok=True)
font=ImageFont.truetype(str(root/'art/fonts/DejaVuSerif-Bold.ttf'),15)
rows=[('pickup',20,'Tree / 1-up / standing ghoul'),('descent',640,'Lower branch platforms'),('descent',840,'Roots and ground')]
canvas=Image.new('RGB',(1024,len(rows)*510),'#101522');d=ImageDraw.Draw(canvas)
for r,(case,frame,label) in enumerate(rows):
    for col,(folder,version) in enumerate([(a.before,'0.1.1'),(a.after,'0.2.0 candidate')]):
        x,y=col*512,r*510
        d.text((x+8,y+6),f'{version} — {label}',font=font,fill='#e7c78b')
        canvas.paste(Image.open(Path(folder)/case/'frames'/f'{frame:04}.png'),(x,y+30))
canvas.save(out/'comparison.png')
rows=[('pickup',120,'Twin Fire: approaching 1-up'),('pickup',140,'Twin Fire: collected (lives 3 → 4)'),
      ('normal_pickup',1480,'Normal: approaching 1-up'),('normal_pickup',1520,'Normal: collected (lives 3 → 4)'),
      ('ledge',588,'Slow walk: before downward motion'),('ledge',596,'Slow walk: falling past native edge')]
canvas=Image.new('RGB',(1024,1530),'#101522');d=ImageDraw.Draw(canvas)
for n,(case,frame,label) in enumerate(rows):
    x,y=n%2*512,n//2*510
    d.text((x+8,y+6),label,font=font,fill='#e7c78b')
    canvas.paste(Image.open(Path(a.after)/case/'frames'/f'{frame:04}.png'),(x,y+30))
canvas.save(out/'pickup_and_edges.png')
poses=json.loads((root/'art/screen1_3/ghoul_poses.json').read_text())
examples={}
for case in ['pickup','ledge']:
    for path in sorted((Path(a.after)/case/'dumps').glob('*.oam')):
        frame=int(path.stem)
        if frame%4 or frame<4:continue
        data=path.read_bytes();sprites=[tuple(data[k:k+4]) for k in range(0,256,4)]
        prior=(path.parent/f'{frame-2:04}.oam').read_bytes()
        old=[tuple(prior[k:k+4]) for k in range(0,256,4)]
        for i,pose in enumerate(poses):
            for y,t,attr,x in sprites:
                if t!=pose['tiles'][0][2] or attr&3!=1 or y>=200:continue
                flip=bool(attr&0x40);key=(i,flip)
                if key in examples:continue
                dx=lambda xx:pose['size'][0]-8-xx if flip else xx
                ax,ay,_=pose['tiles'][0];ox,oy=x-dx(ax),y-ay
                if not all((oy+py,pt,attr,ox+dx(px)) in sprites for px,py,pt in pose['tiles']):continue
                # Require the same tile/attribute footprint in the preceding
                # sample; movement may shift X/Y slightly between samples.
                if not all(any(ot==pt and oa==attr and abs(oy+py-oy0)<=3 and abs(ox+dx(px)-ox0)<=3 for oy0,ot,oa,ox0 in old) for px,py,pt in pose['tiles']):continue
                examples[key]=(case,frame,(ox*2-8,oy*2-6,ox*2+40,oy*2+58))
assert len(examples)==12
canvas=Image.new('RGB',(768,480),'#101522');d=ImageDraw.Draw(canvas)
for n,(key,(case,frame,box)) in enumerate(sorted(examples.items())):
    x,y=n%4*192,n//4*160
    d.text((x+3,y+3),f"Pose {key[0]} / {'right' if key[1] else 'left'}",font=font,fill='#e7c78b')
    for col,folder in enumerate([a.before,a.after]):
        crop=Image.open(Path(folder)/case/'frames'/f'{frame:04}.png').crop(box)
        canvas.paste(crop.resize((96,128),Image.Resampling.NEAREST),(x+col*96,y+26))
canvas.save(out/'enemies_before_after_2x.png')
print('Saved live comparison and pickup/edge captures to',out)
