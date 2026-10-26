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
conditions=[];rules=[]
for i in range(16):
 for suffix,addr,val in [('Type',0x300+i,0x26),('Speed',0x3c0+i,0xcc),('Positive',0x3d0+i,0),('Negative',0x3d0+i,0x80),('Unhit',0x330+i,0)]:conditions.append(f'<condition>fishSmooth{suffix}{i},memoryCheckConstant,{addr:04X},==,{val:02X}')
for i in range(16):
 scope='l3lavaRoom&l3lavaLo&l3lavaHi&'+ '&'.join((''if j==i else'!')+f'fishSmoothType{j}'for j in range(16))+f'&fishSmoothSpeed{i}&fishSmoothUnhit{i}'
 for direction,world in [('Positive',-1),('Negative',1)]:
  for mirrored in [False,True]:
   dx=-world if mirrored else world
   sc=scope+f'&fishSmooth{direction}{i}&'+('hmirror'if mirrored else'!hmirror')
   for t in range(0x6dd,0x6e7):
    x,y=cells[dx,t];rules.append(f'[{sc}]<tile>43,{t:04X},FF301627,{x},{y},1,N')
text=(pack/'hires.txt').read_text();marker='# END LEVEL3_LAVA CONDITIONS\n';text=text.replace(marker,marker+'# BEGIN BIG_FISH_STABILITY CONDITIONS\n'+'\n'.join(conditions)+'\n# END BIG_FISH_STABILITY CONDITIONS\n')
marker='# BEGIN LEVEL3_LAVA MAPPINGS';text=text.replace(marker,'# BEGIN BIG_FISH_STABILITY MAPPINGS\n'+'\n'.join(rules)+'\n# END BIG_FISH_STABILITY MAPPINGS\n'+marker)
(pack/'hires.txt').write_text(text);atlas.save(pack/'Stage3_Lava_Tiles_2x.png')
(evidence/'registration.json').write_text(json.dumps(dict(conditions=len(conditions),tile_rules=len(rules),atlas_cells=20,atlas_rectangle=[0,496,320,512],object_type='26',speed_fraction='CC',direction_offsets={'Positive':-1,'Negative':1},scope='mode 10 / room 9AA6; exactly one large fish; hover speed; no damage timer',native_gameplay_modified=False),indent=2)+'\n')
print('Large fish: graphics-only half-pixel hover stabilization; native movement untouched.')
