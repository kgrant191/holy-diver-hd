"""0.11.2: actual round enemy shot, boot collectible and solid branch surfaces."""
from pathlib import Path
import hashlib,json,re
import numpy as np
from PIL import Image

r=Path(__file__).resolve().parents[1]
pack=r/'build/Holy_Diver_(Tr)';art=r/'art/level3_detail';art.mkdir(exist_ok=True)
text=(pack/'hires.txt').read_text();assert text.count('<img>')==42
atlas=Image.new('RGBA',(256,64));rules=[];records=[];cells={}
def register(im,size):
 im=im.convert('RGBA').resize(size,Image.Resampling.LANCZOS)
 alpha=im.getchannel('A').point(lambda v:255 if v>=128 else 0)
 im=im.convert('RGB').quantize(colors=64).convert('RGBA');im.putalpha(alpha);return im
def cell(t,pal,im,kind,scope=''):
 n=len(records);x,y=n%16*16,n//16*16;atlas.paste(im,(x,y));cells[t]=im
 rules.append(('['+scope+']'if scope else '')+f'<tile>42,{t:04X},{pal},{x},{y},1,N')
 records.append(dict(tile=f'{t:04X}',palette=pal,xy=[x,y],kind=kind,scope=scope))
# Reuse the exact approved small fireball, including its 12x12 placement.
shot_rule=next(l for l in text.splitlines()if '<tile>'in l and l.split('<tile>')[1].split(',')[1:3]==['06D0','FF301116'])
f=shot_rule.split('<tile>')[1].split(',');images=[l[5:]for l in text.splitlines()if l.startswith('<img>')]
x,y=int(f[3]),int(f[4]);shot=Image.open(pack/images[int(f[0])]).convert('RGBA').crop((x,y,x+16,y+16))
shot.save(art/'round_shot.png');cell(0x694,'FF301116',shot,'round_shot')
# One complete boot registration prevents seams across the four native cells.
raw=Image.open(r/'art/generated/level3_boot_generated.png').convert('RGBA')
raw=raw.crop(raw.getchannel('A').point(lambda v:255 if v>=128 else 0).getbbox())
boot=Image.new('RGBA',(32,32));boot.paste(register(raw,(28,30)),(2,1));boot.save(art/'boot.png')
for yy in range(2):
 for xx in range(2):cell(0x68a+yy*2+xx,'FF301525',boot.crop((xx*16,yy*16,xx*16+16,yy*16+16)),'boot')
# Register a complete two-row branch, never the old single-row strip twice.
old=json.loads((r/'art/level3_opening/registration.json').read_text())['terrain_masks']
raw=Image.open(r/'art/generated/level3_branch_generated.png').convert('RGBA')
raw=raw.crop(raw.getchannel('A').point(lambda v:255 if v>=128 else 0).getbbox())
src=np.array(raw.resize((64,48),Image.Resampling.LANCZOS));paint=np.zeros((32,64,4),dtype=np.uint8)
layout=[[0x768,0x769,0x76c,0x76e],[0x76a,0x76b,0x76f,0x770]]
mask=np.zeros((32,64),dtype=np.uint8)
for yy,row in enumerate(layout):
 for xx,t in enumerate(row):mask[yy*16:yy*16+16,xx*16:xx*16+16]=old[f'tree:{t:04X}:0F091929']
# Resample each painted column into the measured native branch envelope.
# This fills the wood body without ever turning transparent RGB black opaque.
for x in range(64):
 sy=np.flatnonzero(src[:,x,3]>=128);dy=np.flatnonzero(mask[:,x])
 if not len(dy):continue
 assert len(sy)
 indices=np.rint(np.linspace(sy[0],sy[-1],dy[-1]-dy[0]+1)).astype(int)
 paint[dy[0]:dy[-1]+1,x,:3]=src[indices,x,:3]
paint[:,:,3]=mask
branch=Image.fromarray(paint);branch.save(art/'branch_short.png')
locations={t:(xx,yy)for yy,row in enumerate(layout)for xx,t in enumerate(row)};locations[0x76d]=(2,1)
scope='l3_treeRoom&l3_treeLo&l3_treeHi'
for t,(xx,yy)in sorted(locations.items()):
 im=branch.crop((xx*16,yy*16,xx*16+16,yy*16+16))
 # Lower middle variant uses the same bark with its own native outline.
 ma=np.array(old[f'tree:{t:04X}:0F091929'],dtype=np.uint8)
 arr=np.array(im);valid=np.argwhere(arr[:,:,3]>0)
 for y,x in np.argwhere((ma>0)&(arr[:,:,3]==0)):
  sy,sx=valid[np.argmin(np.sum((valid-[y,x])**2,axis=1))];arr[y,x,:3]=arr[sy,sx,:3]
 arr[:,:,3]=ma;im=Image.fromarray(arr);cell(t,'0F091929',im,'branch',scope)
long=Image.new('RGBA',(96,32))
for yy,row in enumerate([[0x768,0x769,0x76c,0x769,0x76c,0x76e],[0x76a,0x76b,0x76d,0x76b,0x76f,0x770]]):
 for xx,t in enumerate(row):long.paste(cells[t],(xx*16,yy*16))
long.save(art/'branch_long.png')
def block(name,items):return '# BEGIN LEVEL3_DETAIL '+name+'\n'+'\n'.join(items)+'\n# END LEVEL3_DETAIL '+name+'\n'
end=text.index('\n',text.rfind('<img>'))+1;text=text[:end]+block('IMAGES',['<img>Stage3_Detail_Tiles_2x.png'])+text[end:]
lines=text.splitlines(keepends=True);first=next(i for i,l in enumerate(lines)if '<tile>'in l or '<background>'in l)
lines[first:first]=[block('MAPPINGS',rules)]
(pack/'hires.txt').write_text(''.join(lines));atlas.save(pack/'Stage3_Detail_Tiles_2x.png');atlas.save(art/'Stage3_Detail_Tiles_2x.png')
(art/'registration.json').write_text(json.dumps(dict(tile_rules=len(rules),mappings=records,branch_alpha_preserved=True,projectile_source_rule=shot_rule,native_gameplay_modified=False),indent=2)+'\n')
print('Level 3 details:',len(rules),'scoped registrations; original branch contours preserved.')
