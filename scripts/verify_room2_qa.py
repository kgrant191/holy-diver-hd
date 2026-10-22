"""Compare v12 and v13 native replays; render changes must not change gameplay."""
from pathlib import Path
import argparse,json,hashlib,wave
from PIL import Image
p=argparse.ArgumentParser();p.add_argument('--work',required=True);p.add_argument('--out',required=True);a=p.parse_args();work=Path(a.work);results={}
def same_pixels(x,y):return Image.open(x).tobytes()==Image.open(y).tobytes()
for i in range(1,5):
 before=work/'before'/f'state{i}';after=work/'after'/f'state{i}'
 assert (after/'completed.txt').read_text()=='360'
 r={'frames':360,'snapshots_per_memory_type':180}
 for ext in ['ram','ppu','oam']:
  paths=sorted((before/'dumps').glob('*.'+ext));assert len(paths)==180
  r[ext+'_mismatches']=sum(p.read_bytes()!=(after/'dumps'/p.name).read_bytes()for p in paths);assert r[ext+'_mismatches']==0
 for f in ['apu.tsv','commands.tsv']:r[f+'_equal']=(before/f).read_bytes()==(after/f).read_bytes();assert r[f+'_equal']
 r['pause_frames_equal']=all(same_pixels(before/f'frames/{n:04}.png',after/f'frames/{n:04}.png')for n in range(280,302,2));assert r['pause_frames_equal']
 with wave.open(str(before/'full.wav'))as w:x=w.readframes(w.getnframes())
 with wave.open(str(after/'full.wav'))as w:y=w.readframes(w.getnframes())
 r['pcm_full_equal']=x==y;r['pcm_common_prefix_equal']=x[:min(len(x),len(y))]==y[:min(len(x),len(y))];r['pcm_byte_lengths']=[len(x),len(y)]
 results[f'state{i}']=r
for kind in ['title','entrance']:
 before=work/f'regression_before_{kind}';after=work/f'regression_after_{kind}';r={}
 for ext in ['ram','oam']:
  paths=sorted((before/'dumps').glob('*.'+ext));r[ext+'_snapshots']=len(paths);r[ext+'_mismatches']=sum(p.read_bytes()!=(after/'dumps'/p.name).read_bytes()for p in paths);assert r[ext+'_mismatches']==0
 for f in ['apu.tsv','commands.tsv']:r[f+'_equal']=(before/f).read_bytes()==(after/f).read_bytes();assert r[f+'_equal']
 paths=sorted((before/'frames').glob('*.png'));diff=[int(p.stem)for p in paths if not same_pixels(p,after/'frames'/p.name)];r['screenshots']=len(paths);r['changed_screenshots']=len(diff);r['first_changed_frame']=min(diff)if diff else None
 if kind=='title':assert not diff
 else:assert diff and min(diff)>=500
 results[kind]=r
root=Path(__file__).resolve().parents[1];baseline=root/'rollback/entrance_v12';pack=root/'build/Holy_Diver_(Tr)'
old=list(baseline.glob('*.png'));assert all(p.read_bytes()==(pack/p.name).read_bytes()for p in old)
patch=(pack/'Entrance_SFX_Priority.ips').read_bytes();assert patch==(baseline/'Entrance_SFX_Priority.ips').read_bytes()
results['integrity']={'approved_v12_pngs_unchanged':len(old),'audio_patch_unchanged':True,'audio_patch_sha256':hashlib.sha256(patch).hexdigest(),'room2_frame_total':1440,'room2_snapshots_per_memory_type':720}
Path(a.out).parent.mkdir(parents=True,exist_ok=True);Path(a.out).write_text(json.dumps(results,indent=2)+'\n');print(json.dumps(results,indent=2))
