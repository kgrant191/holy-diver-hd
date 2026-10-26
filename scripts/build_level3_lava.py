"""Level 3 lava corridor, fish, shared Breaker effects and pause-menu boot."""
from pathlib import Path
import hashlib,json,re
import numpy as np
from PIL import Image

r=Path(__file__).resolve().parents[1];pack=r/'build/Holy_Diver_(Tr)';art=r/'art/level3_lava'
text=(pack/'hires.txt').read_text();assert text.count('<img>')==43
images=[l[5:]for l in text.splitlines()if l.startswith('<img>')]
atlas=Image.new('RGBA',(512,512));cache={};rules=[];records=[];poses=[];backgrounds=[]
conditions=['<condition>l3lavaRoom,memoryCheckConstant,0072,==,10','<condition>l3lavaLo,memoryCheckConstant,0078,==,A6','<condition>l3lavaHi,memoryCheckConstant,0079,==,9A']
scope='l3lavaRoom&l3lavaLo&l3lavaHi';patterns={int(k,16):bytes.fromhex(v)for k,v in json.loads((art/'native_patterns.json').read_text()).items()}
for i,pal in enumerate(['0F060616','0F161606','0F122131']):
 for j in range(1,4):conditions.append(f'<condition>l3lavaState{i}_{j},ppuMemoryCheckConstant,{0x3f04+j:04X},==,{pal[j*2:j*2+2]}')
states=[scope+'&'+'&'.join(f'l3lavaState{i}_{j}'for j in range(1,4))for i in range(3)]
def reg(im,size):
 im=im.convert('RGBA').resize(size,Image.Resampling.LANCZOS);alpha=im.getchannel('A').point(lambda v:255 if v>=128 else 0)
 im=im.convert('RGB').quantize(colors=64).convert('RGBA');im.putalpha(alpha);return im
def obj(path):
 im=Image.open(path).convert('RGBA');return im.crop(im.getchannel('A').point(lambda v:255 if v>=128 else 0).getbbox())
def cell(t,pal,im,kind,sc=''):
 assert im.size==(16,16)
 key=hashlib.sha256(im.tobytes()).hexdigest()
 if key not in cache:
  n=len(cache);xy=(n%32*16,n//32*16);assert xy[1]<512;cache[key]=xy;atlas.paste(im,xy)
 x,y=cache[key];rules.append(('['+sc+']'if sc else '')+f'<tile>43,{t:04X},{pal},{x},{y},1,N')
 records.append(dict(tile=f'{t:04X}',palette=pal,xy=[x,y],kind=kind,scope=sc))
def source_cell(line):
 f=line.split('<tile>')[1].split(',');x,y=map(int,f[3:5]);return Image.open(pack/images[int(f[0])]).convert('RGBA').crop((x,y,x+16,y+16))
def sprite(name,im,rows,pals,offsets=(0,)):
 im.save(art/(name+'.png'))
 for y,row in enumerate(rows):
  for x,t in enumerate(row):
   if t is None:continue
   for off in offsets:
    for pal in pals:cell(t+off,pal,im.crop((x*16,y*16,x*16+16,y*16+16)),name)
 poses.append(dict(name=name,rows=rows,palettes=pals,size=list(im.size),alias_offsets=list(offsets)))
# The collected boot uses a separate background-tile layout on the menu.
boot=Image.open(r/'art/level3_detail/boot.png').convert('RGBA')
for y,row in enumerate([[0x974,0x973],[0x972,0x971]]):
 for x,t in enumerate(row):cell(t,'0F172737',boot.crop((x*16,y*16,x*16+16,y*16+16)),'approved boot menu','pauseScreen&pauseMagicRow&pausedPalette')
# A single fish body keeps all six shared native cells identical across poses.
raw=obj(r/'art/generated/level3_fish_generated.png');fish=Image.new('RGBA',(48,48));fish.paste(reg(raw,(46,46)),(1,1))
arr=np.array(fish);assert not arr[:16,:16,3].any(),'Fish crosses absent upper-left native cell'
rows=[[None,0x6dd,0x6de],[0x6df,0x6e0,0x6e1],[0x6e2,0x6e3,0x6e4]]
sprite('fish_0',fish,rows,['FF301627'])
alt=arr.copy()
for y in range(16,48):
 # Flex the rightmost fin while leaving its joining pixels in place.
 for x in range(36,48):
  sy=min(47,max(16,y+round(2*(x-36)/11)));alt[y,x]=arr[sy,x]
alt=Image.fromarray(alt);alt.save(art/'fish_1.png')
for t,y in [(0x6e5,16),(0x6e6,32)]:cell(t,'FF301627',alt.crop((32,y,48,y+16)),'fish_1')
poses.append(dict(name='fish_1',rows=[[None,0x6dd,0x6de],[0x6df,0x6e0,0x6e5],[0x6e2,0x6e3,0x6e6]],palettes=['FF301627'],size=[48,48]))
# Small native forms face right before OAM mirroring; the large fish faces left.
# Keep their moving head aligned with the measured native travel direction.
for i,src in enumerate([fish,alt]):
 small=Image.new('RGBA',(32,16));small.paste(reg(src.transpose(Image.Transpose.FLIP_LEFT_RIGHT),(30,14)),(1,1));sprite(f'fish_small_{i}',small,[[0x6ef+i*2,0x6f0+i*2]],['FF301627'])
# Native Breaker uses three horizontal phases plus distinct upward identities.
source=Image.open(r/'art/generated/level3_breaker_generated.png').convert('RGBA');a=np.array(source)
xs=np.flatnonzero(np.any(a[:,:,3]>=128,axis=0));groups=np.split(xs,np.flatnonzero(np.diff(xs)>source.width*.02)+1);assert len(groups)==3
raws=[]
for g in groups:
 im=source.crop((int(g[0]),0,int(g[-1])+1,source.height));raws.append(im.crop(im.getchannel('A').point(lambda v:255 if v>=128 else 0).getbbox()))
charge=Image.new('RGBA',(48,48));charge.paste(reg(raws[0],(46,46)),(1,1))
launch=Image.new('RGBA',(32,32));launch.paste(reg(raws[1],(30,24)),(1,4))
bolt=Image.new('RGBA',(32,16));bolt.paste(reg(raws[2],(32,12)),(0,2))
offsets=json.loads((art/'breaker_aliases.json').read_text())['offsets'];pals=['FF221136','FF300036']
sprite('breaker_charge',charge,[[0x675+y*3+x for x in range(3)]for y in range(3)],pals,offsets)
sprite('breaker_launch',launch,[[0x67e,0x67f],[0x680,0x681]],pals,offsets)
sprite('breaker_bolt',bolt,[[0x682,0x683]],pals,offsets)
sprite('breaker_launch_up',launch.transpose(Image.Transpose.ROTATE_90),[[0x684,0x685],[0x686,0x687]],pals,offsets)
sprite('breaker_bolt_up',bolt.transpose(Image.Transpose.ROTATE_90),[[0x688],[0x689]],pals,offsets)
empty=Image.new('RGBA',(16,16));masks={};aliases=[]
old=json.loads((r/'art/level3_opening/registration.json').read_text())
floor_sources={int(m['identity'],16):m for m in old['mappings']if m['scope'].startswith('l3_forestRoom')and m['palette']=='0F071727'and 0x734<=int(m['identity'],16)<=0x737}
oldatlas=Image.open(pack/'Stage3_Opening_Tiles_2x.png').convert('RGBA')
# Exact approved brown terrain material, with no newly painted scenery.
geom=json.loads((r/'art/screen2_5_roof/previous_geometry.json').read_text());body=Image.new('RGBA',(32,32))
for i,t in enumerate(range(0x330,0x334)):
 m=geom[f'{t:04X}'];x,y=m['xy'];im=Image.open(pack/m['image']).convert('RGBA').crop((x,y,x+16,y+16));body.paste(im,(i%2*16,i//2*16))
def native(t):
 b=patterns[t];return np.array([[255 if ((b[y]|b[y+8])>>(7-x))&1 else 0 for x in range(8)]for y in range(8)],dtype=np.uint8)
def ceiling_mask(t):
 a=native(t)
 for x in range(8):
  ys=np.flatnonzero(a[:,x])
  if len(ys):a[:ys[-1]+1,x]=255
 return Image.fromarray(a).resize((16,16),Image.Resampling.NEAREST)
# Register both the rising floor and descending ceiling stair arrangements.
step=reg(obj(r/'art/generated/screen2_5_stair_tread_generated.png'),(32,32));steps={}
for i,rows in enumerate([[[0x783,0x782],[0x781,0x780]],[[0x787,0x786],[0x785,0x784]]]):
 ma=np.block([[native(t)for t in row]for row in rows])
 for x in range(16):
  ys=np.flatnonzero(ma[:,x])
  if len(ys):ma[ys[0]:ys[-1]+1,x]=255
 im=step.copy();im.putalpha(Image.fromarray(ma).resize((32,32),Image.Resampling.NEAREST));im.save(art/f'stair_{i}.png')
 for y,row in enumerate(rows):
  for x,t in enumerate(row):steps[t]=im.crop((x*16,y*16,x*16+16,y*16+16))
observed=json.loads((art/'observed_backgrounds.json').read_text());observed['0F122131']=observed['0F161606'].copy()
for pal in ['0F0A1A29','0F071727','0F162726','0F060616','0F161606','0F122131']:observed[pal]=sorted(set(observed.get(pal,[]))|{0x700})
for pal,ts in observed.items():
 for t in ts:
  if 0x73e<=t<=0x743:
   native_alias={0x73e:0x345,0x73f:0x344,0x740:0x343,0x741:0x342,0x742:0x341,0x743:0x334}[t]
   line=next(l for l in text.splitlines()if l.startswith('[s21Room&s21DataLo&s21DataHi]<tile>')and l.split('<tile>')[1].split(',')[1:3]==[f'{native_alias:04X}',pal])
   f=line.split('<tile>')[1].split(',');f[1]=f'{t:04X}'
   for sc in states:rules.append('['+sc+']<tile>'+','.join(f))
   aliases.append(dict(tile=f'{t:04X}',palette=pal,source_rule=line));continue
  if t<=0x704 or t in [0x78a,0x78b]:im=empty;kind='nonsolid hanging decoration / cave reveal'
  elif t in floor_sources:
   m=floor_sources[t];x,y=m['xy'];im=oldatlas.crop((x,y,x+16,y+16));kind='approved native floor cap'
  elif t in steps:im=steps[t];kind='approved carved step material'
  else:
   x,y=(t&1)*16,((t>>1)&1)*16;im=body.crop((x,y,x+16,y+16));kind='approved brown solid terrain'
   if t in [0x792,0x793,0x794,0x795]:im.putalpha(ceiling_mask(t));kind='native ceiling contour'
  masks[f'{t:04X}/{pal}']=np.array(im.getchannel('A')).tolist()
  for sc in states:cell(t,pal,im,kind,sc)
# Rendered guards and the actual hot/ice palette keep menus/fades protected.
for t in sorted(observed['0F0A1A29']):
 guard=f'l3lavaView{t:04X}';conditions.append(f'<condition>{guard},tileAtPosition,128,16,{t:04X},0F0A1A29')
 for sc in states:backgrounds.append(f'[{sc}&{guard}]<background>Stage2_Cave_Background.png,1,1,0,11,0,0')
def block(kind,lines):return '# BEGIN LEVEL3_LAVA '+kind+'\n'+'\n'.join(lines)+'\n# END LEVEL3_LAVA '+kind+'\n'
end=text.index('\n',text.rfind('<img>'))+1;text=text[:end]+block('IMAGES',['<img>Stage3_Lava_Tiles_2x.png'])+text[end:]
lines=text.splitlines(keepends=True);first=next(i for i,l in enumerate(lines)if '<tile>'in l or '<background>'in l);lines[first:first]=[block('CONDITIONS',conditions),block('MAPPINGS',rules+backgrounds)]
(pack/'hires.txt').write_text(''.join(lines));atlas.save(pack/'Stage3_Lava_Tiles_2x.png');atlas.save(art/'Stage3_Lava_Tiles_2x.png')
(art/'poses.json').write_text(json.dumps(poses,indent=2)+'\n')
(art/'registration.json').write_text(json.dumps(dict(tile_rules=len(rules),conditions=len(conditions),background_rules=len(backgrounds),mappings=records,lava_aliases=aliases,terrain_masks=masks,atlas_cells=len(cache),native_gameplay_modified=False,previous_runtime_art_modified=False),indent=2)+'\n')
print('Level 3 lava:',len(rules),'mappings; reused cave, terrain, steps, lava/ice and menu boot; fish and complete Breaker phases.')
