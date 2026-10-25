"""Measure whole and partially visible wood cells from the supplied movie capture."""
from pathlib import Path
from collections import Counter,defaultdict
import json
import argparse
a=argparse.ArgumentParser();a.add_argument('--capture',required=True);a.add_argument('--out');args=a.parse_args()
p=Path(args.capture);r=Path(__file__).resolve().parents[1];hist={k:defaultdict(Counter)for k in [0x988a,0x997a]};views=Counter()
for f in sorted((p/'ram').glob('*.bin')):
 n=int(f.stem);ram=f.read_bytes();ptr=int.from_bytes(ram[0x78:0x7a],'little')
 if ptr not in hist or not(40<=n<=1368 or 1432<=n<=1944):continue
 v=json.loads((p/'view'/f'{n:06}.json').read_text());a=v['vram'];sx=((a&31)<<3)|v['xscroll']|(256 if a&0x400 else 0);sy=((a&0x3e0)>>2)|((a&0x7000)>>12);sy+=240 if a&0x800 else 0
 camera=int.from_bytes(ram[0x60:0x62],'little');cx=sx+round((camera-sx)/512)*512 if ptr==0x988a else 0;cy=0 if ptr==0x988a else sy
 if not(0<=cx<=768 and 0<=cy<=240):continue
 pp=(p/'ppu'/f'{n:06}.bin').read_bytes();views[ptr]+=1
 for y in range(cy//8,(cy+239)//8+1):
  for x in range(cx//8,(cx+255)//8+1):
   px,py=(x*8)%512,(y*8)%480;nt=0x2000+(px//256)*0x400+(py//240)*0x800;tx,ty=(px%256)//8,(py%240)//8
   t=pp[nt+ty*32+tx]+0x700;at=pp[nt+960+(ty//4)*8+tx//4];pal=(at>>(((ty%4)//2)*4+((tx%4)//2)*2))&3
   colors=pp[0x3f00+pal*4:0x3f04+pal*4].hex().upper();hist[ptr][(x,y)][(t,colors)]+=1
out={}
for ptr,coords in hist.items():
 woods=[]
 for (x,y),counts in coords.items():
  (t,pal),n=counts.most_common(1)[0]
  if 0x752<=t<=0x767 and pal=='0F091929':woods.append([x,y,f'{t:04X}'])
 name='forest'if ptr==0x988a else'tree';out[name]=dict(size=[1024,240]if name=='forest'else[256,480],cells=sorted(woods),observed_views=views[ptr],visible_cells=len(coords))
 print(name,len(woods),'bounds',min(x for x,y,t in woods),max(x for x,y,t in woods),min(y for x,y,t in woods),max(y for x,y,t in woods))
(Path(args.out)if args.out else r/'art/level3_review/wood_geometry.json').write_text(json.dumps(out,indent=2)+'\n')
