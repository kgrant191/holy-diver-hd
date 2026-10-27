"""Complete the recorded staff hall, menu item and following outdoor encounter."""
from pathlib import Path
import hashlib,json,re
import numpy as np
from PIL import Image,ImageOps
from prepare_level4_sentinel import prepare

r=Path(__file__).resolve().parents[1];p=r/'build/Holy_Diver_(Tr)';a=r/'art/level4_staff'
text=(p/'hires.txt').read_text();prior=json.loads((r/'evidence/0.17.0-pack-sha256.json').read_text())
assert hashlib.sha256(text.encode()).hexdigest()==prior['hires.txt']
images=[l[5:]for l in text.splitlines()if l.startswith('<img>')];assert len(images)==51
defs={l[11:].split(',')[0]:l for l in text.splitlines()if l.startswith('<condition>')}
old=json.loads((r/'art/level4_courtyard/registration.json').read_text())
patterns=json.loads((a/'native_patterns.json').read_text());observed=json.loads((a/'stable_backgrounds.json').read_text())
atlas=Image.new('RGBA',(512,512));cache={};conditions=[];rules=[];tail_aliases=[];alias_mode=False;records=[];clones=[];backgrounds=[];pose_records=[];alias_records=[];aliasdefs={};imagecache={}
scopes={'AC61':old['scopes']['AC61']}
for suffix,addr,value in [('Mode',0x72,0x18),('Lo',0x78,0xd9),('Hi',0x79,0xac)]:conditions.append(f'<condition>staffArena{suffix},memoryCheckConstant,{addr:04X},==,{value:02X}')
scopes['ACD9']='staffArenaMode&staffArenaLo&staffArenaHi'
def cell_from(fields):
 idx=int(fields[0]);x,y=int(fields[3]),int(fields[4])
 if idx not in imagecache:imagecache[idx]=Image.open(p/images[idx]).convert('RGBA')
 return imagecache[idx].crop((x,y,x+16,y+16))
def tile(t,pal,im,kind,scope='',brightness='1'):
 assert im.size==(16,16)
 digest=hashlib.sha256(im.tobytes()).hexdigest()
 if digest not in cache:
  i=len(cache);xy=(i%32*16,i//32*16);assert xy[1]<512;cache[digest]=xy;atlas.paste(im,xy)
 x,y=cache[digest];line=('['+scope+']'if scope else '')+f'<tile>51,{t:04X},{pal},{x},{y},{brightness},N'
 (tail_aliases if alias_mode else rules).append(line);records.append(dict(tile=f'{t:04X}',palette=pal,xy=[x,y],scope=scope,kind=kind,rule=line));return line
def clone(line,new,kind):
 (tail_aliases if alias_mode else rules).append(new);clones.append(dict(source_rule=line,rule=new,kind=kind))
def reg(im,size):
 im=im.convert('RGBA').resize(size,Image.Resampling.LANCZOS);alpha=im.getchannel('A').point(lambda v:255 if v>=128 else 0)
 im=im.convert('RGB').quantize(colors=96).convert('RGBA');im.putalpha(alpha);return im
def tint(im,dark,light):
 out=ImageOps.colorize(ImageOps.grayscale(im),dark,light).convert('RGBA');out.putalpha(im.getchannel('A'));return out

# Every final courtyard background rule is inherited, with bounded statue
# context and matching capitals intact. The arena selects physical bank 0D,
# byte-identical to 0B; byte matching alone cannot identify the physical bank.
arena_renames={}
for t in range(256):assert patterns[f'{0xb00+t:04X}']==patterns[f'{0xd00+t:04X}']
arena_source=[line for line in text.splitlines()if line.startswith('['+old['scopes']['AB71'])and'<tile>'in line]
arena_conditions={term.lstrip('!')for line in arena_source for term in line.split(']')[0][1:].split('&')}
for name in sorted(arena_conditions):
 line=defs[name]
 fields=line[11:].split(',')
 if fields[1]=='tileNearby' and 0xb00<=int(fields[4],16)<0xc00:
  target='staffArena_'+name;arena_renames[name]=target;fields[0]=target;fields[4]=f'{int(fields[4],16)+0x200:04X}'
  conditions.append('<condition>'+','.join(fields))
for line in text.splitlines():
 if not line.startswith('['+old['scopes']['AB71'])or'<tile>'not in line:continue
 t=int(line.split('<tile>')[1].split(',')[1],16)
 if 0xb00<=t<0xc00:
  new=line.replace(old['scopes']['AB71'],scopes['ACD9']);head,tail=new.split(']',1)
  original_terms=head[1:].split('&')
  # Historical doorway rules put their bound after the probe. Preserve the
  # predicate, but short-circuit on the bound before reading the neighboring
  # screen cell. Earlier installed mappings remain byte-exact.
  bounds=[term for term in original_terms if defs.get(term.lstrip('!'),'').split(',')[1:2]in [['positionCheckX'],['positionCheckY']]]
  ordered=bounds+[term for term in original_terms if term not in bounds]
  terms=[('!'if term.startswith('!')else '')+arena_renames.get(term.lstrip('!'),term.lstrip('!'))for term in ordered]
  fields=tail[6:].split(',');fields[1]=f'{t+0x200:04X}'
  clone(line,'['+'&'.join(terms)+']<tile>'+','.join(fields),'outdoor scenery reuse')

# The upper hall statues use the same complete layouts in a different palette.
# Preserve each guard's position before its neighbor read, including clipping.
for side in ['Left','Right']:
 source='courtyardStatue'+side;target='staffHallStatue'+side
 conditions.append(defs[source].replace(source,target,1).replace('0F071737','0F172737'))
for m in old['mappings']:
 if 'statue'not in m['kind']and'ornament'not in m['kind']:continue
 line=m['rule'];new=line.replace(old['scopes']['AB71'],scopes['AC61']).replace('0F071737','0F172737')
 head,tail=new.split(']',1)
 rename={'courtyardStatue'+s:'staffHallStatue'+s for s in ['Left','Right']}
 new='['+'&'.join(rename.get(t,t)for t in head[1:].split('&'))+']'+tail
 clone(line,new,'complete upper-hall ornament')
empty=Image.new('RGBA',(16,16))
for pal,ts in observed['AC61'].items():
 if pal not in ['0F071727','0F031323']:continue
 for key in ts:tile(int(key,16),pal,empty,'hall decorative wall reveal',scopes['AC61'])

# Guard against every recorded scenery identity, not just the entrance view.
# Rendered CHR checks keep menus, transitions and lives cards independent.
for room,pals in observed.items():
 for pal,ts in pals.items():
  for key in ts:
   name=f'staffView{room}_{key}_{pal}'
   conditions.append(f'<condition>{name},tileAtPosition,128,16,{key},{pal}')
   style='Interior'if room=='AC61'else'Exterior'
   backgrounds.append(f'[{scopes[room]}&{name}]<background>Golden_Temple_{style}.png,1,0,0,1,0,0')

# One complete staff supplies both gameplay cells and the four menu cells.
raw=Image.open(r/'art/generated/temple_staff.png').convert('RGBA')
raw=raw.crop(raw.getchannel('A').point(lambda v:255 if v>=160 else 0).getbbox())
staff=Image.new('RGBA',(16,32));staff.paste(reg(raw,(12,30)),(2,1));staff.save(a/'staff.png')
for i,t in enumerate([0xa95,0xa96]):tile(t,'FF26173A',staff.crop((0,i*16,16,i*16+16)),'staff pickup')
menu=Image.new('RGBA',(32,32));menu.paste(staff,(8,0));menu.save(a/'staff_menu.png')
for y,row in enumerate([[0x96a,0x969],[0x968,0x956]]):
 for x,t in enumerate(row):
  cx,cy=40+x*8,104+y*8;name=f'staffMenu{x}{y}'
  conditions += [f'<condition>{name}X,originPositionCheckX,==,{cx}',f'<condition>{name}Y,originPositionCheckY,==,{cy}']
  scope=f'pauseScreen&pauseMagicRow&pausedPalette&{name}X&{name}Y'
  tile(t,'0F172737',menu.crop((x*16,y*16,x*16+16,y*16+16)),'same staff in Start menu',scope)

# The arena selects 0C00; all 117 returning actor/HUD patterns are identical
# to 0A00. Clone sprite-signature conditions as well as the final tile rules.
for t in range(0x75):assert patterns[f'{0xc00+t:04X}']==patterns[f'{0xa00+t:04X}']
def remap(scope,palette=None):
 terms=[]
 for term in scope.split('&')if scope else []:
  neg='!'if term.startswith('!')else '';name=term.lstrip('!');fields=defs.get(name,'').split('>')[-1].split(',')
  if len(fields)>1 and fields[1]=='spriteNearby'and 0xa00<=int(fields[4],16)<=0xa74:
   fields[4]=f'{int(fields[4],16)+0x200:04X}';new=f'staffCopy_{palette or "native"}_{name}';fields[0]=new
   if palette:fields[5]=palette
   aliasdefs[new]='<condition>'+','.join(fields);name=new
  terms.append(neg+name)
 return '&'.join(terms)
ghost_palettes={'FF061530':('#2e061c','#ffe2cf'),'FF102030':('#42526c','#ffffff'),'FF301116':('#081a46','#6de0ff')}
alias_mode=True
for line in text.splitlines():
 match=re.fullmatch(r'(?:\[([^]]+)\])?<tile>(.*)',line)
 if not match:continue
 sc,fields=match[1]or'',match[2].split(',');t=int(fields[1],16)
 if not 0xa00<=t<=0xa74:continue
 target=t+0x200;newfields=fields.copy();newfields[1]=f'{target:04X}';newscope=remap(sc)
 new=('['+newscope+']'if newscope else '')+'<tile>'+','.join(newfields)
 clone(line,new,'byte-identical arena actor/HUD bank')
 alias_records.append(dict(source=f'{t:04X}',target=f'{target:04X}',source_rule=line,rule=new))
 # The sentinel briefly uses native Randy-shaped decoys in three palettes.
 # Keep the approved pose/alpha and native signatures, tinting only RGB.
 if t<=0xa3f and fields[2]=='FF300036':
  im=cell_from(fields)
  for pal,(dark,light)in ghost_palettes.items():
   newsc=scopes['ACD9'];other=remap(sc,pal)
   if other:newsc+='&'+other
   tile(target,pal,tint(im,dark,light),'native Randy-shaped decoy',newsc,fields[5])
conditions+=list(aliasdefs.values())
alias_mode=False

# Register complete sentinel poses before slicing. Shared cells are asserted
# identical, keeping the torso/head stable through native leg animation.
poses,fit=prepare(r);layouts=json.loads((a/'native_sentinel_layouts.json').read_text());seen={}
colors={'FF061530':None,'FF102030':('#52647a','#ffffff'),'FF122232':('#0b235d','#c3edff')}
for i,(pose,layout)in enumerate(zip(poses,layouts)):
 for pal,pair in colors.items():
  im=pose if pair is None else tint(pose,*pair);name=f'sentinel_{i}_{pal}';im.save(a/(name+'.png'))
  pose_records.append(dict(name=name,palette=pal,layout=layout['layout'],size=[96,96]))
  for key,x,y in layout['layout']:
   part=im.crop((x*2,y*2,x*2+16,y*2+16));identity=(key,pal)
   if identity in seen:assert seen[identity]==part.tobytes();continue
   seen[identity]=part.tobytes();tile(int(key,16),pal,part,'sentinel native animation',scopes['ACD9'])

# The round cannon shot is the already finished, byte-identical 0A94 shot.
assert patterns['0CF8']==patterns['0A94']
source=next(l for l in text.splitlines()if re.match(r'<tile>\d+,0A94,FF301116,',l))
clone(source,source.replace(',0A94,',',0CF8,'),'byte-identical round shot')
tile(0xcf7,'FF162830',Image.open(r/'art/level4_courtyard/fire_orb.png').convert('RGBA'),'small arena ember',scopes['ACD9'])

def block(name,lines):return '# BEGIN TEMPLE_STAFF '+name+'\n'+'\n'.join(lines)+'\n# END TEMPLE_STAFF '+name+'\n'
end=text.index('\n',text.rfind('<img>'))+1;text=text[:end]+block('IMAGES',['<img>Golden_Temple_Staff_2x.png'])+text[end:]
marker='# BEGIN TEMPLE_COURTYARD MAPPINGS'
text=text.replace(marker,block('CONDITIONS',conditions)+block('MAPPINGS',rules+backgrounds)+marker)
text+=block('ALIASES',tail_aliases)
(p/'hires.txt').write_text(text);atlas.save(p/'Golden_Temple_Staff_2x.png')
(a/'registration.json').write_text(json.dumps(dict(scopes=scopes,tile_rules=len(rules)+len(tail_aliases),conditions=len(conditions),background_rules=len(backgrounds),mappings=records,clones=clones,actor_aliases=alias_records,pose_records=pose_records,sentinel_fit=fit,backgrounds=backgrounds,atlas_cells=len(cache),native_gameplay_modified=False,prior_artwork_modified=False),indent=2)+'\n')
print('Staff hall and arena:',len(rules)+len(tail_aliases),'tiles;',len(backgrounds),'rendered background guards;',len(cache),'atlas cells')
