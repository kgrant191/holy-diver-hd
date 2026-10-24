"""Restore a readable solid ceiling while preserving approved stairs and floors."""
from pathlib import Path
import hashlib,json
import numpy as np
from PIL import Image
root=Path(__file__).resolve().parents[1];pack=root/'build/Holy_Diver_(Tr)';art=root/'art/screen2_5_roof'
text=(pack/'hires.txt').read_text();assert text.count('<img>')==38
scope='s25Room&s25DataLo&s25DataHi';atlas=Image.new('RGBA',(256,128));cache={};rules=[];metadata=[]
# The accepted 0.8.1 floor tests remain first, so shared body identities beneath
# platform caps keep their exact gold artwork. Everything else is ceiling.
for line in text.splitlines():
 if line.startswith('['+scope+'&s25FloorY') and '<tile>'in line:rules.append(line)
assert len(rules)==464
geometry=json.loads((art/'previous_geometry.json').read_text());images={}
for g in geometry.values():
 if g['image'] not in images:images[g['image']]=Image.open(pack/g['image']).convert('RGBA')
def old_cell(t):
 g=geometry[f'{t:04X}'];x,y=g['xy'];return images[g['image']].crop((x,y,x+16,y+16))
# Use a broad crop so each 32x32 registration has a few large planes. Blend
# the outer two source pixels to avoid a hard join between repeated tiles.
source=Image.open(root/'art/generated/screen2_5_roof_generated.png').convert('RGB')
box=(0,0,source.width//6,source.height//6);material=source.crop(box).resize((32,32),Image.Resampling.LANCZOS)
a=np.array(material).astype(float)
for axis in [0,1]:
 q=np.moveaxis(a,axis,0);edge=(q[0]+q[-1])/2
 for n in range(2):
  weight=(1-n/2)**2;q[n]=q[n]*(1-weight)+edge*weight;q[-1-n]=q[-1-n]*(1-weight)+edge*weight
material=Image.fromarray(np.clip(a,0,255).astype('uint8')).quantize(colors=48).convert('RGBA');material.save(art/'ceiling_material.png')
cells={}
# Preserve the exact former ceiling silhouette, using complete groups so the
# lower-edge lighting is continuous across native tile boundaries.
for first in [0x35b,0x369,0x38f,0x393,0x397]:
 alpha=Image.new('L',(32,32))
 for i in range(4):alpha.paste(old_cell(first+i).getchannel('A'),(i%2*16,i//2*16))
 mask=np.array(alpha);data=np.array(material).copy()
 for x in range(32):
  ys=np.flatnonzero(mask[:,x])
  if len(ys):
   end=ys[-1]
   for y,gain in [(end,1.8),(end-1,1.5),(end-2,1.2)]:
    if y>=0 and mask[y,x]:data[y,x,:3]=np.clip(data[y,x,:3].astype(float)*gain+12,0,190).astype('uint8')
 data[:,:,3]=mask;whole=Image.fromarray(data);whole.save(art/f'ceiling_{first:04X}.png')
 for i in range(4):x,y=i%2*16,i//2*16;cells[first+i]=whole.crop((x,y,x+16,y+16))
for key in geometry:
 t=int(key,16)
 if t not in cells:
  x,y=(t&1)*16,((t>>1)&1)*16;im=material.crop((x,y,x+16,y+16));im.putalpha(old_cell(t).getchannel('A'));cells[t]=im
for t,im in sorted(cells.items()):
 digest=hashlib.sha256(im.tobytes()).hexdigest()
 if digest not in cache:
  n=len(cache);xy=(n%16*16,n//16*16);assert xy[1]+16<=atlas.height;cache[digest]=xy;atlas.paste(im,xy)
 x,y=cache[digest];rules.append(f'[{scope}]<tile>38,{t:04X},0F071737,{x},{y},1,N')
 metadata.append(dict(identity=f'{t:04X}',atlas=[x,y],previous_source=geometry[f'{t:04X}'],alpha_unchanged=True))
def section(kind,lines):return '# BEGIN SCREEN2_5_ROOF '+kind+'\n'+'\n'.join(lines)+'\n# END SCREEN2_5_ROOF '+kind+'\n'
end=text.index('\n',text.rfind('<img>'))+1;text=text[:end]+section('IMAGES',['<img>Stage2_Crimson_Ceiling_2x.png'])+text[end:]
lines=text.splitlines(keepends=True);first=next(i for i,line in enumerate(lines)if '<tile>'in line or '<background>'in line);lines[first:first]=[section('MAPPINGS',rules)];(pack/'hires.txt').write_text(''.join(lines))
atlas.save(art/'Stage2_Crimson_Ceiling_2x.png');atlas.save(pack/'Stage2_Crimson_Ceiling_2x.png')
(art/'registration.json').write_text(json.dumps(dict(scope=scope,tile_rules=len(rules),floor_preservation_rules=464,ceiling_identities=len(cells),atlas_cells=len(cache),source_crop=box,mappings=metadata,collision_modified=False,stairs_modified=False,previous_runtime_assets_modified=False),indent=2)+'\n')
print('Readable crimson ceiling:',len(cells),'identities,',len(rules),'rules; accepted stairs unchanged')
