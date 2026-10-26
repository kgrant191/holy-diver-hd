"""Cancel native horizontal hover dithering without changing emulated state."""
from pathlib import Path
import json
from PIL import Image
import numpy as np
r=Path(__file__).resolve().parents[1];pack=r/'build/Holy_Diver_(Tr)';evidence=r/'art/big_fish_motion';evidence.mkdir(exist_ok=True)
atlas=Image.open(pack/'Stage3_Lava_Tiles_2x.png').convert('RGBA');assert not np.array(atlas)[496:,:,3].any()
art=r/'art/level3_lava';cells={};n=0
rows0=[[None,0x6dd,0x6de],[0x6df,0x6e0,0x6e1],[0x6e2,0x6e3,0x6e4]]
for dx in [-1,1]:
 seen={}
 for phase in [0,1]:
  im=Image.open(art/f'fish_{phase}.png').convert('RGBA');out=Image.new('RGBA',(48,48));out.paste(im,(dx,0));assert np.array(out)[:,:,3].sum()==np.array(im)[:,:,3].sum();assert not np.array(out)[:16,:16,3].any()
  rows=rows0 if phase==0 else [[None,0x6dd,0x6de],[0x6df,0x6e0,0x6e5],[0x6e2,0x6e3,0x6e6]]
  for y,row in enumerate(rows):
   for x,t in enumerate(row):
    if t is None:continue
    cell=out.crop((x*16,y*16,x*16+16,y*16+16))
    if t in seen:assert cell.tobytes()==seen[t];continue
    seen[t]=cell.tobytes();xy=(n*16,496);atlas.paste(cell,xy);cells[(dx,t)]=xy;n+=1
assert n==20
# Native hover equilibria are relative to Randy's SCREEN X: left-facing
# fish alternate at player+87/+88, mirrored fish at player-88/-87.
# Match the individual rendered tile origin, so two fish can use opposite
# corrections in the same frame. No object-slot inference or single-fish guard.
conditions=[];rules=[];origins=set();positions=set();locations={}
for y,row in enumerate(rows0):
 for x,t in enumerate(row):
  if t:locations[t]=(x,y)
locations[0x6e5]=locations[0x6e1];locations[0x6e6]=locations[0x6e4]
for px in range(256):
 conditions.append(f'<condition>fishPlayerX{px},memoryCheckConstant,0340,==,{px:02X}')
 for mirrored in [False,True]:
  for phase in [0,1]:
   left=px+75+phase if not mirrored else px-100+phase
   # Preserve the original registration for partly clipped boundary sprites.
   if not 7<=left<=225:continue
   world=1 if phase==0 else -1;dx=-world if mirrored else world
   for t,(col,row)in locations.items():
    origin_x=left+(2-col if mirrored else col)*8
    for k in (range(8)if mirrored else [0]):
     # Stock Mesen 2.2.1 originPositionCheckX subtracts 7-OffsetX for
     # mirrored sprites, although OffsetX is already screen-relative.
     # Pair the computed origin with this pixel's X to disambiguate all
     # eight columns; an origin-only guard shifts isolated pixel stripes.
     origin=origin_x+2*k-7 if mirrored else origin_x;origins.add(origin)
     sc=f'l3lavaRoom&fishPlayerX{px}&fishOriginX{origin}&'+('hmirror'if mirrored else'!hmirror')
     if mirrored:positions.add(origin_x+k);sc+=f'&fishPixelX{origin_x+k}'
     x,y=cells[dx,t];rules.append(f'[{sc}]<tile>43,{t:04X},FF301627,{x},{y},1,N')
conditions += [f'<condition>fishOriginX{x},originPositionCheckX,==,{x}'for x in sorted(origins)]
conditions += [f'<condition>fishPixelX{x},positionCheckX,==,{x}'for x in sorted(positions)]
text=(pack/'hires.txt').read_text();marker='# END LEVEL3_LAVA CONDITIONS\n';text=text.replace(marker,marker+'# BEGIN BIG_FISH_STABILITY CONDITIONS\n'+'\n'.join(conditions)+'\n# END BIG_FISH_STABILITY CONDITIONS\n')
marker='# BEGIN LEVEL3_LAVA MAPPINGS';text=text.replace(marker,'# BEGIN BIG_FISH_STABILITY MAPPINGS\n'+'\n'.join(rules)+'\n# END BIG_FISH_STABILITY MAPPINGS\n'+marker)
(pack/'hires.txt').write_text(text);atlas.save(pack/'Stage3_Lava_Tiles_2x.png')
(evidence/'registration.json').write_text(json.dumps(dict(conditions=len(conditions),tile_rules=len(rules),atlas_cells=20,atlas_rectangle=[0,496,320,512],object_type='26',speed_fraction='CC',direction_offsets={'lower_native_x':1,'upper_native_x':-1},scope='mode 10; native fish identities/palette; each complete fish at its player-relative hover equilibrium',multiple_fish_independent=True,source_left_range=[7,225],mirrored_origin_workaround=True,native_gameplay_modified=False),indent=2)+'\n')
print('Large fish: independent graphics-only half-pixel hover stabilization; native movement untouched.')
