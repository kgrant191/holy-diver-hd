"""Replace only temple foreground stone, destructible blocks and structural columns."""
from pathlib import Path
import json,hashlib
import numpy as np
from PIL import Image

r=Path(__file__).resolve().parents[1];p=r/'build/Holy_Diver_(Tr)';a=r/'art/level4_masonry';g=r/'art/generated'
text=(p/'hires.txt').read_text();assert sum(l.startswith('<img>')for l in text.splitlines())==48
old=json.loads((r/'art/level4/registration.json').read_text());patterns=json.loads((r/'art/level4/native_patterns.json').read_text())
atlas=Image.new('RGBA',(512,256));cache={};rules=[];conditions=[];records=[]
def tight(im):
 im=im.convert('RGBA');box=im.getchannel('A').point(lambda x:255 if x>=160 else 0).getbbox();assert box
 return im.crop(box)
def reg(im,size):
 im=im.convert('RGBA').resize(size,Image.Resampling.LANCZOS);alpha=im.getchannel('A').point(lambda x:255 if x>=128 else 0)
 im=im.convert('RGB').quantize(colors=96).convert('RGBA');im.putalpha(alpha);return im
def opaque(im):
 im=im.copy();im.putalpha(255);return im
def hull(t):
 b=bytes.fromhex(patterns[f'{t:04X}']);v=np.array([[255 if ((b[y]|b[y+8])>>(7-x))&1 else 0 for x in range(8)]for y in range(8)],dtype=np.uint8)
 for y in range(8):
  xs=np.flatnonzero(v[y])
  if len(xs):v[y,xs[0]:xs[-1]+1]=255
 for x in range(8):
  ys=np.flatnonzero(v[:,x])
  if len(ys):v[ys[0]:ys[-1]+1,x]=255
 return Image.fromarray(v).resize((16,16),Image.Resampling.NEAREST)
def tile(t,pal,im,kind,scope):
 assert im.size==(16,16);digest=hashlib.sha256(im.tobytes()).hexdigest()
 if digest not in cache:
  n=len(cache);xy=(n%32*16,n//32*16);assert xy[1]<256;cache[digest]=xy;atlas.paste(im,xy)
 x,y=cache[digest];line=f'[{scope}]<tile>48,{t:04X},{pal},{x},{y},1,N';rules.append(line)
 records.append(dict(tile=f'{t:04X}',palette=pal,xy=[x,y],kind=kind,scope=scope,rule=line))

solid=reg(tight(Image.open(g/'temple_solid_0_16_1.png')),(64,32));solid.save(a/'solid.png')
broken=reg(tight(Image.open(g/'temple_breakable_0_16_1.png')),(32,32));broken.save(a/'breakable.png')
pillar=tight(Image.open(g/'temple_pillar_0_16_1.png'));w,h=pillar.size
cap=reg(tight(pillar.crop((0,0,w,int(h*.215)))),(64,32))
base=reg(tight(pillar.crop((0,int(h*.82),w,h))),(64,32))
shaft=opaque(reg(tight(pillar.crop((0,int(h*.30),w,int(h*.38)))),(64,16)))
for n,im in [('column_cap',cap),('column_base',base),('column_shaft',shaft)]:im.save(a/(n+'.png'))

# Native large stones use four horizontal cells, with staggered half-block starts.
terrain={};layout=[[0xb3c,0xb3d,0xb3a,0xb3b],[0xb40,0xb41,0xb3e,0xb3f]]
for y,row in enumerate(layout):
 for x,t in enumerate(row):terrain[t]=solid.crop((x*16,y*16,x*16+16,y*16+16))
for t,x,y in [(0xb42,0,0),(0xb43,16,0),(0xb44,32,0),(0xb45,48,0),(0xb46,0,16),(0xb47,16,16),(0xb48,32,16),(0xb49,48,16),(0xb52,0,0),(0xb53,0,16)]:
 im=solid.crop((x,y,x+16,y+16));im.putalpha(hull(t));terrain[t]=im
for i,t in enumerate(range(0xb4e,0xb52)):
 x=i%2*16;y=i//2*16;terrain[t]=broken.crop((x,y,x+16,y+16))
for t in range(0xb78,0xb7c):terrain[t]=solid.crop(((t-0xb78)*16,8,(t-0xb78+1)*16,24))
small_stone=reg(solid,(32,32))
stair_parts={0xb80:(16,16),0xb81:(0,16),0xb82:(0,0),0xb83:(16,0),0xb84:(0,16),0xb85:(16,16),0xb86:(0,0),0xb87:(16,0),0xb88:(0,16)}
for t,(x,y)in stair_parts.items():
 im=small_stone.crop((x,y,x+16,y+16));im.putalpha(hull(t));terrain[t]=im
# Keep the already verified complete step silhouettes while changing their stone.
for key,alpha in old['geometry'].items():
 t=int(key,16)
 if 0xb80<=t<=0xb87:terrain[t].putalpha(Image.fromarray(np.array(alpha,dtype=np.uint8)))

observed=json.loads((r/'art/level4/observed_backgrounds.json').read_text())
for room,scope in old['scopes'].items():
 for pal,ids in observed[room].items():
  if not pal.startswith('0F'):continue
  for key in ids:
   t=int(key,16)
   if t not in terrain:continue
   if room!='A865' and 0xb78<=t<=0xb7b:
    # Context identifies the ends of each structural column without altering
    # its native cell positions, including supports that cross the floor.
    names={}
    for label,dy in [('above',-8),('above2',-16),('below',8),('below2',16)]:
     name=f'masonry{room}{t:04X}{pal}{label}';names[label]=name
     conditions.append(f'<condition>{name},tileNearby,0,{dy},{t:04X},{pal}')
    x=(t-0xb78)*16
    for kind,im,guard in [('column cap upper',cap.crop((x,0,x+16,16)),'!'+names['above']),('column cap lower',cap.crop((x,16,x+16,32)),names['above']+'&!'+names['above2']),('column base lower',base.crop((x,16,x+16,32)),'!'+names['below']),('column base upper',base.crop((x,0,x+16,16)),names['below']+'&!'+names['below2'])]:tile(t,pal,im,kind,scope+'&'+guard)
    tile(t,pal,shaft.crop((x,0,x+16,16)),'column shaft',scope)
   else:
    tile(t,pal,terrain[t],'breakable block'if 0xb4e<=t<=0xb51 else'solid stone',scope)

# The moving platform is physical masonry, so it uses the same solid treatment.
moving=reg(solid,(32,32));moving.save(a/'moving_platform.png')
for room,scope in old['scopes'].items():
 for i,t in enumerate(range(0xaf8,0xafc)):
  x=i%2*16;y=i//2*16;tile(t,'FF172737',moving.crop((x,y,x+16,y+16)),'moving solid platform',scope)
def block(name,lines):return '# BEGIN TEMPLE_MASONRY '+name+'\n'+'\n'.join(lines)+'\n# END TEMPLE_MASONRY '+name+'\n'
end=text.index('\n',text.rfind('<img>'))+1;text=text[:end]+block('IMAGES',['<img>Golden_Temple_Masonry_2x.png'])+text[end:]
# The existing temple room conditions must be declared before these rules.
mark='# BEGIN GOLDEN_TEMPLE MAPPINGS';at=text.index(mark)
text=text[:at]+block('CONDITIONS',conditions)+block('MAPPINGS',rules)+text[at:]
(p/'hires.txt').write_text(text);atlas.save(p/'Golden_Temple_Masonry_2x.png');atlas.save(a/'Golden_Temple_Masonry_2x.png')
(a/'registration.json').write_text(json.dumps(dict(mappings=records,tile_rules=len(rules),conditions=len(conditions),atlas_cells=len(cache),backgrounds_modified=False,outdoor_columns_modified=False,breakable_tiles=['0B4E','0B4F','0B50','0B51']),indent=2)+'\n')
print('Temple masonry:',len(rules),'scoped tiles;',len(conditions),'column-end guards;',len(cache),'atlas cells')
