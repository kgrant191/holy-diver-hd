"""Extend approved temple treatments to the recorded hall, court and re-entry."""
from pathlib import Path
import hashlib,json,re
import numpy as np
from PIL import Image,ImageOps

r=Path(__file__).resolve().parents[1];p=r/'build/Holy_Diver_(Tr)';a=r/'art/level4_courtyard'
text=(p/'hires.txt').read_text();prior=json.loads((r/'evidence/0.16.3-pack-sha256.json').read_text())
assert hashlib.sha256(text.encode()).hexdigest()==prior['hires.txt']
assert sum(l.startswith('<img>')for l in text.splitlines())==50
old=json.loads((r/'art/level4/registration.json').read_text())
patterns=json.loads((a/'native_patterns.json').read_text())
observed=json.loads((a/'stable_backgrounds.json').read_text())
views=json.loads((a/'stable_view_guards.json').read_text())
aliases=json.loads((a/'item_enemy_aliases.json').read_text())
definitions={l[11:].split(',')[0]:l for l in text.splitlines()if l.startswith('<condition>')}
conditions=[];early=[];clones=[];backgrounds=[];records=[];scopes={};clone_records=[];rename_sets={}
atlas=Image.new('RGBA',(256,128));cache={}
def reg(im,size,colors=64):
 im=im.convert('RGBA').resize(size,Image.Resampling.LANCZOS);alpha=im.getchannel('A').point(lambda x:255 if x>=128 else 0)
 im=im.convert('RGB').quantize(colors=colors).convert('RGBA');im.putalpha(alpha);return im
def tight(im):
 im=im.convert('RGBA');return im.crop(im.getchannel('A').point(lambda x:255 if x>=160 else 0).getbbox())
def tile(t,pal,im,kind,scope=''):
 digest=hashlib.sha256(im.tobytes()).hexdigest()
 if digest not in cache:
  i=len(cache);xy=(i%16*16,i//16*16);assert xy[1]<128;cache[digest]=xy;atlas.paste(im,xy)
 x,y=cache[digest];line=('['+scope+']'if scope else '')+f'<tile>50,{t:04X},{pal},{x},{y},1,N'
 early.append(line);records.append(dict(tile=f'{t:04X}',palette=pal,xy=[x,y],scope=scope,kind=kind,rule=line))
def hull(t):
 raw=bytes.fromhex(patterns[f'{t:04X}']);v=np.array([[255 if ((raw[y]|raw[y+8])>>(7-x))&1 else 0 for x in range(8)]for y in range(8)],np.uint8)
 for y in range(8):
  xs=np.flatnonzero(v[y])
  if len(xs):v[y,xs[0]:xs[-1]+1]=255
 for x in range(8):
  ys=np.flatnonzero(v[:,x])
  if len(ys):v[ys[0]:ys[-1]+1,x]=255
 return Image.fromarray(v).resize((16,16),Image.Resampling.NEAREST)

room_specs=[('AAF9',8,['AA09','AA81'],'Interior'),('AB71',0x10,['A865'],'Exterior'),('AC61',4,['AA09','AA81'],'Interior')]
for room,mode,sources,style in room_specs:
 prefix='courtyard'+room
 for suffix,addr,value in [('Mode',0x72,mode),('Lo',0x78,int(room,16)&255),('Hi',0x79,int(room,16)>>8)]:
  conditions.append(f'<condition>{prefix}{suffix},memoryCheckConstant,{addr:04X},==,{value:02X}')
 scope='&'.join(prefix+s for s in ['Mode','Lo','Hi']);scopes[room]=scope
 # Copy final, repaired rules in their original priority order, including the
 # restored stairs and EVERY short-circuit neighbor bound. Never copy 0.16.0
 # alone: doing so would reintroduce the crash and invisible-step regressions.
 for source in sources:
  source_scope=old['scopes'][source];rename={}
  selected=[l for l in text.splitlines()if l.startswith('['+source_scope)and '<tile>'in l]
  for line in selected:
   for term in line.split(']')[0][1:].split('&'):
    name=term.lstrip('!')
    if name.startswith('masonry'+source):rename[name]='cy'+room+source+'_'+name
  for name,target in rename.items():conditions.append(definitions[name].replace(name,target,1))
  rename_key=room+'/'+source;rename_sets[rename_key]=rename
  for line in selected:
   new=line.replace(source_scope,scope)
   head,tail=new.split(']',1)
   new='['+'&'.join(('!'if term.startswith('!')else '')+rename.get(term.lstrip('!'),term.lstrip('!'))for term in head[1:].split('&'))+']'+tail
   clones.append(new);clone_records.append(dict(room=room,source_room=source,source_rule=line,rule=new,rename_key=rename_key))
 # Normal rendered-tile guards exclude menus and blank/fade screens.
 for key,pal in views[room]:
  name=f'courtyardView{room}_{key}_{pal}'
  conditions.append(f'<condition>{name},tileAtPosition,128,16,{key},{pal}')
  backgrounds.append(f'[{scope}&{name}]<background>Golden_Temple_{style}.png,1,0,0,1,0,0')

empty=Image.new('RGBA',(16,16));stone=Image.open(r/'art/level4_masonry/solid.png').convert('RGBA')
for room,pals in observed.items():
 scope=scopes[room]
 for pal,ts in pals.items():
  for key in ts:
   t=int(key,16)
   if room in ['AAF9','AC61']:
    # The purple/amber window-wall palette reuses stair-shaped CHR cells.
    # Only the bright 0F172737 palette is physical in these recorded halls.
    if pal in ['0F071723','0F071727','0F031323','0F071737']:
     tile(t,pal,empty,'indoor decorative wall reveal',scope)
   else:
    if pal in ['0F031323','0F073703']:
     tile(t,pal,empty,'courtyard clouds or decorative screen reveal',scope)
    elif t in [0xb56,0xb57,0xb58]:
     tile(t,pal,Image.new('RGBA',(16,16),'#070b16'),'recessed temple entrance',scope)

# Alternate native capital cells still form the same four-cell fluted column.
# Reuse the complete approved capital rather than mixing in flat wall tiles.
old_atlas=Image.open(p/'Golden_Temple_Tiles_2x.png').convert('RGBA')
for target,source in [(0xba2,0xb03),(0xb54,0xb06),(0xbe6,0xb04),(0xbe7,0xb05)]:
 m=next(m for m in old['mappings']if int(m['tile'],16)==source and m['kind']=='outdoor gold column'and m['palette']=='0F071737')
 x,y=m['xy'];tile(target,'0F071737',old_atlas.crop((x,y,x+16,y+16)),'approved outdoor capital',scopes['AB71'])

# Reuse the existing complete gargoyle as a gold-stone architectural statue.
# Each native statue is a unique four-by-four background cell layout.
statue=reg(tight(Image.open(r/'art/level4/gargoyle_0.png')),(60,60))
alpha=statue.getchannel('A');statue=ImageOps.colorize(ImageOps.grayscale(statue),'#342715','#f1d39a').convert('RGBA');statue.putalpha(alpha)
full=Image.new('RGBA',(64,64));full.paste(statue,(2,2));full.save(a/'courtyard_statue.png')
# The opposite-facing statue uses a second layout, sharing only the native A0
# foot cell. Bounded left/right context selects that complete pose even when
# either neighboring cell is clipped offscreen.
alternate=full.transpose(Image.Transpose.FLIP_LEFT_RIGHT);alternate.save(a/'courtyard_statue_alt.png')
conditions += ['<condition>courtyardStatueLeftSafe,positionCheckX,>=,8',
 '<condition>courtyardStatueRightSafe,positionCheckX,<,248',
 '<condition>courtyardStatueLeft,tileNearby,-8,0,0BE3,0F071737',
 '<condition>courtyardStatueRight,tileNearby,8,0,0BE4,0F071737']
layout=[[0xbdf,0xbe0,0xbe1,0xbe2],[0xb5b,0xb5c,0xb63,0xb64],[0xb5d,0xb5e,0xb65,0xb66],[0xbe3,0xba0,0xbe4,0xbe5]]
for y,row in enumerate(layout):
 for x,t in enumerate(row):
  im=alternate.crop((x*16,y*16,x*16+16,y*16+16))
  if t==0xba0:
   for side in ['Left','Right']:tile(t,'0F071737',im,'opposite statue shared foot',scopes['AB71']+'&courtyardStatue'+side+'Safe&courtyardStatue'+side)
  else:tile(t,'0F071737',im,'opposite gargoyle stone ornament',scopes['AB71'])
for i,t in enumerate(range(0xb92,0xba2)):
 x=i%4*16;y=i//4*16;tile(t,'0F071737',full.crop((x,y,x+16,y+16)),'reused gargoyle stone ornament',scopes['AB71'])

wings=Image.new('RGBA',(32,16));wings.paste(reg(tight(Image.open(r/'art/generated/temple_wings.png')),(30,14)),(1,1));wings.save(a/'wings.png')
for i,t in enumerate([0xa92,0xa93]):
 for key in aliases[f'{t:04X}']:tile(int(key,16),'FF301116',wings.crop((i*16,0,i*16+16,16)),'wing pickup, native-identical bank')
orb=Image.new('RGBA',(16,16));orb.paste(reg(tight(Image.open(r/'art/generated/temple_fire_orb.png')),(14,14),48),(1,1));orb.save(a/'fire_orb.png')
tile(0xae1,'FF162830',orb,'independent fire-chain bead',scopes['AB71'])

def block(name,lines):return '# BEGIN TEMPLE_COURTYARD '+name+'\n'+'\n'.join(lines)+'\n# END TEMPLE_COURTYARD '+name+'\n'
end=text.index('\n',text.rfind('<img>'))+1;text=text[:end]+block('IMAGES',['<img>Golden_Temple_Courtyard_2x.png'])+text[end:]
marker='# BEGIN TEMPLE_MASONRY MAPPINGS'
text=text.replace(marker,block('CONDITIONS',conditions)+block('MAPPINGS',early+clones+backgrounds)+marker)
(p/'hires.txt').write_text(text);atlas.save(p/'Golden_Temple_Courtyard_2x.png')
(a/'registration.json').write_text(json.dumps(dict(scopes=scopes,tile_rules=len(early)+len(clones),conditions=len(conditions),background_rules=len(backgrounds),mappings=records,clones=clone_records,rename_sets=rename_sets,backgrounds=backgrounds,atlas_cells=len(cache),native_gameplay_modified=False,prior_artwork_modified=False),indent=2)+'\n')
print('Temple courtyard:',len(early)+len(clones),'tile mappings;',len(backgrounds),'rendered guards;',len(cache),'new atlas cells')
