"""Validate controller-derived left stop and no-jump ledge walk-off."""
import argparse,hashlib,json,wave
from pathlib import Path
p=argparse.ArgumentParser()
for k in ['left-before','left-after','ledge-before','ledge-after','out']:p.add_argument('--'+k,required=True)
a=p.parse_args();root=Path(__file__).resolve().parents[1];report={}
for name,b,c in [('entrance_left_stop',a.left_before,a.left_after),('raised_ledge_slow_walkoff',a.ledge_before,a.ledge_after)]:
 b,c=Path(b),Path(c);bi=json.loads((b/'result.json').read_text());ci=json.loads((c/'result.json').read_text())
 assert bi['movie_completed']and ci['movie_completed']and bi['movie_sha256']==ci['movie_sha256']
 assert bi['core_sha256']==ci['core_sha256']and bi['rom_sha1']==ci['rom_sha1']
 frames=sorted(f.stem for f in(c/'ram').glob('*.bin'));assert len(frames)==ci['movie_frames']//2
 for kind in ['ram','ppu','oam','view']:
  for n in frames:
   f=n+('.json'if kind=='view'else'.bin');assert(b/kind/f).read_bytes()==(c/kind/f).read_bytes(),(name,kind,n)
 apu=(b/'apu.tsv').read_bytes();assert apu==(c/'apu.tsv').read_bytes()
 with wave.open(str(b/'full.wav'),'rb')as f:bp=f.readframes(f.getnframes());params=f.getparams()
 with wave.open(str(c/'full.wav'),'rb')as f:assert f.getparams()==params;cp=f.readframes(f.getnframes())
 assert bp==cp
 positions={int(n):[int.from_bytes((c/'ram'/f'{n}.bin').read_bytes()[i:i+2],'little')for i in [0x74,0x76]]for n in frames}
 if name=='entrance_left_stop':
  window=range(42,83,2);assert all(positions[n]==[23,176]for n in window)
  detail=dict(held_left_frames=90,stationary_window=[42,82],world_position=[23,176])
 else:
  window=range(744,785,2);ps=[positions[n]for n in window]
  assert ps[0]==[448,112]and ps[-1]==[480,128]
  assert all(q[0]>=p[0]and q[1]>=p[1]for p,q in zip(ps,ps[1:]))
  detail=dict(no_jump_input_after_frame=640,checked_window=[744,784],positions=[[n,*positions[n]]for n in window])
 expected=json.loads((root/'evidence/0.11.0-pack-sha256.json').read_text());assert json.loads((c/'installed_pack.json').read_text())==expected
 report[name]=dict(movie_sha256=ci['movie_sha256'],movie_frames=ci['movie_frames'],paired_native_samples=len(frames),identical_pcm_bytes=len(bp),pcm_sha256=hashlib.sha256(bp).hexdigest(),apu_write_count=len(apu.splitlines()),apu_sha256=hashlib.sha256(apu).hexdigest(),controller_only=True,ram_writes=False,trajectory=detail)
Path(a.out).write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
