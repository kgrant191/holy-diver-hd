from pathlib import Path
import argparse,json,wave
p=argparse.ArgumentParser();p.add_argument('--work',required=True);p.add_argument('--v15-motion',required=True);p.add_argument('--out',required=True);a=p.parse_args();w=Path(a.work);m=Path(a.v15_motion);result={}
cases=[('arms_normal',w/'before/normal',w/'after/normal',480),('arms_twin',w/'before/twin',w/'after/twin',480),('room2_enemy',m/'enemy',w/'room2/enemy',360),('room2_death',m/'normal',w/'room2/normal',720)]
for name,b,c,end in cases:
 r={};assert(b/'completed.txt').read_text()==(c/'completed.txt').read_text()==str(end)
 for ext in ['ram','ppu','oam']:
  files=sorted((b/'dumps').glob('*.'+ext));assert all(f.read_bytes()==(c/'dumps'/f.name).read_bytes()for f in files),(name,ext);r[ext+'_identical_frames']=len(files)
 for f in ['apu.tsv','commands.tsv']:assert(b/f).read_bytes()==(c/f).read_bytes(),(name,f);r[f+'_identical']=True
 with wave.open(str(b/'full.wav'),'rb')as f:aa=f.readframes(f.getnframes())
 with wave.open(str(c/'full.wav'),'rb')as f:ab=f.readframes(f.getnframes())
 n=min(len(aa),len(ab));assert aa[:n]==ab[:n],name;r['pcm_identical_bytes']=n
 r['changed_render_frames']=sum(f.read_bytes()!=(c/'frames'/f.name).read_bytes()for f in(b/'frames').glob('*.png'))
 if name.startswith('arms'):
  for f in [312,340,400]:assert(b/f'frames/{f:04}.png').read_bytes()==(c/f'frames/{f:04}.png').read_bytes(),(name,f)
  for f in [20,50,90,104,166,190,230,244]:assert(b/f'frames/{f:04}.png').read_bytes()!=(c/f'frames/{f:04}.png').read_bytes(),(name,f)
  r['observed_repaired_poses']=['idle right','cast right','airborne idle right','airborne cast right','idle left','cast left','airborne idle left','airborne cast left'];r['unchanged_run_and_upward_samples']=[312,340,400]
 if name=='room2_death':
  for f in [78,82,280]:assert(b/f'frames/{f:04}.png').read_bytes()==(c/f'frames/{f:04}.png').read_bytes(),(name,f)
  assert(b/'frames/0077.png').read_bytes()!=(c/'frames/0077.png').read_bytes();r['repaired_death_frozen_hero_frame']=77;r['unchanged_explosion_and_lives_samples']=[78,82,280]
 result[name]=r
o=Path(a.out);o.parent.mkdir(parents=True,exist_ok=True);o.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
