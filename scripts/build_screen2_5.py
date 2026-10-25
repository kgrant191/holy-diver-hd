"""Crimson cavern: reuse accepted enemies/terrain and register new red mineral art."""
from pathlib import Path
import hashlib,json
import numpy as np
from PIL import Image
root=Path(__file__).resolve().parents[1]
pack=root/'build/Holy_Diver_(Tr)';art=root/'art/screen2_5'
text=(pack/'hires.txt').read_text();assert text.count('<img>')==36
scope='s25Room&s25DataLo&s25DataHi'
conditions=['<condition>s25Room,memoryCheckConstant,0072,==,10',
 '<condition>s25DataLo,memoryCheckConstant,0078,==,9D',
 '<condition>s25DataHi,memoryCheckConstant,0079,==,8D',
 '<condition>s25Wall0,ppuMemoryCheckConstant,3F09,==,06',
 '<condition>s25Wall1,ppuMemoryCheckConstant,3F0A,==,16',
 '<condition>s25Wall2,ppuMemoryCheckConstant,3F0B,==,26']
aliases=[];rules=[];metadata=[];cache={};atlas=Image.new('RGBA',(256,128))
for screen,include in [('screen2_4',lambda t,p: t>=0x300 and p!='0F061828'),
                       ('screen2_2',lambda t,p:0x28e<=t<=0x2b6 or 0x34b<=t<=0x34d),
                       ('screen2_3',lambda t,p:0x2d8<=t<=0x2dd)]:
 prior=json.loads((root/'art'/screen/'registration.json').read_text())['scope']
 for line in text.splitlines():
  if not line.startswith('['+prior) or '<tile>' not in line:continue
  f=line.split('<tile>')[1].split(',');t=int(f[1],16)
  if include(t,f[2]):aliases.append(line.replace(prior,scope,1))

def tile(t,pal,im,kind):
 assert im.size==(16,16)
 digest=hashlib.sha256(im.tobytes()).hexdigest()
 if digest not in cache:
  n=len(cache);xy=(n%16*16,n//16*16);assert xy[1]+16<=atlas.height
  atlas.paste(im,xy);cache[digest]=xy
 x,y=cache[digest];rules.append(f'[{scope}]<tile>36,{t:04X},{pal},{x},{y},1,N')
 metadata.append(dict(identity=f'{t:04X}',palette=pal,atlas=[x,y],kind=kind))

source=Image.open(root/'art/generated/screen2_5_crimson_generated.png').convert('RGB')
split=source.width//2

def material(box,size,brightness):
 im=source.crop(box).resize(size,Image.Resampling.LANCZOS)
 a=np.array(im).astype(float)*brightness
 # Blend only the outermost two pixels to keep repeated tile joins continuous.
 for axis in [0,1]:
  q=np.moveaxis(a,axis,0);edge=(q[0]+q[-1])/2
  for n in range(2):
   w=(1-n/2)**2;q[n]=q[n]*(1-w)+edge*w;q[-1-n]=q[-1-n]*(1-w)+edge*w
 im=Image.fromarray(np.clip(a,0,255).astype('uint8')).quantize(colors=48).convert('RGBA')
 return im
rock=material((0,0,int(split*.60),int(source.height*.30)),(64,32),1.0)
# Broad side shading gives each native column readable depth at game scale.
a=np.array(rock).astype(float)
shade=0.58+0.42*np.sin(np.linspace(0,np.pi,64))
a[:,:,:3]*=shade[None,:,None]
rock=Image.fromarray(np.clip(a,0,255).astype('uint8'))
rock.save(art/'crimson_rock_registered.png')
patterns=json.loads((art/'native_patterns.json').read_text())

def native_mask(t):
 b=bytes.fromhex(patterns[f'{t:04X}'])
 return np.array([[255 if ((b[y]|b[y+8])>>(7-x))&1 else 0 for x in range(8)]for y in range(8)],dtype=np.uint8)

# Wide red columns: cap and two repeating body rows, registered as a whole.
layout=[[0x371,0x372,0x373,0x374],[0x36d,0x370,0x3a3,0x3a4],[0x3a5,0x3a6,0x3a7,0x34f]]
mask=np.concatenate([np.concatenate([native_mask(t)for t in row],axis=1)for row in layout],axis=0)
for y in range(mask.shape[0]):
 xs=np.flatnonzero(mask[y])
 if len(xs):mask[y,xs[0]:xs[-1]+1]=255
for y,row in enumerate(layout):
 for x,t in enumerate(row):
  sy=16 if y in [0,2] else 0
  im=rock.crop((x*16,sy,x*16+16,sy+16))
  im.putalpha(Image.fromarray(mask[y*8:y*8+8,x*8:x*8+8]).resize((16,16),Image.Resampling.NEAREST))
  tile(t,'0F061626',im,'crimson mineral column')

# The nonsolid repeating wall is represented by broad formations in the new
# crimson panorama; keep the native red column geometry in front of it.
for t in range(0x35f,0x369):
 tile(t,'0F061627',Image.new('RGBA',(16,16)),'crimson panorama reveal')
for pal in ['0F061626','0F061627']:
 tile(0x300,pal,Image.new('RGBA',(16,16)),'empty cave space')
for t in [0x36e,0x36f,*range(0x39b,0x3a1)]:
 tile(t,'0F061626',Image.new('RGBA',(16,16)),'distant cave reveal')

backgrounds=[]
guards=[(t,'0F071737')for t in [*range(0x32e,0x334),*range(0x35b,0x35f),*range(0x369,0x36d),*range(0x375,0x385),*range(0x38f,0x39b)]]
guards +=[(t,'0F061627')for t in range(0x35f,0x369)]+[(t,'0F061626')for t in range(0x39b,0x3a1)]
for i,(t,pal)in enumerate(guards):
 name=f's25Rendered{i}';conditions.append(f'<condition>{name},tileAtPosition,128,16,{t:04X},{pal}')
 backgrounds.append(f'[{scope}&s25Wall0&s25Wall1&s25Wall2&{name}]<background>Stage2_Crimson_Cave_Background.png,1,1,1,11,0,0')
bg=Image.open(root/'art/generated/screen2_5_background_generated.png').convert('RGB').resize((1024,480),Image.Resampling.LANCZOS)
a=np.array(bg).astype(float);edge=(a[:,0]+a[:,-1])/2
for x in range(24):
 w=(1-x/24)**2;a[:,x]=a[:,x]*(1-w)+edge*w;a[:,-1-x]=a[:,-1-x]*(1-w)+edge*w
bg=Image.fromarray(a.astype('uint8'));panorama=Image.new('RGB',(8704,480))
for x in range(0,8704,1024):panorama.paste(bg,(x,0))
panorama.save(pack/'Stage2_Crimson_Cave_Background.png')
atlas.save(art/'Stage2_Crimson_Cave_Tiles_2x.png');atlas.save(pack/'Stage2_Crimson_Cave_Tiles_2x.png')
def section(kind,lines):return '# BEGIN SCREEN2_5 '+kind+'\n'+'\n'.join(lines)+'\n# END SCREEN2_5 '+kind+'\n'
end=text.index('\n',text.rfind('<img>'))+1;text=text[:end]+section('IMAGES',['<img>Stage2_Crimson_Cave_Tiles_2x.png'])+text[end:]
lines=text.splitlines(keepends=True);first=next(i for i,line in enumerate(lines)if '<tile>'in line or '<background>'in line)
lines[first:first]=[section('CONDITIONS',conditions),section('MAPPINGS',aliases+rules+backgrounds)]
(pack/'hires.txt').write_text(''.join(lines))
(art/'registration.json').write_text(json.dumps(dict(scope=scope,shared_aliases=len(aliases),new_tile_rules=len(rules),atlas_cells=len(cache),background_rules=len(backgrounds),mappings=metadata,native_collision_modified=False,previous_artwork_modified=False),indent=2)+'\n')
print('Stage 2 crimson cave:',len(aliases),'shared aliases,',len(rules),'new tile mappings')
