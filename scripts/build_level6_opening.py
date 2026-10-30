"""Cold citadel scenery and cape; preserve all native movement and prior assets."""
from pathlib import Path
import hashlib,json,re,io
import numpy as np
from PIL import Image
R=Path(__file__).resolve().parents[1];P=R/'build/Holy_Diver_(Tr)';A=R/'art/level6_opening'
text=(P/'hires.txt').read_text();prior=json.loads((R/'evidence/0.24.0-pack-sha256.json').read_text())
assert hashlib.sha256(text.encode()).hexdigest()==prior['hires.txt']
lines=text.splitlines();images=[l[5:]for l in lines if l.startswith('<img>')];index=len(images);assert index==62
patterns={int(k,16):bytes.fromhex(v)for k,v in json.loads((A/'native_patterns.json').read_text()).items()}
inv=json.loads((A/'inventory.json').read_text());defs={l[11:].split(',')[0]:l[11:].split(',')for l in lines if l.startswith('<condition>')}
conditions=[];rules=[];backgrounds=[];records=[];clones=[];scopes={};cache={};atlas=Image.new('RGBA',(512,256));dependency_cache={}
def save(im,path):
 b=io.BytesIO();im.save(b,format='PNG');data=b.getvalue();path.write_bytes(data);assert path.read_bytes()==data
def hull(t):
 b=patterns[t];a=np.array([[255 if(b[y]|b[y+8])>>(7-x)&1 else 0 for x in range(8)]for y in range(8)],dtype=np.uint8)
 for y in range(8):
  xs=np.flatnonzero(a[y])
  if len(xs):a[y,xs[0]:xs[-1]+1]=255
 for x in range(8):
  ys=np.flatnonzero(a[:,x])
  if len(ys):a[ys[0]:ys[-1]+1,x]=255
 return Image.fromarray(a).resize((16,16),Image.Resampling.NEAREST)
def emit(t,pal,im,scope,kind):
 h=hashlib.sha256(im.tobytes()).hexdigest()
 if h not in cache:
  n=len(cache);xy=(n%32*16,n//32*16);assert xy[1]<256;cache[h]=xy;atlas.paste(im,xy)
 x,y=cache[h];rule=f'[{scope}]<tile>{index},{t:04X},{pal},{x},{y},1,N'
 rules.append(rule);records.append(dict(tile=f'{t:04X}',palette=pal,xy=[x,y],scope=scope,kind=kind,rule=rule))
def dependency(name):
 neg='!'if name.startswith('!')else'';name=name.lstrip('!')
 if name in {'hmirror','vmirror','bgpriority'}:return neg+name
 if name not in dependency_cache:
  d=defs[name].copy();new='citadelReuse'+str(len(dependency_cache));dependency_cache[name]=new;d[0]=new
  assert d[1]!='tileNearby','No new background neighbor probes'
  conditions.append('<condition>'+','.join(d))
 return neg+dependency_cache[name]
def clone(source,t,pal,scope,kind,keep_terms=()):
 f=source.split('<tile>')[1].split(',');src=int(f[1],16);assert patterns[src]==patterns[t]
 f[1]=f'{t:04X}';f[2]=pal;head='&'.join([scope]+[dependency(k)for k in keep_terms])
 rule=f'[{head}]<tile>'+','.join(f);rules.append(rule);clones.append(dict(source_rule=source,rule=rule,kind=kind,source_tile=f'{src:04X}',tile=f'{t:04X}',palette=pal))
for room,mode in [('9A8B',4),('9BB7',16),('9CA7',12)]:
 terms=[]
 for suffix,addr,value in [('Mode',0x72,mode),('Lo',0x78,int(room,16)&255),('Hi',0x79,int(room,16)>>8)]:
  name='citadel'+room+suffix;conditions.append(f'<condition>{name},memoryCheckConstant,{addr:04X},==,{value:02X}');terms.append(name)
 scopes[room]='&'.join(terms)

# Register complete materials before slicing their native unions.
sheet=Image.open(R/'art/generated/level6_terrain.png').convert('RGBA');w,h=sheet.size;hw,hh=w//2,h//2
rock=sheet.crop((hw+4,hh+4,w,h)).resize((64,64),Image.Resampling.LANCZOS)
brick=sheet.crop((0,0,hw//2,hh*2//5)).resize((32,32),Image.Resampling.LANCZOS)
skull=sheet.crop((hw+4,4,w-4,hh-4)).resize((32,32),Image.Resampling.LANCZOS)
cornice=sheet.crop((0,hh+4,hw-4,h)).resize((64,64),Image.Resampling.LANCZOS)
# Shared top-half identities repeat every 16 native pixels.
cornice.paste(cornice.crop((0,0,32,32)),(32,0))
materials={};groups={
 'brick':[[0x1731,0x1732],[0x1733,0x172c]],
 'skull':[[0x171d,0x171e],[0x171f,0x1720]],
 'cornice':[[0x171b,0x171c,0x171b,0x171c],[0x1780,0x1781,0x1780,0x1781],[0x1778,0x1782,0x1783,0x1784],[0x1785,0x1786,0x1787,0x1788]]}
for name,im in [('brick',brick),('skull',skull),('cornice',cornice)]:
 union=Image.new('L',im.size)
 for y,row in enumerate(groups[name]):
  for x,t in enumerate(row):
   cell=im.crop((x*16,y*16,x*16+16,y*16+16));cell.putalpha(hull(t));union.paste(hull(t),(x*16,y*16))
   if t in materials:assert materials[t].tobytes()==cell.tobytes()
   materials[t]=cell
 im.putalpha(union);save(im,A/(name+'.png'))
save(rock,A/'rock_material.png');empty=Image.new('RGBA',(16,16))
solid=set(int(k,16)for room in ['9A8B','9BB7','9CA7']for k in inv['visible_backgrounds'][room].get('0F061636',{}))
solid.discard(0x1700)
wall=set(range(0x1734,0x173b))|set(range(0x1751,0x1769))|{0x1700}
normal_roles={'solid':['061636','072830'],'skull':['081030','1B2B3B'],'wall':['071727','172737']}
for room in scopes:
 for phase in ['0F','30','31']:
  for pal in normal_roles['solid']:
   emit(0x1700,phase+pal,empty,scopes[room],'empty native space')
   for t in sorted(solid):
    if t in materials:im=materials[t]
    elif t in [0x1727,0x1728]:
     im=cornice.crop(((t-0x1727)*16,16,(t-0x1727)*16+16,32));im.putalpha(hull(t))
    else:
     x,y=t%4*16,t//4%4*16;im=rock.crop((x,y,x+16,y+16));im.putalpha(hull(t))
    emit(t,phase+pal,im,scopes[room],'native structural stone')
  for pal in normal_roles['skull']:
   for t in range(0x171d,0x1721):emit(t,phase+pal,materials[t],scopes[room],'whole skull block')
  for pal in normal_roles['wall']:
   for t in sorted(wall):emit(t,phase+pal,empty,scopes[room],'distant wall')

# Byte-proven accepted lava/ice remains animated/frozen at the native cadence.
parsed=[]
for line in lines:
 m=re.fullmatch(r'(?:\[([^]]+)\])?<tile>(.*)',line)
 if m:parsed.append((line,m[1]or'',m[2].split(',')))
lava_palettes=['0F060616','0F161606','0F122131']
for t in range(0x1769,0x1775):
 donors={i for i in range(0x300,0x400)if patterns[i]==patterns[t]}
 for pal in lava_palettes:
  found=[(l,head,f)for l,head,f in parsed if int(f[1],16)in donors and f[2]==pal and head.startswith('s25Room&s25DataLo&s25DataHi')]
  assert found,(hex(t),pal)
  for source,head,f in found:
   terms=head.split('&')[3:]
   for room in scopes:
    for phase in ['0F','30','31']:clone(source,t,phase+pal[2:],scopes[room],'approved lava and ice',terms)

# Restore every observed returning actor from a complete accepted source.
by_pattern={}
for source,head,f in parsed:
 t=int(f[1],16)
 if t<0x1600 and f[2].startswith('FF'):by_pattern.setdefault(patterns[t],[]).append((source,head,f))
actor_pairs=sorted({(int(e['tile'],16),e['palette'])for room in ['9A8B','9BB7']for e in inv['sprites'][room]if int(e['tile'],16)>=0x168e})
for t,pal in actor_pairs:
 candidates=by_pattern.get(patterns[t],[])
 # Accept only unconditional donors or donors whose conditions merely scope a room.
 candidates=[q for q in candidates if not q[1]or all(defs.get(k.lstrip('!'),['',''])[1]=='memoryCheckConstant'and int(defs[k.lstrip('!')][2],16)in [0x72,0x78,0x79]for k in q[1].split('&'))]
 assert candidates,(hex(t),pal)
 def rank(q):
  return (q[2][2]!=pal,q[2][2]in ['FF303030','FF200106','FF100F0F','FF000F0F'],q[2][2]!='FF190927'if 0x169c<=t<=0x16b7 else False,bool(q[1]))
 source,head,f=sorted(candidates,key=rank)[0]
 for room in scopes:clone(source,t,pal,scopes[room],'accepted returning actor')

# The cape occupies the lower-right 16x16-native inventory slot.
raw=Image.open(R/'art/generated/level6_cape.png').convert('RGBA');box=raw.getchannel('A').point(lambda x:255 if x>=128 else 0).getbbox();raw=raw.crop(box)
raw.thumbnail((28,30),Image.Resampling.LANCZOS);cape=Image.new('RGBA',(32,32));cape.paste(raw,((32-raw.width)//2,(32-raw.height)//2))
alpha=cape.getchannel('A').point(lambda x:255 if x>=128 else 0);cape=cape.convert('RGB').quantize(colors=64).convert('RGBA');cape.putalpha(alpha);save(cape,A/'cape_menu.png')
for y,row in enumerate([[0x955,0x954],[0x952,0x951]]):
 for x,t in enumerate(row):
  name=f'citadelCape{x}{y}';conditions += [f'<condition>{name}X,originPositionCheckX,==,{72+x*8}',f'<condition>{name}Y,originPositionCheckY,==,{104+y*8}']
  scope='&'.join([dependency(k)for k in ['pauseScreen','pauseMagicRow','pausedPalette']]+[name+'X',name+'Y'])
  emit(t,'0F172737',cape.crop((x*16,y*16,x*16+16,y*16+16)),scope,'cape menu')

# Complete rendered-bank guards survive scrolling, pause/resume and native flashes.
guard_palettes=['061636','060616','161606','122131','081030','071727','072830','071737','1B2B3B','172737']
for style in ['Exterior','Interior']:
 im=Image.open(R/f'art/generated/level6_{style.lower()}.png').convert('RGBA').resize((512,480),Image.Resampling.LANCZOS)
 save(im,P/f'Final_Citadel_{style}.png')
 flash=im.copy();flash.putalpha(176);save(flash,P/f'Final_Citadel_{style}_Flash.png')
for room in scopes:
 style='Interior'if room=='9BB7'else'Exterior'
 for phase in ['0F','30','31']:
  for suffix in guard_palettes:
   pal=phase+suffix
   for t in range(0x1700,0x1800):
    name=f'citadelView{room}_{t:04X}_{pal}';conditions.append(f'<condition>{name},tileAtPosition,128,16,{t:04X},{pal}')
    image=f'Final_Citadel_{style}'+('_Flash'if phase!='0F'else'')+'.png'
    backgrounds.append(f'[{scopes[room]}&{name}]<background>{image},1,0,0,1,0,0')
def block(part,items):return '# BEGIN LEVEL6_OPENING '+part+'\n'+'\n'.join(items)+'\n# END LEVEL6_OPENING '+part+'\n'
end=text.index('\n',text.rfind('<img>'))+1;text=text[:end]+block('IMAGES',['<img>Final_Citadel_Tiles_2x.png'])+block('CONDITIONS',conditions)+block('MAPPINGS',rules+backgrounds)+text[end:]
(P/'hires.txt').write_text(text);save(atlas,P/'Final_Citadel_Tiles_2x.png');save(atlas,A/'Final_Citadel_Tiles_2x.png')
(A/'registration.json').write_text(json.dumps(dict(atlas_index=index,atlas_cells=len(cache),scopes=scopes,groups=groups,mappings=records,clones=clones,conditions=conditions,backgrounds=backgrounds,guard_palettes=guard_palettes,solid_tiles=sorted(solid),wall_tiles=sorted(wall)),indent=2)+'\n')
print('Level 6 opening:',len(rules),'tiles;',len(backgrounds),'backgrounds;',len(cache),'atlas cells; all prior art unchanged')
