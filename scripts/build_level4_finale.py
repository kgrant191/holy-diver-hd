"""Reuse temple halls and actors; register the rotating eye-tower encounter."""
from pathlib import Path
import hashlib,json,re
from PIL import Image,ImageOps
from prepare_boss4 import prepare
r=Path(__file__).resolve().parents[1];p=r/'build/Holy_Diver_(Tr)';a=r/'art/level4_finale';text=(p/'hires.txt').read_text();prior=json.loads((r/'evidence/0.19.1-pack-sha256.json').read_text());assert hashlib.sha256(text.encode()).hexdigest()==prior['hires.txt']
images=[l[5:]for l in text.splitlines()if l.startswith('<img>')];assert len(images)==53
defs={l[11:].split(',')[0]:l[11:].split(',')for l in text.splitlines()if l.startswith('<condition>')}
staff=json.loads((r/'art/level4_staff/registration.json').read_text());dragon=json.loads((r/'art/level4_dragon/registration.json').read_text());observed=json.loads((a/'stable_backgrounds.json').read_text());patterns=json.loads((a/'native_patterns.json').read_text());aliases=json.loads((a/'native_aliases.json').read_text())
conditions=[];rules=[];tail=[];clones=[];records=[];backgrounds=[];scopes={};atlas=Image.new('RGBA',(512,512));cache={};renames={};pose_rules=[]
for room,mode in [('AE41',12),('AEF5',12),('AFA9',4)]:
 for suffix,addr,v in [('Mode',0x72,mode),('Lo',0x78,int(room,16)&255),('Hi',0x79,int(room,16)>>8)]:conditions.append(f'<condition>finale{room}{suffix},memoryCheckConstant,{addr:04X},==,{v:02X}')
 scopes[room]='&'.join('finale'+room+s for s in ['Mode','Lo','Hi'])
def tile(key,pal,im,kind,scope='',target=None):
 assert im.size==(16,16);digest=hashlib.sha256(im.tobytes()).hexdigest()
 if digest not in cache:
  i=len(cache);xy=(i%32*16,i//32*16);assert xy[1]<512;cache[digest]=xy;atlas.paste(im,xy)
 x,y=cache[digest];line=('['+scope+']'if scope else '')+f'<tile>53,{key},{pal},{x},{y},1,N';(rules if target is None else target).append(line);records.append(dict(tile=key,palette=pal,xy=[x,y],scope=scope,kind=kind,rule=line));return line

def clone(src,new,kind,target=None):
 (rules if target is None else target).append(new);clones.append(dict(source_rule=src,rule=new,kind=kind))

# Final interior mappings include all past stone/stair/ornament repairs. The
# new halls use physical bank0D, not the first byte-identical0B match.
source_scope=staff['scopes']['AC61'];arena_scope=staff['scopes']['ACD9']
for room in ['AE41','AEF5']:
 scope=scopes[room]
 for line in text.splitlines():
  if '<tile>'not in line or not line.startswith('['):continue
  head,fields=line[1:].split(']<tile>');fields=fields.split(',')
  if not all(t in head.split('&')for t in source_scope.split('&'))or not 0xb00<=int(fields[1],16)<0xc00:continue
  terms=head.replace(source_scope,scope).split('&');bounds=[t for t in terms if defs.get(t.lstrip('!'),['',''])[1]in ['positionCheckX','positionCheckY']];terms=bounds+[t for t in terms if t not in bounds];mapped=[]
  for term in terms:
   neg='!'if term.startswith('!')else '';name=term.lstrip('!');d=defs.get(name)
   if d and d[1]=='tileNearby'and 0xb00<=int(d[4],16)<0xc00:
    new='finaleD_'+name
    if name not in renames:
     f=d.copy();f[0]=new;f[4]=f'{int(f[4],16)+0x200:04X}';conditions.append('<condition>'+','.join(f));renames[name]=new
    name=new
   mapped.append(neg+name)
  fields[1]=f'{int(fields[1],16)+0x200:04X}';clone(line,'['+'&'.join(mapped)+']<tile>'+','.join(fields),'final repaired interior scenery')
 empty=Image.new('RGBA',(16,16))
 for pal,keys in observed[room].items():
  for key in keys:
   if pal in ['0F071723','0F071727','0F071737','0F031323']:tile(key,pal,empty,'decorative interior reveal',scope)
   name=f'finaleView{room}_{key}_{pal}';conditions.append(f'<condition>{name},tileAtPosition,128,16,{key},{pal}');backgrounds.append(f'[{scope}&{name}]<background>Golden_Temple_Interior.png,1,0,0,1,0,0')
 # The finished sentinel and native decoy palettes share their exact0C cells.
 for m in staff['mappings']:
  if m['scope'].startswith(arena_scope)and m['kind']in ['sentinel native animation','native Randy-shaped decoy','small arena ember']:
   clone(m['rule'],m['rule'].replace(arena_scope,scope),'returning sentinel and native decoy')
 # Extend the improved health/magic drops without changing earlier priorities.
 for m in dragon['mappings']:
  if m['scope']==source_scope and m['kind']in ['visible heart','visible magic']:clone(m['rule'],m['rule'].replace(source_scope,scope),'visible recovery pickup')

# The boss room switches to0E actor/HUD graphics, byte-identical to0A00–74.
# Keep earlier specific mappings first and reproduce native pose signatures.
aliasdefs={}
for line in text.splitlines():
 m=re.fullmatch(r'(?:\[([^]]+)\])?<tile>(.*)',line)
 if not m:continue
 head,fields=m[1]or'',m[2].split(',');t=int(fields[1],16)
 if not 0xa00<=t<=0xa74:continue
 assert patterns[f'{t:04X}']==patterns[f'{t+0x400:04X}']
 if any(defs[t.lstrip('!')][1]=='memoryCheckConstant' and int(defs[t.lstrip('!')][2],16) in [0x72,0x78,0x79] for t in head.split('&') if t):continue
 terms=[]
 for term in head.split('&')if head else []:
  neg='!'if term.startswith('!')else '';name=term.lstrip('!');d=defs[name]
  if d[1]=='spriteNearby'and 0xa00<=int(d[4],16)<=0xa74:
   new='finaleE_'+name;f=d.copy();f[0]=new;f[4]=f'{int(f[4],16)+0x400:04X}';aliasdefs[new]='<condition>'+','.join(f);name=new
  terms.append(neg+name)
 fields[1]=f'{t+0x400:04X}';clone(line,('['+'&'.join(terms)+']'if terms else '')+'<tile>'+','.join(fields),'byte-identical boss actor/HUD bank',rules if head else tail)
conditions+=list(aliasdefs.values())
for m in dragon['mappings']:
 if m['scope']==source_scope and m['kind']in ['visible heart','visible magic']:clone(m['rule'],m['rule'].replace(source_scope,scopes['AFA9']),'boss recovery pickup')
source=next(l for l in text.splitlines()if re.match(r'<tile>\d+,0A94,FF301116,',l));clone(source,source.replace(',0A94,',',0E8E,'),'byte-identical boss projectile')
assert patterns['0E8E']==patterns['0A94']

panels,rings,fit=prepare(r)
for i,keys in enumerate([['0CB6','0CB7','0CB8','0CB9'],['0CBA','0CBB','0CBC','0CBD']]):
 for j,key in enumerate(keys):
  for target in aliases[key]:
   assert patterns[key]==patterns[target];tile(target,'FF301116',rings[i].crop((j%2*16,j//2*16,j%2*16+16,j//2*16+16)),'hovering ring native phase')
# A full64x32 piece of the accepted stone supplies the complete moving ledge.
stone=Image.open(r/'art/level4_masonry/solid.png').convert('RGBA');stone.save(a/'moving_platform.png')
for j,key in enumerate(['0EB4','0EB5','0EB6','0EB7']):
 for target in aliases[key]:
  for half in [0,1]:
   name=f'finalePlatform{target}_{half}';conditions.append(f'<condition>{name},spriteNearby,{16 if half==0 else -16},0,{target},FF172737')
   x=(half*2+j%2)*16;y=j//2*16;tile(target,'FF172737',stone.crop((x,y,x+16,y+16)),'complete moving stone platform',name)
  # Single clipped platform halves retain the matching established stone.
  tile(target,'FF172737',stone.crop((j%2*16,j//2*16,j%2*16+16,j//2*16+16)),'clipped moving stone platform',target=tail)
# One recorded sentinel ember briefly uses the shared white/red palette.
source=next(m for m in staff['mappings']if m['tile']=='0CF7'and m['palette']=='FF162830')
for room in ['AE41','AEF5']:clone(source['rule'],source['rule'].replace(arena_scope,scopes[room]).replace('FF162830','FF301116'),'native ember palette')

# Boss bands are complete4x7 layouts. Exact native neighborhood signatures
# select a WHOLE phase; shared tile identities never splice different eyes.
layouts=json.loads((a/'boss_band_layouts.json').read_text())[:8];palettes=['0F071727','0F001030'];seen_fallback={}
for phase,(layout,panel)in enumerate(zip(layouts,panels)):
 for pal in palettes:
  im=panel if pal=='0F071727'else ImageOps.colorize(ImageOps.grayscale(panel),'#203540','#f4ffff').convert('RGBA');im.save(a/f'tower_band_{phase}_{pal}.png')
  for key,x,y in layout['layout']:
   prefix=f'finaleBand{phase}_{pal}_{x}_{y}';terms=[scopes['AFA9']]
   # Bounds short-circuit every neighbor read, including offscreen cells.
   for suffix,typ,op,value in [('L','positionCheckX','>=',x*8),('R','positionCheckX','<',256-(6-x)*8),('T','positionCheckY','>=',y*8),('B','positionCheckY','<',240-(3-y)*8)]:
    name=prefix+suffix;conditions.append(f'<condition>{name},{typ},{op},{value}');terms.append(name)
   signature=[]
   for other,xx,yy in layout['layout']:
    if (xx,yy)==(x,y):continue
    name=prefix+f'N{xx}_{yy}';conditions.append(f'<condition>{name},tileNearby,{(xx-x)*8},{(yy-y)*8},{other},{pal}');terms.append(name);signature.append([other,xx-x,yy-y])
   part=im.crop((x*16,y*16,x*16+16,y*16+16));line=tile(key,pal,part,'whole eye-tower phase','&'.join(terms));pose_rules.append(dict(rule=line,phase=phase,tile=key,palette=pal,x=x,y=y,signature=signature))
   seen_fallback.setdefault((key,pal),part)
for (key,pal),im in seen_fallback.items():tile(key,pal,im,'tower transition fallback',scopes['AFA9'])
# A subdued existing hall keeps the active eye and ledges readable. Rendered
# guards retain menu/entry blackouts and native background disable on death.
# A blank tile also exists for one rendered black frame at room entry. Require
# an actual tower identity instead. Four samples cover the moving96-pixel
# body; the extra128 sample also catches its first, partially drawn band.
edge_keys=sorted({key for layout in layouts for key,x,y in layout['layout']if x==0})
for pal in ['0F071727','0F001030']:
 for y in [32,96,128,160,224]:
  for key in edge_keys:
   name=f'finaleBossView_{y}_{key}_{pal}';conditions.append(f'<condition>{name},tileAtPosition,96,{y},{key},{pal}');backgrounds.append(f'[{scopes["AFA9"]}&{name}]<background>Golden_Temple_Interior.png,0.5,0,0,1,0,0')

def block(name,lines):return '# BEGIN TEMPLE_FINALE '+name+'\n'+'\n'.join(lines)+'\n# END TEMPLE_FINALE '+name+'\n'
end=text.index('\n',text.rfind('<img>'))+1;text=text[:end]+block('IMAGES',['<img>Golden_Temple_Finale_2x.png'])+text[end:]
marker='# BEGIN TEMPLE_RESIDUE MAPPINGS';text=text.replace(marker,block('CONDITIONS',conditions)+block('MAPPINGS',rules+backgrounds)+marker);text+=block('ALIASES',tail)
(p/'hires.txt').write_text(text);atlas.save(p/'Golden_Temple_Finale_2x.png')
(a/'registration.json').write_text(json.dumps(dict(scopes=scopes,tile_rules=len(rules)+len(tail),conditions=len(conditions),background_rules=len(backgrounds),mappings=records,clones=clones,backgrounds=backgrounds,boss_pose_rules=pose_rules,art_registration=fit,atlas_cells=len(cache),native_gameplay_modified=False,prior_artwork_modified=False),indent=2)+'\n');print('Temple finale:',len(rules)+len(tail),'tile rules;',len(conditions),'conditions;',len(cache),'atlas cells')
