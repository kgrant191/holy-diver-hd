"""Verify the green entry floor's full span, left stop and native right walk-off."""
from pathlib import Path
import argparse,json,tempfile
import numpy as np
from PIL import Image
from verify_level6_late_replay import compare
from verify_level6_opening_replay import source,matches
from verify_level6_opening_rules import native_hull
p=argparse.ArgumentParser()
for k in ['before','after','out']:p.add_argument('--'+k,required=True)
a=p.parse_args();root=Path(__file__).resolve().parents[1];b,c=Path(a.before),Path(a.after);frames,data,report=compare(root,b,c);assert frames==list(range(1,701))
pos={n:[int.from_bytes(data['ram'][n][o:o+2],'little')for o in [0x74,0x76]]for n in frames};states={n:data['ram'][n][0x300]for n in frames}
assert all(pos[n]==[23,96]and states[n]==0 for n in range(342,381))
assert all(pos[n][1]==96 and pos[n+1][0]-pos[n][0]in [0,1]for n in range(381,530))
assert pos[530]==[135,96]and pos[531]==[136,96]and states[531]==2
first_descent=next(n for n in range(531,545)if pos[n][1]>96);assert first_descent==535
pack=c/'mesen_home/HdPacks/Holy_Diver_(Tr)';reg=json.loads((root/'art/level6_late/registration.json').read_text());images=[l[5:]for l in(pack/'hires.txt').read_text().splitlines()if l.startswith('<img>')]
entries={}
for e in reg['clones']+reg['mappings']:
 line=e['rule']
 if line.startswith('['+reg['scopes']['A20B']+']<tile>'):
  f=line.split('<tile>')[1].split(',')
  entries.setdefault((int(f[1],16),f[2]),f)
ppu=data['ppu'][450];whole=Image.new('RGBA',(224,256));native_mask=Image.new('L',whole.size);layout=[];cache={}
patterns={int(k,16):bytes.fromhex(v)for k,v in json.loads((root/'art/level6_opening/native_patterns.json').read_text()).items()}
for y in range(16):
 row=[]
 for x in range(14):
  tx,ty=2+x,14+y;t=0x1700+ppu[0x2000+ty*32+tx];at=ppu[0x23c0+ty//4*8+tx//4];pi=(at>>((ty%4)//2*4+(tx%4)//2*2))&3;pal=(bytes([ppu[0x3f00]])+ppu[0x3f01+4*pi:0x3f04+4*pi]).hex().upper();row.append([f'{t:04X}',pal]);f=entries[t,pal];i,cx,cy=int(f[0]),int(f[3]),int(f[4])
  if i not in cache:cache[i]=Image.open(pack/images[i]).convert('RGBA')
  whole.paste(cache[i].crop((cx,cy,cx+16,cy+16)),(x*16,y*16))
  assert pal in ['0F0B1B3B','0F0A1A29']
  if pal=='0F0B1B3B':native_mask.paste(Image.fromarray(native_hull(patterns[t]).astype(np.uint8)*255),(x*16,y*16))
 layout.append(row)
assert np.array_equal(np.array(whole.getchannel('A')),np.array(native_mask))
hits=[]
with tempfile.TemporaryDirectory()as temp:
 path=Path(temp)/'platform.png';whole.save(path);item=source(path)
 for n in range(342,539):
  im=np.array(Image.open(c/'frames'/f'{n:06}.png').convert('RGB'));found=matches(im,item)
  if found:hits.append(dict(frame=n,positions=found))
assert len(hits)>80,len(hits)
report.update(controller_only=True,unchanged_embedded_state=True,no_jump_after_branch=True,left_stop=dict(frames=[342,380],world_position=[23,96]),
 platform_native_world_bounds=dict(left=16,right_exclusive=128,top=112),native_fall_start=dict(frame=531,world_position=pos[531]),native_first_descent=dict(frame=first_descent,world_position=pos[first_descent]),
 native_platform_layout=layout,whole_platform_dimensions=list(whole.size),complete_platform_source_matches=hits)
Path(a.out).write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:v for k,v in report.items()if k not in ['native_platform_layout','complete_platform_source_matches']},indent=2));print('Complete platform matches:',len(hits))
