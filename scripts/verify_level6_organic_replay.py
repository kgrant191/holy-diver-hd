"""Pair native execution and verify room-specific artwork in actual Mesen frames."""
from pathlib import Path
from collections import Counter
import argparse,json,hashlib,wave
import numpy as np
from PIL import Image
from verify_level6_opening_replay import source,matches,variants

def compare(root,before,after):
 infos=[json.loads((d/'result.json').read_text())for d in [before,after]]
 for k in ['movie_sha256','rom_sha1','core_sha256','movie_frames','captured_frames','stride']:assert infos[0][k]==infos[1][k],k
 assert all(i['movie_completed']for i in infos)
 for d,version in [(before,'0.28.0'),(after,'0.29.0')]:
  assert json.loads((d/'installed_pack.json').read_text())==json.loads((root/f'evidence/{version}-pack-sha256.json').read_text())
 frames=sorted(int(p.stem)for p in(after/'ram').glob('*.bin'));data={k:{}for k in ['ram','ppu','oam','view']}
 for n in frames:
  for kind in data:
   name=f'{n:06}'+('.json'if kind=='view'else'.bin');raw=(after/kind/name).read_bytes()
   assert raw==(before/kind/name).read_bytes(),(n,kind);data[kind][n]=json.loads(raw)if kind=='view'else raw
 apu=(after/'apu.tsv').read_bytes();assert apu==(before/'apu.tsv').read_bytes()
 with wave.open(str(before/'full.wav'))as f:params=f.getparams();pcm=f.readframes(f.getnframes())
 with wave.open(str(after/'full.wav'))as f:assert f.getparams()==params and f.readframes(f.getnframes())==pcm
 return frames,data,dict(movie=infos[1],native_samples_per_type=len(frames),native_exact=True,apu_exact=True,pcm_exact=True,
  apu_sha256=hashlib.sha256(apu).hexdigest(),pcm_sha256=hashlib.sha256(pcm).hexdigest(),delivered_runtime_exact=True)
def main():
 p=argparse.ArgumentParser()
 for k in ['before','after','out']:p.add_argument('--'+k,required=True)
 p.add_argument('--regression',action='store_true');a=p.parse_args();root=Path(__file__).resolve().parents[1];b,c=Path(a.before),Path(a.after)
 frames,data,report=compare(root,b,c);assert frames==list(range(1,(7648 if a.regression else 4761)+1))
 pack=c/'mesen_home/HdPacks/Holy_Diver_(Tr)';bg=variants(np.array(Image.open(pack/'Final_Citadel_Organic.png').convert('RGB')))
 paths={n:root/f'art/level6_organic/{n}.png'for n in ['body','ceiling','platform_top','wall_face','orb_0','orb_1']}
 sources={n:[source(path,m)for m in [False,True]]for n,path in paths.items()};hits={};stats=Counter();roomstats=Counter();bgcounts=[];missing=[];changed=[];boundaries=[]
 menu_reference=np.array(Image.open(b/'frames'/'000010.png').convert('RGB'))[106:136,60:480]
 for n in frames:
  fs=[d/'frames'/f'{n:06}.png'for d in [b,c]]
  if not all(f.stat().st_size for f in fs):assert fs[0].stat().st_size==fs[1].stat().st_size;stats['empty_initial']+=1;continue
  old,im=[np.array(Image.open(f).convert('RGB'))for f in fs];different=not np.array_equal(old,im);stats['changed'if different else'identical']+=1
  room=f'{int.from_bytes(data["ram"][n][0x78:0x7a],"little"):04X}';roomstats[room]+=1
  if a.regression:assert not different,(n,'earlier accepted image changed');continue
  if not old.any():assert not im.any(),(n,'blackout changed');stats['native_black_exact']+=1;continue
  if np.array_equal(old[106:136,60:480],menu_reference):assert not different,(n,'menu changed');stats['menus_exact']+=1
  previous=f'{int.from_bytes(data["ram"][n-1][0x78:0x7a],"little"):04X}'if n>1 else room
  if different:
   changed.append(n);assert room=='A3AF'or previous=='A3AF',(n,room,previous)
   best=0
   for v in bg:
    best=max(best,int(np.all(im==v,2).sum()))
    if best>=8000:break
   if best<8000:missing.append([n,room,best])
   else:bgcounts.append(best)
   if room!='A3AF':boundaries.append(dict(frame=n,rendered_room=previous,ram_room=room))
  if n%2==0 and (room=='A3AF'or previous=='A3AF'):
   for name,ss in sources.items():
    if name in hits:continue
    for mirror,item in enumerate(ss):
     found=matches(im,item)
     if found:hits[name]=dict(frame=n,mirrored=bool(mirror),positions=found);break
 report.update(images=stats,rooms=roomstats,background=dict(samples=len(bgcounts),minimum_pixels=min(bgcounts)if bgcounts else None),missing_backgrounds=missing,live_whole_source_matches=hits,sources_not_observed_whole=sorted(set(sources)-set(hits)),first_changed=min(changed)if changed else None,last_changed=max(changed)if changed else None,outgoing_room_boundaries=boundaries,regression=a.regression,live_Thunder_or_dragon_flash_coverage=False)
 Path(a.out).write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:v for k,v in report.items()if k!='live_whole_source_matches'},indent=2));print('Whole sources:',sorted(hits));assert not missing,missing[:10]
 if not a.regression:assert set(hits)==set(sources),set(sources)-set(hits)
if __name__=='__main__':main()
