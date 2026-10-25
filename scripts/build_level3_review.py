"""0.11.1: spinning blade-ring, flame shots, insect and continuous bark surfaces."""
from pathlib import Path
import json,re,hashlib
import numpy as np
from PIL import Image,ImageFilter
r=Path(__file__).resolve().parents[1];pack=r/'build/Holy_Diver_(Tr)';art=r/'art/level3_review';text=(pack/'hires.txt').read_text()
assert text.count('<img>')==41
atlas=Image.new('RGBA',(512,512));cache={};rules=[];conditions=[];backgrounds=[];records=[];poses=[]
empty=Image.new('RGBA',(16,16))
def register(im,size):
 im=im.convert('RGBA').resize(size,Image.Resampling.LANCZOS);alpha=im.getchannel('A').point(lambda x:255 if x>=128 else 0);im=im.convert('RGB').quantize(colors=64).convert('RGBA');im.putalpha(alpha);return im

def cell(t,pal,im,kind,scope=''):
 key=hashlib.sha256(im.tobytes()).hexdigest()
 if key not in cache:
  n=len(cache);xy=(n%32*16,n//32*16);assert xy[1]<512;cache[key]=xy;atlas.paste(im,xy)
 x,y=cache[key];rules.append(('['+scope+']'if scope else'')+f'<tile>41,{t:04X},{pal},{x},{y},1,N');records.append(dict(tile=f'{t:04X}',palette=pal,xy=[x,y],kind=kind,scope=scope))
def sprite(name,im,rows,palette):
 im.save(art/(name+'.png'))
 for y,row in enumerate(rows):
  for x,t in enumerate(row):
   for pal in palette if isinstance(palette,list)else[palette]:cell(t,pal,im.crop((x*16,y*16,x*16+16,y*16+16)),name)
 poses.append(dict(name=name,rows=rows,palette=palette,size=list(im.size)))
# New spinner: full 24x24-native footprint for each native turn phase.
source=Image.open(r/'art/generated/level3_spinner_generated.png').convert('RGBA')
raw=source.crop((0,0,source.width//3,source.height));raw=raw.crop(raw.getchannel('A').point(lambda x:255 if x>=128 else 0).getbbox())
base=Image.new('RGBA',(48,48));base.paste(register(raw,(44,44)),(2,2))
for i in range(3):
 # Rotate one coherent painted body through the native three-phase cadence.
 im=register(base.rotate(-40*i,resample=Image.Resampling.BICUBIC),(48,48))
 sprite(f'spinner_{i}',im,[[0x695+i*9+y*3+x for x in range(3)]for y in range(3)],['FF002630','FF162631'])
# B6/B7 and B8/B9 are independent shots, not body/emergence tiles.
source=Image.open(r/'art/boss1/boss_fireball_registered.png').convert('RGBA')
for i in range(2):
 im=Image.new('RGBA',(32,16));im.paste(register(source,(30-i*4,16)),(1+i*2,0))
 sprite(f'ember_shot_{i}',im,[[0x6b6+i*2,0x6b7+i*2]],'FF172737')
# Align both wing frames in a common source canvas, preserving the centered body.
source=Image.open(r/'art/generated/level3_insect_generated.png').convert('RGBA');half=source.width//2
raws=[source.crop((i*half,0,(i+1)*half,source.height))for i in range(2)]
boxes=[im.getchannel('A').point(lambda x:255 if x>=128 else 0).getbbox()for im in raws];box=(min(b[0]for b in boxes),min(b[1]for b in boxes),max(b[2]for b in boxes),max(b[3]for b in boxes))
for i,raw in enumerate(raws):
 im=Image.new('RGBA',(32,32));im.paste(register(raw.crop(box),(32,24)),(0,4))
 sprite(f'insect_{i}',im,[[0x6e7+i*4+y*2+x for x in range(2)]for y in range(2)],['FF162631','FF002630'])
# Paint large continuous bark through the exact measured native wood mask.
# Native branches and terrain remain tile-bound and unchanged.
geometry=json.loads((art/'wood_geometry.json').read_text());old=json.loads((r/'art/level3_opening/registration.json').read_text())
bark=Image.open(r/'art/generated/level3_bark_review_generated.png').convert('RGB').resize((512,512),Image.Resampling.LANCZOS)
a=np.array(bark).astype(float)
for axis in [0,1]:
 a=np.swapaxes(a,0,axis);edge=(a[0]+a[-1])/2
 for n in range(12):w=(1-n/12)**2;a[n]=a[n]*(1-w)+edge*w;a[-1-n]=a[-1-n]*(1-w)+edge*w
 a=np.swapaxes(a,0,axis)
bark=Image.fromarray(a.astype('uint8'))
for name,g in geometry.items():
 size=tuple(v*2 for v in g['size']);mask=Image.new('L',size)
 for x,y,t in g['cells']:
  ma=Image.fromarray(np.array(old['terrain_masks'][f'{name}:{t}:0F091929'],dtype='uint8'));mask.paste(ma,(x*16,y*16))
 surface=Image.new('RGB',size)
 for y in range(0,size[1],512):
  for x in range(0,size[0],512):surface.paste(bark,(x,y))
 eroded=mask;distance=np.zeros((size[1],size[0]),dtype=float)
 for n in range(12):distance+=(np.array(eroded)>0);eroded=eroded.filter(ImageFilter.MinFilter(3))
 rgb=np.array(surface).astype(float);rgb*= (.46+.54*np.minimum(distance/12,1))[:,:,None]
 surface=Image.fromarray(rgb.astype('uint8')).convert('RGBA');surface.putalpha(mask)
 asset=f'Stage3_{name.title()}_Wood.png';surface.save(pack/asset);surface.save(art/asset)
 scope=f'l3_{name}Room&l3_{name}Lo&l3_{name}Hi'
 for t in sorted({int(t,16)for x,y,t in g['cells']}):cell(t,'0F091929',empty,'wood supplied by continuous native-aligned surface',scope)
 # Use the existing view guards so fades/menus never expose a full-bright overlay.
 guards=[line.split(',')[0][11:]for line in text.splitlines()if line.startswith(f'<condition>l3_{name}View_')]
 if name=='forest':
  conditions+=['<condition>l3reviewForestPage0,memoryCheckConstant,0061,<,02','<condition>l3reviewForestPage1,memoryCheckConstant,0061,>=,02']
  for guard in guards:
   for page in range(2):backgrounds.append(f'[{scope}&{guard}&l3reviewForestPage{page}]<background>{asset},1,1,0,12,{page*512},0')
 else:
  for guard in guards:backgrounds.append(f'[{scope}&{guard}]<background>{asset},1,0,1,12,0,0')
def block(name,items):return '# BEGIN LEVEL3_REVIEW '+name+'\n'+'\n'.join(items)+'\n# END LEVEL3_REVIEW '+name+'\n'
end=text.index('\n',text.rfind('<img>'))+1;text=text[:end]+block('IMAGES',['<img>Stage3_Review_Tiles_2x.png'])+text[end:]
lines=text.splitlines(keepends=True);first=next(i for i,l in enumerate(lines)if '<tile>'in l or '<background>'in l);lines[first:first]=[block('CONDITIONS',conditions),block('MAPPINGS',rules+backgrounds)]
(pack/'hires.txt').write_text(''.join(lines));atlas.save(pack/'Stage3_Review_Tiles_2x.png');atlas.save(art/'Stage3_Review_Tiles_2x.png')
(art/'poses.json').write_text(json.dumps(poses,indent=2)+'\n');(art/'registration.json').write_text(json.dumps(dict(tile_rules=len(rules),conditions=len(conditions),background_rules=len(backgrounds),mappings=records,atlas_cells=len(cache)),indent=2)+'\n')
print('Level 3 review:',len(rules),'tile rules;',len(backgrounds),'continuous wood view guards.')
