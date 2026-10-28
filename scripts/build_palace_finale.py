"""Finish the recorded Palace shaft, boss, victory ascent and Level 6 entry."""
from pathlib import Path
import hashlib,json,re
import numpy as np
from PIL import Image
from prepare_palace_finale import prepare
R=Path(__file__).resolve().parents[1];P=R/'build/Holy_Diver_(Tr)';A=R/'art/level5_finale'
text=(P/'hires.txt').read_text();prior=json.loads((R/'evidence/0.23.0-pack-sha256.json').read_text());assert hashlib.sha256(text.encode()).hexdigest()==prior['hires.txt']
lines=text.splitlines();images=[l[5:]for l in lines if l.startswith('<img>')];index=len(images);assert index==61
patterns={int(k,16):bytes.fromhex(v)for k,v in json.loads((A/'native_patterns.json').read_text()).items()};inv=json.loads((A/'inventory.json').read_text());defs={l[11:].split(',')[0]:l[11:].split(',')for l in lines if l.startswith('<condition>')}
conditions=[];rules=[];tail=[];records=[];clones=[];backgrounds=[];scopes={};cache={};image_cache={};atlas=Image.new('RGBA',(512,512));condition_cache={}
for room,mode in [('8D3E',4),('8E6A',8),('8EE2',4),('9A8B',4)]:
 names=[]
 for suffix,addr,val in [('Mode',0x72,mode),('Lo',0x78,int(room,16)&255),('Hi',0x79,int(room,16)>>8)]:
  name='palaceFinale'+room+suffix;conditions.append(f'<condition>{name},memoryCheckConstant,{addr:04X},==,{val:02X}');names.append(name)
 scopes[room]='&'.join(names)
def emit(t,pal,im,scope,kind,brightness=1):
 h=hashlib.sha256(im.tobytes()).hexdigest()
 if h not in cache:
  n=len(cache);xy=(n%32*16,n//32*16);assert xy[1]<512;cache[h]=xy;atlas.paste(im,xy)
 x,y=cache[h];rule=('['+scope+']'if scope else'')+f'<tile>{index},{t:04X},{pal},{x},{y},{brightness},N'
 rules.append(rule);records.append(dict(tile=f'{t:04X}',palette=pal,xy=[x,y],scope=scope,kind=kind,rule=rule));return rule
def clone(source,target,kind,destination=None):
 (rules if destination is None else destination).append(target);clones.append(dict(source_rule=source,rule=target,kind=kind))
def cell(source):
 f=source.split('<tile>')[1].split(',');i,x,y=int(f[0]),int(f[3]),int(f[4])
 if i not in image_cache:image_cache[i]=Image.open(P/images[i]).convert('RGBA')
 return image_cache[i].crop((x,y,x+16,y+16))
def hull(t):
 b=patterns[t];a=np.array([[255 if(b[y]|b[y+8])>>(7-x)&1 else 0 for x in range(8)]for y in range(8)],dtype=np.uint8)
 for y in range(8):
  xs=np.flatnonzero(a[y])
  if len(xs):a[y,xs[0]:xs[-1]+1]=255
 for x in range(8):
  ys=np.flatnonzero(a[:,x])
  if len(ys):a[ys[0]:ys[-1]+1,x]=255
 return Image.fromarray(a).resize((16,16),Image.Resampling.NEAREST)
def dependency(term,bank=0,palettes=None):
 palettes=palettes or{};neg='!'if term.startswith('!')else'';name=term.lstrip('!')
 if name in {'hmirror','vmirror','bgpriority'}:return term
 key=(name,bank,tuple(sorted(palettes.items())))
 if key not in condition_cache:
  d=defs[name].copy();new='palaceFinaleCopy'+str(len(condition_cache));condition_cache[key]=new;d[0]=new
  if d[1]in ['spriteNearby','tileNearby','tileAtPosition']:
   if bank and 0xa00<=int(d[4],16)<=0xa8d:dst=int(d[4],16)+bank;assert patterns[int(d[4],16)]==patterns[dst];d[4]=f'{dst:04X}'
   if d[5]in palettes:d[5]=palettes[d[5]]
  conditions.append('<condition>'+','.join(d))
 return neg+condition_cache[key]
# Reuse the existing complete lift block in the later skull shaft.
for t in range(0x12f7,0x12fb):
 source=next(l for l in lines if re.search(r'<tile>60,'+f'{t:04X},FF003008,',l));clone(source,'['+scopes['8D3E']+']<tile>'+source.split('<tile>')[1],'existing moving lift')
stone=Image.open(R/'art/level5_repair/stair_material.png').convert('RGBA');empty=Image.new('RGBA',(16,16))
for t in range(0x116a,0x116e):
 x,y=t%4*16,t//4%4*16;im=stone.crop((x,y,x+16,y+16));im.putalpha(hull(t))
 for bank in [0,0x200]:
  assert patterns[t]==patterns[t+bank]
  for phase in ['0F','30','31']:emit(t+bank,phase+'001030',im,scopes['8D3E'],'shaft structural stone')
# All normal player/HUD/Breaker/Overdrive identities are exact native copies.
actor_sources=[]
for line in lines:
 m=re.fullmatch(r'(?:\[([^]]+)\])?<tile>(.*)',line)
 if not m:continue
 head=m[1]or'';f=m[2].split(',');src=int(f[1],16)
 if not 0xa00<=src<=0xa8d:continue
 if any(defs.get(t.lstrip('!'),['',''])[1]=='memoryCheckConstant'and int(defs[t.lstrip('!')][2],16)in [0x72,0x78,0x79]for t in head.split('&')if t):continue
 actor_sources.append((line,head,f))
 for bank in [0xa00,0xc00]:
  dst=src+bank;assert patterns[src]==patterns[dst];terms=[dependency(t,bank)for t in head.split('&')if t];out=f.copy();out[1]=f'{dst:04X}'
  clone(line,('['+'&'.join(terms)+']'if terms else'')+'<tile>'+','.join(out),'exact actor HUD effects alias',rules if head else tail)
# Victory phases retain complete signatures and native fade cadence.
phase_maps=[({'FF301116':'FF200106','FF221136':'FF120126','FF300036':'FF200F26'},.65),({'FF301116':'FF100F0F','FF221136':'FF020F16','FF300036':'FF100F16'},.30),({'FF301116':'FF000F0F','FF221136':'FF0F0F06','FF300036':'FF000F06'},.12)]
for palettes,brightness in phase_maps:
 for line,head,f in actor_sources:
  if f[2]not in palettes:continue
  terms=[scopes['8EE2']]+[dependency(t,0xa00,palettes)for t in head.split('&')if t];out=f.copy();out[1]=f'{int(f[1],16)+0xa00:04X}';out[2]=palettes[f[2]];out[5]=str(float(out[5])*brightness)
  clone(line,'['+'&'.join(terms)+']<tile>'+','.join(out),'victory actor fade')
# White silhouettes use the accepted source alpha. Resolve the normal white
# Randy/HUD palette first so a collapsed all-white palette stays coherent.
for line,head,f in sorted(actor_sources,key=lambda e:0 if e[2][2]=='FF300036'else 1):
 palettes={p:'FF303030'for p in ['FF301116','FF221136','FF300036']};terms=[scopes['8EE2']]+[dependency(t,0xa00,palettes)for t in head.split('&')if t];im=np.array(cell(line));im[:,:,:3]=255
 emit(int(f[1],16)+0xa00,'FF303030',Image.fromarray(im),'&'.join(terms),'victory actor white')
# Recorded Level 6 entry's red charge orb is Breaker, not a new enemy.
for line,head,f in actor_sources:
 if not 0xa75<=int(f[1],16)<=0xa7d or f[2]!='FF221136':continue
 terms=[scopes['9A8B']]+[dependency(t,0xc00,{'FF221136':'FF160636'})for t in head.split('&')if t];out=f.copy();out[1]=f'{int(f[1],16)+0xc00:04X}';out[2]='FF160636'
 clone(line,'['+'&'.join(terms)+']<tile>'+','.join(out),'existing Breaker charge')
for dst,src,count,pal,kind in [(0x148e,0x108e,12,'FF301116','Thunder'),(0x149a,0x0a94,1,'FF301116','boss projectile')]:
 for j in range(count):
  assert patterns[src+j]==patterns[dst+j];source=next(l for l in lines if re.fullmatch(r'<tile>\d+,'+f'{src+j:04X},{pal},.*',l));f=source[6:].split(',');f[1]=f'{dst+j:04X}';clone(source,'<tile>'+','.join(f),'exact '+kind)
# Whole component paintings, followed by native slicing. OAM supplies mirrors,
# independent motion, disappearance, timing and priority.
prepare();seen={}
for name,layout in json.loads((A/'boss_layouts.json').read_text()).items():
 im=Image.open(A/(name+'.png')).convert('RGBA')
 for key,x,y in layout:
  part=im.crop((x*2,y*2,x*2+16,y*2+16))
  if key in seen:assert seen[key]==part.tobytes();continue
  seen[key]=part.tobytes();emit(int(key,16),'FF052730',part,scopes['8E6A'],'boss '+name)
ornaments=json.loads((A/'ornament_layouts.json').read_text())
for room in ['8E6A','8EE2']:
 # Boss/exit structural cells equal the approved shaft stone exactly.
 for t in range(0x1501,0x150d):
  donor=t-0x1501+0x11de;assert patterns[t]==patterns[donor]
  source=next(l for l in lines if re.search(r'<tile>60,'+f'{donor:04X},0F001030,',l))
  for pal,brightness in [('0F001030',1),('30001030',1),('31001030',1),('0F0F0020',.65),('0F0F0F10',.30),('0F0F0F00',.12),('0F021222',.65),('0F1B2B3B',1)]:
   f=source.split('<tile>')[1].split(',');f[1]=f'{t:04X}';f[2]=pal;f[5]=str(brightness);clone(source,'['+scopes[room]+']<tile>'+','.join(f),'approved boss masonry')
  white=np.array(cell(source));white[:,:,:3]=255;emit(t,'30303030',Image.fromarray(white),scopes[room],'white structural stone')
 for name,palette in [('idol','0F071728'),('effigy','0F200B26')]:
  im=Image.open(A/(name+'.png')).convert('RGBA')
  pals=[(palette,1),('30'+palette[2:],1),('31'+palette[2:],1)]
  # The intermediate entrance palette occurs while rendering resumes.
  pals += [('0F041424',.65)]if name=='idol'else [('0F001020',.65),('0F071737',1)]
  for key,x,y in ornaments[name]:
   for pal,brightness in pals:emit(int(key,16),pal,im.crop((x,y,x+16,y+16)),scopes[room],name+' ornament',brightness)
  # All-black effigy cells remain native when the rising sprite takes over.
for key,x,y in json.loads((A/'effigy_sprite_layout.json').read_text()):
 im=Image.open(A/'effigy_sprite.png').convert('RGBA').crop((x,y,x+16,y+16))
 for room in ['8E6A','8EE2']:emit(int(key,16),'FF200B26',im,scopes[room],'rising effigy')
 white=np.array(im);white[:,:,:3]=255;emit(int(key,16),'FF303030',Image.fromarray(white),scopes['8EE2'],'rising white effigy')
# The blue skull fill is a distant wall behind the vertical victory flight.
for t in range(0x1501,0x1509):
 for pal in ['0F011121','0F0F0111','0F0F0F01']:emit(t,pal,empty,scopes['8EE2'],'exit distant wall')
# Whole-bank rendered guards retain background-disable and native blackouts.
guards={
 '8E6A':[(p,1 if p.startswith(('30','31'))else .5)for p in ['0F072737','0F200B26','0F001030','0F071728','30072737','30200B26','30001030','30071728','31072737','31200B26','31001030','31071728']],
 '8EE2':[('0F072737',.5),('0F001030',.5),('0F011121',.5),('0F0F0111',.325),('0F0F0020',.325),('0F0F0F01',.15),('0F0F0F10',.15),('0F0F0F00',.06)],
 '9A8B':[('0F061636',1)]}
# Half-brightness flash panorama keeps the established native-color blend.
flash=Image.open(P/'Demonic_Palace_Interior.png').convert('RGBA');arr=np.array(flash);arr[:,:,:3]=(arr[:,:,:3].astype(float)*.5).astype(np.uint8);arr[:,:,3]=176;Image.fromarray(arr).save(P/'Demonic_Palace_Boss_Flash.png')
for room,phases in guards.items():
 base=0x1700 if room=='9A8B'else 0x1500
 for pal,brightness in phases:
  for t in range(base,base+256):
   name=f'palaceFinaleView{room}_{t:04X}_{pal}';conditions.append(f'<condition>{name},tileAtPosition,128,16,{t:04X},{pal}')
   image='Stage2_Crimson_Cave_Background.png'if room=='9A8B'else('Demonic_Palace_Boss_Flash.png'if pal[:2]in ['30','31']else'Demonic_Palace_Interior.png')
   backgrounds.append(f'[{scopes[room]}&{name}]<background>{image},{brightness},0,0,1,0,0')
# Reuse the approved crimson rock at the recorded Level 6 threshold. Every
# physical edge follows the native tile hull; blank space reveals the cave.
rock=Image.open(R/'art/screen2_5/crimson_rock_registered.png').convert('RGBA')
for key in inv['visible_backgrounds']['9A8B']['0F061636']:
 t=int(key,16)
 if t==0x1700:im=empty;kind='Level 6 entry space'
 else:
  x,y=(t%4)*16,(t//4%2)*16;im=rock.crop((x,y,x+16,y+16));im.putalpha(hull(t));kind='Level 6 native crimson rock'
 emit(t,'0F061636',im,scopes['9A8B'],kind)
# The RAM rendering latch changes one submission before the card closes.
# Use the actual rendered S tile to retain the existing HD card for that last
# visible frame, while remaining inactive when native rendering is disabled.
conditions.append('<condition>palaceFinaleStage6Rendered,tileAtPosition,96,80,1F34,0F213029')
card_clones=[]
for line in lines:
 if not line.startswith('[cardPal1&cardPal2&cardPal3&cardRendering&stageCardS&stageCardT&stageCardA&stageCardG&stageCardE&stageRandy'):continue
 if '<background>'in line and not any(n in line for n in ['Intermission_HD.png','Stage_Title_6.png','Stage_Lives_']):continue
 if not ('<tile>'in line or '<background>'in line):continue
 target=line.replace('&cardRendering','&palaceFinaleStage6Rendered')
 if '&stageNumber6'not in target:target=target.replace(']','&stageNumber6]',1)
 rules.append(target);card_clones.append(dict(source_rule=line,rule=target))
assert len(card_clones)==61,len(card_clones)
# Preserve the exact prior mapping text after removal of these marked blocks.
def block(name,ls):return '# BEGIN PALACE_FINALE '+name+'\n'+'\n'.join(ls)+'\n# END PALACE_FINALE '+name+'\n'
end=text.index('\n',text.rfind('<img>'))+1;text=text[:end]+block('IMAGES',['<img>Demonic_Palace_Finale_2x.png'])+text[end:]
at=text.index('# BEGIN PALACE_CONTINUATION CONDITIONS');text=text[:at]+block('CONDITIONS',conditions)+block('MAPPINGS',rules+backgrounds)+text[at:]+block('ALIASES',tail)
(P/'hires.txt').write_text(text);atlas.save(P/'Demonic_Palace_Finale_2x.png');atlas.save(A/'Demonic_Palace_Finale_2x.png')
(A/'registration.json').write_text(json.dumps(dict(atlas_index=index,atlas_cells=len(cache),scopes=scopes,mappings=records,clones=clones,conditions=conditions,backgrounds=backgrounds,guard_palettes=guards,card_clones=card_clones),indent=2)+'\n')
print('Palace finale:',len(rules)+len(tail),'tile rules;',len(backgrounds),'backgrounds;',len(cache),'cells')
