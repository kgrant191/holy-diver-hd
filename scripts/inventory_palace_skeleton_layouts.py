"""Record complete recurring skeleton layouts; exclude clipped/transition OAM."""
from pathlib import Path
from collections import Counter
import argparse,json
p=argparse.ArgumentParser();p.add_argument('--capture',required=True);p.add_argument('--out',required=True);a=p.parse_args();root=Path(a.capture);counts=Counter();examples={}
for f in sorted((root/'oam').glob('*.bin')):
 ram=(root/'ram'/f.name).read_bytes()
 if ram[0x78:0x7a].hex()not in ['e68a','d68b','4e8c','3e8d']:continue
 o=f.read_bytes();cells=[(t,x,y+1,at&0xc0)for y,t,at,x in zip(o[::4],o[1::4],o[2::4],o[3::4])if y<239 and 0xe5<=t<=0xf4]
 if not 8<=len(cells)<=11 or len(set(t for t,x,y,at in cells))!=len(cells)or len(set(at for t,x,y,at in cells))!=1:continue
 x0=min(x for t,x,y,at in cells);y0=min(y for t,x,y,at in cells);w=max(x for t,x,y,at in cells)-x0+8;h=max(y for t,x,y,at in cells)-y0+8
 if w!=32 or h not in [24,32]:continue
 key=tuple(sorted((f'{t+0x1200:04X}',w-8-(x-x0)if at&64 else x-x0,y-y0)for t,x,y,at in cells));counts[key]+=1;examples.setdefault(key,int(f.stem))
records=[dict(cells=key,samples=count,example=examples[key])for key,count in counts.most_common()if count>=100]
assert len(records)==4
Path(a.out).write_text(json.dumps(records,indent=2)+'\n');print([(x['example'],x['samples'])for x in records])
