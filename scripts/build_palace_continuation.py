"""Extend approved Palace scenery through the four recorded late chambers."""
from pathlib import Path
import hashlib,json,re
import numpy as np
from PIL import Image
R=Path(__file__).resolve().parents[1];P=R/'build/Holy_Diver_(Tr)';A=R/'art/level5_continuation'
text=(P/'hires.txt').read_text();prior=json.loads((R/'evidence/0.22.2-pack-sha256.json').read_text())
assert hashlib.sha256(text.encode()).hexdigest()==prior['hires.txt']
lines=text.splitlines();images=[l[5:]for l in lines if l.startswith('<img>')];index=len(images);assert index==60
patterns={int(k,16):bytes.fromhex(v)for k,v in json.loads((A/'native_patterns.json').read_text()).items()}
inv=json.loads((A/'inventory.json').read_text());defs={l[11:].split(',')[0]:l[11:].split(',')for l in lines if l.startswith('<condition>')}
conditions=[];rules=[];backgrounds=[];records=[];clones=[];scopes={};cache={};atlas=Image.new('RGBA',(256,256))
for room,mode in [('8AE6',16),('8BD6',4),('8C4E',16),('8D3E',4)]:
 names=[]
 for suffix,addr,val in [('Mode',0x72,mode),('Lo',0x78,int(room,16)&255),('Hi',0x79,int(room,16)>>8)]:
  name='palaceContinue'+room+suffix;conditions.append(f'<condition>{name},memoryCheckConstant,{addr:04X},==,{val:02X}');names.append(name)
 scopes[room]='&'.join(names)
def tile(t,pal,im,scope,kind):
 h=hashlib.sha256(im.tobytes()).hexdigest()
 if h not in cache:
  n=len(cache);xy=(n%16*16,n//16*16);assert xy[1]<256;cache[h]=xy;atlas.paste(im,xy)
 x,y=cache[h];rule=f'[{scope}]<tile>{index},{t:04X},{pal},{x},{y},1,N'
 rules.append(rule);records.append(dict(tile=f'{t:04X}',palette=pal,xy=[x,y],scope=scope,kind=kind,rule=rule))
def clone(source,target,kind):
 rules.append(target);clones.append(dict(source_rule=source,rule=target,kind=kind))
def hull(t):
 b=patterns[t];a=np.array([[255 if (b[y]|b[y+8])>>(7-x)&1 else 0 for x in range(8)]for y in range(8)],dtype=np.uint8)
 for y in range(8):
  xs=np.flatnonzero(a[y])
  if len(xs):a[y,xs[0]:xs[-1]+1]=255
 for x in range(8):
  ys=np.flatnonzero(a[:,x])
  if len(ys):a[ys[0]:ys[-1]+1,x]=255
 return Image.fromarray(a).resize((16,16),Image.Resampling.NEAREST)
material=Image.open(R/'art/level5_repair/stair_material.png').convert('RGBA');empty=Image.new('RGBA',(16,16))
distant={'0F071727','0F0F0121','0F0F0717','0F0F0111'};solid={'0F040F24','0F001030','0F0B1B3B'}
for room,pals in inv['visible_backgrounds'].items():
 for pal,keys in pals.items():
  if pal not in distant|solid:continue
  for key in keys:
   t=int(key,16)
   if pal in distant:im=empty;kind='distant palace wall'
   else:
    x,y=t%4*16,t//4%4*16;im=material.crop((x,y,x+16,y+16));im.putalpha(hull(t));kind='native structural stone'
   for bank in [0,0x200]:
    assert patterns[t]==patterns[t+bank];tile(t+bank,pal,im,scopes[room],kind)
# Whole bank guard families cover camera motion and both physical CHR copies.
guard_palettes={
 '8AE6':['0F071727','0F0F0121','0F040F24','0F060616','0F161606','0F122131'],
 '8BD6':['0F0F0717','0F001030','0F0F0121','0F040F24','0F161606'],
 '8C4E':['0F0F0111','0F0B1B3B','0F0F0717','0F001030'],
 '8D3E':['0F0F0111','0F001030','0F0B1B3B']}
for room,palettes in guard_palettes.items():
 for pal in palettes:
  for base in [0x1100,0x1300]:
   for t in range(base,base+256):
    name=f'palaceContinueView{room}_{t:04X}_{pal}';conditions.append(f'<condition>{name},tileAtPosition,128,16,{t:04X},{pal}')
    backgrounds.append(f'[{scopes[room]}&{name}]<background>Demonic_Palace_Interior.png,1,0,0,1,0,0')
oldreg=json.loads((R/'art/level5/registration.json').read_text())
for room in ['8AE6','8BD6']:
 for entry in oldreg['clones']:
  if entry['kind']not in ['approved lava pool and ice','approved animated lava falls and ice']:continue
  source=entry['rule'];clone(source,source.replace(oldreg['scopes']['850A'],scopes[room]),entry['kind'])
# Native bytes prove all three recorded skeleton palettes use the same poses.
for pal in ['FF160730','FF110130','FF0C1C30']:
 for j in range(18):
  src,dst=0x10e8+j,0x12e5+j;assert patterns[src]==patterns[dst]
  source=next(l for l in lines if re.fullmatch(r'<tile>57,'+f'{src:04X},FF110130,.*',l))
  f=source[6:].split(',');f[1]=f'{dst:04X}';f[2]=pal;clone(source,'<tile>'+','.join(f),'byte-identical skeleton and bone')
nextreg=json.loads((R/'art/level5_next/registration.json').read_text())
for entry in nextreg['mappings']:
 if entry['kind']=='rising armored sentry':
  source=entry['rule'];clone(source,source.replace(nextreg['scopes']['897E'],scopes['8C4E']),'returning rising sentry')
# These small recovery drops retain the approved visibility treatment.
for room in scopes:
 for entry in oldreg['mappings']:
  if entry['scope']!=oldreg['scopes']['850A']or entry['kind']not in ['visible heart','visible magic']:continue
  source=entry['rule'];f=source.split('<tile>')[1].split(',');t=int(f[1],16);assert patterns[t]==patterns[t+0x200];f[1]=f'{t+0x200:04X}'
  clone(source,'['+scopes[room]+']<tile>'+','.join(f),'existing '+entry['kind'])
# The lift repeats a two-by-two native block twice. Register its complete
# 32x32 HD unit before slicing; native OAM supplies the unchanged 64x32 span.
lift=material.crop((0,0,32,32));mask=Image.new('L',(32,32))
for j,t in enumerate(range(0x12f7,0x12fb)):mask.paste(hull(t),(j%2*16,j//2*16))
lift.putalpha(mask);lift.save(A/'lift_unit.png')
for j,t in enumerate(range(0x12f7,0x12fb)):
 x,y=j%2*16,j//2*16;tile(t,'FF003008',lift.crop((x,y,x+16,y+16)),scopes['8BD6'],'moving stone lift')
# Definitions are local and precede every use. Preserve native lava phases.
reuse={};local_conditions={l[11:].split(',')[0]for l in conditions}
def ordered(line):
 if not line.startswith('['):return line
 head,rest=line[1:].split(']',1);terms=[]
 for term in head.split('&'):
  neg='!'if term.startswith('!')else'';name=term.lstrip('!')
  if name not in local_conditions|{'hmirror','vmirror','bgpriority'}:
   if name not in reuse:
    new='palaceContinueReuse_'+name;d=defs[name].copy();d[0]=new;conditions.append('<condition>'+','.join(d));reuse[name]=new
   name=reuse[name]
  terms.append(neg+name)
 return '['+'&'.join(terms)+']'+rest
rules=[ordered(l)for l in rules]
for e in records+clones:e['rule']=ordered(e['rule'])
# Carry the accepted 30/31 flash behavior into every new background rule.
normal_conditions={l[11:].split(',')[0]:l[11:].split(',')for l in conditions};flash_names={}
def flash_head(head,phase):
 terms=[]
 for term in head.split('&'):
  neg='!'if term.startswith('!')else'';name=term.lstrip('!')
  if name in {'hmirror','vmirror','bgpriority'}:terms.append(term);continue
  key=(name,phase)
  if key not in flash_names:
   new='palaceContinueFlash'+phase+'_'+name;d=normal_conditions[name].copy();d[0]=new
   if d[1]in ['tileAtPosition','tileNearby']and d[5].startswith('0F'):d[5]=phase+d[5][2:]
   conditions.append('<condition>'+','.join(d));flash_names[key]=new
  terms.append(neg+flash_names[key])
 return '&'.join(terms)
flash=[]
for phase in ['30','31']:
 for source in rules.copy()+backgrounds.copy():
  m=re.fullmatch(r'\[([^]]+)\]<(tile|background)>(.*)',source)
  if not m:continue
  f=m[3].split(',')
  if m[2]=='tile':
   if not f[2].startswith('0F'):continue
   f[2]=phase+f[2][2:]
  else:f[0]='Demonic_Palace_Interior_Flash.png'
  rule='['+flash_head(m[1],phase)+']<'+m[2]+'>'+','.join(f);flash.append(dict(source_rule=source,rule=rule,phase=phase,kind=m[2]))
# Place flash rules first; all scopes remain disjoint from the prior rooms.
def block(name,ls):return '# BEGIN PALACE_CONTINUATION '+name+'\n'+'\n'.join(ls)+'\n# END PALACE_CONTINUATION '+name+'\n'
end=text.index('\n',text.rfind('<img>'))+1;text=text[:end]+block('IMAGES',['<img>Demonic_Palace_Continuation_2x.png'])+text[end:]
at=text.index('# BEGIN PALACE_FLASH CONDITIONS');text=text[:at]+block('CONDITIONS',conditions)+block('MAPPINGS',[e['rule']for e in flash]+rules+backgrounds)+text[at:]
(P/'hires.txt').write_text(text);atlas.save(P/'Demonic_Palace_Continuation_2x.png');atlas.save(A/'Demonic_Palace_Continuation_2x.png')
(A/'registration.json').write_text(json.dumps(dict(atlas_index=index,atlas_cells=len(cache),scopes=scopes,mappings=records,clones=clones,conditions=conditions,backgrounds=backgrounds,flash=flash,guard_palettes=guard_palettes),indent=2)+'\n')
print('Palace continuation:',len(rules),'normal tile rules;',len(backgrounds),'normal backgrounds;',len(flash),'flash rules;',len(cache),'atlas cells')
