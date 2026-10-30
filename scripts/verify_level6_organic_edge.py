"""Verify the full organic pillar, supported left stop and native right walk-off."""
from pathlib import Path
import argparse,json,tempfile
import numpy as np
from PIL import Image
from verify_level6_organic_replay import compare
from verify_level6_opening_replay import source,matches
from verify_level6_opening_rules import native_hull
p=argparse.ArgumentParser()
for k in ['before','after','out']:p.add_argument('--'+k,required=True)
a=p.parse_args();root=Path(__file__).resolve().parents[1];b,c=Path(a.before),Path(a.after);frames,data,report=compare(root,b,c);assert frames==list(range(1,732))
pos={n:[int.from_bytes(data['ram'][n][o:o+2],'little')for o in [0x74,0x76]]for n in frames};state={n:data['ram'][n][0x300]for n in frames}
assert all(pos[n]==[794,80]and state[n]==0 for n in range(566,576))
assert all(pos[n][1]==80 and state[n]in [0,1]and pos[n+1][0]-pos[n][0]in [0,1]for n in range(576,635))
assert pos[635]==[839,80]and state[635]==0 and pos[636]==[839,80]and state[636]==2
assert next(n for n in range(636,650)if pos[n][1]>80)==640 and pos[640]==[842,81]
reg=json.loads((root/'art/level6_organic/registration.json').read_text());atlas=Image.open(root/'art/level6_organic/Final_Citadel_Organic_2x.png').convert('RGBA');cells={int(e['tile'],16):e['xy']for e in reg['mappings']if e['palette']=='0F162638'and e['kind']=='native organic terrain'}
patterns={int(k,16):bytes.fromhex(v)for k,v in json.loads((root/'art/level6_opening/native_patterns.json').read_text()).items()};ppu=data['ppu'][590];whole=Image.new('RGBA',(64,288));mask=Image.new('L',whole.size);layout=[]
for y in range(18):
 row=[]
 for x in range(4):
  tx,ty=4+x,12+y;t=0x1b00+ppu[0x2400+ty*32+tx];row.append(f'{t:04X}');cx,cy=cells[t];whole.paste(atlas.crop((cx,cy,cx+16,cy+16)),(x*16,y*16));mask.paste(Image.fromarray(native_hull(patterns[t]).astype(np.uint8)*255),(x*16,y*16))
 layout.append(row)
assert np.array_equal(np.array(whole.getchannel('A')),np.array(mask))
hits=[]
with tempfile.TemporaryDirectory()as temp:
 path=Path(temp)/'platform.png';whole.save(path);item=source(path)
 for n in range(566,641):
  im=np.array(Image.open(c/'frames'/f'{n:06}.png').convert('RGB'));found=matches(im,item)
  if found:hits.append(dict(frame=n,positions=found))
assert len(hits)>=50,len(hits)
report.update(controller_only=True,unchanged_embedded_state=True,no_jump_after_branch=True,left_stop=dict(frames=[566,575],world_position=[794,80]),platform_native_world_bounds=dict(left=800,right_exclusive=832,top=96),native_fall_start=dict(frame=636,world_position=pos[636]),native_first_descent=dict(frame=640,world_position=pos[640]),whole_platform_dimensions=list(whole.size),native_platform_layout=layout,complete_platform_source_matches=hits)
Path(a.out).write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:v for k,v in report.items()if k not in ['native_platform_layout','complete_platform_source_matches']},indent=2));print('Complete platform matches',len(hits))
