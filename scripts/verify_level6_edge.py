"""Verify the opening platform's visible span and native controller-only fall."""
from pathlib import Path
import argparse,json,tempfile
import numpy as np
from PIL import Image
from verify_level6_opening_replay import compare_native,source,matches

p=argparse.ArgumentParser()
for key in ['before','after','out']:p.add_argument('--'+key,required=True)
a=p.parse_args();root=Path(__file__).resolve().parents[1];b,c=Path(a.before),Path(a.after)
frames,data,report=compare_native(root,b,c);assert frames==list(range(1,181))
assert not report['delivery_note_only_differences']
positions={n:[int.from_bytes(data['ram'][n][o:o+2],'little')for o in [0x74,0x76]]for n in frames}
states={n:data['ram'][n][0x300]for n in frames}
assert all(positions[n]==[128,176]and states[n]==0 for n in range(1,61))
assert all(positions[n][1]==176 and positions[n+1][0]-positions[n][0]in [0,1]for n in range(61,113))
assert positions[112]==[167,176]and states[112]==0
assert positions[113]==[167,176]and states[113]==2
assert positions[117]==[170,177]
assert all(positions[n+1][1]>=positions[n][1]for n in range(113,146))
assert positions[147]==[200,240]and states[147]==0
reg=json.loads((root/'art/level6_opening/registration.json').read_text())
atlas=Image.open(c/'mesen_home/HdPacks/Holy_Diver_(Tr)/Final_Citadel_Tiles_2x.png').convert('RGBA')
entries={int(e['tile'],16):e for e in reg['mappings']if e['scope']==reg['scopes']['9A8B']and e['palette']=='0F061636'}
ppu=data['ppu'][2];whole=Image.new('RGBA',(64,80));layout=[]
for y in range(5):
 row=[]
 for x in range(4):
  t=0x1700+ppu[0x2000+(24+y)*32+16+x];row.append(f'{t:04X}');e=entries[t];cx,cy=e['xy']
  whole.paste(atlas.crop((cx,cy,cx+16,cy+16)),(x*16,y*16))
 layout.append(row)
alpha=np.array(whole.getchannel('A'))
# Native stone has one transparent top row and a one-pixel rough ridge.
assert np.all(alpha[4:6]==255)and not alpha[:2].any()
assert all(np.flatnonzero(alpha[:,x])[0]in [2,4]for x in range(64))
hits=[]
with tempfile.TemporaryDirectory()as temporary:
 path=Path(temporary)/'platform.png';whole.save(path);item=source(path)
 for n in range(2,141):
  im=np.array(Image.open(c/'frames'/f'{n:06}.png').convert('RGB'));found=matches(im,item)
  if found:hits.append(dict(frame=n,positions=found))
assert any(h['frame']<=60 for h in hits)and any(h['frame']>=117 for h in hits)
report.update(controller_only=True,no_jump=True,unchanged_embedded_state=True,
 left_stop=dict(frames=[1,60],world_position=[128,176]),
 platform_native_world_bounds=dict(left=128,right_exclusive=160,top=192),
 native_fall_start=dict(frame=113,world_position=[167,176]),
 native_first_descent=dict(frame=117,world_position=[170,177]),
 native_lower_platform_landing=dict(frame=147,world_position=[200,240]),
 native_platform_layout=layout,whole_platform_dimensions=list(whole.size),
 complete_platform_source_matches=hits,continuous_stone_across_full_span=True,
 native_ridge_top_rows=[1,2],continuous_opaque_row_native=2)
Path(a.out).write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({k:v for k,v in report.items()if k!='complete_platform_source_matches'},indent=2))
print('Complete platform matches:',len(hits))
