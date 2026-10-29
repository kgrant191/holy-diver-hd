"""Prove the complete corridor platform and native slow walk-off boundary."""
from pathlib import Path
import argparse,json,tempfile
import numpy as np
from PIL import Image
from verify_level6_next_replay import compare
from verify_level6_opening_replay import source,matches

p=argparse.ArgumentParser()
for k in ['before','after','out']:p.add_argument('--'+k,required=True)
a=p.parse_args();root=Path(__file__).resolve().parents[1];b,c=Path(a.before),Path(a.after)
frames,data,report=compare(root,b,c);assert frames==list(range(1400,1767));assert not report['install_note_only_differences']
positions={n:[int.from_bytes(data['ram'][n][o:o+2],'little')for o in [0x74,0x76]]for n in frames}
states={n:data['ram'][n][0x300]for n in frames}
assert all(positions[n]==[527,144]and states[n]==0 for n in range(1427,1487))
assert all(positions[n][1]==144 and positions[n+1][0]-positions[n][0]in [0,1]for n in range(1487,1689))
assert positions[1689]==[679,144]and states[1689]==1
assert positions[1690]==[680,144]and states[1690]==2
first_descent=next(n for n in range(1690,1707)if positions[n][1]>144)
assert all(positions[n+1][1]>=positions[n][1]for n in range(1690,1725))
pack=c/'mesen_home/HdPacks/Holy_Diver_(Tr)';reg=json.loads((root/'art/level6_next/registration.json').read_text())
text=(pack/'hires.txt').read_text();images=[l[5:]for l in text.splitlines()if l.startswith('<img>')]
entries={}
for e in reg['mappings']+reg['clones']:
 line=e['rule']
 if line.startswith('['+reg['scopes']['9F3B']+']<tile>'):
  f=line.split('<tile>')[1].split(',')
  if f[2]=='0F162738':entries.setdefault(int(f[1],16),f)
ppu=data['ppu'][1580];whole=Image.new('RGBA',(288,160));layout=[];cache={}
for y in range(10):
 row=[]
 for x in range(18):
  t=0x1700+ppu[0x2000+(20+y)*32+2+x];row.append(f'{t:04X}');f=entries[t];i,cx,cy=int(f[0]),int(f[3]),int(f[4])
  if i not in cache:cache[i]=Image.open(pack/images[i]).convert('RGBA')
  whole.paste(cache[i].crop((cx,cy,cx+16,cy+16)),(x*16,y*16))
 layout.append(row)
# The solid full-width row and the native rough top contour remain exact.
alpha=np.array(whole.getchannel('A'));assert np.all(alpha[4:6]==255)
hits=[]
with tempfile.TemporaryDirectory()as temp:
 path=Path(temp)/'platform.png';whole.save(path);item=source(path)
 for n in range(1487,1697):
  im=np.array(Image.open(c/'frames'/f'{n:06}.png').convert('RGB'));found=matches(im,item)
  if found:hits.append(dict(frame=n,positions=found))
assert len(hits)>80,hits
report.update(controller_only=True,unchanged_embedded_state=True,no_jump_after_branch=True,
 left_stop=dict(frames=[1427,1486],world_position=[527,144]),
 platform_native_world_bounds=dict(left=528,right_exclusive=672,top=160),
 native_fall_start=dict(frame=1690,world_position=positions[1690]),
 native_first_descent=dict(frame=first_descent,world_position=positions[first_descent]),
 native_platform_layout=layout,whole_platform_dimensions=list(whole.size),complete_platform_source_matches=hits)
Path(a.out).write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({k:v for k,v in report.items()if k not in ['native_platform_layout','complete_platform_source_matches']},indent=2));print('Complete platform matches:',len(hits))
