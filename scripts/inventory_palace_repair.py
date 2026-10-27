"""Read the user stair-climb movie's visible native identities and guards."""
from pathlib import Path
from collections import defaultdict,Counter
import argparse,json,hashlib
p=argparse.ArgumentParser()
for k in ['capture','rom','out']:p.add_argument('--'+k,required=True)
a=p.parse_args();c=Path(a.capture);out=Path(a.out);out.mkdir(parents=True,exist_ok=True)
rom=Path(a.rom).read_bytes();ch=rom[16+rom[4]*16384+(512 if rom[6]&4 else 0):];seen=defaultdict(lambda:defaultdict(Counter));guards=defaultdict(set);sprites=defaultdict(Counter);frames=defaultdict(list)
for f in sorted((c/'ram').glob('*.bin')):
 r=f.read_bytes();room=f'{int.from_bytes(r[0x78:0x7a],"little"):04X}'
 if room not in {'8816','888E'}:continue
 pp=(c/'ppu'/f.name).read_bytes()
 if pp[4096:8192]!=ch[0x1100*16:0x1200*16]or pp[0x3f00:0x3f04].hex()!='0f0f0717':continue
 v=json.loads((c/'view'/(f.stem+'.json')).read_text());vv=v['vram'];sx=(vv&31)*8+v['xscroll']+(256 if vv&0x400 else 0);sy=((vv>>5)&31)*8+((vv>>12)&7)+(240 if vv&0x800 else 0)
 def cell(x,y):
  tx,ty=x%32,y%30;nt=0x2000+x//32%2*0x400+y//30%2*0x800;t=0x1100+pp[nt+ty*32+tx];at=pp[nt+960+ty//4*8+tx//4];pa=at>>((ty%4)//2*4+(tx%4)//2*2)&3;pal=(bytes([pp[0x3f00]])+pp[0x3f01+pa*4:0x3f04+pa*4]).hex().upper();return f'{t:04X}',pal
 for yy in range(sy//8,(sy+239)//8+1):
  for xx in range(sx//8,(sx+255)//8+1):
   t,pal=cell(xx,yy);seen[room][pal][t]+=1
 guards[room].add(cell((sx+128)//8,(sy+16)//8));frames[room].append(int(f.stem))
 oam=(c/'oam'/f.name).read_bytes()
 for i in range(0,256,4):
  y,t,at,x=oam[i:i+4]
  if y<240:sprites[room][f'{0x1000+t:04X}/FF'+pp[0x3f11+(at&3)*4:0x3f14+(at&3)*4].hex().upper()]+=1
report=dict(visible_backgrounds={r:{pal:dict(sorted(ts.items()))for pal,ts in pals.items()}for r,pals in seen.items()},view_guards={r:sorted(s)for r,s in guards.items()},sprites={r:dict(sorted(v.items()))for r,v in sprites.items()},frames={r:dict(first=min(s),last=max(s),samples=len(s))for r,s in frames.items()},movie=json.loads((c/'result.json').read_text()))
(out/'inventory.json').write_text(json.dumps(report,indent=2)+'\n')
patterns={f'{t:04X}':ch[t*16:t*16+16].hex()for t in range(0x1100,0x1400)};(out/'native_patterns.json').write_text(json.dumps(patterns,indent=2)+'\n')
for room,v in report['visible_backgrounds'].items():print(room,{pal:list(ts)for pal,ts in v.items()},'guards',report['view_guards'][room])
