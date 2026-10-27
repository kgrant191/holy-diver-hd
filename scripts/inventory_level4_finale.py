"""Inventory the supplied final temple recording and prove native bank reuse."""
from pathlib import Path
from collections import Counter,defaultdict
import argparse,json,subprocess,sys
p=argparse.ArgumentParser()
for k in ['capture','rom','out']:p.add_argument('--'+k,required=True)
a=p.parse_args();c=Path(a.capture);out=Path(a.out);out.mkdir(exist_ok=True,parents=True)
subprocess.run([sys.executable,str(Path(__file__).with_name('inventory_level3_finale.py')),'--capture',a.capture,'--rom',a.rom,'--out',a.out],check=True)
rom=Path(a.rom).read_bytes();chr=rom[16+rom[4]*16384:];tiles=[chr[i:i+16]for i in range(0,len(chr),16)];patterns=json.loads((out/'native_patterns.json').read_text())
subjects={*range(0xcb6,0xcbe),*range(0xe00,0xe75),0xe8e,*range(0xeb4,0xeb8)};aliases={f'{t:04X}':[f'{i:04X}'for i,v in enumerate(tiles)if v==tiles[t]]for t in sorted(subjects)}
for t in range(256):assert tiles[0xb00+t]==tiles[0xd00+t];patterns[f'{0xd00+t:04X}']=tiles[0xd00+t].hex()
for t in range(0x75):assert tiles[0xa00+t]==tiles[0xe00+t];patterns[f'{0xa00+t:04X}']=tiles[0xa00+t].hex()
for targets in aliases.values():
 for t in targets:patterns[t]=tiles[int(t,16)].hex()
observed=defaultdict(lambda:defaultdict(set));groups=Counter();examples={}
for f in sorted((c/'ram').glob('*.bin')):
 ram=f.read_bytes();room=f'{int.from_bytes(ram[0x78:0x7a],"little"):04X}'
 if room not in ['AE41','AEF5','AFA9']:continue
 pp=(c/'ppu'/f.name).read_bytes();v=json.loads((c/'view'/(f.stem+'.json')).read_text())
 if room in ['AE41','AEF5']and pp[0x3f00:0x3f10].hex()=='0f1727370f0717230f0717370f031323'and not v['grayscale']:
  for nt in [0x2000,0x2400,0x2800,0x2c00]:
   for y in range(30):
    for x in range(32):
     attr=pp[nt+960+y//4*8+x//4];pa=attr>>((y%4)//2*4+(x%4)//2*2)&3;pal=(bytes([pp[0x3f00]])+pp[0x3f01+pa*4:0x3f04+pa*4]).hex().upper();observed[room][pal].add(f'{0xd00+pp[nt+y*32+x]:04X}')
 if room=='AFA9':
  for y0 in [16,20,24]:
   layout=tuple((f'{0xf00+pp[0x2000+(y0+y)*32+12+x]:04X}',x,y)for y in range(4)for x in range(7))
   if any(t=='0F00'for t,x,y in layout):continue
   groups[layout]+=1;examples.setdefault(layout,dict(frame=int(f.stem),band=(y0-16)//4))
layouts=[dict(name=f'band_{i}',count=count,example=examples[layout],layout=layout)for i,(layout,count)in enumerate(groups.most_common())]
for name,data in [('native_patterns',patterns),('native_aliases',aliases),('stable_backgrounds',{room:{pal:sorted(ts)for pal,ts in ps.items()}for room,ps in observed.items()}),('boss_band_layouts',layouts)]: (out/(name+'.json')).write_text(json.dumps(data,indent=2)+'\n')
print('Stable tower bands:',sum(q['count']>10 for q in layouts))
