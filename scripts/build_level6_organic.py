"""Register the recorded crimson organic hall without changing native execution."""
from pathlib import Path
import hashlib,json,re
import numpy as np
from PIL import Image
from verify_level6_opening_rules import native_hull
R=Path(__file__).resolve().parents[1];P=R/'build/Holy_Diver_(Tr)';A=R/'art/level6_organic'
text=(P/'hires.txt').read_text();prior=json.loads((R/'evidence/0.28.0-pack-sha256.json').read_text());assert hashlib.sha256(text.encode()).hexdigest()==prior['hires.txt']
lines=text.splitlines();index=sum(l.startswith('<img>')for l in lines);assert index==67
patterns={int(k,16):bytes.fromhex(v)for k,v in json.loads((R/'art/level6_opening/native_patterns.json').read_text()).items()}
defs={l[11:].split(',')[0]:l[11:].split(',')for l in lines if l.startswith('<condition>')}
conditions=[];rules=[];tail=[];records=[];clones=[];copies={};cache={};backgrounds=[]
scope='organicMode&organicLo&organicHi'
for name,addr,val in [('organicMode',0x72,0x10),('organicLo',0x78,0xaf),('organicHi',0x79,0xa3)]:conditions.append(f'<condition>{name},memoryCheckConstant,{addr:04X},==,{val:02X}')
def dependency(term,shift=0):
 neg='!'if term.startswith('!')else'';name=term.lstrip('!')
 if name in ['hmirror','vmirror','bgpriority']:return term
 key=(name,shift)
 if key not in copies:
  d=defs[name].copy();new='organicReuse'+str(len(copies));copies[key]=new;d[0]=new;assert d[1]!='tileNearby'
  if d[1]=='spriteNearby'and shift and 0xa00<=int(d[4],16)<=0xa8d:
   src=int(d[4],16);assert patterns[src]==patterns[src+shift];d[4]=f'{src+shift:04X}'
  conditions.append('<condition>'+','.join(d))
 return neg+copies[key]
def clone(source,t,pal,kind,terms=(),shift=0,destination=None):
 f=source.split('<tile>')[1].split(',');assert patterns[int(f[1],16)]==patterns[t];f[1]=f'{t:04X}';f[2]=pal
 head='&'.join([scope]+[dependency(k,shift)for k in terms]);line=f'[{head}]<tile>'+','.join(f)
 (rules if destination is None else destination).append(line);clones.append(dict(source_rule=source,rule=line,kind=kind))
atlas=Image.new('RGBA',(256,256))
def emit(t,pal,im,kind):
 h=hashlib.sha256(im.tobytes()).hexdigest()
 if h not in cache:
  n=len(cache);xy=(n%16*16,n//16*16);assert xy[1]<256;cache[h]=xy;atlas.paste(im,xy)
 x,y=cache[h];line=f'[{scope}]<tile>{index},{t:04X},{pal},{x},{y},1,N';rules.append(line);records.append(dict(tile=f'{t:04X}',palette=pal,xy=[x,y],kind=kind,rule=line))
material=Image.open(R/'art/generated/level6_organic_material.png').convert('RGBA').resize((128,128),Image.Resampling.LANCZOS);material.save(A/'material.png')
groups={
 'body':[[0x1b01,0x1b46,0x1b5c,0x1b5d],[0x1b5e,0x1b5f,0x1b60,0x1b61]],
 'ceiling':[[0x1b62,0x1b63,0x1b64,0x1b65],[0x1bd0,0x1bcf,0x1bd3,0x1bd2],[0x1bce,0x1bcd,None,None]],
 'platform_top':[[0x1b94,0x1b93,0x1b94,0x1b93],[0x1b7d,0x1b7c,0x1b7b,0x1b7a]],
 'wall_face':[[0x1b90,0x1b8f,0x1b8e],[0x1b8d,0x1b8c,0x1b8b],[0x1b8a,0x1b89,0x1b88],[0x1b8d,0x1b87,0x1b86],[0x1b8a,0x1b85,0x1b84],[0x1b8d,0x1b83,0x1b82],[0x1b8a,0x1b81,0x1b80],[0x1b8d,0x1b7f,0x1b7e]]}
cells={}
for name,layout in groups.items():
 size=(len(layout[0])*16,len(layout)*16)
 if name=='wall_face':
  raw=Image.open(R/'art/generated/level6_organic_head.png').convert('RGBA');box=raw.getchannel('A').point(lambda v:255 if v>=128 else 0).getbbox();im=raw.crop(box).resize(size,Image.Resampling.LANCZOS)
  # The face is embedded in solid terrain: fill only translucent source padding
  # with the matching material, then apply the independently measured hull.
  under=material.crop((0,0,*size));under.alpha_composite(im);im=under
 else:im=material.crop((0,0,*size))
 for y,row in enumerate(layout):
  for x,t in enumerate(row):
   if t is None:continue
   if t not in cells:
    cell=im.crop((x*16,y*16,x*16+16,y*16+16));cell.putalpha(Image.fromarray(native_hull(patterns[t]).astype(np.uint8)*255));cells[t]=cell
 # Shared native identities must remain the same across repeated cells.
 whole=Image.new('RGBA',size)
 for y,row in enumerate(layout):
  for x,t in enumerate(row):
   if t is not None:whole.paste(cells[t],(16*x,16*y))
 whole.save(A/(name+'.png'))
inv=json.loads((A/'inventory.json').read_text());solid=sorted({int(t,16)for pal,ts in inv['visible_backgrounds']['A3AF'].items()if pal in ['0F162638','0F072830','0F0A1A39']for t in ts})
for t in solid:
 if t not in cells:
  x,y=(t%8)*16,((t//8)%8)*16;im=material.crop((x,y,x+16,y+16));im.putalpha(Image.fromarray(native_hull(patterns[t]).astype(np.uint8)*255));cells[t]=im
wall=sorted({int(t,16)for pal,ts in inv['visible_backgrounds']['A3AF'].items()if pal in ['0F070010','0F172737']for t in ts});empty=Image.new('RGBA',(16,16))
for phase in ['0F','30','31']:
 for suffix in ['162638','072830','0A1A39']:
  for t in solid:emit(t,phase+suffix,cells[t],'native organic terrain')
 for suffix in ['070010','172737','081030','1B2B3B']:
  for t in wall:emit(t,phase+suffix,empty,'distant organic wall')
 for suffix in ['162638','072830','070010','172737','0A1A39']:emit(0x1b00,phase+suffix,empty,'empty space')
parsed=[]
for line in lines:
 m=re.fullmatch(r'(?:\[([^]]+)\])?<tile>(.*)',line)
 if m:parsed.append((line,m[1]or'',m[2].split(',')))
# Complete player/HUD/effect aliases in original order and mirrored poses.
for source,head,f in parsed:
 t=int(f[1],16)
 if not 0xa00<=t<=0xa8d:continue
 terms=head.split('&')if head else[]
 if any(defs.get(k.lstrip('!'),['',''])[1]=='memoryCheckConstant'and int(defs[k.lstrip('!')][2],16)in [0x72,0x78,0x79]for k in terms):continue
 clone(source,t+0x1000,f[2],'player HUD effects',terms,0x1000,rules if head else tail)
for pal,donor in [('FF300036','FF300036'),('FF221136','FF221136'),('FF190927','FF300036')]:
 for t in [0x4e,0x4f]:
  s=next(l for l in lines if l.startswith(f'<tile>29,{0x200+t:04X},{donor},'));clone(s,0x1a00+t,pal,'accepted 1-up',destination=tail)
for j in range(12):
 s=next(l for l,head,f in parsed if int(f[0])==57 and int(f[1],16)==0x108e+j and f[2]=='FF301116');clone(s,0x1a8e+j,'FF301116','Thunder')
s=next(l for l,head,f in parsed if int(f[0])==42 and int(f[1],16)==0x694 and f[2]=='FF301116');clone(s,0x1acd,'FF301116','returning projectile')
# Six native lava cells are exact copies of accepted Stage 2 lava/ice.
for t in range(0x1b6f,0x1b75):
 for pal in ['0F060616','0F161606','0F122131']:
  found=[(l,h,f)for l,h,f in parsed if 0x300<=int(f[1],16)<0x400 and patterns[int(f[1],16)]==patterns[t]and f[2]==pal and h.startswith('s25Room&s25DataLo&s25DataHi')];assert found
  for s,h,f in found:
   for phase in ['0F','30','31']:clone(s,t,phase+pal[2:],'approved lava ice',h.split('&')[3:])
raw=Image.open(R/'art/generated/level6_organic_orb.png').convert('RGBA');poses=[]
for i in range(2):
 part=raw.crop((i*raw.width//2,0,(i+1)*raw.width//2,raw.height));box=part.getchannel('A').point(lambda v:255 if v>=160 else 0).getbbox();im=part.crop(box).resize((32,32),Image.Resampling.LANCZOS);alpha=np.array(im.getchannel('A'))>=160;im=im.convert('RGB').quantize(colors=48).convert('RGBA');im.putalpha(Image.fromarray(alpha.astype(np.uint8)*255));im.save(A/f'orb_{i}.png')
 layout=[[0x1a9c+4*i,0x1a9d+4*i],[0x1a9e+4*i,0x1a9f+4*i]];poses.append(dict(name=f'orb_{i}',layout=layout,size=[32,32]))
 for y,row in enumerate(layout):
  for x,t in enumerate(row):emit(t,'FF0A1930',im.crop((x*16,y*16,x*16+16,y*16+16)),'whole orb')
guard_palettes=['162638','070010','060616','161606','122131','072830','172737','071737','1B2B3B','0A1A39','081030']
im=Image.open(R/'art/generated/level6_organic_background.png').convert('RGBA').resize((512,480),Image.Resampling.LANCZOS);im.save(P/'Final_Citadel_Organic.png');flash=im.copy();flash.putalpha(176);flash.save(P/'Final_Citadel_Organic_Flash.png')
for phase in ['0F','30','31']:
 for suffix in guard_palettes:
  pal=phase+suffix
  for t in range(0x1b00,0x1c00):
   name=f'organicView{t:04X}_{pal}';conditions.append(f'<condition>{name},tileAtPosition,128,16,{t:04X},{pal}')
   backgrounds.append(f'[{scope}&{name}]<background>Final_Citadel_Organic'+('_Flash'if phase!='0F'else'')+'.png,1,0,0,1,0,0')
def block(part,entries):return '# BEGIN LEVEL6_ORGANIC '+part+'\n'+'\n'.join(entries)+'\n# END LEVEL6_ORGANIC '+part+'\n'
anchor='# END LEVEL6_LATE IMAGES\n';at=text.index(anchor)+len(anchor);text=text[:at]+block('IMAGES',['<img>Final_Citadel_Organic_2x.png'])+block('CONDITIONS',conditions)+block('MAPPINGS',rules+tail+backgrounds)+text[at:]
(P/'hires.txt').write_text(text);atlas.save(P/'Final_Citadel_Organic_2x.png');atlas.save(A/'Final_Citadel_Organic_2x.png')
(A/'registration.json').write_text(json.dumps(dict(atlas_index=index,scope=scope,conditions=conditions,mappings=records,clones=clones,groups=groups,poses=poses,solid_tiles=solid,wall_tiles=wall,backgrounds=backgrounds,guard_palettes=guard_palettes),indent=2)+'\n')
print('Level 6 organic:',len(rules)+len(tail),'tile rules;',len(backgrounds),'background guards;',len(cache),'atlas cells')
