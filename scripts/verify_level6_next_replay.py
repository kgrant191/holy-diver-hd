"""Compare actual native execution and inspect the complete new-screen replay."""
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
 note_differences=[]
 for d,version in [(before,'0.25.1'),(after,'0.26.0')]:
  actual=json.loads((d/'installed_pack.json').read_text());expected=json.loads((root/f'evidence/{version}-pack-sha256.json').read_text())
  differences=[k for k in expected if expected[k]!=actual.get(k)];assert set(actual)==set(expected)
  if d==after and differences:
   # Only the noun in the install note changed after this full capture.
   assert differences==['README.txt']
   note=root/'evidence/level6_next/capture_README.txt';assert hashlib.sha256(note.read_bytes()).hexdigest()==actual['README.txt']
   assert note.read_text().replace('HUD, ghouls,','HUD, flying skulls,')==(root/'INSTALL.txt').read_text()
   note_differences=differences
  else:assert not differences
 frames=sorted(int(p.stem)for p in(after/'ram').glob('*.bin'));data={k:{}for k in ['ram','ppu','oam','view']}
 for n in frames:
  for kind in data:
   name=f'{n:06}'+('.json'if kind=='view'else'.bin');raw=(after/kind/name).read_bytes()
   assert raw==(before/kind/name).read_bytes(),(n,kind);data[kind][n]=json.loads(raw)if kind=='view'else raw
 apu=(after/'apu.tsv').read_bytes();assert apu==(before/'apu.tsv').read_bytes()
 with wave.open(str(before/'full.wav'))as f:params=f.getparams();pcm=f.readframes(f.getnframes())
 with wave.open(str(after/'full.wav'))as f:assert f.getparams()==params and f.readframes(f.getnframes())==pcm
 return frames,data,dict(movie=infos[1],native_samples_per_type=len(frames),native_exact=True,apu_exact=True,pcm_exact=True,
  apu_sha256=hashlib.sha256(apu).hexdigest(),pcm_sha256=hashlib.sha256(pcm).hexdigest(),delivered_runtime_exact=True,install_note_only_differences=note_differences)

def main():
 p=argparse.ArgumentParser()
 for k in ['before','after','out']:p.add_argument('--'+k,required=True)
 p.add_argument('--regression',action='store_true');a=p.parse_args();root=Path(__file__).resolve().parents[1];b,c=Path(a.before),Path(a.after)
 frames,data,report=compare(root,b,c);pack=c/'mesen_home/HdPacks/Holy_Diver_(Tr)';art=root/'art/level6_next'
 bg=variants(np.array(Image.open(pack/'Final_Citadel_Interior.png').convert('RGB')))
 paths={n:art/(n+'.png')for n in ['corridor_body','corridor_inset','corridor_ceiling','corridor_corner','corridor_floor','entry_base','crawler_rest','crawler_leap']}
 paths.update({f'sentinel_{i}':root/f'art/level4_staff/sentinel_{i}_FF102030.png'for i in range(4)})
 paths['skull']=root/'art/level6_opening/skull.png'
 paths.update({f'flying_skull_{i}':root/f'art/screen1_3/blue_skull_pose_{i}.png'for i in range(2)})
 sources={n:[source(path,m)for m in [False,True]]for n,path in paths.items()};hits={};stats=Counter();roomstats=Counter();counts=[];missing=[];changed=[];boundary=[]
 menu_reference=np.array(Image.open(b/'frames/002400.png').convert('RGB'))[106:136,60:480]if not a.regression else None
 for n in frames:
  fs=[d/'frames'/f'{n:06}.png'for d in [b,c]]
  if not all(f.stat().st_size for f in fs):assert fs[0].stat().st_size==fs[1].stat().st_size;stats['empty_initial']+=1;continue
  old,im=[np.array(Image.open(f).convert('RGB'))for f in fs];different=not np.array_equal(old,im);stats['changed'if different else'identical']+=1
  room=f'{int.from_bytes(data["ram"][n][0x78:0x7a],"little"):04X}';roomstats[room]+=1
  if a.regression:assert not different,(n,'earlier movie changed');continue
  if not old.any():assert not im.any(),(n,'blackout changed');stats['native_black_exact']+=1;continue
  if np.array_equal(old[106:136,60:480],menu_reference):assert not different,(n,'menu changed');stats['menus_exact']+=1;continue
  if different:
   changed.append(n)
   previous=f'{int.from_bytes(data["ram"][n-1][0x78:0x7a],"little"):04X}'if n>1 else room
   assert room in ['9F3B','A02B']or previous in ['9F3B','A02B'],(n,room,previous)
   if room not in ['9F3B','A02B']:boundary.append(dict(frame=n,rendered_room=previous,ram_room=room))
   best=max(int(np.all(im==v,2).sum())for v in bg[:1])
   if best<10000:best=max(int(np.all(im==v,2).sum())for v in bg)
   if best<10000:missing.append([n,room,best])
   else:counts.append(best)
  if n%4==0 or n>=2048:
   for name,ss in sources.items():
    if name in hits:continue
    for mirrored,item in enumerate(ss):
     found=matches(im,item)
     if found:hits[name]=dict(frame=n,mirrored=bool(mirrored),positions=found);break
 report.update(images=stats,rooms=roomstats,backgrounds=dict(samples=len(counts),minimum_pixels=min(counts)if counts else None),
  missing_backgrounds=missing,live_whole_source_matches=hits,sources_not_observed_whole=sorted(set(sources)-set(hits)),
  first_changed=min(changed)if changed else None,last_changed=max(changed)if changed else None,outgoing_room_boundaries=boundary,
  live_new_room_spell_flash_coverage=False)
 Path(a.out).write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps({k:v for k,v in report.items()if k!='live_whole_source_matches'},indent=2));print('Whole sources:',sorted(hits))
 assert not missing,missing[:20]
 if not a.regression:
  assert frames==list(range(1,2529))
  assert all(k in hits for k in ['corridor_body','corridor_floor','skull','sentinel_0','sentinel_1','sentinel_2','sentinel_3','crawler_rest','crawler_leap']),hits.keys()
if __name__=='__main__':main()
