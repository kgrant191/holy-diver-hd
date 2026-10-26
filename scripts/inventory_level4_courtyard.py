"""Reproduce recorded room/palette identities and exact pickup-bank proofs."""
from pathlib import Path
from collections import Counter,defaultdict
import argparse,json,subprocess,sys
p=argparse.ArgumentParser()
for key in ['capture','rom','out']:p.add_argument('--'+key,required=True)
a=p.parse_args();c=Path(a.capture);out=Path(a.out);out.mkdir(parents=True,exist_ok=True)
# Retain the complete raw inventory, including load/menu phases, for audit.
subprocess.run([sys.executable,str(Path(__file__).with_name('inventory_level3_finale.py')),'--capture',str(c),'--rom',a.rom,'--out',str(out)],check=True)
for name in ['shared_patterns.json','terrain_aliases.json']:(out/name).unlink()
expected={'AAF9':'0f1727370f0717230f0717370f031323','AB71':'0f0717370f0717030f0737030f031323','AC61':'0f1727370f0717270f0717370f031323'}
observed=defaultdict(lambda:defaultdict(Counter));views=defaultdict(set)
for f in sorted((c/'ram').glob('*.bin')):
 ram=f.read_bytes();room=f'{int.from_bytes(ram[0x78:0x7a],"little"):04X}'
 if room not in expected:continue
 pp=(c/'ppu'/f.name).read_bytes()
 if pp[0x3f00:0x3f10].hex()!=expected[room]:continue
 v=json.loads((c/'view'/(f.stem+'.json')).read_text());vv=v['vram']
 sx=(vv&31)*8+v['xscroll']+(256 if vv&0x400 else 0)
 sy=((vv>>5)&31)*8+((vv>>12)&7)+(240 if vv&0x800 else 0)
 def cell(xx,yy):
  tx,ty=xx%32,yy%30;nt=0x2000+xx//32%2*0x400+yy//30%2*0x800
  t=0xb00+pp[nt+ty*32+tx];attr=pp[nt+960+ty//4*8+tx//4]
  pa=(attr>>((ty%4)//2*4+(tx%4)//2*2))&3
  pal=(bytes([pp[0x3f00]])+pp[0x3f01+pa*4:0x3f04+pa*4]).hex().upper()
  return f'{t:04X}',pal
 for yy in range(sy//8,(sy+239)//8+1):
  for xx in range(sx//8,(sx+255)//8+1):
   t,pal=cell(xx,yy);observed[room][pal][t]+=1
 views[room].add(cell((sx+128)//8,(sy+16)//8))
(out/'stable_backgrounds.json').write_text(json.dumps({r:{p:dict(sorted(ts.items()))for p,ts in pals.items()}for r,pals in observed.items()},indent=2)+'\n')
(out/'stable_view_guards.json').write_text(json.dumps({r:sorted(ts)for r,ts in views.items()},indent=2)+'\n')
rom=Path(a.rom).read_bytes();start=16+rom[4]*16384+(512 if rom[6]&4 else 0);chr=rom[start:]
tiles=[chr[i:i+16]for i in range(0,len(chr),16)]
aliases={f'{t:04X}':[f'{i:04X}'for i,v in enumerate(tiles)if v==tiles[t]]for t in [0xa92,0xa93,*range(0xadb,0xae3)]}
(out/'item_enemy_aliases.json').write_text(json.dumps(aliases,indent=2)+'\n')
patterns=json.loads((out/'native_patterns.json').read_text())
for source,targets in aliases.items():
 for target in targets:
  patterns[target]=tiles[int(target,16)].hex();assert patterns[target]==patterns[source]
(out/'native_patterns.json').write_text(json.dumps(patterns,indent=2)+'\n')
