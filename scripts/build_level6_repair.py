"""Reuse citadel stone for the upper ceiling and accepted Level 6 1-ups."""
from pathlib import Path
import hashlib,json,io
from PIL import Image
import numpy as np

R=Path(__file__).resolve().parents[1];P=R/'build/Holy_Diver_(Tr)';A=R/'art/level6_repair';A.mkdir(exist_ok=True)
previous=json.loads((R/'evidence/0.25.0-pack-sha256.json').read_text());text=(P/'hires.txt').read_text()
assert hashlib.sha256(text.encode()).hexdigest()==previous['hires.txt']
lines=text.splitlines();index=sum(l.startswith('<img>')for l in lines);assert index==63
patterns={int(k,16):bytes.fromhex(v)for k,v in json.loads((R/'art/level6_opening/native_patterns.json').read_text()).items()}
def hull(t):
 b=patterns[t];a=np.array([[255 if(b[y]|b[y+8])>>(7-x)&1 else 0 for x in range(8)]for y in range(8)],dtype=np.uint8)
 for y in range(8):
  xs=np.flatnonzero(a[y])
  if len(xs):a[y,xs[0]:xs[-1]+1]=255
 for x in range(8):
  ys=np.flatnonzero(a[:,x])
  if len(ys):a[ys[0]:ys[-1]+1,x]=255
 return Image.fromarray(a).resize((16,16),Image.Resampling.NEAREST)
def save(im,path):
 b=io.BytesIO();im.save(b,format='PNG');raw=b.getvalue();path.write_bytes(raw);assert path.read_bytes()==raw
unit=Image.open(R/'art/level6_opening/rock_material.png').convert('RGBA').crop((0,16,32,48))
layout=[[0x17b4,0x17b5],[0x17b6,0x17b7]];mask=Image.new('L',(32,32))
for y,row in enumerate(layout):
 for x,t in enumerate(row):mask.paste(hull(t),(16*x,16*y))
unit.putalpha(mask);save(unit,A/'ceiling_unit.png');save(unit,P/'Final_Citadel_Repair_2x.png')
conditions=[];rules=[];mappings=[];clones=[];scopes={}
for room,mode in [('9A8B',4),('9BB7',16),('9CA7',12)]:
 terms=[]
 for label,address,value in [('Mode',0x72,mode),('Lo',0x78,int(room,16)&255),('Hi',0x79,int(room,16)>>8)]:
  name=f'citadelRepair{room}{label}';conditions.append(f'<condition>{name},memoryCheckConstant,{address:04X},==,{value:02X}');terms.append(name)
 scope='&'.join(terms);scopes[room]=scope
 for phase in ['0F','30','31']:
  for suffix in ['061636','072830']:
   pal=phase+suffix
   for y,row in enumerate(layout):
    for x,t in enumerate(row):
     rule=f'[{scope}]<tile>{index},{t:04X},{pal},{x*16},{y*16},1,N';rules.append(rule)
     mappings.append(dict(tile=f'{t:04X}',palette=pal,xy=[x*16,y*16],scope=scope,rule=rule))
for pal,source_pal in [('FF300036','FF300036'),('FF221136','FF221136'),('FF190927','FF300036')]:
 for offset in [0x4e,0x4f]:
  source=0x200+offset;target=0x1600+offset;assert patterns[source]==patterns[target]
  found=[l for l in lines if l.startswith(f'<tile>29,{source:04X},{source_pal},')];assert len(found)==1
  old=found[0];f=old[6:].split(',');f[1]=f'{target:04X}';f[2]=pal;rule='<tile>'+','.join(f)
  assert not any(f',{target:04X},{pal},'in l and '<tile>'in l for l in lines)
  clones.append(dict(source_rule=old,rule=rule,source_tile=f'{source:04X}',tile=f'{target:04X}',palette=pal,source_palette=source_pal))
def block(section,entries):return '# BEGIN LEVEL6_REPAIR '+section+'\n'+'\n'.join(entries)+'\n# END LEVEL6_REPAIR '+section+'\n'
anchor='# END LEVEL6_OPENING IMAGES\n';assert text.count(anchor)==1;pos=text.index(anchor)+len(anchor)
text=text[:pos]+block('IMAGES',['<img>Final_Citadel_Repair_2x.png'])+block('CONDITIONS',conditions)+block('MAPPINGS',rules)+text[pos:]
text+=block('ALIASES',[e['rule']for e in clones]);(P/'hires.txt').write_text(text)
(A/'registration.json').write_text(json.dumps(dict(atlas_index=index,layout=layout,scopes=scopes,conditions=conditions,mappings=mappings,clones=clones,ceiling_source='art/level6_opening/rock_material.png',source_crop=[0,16,32,48],new_generated_art=False,native_gameplay_modified=False),indent=2)+'\n')
print('Level 6 repair:',len(rules),'ceiling rules;',len(clones),'1-up aliases; existing artwork preserved')
