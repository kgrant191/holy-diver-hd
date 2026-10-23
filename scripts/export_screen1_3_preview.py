"""Export labeled, unretouched live screenshots and nearest-neighbor details."""
from pathlib import Path
from PIL import Image, ImageDraw
import argparse

p = argparse.ArgumentParser()
for name in ['before', 'after', 'out']:
    p.add_argument('--'+name, required=True)
a = p.parse_args()
before, after, out = [Path(v) for v in [a.before, a.after, a.out]]
out.mkdir(parents=True, exist_ok=True)
comparison = Image.new('RGB', (1024, 1536), '#101724')
d = ImageDraw.Draw(comparison)
for i in range(3):
    for j, source in enumerate([before, after]):
        d.text((j*512+12, i*512+8), f'State {i+1} / frame 20 / '+('approved 0.0.2' if j==0 else '0.1.0 candidate'), fill='white')
        comparison.paste(Image.open(source/f'state{i+1}/frames/0020.png'), (j*512, i*512+32))
comparison.save(out/'comparison.png')

# Full screenshots preserve spatial context for effects and palette transitions.
samples = [('state1',220,'flying enemies and expanding impact'),
           ('state3',268,'small initial impact'),
           ('state2',360,'rolling ghoul and left-facing Randy'),
           ('state3',420,'normal costume and flying skulls'),
           ('state3',680,'shared Randy defeat effect'),
           ('state2',700,'shared lives card')]
motion = Image.new('RGB',(1024,1536),'#101724')
d = ImageDraw.Draw(motion)
for i,(case,frame,label) in enumerate(samples):
    x,y=i%2*512,i//2*512
    d.text((x+12,y+8),f'{case} / frame {frame} / {label}',fill='white')
    motion.paste(Image.open(after/f'{case}/frames/{frame:04}.png'),(x,y+32))
motion.save(out/'motion.png')

# Fixed native-area crops enlarged 3x; no sprite reconstruction or recoloring.
ghoul = Image.new('RGB',(6*240,560),'#101724')
d = ImageDraw.Draw(ghoul)
for i,frame in enumerate([20,28,204,212,220,228,180,300,268,276,284,260]):
    oam=(after/f'state2/dumps/{frame-2:04}.oam').read_bytes()
    sprites=[(x,y) for y,t,a,x in [oam[k:k+4] for k in range(0,256,4)] if y<239 and a&3==1 and 0x94<=t<=0xab]
    assert sprites,frame
    cx=round((min(x for x,y in sprites)+max(x for x,y in sprites)+8))
    cy=round((min(y for x,y in sprites)+max(y for x,y in sprites)+10))
    x,y=i%6*240,i//6*280
    d.text((x+8,y+8),f'state2 / {frame} / 3x crop',fill='white')
    crop=Image.open(after/f'state2/frames/{frame:04}.png').crop((cx-40,cy-36,cx+40,cy+36))
    ghoul.paste(crop.resize((240,216),Image.Resampling.NEAREST),(x,y+40))
ghoul.save(out/'ghoul_live_poses.png')
