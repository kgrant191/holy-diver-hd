"""Demonic Palace stair-hall continuity and the two following lava rooms."""
from pathlib import Path
import hashlib,json,re
import numpy as np
from PIL import Image
from prepare_palace_next import prepare
R=Path(__file__).resolve().parents[1];P=R/'build/Holy_Diver_(Tr)';A=R/'art/level5_next'
text=(P/'hires.txt').read_text();prior=json.loads((R/'evidence/0.21.1-pack-sha256.json').read_text());assert hashlib.sha256(text.encode()).hexdigest()==prior['hires.txt']
lines=text.splitlines();images=[l[5:]for l in lines if l.startswith('<img>')];index=len(images);assert index==59
patterns={int(k,16):bytes.fromhex(v)for k,v in json.loads((A/'native_patterns.json').read_text()).items()};inv=json.loads((A/'inventory.json').read_text())
defs={l[11:].split(',')[0]:l[11:].split(',')for l in lines if l.startswith('<condition>')}
conditions=[];rules=[];tail=[];records=[];clones=[];backgrounds=[];scopes={};atlas=Image.new('RGBA',(256,256));cache={}
for room,mode in [('888E',0x10),('897E',0x10),('8A6E',8)]:
 names=[]
 for suffix,addr,val in [('Mode',0x72,mode),('Lo',0x78,int(room,16)&255),('Hi',0x79,int(room,16)>>8)]:
  name='palaceNext'+room+suffix;conditions.append(f'<condition>{name},memoryCheckConstant,{addr:04X},==,{val:02X}');names.append(name)
 scopes[room]='&'.join(names)
def emit(t,pal,im,scope,kind):
 h=hashlib.sha256(im.tobytes()).hexdigest()
 if h not in cache:
  n=len(cache);xy=(n%16*16,n//16*16);assert xy[1]<256;cache[h]=xy;atlas.paste(im,xy)
 x,y=cache[h];rule=('['+scope+']'if scope else '')+f'<tile>{index},{t:04X},{pal},{x},{y},1,N'
 rules.append(rule);records.append(dict(tile=f'{t:04X}',palette=pal,scope=scope,kind=kind,xy=[x,y],rule=rule))
def clone(source,target,kind,destination=None):
 (rules if destination is None else destination).append(target);clones.append(dict(source_rule=source,rule=target,kind=kind))
def hull(t):
 b=patterns[t];a=np.array([[255 if ((b[y]|b[y+8])>>(7-x))&1 else 0 for x in range(8)]for y in range(8)],dtype=np.uint8)
 for y in range(8):
  xs=np.flatnonzero(a[y])
  if len(xs):a[y,xs[0]:xs[-1]+1]=255
 for x in range(8):
  ys=np.flatnonzero(a[:,x])
  if len(ys):a[ys[0]:ys[-1]+1,x]=255
 return Image.fromarray(a).resize((16,16),Image.Resampling.NEAREST)
material=Image.open(R/'art/level5_repair/stair_material.png').convert('RGBA');empty=Image.new('RGBA',(16,16))
for room,pals in inv['visible_backgrounds'].items():
 for pal,tiles in pals.items():
  if pal not in ['0F001030','0F040F24','0F0F0717','0F071727']:continue
  for key in tiles:
   t=int(key,16)
   if pal in ['0F0F0717','0F071727']:im=empty;kind='distant palace wall reveal'
   else:
    x,y=t%4*16,t//4%4*16;im=material.crop((x,y,x+16,y+16));im.putalpha(hull(t));kind='native stair stone'
   for bank in [0,0x200]:
    assert patterns[t]==patterns[t+bank];emit(t+bank,pal,im,scopes[room],kind)
 # A complete bank family prevents viewport-dependent background holes.
 # Exact rendered palettes exclude native all-black transitions and flashes.
 guard_pals=['0F0F0717','0F001030']if room=='888E'else ['0F071727','0F040F24','0F060616','0F161606','0F122131']
 if room=='897E':guard_pals+=['0F0F0717','0F001030']
 for pal in guard_pals:
  for base in [0x1100,0x1300]:
   for t in range(base,base+256):
    name=f'palaceNextView{room}_{t:04X}_{pal}';conditions.append(f'<condition>{name},tileAtPosition,128,16,{t:04X},{pal}')
    backgrounds.append(f'[{scopes[room]}&{name}]<background>Demonic_Palace_Interior.png,1,0,0,1,0,0')
# Preserve every native lava animation/freeze condition while changing scope.
oldreg=json.loads((R/'art/level5/registration.json').read_text())
for room in ['897E','8A6E']:
 for entry in oldreg['clones']:
  if entry['kind']not in ['approved lava pool and ice','approved animated lava falls and ice']:continue
  source=entry['rule'];target=source.replace(oldreg['scopes']['850A'],scopes[room]);clone(source,target,entry['kind'])
# Whole pose-conditioned Randy and HUD aliases, with corresponding native
# sprite-neighbor identities. Broad aliases remain after all specific rules.
copy_defs={}
for line in lines:
 m=re.fullmatch(r'(?:\[([^]]+)\])?<tile>(.*)',line)
 if not m:continue
 head=m[1]or'';f=m[2].split(',');src=int(f[1],16)
 if not 0xa00<=src<=0xa89:continue
 dst=src+0x800;assert patterns[src]==patterns[dst]
 if any(defs.get(t.lstrip('!'),['',''])[1]=='memoryCheckConstant'and int(defs[t.lstrip('!')][2],16)in [0x72,0x78,0x79]for t in head.split('&')if t):continue
 terms=[]
 for term in head.split('&')if head else []:
  neg='!'if term.startswith('!')else'';name=term.lstrip('!');d=defs.get(name)
  if d and d[1]=='spriteNearby'and 0xa00<=int(d[4],16)<=0xa89:
   new='palaceNextCopy_'+name
   if new not in copy_defs:
    v=d.copy();v[0]=new;v[4]=f'{int(v[4],16)+0x800:04X}';copy_defs[new]='<condition>'+','.join(v)
   name=new
  terms.append(neg+name)
 f[1]=f'{dst:04X}';clone(line,('['+'&'.join(terms)+']'if terms else'')+'<tile>'+','.join(f),'exact player HUD and shared effects',rules if head else tail)
conditions+=list(copy_defs.values())
# Native-byte-identical returning enemies, pickups and lightning. Their whole
# sources and animation layouts already exist; only bank/palette differs.
families=[(0x128e,0x108e,12,'FF301116','FF301116','Thunder'),(0x129a,0x0a8e,4,'FF301116','FF301116','pickup'),(0x129e,0x109a,2,'FF301116','FF301116','wings'),(0x12a4,0x0ae2,12,'FF003008','FF003008','floating guardian'),(0x12b0,0x0afc,1,'FF301116','FF301116','curved shot'),(0x12c4,0x02b7,33,'FF162730','FF160730','walking dragon')]
for dst,src,count,oldpal,newpal,kind in families:
 for j in range(count):
  assert patterns[dst+j]==patterns[src+j],(kind,j)
  candidates=[l for l in lines if re.fullmatch(r'<tile>\d+,'+f'{src+j:04X},{oldpal},.*',l)]
  assert candidates,(kind,src+j)
  source=candidates[0];f=source.split('<tile>')[1].split(',');f[1]=f'{dst+j:04X}';f[2]=newpal
  clone(source,'<tile>'+','.join(f),'native byte alias: '+kind)
# Existing room-specific small drops and transformation stars carry forward.
for room in scopes:
 for entry in oldreg['mappings']:
  if entry['scope'].split('&')[:3]!=oldreg['scopes']['850A'].split('&'):continue
  if entry['kind']not in ['visible heart','visible magic','transformation star']:continue
  source=entry['rule'];f=source.split('<tile>')[1].split(',');t=int(f[1],16)
  if room!='888E':assert patterns[t]==patterns[t+0x200];f[1]=f'{t+0x200:04X}'
  head=source[:source.index('<tile>')].replace(oldreg['scopes']['850A'],scopes[room]);clone(source,head+'<tile>'+','.join(f),'existing '+entry['kind'])
im=prepare();seen={}
for key,x,y in json.loads((A/'sentry_layout.json').read_text()):
 part=im.crop((x,y,x+16,y+16))
 if key in seen:assert seen[key]==part.tobytes();continue
 seen[key]=part.tobytes();emit(int(key,16),'FF0C1C30',part,scopes['897E'],'rising armored sentry')
# New aliases precede older mappings, so clone any later definition locally.
early={l[11:].split(',')[0]for l in conditions}|{'hmirror','vmirror','bgpriority'};reuse={}
def ordered(line):
 if not line.startswith('['):return line
 head,rest=line[1:].split(']',1);terms=[]
 for term in head.split('&'):
  neg='!'if term.startswith('!')else'';name=term.lstrip('!')
  if name not in early:
   if name not in reuse:
    new='palaceNextReuse_'+name;d=defs[name].copy();d[0]=new;conditions.append('<condition>'+','.join(d));reuse[name]=new
   name=reuse[name]
  terms.append(neg+name)
 return '['+'&'.join(terms)+']'+rest
rules=[ordered(l)for l in rules];tail=[ordered(l)for l in tail];backgrounds=[ordered(l)for l in backgrounds]
for entry in records+clones:entry['rule']=ordered(entry['rule'])
def block(name,ls):return '# BEGIN PALACE_NEXT '+name+'\n'+'\n'.join(ls)+'\n# END PALACE_NEXT '+name+'\n'
end=text.index('\n',text.rfind('<img>'))+1;text=text[:end]+block('IMAGES',['<img>Demonic_Palace_Next_2x.png'])+text[end:]
start=text.index('# BEGIN PALACE_REPAIR CONDITIONS');text=text[:start]+block('CONDITIONS',conditions)+block('MAPPINGS',rules+backgrounds)+text[start:]+block('ALIASES',tail)
(P/'hires.txt').write_text(text);atlas.save(P/'Demonic_Palace_Next_2x.png');atlas.save(A/'Demonic_Palace_Next_2x.png')
(A/'registration.json').write_text(json.dumps(dict(atlas_index=index,atlas_cells=len(cache),scopes=scopes,mappings=records,clones=clones,conditions=conditions,backgrounds=backgrounds),indent=2)+'\n')
print('Palace next:',len(rules)+len(tail),'tiles,',len(backgrounds),'background guards,',len(cache),'cells')
