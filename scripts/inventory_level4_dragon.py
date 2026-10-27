"""Inventory native dragon poses, pickup identities and exact CHR copies."""
from pathlib import Path
from collections import Counter,defaultdict
import argparse,json,subprocess,sys

p=argparse.ArgumentParser();p.add_argument('--capture',action='append',required=True)
for k in ['rom','out']:p.add_argument('--'+k,required=True)
a=p.parse_args();out=Path(a.out);out.mkdir(parents=True,exist_ok=True)
subprocess.run([sys.executable,str(Path(__file__).with_name('inventory_level3_finale.py')),'--capture',a.capture[0],'--rom',a.rom,'--out',str(out)],check=True)
for name in ['shared_patterns.json','terrain_aliases.json']:(out/name).unlink()
groups=Counter();examples=defaultdict(list);backgrounds=defaultdict(Counter);form_palettes=Counter()
for folder in a.capture:
 c=Path(folder)
 for f in sorted((c/'ram').glob('*.bin')):
  ram=f.read_bytes()
  if ram[0x72]!=0x18 or ram[0x78:0x7a]!=bytes.fromhex('d9ac'):continue
  pp=(c/'ppu'/f.name).read_bytes();oam=(c/'oam'/f.name).read_bytes();cells=[]
  for offset in range(0,256,4):
   y,t,attr,x=oam[offset:offset+4]
   pal=('FF'+pp[0x3f11+(attr&3)*4:0x3f14+(attr&3)*4].hex()).upper()
   if y<239 and 0x94<=t<=0xaf and (attr&3)==3:
    form_palettes[pal]+=1
    if pal=='FF190927':cells.append([t,x,y,attr])
  if cells:
   flip=bool(cells[0][3]&64);x0=ram[0x4e0]-28;y0=ram[0x4f0]-25
   layout=tuple(sorted((f'{t+0xc00:04X}',48-(x-x0)if flip else x-x0,y-y0)for t,x,y,attr in cells))
   assert all(0<=x<=48 and 0<=y<=16 for t,x,y in layout),layout
   groups[layout]+=1;examples[layout].append(dict(capture=c.name,frame=int(f.stem),mirror=flip))
  # Physical background bank 0D is byte-identical to 0B. Keep its actual
  # replacement identities, rather than the generic first-byte-match result.
  for nt in [0x2000,0x2400,0x2800,0x2c00]:
   for y in range(30):
    for x in range(32):
     t=0xd00+pp[nt+y*32+x];attr=pp[nt+960+y//4*8+x//4]
     pa=attr>>((y%4)//2*4+(x%4)//2*2)&3
     pal=(bytes([pp[0x3f00]])+pp[0x3f01+pa*4:0x3f04+pa*4]).hex().upper()
     backgrounds[pal][f'{t:04X}']+=1
layouts=[dict(name=f'pose_{i}',count=count,examples=examples[layout][:8],layout=layout)for i,(layout,count)in enumerate(groups.most_common())]
(out/'native_dragon_layouts.json').write_text(json.dumps(layouts,indent=2)+'\n')
(out/'arena_backgrounds.json').write_text(json.dumps({p:dict(sorted(ts.items()))for p,ts in backgrounds.items()},indent=2)+'\n')
rom=Path(a.rom).read_bytes();start=16+rom[4]*16384+(512 if rom[6]&4 else 0);chr=rom[start:]
tiles=[chr[i:i+16]for i in range(0,len(chr),16)]
subjects={int(t,16)for layout in layouts for t,x,y in layout['layout']}|{0xcb0,0xcb1,0xcb2,0xcb3,0xcb4,0xc74,0xa95,0xa96,0xa47,0xa48}
aliases={f'{t:04X}':[f'{i:04X}'for i,v in enumerate(tiles)if v==tiles[t]]for t in sorted(subjects)}
patterns=json.loads((out/'native_patterns.json').read_text())
for source,targets in aliases.items():
 for target in targets:patterns[target]=tiles[int(target,16)].hex()
for t in range(256):
 assert tiles[0xb00+t]==tiles[0xd00+t]
 for bank in [0xb00,0xd00]:patterns[f'{bank+t:04X}']=tiles[bank+t].hex()
(out/'native_patterns.json').write_text(json.dumps(patterns,indent=2)+'\n')
(out/'native_aliases.json').write_text(json.dumps(aliases,indent=2)+'\n')
(out/'inventory_summary.json').write_text(json.dumps(dict(captures=[Path(p).name for p in a.capture],complete_pose_layouts=len(layouts),form_palettes=form_palettes,physical_arena_background_bank='0D',body_size=[112,48]),indent=2)+'\n')
print('Dragon layouts:',[(p['name'],p['count'],len(p['layout']))for p in layouts])
