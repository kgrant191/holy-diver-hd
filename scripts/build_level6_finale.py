"""Final climb, two native boss forms and ending; earlier pack is removable intact."""
from pathlib import Path
import hashlib,json,re,colorsys
import numpy as np
from PIL import Image,ImageEnhance,ImageOps
from prepare_level6_finale import prepare
from verify_level6_opening_rules import native_hull
R=Path(__file__).resolve().parents[1];P=R/'build/Holy_Diver_(Tr)';A=R/'art/level6_finale'
text=(P/'hires.txt').read_text();prior=json.loads((R/'evidence/0.29.1-pack-sha256.json').read_text());assert hashlib.sha256(text.encode()).hexdigest()==prior['hires.txt']
lines=text.splitlines();images=[l[5:]for l in lines if l.startswith('<img>')];index=len(images);assert index==69
patterns={int(k,16):bytes.fromhex(v)for k,v in json.loads((A/'native_patterns.json').read_text()).items()};inv=json.loads((A/'inventory.json').read_text());defs={l[11:].split(',')[0]:l[11:].split(',')for l in lines if l.startswith('<condition>')}
parsed=[];bykey={}
for l in lines:
 m=re.fullmatch(r'(?:\[([^]]+)\])?<tile>(.*)',l)
 if m:
  h=m[1]or'';f=m[2].split(',');parsed.append((l,h,f));bykey.setdefault((int(f[1],16),f[2]),[]).append((l,h,f))
conditions=[];rules=[];tail=[];records=[];clones=[];backgrounds=[];scopes={};cache={};copies={};imcache={};atlas=Image.new('RGBA',(1024,512));empty=Image.new('RGBA',(16,16));newfiles=[]
for room in ['A49F','A553','A58F','B01C']:
 terms=[]
 for label,addr,value in [('Mode',0x72,4),('Lo',0x78,int(room,16)&255),('Hi',0x79,int(room,16)>>8)]:
  name='finale'+room+label;conditions.append(f'<condition>{name},memoryCheckConstant,{addr:04X},==,{value:02X}');terms.append(name)
 scopes[room]='&'.join(terms)
for name,addr,value in [('finaleBody1',0x208c,0x3b),('finaleBody1B',0x20cc,0x43),('finaleBody2',0x218c,0x3b),('finaleBody2B',0x212d,0xc5),('finaleBody2Intro',0x202d,0xc5)]:conditions.append(f'<condition>{name},ppuMemoryCheckConstant,{addr:04X},==,{value:02X}')
intro_scope=scopes['A58F']+'&finaleBody1&finaleBody2Intro'
body_scopes={'boss1':[scopes[r]+'&finaleBody1&finaleBody1B&!finaleBody2Intro'for r in ['A553','A58F']],'boss2':[scopes['A58F']+'&finaleBody2&finaleBody2B',intro_scope]}
def source_cell(source):
 f=source.split('<tile>')[1].split(',');i,x,y=int(f[0]),int(f[3]),int(f[4])
 if i not in imcache:imcache[i]=Image.open(P/images[i]).convert('RGBA')
 return imcache[i].crop((x,y,x+16,y+16))
def emit(t,pal,im,scope,kind,brightness=1):
 digest=hashlib.sha256(im.tobytes()).hexdigest()
 if digest not in cache:
  n=len(cache);xy=(n%64*16,n//64*16);assert xy[1]<512;cache[digest]=xy;atlas.paste(im,xy)
 x,y=cache[digest];rule=f'[{scope}]<tile>{index},{t:04X},{pal},{x},{y},{brightness},N';rules.append(rule);records.append(dict(tile=f'{t:04X}',palette=pal,xy=[x,y],scope=scope,kind=kind,rule=rule));return rule
def dep(term,shift=0,palmap=None):
 palmap=palmap or{};neg='!'if term.startswith('!')else'';name=term.lstrip('!')
 if name in ['hmirror','vmirror','bgpriority']:return term
 key=(name,shift,tuple(sorted(palmap.items())))
 if key not in copies:
  d=defs[name].copy();new='finaleReuse'+str(len(copies));copies[key]=new;d[0]=new;assert d[1]!='tileNearby'
  if d[1]in ['spriteNearby','tileAtPosition']:
   t=int(d[4],16)
   if shift and 0xa00<=t<=0xa8d:assert patterns[t]==patterns[t+shift];d[4]=f'{t+shift:04X}'
   if d[5]in palmap:d[5]=palmap[d[5]]
  conditions.append('<condition>'+','.join(d))
 return neg+copies[key]
def clone(source,t,pal,scope,kind,terms=(),shift=0,palmap=None,brightness=1,destination=None):
 f=source.split('<tile>')[1].split(',');assert patterns[int(f[1],16)]==patterns[t],(f[1],hex(t));f[1]=f'{t:04X}';f[2]=pal;f[5]=str(float(f[5])*brightness)if brightness!=1 else f[5]
 head='&'.join([scope]+[dep(k,shift,palmap)for k in terms]);rule=f'[{head}]<tile>'+','.join(f);(rules if destination is None else destination).append(rule);clones.append(dict(source_rule=source,rule=rule,kind=kind))
def first(t,pal,atlas_id=None):
 matches=bykey[t,pal]
 if atlas_id is not None:matches=[x for x in matches if int(x[2][0])==atlas_id]
 return next((x for x in matches if not x[1]),matches[0])
# Complete accepted climb terrain, effects, player poses and the approved blob.
organic=json.loads((R/'art/level6_organic/registration.json').read_text());revision=json.loads((R/'art/level6_enemy_revision/registration.json').read_text())
for e in revision['mappings']+organic['mappings']+organic['clones']:
 src=e['rule'];rule=src.replace('['+organic['scope'],'['+scopes['A49F'],1);rules.append(rule);clones.append(dict(source_rule=src,rule=rule,kind='accepted organic climb'))
# The last shaft uses a different native ribbed wall family from A3AF.
# Only its measured decorative palette is cleared; all ledge IDs stay opaque.
climb_wall=sorted(int(t,16)for t in inv['visible_backgrounds']['A49F']['0F070010'])
assert not set(climb_wall)&{int(t,16)for t in inv['visible_backgrounds']['A49F']['0F162638']}
for t in climb_wall:
 for suffix in ['070010','1B2B3B']:
  for phase in ['0F','30','31']:emit(t,phase+suffix,empty,scopes['A49F'],'final ascent decorative wall')
for dst,src,count,pal,aid,kind in [(0x1aad,0x12e5,18,'FF110130',57,'returning flying skeleton'),(0x1abf,0x008c,8,'FF301116',None,'returning flying skull')]:
 for j in range(count):
  s,h,f=first(src+j,pal,aid);clone(s,dst+j,pal,scopes['A49F'],kind)
# Complete actor aliases in the boss bank. Preserve pose-specific priority.
actors=[]
for s,h,f in parsed:
 t=int(f[1],16)
 if not 0xa00<=t<=0xa8d:continue
 terms=h.split('&')if h else[]
 if any(defs.get(k.lstrip('!'),['',''])[1]=='memoryCheckConstant'and int(defs[k.lstrip('!')][2],16)in [0x72,0x78,0x79]for k in terms):continue
 actors.append((s,h,f))
 for room in ['A553','A58F']:
  clone(s,t+0x1200,f[2],scopes[room],'player HUD effects',terms,0x1200,destination=rules if h else tail)
phases=[({'FF301116':'FF200106','FF221136':'FF120126','FF300036':'FF200F26'},.65),({'FF301116':'FF100F0F','FF221136':'FF020F16','FF300036':'FF100F16'},.3),({'FF301116':'FF000F0F','FF221136':'FF0F0F06','FF300036':'FF000F06'},.12)]
for pm,brightness in phases:
 for s,h,f in actors:
  if f[2]not in pm:continue
  for room in ['A553','A58F']:clone(s,int(f[1],16)+0x1200,pm[f[2]],scopes[room],'native actor fade',h.split('&')if h else[],0x1200,pm,brightness,rules if h else tail)
for room in ['A553','A58F']:
 for j in range(12):
  s,h,f=first(0x108e+j,'FF301116',57);clone(s,0x1c8e+j,'FF301116',scopes[room],'approved Thunder')
 for t in [0x4e,0x4f]:
  for pal,donor in [('FF300036','FF300036'),('FF221136','FF221136'),('FF190927','FF300036')]:s,h,f=first(0x200+t,donor,29);clone(s,0x1c00+t,pal,scopes[room],'approved 1-up')
# Existing dragon artwork already covers its normal green palette globally.
dragon_sources={int(f[1],16):s for s,h,f in parsed if not h and f[0]=='52'and f[2]=='FF190927'and 0x1c00<=int(f[1],16)<0x1d00}
for room in ['A553','A58F']:
 for e in inv['sprites'][room]:
  t=int(e['tile'],16);pal=e['palette']
  if t not in dragon_sources or pal in ['FF190927','FF0F0F0F']:continue
  s=dragon_sources[t];im=source_cell(s);brightness=1
  if pal in ['FF300036','FF3F3F3F']:a=np.array(im);a[:,:,:3]=255;im=Image.fromarray(a)
  elif pal=='FF0F0F07':brightness=.12
  elif pal=='FF090F17':brightness=.35
  emit(t,pal,im,scopes[room],'dragon transformation and fade',brightness)
# Returning bronze crawler, including the differently colored native variant.
for j in range(12):
 s,h,f=first(0x18e7+j,'FF072630',64)
 for room in ['A553','A58F']:clone(s,0x1ce3+j,'FF062630',scopes[room],'returning crawler')
body_cells,body_fills,parts,dragons=prepare();fill_sources=[]
# Room colors/fades. Damage palettes keep painted details while visibly flashing.
normal=['061628','163636','063026','072830','071737','1B2B3B','172737','162638','060616','070010']
palettes={p:('normal',1)for p in normal};palettes.update({'302010':('hit',1),'102030':('hit',1),'0F0618':('normal',.65),'062626':('normal',.65),'0F2016':('normal',.65),'0F0F08':('normal',.3),'0F1616':('normal',.3),'0F1006':('normal',.3),'0F0606':('normal',.12),'0F000F':('normal',.12)})
def treatment(im,kind):
 if kind!='hit':return im
 alpha=im.getchannel('A');im=ImageOps.colorize(ImageOps.grayscale(im),'#251324','#fff1d1').convert('RGBA');im.putalpha(alpha);return im
variants=json.loads((A/'boss_background_variants.json').read_text());native_old={patterns[t]:t for t in range(0x1b00,0x1c00)}
for name,table in body_cells.items():
 for key,entry in table.items():
  t=int(key,16);im=entry['image']
  # Alternate native stump cells retain their smaller native outlines.
  pos=next(p for p in variants[name]['positions']if p['x']==entry['x']+variants[name]['box'][0]and p['y']==entry['y']+variants[name]['box'][1])
  if len(pos['tiles'])>1:
   alpha=np.array(im.getchannel('A'));alpha[~native_hull(patterns[t])]=0;im=im.copy();im.putalpha(Image.fromarray(alpha))
  for scope in body_scopes[name]:
   for suffix,(kind,bri)in palettes.items():
    for phase in ['0F','30','31']:emit(t,phase+suffix,treatment(im,kind),scope,name+' body',bri)
 for i,e in enumerate(body_fills[name]):
  # Blank interior cells have no distinct CHR identity. Register them to a
  # unique stable body tile so the entire form follows native scrolling and
  # horizontal motion. Explicit bounds precede every neighbor observation.
  positions=variants[name]['positions'];counts={}
  for pos in positions:
   for t in pos['tiles']:counts[t]=counts.get(t,0)+1
  choices=[pos for pos in positions if len(pos['tiles'])==1 and next(iter(pos['tiles']))!='1D00'and counts[next(iter(pos['tiles']))]==1]
  anchor=min(choices,key=lambda p:abs(p['x']-e['x'])+abs(p['y']-e['y']))
  t=next(iter(anchor['tiles']));dx=(anchor['x']-e['x'])//2;dy=(anchor['y']-e['y'])//2;prefix=f'finale{name}Fill{i}';terms=[]
  for label,typ,op,value in [('L','positionCheckX','>=',max(0,-dx)),('R','positionCheckX','<',min(256,256-dx)),('T','positionCheckY','>=',max(0,-dy)),('B','positionCheckY','<',min(240,240-dy))]:
   cond=prefix+label;conditions.append(f'<condition>{cond},{typ},{op},{value}');terms.append(cond)
  probe=prefix+'Anchor';conditions.append(f'<condition>{probe},tileNearby,{dx},{dy},{t},0F063026,Y');terms.append(probe)
  fill_sources.append(dict(form=name,x=e['x'],y=e['y'],anchor=t,dx=dx,dy=dy,terms=terms))
  for scope in body_scopes[name]:
   for suffix,(kind,bri)in palettes.items():
    for phase in ['0F','30','31']:emit(0x1d00,phase+suffix,treatment(e['image'],kind),scope+'&'+'&'.join(terms),name+' static interior fill',bri)
# Boss chamber structural terrain uses the exact accepted chitin source/masks.
terrain={int(e['tile'],16):e['rule']for e in organic['mappings']if e['kind']=='native organic terrain'and e['palette']=='0F162638'}
for t in range(0x1d00,0x1e00):
 src=native_old.get(patterns[t])
 if src not in terrain:continue
 s=terrain[src]
 for room in ['A553','A58F']:
  for suffix,(kind,bri)in palettes.items():
   for phase in ['0F','30','31']:clone(s,t,phase+suffix,scopes[room],'approved chitin geometry',brightness=bri)
material=Image.open(R/'art/level6_organic/material.png').convert('RGBA');im=material.crop((16,0,32,16));im.putalpha(Image.fromarray(native_hull(patterns[0x1d7d]).astype(np.uint8)*255))
for scope in body_scopes['boss1']:
 for suffix,(kind,bri)in palettes.items():
  for phase in ['0F','30','31']:emit(0x1d7d,phase+suffix,im,scope,'native ceiling attachment',bri)
# Independent articulated boss attacks follow their native OAM cells and flips.
components={}
for i in range(4):components['joint'+str(i)]=[(0x1cc3+i*4+j,j%2*16,j//2*16)for j in range(4)]
components.update(connector=[(0x1cdd+j,j%3*16,j//3*16)for j in range(6)],shot=[(0x1cd3,0,0)],arc0=[(0x1cd4,0,0),(0x1cd5,16,0)],arc1=[(0x1cd6+j,j%2*16,j//2*16)for j in range(4)],arc2=[(0x1cda,0,0),(0x1cdb,16,0),(0x1cdc,0,16)])
for name,layout in components.items():
 for t,x,y in layout:
  im=parts[name].crop((x,y,x+16,y+16))
  for room in ['A553','A58F']:
   for pal in sorted({e['palette']for e in inv['sprites'][room]if int(e['tile'],16)==t} - {'FF0F0F0F'}):
    bri={'FF0F0F00':.12,'FF0F0610':.3,'FF0F1620':.65}.get(pal,1);emit(t,pal,im,scopes[room],'boss '+name,bri)
# Green spore projectiles inherit the newly approved blob, with exact four-cell poses.
for i in range(2):
 blob=Image.open(R/f'art/level6_enemy_revision/blob_{i}.png').convert('RGBA')
 for j in range(4):
  t=0x1cbb+i*4+j
  for room in ['A553','A58F']:
   for pal in sorted({e['palette']for e in inv['sprites'][room]if int(e['tile'],16)==t} - {'FF0F0F0F'}):
    im=(blob if pal=='FF0A1930'else parts['joint0']).crop((j%2*16,j//2*16,j%2*16+16,j//2*16+16));emit(t,pal,im,scopes[room],'approved green blob'if pal=='FF0A1930'else'red boss spore')
# Clear only the measured blank identity; retain native all-black fade states.
for room in ['A553','A58F']:
 for suffix in palettes:
  for phase in ['0F','30','31']:emit(0x1d00,phase+suffix,empty,scopes[room],'native empty space')
# Ending dragon: native movement, two frames, palette cycle, fade and priority.
# These dragon CHR cells never use color index 3, so FF0F0F07 is
# genuinely all black. Do not reveal the HD source during that native fade.
for t in range(0x1ecd,0x1eec):assert not any(patterns[t][y]&patterns[t][y+8]for y in range(8))
ending_palettes=sorted({e['palette']for e in inv['sprites']['B01C']if int(e['tile'],16)>=0x1ecd}-{'FF0F0F0F','FF0F0F07'})
seen=set()
for im,layout in dragons:
 for t,x,y in layout:
  if t in seen:continue
  seen.add(t);base=im.crop((x*2,y*2,x*2+16,y*2+16))
  for pal in ending_palettes:
   cell=base;bri=1
   if pal=='FF0F0F07':bri=.12
   elif pal=='FF090F17':bri=.35
   elif pal!='FF190927':
    hue=int(pal[2:4],16)&15;rgb=colorsys.hsv_to_rgb(((hue-1)*30+225)%360/360,.8,1);light=tuple(int(100+155*v)for v in rgb);dark=tuple(int(10*v)for v in rgb);cell=ImageOps.colorize(ImageOps.grayscale(base),dark,light).convert('RGBA');cell.putalpha(base.getchannel('A'))
   emit(0x1e00+t,pal,cell,scopes['B01C'],'ending dragon',bri)
def save_background(source,base,levels=False):
 raw=Image.open(R/'art/generated'/source).convert('RGBA')
 if base=='Final_Citadel_Last_Chamber':raw=raw.crop((0,0,raw.width,int(raw.height*.89)))
 raw=raw.resize((512,480),Image.Resampling.LANCZOS);raw.putalpha(255)
 names={}
 for label,bri,alpha in [('normal',1,255),('flash',1,176)]+([('fade1',.65,255),('fade2',.3,255),('fade3',.12,255)]if levels else[]):
  im=ImageEnhance.Brightness(raw).enhance(bri);im.putalpha(alpha);filename=base+(''if label=='normal'else'_'+label)+'.png';im.save(P/filename);newfiles.append(filename);names[label]=filename
 return names
ascent=save_background('level6_final_ascent.png','Final_Citadel_Last_Ascent')
for tile,palette in inv['view_guards']['A49F']:
 for phase in ['0F','30','31']:
  t=int(tile,16);pal=phase+palette[2:];name=f'finaleClimbView{t:04X}_{pal}';conditions.append(f'<condition>{name},tileAtPosition,128,16,{t:04X},{pal}');backgrounds.append(f'[{scopes["A49F"]}&{name}]<background>{ascent["normal"if phase=="0F"else"flash"]},1,0,0,1,0,0')
for kind,source,base,x,y in [('boss1','level6_final_chamber.png','Final_Citadel_Last_Chamber',96,32),('boss2','level6_final_void.png','Final_Citadel_Last_Void',96,96)]:
 names=save_background(source,base,True)
 if kind=='boss2':continue
 for suffix,(tint,bri)in palettes.items():
  for phase in ['0F','30','31']:
   pal=phase+suffix;name=f'finale{kind}View{pal}';conditions.append(f'<condition>{name},tileAtPosition,{x},{y},1D3B,{pal}');label='flash'if phase!='0F'else{1:'normal',.65:'fade1',.3:'fade2',.12:'fade3'}[bri]
   for scope in [s for s in body_scopes[kind]if s!=intro_scope]:backgrounds.append(f'[{scope}&{name}]<background>{names[label]},1,0,0,1,0,0')
# The second form moves with native background scrolling. A rendered bank
# sample additionally prevents panoramas during native background-disable frames.
for t in [0x1d00,0x1dc7]:conditions.append(f'<condition>finaleDetachedRendered{t:04X},tileAtPosition,128,16,{t:04X},0F061628,Y')
for suffix,(kind,bri)in palettes.items():
 terms=[]
 for i in range(3):
  name=f'finaleDetachedPalette{suffix}_{i}';conditions.append(f'<condition>{name},ppuMemoryCheckConstant,{0x3f09+i:04X},==,{suffix[i*2:i*2+2]}');terms.append(name)
 for phase in ['0F','30','31']:
  pn='finaleDetachedPhase'+phase
  if suffix==next(iter(palettes)):conditions.append(f'<condition>{pn},ppuMemoryCheckConstant,3F00,==,{phase}')
  label='flash'if phase!='0F'else{1:'normal',.65:'fade1',.3:'fade2',.12:'fade3'}[bri]
  for scope in body_scopes['boss2']:
   for t in [0x1d00,0x1dc7]:backgrounds.append(f'[{scope}&{pn}&{"&".join(terms)}&finaleDetachedRendered{t:04X}]<background>{names[label]},1,0,0,1,0,0')
def block(part,entries):return '# BEGIN LEVEL6_FINALE '+part+'\n'+'\n'.join(entries)+'\n# END LEVEL6_FINALE '+part+'\n'
# All original conditions are already defined at this insertion point. New
# overrides precede the prior room mappings, while old bytes stay recoverable.
anchor='# END LEVEL6_ENEMY_REVISION MAPPINGS\n';at=text.index(anchor)+len(anchor);text=text[:at]+block('IMAGES',['<img>Final_Citadel_Finale_2x.png'])+block('CONDITIONS',conditions)+block('MAPPINGS',rules+tail+backgrounds)+text[at:]
(P/'hires.txt').write_text(text);atlas.save(P/'Final_Citadel_Finale_2x.png');atlas.save(A/'Final_Citadel_Finale_2x.png');newfiles.append('Final_Citadel_Finale_2x.png')
(A/'registration.json').write_text(json.dumps(dict(atlas_index=index,scopes=scopes,body_scopes=body_scopes,conditions=conditions,mappings=records,clones=clones,backgrounds=backgrounds,new_files=sorted(newfiles),components=components,ending_layouts=[layout for _,layout in dragons],ending_palettes=ending_palettes,body_palettes=palettes,fill_sources=fill_sources,atlas_cells=len(cache)),indent=2)+'\n')
print('Level 6 finale:',len(rules)+len(tail),'tiles;',len(backgrounds),'backgrounds;',len(cache),'atlas cells;',len(newfiles),'new files')
