"""Review: distinct carved steps, open crimson scenery and the large health jug."""
from pathlib import Path
import hashlib,json
import numpy as np
from PIL import Image
root=Path(__file__).resolve().parents[1];pack=root/'build/Holy_Diver_(Tr)';art=root/'art/screen2_5_review'
text=(pack/'hires.txt').read_text();assert text.count('<img>')==37
scope='s25Room&s25DataLo&s25DataHi';stairs_scope='s24Room&s24DataLo&s24DataHi'
atlas=Image.new('RGBA',(256,128));cache={};rules=[];conditions=[];metadata=[]
def add(t,pal,im,kind,condition=scope):
 assert im.size==(16,16)
 key=hashlib.sha256(im.tobytes()).hexdigest()
 if key not in cache:
  n=len(cache);xy=(n%16*16,n//16*16);assert xy[1]+16<=atlas.height;cache[key]=xy;atlas.paste(im,xy)
 x,y=cache[key];pre='['+condition+']' if condition else ''
 rules.append(f'{pre}<tile>37,{t:04X},{pal},{x},{y},1,N')
 metadata.append(dict(identity=f'{t:04X}',palette=pal,atlas=[x,y],scope=condition,kind=kind))
def register(source,size,colors=48):
 im=Image.open(source).convert('RGBA');bbox=im.getchannel('A').point(lambda v:255 if v>=128 else 0).getbbox()
 im=im.crop(bbox).resize(size,Image.Resampling.LANCZOS);alpha=im.getchannel('A').point(lambda v:255 if v>=128 else 0)
 im=im.convert('RGB').quantize(colors=colors).convert('RGBA');im.putalpha(alpha);return im
empty=Image.new('RGBA',(16,16))
# Preserve all previous sources. New treads occupy the identical native contours.
step=register(root/'art/generated/screen2_5_stair_tread_generated.png',(32,32))
patterns=json.loads((root/'art/screen2_4/native_stairs.json').read_text())
for first in [0x375,0x379,0x37d]:
 mask=np.zeros((16,16),dtype=np.uint8)
 for i,t in enumerate(range(first,first+4)):
  b=bytes.fromhex(patterns[f'{t:04X}'])
  for y in range(8):
   for x in range(8):mask[i//2*8+y,i%2*8+x]=255 if (b[y]|b[y+8])>>(7-x)&1 else 0
 for x in range(16):
  ys=np.flatnonzero(mask[:,x])
  if len(ys):mask[ys[0]:ys[-1]+1,x]=255
 im=step.copy();im.putalpha(Image.fromarray(mask).resize((32,32),Image.Resampling.NEAREST));im.save(art/f'stair_{first:04X}.png')
 for i,t in enumerate(range(first,first+4)):
  x,y=i%2*16,i//2*16;cell=im.crop((x,y,x+16,y+16))
  for room in [stairs_scope,scope]:add(t,'0F071737',cell,'carved stair tread',room)
# The bulky red foreground decoration no longer obscures the accepted panorama.
for t in [0x371,0x372,0x373,0x374,0x36d,0x370,0x3a3,0x3a4,0x3a5,0x3a6,0x3a7,0x34f]:add(t,'0F061626',empty,'red decoration removed')
# Rock body identities are shared by ceiling and ground. Retain exact gold
# bodies below a native platform cap, with Y bounds preventing wrapped probes.
body=[0x330,0x331,0x332,0x333,0x381,0x382,0x383,0x384]
old={}
for line in text.splitlines():
 if line.startswith('['+scope+']<tile>'):
  f=line.split('<tile>')[1].split(',')
  if int(f[1],16) in body and f[2]=='0F071737':old[int(f[1],16)]=line
assert set(old)==set(body)
for distance in range(8,240,8):
 yn=f's25FloorY{distance}';conditions.append(f'<condition>{yn},positionCheckY,>=,{distance}')
 for cap in [0x32e,0x32f]:
  cn=f's25Floor{cap:X}_{distance}';conditions.append(f'<condition>{cn},tileNearby,0,{-distance},{cap:04X},0F071737')
  for t in body:rules.append(old[t].replace('['+scope+']','['+scope+'&'+yn+'&'+cn+']',1))
for t in body:add(t,'0F071737',empty,'ceiling fill removed; floor bodies retained above')
# A narrow dark crimson rim follows the original overhead boundary. Interior
# fill stays transparent, exposing the existing red cave instead of gold slabs.
patterns=json.loads((art/'native_ceiling.json').read_text())
material=Image.open(root/'art/screen2_5/crimson_rock_registered.png').convert('RGBA').resize((32,32),Image.Resampling.LANCZOS)
a=np.array(material);a[:,:,:3]=(a[:,:,:3].astype(float)*.42).astype('uint8');material=Image.fromarray(a)
for first in [0x35b,0x369,0x38f,0x393,0x397]:
 mask=np.zeros((16,16),dtype=np.uint8)
 for i,t in enumerate(range(first,first+4)):
  b=bytes.fromhex(patterns[f'{t:04X}'])
  for y in range(8):
   for x in range(8):mask[i//2*8+y,i%2*8+x]=255 if (b[y]|b[y+8])>>(7-x)&1 else 0
 rim=np.zeros_like(mask)
 for x in range(16):
  ys=np.flatnonzero(mask[:,x])
  if len(ys):rim[ys[-1],x]=255
 im=material.copy();im.putalpha(Image.fromarray(rim).resize((32,32),Image.Resampling.NEAREST))
 for i,t in enumerate(range(first,first+4)):
  x,y=i%2*16,i//2*16;add(t,'0F071737',im.crop((x,y,x+16,y+16)),'slim overhead boundary')
# The screenshot shows a distinct four-tile handled jug, not the two-tile
# bottles already covered. Match only proven byte-identical CHR groups.
jug=register(root/'art/generated/screen2_5_health_jug_generated.png',(30,30))
full=Image.new('RGBA',(32,32));full.paste(jug,(1,1));full.save(art/'health_jug.png')
identity=json.loads((art/'native_jug.json').read_text())
for first in identity['identical_groups']:
 for i in range(4):
  x,y=i%2*16,i//2*16;add(int(first,16)+i,'FF301116',full.crop((x,y,x+16,y+16)),'opaque handled health jug',None)

def section(kind,lines):return '# BEGIN SCREEN2_5_REVIEW '+kind+'\n'+'\n'.join(lines)+'\n# END SCREEN2_5_REVIEW '+kind+'\n'
end=text.index('\n',text.rfind('<img>'))+1;text=text[:end]+section('IMAGES',['<img>Stage2_Cave_Review_2x.png'])+text[end:]
lines=text.splitlines(keepends=True);first=next(i for i,line in enumerate(lines)if '<tile>'in line or '<background>'in line)
lines[first:first]=[section('CONDITIONS',conditions),section('MAPPINGS',rules)];(pack/'hires.txt').write_text(''.join(lines))
atlas.save(art/'Stage2_Cave_Review_2x.png');atlas.save(pack/'Stage2_Cave_Review_2x.png')
(art/'registration.json').write_text(json.dumps(dict(tile_rules=len(rules),conditions=len(conditions),atlas_cells=len(cache),mappings=metadata,previous_runtime_assets_modified=False,collision_modified=False),indent=2)+'\n')
print('Screen 2-5 review:',len(rules),'rules,',len(conditions),'conditions,',len(cache),'atlas cells')
