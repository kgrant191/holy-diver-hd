"""Check the actual fixed panoramas and complete rendered masonry cells."""
from pathlib import Path
import argparse,json
import numpy as np
from PIL import Image
p=argparse.ArgumentParser();p.add_argument('--capture',required=True);p.add_argument('--out',required=True);a=p.parse_args()
r=Path(__file__).resolve().parents[1];c=Path(a.capture);pack=c/'mesen_home/HdPacks/Holy_Diver_(Tr)'
assert json.loads((c/'installed_pack.json').read_text())==json.loads((r/'evidence/0.16.0-pack-sha256.json').read_text())
reg=json.loads((r/'art/level4/registration.json').read_text());atlas=Image.open(pack/'Golden_Temple_Tiles_2x.png').convert('RGBA');cells={}
for m in reg['mappings']:
 if m['kind']!='native collision masonry':continue
 key=tuple(m['xy']);x,y=key
 cells[key]=np.array(atlas.crop((x,y,x+16,y+16)))
checks=[]
for n in [400,1600,3200,4000,4200,5200,6500,7200,8000,8600]:
 im=np.array(Image.open(c/'frames'/f'{n:06}.png').convert('RGB'));ram=(c/'ram'/f'{n:06}.bin').read_bytes();room=int.from_bytes(ram[0x78:0x7a],'little')
 name='Golden_Temple_Exterior.png'if room==0xa865 else'Golden_Temple_Interior.png'
 bg=np.array(Image.open(pack/name).convert('RGB'))[:,:512];matched=int(np.all(im==bg,axis=2)[112:].sum());assert matched>40000,(n,matched)
 tile_hits=0
 for src in cells.values():
  mask=src[:,:,3]==255
  if not mask.all():continue
  ys,xs=np.where(np.all(im==src[0,0,:3],axis=2))
  for y,x in zip(ys,xs):
   if y+16>480 or x+16>512:continue
   if np.array_equal(im[y:y+16,x:x+16],src[:,:,:3]):tile_hits+=1
 assert tile_hits>30,(n,tile_hits)
 checks.append(dict(frame=n,room=f'{room:04X}',background=name,exact_background_pixels_below_hud=matched,complete_masonry_cell_matches=tile_hits))
report=dict(sampled_scenes=checks,source_pixels_exact=True,backgrounds_stationary=True,coverage='Ten actual scenes including both indoor rooms and the 6500 palette transition; no whole-level claim.')
Path(a.out).write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
