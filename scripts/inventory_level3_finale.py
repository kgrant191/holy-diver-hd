"""Extract recorded identities and exact CHR alias tables for reproducible builds."""
from pathlib import Path
from collections import Counter,defaultdict
import json,hashlib,argparse
p=argparse.ArgumentParser()
for key in ['capture','rom','out']:p.add_argument('--'+key,required=True)
a=p.parse_args();c=Path(a.capture);art=Path(a.out);art.mkdir(parents=True,exist_ok=True)
rom=Path(a.rom).read_bytes();start=16+rom[4]*16384+(512 if rom[6]&4 else 0);chr=rom[start:];print('CHR',len(chr))
observed=defaultdict(lambda:defaultdict(set));sprites=defaultdict(Counter);patterns={};banks=defaultdict(Counter);phases=defaultdict(Counter);bgexamples={};sprite_examples={};roomframes=defaultdict(list);boss_oams={}
for f in sorted((c/'ram').glob('*.bin')):
 n=int(f.stem);ram=f.read_bytes();room=f'{int.from_bytes(ram[0x78:0x7a],"little"):04X}';roomframes[room].append(n)
 if room=='FFFF':continue
 pp=(c/'ppu'/f.name).read_bytes();o=(c/'oam'/f.name).read_bytes();bases=[chr.find(pp[a:a+4096])//16 for a in [0,4096]];assert min(bases)>=0,(n,bases);banks[room][tuple(bases)]+=1
 for base,offset in zip(bases,[0,4096]):
  for t in range(256):patterns[f'{base+t:04X}']=pp[offset+t*16:offset+(t+1)*16].hex()
 for nt in [0x2000,0x2400,0x2800,0x2c00]:
  for y in range(30):
   for x in range(32):
    t=bases[1]+pp[nt+y*32+x];attr=pp[nt+960+y//4*8+x//4];pa=(attr>>((y%4)//2*4+(x%4)//2*2))&3;pal=bytes([pp[0x3f00]])+pp[0x3f01+pa*4:0x3f04+pa*4];pal=pal.hex().upper();observed[room][pal].add(t);bgexamples.setdefault((room,t,pal),n)
 for i in range(0,256,4):
  y,t,at,x=o[i:i+4]
  if y>=239:continue
  pal=('FF'+pp[0x3f11+(at&3)*4:0x3f14+(at&3)*4].hex()).upper();key=(bases[0]+t,pal,at&0xc0);sprites[room][key]+=1;sprite_examples.setdefault((room,*key),n)
 if room=='9F92':
  boss=[list(o[i:i+4])for i in range(0,256,4)if o[i]<239 and o[i+1]>=0x75]
  if boss:boss_oams[str(n)]=boss
 phases[room][(ram[0x72],pp[0x3f00:0x3f20].hex())]+=1
inv=dict(rooms={room:dict(first=min(fs),last=max(fs),samples=len(fs),banks=[dict(sprite_base=f'{a:04X}',background_base=f'{b:04X}',count=v)for(a,b),v in banks[room].items()])for room,fs in roomframes.items()},sprites={room:[dict(tile=f'{t:04X}',palette=pal,flip=flip,count=v,example=sprite_examples[room,t,pal,flip])for(t,pal,flip),v in sorted(ts.items())]for room,ts in sprites.items()},palette_phases={room:[dict(mode=m,palettes=pa,count=v)for(m,pa),v in ts.items()]for room,ts in phases.items()})
(art/'native_inventory.json').write_text(json.dumps(inv,indent=2)+'\n');(art/'native_patterns.json').write_text(json.dumps(patterns,indent=2)+'\n');(art/'observed_backgrounds.json').write_text(json.dumps({r:{p:[f'{t:04X}'for t in sorted(ts)]for p,ts in pals.items()}for r,pals in observed.items()},indent=2)+'\n');print(json.dumps(inv['rooms'],indent=2))

# Prove bank aliases directly from the supplied original CHR bytes.
alltiles=[chr[i:i+16]for i in range(0,len(chr),16)]
shared={f'{t:04X}':[f'{j:04X}'for j,b in enumerate(alltiles)if b==alltiles[t]]for t in [*range(0x800,0x88f),*range(0xa00,0xa75)]}
terrain={f'{t:04X}':[f'{j:04X}'for j in range(0x700,0x800)if alltiles[j]==alltiles[t]]for t in range(0x900,0x9a0)}
terrain={k:v for k,v in terrain.items()if v}
for name,data in [('shared_patterns.json',shared),('terrain_aliases.json',terrain)]:
 (art/name).write_text(json.dumps(data,indent=2)+'\n')
