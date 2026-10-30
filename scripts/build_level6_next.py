"""Carry the citadel through the recorded skull corridor and next-room entry."""
from pathlib import Path
import hashlib, json, re
import numpy as np
from PIL import Image
from verify_level6_opening_rules import native_hull

R=Path(__file__).resolve().parents[1];P=R/'build/Holy_Diver_(Tr)';A=R/'art/level6_next'
text=(P/'hires.txt').read_text();prior=json.loads((R/'evidence/0.25.1-pack-sha256.json').read_text())
assert hashlib.sha256(text.encode()).hexdigest()==prior['hires.txt']
lines=text.splitlines();images=[l[5:]for l in lines if l.startswith('<img>')];index=len(images);assert index==64
patterns={int(k,16):bytes.fromhex(v)for k,v in json.loads((R/'art/level6_opening/native_patterns.json').read_text()).items()}
defs={l[11:].split(',')[0]:l[11:].split(',')for l in lines if l.startswith('<condition>')}
opening=json.loads((R/'art/level6_opening/registration.json').read_text())
repair=json.loads((R/'art/level6_repair/registration.json').read_text())
inv=json.loads((A/'inventory.json').read_text())
conditions=[];rules=[];tail=[];records=[];clones=[];backgrounds=[];scopes={};cache={};copies={}
atlas=Image.new('RGBA',(256,256));parsed=[]
for line in lines:
 m=re.fullmatch(r'(?:\[([^]]+)\])?<tile>(.*)',line)
 if m:parsed.append((line,m[1]or'',m[2].split(',')))
for room,mode in [('9F3B',16),('A02B',4)]:
 terms=[]
 for suffix,addr,val in [('Mode',0x72,mode),('Lo',0x78,int(room,16)&255),('Hi',0x79,int(room,16)>>8)]:
  name='citadelNext'+room+suffix;conditions.append(f'<condition>{name},memoryCheckConstant,{addr:04X},==,{val:02X}');terms.append(name)
 scopes[room]='&'.join(terms)
def dependency(term,bank=0):
 neg='!'if term.startswith('!')else'';name=term.lstrip('!')
 if name in {'hmirror','vmirror','bgpriority'}:return term
 key=(name,bank)
 if key not in copies:
  d=defs[name].copy();new='citadelNextReuse'+str(len(copies));copies[key]=new;d[0]=new
  assert d[1]!='tileNearby','No new background neighbor probes'
  if d[1]=='spriteNearby'and bank and 0xa00<=int(d[4],16)<=0xa8d:
   src=int(d[4],16);assert patterns[src]==patterns[src+bank];d[4]=f'{src+bank:04X}'
  conditions.append('<condition>'+','.join(d))
 return neg+copies[key]
def clone(source,t,pal,scope,kind,terms=(),bank=0,destination=None):
 f=source.split('<tile>')[1].split(',');src=int(f[1],16);assert patterns[src]==patterns[t],(kind,hex(src),hex(t))
 f[1]=f'{t:04X}';f[2]=pal;head='&'.join(([scope]if scope else[])+[dependency(k,bank)for k in terms])
 rule=('['+head+']'if head else'')+'<tile>'+','.join(f)
 (rules if destination is None else destination).append(rule)
 clones.append(dict(source_rule=source,rule=rule,kind=kind,source_tile=f'{src:04X}',tile=f'{t:04X}',palette=pal))
def emit(t,pal,im,scope,kind):
 h=hashlib.sha256(im.tobytes()).hexdigest()
 if h not in cache:
  n=len(cache);xy=(n%16*16,n//16*16);assert xy[1]<256;cache[h]=xy;atlas.paste(im,xy)
 x,y=cache[h];rule=f'[{scope}]<tile>{index},{t:04X},{pal},{x},{y},1,N';rules.append(rule)
 records.append(dict(tile=f'{t:04X}',palette=pal,xy=[x,y],scope=scope,kind=kind,rule=rule))
def hull(t):return Image.fromarray(native_hull(patterns[t]).astype(np.uint8)*255)
empty=Image.new('RGBA',(16,16));stone=Image.open(R/'art/level6_opening/rock_material.png').convert('RGBA')
# Every older citadel foreground rule is reused exactly, with the new scope
# and both indistinguishable native background-bank copies.
for reg in [opening,repair]:
 donor_scope=reg['scopes']['9BB7']
 entries=reg['mappings']+reg.get('clones',[])
 for e in entries:
  source=e['rule'];m=re.fullmatch(r'\[([^]]+)\]<tile>(.*)',source)
  if not m or not m[1].startswith(donor_scope):continue
  f=m[2].split(',');t=int(f[1],16)
  if not 0x1700<=t<0x1800:continue
  extra=m[1].split('&')[3:]
  for room in scopes:
   for shift in [0,0x200]:clone(source,t+shift,f[2],scopes[room],'existing citadel terrain',extra)
# Additional native units are registered whole before slicing. Shared cells
# retain one source across all rooms, palettes and physical CHR copies.
groups={
 'corridor_body':[[0x1795,0x1796],[0x1797,0x1798]],
 'corridor_inset':[[0x179f,0x17a0],[0x17a1,0x17a2]],
 'corridor_ceiling':[[0x1799,0x179a,0x179b,0x179c],[0x179d,0x179e,None,None]],
 'corridor_corner':[[0x17a3,0x17a4],[0x17a5,0x17a6]],
 'corridor_floor':[[0x17ab,0x17ac],[0x17ad,0x17ae]],
 'entry_base':[[0x17e3,0x17e4],[0x17e5,0x17e6]]}
cells={}
for name,layout in groups.items():
 im=stone.crop((0,0,len(layout[0])*16,len(layout)*16));mask=Image.new('L',im.size)
 for y,row in enumerate(layout):
  for x,t in enumerate(row):
   if t is None:continue
   mask.paste(hull(t),(16*x,16*y))
 im.putalpha(mask);im.save(A/(name+'.png'))
 for y,row in enumerate(layout):
  for x,t in enumerate(row):
   if t is not None:cells[t]=im.crop((16*x,16*y,16*x+16,16*y+16))
old_cells={int(e['tile'],16):e['rule']for e in opening['mappings']if e['scope']==opening['scopes']['9BB7']and e['palette']=='0F061636'}
solid=set(opening['solid_tiles'])|set(cells)|set(range(0x17b4,0x17b8))
for room in scopes:
 for pal,tiles in inv['visible_backgrounds'][room].items():
  if pal in ['0F061636','0F162738','0F072830']:solid.update(int(t,16)for t in tiles)
solid.discard(0x1700)
wall=set(opening['wall_tiles'])|set(range(0x178d,0x1795))|set(range(0x17a7,0x17ab))|set(range(0x17af,0x17b4))
for room,scope in scopes.items():
 for phase in ['0F','30','31']:
  for suffix in ['061636','162738','072830']:
   for shift in [0,0x200]:
    emit(0x1700+shift,phase+suffix,empty,scope,'empty native space')
    for t in sorted(solid):
     if t in old_cells:
      clone(old_cells[t],t+shift,phase+suffix,scope,'existing structural cell');continue
     if 0x17b4<=t<0x17b8:
      source=next(e['rule']for e in repair['mappings']if e['tile']==f'{t:04X}'and e['palette']=='0F061636')
      clone(source,t+shift,phase+suffix,scope,'existing upper ceiling');continue
     if t in cells:im=cells[t]
     else:
      x,y=t%4*16,t//4%4*16;im=stone.crop((x,y,x+16,y+16));im.putalpha(hull(t))
     emit(t+shift,phase+suffix,im,scope,'native structural stone')
  for suffix in ['071727','0F0717','172737']:
   for t in sorted(wall):
    for shift in [0,0x200]:emit(t+shift,phase+suffix,empty,scope,'distant wall')
# Exact pose-conditioned Randy, HUD, items and effects; specific rules before
# broad aliases, with matching sprite-neighbor signatures in the new bank.
for source,head,f in parsed:
 t=int(f[1],16)
 if not 0xa00<=t<=0xa8d:continue
 terms=head.split('&')if head else[]
 if any(defs.get(k.lstrip('!'),['',''])[1]=='memoryCheckConstant'and int(defs[k.lstrip('!')][2],16)in [0x72,0x78,0x79]for k in terms):continue
 clone(source,t+0xe00,f[2],'','exact player HUD effects',terms,0xe00,rules if head else tail)
for pal,donor in [('FF300036','FF300036'),('FF221136','FF221136'),('FF190927','FF300036')]:
 for offset in [0x4e,0x4f]:
  source=next(l for l in lines if l.startswith(f'<tile>29,{0x200+offset:04X},{donor},'))
  clone(source,0x1800+offset,pal,'','accepted 1-up',destination=tail)
# Native bytes prove the complete sentinel, flying skull and projectile reuse.
for dst,src,count,oldpal,newpal,atlas_id,kind in [
 (0x18a9,0x0cbe,53,'FF102030','FF000F30',51,'silver armored sentinel'),
 (0x18df,0x008c,8,'FF301116','FF301116',28,'returning flying skull'),
 (0x18f9,0x0694,1,'FF301116','FF301116',42,'existing round projectile'),
 (0x188e,0x108e,12,'FF301116','FF301116',57,'Thunder')]:
 for j in range(count):
  candidates=[l for l,head,f in parsed if int(f[1],16)==src+j and f[2]==oldpal and int(f[0])==atlas_id]
  assert candidates,(kind,hex(src+j));source=candidates[0]
  for scope in scopes.values():clone(source,dst+j,newpal,scope,kind)
# 18EB is a new one-cell shot identity in the sentinel's monochrome palette.
# Reuse the finished round fireball as an art source, not a claimed CHR alias.
shot_source=next(l for l,head,f in parsed if int(f[1],16)==0x694 and f[2]=='FF301116'and int(f[0])==42)
for scope in scopes.values():
 f=shot_source.split('<tile>')[1].split(',');f[1]='18EB';f[2]='FF000F30';rule=f'[{scope}]<tile>'+','.join(f);rules.append(rule)
 clones.append(dict(source_rule=shot_source,rule=rule,kind='one-cell shot art reuse',source_tile='0694',tile='18EB',palette='FF000F30',native_bytes_identical=False))
# New crawler poses at the actually visible next-room entrance. Register the
# entire body in its native cell union, then slice; no individual limb edits.
raw=Image.open(R/'art/generated/level6_crawler.png').convert('RGBA');layouts=json.loads((A/'crawler_layouts.json').read_text());pose_records=[]
for i,(name,layout)in enumerate(layouts.items()):
 crop=raw.crop((0,i*raw.height//2,raw.width,(i+1)*raw.height//2))
 box=crop.getchannel('A').point(lambda v:255 if v>=160 else 0).getbbox();crop=crop.crop(box)
 size=(48,32)if name=='rest'else(64,32);scaled=crop.resize(size,Image.Resampling.LANCZOS)
 # Smoothly fit the complete image around the missing native corner cell.
 # The tail/claw stays intact instead of being cut by the cell union.
 pose=Image.new('RGBA',size)
 for x in range(size[0]):
  inset=round(16*max(0,min(1,(32-x)/16)))if name=='rest'else round(16*max(0,min(1,(x-32)/16)))
  column=scaled.crop((x,0,x+1,32)).resize((1,32-inset),Image.Resampling.LANCZOS)
  pose.paste(column,(x,inset))
 alpha=np.array(pose.getchannel('A'))>=160;union=np.zeros((size[1],size[0]),bool)
 for key,x,y in layout:union[y*2:y*2+16,x*2:x*2+16]=True
 clipped=int((alpha&~union).sum());assert clipped==0;alpha&=union
 pose=pose.convert('RGB').quantize(colors=64).convert('RGBA');pose.putalpha(Image.fromarray(alpha.astype(np.uint8)*255));pose.save(A/f'crawler_{name}.png')
 pose_records.append(dict(name=name,size=size,layout=layout,clipped_native_empty_cell_pixels=clipped))
 for key,x,y in layout:emit(int(key,16),'FF072630',pose.crop((x*2,y*2,x*2+16,y*2+16)),scopes['A02B'],'whole crawler '+name)
# Full rendered-bank guards preserve scroll, pause, blackouts and native
# Thunder/pickup phases. The movie contains no cast in these new rooms.
guard_palettes=sorted(set(opening['guard_palettes'])|{'162738','0F0717'})
for room,scope in scopes.items():
 for phase in ['0F','30','31']:
  for suffix in guard_palettes:
   pal=phase+suffix
   for base in [0x1700,0x1900]:
    for t in range(base,base+256):
     name=f'citadelNextView{room}_{t:04X}_{pal}';conditions.append(f'<condition>{name},tileAtPosition,128,16,{t:04X},{pal}')
     image='Final_Citadel_Interior'+('_Flash'if phase!='0F'else'')+'.png'
     backgrounds.append(f'[{scope}&{name}]<background>{image},1,0,0,1,0,0')
def block(section,entries):return '# BEGIN LEVEL6_NEXT '+section+'\n'+'\n'.join(entries)+'\n# END LEVEL6_NEXT '+section+'\n'
anchor='# END LEVEL6_REPAIR IMAGES\n';at=text.index(anchor)+len(anchor)
text=text[:at]+block('IMAGES',['<img>Final_Citadel_Next_2x.png'])+block('CONDITIONS',conditions)+block('MAPPINGS',rules+backgrounds)+text[at:]+block('ALIASES',tail)
(P/'hires.txt').write_text(text);atlas.save(P/'Final_Citadel_Next_2x.png');atlas.save(A/'Final_Citadel_Next_2x.png')
(A/'registration.json').write_text(json.dumps(dict(atlas_index=index,atlas_cells=len(cache),scopes=scopes,conditions=conditions,mappings=records,clones=clones,backgrounds=backgrounds,groups=groups,poses=pose_records,solid_tiles=sorted(solid),wall_tiles=sorted(wall),guard_palettes=guard_palettes),indent=2)+'\n')
print('Level 6 next:',len(rules)+len(tail),'tile rules;',len(backgrounds),'backgrounds;',len(cache),'new atlas cells')
