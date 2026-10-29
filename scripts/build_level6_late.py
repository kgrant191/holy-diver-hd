"""Extend accepted Level 6 artwork through the green reliquary and descent."""
from pathlib import Path
import hashlib,json,re
import numpy as np
from PIL import Image
from verify_level6_opening_rules import native_hull
R=Path(__file__).resolve().parents[1];P=R/'build/Holy_Diver_(Tr)';A=R/'art/level6_late'
text=(P/'hires.txt').read_text();prior=json.loads((R/'evidence/0.27.0-pack-sha256.json').read_text());assert hashlib.sha256(text.encode()).hexdigest()==prior['hires.txt']
lines=text.splitlines();images=[l[5:]for l in lines if l.startswith('<img>')];index=len(images);assert index==66
old=json.loads((R/'art/level6_variety/registration.json').read_text());opening=json.loads((R/'art/level6_opening/registration.json').read_text());inv=json.loads((A/'inventory.json').read_text())
patterns={int(k,16):bytes.fromhex(v)for k,v in json.loads((R/'art/level6_opening/native_patterns.json').read_text()).items()}
conditions=[];rules=[];clones=[];records=[];backgrounds=[];scopes={};atlas=Image.new('RGBA',(32,48))
for room,mode in [('A20B',0x10),('A2FB',4)]:
 names=[]
 for suffix,addr,value in [('Mode',0x72,mode),('Lo',0x78,int(room,16)&255),('Hi',0x79,int(room,16)>>8)]:
  name='citadelLate'+room+suffix;conditions.append(f'<condition>{name},memoryCheckConstant,{addr:04X},==,{value:02X}');names.append(name)
 scopes[room]='&'.join(names)
def clone(source,rule,kind):
 a=source.split('<tile>')[1].split(',');b=rule.split('<tile>')[1].split(',');assert patterns[int(a[1],16)]==patterns[int(b[1],16)]
 rules.append(rule);clones.append(dict(source_rule=source,rule=rule,kind=kind))
def emit(t,pal,xy,scope,kind):
 x,y=xy;rule=f'[{scope}]<tile>{index},{t:04X},{pal},{x},{y},1,N';rules.append(rule);records.append(dict(tile=f'{t:04X}',palette=pal,xy=xy,scope=scope,kind=kind,rule=rule))
# Measured native 2x2 floating ledge, registered whole before slicing.
layout=[[0x17f6,0x17f7],[0x17f8,0x17f9]];stone=Image.open(R/'art/level6_variety/green_material.png').convert('RGBA');ledge=stone.crop((0,0,32,32));mask=Image.new('L',(32,32))
for y,row in enumerate(layout):
 for x,t in enumerate(row):mask.paste(Image.fromarray(native_hull(patterns[t]).astype(np.uint8)*255),(x*16,y*16))
ledge.putalpha(mask);ledge.save(A/'floating_ledge.png');atlas.paste(ledge,(0,0))
# Reuse the complete ordered A0DF tile layer: green stone, ornaments,
# specific actor poses and both sentinel hit palettes. Global player aliases
# already cover bank 1800. Earlier room rules stay byte-identical.
donor=old['scopes']['A0DF'];donors=[l for l in lines if l.startswith('['+donor)and'<tile>'in l]
for room,scope in scopes.items():
 # First cover the shaft's new native green palette with the accepted green RGB.
 for line in donors:
  f=line.split('<tile>')[1].split(',')
  if f[2][2:]=='0B1B3B':
   new=line.replace(donor,scope,1).replace(','+f[2]+',',','+f[2][:2]+'0A1A39,',1);clone(line,new,'shaft green palette')
 # Full original priority, not a broad unconditional sprite fallback.
 for line in donors:clone(line,line.replace(donor,scope,1),'complete accepted room rule')
 for phase in ['0F','30','31']:
  for suffix in ['0B1B3B','0A1A39','072830']:
   for y,row in enumerate(layout):
    for x,t in enumerate(row):
     for shift in [0,0x200]:emit(t+shift,phase+suffix,[x*16,y*16],scope,'whole floating ledge')
 # Native decorative green skull wall: only this measured palette is cleared.
 wall=sorted(int(t,16)for t in inv['visible_backgrounds']['A20B']['0F0A1A29'])
 for phase in ['0F','30','31']:
  for suffix in ['0A1A29','172737']:
   for t in wall:
    for shift in [0,0x200]:emit(t+shift,phase+suffix,[0,32],scope,'distant green wall')
 # Returning eye and its two-cell falling tear reuse exact approved atlas 34.
 for j in range(6):
  pal='FF060C30'if j<4 else'FF301116';src=0x2d8+j;dst=0x18f3+j
  source=next(l for l in lines if l.startswith(f'<tile>34,{src:04X},{pal},'))
  f=source.split('<tile>')[1].split(',');f[1]=f'{dst:04X}';clone(source,f'[{scope}]<tile>'+','.join(f),'returning eye and tear')
# Whole rendered-bank families survive scrolling, pause and 30/31 phases.
# Death/card-only palettes 213029/041424 are deliberately not room guards.
guard_palettes=['0B1B3B','011121','0A1A29','0A1A39','072830','172737','081030','1B2B3B']
styles={'A20B':('Reliquary','level6_reliquary'),'A2FB':('Green_Shaft','level6_green_shaft')}
for room,(style,source)in styles.items():
 im=Image.open(R/f'art/generated/{source}.png').convert('RGBA').resize((512,480),Image.Resampling.LANCZOS);im.save(P/f'Final_Citadel_{style}.png');flash=im.copy();flash.putalpha(176);flash.save(P/f'Final_Citadel_{style}_Flash.png')
 for phase in ['0F','30','31']:
  for suffix in guard_palettes:
   pal=phase+suffix
   for base in [0x1700,0x1900]:
    for t in range(base,base+256):
     name=f'citadelLateView{room}_{t:04X}_{pal}';conditions.append(f'<condition>{name},tileAtPosition,128,16,{t:04X},{pal}')
     image=f'Final_Citadel_{style}'+('_Flash'if phase!='0F'else'')+'.png';backgrounds.append(f'[{scopes[room]}&{name}]<background>{image},1,0,0,1,0,0')
def block(part,entries):return '# BEGIN LEVEL6_LATE '+part+'\n'+'\n'.join(entries)+'\n# END LEVEL6_LATE '+part+'\n'
anchor='# END LEVEL6_VARIETY IMAGES\n';at=text.index(anchor)+len(anchor);text=text[:at]+block('IMAGES',['<img>Final_Citadel_Late_2x.png'])+block('CONDITIONS',conditions)+text[at:]
anchor='# END LEVEL6_NEXT CONDITIONS\n';at=text.index(anchor)+len(anchor);text=text[:at]+block('MAPPINGS',rules+backgrounds)+text[at:]
(P/'hires.txt').write_text(text);atlas.save(P/'Final_Citadel_Late_2x.png');atlas.save(A/'Final_Citadel_Late_2x.png')
(A/'registration.json').write_text(json.dumps(dict(atlas_index=index,scopes=scopes,conditions=conditions,mappings=records,clones=clones,backgrounds=backgrounds,guard_palettes=guard_palettes,styles=styles,ledge_layout=layout,green_wall=wall),indent=2)+'\n')
print('Level 6 late:',len(rules),'tile rules;',len(backgrounds),'backgrounds; 4 new ledge cells; all accepted artwork unchanged')
