"""Level 3 opening: three native rooms, approved shared actors and new forest art."""
from pathlib import Path
import hashlib,json,re
import numpy as np
from PIL import Image,ImageDraw

root=Path(__file__).resolve().parents[1];pack=root/'build/Holy_Diver_(Tr)';art=root/'art/level3_opening'
text=(pack/'hires.txt').read_text();assert text.count('<img>')==40
patterns={int(k,16):bytes.fromhex(v)for k,v in json.loads((art/'native_patterns.json').read_text()).items()}
native_aliases={int(k,16):[int(x,16)for x in v]for k,v in json.loads((art/'native_aliases.json').read_text()).items()}
images=[l[5:]for l in text.splitlines()if l.startswith('<img>')]
defs={l[11:].split(',')[0]:l[11:].split(',')for l in text.splitlines()if l.startswith('<condition>')}
conditions=[];rules=[];aliases=[];records=[];atlas=Image.new('RGBA',(512,512));cache={}
rooms={'forest':(0x10,0x988a),'tree':(4,0x997a),'shaft':(4,0x99f2)}
scopes={}
for name,(room,ptr)in rooms.items():
 scope=f'l3_{name}Room&l3_{name}Lo&l3_{name}Hi';scopes[name]=scope
 for suffix,addr,val in [('Room',0x72,room),('Lo',0x78,ptr&255),('Hi',0x79,ptr>>8)]:conditions.append(f'<condition>l3_{name}{suffix},memoryCheckConstant,{addr:04X},==,{val:02X}')
def reg(im,size):
 im=im.convert('RGBA').resize(size,Image.Resampling.LANCZOS);a=im.getchannel('A').point(lambda a:255 if a>=128 else 0);im=im.convert('RGB').quantize(colors=64).convert('RGBA');im.putalpha(a);return im
def tile(t,pal,im,kind,scope=''):
 h=hashlib.sha256(im.tobytes()).hexdigest()
 if h not in cache:
  n=len(cache);xy=(n%32*16,n//32*16);assert xy[1]+16<=atlas.height;cache[h]=xy;atlas.paste(im,xy)
 x,y=cache[h];rules.append(('['+scope+']'if scope else '')+f'<tile>40,{t:04X},{pal},{x},{y},1,N');records.append(dict(identity=f'{t:04X}',palette=pal,xy=[x,y],kind=kind,scope=scope))
def mask(t,kind='hull'):
 b=patterns.get(t,bytes(16));a=np.array([[bool((b[y]|b[y+8])&(1<<(7-x)))for x in range(8)]for y in range(8)])
 if kind=='full':a[:]=True
 else:
  for y in range(8):
   xs=np.flatnonzero(a[y])
   if len(xs):a[y,xs[0]:xs[-1]+1]=True
  for x in range(8):
   ys=np.flatnonzero(a[:,x])
   if len(ys):a[ys[0]:ys[-1]+1,x]=True
 return Image.fromarray((a*255).astype('uint8')).resize((16,16),Image.Resampling.NEAREST)
empty=Image.new('RGBA',(16,16))
# Existing materials retain their approved colors. Only their registration is new.
floor=Image.open(root/'art/layers/50_floor.png').convert('RGBA').crop((256,864,320,928))
cap=reg(floor.crop((0,0,64,16)),(32,16));body=reg(floor.crop((0,16,64,48)),(32,32))
tree=Image.open(root/'art/layers/20_tree_and_branches.png').convert('RGBA')
bark=reg(Image.open(root/'art/generated/level3_bark_generated.png'),(96,32))
ba=np.array(bark);edge=((ba[0].astype(int)+ba[-1].astype(int))//2).astype('uint8');ba[0]=edge;ba[-1]=edge;bark=Image.fromarray(ba)
branch=reg(tree.crop((224,384,288,400)),(64,16))
wall=Image.open(root/'art/screen1_3/Nave_Background.png').convert('RGBA')
stone=reg(wall.crop((0,48,64,112)),(32,32))
observed=json.loads((art/'observed_backgrounds.json').read_text())
terrain_masks={}
for name,(room,ptr)in rooms.items():
 pals=observed[f'{ptr:04X}'];scope=scopes[name]
 # Include both native hot-lava phases, even if the sparse intake only caught one.
 if name=='forest':pals['0F161606']=pals.get('0F060616',[])
 for pal,ts in pals.items():
  for t in ts:
   if t==0x700:tile(t,pal,empty,'room space',scope);continue
   if name in ('forest','tree') and t<0x734:
    tile(t,pal,empty,'nonsolid distant forest',scope);continue
   if name=='shaft' and pal=='0F0F0A1A':
    tile(t,pal,empty,'nonsolid masonry wall',scope);continue
   if pal in ('0F161606','0F060616','0F122131'):
    # Identical native lava patterns may be rearranged in this bank.
    old=next((v for v in native_aliases.get(t,[])if 0x334<=v<=0x345),None)
    source=next((l for l in text.splitlines()if '<tile>'in l and l.split('<tile>')[1].split(',')[1:3]==[f'{old:04X}',pal]),None)if old is not None else None
    if source:
     f=source.split('<tile>')[1].split(',');f[1]=f'{t:04X}';rules.append(f'[{scope}]<tile>'+','.join(f));continue
    raise AssertionError(('lava alias missing',t,pal))
   if pal=='0F091929':
    # The six-column trunk and its actual branches remain bound to native cells.
    trunk_rows=[[0x752,0x753,0x754,0x755,0x75a,0x75b],[0x756,0x757,0x758,0x759,0x75c,0x75d]]
    locations={v:(x,y)for y,row in enumerate(trunk_rows)for x,v in enumerate(row)}
    col,row=locations.get(t,((t-0x762)%6,0))
    im=bark.crop((col*16,row*16,col*16+16,row*16+16))
    if 0x768<=t<=0x770:im=branch.crop(((t%4)*16,0,(t%4+1)*16,16))
    kind='wide tree bark and approved branches';geometry='full'if 0x752<=t<=0x761 else 'hull'
   elif name=='shaft' and pal=='0F0A1A29':
    im=stone.crop(((t%2)*16,((t//2)%2)*16,(t%2+1)*16,((t//2)%2+1)*16));kind='approved stone column material';geometry='full'if t in [0x744,0x745,0x746,0x747,0x748]else 'hull'
   else:
    im=cap.crop(((t%2)*16,0,(t%2+1)*16,16))if t in [0x734,0x735]else body.crop(((t%2)*16,((t//2)%2)*16,(t%2+1)*16,((t//2)%2+1)*16))
    kind='approved brown solid terrain';geometry='full'if t in [0x738,0x739,0x73a,0x73b,0x73c,0x73d]else 'hull'
   ma=mask(t,geometry);im.putalpha(ma);terrain_masks[f'{name}:{t:04X}:{pal}']=np.array(ma).tolist();tile(t,pal,im,kind,scope)
# Distant layers only activate on the matching room, palette and rendered bank.
bg=Image.open(root/'art/generated/level3_forest_generated.png').convert('RGB').resize((1024,480),Image.Resampling.LANCZOS)
a=np.array(bg).astype(float);edge=(a[:,0]+a[:,-1])/2
for x in range(24):
 w=(1-x/24)**2;a[:,x]=a[:,x]*(1-w)+edge*w;a[:,-1-x]=a[:,-1-x]*(1-w)+edge*w
bg=Image.fromarray(a.astype('uint8'));pan=Image.new('RGB',(4608,480))
for x in range(0,4608,1024):pan.paste(bg,(x,0))
pan.save(pack/'Stage3_Forest_Background.png')
backgrounds=[]
for name,(room,ptr)in rooms.items():
 for n,(pal,ts)in enumerate(observed[f'{ptr:04X}'].items()):
  for t in ts:
   guard=f'l3_{name}View_{n}_{t:04X}';conditions.append(f'<condition>{guard},tileAtPosition,128,16,{t:04X},{pal}')
   asset='Nave_Background.png'if name=='shaft'else 'Stage3_Forest_Background.png'
   sx=1 if name=='forest'else 0
   backgrounds.append(f'[{scopes[name]}&{guard}]<background>{asset},1,{sx},0,11,0,0')
# Player/HUD aliases retain exact native identity, approved rule order and pose anchors.
aliasdefs={}
def remap(sc):
 out=[]
 for term in sc.split('&')if sc else []:
  neg='!'if term.startswith('!')else '';name=term.lstrip('!');d=defs.get(name,[])
  if len(d)>4 and d[1]=='spriteNearby'and int(d[4],16)<0x100:
   q=d.copy();target=int(q[4],16)+0x600
   assert int(q[4],16)in native_aliases[target]
   name='l3copy_'+name;q[0]=name;q[4]=f'{target:04X}';aliasdefs[name]='<condition>'+','.join(q)
  out.append(neg+name)
 return '&'.join(out)
for line in text.splitlines():
 m=re.fullmatch(r'(?:\[([^]]+)\])?<tile>(.*)',line)
 if not m:continue
 sc,p=m[1]or'',m[2].split(',');idx=int(p[0]);t=int(p[1],16)
 if idx not in [18,19,20,21,22,23,26,27,31]or t>=0x74 or any(k in sc for k in ['pause','cardPal','lives']):continue
 if t not in native_aliases.get(t+0x600,[]):continue
 p[1]=f'{t+0x600:04X}';ns=remap(sc);aliases.append(('['+ns+']'if ns else '')+'<tile>'+','.join(p))
# Choose finished shared fallback cells for returning eyes, bats and their shots.
shared='\n'.join(r['rule']for r in json.loads((root/'art/shared_stage2/registration.json').read_text())['records'])
for target,olds in native_aliases.items():
 if not 0x6b0<=target<=0x6d0:continue
 # Preserve the known pose sequence, not merely the first identical tile:
 # folded/open bat lower cells share CHR bytes but use different HD paint.
 old=target-0x3d8 if 0x6b0<=target<=0x6b5 else target-0x41a if 0x6c0<=target<=0x6d0 else None
 if old is None:continue
 assert old in olds
 for line in shared.splitlines():
  if '<tile>'not in line:continue
  p=line.split('<tile>')[1].split(',')
  if int(p[1],16)!=old:continue
  p[1]=f'{target:04X}';aliases.append('<tile>'+','.join(p))
# Existing recovery and Blizzard cells are exact CHR copies; reuse their art.
for old,target in [(0x247,0x647),(0x248,0x648),(0x24e,0x64e),(0x24f,0x64f),(0x274,0x674)]:
 for line in shared.splitlines():
  if '<tile>'not in line:continue
  p=line.split('<tile>')[1].split(',')
  if int(p[1],16)==old and old in native_aliases.get(target,[]):p[1]=f'{target:04X}';aliases.append('<tile>'+','.join(p))
conditions+=list(aliasdefs.values())
# Register native emergence as two 16x8 frames, not one 16x16 sprite.
# The two larger forms share the exact head and left body cells.
source=Image.open(root/'art/generated/level3_ember_generated.png').convert('RGBA');cells={};poses=[]
raw=source.crop((0,0,source.width//3,source.height));raw=raw.crop(raw.getchannel('A').point(lambda a:255 if a>=128 else 0).getbbox())
for i in range(2):
 im=Image.new('RGBA',(32,16));im.paste(reg(raw,(32-i*4,16)),(i*2,0));rows=[[0x6b6+i*2,0x6b7+i*2]]
 for x,t in enumerate(rows[0]):cells[t]=im.crop((x*16,0,x*16+16,16))
 name=f'ember_emerge_{i}';im.save(art/f'{name}.png');poses.append(dict(name=name,palette='FF172737',rows=rows,size=[32,16]))
layouts=[[[0x6ba,0x6bb],[0x6bc,0x6bd]],[[0x6ba,0x6bb,None],[0x6bc,0x6be,0x6bf]]]
for i,rows in enumerate(layouts,1):
 raw=source.crop((i*source.width//3,0,(i+1)*source.width//3,source.height));raw=raw.crop(raw.getchannel('A').point(lambda a:255 if a>=128 else 0).getbbox());size=(len(rows[0])*16,32);im=reg(raw,size)
 for y,row in enumerate(rows):
  for x,t in enumerate(row):
   xy=(x*16,y*16)
   if t is None:im.paste(empty,xy);continue
   if t in cells:im.paste(cells[t],xy)
   else:cells[t]=im.crop((*xy,xy[0]+16,xy[1]+16))
 im.save(art/f'ember_{i}.png');poses.append(dict(name=f'ember_{i}',palette='FF172737',rows=rows,size=size))
for t,im in cells.items():tile(t,'FF172737',im,'new ember creature')
source=Image.open(root/'art/generated/level3_flyer_generated.png').convert('RGBA')
for i in range(2):
 raw=source.crop((i*source.width//2,0,(i+1)*source.width//2,source.height));raw=raw.crop(raw.getchannel('A').point(lambda a:255 if a>=128 else 0).getbbox());im=reg(raw,(32,32));im.save(art/f'flyer_{i}.png');rows=[]
 for y in range(2):
  row=[]
  for x in range(2):
   t=0x6e7+i*4+y*2+x;row.append(t);tile(t,'FF162631',im.crop((x*16,y*16,x*16+16,y*16+16)),'new crimson flyer')
  rows.append(row)
 poses.append(dict(name=f'flyer_{i}',palette='FF162631',rows=rows,size=[32,32]))
def block(name,items):return '# BEGIN LEVEL3_OPENING '+name+'\n'+'\n'.join(items)+'\n# END LEVEL3_OPENING '+name+'\n'
end=text.index('\n',text.rfind('<img>'))+1;text=text[:end]+block('IMAGES',['<img>Stage3_Opening_Tiles_2x.png'])+text[end:]
lines=text.splitlines(keepends=True);first=next(i for i,l in enumerate(lines)if '<tile>'in l or '<background>'in l)
lines[first:first]=[block('CONDITIONS',conditions),block('MAPPINGS',rules+backgrounds)]
(pack/'hires.txt').write_text(''.join(lines)+block('ALIASES',aliases));atlas.save(pack/'Stage3_Opening_Tiles_2x.png');atlas.save(art/'Stage3_Opening_Tiles_2x.png')
(art/'poses.json').write_text(json.dumps(poses,indent=2)+'\n')
(art/'registration.json').write_text(json.dumps(dict(tile_rules=len(rules)+len(aliases),conditions=len(conditions),background_rules=len(backgrounds),alias_rules=len(aliases),atlas_cells=len(cache),rooms=rooms,mappings=records,terrain_masks=terrain_masks,previous_artwork_modified=False),indent=2)+'\n')
print('Level 3 opening:',len(rules),'new registrations;',len(aliases),'approved-art aliases; three rooms.')
