"""Demonic Palace opening: scoped scenery and native registered actors/effects."""
from pathlib import Path
import hashlib,json,re
import numpy as np
from PIL import Image,ImageDraw,ImageFont,ImageOps
from prepare_level5 import reg,framed
R=Path(__file__).resolve().parents[1];P=R/'build/Holy_Diver_(Tr)';A=R/'art/level5';G=R/'art/generated'
text=(P/'hires.txt').read_text();prior=json.loads((R/'evidence/0.20.5-pack-sha256.json').read_text());assert hashlib.sha256(text.encode()).hexdigest()==prior['hires.txt']
images=[l[5:]for l in text.splitlines()if l.startswith('<img>')];index=len(images)
patterns={int(k,16):bytes.fromhex(v)for k,v in json.loads((A/'native_patterns.json').read_text()).items()};aliases=json.loads((A/'native_aliases.json').read_text());defs={l[11:].split(',')[0]:l[11:].split(',')for l in text.splitlines()if l.startswith('<condition>')}
rooms={'850A':24,'8672':4,'86EA':8,'8762':4,'8816':4};conds=[];rules=[];tail=[];records=[];clones=[];backgrounds=[];scopes={};atlas=Image.new('RGBA',(512,512));cache={};geom={}
for room,mode in rooms.items():
 names=[]
 for suffix,addr,val in [('Mode',0x72,mode),('Lo',0x78,int(room,16)&255),('Hi',0x79,int(room,16)>>8)]:
  name='palace'+room+suffix;conds.append(f'<condition>{name},memoryCheckConstant,{addr:04X},==,{val:02X}');names.append(name)
 scopes[room]='&'.join(names)
def tile(t,pal,im,kind,scope='',destination=None):
 assert im.size==(16,16);h=hashlib.sha256(im.tobytes()).hexdigest()
 if h not in cache:
  i=len(cache);xy=(i%32*16,i//32*16);assert xy[1]<512;cache[h]=xy;atlas.paste(im,xy)
 x,y=cache[h];line=('['+scope+']'if scope else '')+f'<tile>{index},{t:04X},{pal},{x},{y},1,N';(rules if destination is None else destination).append(line);records.append(dict(tile=f'{t:04X}',palette=pal,xy=[x,y],kind=kind,scope=scope,rule=line));return line
def clone(old,new,kind,destination=None):
 (rules if destination is None else destination).append(new);clones.append(dict(source_rule=old,rule=new,kind=kind))
def cellsrc(line):
 f=line.split('<tile>')[1].split(',');x,y=map(int,f[3:5]);return Image.open(P/images[int(f[0])]).convert('RGBA').crop((x,y,x+16,y+16))
def hull(t):
 b=patterns[t];a=np.array([[255 if ((b[y]|b[y+8])>>(7-x))&1 else 0 for x in range(8)]for y in range(8)],dtype=np.uint8)
 for yy in range(8):
  xs=np.flatnonzero(a[yy]);
  if len(xs):a[yy,xs[0]:xs[-1]+1]=255
 for xx in range(8):
  ys=np.flatnonzero(a[:,xx]);
  if len(ys):a[ys[0]:ys[-1]+1,xx]=255
 return Image.fromarray(a).resize((16,16),Image.Resampling.NEAREST)
empty=Image.new('RGBA',(16,16));stone=reg(Image.open(G/'palace_stone.png'),(64,64));stone.save(A/'cavern_stone.png')
# Native four-wide rock courses and their cap contours; material only changes.
terrain={}
for t in range(0x1101,0x112b):
 n=t-0x1105 if t>=0x1105 else t-0x1101;x=n%4*16;y=n//4%4*16;im=stone.crop((x,y,x+16,y+16))
 ma=np.array(hull(t))
 if 0x110d<=t<=0x111c:ma[:]=255
 elif 0x1105<=t<=0x110c or 0x1127<=t<=0x112a:
  # A cap retains its first opaque pixel in each column; stone fills beneath.
  for xx in range(16):
   ys=np.flatnonzero(ma[:,xx])
   if len(ys):ma[ys[0]:,xx]=255
 elif t<=0x1104:
  # Roof material is closed above its unchanged bottom contour.
  for xx in range(16):
   ys=np.flatnonzero(ma[:,xx])
   if len(ys):ma[:ys[-1]+1,xx]=255
 im.putalpha(Image.fromarray(ma));terrain[t]=im
# Join each complete four-cell-wide standing cap before filling internal stone.
# Native texture gaps inside a cap are not holes through the physical platform.
for first in [0x1105,0x1127]:
 keys=list(range(first,min(first+8,0x112b)))
 rows=(len(keys)+3)//4;joined=np.zeros((rows*16,64),dtype=np.uint8)
 for j,t in enumerate(keys):joined[j//4*16:j//4*16+16,j%4*16:j%4*16+16]=np.array(hull(t))
 for y in range(joined.shape[0]):
  xs=np.flatnonzero(joined[y])
  if len(xs):joined[y,xs[0]:xs[-1]+1]=255
 for x in range(64):
  ys=np.flatnonzero(joined[:,x])
  if len(ys):joined[ys[0]:,x]=255
 for j,t in enumerate(keys):terrain[t].putalpha(Image.fromarray(joined[j//4*16:j//4*16+16,j%4*16:j%4*16+16]))
# Interior roof tiles are closed stone. Only the bottom row keeps its contour.
conds.append('<condition>palaceRoofBelowBound,positionCheckY,<,232')
for bank in [0,0x200]:
 for below in range(0x1101,0x1105):
  name=f'palaceRoofBelow{below+bank:04X}';conds.append(f'<condition>{name},tileNearby,0,8,{below+bank:04X},0F182819')
  for t in range(0x1101,0x1105):
   im=terrain[t].copy();im.putalpha(Image.new('L',(16,16),255))
   tile(t+bank,'0F182819',im,'closed interior roof',scopes['850A']+'&palaceRoofBelowBound&'+name)
# A complete pillar cap occupies one native row; the shaft repeats two rows.
raw=Image.open(G/'palace_column.png').convert('RGBA');cap=reg(raw.crop((381,27,644,208)),(32,16));cap.putalpha(Image.new('L',(32,16),255))
shaft=reg(raw.crop((443,324,586,489)),(32,32));shaft.putalpha(Image.new('L',(32,32),255))
# Repeat one complete spiral turn across the four native shaft identities.
cap.save(A/'column_cap.png');shaft.save(A/'column_shaft.png')
column={0x115c:cap.crop((0,0,16,16)),0x115d:cap.crop((16,0,32,16)),0x115e:shaft.crop((0,0,16,16)),0x115f:shaft.crop((16,0,32,16)),0x1160:shaft.crop((0,16,16,32)),0x1161:shaft.crop((16,16,32,32))}
for t in column:column[t].putalpha(hull(t))
# Both palettes still encode collision. Only the known distant frieze is cleared.
observed=json.loads((A/'visible_backgrounds.json').read_text())
for room in rooms:
 scope=scopes[room]
 for pal,keys in observed.get(room,{}).items():
  for key in keys:
   t=int(key,16);im=None;kind=''
   if t==0x1100:im=empty;kind='room space'
   elif room=='850A':
    if pal=='0F071727':im=empty;kind='distant cavern reveal'
    elif pal in ['0F182819','0F182838'] and t in terrain:im=terrain[t];kind='solid cavern rock'
   elif room in ['8672','86EA','8762']:
    if pal[2:]=='062636':im=empty;kind='distant palace frieze reveal'
    elif t in column and pal[2:]=='061634':im=column[t];kind='solid crimson column'
    elif t in terrain and pal in ['0F172737','0F182819','0F182838']:
     im=terrain[t];kind='solid inner rock'
    elif 0x114f<=t<=0x1154 and pal=='0F061634':
     im=stone.crop(((t%4)*16,16,(t%4+1)*16,32));im.putalpha(hull(t));kind='solid palace rock underside'
    elif 0x114f<=t<=0x116d and pal=='0F172737':
     im=stone.crop(((t%4)*16,32,(t%4+1)*16,48));im.putalpha(hull(t));kind='native structural stone'
   elif room=='8816':
    if pal=='0F0F0717':im=empty;kind='stair hall distant wall reveal'
    elif pal=='0F001030':
     # Existing cut-stone material, registered within these native stair edges.
     material=reg(Image.open(R/'art/generated/screen2_5_stair_tread_generated.png'),(64,64))
     im=material.crop((t%4*16,(t//4%4)*16,t%4*16+16,(t//4%4)*16+16));im.putalpha(hull(t));kind='solid stair hall stone'
   if im is not None:
    for bank in [0,0x200]:tile(t+bank,pal,im,kind,scope)
    if kind.startswith('solid'):geom[f'{room}:{key}:{pal}']={'size':[16,16],'alpha_hex':im.getchannel('A').tobytes().hex()}
# Native lava topology is different, but the approved surfaces/falls are reused.
for pal in ['0F060616','0F161606','0F122131']:
 poolmap={0x1143:0x345,0x1144:0x344,0x1145:0x343,0x1146:0x342,0x1147:0x341,0x1148:0x334}
 for target,source in poolmap.items():
  old=next(l for l in text.splitlines()if re.search(r'<tile>32,'+f'{source:04X},{pal},',l));f=old.split('<tile>')[1].split(',')
  for bank in [0,0x200]:f[1]=f'{target+bank:04X}';clone(old,f'[{scopes["850A"]}]<tile>'+','.join(f),'approved lava pool and ice')
 for old in text.splitlines():
  m=re.fullmatch(r'\[(s22Room&s22DataLo&s22DataHi(?:&s22FallPhase\d+)?)\]<tile>(.*)',old)
  if not m:continue
  f=m[2].split(',');src=int(f[1],16)
  if not 0x389<=src<=0x38e or f[2]!=pal:continue
  sc=m[1].replace('s22Room&s22DataLo&s22DataHi',scopes['850A'])
  for bank in [0,0x200]:
   ff=f.copy();ff[1]=f'{src-0x389+0x1149+bank:04X}';clone(old,f'[{sc}]<tile>'+','.join(ff),'approved animated lava falls and ice')
# Distant layers activate only for normal rendered scenery, never native flashes.
for name,source in [('Demonic_Palace_Cavern.png','palace_cavern.png'),('Demonic_Palace_Interior.png','palace_interior.png')]:reg(Image.open(G/source),(768,480),192).convert('RGB').save(P/name)
guards=json.loads((A/'view_guards.json').read_text())
for room,seen in guards.items():
 for key,pal in seen:
  if not pal.startswith('0F')or pal in ['0F072830','0F071737','0F1B2B3B']:continue
  for bank in [0,0x200]:
   t=int(key,16)+bank;name=f'palaceView{room}_{t:04X}_{pal}';conds.append(f'<condition>{name},tileAtPosition,128,16,{t:04X},{pal}')
   file='Demonic_Palace_Cavern.png'if room=='850A'else'Demonic_Palace_Interior.png';backgrounds.append(f'[{scopes[room]}&{name}]<background>{file},1,0,0,1,0,0')
# Restore the single missing menu glyph in the existing font and exact slot.
letter=Image.new('RGBA',(16,16));font=ImageFont.truetype(str(R/'art/fonts/DejaVuSerif-Bold.ttf'),14);ImageDraw.Draw(letter).text((8,8),'H',font=font,anchor='mm',fill='#f4deb0')
tile(0x946,'0F072830',letter,'Thunder H','pauseScreen&pauseMagicRow&pausedPalette')
# Copy exact finished normal/Twin Fire player, HUD and shared pickups. Preserve
# every pose signature; conditional aliases come before broad original aliases.
condition_map={}
for line in text.splitlines():
 m=re.fullmatch(r'(?:\[([^]]+)\])?<tile>(.*)',line)
 if not m:continue
 head=m[1]or'';f=m[2].split(',');src=int(f[1],16)
 if not 0xa00<=src<=0xa74:continue
 target=src+0x600
 assert f'{src:04X}'in aliases[f'{target:04X}']
 if any(defs.get(t.lstrip('!'),['',''])[1]=='memoryCheckConstant'and int(defs[t.lstrip('!')][2],16)in[0x72,0x78,0x79]for t in head.split('&')if t):continue
 terms=[]
 for term in head.split('&')if head else []:
  neg='!'if term.startswith('!')else'';name=term.lstrip('!');d=defs.get(name)
  if d and d[1]=='spriteNearby'and 0xa00<=int(d[4],16)<=0xa74:
   new='palaceCopy_'+name
   if new not in condition_map:
    v=d.copy();v[0]=new;v[4]=f'{int(v[4],16)+0x600:04X}';condition_map[new]='<condition>'+','.join(v)
   name=new
  terms.append(neg+name)
 f[1]=f'{target:04X}';clone(line,('['+'&'.join(terms)+']'if terms else'')+'<tile>'+','.join(f),'exact shared player HUD bank',rules if head else tail)
conds+=list(condition_map.values())
for room,scope in scopes.items():
 for t,name in [(0x1047,'heart'),(0x1048,'magic')]:tile(t,'FF301116',Image.open(R/'art/level4_dragon'/f'{name}.png').convert('RGBA'),'visible '+name,scope)
 # Native transformation uses the same star but a different room and bank.
 tile(0x1074,'FF301116',Image.open(R/'art/level4_dragon/transform_star.png').convert('RGBA'),'transformation star',scope+'&dragonTransform')
# Complete skeleton animations share identical native head/body cells.
seen={};layouts=json.loads((A/'skeleton_layouts.json').read_text())
for i,layout in enumerate(layouts):
 im=Image.open(A/f'skeleton_{i}.png').convert('RGBA')
 for key,x,y in layout:
  part=im.crop((x*2,y*2,x*2+16,y*2+16))
  if key in seen:assert seen[key]==part.tobytes();continue
  seen[key]=part.tobytes();tile(int(key,16),'FF110130',part,'floating skeleton')
for i in range(2):tile(0x10f8+i,'FF110130',Image.open(A/'bone.png').crop((0,i*16,16,i*16+16)),'bone projectile')
for j in range(3):
 im=Image.open(A/'boulder_emerge.png');tile(0x10bd+j,'FF1B0B3B',im.crop((j*16,0,j*16+16,16)),'boulder emergence')
for pose,first in enumerate([0x10c0,0x10c9,0x10d2]):
 im=Image.open(A/f'boulder_{pose}.png')
 for j in range(9):tile(first+j,'FF1B0B3B',im.crop((j%3*16,j//3*16,j%3*16+16,j//3*16+16)),'rolling jade boulder')
for first,size,name in [(0x10db,3,'serpent_head'),(0x10e4,2,'serpent_segment')]:
 im=Image.open(A/(name+'.png'))
 for j in range(size*size):tile(first+j,'FF0B2B30',im.crop((j%size*16,j//size*16,j%size*16+16,j//size*16+16)),name)
# The small blue star uses an existing complete orb, not a quarter of Breaker.
orb=reg(Image.open(R/'art/level4/overdrive_orb.png'),(16,16));tile(0x107a,'FF110130',orb,'small blue star')
# Thunder preserves its staggered native four-cell bolt shapes and all OAM flips.
raw=Image.open(G/'palace_thunder.png').convert('RGBA');sources=[raw.crop((0,250,680,990)),raw.crop((695,20,1000,990)),raw.crop((1010,45,1536,990))]
thunder=[(0x108e,(48,32),[(16,0),(32,0),(0,16),(16,16)]),(0x1092,(32,64),[(0,0),(16,16),(16,32),(0,48)]),(0x1096,(32,48),[(16,0),(0,16),(16,16),(16,32)])]
for i,(first,size,positions)in enumerate(thunder):
 # Register the whole painted core along the native lightning centerline.
 # This keeps the native zigzag continuous through staggered tile corners.
 native=Image.new('L',size);union=Image.new('L',size);draw=ImageDraw.Draw(union)
 for j,(x,y)in enumerate(positions):
  b=patterns[first+j];bits=np.array([[255 if (b[yy]|b[yy+8])>>(7-xx)&1 else 0 for xx in range(8)]for yy in range(8)],dtype=np.uint8)
  native.paste(Image.fromarray(bits).resize((16,16),Image.Resampling.NEAREST),(x,y));draw.rectangle((x,y,x+15,y+15),fill=255)
 rawpart=sources[i];rawpart=rawpart.crop(rawpart.getchannel('A').point(lambda v:255 if v>=190 else 0).getbbox())
 turn=i==0
 if turn:rawpart=rawpart.transpose(Image.Transpose.TRANSPOSE);native=native.transpose(Image.Transpose.TRANSPOSE);union=union.transpose(Image.Transpose.TRANSPOSE)
 painted=reg(rawpart,(64,native.height));pixels=np.array(painted);mask=np.array(native);allowed=np.array(union);output=Image.new('RGBA',native.size)
 for y in range(native.height):
  xs=np.flatnonzero(mask[y]);sx=np.flatnonzero(pixels[y,:,3]>=160)
  if not len(xs)or not len(sx):continue
  center=(float(xs[0])+float(xs[-1]))/2;lo,hi=int(xs[0]),int(xs[-1]);w=min(10,max(4,hi-lo+3));x=max(0,min(native.width-w,round(center-(w-1)/2)))
  row=painted.crop((int(sx[0]),y,int(sx[-1])+1,y+1)).resize((w,1),Image.Resampling.LANCZOS);output.paste(row,(x,y))
 arr=np.array(output);arr[:,:,3]=np.where((arr[:,:,3]>=128)&(allowed>0),255,0);im=Image.fromarray(arr)
 if turn:im=im.transpose(Image.Transpose.TRANSPOSE)
 im.save(A/f'thunder_{i}.png')
 for j,(x,y)in enumerate(positions):tile(first+j,'FF301116',im.crop((x,y,x+16,y+16)),'Thunder bolt '+str(i))

# Aliases execute before the original mappings; give any later condition a local
# identical definition so every reference is defined before first use.
first_rule=next(i for i,l in enumerate(text.splitlines())if '<tile>'in l or '<background>'in l)
early={l[11:].split(',')[0]for l in text.splitlines()[:first_rule]if l.startswith('<condition>')}|{'hmirror','vmirror','bgpriority'}
early|={l[11:].split(',')[0]for l in conds};reuse={}
def ordered(line):
 if not line.startswith('['):return line
 head,rest=line[1:].split(']',1);terms=[]
 for term in head.split('&'):
  name=term.lstrip('!');neg='!'if term.startswith('!')else''
  if name not in early:
   if name not in reuse:
    new='palaceReuse_'+name;d=defs[name].copy();d[0]=new;conds.append('<condition>'+','.join(d));reuse[name]=new
   name=reuse[name]
  terms.append(neg+name)
 return '['+'&'.join(terms)+']'+rest
rules=[ordered(l)for l in rules];tail=[ordered(l)for l in tail];backgrounds=[ordered(l)for l in backgrounds]
for m in records:
 m['rule']=ordered(m['rule']);m['scope']=m['rule'][1:m['rule'].index(']')]if m['rule'].startswith('[')else''
for m in clones:m['rule']=ordered(m['rule'])

def block(name,lines):return '# BEGIN DEMONIC_PALACE '+name+'\n'+'\n'.join(lines)+'\n# END DEMONIC_PALACE '+name+'\n'
end=text.index('\n',text.rfind('<img>'))+1;text=text[:end]+block('IMAGES',['<img>Demonic_Palace_Tiles_2x.png'])+text[end:]
lines=text.splitlines(keepends=True);first=next(i for i,l in enumerate(lines)if '<tile>'in l or'<background>'in l);lines[first:first]=[block('CONDITIONS',conds),block('MAPPINGS',rules+backgrounds)];text=''.join(lines)+block('ALIASES',tail)
(P/'hires.txt').write_text(text);atlas.save(P/'Demonic_Palace_Tiles_2x.png');atlas.save(A/'Demonic_Palace_Tiles_2x.png')
(A/'registration.json').write_text(json.dumps(dict(atlas_index=index,scopes=scopes,mappings=records,clones=clones,backgrounds=backgrounds,conditions=conds,geometry=geom,atlas_cells=len(cache)),indent=2)+'\n');print('Demonic Palace:',len(rules)+len(tail),'rules;',len(conds),'conditions;',len(cache),'cells')
