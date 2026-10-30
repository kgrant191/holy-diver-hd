"""Original room colors, distinct new citadel scenery, and complete sentinel hits."""
from pathlib import Path
import hashlib,json,re
import numpy as np
from PIL import Image
from verify_level6_opening_rules import native_hull
R=Path(__file__).resolve().parents[1];P=R/'build/Holy_Diver_(Tr)';A=R/'art/level6_variety'
text=(P/'hires.txt').read_text();previous=json.loads((R/'evidence/0.26.0-pack-sha256.json').read_text())
assert hashlib.sha256(text.encode()).hexdigest()==previous['hires.txt']
lines=text.splitlines();images=[l[5:]for l in lines if l.startswith('<img>')];index=len(images);assert index==65
patterns={int(k,16):bytes.fromhex(v)for k,v in json.loads((R/'art/level6_opening/native_patterns.json').read_text()).items()}
opening=json.loads((R/'art/level6_opening/registration.json').read_text());repair=json.loads((R/'art/level6_repair/registration.json').read_text());nxt=json.loads((R/'art/level6_next/registration.json').read_text());inv=json.loads((A/'inventory.json').read_text())
scopes={**opening['scopes'],**nxt['scopes']};conditions=[];rules=[];records=[];clones=[];backgrounds=[];substitutions=[];cache={};atlas=Image.new('RGBA',(512,512))
terms=[]
for suffix,addr,val in [('Mode',0x72,0x14),('Lo',0x78,0xdf),('Hi',0x79,0xa0)]:
 name='citadelVarietyA0DF'+suffix;conditions.append(f'<condition>{name},memoryCheckConstant,{addr:04X},==,{val:02X}');terms.append(name)
scopes['A0DF']='&'.join(terms)
def emit(t,pal,im,scope,kind):
 h=hashlib.sha256(im.tobytes()).hexdigest()
 if h not in cache:
  n=len(cache);xy=(n%32*16,n//32*16);assert xy[1]<512;cache[h]=xy;atlas.paste(im,xy)
 x,y=cache[h];rule=f'[{scope}]<tile>{index},{t:04X},{pal},{x},{y},1,N';rules.append(rule)
 records.append(dict(tile=f'{t:04X}',palette=pal,xy=[x,y],scope=scope,kind=kind,rule=rule))
def clone(source,t,pal,scope,kind,identity=True):
 f=source.split('<tile>')[1].split(',');src=int(f[1],16)
 if identity:assert patterns[src]==patterns[t]
 f[1]=f'{t:04X}';f[2]=pal;rule=f'[{scope}]<tile>'+','.join(f);rules.append(rule)
 clones.append(dict(source_rule=source,rule=rule,kind=kind,native_bytes_identical=identity))
def hull(t):return Image.fromarray(native_hull(patterns[t]).astype(np.uint8)*255)
# Distinct material sources are registered whole. Every native hull is retained.
materials={}
for color in ['red','amber','green']:
 im=Image.open(R/f'art/generated/level6_{color}_stone.png').convert('RGB').resize((64,64),Image.Resampling.LANCZOS).quantize(colors=96).convert('RGBA');im.save(A/f'{color}_material.png');materials[color]=im
# Existing authored ornaments retain their shape, color and full registration.
ornaments={t for layout in opening['groups'].values()for row in layout for t in row}|{0x1727,0x1728}
groups=dict(nxt['groups']);groups['upper_ceiling']=[[0x17b4,0x17b5],[0x17b6,0x17b7]]
# Native nametable groups measured throughout the vertical shaft and green room.
groups.update({
 'shaft_ceiling':[[0x17b8,0x17b9,0x17ba,0x17bb],[0x17bc,0x17bd,0x17be,0x17bf],[0x17c0,0x17c1,0x17c2,None]],
 'shaft_left':[[0x17c3,0x17c4],[0x17c7,0x17c8]],
 'shaft_center':[[0x17c5,0x17c6],[0x17c9,0x17ca]],
 'shaft_right':[[0x17cb,0x17cc],[0x17cf,0x17d0]],
 'shaft_floor':[[0x17cd,0x17ce],[0x17d1,0x17d2]],
 'shaft_low':[[0x17d6,0x17d7],[0x17d8,0x17d9],[0x17da,0x17db]],
 'shaft_pillar':[[0x17dd,0x17de],[0x17df,0x17e0]],
 'crypt_floor':[[0x17e7,0x17e8],[0x17e9,0x17ea]],
 'crypt_ceiling':[[0x17eb,0x17ec,0x17ed,0x17ee],[0x17ef,0x17f0,0x17f1,0x17f2],[0x17f3,0x17f4,0x17f5,0x1757],[0x1756,None,0x1755,0x1754]]})
cells={};group_records=[]
for color,stone in materials.items():
 cells[color]={}
 for name,layout in groups.items():
  im=stone.crop((0,0,len(layout[0])*16,len(layout)*16));mask=Image.new('L',im.size)
  for y,row in enumerate(layout):
   for x,t in enumerate(row):
    if t is not None:mask.paste(hull(t),(x*16,y*16))
  im.putalpha(mask);im.save(A/f'{color}_{name}.png')
  for y,row in enumerate(layout):
   for x,t in enumerate(row):
    if t is not None:cells[color][t]=im.crop((x*16,y*16,x*16+16,y*16+16))
 # Shape variants borrow the same material coordinates as the shared adjoining cells.
 for t,src in [(0x17dc,0x17c3),(0x17d3,0x17cb),(0x17d4,0x17cd),(0x17d5,0x17cf),(0x17e1,0x17de),(0x17e2,0x17e0)]:
  im=cells[color][src].copy();im.putalpha(hull(t));cells[color][t]=im
empty=Image.new('RGBA',(16,16))
# Complete scope-specific rules take priority over older blue generic stone.
for room,scope in scopes.items():
 color='amber'if room=='9F3B'else'green'if room=='A0DF'else'red'
 solid=set(nxt['solid_tiles'])if room in ['9F3B','A02B','A0DF']else set(opening['solid_tiles'])|set(range(0x17b4,0x17b8))
 if room in inv['visible_backgrounds']:
  for pal in ['0F061636','0F162738','0F0B1B3B']:
   solid.update(int(t,16)for t in inv['visible_backgrounds'][room].get(pal,{}))
 solid.discard(0x1700)
 suffixes=['061636','072830']+(['162738']if room in ['9F3B','A02B']else[])+(['0B1B3B']if room=='A0DF'else[])
 for phase in ['0F','30','31']:
  for suffix in suffixes:
   for shift in [0,0x200]:
    emit(0x1700+shift,phase+suffix,empty,scope,'empty native space')
    for t in sorted(solid-ornaments):
     im=cells[color].get(t)
     if im is None:
      x,y=t%4*16,t//4%4*16;im=materials[color].crop((x,y,x+16,y+16));im.putalpha(hull(t))
     emit(t+shift,phase+suffix,im,scope,color+' structural stone')
# Copy A02B's retained ornaments, animation, wall clearing and actor sources.
# New structural rules above precede these fallbacks. Their native cell IDs match.
donor=nxt['scopes']['A02B'];target=scopes['A0DF']
for line in lines:
 if line.startswith('['+donor)and '<tile>'in line:
  rule=line.replace(donor,target,1);rules.append(rule);clones.append(dict(source_rule=line,rule=rule,kind='new room exact rule reuse',native_bytes_identical=True))
# Only the green room's measured blue decorative wall layer is cleared.
wall=sorted(int(t,16)for t in inv['visible_backgrounds']['A0DF']['0F011121'])
for phase in ['0F','30','31']:
 for suffix in ['011121','172737','071727']:
  for t in wall:
   for shift in [0,0x200]:emit(t+shift,phase+suffix,empty,target,'green room distant wall')
# Both damage palettes, all 53 sentinel cells and four poses, use finished art.
for room in ['9F3B','A02B','A0DF']:
 scope=scopes[room]
 for pal in ['FF102030','FF122232']:
  for j in range(53):
   source=next(l for l in lines if '<tile>51,'+f'{0xcbe+j:04X},'+pal+','in l)
   clone(source,0x18a9+j,pal,scope,'sentinel hit')
 # The projectile also changes with its owner's palette. Keep its HD source.
 shot=next(e['rule']for e in nxt['clones']if e['kind']=='one-cell shot art reuse')
 for pal in ['FF102030','FF122232']:clone(shot,0x18eb,pal,scope,'shot hit palette')
 spark=next(l for l in lines if '<tile>51,0CF7,FF301116,'in l)
 for pal in ['FF301116','FF072630']:clone(spark,0x18de,pal,scope,'returning spark')
# Replace only the existing corridor/shaft panorama references, reversibly.
styles={'9F3B':('Amber_Ossuary','level6_amber_ossuary'),'A02B':('Crimson_Shaft','level6_crimson_shaft'),'A0DF':('Verdant_Crypt','level6_verdant_crypt')}
for room,(style,source)in styles.items():
 im=Image.open(R/f'art/generated/{source}.png').convert('RGBA').resize((512,480),Image.Resampling.LANCZOS);im.save(P/f'Final_Citadel_{style}.png')
 flash=im.copy();flash.putalpha(176);flash.save(P/f'Final_Citadel_{style}_Flash.png')
 if room!='A0DF':
  for old in nxt['backgrounds']:
   if old.startswith('['+scopes[room]+'&'):
    new=old.replace('Final_Citadel_Interior','Final_Citadel_'+style);substitutions.append([old,new])
replacements=dict(substitutions);assert len(replacements)==len(substitutions)
text='\n'.join(replacements.get(l,l)for l in lines)+'\n'
guard_palettes=sorted(set(nxt['guard_palettes'])|{'0B1B3B','011121'})
for phase in ['0F','30','31']:
 for suffix in guard_palettes:
  pal=phase+suffix
  for base in [0x1700,0x1900]:
   for t in range(base,base+256):
    name=f'citadelVarietyViewA0DF_{t:04X}_{pal}';conditions.append(f'<condition>{name},tileAtPosition,128,16,{t:04X},{pal}')
    image='Final_Citadel_Verdant_Crypt'+('_Flash'if phase!='0F'else'')+'.png'
    backgrounds.append(f'[{target}&{name}]<background>{image},1,0,0,1,0,0')
def block(part,entries):return '# BEGIN LEVEL6_VARIETY '+part+'\n'+'\n'.join(entries)+'\n# END LEVEL6_VARIETY '+part+'\n'
anchor='# END LEVEL6_NEXT IMAGES\n';at=text.index(anchor)+len(anchor)
# New A0DF room conditions precede reused donor conditions, so put mappings
# after all old next conditions but before next mappings. Opening scopes have
# not been declared yet: new aliases below use their own declarations.
newscope={}
for room in scopes:
 if room=='A0DF':continue
 names=[]
 for old in scopes[room].split('&'):
  source=next(l for l in lines if l.startswith('<condition>'+old+','));name=old+'Variety';conditions.append(source.replace(old,name,1));names.append(name)
 newscope[scopes[room]]='&'.join(names)
for old,new in newscope.items():
 rules=[l.replace(old,new,1)if l.startswith('['+old)else l for l in rules]
 for e in records:
  if e['scope']==old:e['scope']=new;e['rule']=e['rule'].replace(old,new,1)
 for e in clones:
  if e['rule'].startswith('['+old):e['rule']=e['rule'].replace(old,new,1)
for room in scopes:scopes[room]=newscope.get(scopes[room],scopes[room])
text=text[:at]+block('IMAGES',['<img>Final_Citadel_Variety_2x.png'])+block('CONDITIONS',conditions)+text[at:]
anchor='# END LEVEL6_NEXT CONDITIONS\n';at=text.index(anchor)+len(anchor)
text=text[:at]+block('MAPPINGS',rules+backgrounds)+text[at:]
(P/'hires.txt').write_text(text);atlas.save(P/'Final_Citadel_Variety_2x.png');atlas.save(A/'Final_Citadel_Variety_2x.png')
(A/'registration.json').write_text(json.dumps(dict(atlas_index=index,atlas_cells=len(cache),scopes=scopes,conditions=conditions,mappings=records,clones=clones,backgrounds=backgrounds,substitutions=substitutions,groups=groups,ornaments=sorted(ornaments),green_wall=wall,guard_palettes=guard_palettes),indent=2)+'\n')
print('Level 6 variety:',len(rules),'tile rules;',len(backgrounds),'new backgrounds;',len(substitutions),'changed backgrounds;',len(cache),'atlas cells')
