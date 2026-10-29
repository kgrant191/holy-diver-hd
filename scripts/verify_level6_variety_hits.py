"""Require actual whole sentinel matches during native silver and blue hit phases."""
from pathlib import Path
from collections import Counter
import json,sys
import numpy as np
from PIL import Image
from verify_level6_opening_replay import source,matches
r=Path(__file__).resolve().parents[1];c=Path(sys.argv[1]);out=Path(sys.argv[2]);hits={};counts=Counter();examples={}
sources={(pal,i,mirror):source(r/f'art/level4_staff/sentinel_{i}_{pal}.png',mirror)for pal in ['FF102030','FF122232']for i in range(4)for mirror in [False,True]}
frames=sorted(int(p.stem)for p in(c/'oam').glob('*.bin'))
for n in frames:
 if n<2:continue
 ppu=(c/'ppu'/f'{n:06}.bin').read_bytes();oam=(c/'oam'/f'{n:06}.bin').read_bytes();ram=(c/'ram'/f'{n:06}.bin').read_bytes();room=int.from_bytes(ram[0x78:0x7a],'little')
 if room not in [0x9f3b,0xa02b,0xa0df]:continue
 palettes=set()
 for j in range(0,256,4):
  y,t,attr,x=oam[j:j+4]
  if y<239 and 0xa9<=t<=0xdd:
   pal='FF'+ppu[0x3f11+(attr&3)*4:0x3f14+(attr&3)*4].hex().upper()
   if pal in ['FF102030','FF122232']:palettes.add(pal)
 if not palettes:continue
 im=np.array(Image.open(c/'frames'/f'{n:06}.png').convert('RGB'))
 for pal in palettes:
  counts[pal]+=1
  for i in range(4):
   for mirror in [False,True]:
    key=f'{pal}_pose{i}_'+('left'if mirror else'right')
    if key in hits:continue
    found=matches(im,sources[pal,i,mirror])
    if found:hits[key]=dict(frame=n,positions=found,native_palette=pal);examples.setdefault(pal,n)
assert all(p in examples for p in ['FF102030','FF122232'])
# Native horizontal flipping remains demonstrable for both hit colors.
for pal in ['FF102030','FF122232']:
 assert any(k.startswith(pal)and k.endswith('left')for k in hits),(pal,'no mirrored hit match')
 assert any(k.startswith(pal)and k.endswith('right')for k in hits),(pal,'no unmirrored hit match')
result=dict(native_hit_palette_frame_counts=counts,whole_hit_source_matches=hits,unobserved_whole_sources=sorted(f'{p}_pose{i}_'+('left'if m else'right')for p,i,m in sources if f'{p}_pose{i}_'+('left'if m else'right')not in hits))
out.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(dict(counts=counts,matches={k:v['frame']for k,v in hits.items()}),indent=2))
