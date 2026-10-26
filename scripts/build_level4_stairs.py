"""Restore the descending temple stair family incorrectly cleared as scenery."""
from pathlib import Path
import hashlib,json,re
import numpy as np
from PIL import Image

r=Path(__file__).resolve().parents[1];p=r/'build/Holy_Diver_(Tr)';a=r/'art/level4_stairs';a.mkdir(exist_ok=True)
text=(p/'hires.txt').read_text();previous=json.loads((r/'evidence/0.16.2-pack-sha256.json').read_text())
assert hashlib.sha256(text.encode()).hexdigest()==previous['hires.txt']
assert sum(l.startswith('<img>')for l in text.splitlines())==49
patterns=json.loads((r/'art/level4/native_patterns.json').read_text())
native=np.zeros((16,16),np.uint8)
for i,t in enumerate(range(0xb7c,0xb80)):
 raw=bytes.fromhex(patterns[f'{t:04X}'])
 cell=np.array([[255 if ((raw[y]|raw[y+8])>>(7-x))&1 else 0 for x in range(8)]for y in range(8)],dtype=np.uint8)
 native[i//2*8:i//2*8+8,i%2*8:i%2*8+8]=cell
# Register the complete step before slicing. Fill recesses inside the native
# silhouette, retaining its top surface and irregular sloping underside.
mask=native.copy()
for y in range(16):
 xs=np.flatnonzero(mask[y])
 if len(xs):mask[y,xs[0]:xs[-1]+1]=255
for x in range(16):
 ys=np.flatnonzero(mask[:,x])
 if len(ys):mask[ys[0]:ys[-1]+1,x]=255
mask=Image.fromarray(mask).resize((32,32),Image.Resampling.NEAREST)
step=Image.open(r/'art/level4_masonry/moving_platform.png').convert('RGBA')
step.putalpha(mask);step.save(a/'descending_step.png')
step.save(p/'Golden_Temple_Stairs_2x.png')
reg=json.loads((r/'art/level4/registration.json').read_text());rules=[];records=[]
for old in reg['mappings']:
 t=int(old['tile'],16)
 if not 0xb7c<=t<=0xb7f:continue
 assert old['kind']=='nonsolid scenery reveal'
 i=t-0xb7c;x=i%2*16;y=i//2*16
 rule=f'[{old["scope"]}]<tile>49,{t:04X},{old["palette"]},{x},{y},1,N'
 rules.append(rule);records.append(dict(tile=f'{t:04X}',palette=old['palette'],scope=old['scope'],xy=[x,y],rule=rule,overridden_rule=old['rule']))
assert len(rules)==24
def block(name,lines):return '# BEGIN TEMPLE_STAIRS '+name+'\n'+'\n'.join(lines)+'\n# END TEMPLE_STAIRS '+name+'\n'
end=text.index('\n',text.rfind('<img>'))+1
text=text[:end]+block('IMAGES',['<img>Golden_Temple_Stairs_2x.png'])+text[end:]
mark='# BEGIN TEMPLE_REPAIRS CONDITIONS'
text=text.replace(mark,block('MAPPINGS',rules)+mark)
(p/'hires.txt').write_text(text)
(a/'registration.json').write_text(json.dumps(dict(tile_rules=len(rules),mappings=records,
 source='art/level4_masonry/moving_platform.png',source_sha256=hashlib.sha256((r/'art/level4_masonry/moving_platform.png').read_bytes()).hexdigest(),
 native_patterns={f'{t:04X}':patterns[f'{t:04X}']for t in range(0xb7c,0xb80)},
 native_alpha=native.tolist(),alpha=np.array(mask).tolist(),native_gameplay_modified=False,
 prior_artwork_modified=False),indent=2)+'\n')
print('Temple stairs:',len(rules),'scoped mappings; four restored native cells; existing stone reused')
