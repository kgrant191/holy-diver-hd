"""Inventory actual visible finale tiles, palettes, banks and native actor layouts."""
from pathlib import Path
from collections import Counter, defaultdict
import argparse, json, hashlib
import numpy as np

p=argparse.ArgumentParser()
for key in ['capture','rom','out']:p.add_argument('--'+key,required=True)
a=p.parse_args();capture=Path(a.capture);out=Path(a.out);out.mkdir(parents=True,exist_ok=True)
rom=Path(a.rom).read_bytes();ch=rom[16+rom[4]*16384+(512 if rom[6]&4 else 0):]
bank_cache={};rooms=defaultdict(list);modes=defaultdict(Counter);banks=defaultdict(Counter);phases=defaultdict(Counter);visible=defaultdict(lambda:defaultdict(Counter));sprites=defaultdict(Counter);examples={};guards=defaultdict(set);layouts={};observed_tiles=set()
for f in sorted((capture/'ram').glob('*.bin')):
 n=int(f.stem);r=f.read_bytes();room=f'{int.from_bytes(r[0x78:0x7a],"little"):04X}';rooms[room].append(n);modes[room][r[0x72]]+=1
 pp=(capture/'ppu'/f.name).read_bytes();o=(capture/'oam'/f.name).read_bytes();bases=[]
 for offset in [0,4096]:
  raw=pp[offset:offset+4096]
  if raw not in bank_cache:
   matches=[j//16 for j in range(0,len(ch)-4095,4096)if ch[j:j+4096]==raw];assert matches,(n,offset);bank_cache[raw]=matches
  bases.append(bank_cache[raw])
 sb,bb=bases[0][0],bases[1][0];banks[room][(sb,bb)]+=1;phases[room][(r[0x72],pp[0x3f00:0x3f20].hex().upper())]+=1
 v=json.loads((capture/'view'/f'{n:06}.json').read_text());vv=v['vram'];sx=(vv&31)*8+v['xscroll']+(256 if vv&0x400 else 0);sy=((vv>>5)&31)*8+((vv>>12)&7)+(240 if vv&0x800 else 0)
 if room not in ['FFFF','0000']:
  # All visible cells, including the extra row/column exposed by fine scroll.
  xx,yy=np.meshgrid(np.arange(sx//8,(sx+255)//8+1),np.arange(sy//8,(sy+239)//8+1));tx,ty=xx%32,yy%30;nt=0x2000+(xx//32%2)*0x400+(yy//30%2)*0x800;mem=np.frombuffer(pp,dtype=np.uint8)
  ts=bb+mem[nt+ty*32+tx].astype(np.int32);attrs=mem[nt+960+ty//4*8+tx//4];pa=(attrs>>((ty%4)//2*4+(tx%4)//2*2))&3
  for palidx in range(4):
   pal=(bytes([pp[0x3f00]])+pp[0x3f01+4*palidx:0x3f04+4*palidx]).hex().upper();keys,counts=np.unique(ts[pa==palidx],return_counts=True)
   for key,count in zip(keys,counts):visible[room][pal][f'{key:04X}']+=int(count);observed_tiles.add(int(key))
  x,y=(sx+128)//8,(sy+16)//8;tx,ty=x%32,y%30;nt=0x2000+x//32%2*0x400+y//30%2*0x800;t=bb+pp[nt+ty*32+tx];palidx=(pp[nt+960+ty//4*8+tx//4]>>((ty%4)//2*4+(tx%4)//2*2))&3;pal=(bytes([pp[0x3f00]])+pp[0x3f01+4*palidx:0x3f04+4*palidx]).hex().upper();guards[room].add((f'{t:04X}',pal))
 actor=[]
 for i in range(0,256,4):
  y,t,at,x=o[i:i+4]
  if y>=239:continue
  key=f'{sb+t:04X}';pal='FF'+pp[0x3f11+4*(at&3):0x3f14+4*(at&3)].hex().upper();identity=(key,pal,at&0xe0);sprites[room][identity]+=1;examples.setdefault((room,*identity),n);observed_tiles.add(sb+t)
  if t>=0x75:actor.append([key,pal,x,y+1,at])
 if sb>=0x1400 and room not in ['FFFF','0000']:layouts[str(n)]=actor
report=dict(rooms={room:dict(first=min(fs),last=max(fs),samples=len(fs),modes={f'{k:02X}':v for k,v in modes[room].items()},banks=[dict(sprite=f'{s:04X}',background=f'{b:04X}',samples=count)for(s,b),count in banks[room].items()])for room,fs in rooms.items()},visible_backgrounds={room:{pal:dict(sorted(ts.items()))for pal,ts in pals.items()}for room,pals in visible.items()},view_guards={room:sorted(gs)for room,gs in guards.items()},sprites={room:[dict(tile=t,palette=pal,attributes=at,count=count,example=examples[room,t,pal,at])for(t,pal,at),count in sorted(xs.items())]for room,xs in sprites.items()},palette_phases={room:[dict(mode=f'{m:02X}',palettes=pal,samples=count)for(m,pal),count in xs.items()]for room,xs in phases.items()},movie=json.loads((capture/'result.json').read_text())if(capture/'result.json').exists()else None)
(out/'inventory.json').write_text(json.dumps(report,indent=2)+'\n');(out/'actor_layouts.json').write_text(json.dumps(layouts,separators=(',',':'))+'\n')
patterns={f'{i:04X}':ch[i*16:i*16+16].hex()for i in range(len(ch)//16)};(out/'native_patterns.json').write_text(json.dumps(patterns,indent=2)+'\n')
bybytes=defaultdict(list)
for tile,raw in patterns.items():bybytes[raw].append(tile)
aliases={f'{t:04X}':bybytes[patterns[f'{t:04X}']]for t in sorted(observed_tiles)};(out/'native_aliases.json').write_text(json.dumps(aliases,indent=2)+'\n')
print(json.dumps(report['rooms'],indent=2))
