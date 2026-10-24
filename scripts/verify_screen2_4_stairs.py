"""Verify the stair repair against 0.7.0, including unchanged next-room arrival."""
from pathlib import Path
import argparse,hashlib,json,re
from collections import Counter
import numpy as np
from PIL import Image
p=argparse.ArgumentParser()
for k in ['before','after','out']:p.add_argument('--'+k,required=True)
a=p.parse_args();root=Path(__file__).resolve().parents[1]
old=json.loads((root/'evidence/0.7.0-pack-sha256.json').read_text());new=json.loads((root/'evidence/0.7.1-pack-sha256.json').read_text())
assert set(old)==set(new)
assert sorted(k for k in old if old[k]!=new[k])==['README.txt','Stage2_Second_Cave_Tiles_2x.png','hires.txt']
routes=json.loads((root/'scripts/screen2_4_stairs_routes.json').read_text())
report=dict(baseline='0.7.0',candidate='0.7.1',cases={},controller_only=True,ram_writes=False)
seen=Counter()
for case,route in routes.items():
 b,c=Path(a.before)/case,Path(a.after)/case;frames=route['frames']
 assert (b/'completed.txt').read_text()==(c/'completed.txt').read_text()==str(frames)
 assert (b/'input.json').read_bytes()==(c/'input.json').read_bytes()
 for folder,expected in [(b,old),(c,new)]:
  for n in ['installed_pack_sha256.json','installed_pack_after_sha256.json']:assert json.loads((folder/n).read_text())==expected
 for ext in ['ram','ppu','oam']:
  fs=list((b/'dumps').glob('*.'+ext));assert len(fs)==frames//2
  for f in fs:assert f.read_bytes()==(c/'dumps'/f.name).read_bytes(),(case,f.name)
 assert (b/'apu.tsv').read_bytes()==(c/'apu.tsv').read_bytes()
 bp,cp=(b/'full.wav').read_bytes()[44:],(c/'full.wav').read_bytes()[44:];common=min(len(bp),len(cp));tail=abs(len(bp)-len(cp))
 assert common and bp[:common]==cp[:common] and tail<=3200
 changed=exact=outside=black=0
 for n in range(2,frames+1,2):
  before=np.array(Image.open(b/f'frames/{n:04}.png').convert('RGB'));after=np.array(Image.open(c/f'frames/{n:04}.png').convert('RGB'))
  diff=np.any(before!=after,axis=2);allowed=np.zeros((480,512),dtype=bool)
  for j in [max(2,n-2),n,min(frames,n+2)]:
   ram=(c/f'dumps/{j:04}.ram').read_bytes();ppu=(c/f'dumps/{j:04}.ppu').read_bytes()
   if ram[0x78:0x7a]!=bytes.fromhex('ad8c'):continue
   sc=int.from_bytes(ram[0x60:0x62],'little')
   # The game's RAM camera resets before the displayed nametable on return.
   # PPU temporary address retains the actual visible page.
   state_ns={max(20,(j//20)*20),min(frames,((j+19)//20)*20)}
   pages=set()
   for state_n in state_ns:
    state=(c/f'dumps/{state_n:04}.state').read_text()
    tmp=int(re.search(r'^ppu.tmpVideoRamAddr=(\d+)$',state,re.M).group(1))
    pages.add((tmp>>10)&1)
   offsets={sc%256+page*256 for page in pages}
   for page in [0,1]:
    base=0x2000+page*0x400
    for ty in range(30):
     for tx in range(32):
      t=ppu[base+ty*32+tx]
      if not 0x75<=t<=0x80:continue
      seen[f'{t+0x300:04X}']+=1
      for offset in offsets:
       x=(page*256+tx*8-offset)%512
       if x<256:allowed[ty*16:ty*16+16,x*2:min(512,x*2+16)]=True
  assert not np.any(diff&~allowed),(case,n,'changed outside native stair cells')
  changed+=bool(diff.any());exact+=not diff.any()
  ram=(c/f'dumps/{n:04}.ram').read_bytes()
  if ram[0x78:0x7a]==bytes.fromhex('9d8d') and n>100:
   assert not diff.any(),(case,n,'next room changed');outside+=1
  if before.max()==0:assert after.max()==0;black+=1
 report['cases'][case]=dict(frames=frames,identical_samples_per_memory_type=frames//2,identical_pcm_bytes=common,shutdown_tail_bytes=tail,changed_images=changed,exact_images=exact,unchanged_next_room_images=outside,exact_black_images=black)
assert set(seen)=={f'{i:04X}' for i in range(0x375,0x381)}
report.update(total_frames_per_build=sum(v['frames'] for v in routes.values()),native_stair_identities=dict(seen),unchanged_pack_files=83)
out=Path(a.out);out.parent.mkdir(parents=True,exist_ok=True);out.write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
