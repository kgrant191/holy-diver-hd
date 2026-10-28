"""Inventory only the supplied Demonic Palace movie; never mutate emulated state."""
from pathlib import Path
from collections import defaultdict,Counter
import argparse,json,subprocess,sys
p=argparse.ArgumentParser()
for k in ['capture','rom','out']:p.add_argument('--'+k,required=True)
a=p.parse_args();c=Path(a.capture);out=Path(a.out);out.mkdir(parents=True,exist_ok=True)
subprocess.run([sys.executable,str(Path(__file__).with_name('inventory_level3_finale.py')),'--capture',a.capture,'--rom',a.rom,'--out',a.out],check=True)
for name in ['shared_patterns.json','terrain_aliases.json']:(out/name).unlink()
rom=Path(a.rom).read_bytes();ch=rom[16+rom[4]*16384+(512 if rom[6]&4 else 0):];tiles=[ch[i:i+16]for i in range(0,len(ch),16)]
aliases={f'{i:04X}':[f'{j:04X}'for j,t in enumerate(tiles)if t==tiles[i]]for i in range(0x1000,0x1400)}
(out/'native_aliases.json').write_text(json.dumps(aliases,indent=2)+'\n')
patterns=json.loads((out/'native_patterns.json').read_text())
for i in [*range(0xa00,0xa75),*range(0x1300,0x1400)]:patterns[f'{i:04X}']=tiles[i].hex()
(out/'native_patterns.json').write_text(json.dumps(patterns,indent=2)+'\n')
rooms={'850A':24,'8672':4,'86EA':8,'8762':4,'8816':4};seen=defaultdict(lambda:defaultdict(Counter));guards=defaultdict(set)
for f in sorted((c/'ram').glob('*.bin')):
 ram=f.read_bytes();room=f'{int.from_bytes(ram[0x78:0x7a],"little"):04X}'
 if room not in rooms:continue
 pp=(c/'ppu'/f.name).read_bytes()
 if pp[4096:8192]!=ch[0x1100*16:0x1200*16]:continue
 if pp[0x3f00:0x3f04].hex() not in ['0f071727','0f061634','30061634','31061634','0f0f0717']:continue
 if room=='8816'and pp[0x3f00:0x3f04].hex()!='0f0f0717':continue
 v=json.loads((c/'view'/(f.stem+'.json')).read_text());vv=v['vram'];sx=(vv&31)*8+v['xscroll']+(256 if vv&0x400 else 0);sy=((vv>>5)&31)*8+((vv>>12)&7)+(240 if vv&0x800 else 0)
 def cell(x,y):
  tx,ty=x%32,y%30;nt=0x2000+x//32%2*0x400+y//30%2*0x800;t=0x1100+pp[nt+ty*32+tx];at=pp[nt+960+ty//4*8+tx//4];pa=at>>((ty%4)//2*4+(tx%4)//2*2)&3;pal=(bytes([pp[0x3f00]])+pp[0x3f01+pa*4:0x3f04+pa*4]).hex().upper();return f'{t:04X}',pal
 for yy in range(sy//8,(sy+239)//8+1):
  for xx in range(sx//8,(sx+255)//8+1):
   t,pal=cell(xx,yy);seen[room][pal][t]+=1
 guards[room].add(cell((sx+128)//8,(sy+16)//8))
(out/'visible_backgrounds.json').write_text(json.dumps({r:{pal:dict(sorted(ts.items()))for pal,ts in pals.items()}for r,pals in seen.items()},indent=2)+'\n')
(out/'view_guards.json').write_text(json.dumps({r:sorted(s)for r,s in guards.items()},indent=2)+'\n')
