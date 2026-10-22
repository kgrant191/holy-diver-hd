"""Register the measured upward-casting pose and vertical projectile sprites.

Only the raised-hand neighborhood may select the new full Randy pose. Existing
horizontal, walking, crouching and jumping assets and rules remain unchanged.
"""
from pathlib import Path
import json,re
import numpy as np
from PIL import Image,ImageDraw

root=Path(__file__).resolve().parents[1]
art=root/'art';out=root/'build/Holy_Diver_(Tr)'
pose=json.loads((art/'upward_pose.json').read_text())['tiles']
hero=Image.open(art/'generated/randy_upward_generated.png').convert('RGBA')
atlas=Image.new('RGBA',(64,80));conditions=[];rules=[]
scope=['gameplay','entranceLowerA','entranceLowerB','entrancePillar','litPalette']
coverage=Image.new('L',(32,80));draw=ImageDraw.Draw(coverage)
for x,y,t in pose:draw.rectangle((x*2,y*2,x*2+15,y*2+15),fill=255)

def registered(cell,size,colors,threshold=135):
    bb=cell.getchannel('A').point(lambda x:255 if x>=80 else 0).getbbox()
    assert bb
    cell=cell.crop(bb).resize(size,Image.Resampling.LANCZOS)
    alpha=cell.getchannel('A').point(lambda x:255 if x>=threshold else 0)
    result=cell.convert('RGB').quantize(colors=colors,method=Image.Quantize.MEDIANCUT).convert('RGBA')
    result.putalpha(alpha)
    return result

for mode,palette in enumerate(['FF300036','FF221136']):
    cell=hero.crop((round(mode*hero.width/2),0,round((mode+1)*hero.width/2),hero.height))
    sprite=Image.new('RGBA',(32,80))
    sprite.alpha_composite(registered(cell,(32,76),40),(0,4))
    arr=np.array(sprite);clipped=int(((arr[:,:,3]>0)&(np.array(coverage)==0)).sum())
    assert clipped==0,('Artwork extends outside native sprite coverage',mode,clipped)
    sprite.save(art/f'randy_upward_{mode}.png');atlas.alpha_composite(sprite,(mode*32,0))
    for index,(x,y,t) in enumerate(pose):
        # Tile $40 is exclusive to upward casting. For $40 itself, use $41 below.
        anchor=(8,8,0x41) if t==0x40 else (8,0,0x40)
        name=f'randyUp{mode}_{index}'
        conditions.append(f'<condition>{name},spriteNearby,{anchor[0]-x},{anchor[1]-y},{anchor[2]:02X},{palette}')
        prefix='['+'&'.join(scope+[name])+']'
        rules.append(prefix+f'<tile>22,{t:02X},{palette},{mode*32+x*2},{y*2},1,N')
atlas.save(art/'Randy_Upward_2x.png');atlas.save(out/'Randy_Upward_2x.png')

src=Image.open(art/'generated/weapons_upward_generated.png').convert('RGBA')
bolts=Image.new('RGBA',(64,32))
for row in range(2):
    for col in range(4):
        cell=src.crop((round(col*src.width/4),round(row*src.height/2),round((col+1)*src.width/4),round((row+1)*src.height/2)))
        bolts.alpha_composite(registered(cell,(12,16),18,100),(col*16+2,row*16))
    for phase in [3,2,1,0]:
        terms=scope+(['twinFireEquipped'] if row else ['!twinFireEquipped'])
        if phase:terms+=[f'firePhase{phase}']
        rules.append('['+'&'.join(terms)+f']<tile>23,44,FF301116,{phase*16},{row*16},1,N')
bolts.save(art/'Weapon_Upward_2x.png');bolts.save(out/'Weapon_Upward_2x.png')

# Retain original atlas indices, but declare all atlases before any new rules.
base=(out/'hires.txt').read_text()
images=re.findall(r'^<img>.*$',base,re.M)
assert len(images)==22
base=re.sub(r'^<img>.*\n','',base,flags=re.M)
images+=['<img>Randy_Upward_2x.png','<img>Weapon_Upward_2x.png']
pos=base.index('\n',base.index('<scale>'))+1
base=base[:pos]+'\n'.join(images)+'\n'+base[pos:]
# Place all condition definitions before rules, then prioritize the new pose.
pos=base.index('<condition>randySig')
base=base[:pos]+'\n'.join(conditions)+'\n'+base[pos:]
late=[]
lines=base.splitlines()
for line in lines:
    if line.startswith('<condition>'):late.append(line)
lines=[line for line in lines if not line.startswith('<condition>')]
first_rule=next(i for i,line in enumerate(lines) if '<tile>' in line or '<background>' in line)
lines[first_rule:first_rule]=late+['# v11: upward pose and vertical fire; scoped to approved entrance.']+rules
(out/'hires.txt').write_text('\n'.join(lines)+'\n')
print(f'Upward: {len(conditions)} signatures, {len(rules)} rules; native 9-sprite pose.')
