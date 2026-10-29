"""Reversible blob/face visual revision; the original green orb stays intact."""
from pathlib import Path
import hashlib,json
import numpy as np
from PIL import Image
R=Path(__file__).resolve().parents[1];P=R/'build/Holy_Diver_(Tr)';A=R/'art/level6_enemy_revision'
text=(P/'hires.txt').read_text();prior=json.loads((R/'evidence/0.29.0-pack-sha256.json').read_text());assert hashlib.sha256(text.encode()).hexdigest()==prior['hires.txt']
old=json.loads((R/'art/level6_organic/registration.json').read_text());scope=old['scope'];index=sum(l.startswith('<img>')for l in text.splitlines());assert index==68
choice=json.loads((A/'choice.json').read_text())['green_enemy'];assert choice in ['blob','rock']
atlas=Image.new('RGBA',(128,128));layout=old['groups']['wall_face'];oldface=Image.open(R/'art/level6_organic/wall_face.png').convert('RGBA');material=Image.open(R/'art/level6_organic/material.png').convert('RGBA')
original=Image.open(R/'art/generated/level6_organic_head.png').convert('RGBA');raw=Image.open(R/'art/generated/level6_face_bonegray.png').convert('RGBA');assert original.size==raw.size
box=original.getchannel('A').point(lambda v:255 if v>=128 else 0).getbbox();im=raw.crop(box).resize(oldface.size,Image.Resampling.LANCZOS);under=material.crop((0,0,*oldface.size));under.alpha_composite(im)
cells={};coords={}
for y,row in enumerate(layout):
 for x,t in enumerate(row):
  if t in cells:continue
  cell=under.crop((16*x,16*y,16*x+16,16*y+16));cell.putalpha(oldface.crop((16*x,16*y,16*x+16,16*y+16)).getchannel('A'));cells[t]=cell;coords[t]=[16*x,16*y]
face=Image.new('RGBA',oldface.size)
for y,row in enumerate(layout):
 for x,t in enumerate(row):face.paste(cells[t],(16*x,16*y))
face.save(A/'wall_face.png');atlas.paste(face,(0,0))
raw=Image.open(R/'art/generated/level6_mucus_blob.png').convert('RGBA');poses=[]
for i in range(2):
 part=raw.crop((i*raw.width//2,0,(i+1)*raw.width//2,raw.height));box=part.getchannel('A').point(lambda v:255 if v>=160 else 0).getbbox();im=part.crop(box).resize((32,32),Image.Resampling.LANCZOS);alpha=np.array(im.getchannel('A'))>=160;im=im.convert('RGB').quantize(colors=48).convert('RGBA');im.putalpha(Image.fromarray(alpha.astype(np.uint8)*255));im.save(A/f'blob_{i}.png');atlas.paste(im,(48+i*32,0));poses.append(dict(name=f'blob_{i}',layout=old['poses'][i]['layout'],xy=[48+i*32,0],size=[32,32]))
rules=[];records=[]
for e in old['mappings']:
 t=int(e['tile'],16);xy=None;kind=None
 if e['kind']=='native organic terrain'and t in cells:xy=coords[t];kind='wall face color'
 if e['kind']=='whole orb'and choice=='blob':
  i=(t-0x1a9c)//4;j=(t-0x1a9c)%4;xy=[48+i*32+j%2*16,j//2*16];kind='mucus blob'
 if xy is not None:
  x,y=xy;rule=f'[{scope}]<tile>{index},{t:04X},{e["palette"]},{x},{y},1,N';rules.append(rule);records.append(dict(source_rule=e['rule'],rule=rule,tile=e['tile'],palette=e['palette'],xy=xy,kind=kind))
def block(part,entries):return '# BEGIN LEVEL6_ENEMY_REVISION '+part+'\n'+'\n'.join(entries)+'\n# END LEVEL6_ENEMY_REVISION '+part+'\n'
anchor='# END LEVEL6_ORGANIC IMAGES\n';at=text.index(anchor)+len(anchor);text=text[:at]+block('IMAGES',['<img>Final_Citadel_Enemy_Revision_2x.png'])+text[at:]
anchor='# END LEVEL6_ORGANIC CONDITIONS\n';at=text.index(anchor)+len(anchor);text=text[:at]+block('MAPPINGS',rules)+text[at:]
(P/'hires.txt').write_text(text);atlas.save(P/'Final_Citadel_Enemy_Revision_2x.png');atlas.save(A/'Final_Citadel_Enemy_Revision_2x.png')
(A/'registration.json').write_text(json.dumps(dict(atlas_index=index,scope=scope,choice=choice,mappings=records,face_layout=layout,poses=poses),indent=2)+'\n')
paths=['art/generated/level6_organic_orb.png','art/level6_organic/orb_0.png','art/level6_organic/orb_1.png','art/level6_organic/Final_Citadel_Organic_2x.png']
(A/'standby.json').write_text(json.dumps(dict(version='0.29.0',source_commit='e18e1db60c1c5c48ec428c67fd8bd2d868340d35',original_files={p:hashlib.sha256((R/p).read_bytes()).hexdigest()for p in paths},original_orb_rules=[e['rule']for e in old['mappings']if e['kind']=='whole orb'],restore='Set green_enemy to rock in choice.json and rebuild; face overrides remain. Original art and rules are retained byte-for-byte.'),indent=2)+'\n')
print('Level 6 enemy revision:',len(rules),'overrides; choice',choice,'; original orb retained')
