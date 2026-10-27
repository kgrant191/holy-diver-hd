"""Isolated Palace ceiling, scrolling-background and serpent-palette repair."""
from pathlib import Path
import hashlib,json,re
import numpy as np
from PIL import Image
from prepare_level5 import reg
R=Path(__file__).resolve().parents[1];P=R/'build/Holy_Diver_(Tr)';A=R/'art/level5_repair';G=R/'art/generated'
text=(P/'hires.txt').read_text();prior=json.loads((R/'evidence/0.21.0-pack-sha256.json').read_text());assert hashlib.sha256(text.encode()).hexdigest()==prior['hires.txt']
old=json.loads((R/'art/level5/registration.json').read_text());inv=json.loads((A/'inventory.json').read_text());patterns={int(k,16):bytes.fromhex(v)for k,v in json.loads((A/'native_patterns.json').read_text()).items()}
images=[l[5:]for l in text.splitlines()if l.startswith('<img>')];index=len(images);assert index==58
atlas=Image.new('RGBA',(128,128));cache={};rules=[];conditions=[];backgrounds=[];records=[];clones=[]
scopes={**old['scopes'],'888E':'palaceRepair888EMode&palaceRepair888ELo&palaceRepair888EHi'}
for suffix,addr,val in [('Mode',0x72,0x10),('Lo',0x78,0x8e),('Hi',0x79,0x88)]:conditions.append(f'<condition>palaceRepair888E{suffix},memoryCheckConstant,{addr:04X},==,{val:02X}')
def cell(line):
 f=line.split('<tile>')[1].split(',');x,y=map(int,f[3:5]);return Image.open(P/images[int(f[0])]).convert('RGBA').crop((x,y,x+16,y+16))
def emit(t,pal,im,scope,kind,source_rule=None):
 h=hashlib.sha256(im.tobytes()).hexdigest()
 if h not in cache:
  i=len(cache);xy=(i%8*16,i//8*16);assert xy[1]<128;cache[h]=xy;atlas.paste(im,xy)
 x,y=cache[h];rule=f'[{scope}]<tile>{index},{t:04X},{pal},{x},{y},1,N';rules.append(rule);records.append(dict(tile=f'{t:04X}',palette=pal,scope=scope,kind=kind,xy=[x,y],source_rule=source_rule,rule=rule))
def hull(t):
 b=patterns[t];a=np.array([[255 if ((b[y]|b[y+8])>>(7-x))&1 else 0 for x in range(8)]for y in range(8)],dtype=np.uint8)
 for y in range(8):
  xs=np.flatnonzero(a[y]);
  if len(xs):a[y,xs[0]:xs[-1]+1]=255
 for x in range(8):
  ys=np.flatnonzero(a[:,x]);
  if len(ys):a[ys[0]:ys[-1]+1,x]=255
 return Image.fromarray(a).resize((16,16),Image.Resampling.NEAREST)
# Only the cavern roof changes material. Every original alpha/bound/identity
# stays exact, including the higher-priority closed interior roof variants.
slime=reg(Image.open(G/'palace_slime.png'),(64,64),128).crop((16,16,48,48));slime.save(A/'slime_ceiling_material.png')
for m in old['mappings']:
 t=int(m['tile'],16)
 if (t&255)not in [1,2,3,4,0x1d,0x1e,0x1f,0x20]or not m['scope'].startswith(scopes['850A']):continue
 source=cell(m['rule']);j=(t&255)-(1 if(t&255)<5 else 0x1d);x,y=j%2*16,j//2*16;im=slime.crop((x,y,x+16,y+16));im.putalpha(source.getchannel('A'));emit(t,m['palette'],im,m['scope'],'slime cavern ceiling',m['rule'])
# Add the missing stair-hall cells, then reuse the same material in its next
# recorded hall. Existing native masks and opaque tread pixels remain exact.
raw=Image.open(G/'screen2_5_stair_tread_generated.png').convert('RGBA')
material=reg(raw,(64,64));face=reg(raw.crop((400,380,1800,525)),(64,64))
# The original registration included transparent padding around the tread.
# Its RGB turned black when native masks made it solid. Fill only that padding
# from the same source's opaque stone face; retain all existing tread artwork.
m=np.array(material);fill=np.array(face);padding=m[:,:,3]==0;m[padding,:3]=fill[padding,:3];m[:,:,3]=255;material=Image.fromarray(m);material.save(A/'stair_material.png')
empty=Image.new('RGBA',(16,16))
for room,pals in inv['visible_backgrounds'].items():
 for pal,ts in pals.items():
  assert pal in ['0F001030','0F0F0717']
  for key in ts:
   t=int(key,16)
   if room=='8816'and pal=='0F0F0717'and any(m['tile']==key and m['palette']==pal and m['scope']==scopes[room]for m in old['mappings']):continue
   if pal=='0F0F0717':im=empty;kind='distant hall wall reveal'
   else:
    im=material.crop((t%4*16,t//4%4*16,t%4*16+16,t//4%4*16+16));im.putalpha(hull(t));kind='stair hall stone'
   for bank in [0,0x200]:emit(t+bank,pal,im,scopes[room],kind)
 for key,pal in inv['view_guards'][room]:
  assert pal in ['0F001030','0F0F0717']
  for bank in [0,0x200]:
   t=int(key,16)+bank;name=f'palaceRepairView{room}_{t:04X}_{pal}';conditions.append(f'<condition>{name},tileAtPosition,128,16,{t:04X},{pal}')
   backgrounds.append(f'[{scopes[room]}&{name}]<background>Demonic_Palace_Interior.png,1,0,0,1,0,0')
# Same native head and independent segment cells, another normal room palette.
for source in text.splitlines():
 m=re.fullmatch(r'<tile>57,(10(?:D[B-F]|E[0-7])),FF0B2B30,(.*)',source)
 if not m:continue
 rule=f'[{scopes["8816"]}]<tile>57,{m[1]},FF110130,{m[2]}';rules.append(rule);clones.append(dict(source_rule=source,rule=rule,kind='existing complete serpent in climb palette'))
assert len(clones)==13

def block(name,lines):return '# BEGIN PALACE_REPAIR '+name+'\n'+'\n'.join(lines)+'\n# END PALACE_REPAIR '+name+'\n'
end=text.index('\n',text.rfind('<img>'))+1;text=text[:end]+block('IMAGES',['<img>Demonic_Palace_Repair_2x.png'])+text[end:]
start=text.index('# BEGIN DEMONIC_PALACE MAPPINGS');text=text[:start]+block('CONDITIONS',conditions)+block('MAPPINGS',rules+backgrounds)+text[start:]
(P/'hires.txt').write_text(text);atlas.save(P/'Demonic_Palace_Repair_2x.png');atlas.save(A/'Demonic_Palace_Repair_2x.png')
(A/'registration.json').write_text(json.dumps(dict(atlas_index=index,atlas_cells=len(cache),mappings=records,clones=clones,backgrounds=backgrounds,conditions=conditions,scopes=scopes),indent=2)+'\n');print('Palace repair:',len(rules),'tiles,',len(backgrounds),'background guards,',len(cache),'atlas cells')
