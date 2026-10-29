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
 for d,version in [(before,'0.26.0'),(after,'0.27.0')]:
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
 p.add_argument('--opening',action='store_true');a=p.parse_args();root=Path(__file__).resolve().parents[1];b,c=Path(a.before),Path(a.after)
 frames,data,report=compare(root,b,c);assert frames==list(range(1,(6427 if a.opening else 3393)+1))
 pack=c/'mesen_home/HdPacks/Holy_Diver_(Tr)';art=root/'art/level6_variety'
 styles={'9A8B':'Exterior','9BB7':'Interior','9CA7':'Exterior'}if a.opening else{'9F3B':'Amber_Ossuary','A02B':'Crimson_Shaft','A0DF':'Verdant_Crypt'}
 backgrounds={style:variants(np.array(Image.open(pack/f'Final_Citadel_{style}.png').convert('RGB')))for style in set(styles.values())}
 flashes={}
 if a.opening:
  for style in backgrounds:
   bg=np.array(Image.open(pack/f'Final_Citadel_{style}.png').convert('RGB'))
   for phase,color in [('30',[255,254,255]),('31',[192,223,255])]:
    flashes[style,phase]=variants(((bg.astype(np.uint16)*177>>8)+(np.array(color,dtype=np.uint16)*80>>8)).astype(np.uint8))
 paths={f'{color}_{name}':art/f'{color}_{name}.png'for color,name in [('amber','corridor_body'),('amber','corridor_floor'),('red','shaft_center'),('red','upper_ceiling'),('green','crypt_floor'),('green','crypt_ceiling')]}
 paths.update({f'sentinel_{i}_{pal}':root/f'art/level4_staff/sentinel_{i}_{pal}.png'for i in range(4)for pal in ['FF102030','FF122232']})
 paths.update({f'crawler_{p}':root/f'art/level6_next/crawler_{p}.png'for p in ['rest','leap']})
 if a.opening:
  paths={n:root/f'art/level6_opening/{n}.png'for n in ['cape_menu','skull','brick','cornice']}
  paths.update({f'one_up_{pal}':root/f'art/screen1_4/one_up_{pal}.png'for pal in ['FF300036','FF221136']})
 sources={n:[source(path,m)for m in [False,True]]for n,path in paths.items()};hits={};stats=Counter();roomstats=Counter();bgcounts={};missing=[];changed=[];boundaries=[];same_nonpanorama=[];unchanged_bg=Counter()
 menu_reference=np.array(Image.open(b/'frames'/('002800.png'if a.opening else'001720.png')).convert('RGB'))[106:136,60:480]
 for n in frames:
  fs=[d/'frames'/f'{n:06}.png'for d in [b,c]]
  if not all(f.stat().st_size for f in fs):assert fs[0].stat().st_size==fs[1].stat().st_size;stats['empty_initial']+=1;continue
  old,im=[np.array(Image.open(f).convert('RGB'))for f in fs];different=not np.array_equal(old,im);stats['changed'if different else'identical']+=1
  room=f'{int.from_bytes(data["ram"][n][0x78:0x7a],"little"):04X}';roomstats[room]+=1
  if not old.any():assert not im.any(),(n,'blackout changed');stats['native_black_exact']+=1;continue
  menu=np.array_equal(old[106:136,60:480],menu_reference)
  if menu:assert not different,(n,'menu changed');stats['menus_exact']+=1
  if different:
   changed.append(n);previous=f'{int.from_bytes(data["ram"][n-1][0x78:0x7a],"little"):04X}'if n>1 else room
   assert room in styles or previous in styles,(n,room,previous)
   choices=[styles[r]for r in dict.fromkeys([room,previous])if r in styles];best=0;beststyle=None
   for style in choices:
    for v in backgrounds[style]:
     count=int(np.all(im==v,2).sum())
     if count>best:best,beststyle=count,style
     if best>10000:
      if a.opening:
       mask=np.all(old==v,2);assert mask.sum()>10000,(n,'old background missing');assert np.array_equal(old[mask],im[mask]),(n,'opening background changed');unchanged_bg['normal']+=1
      break
    if best>10000:break
   # In the opening regression the original backdrop itself must stay exact,
   # including the existing native flash blend. Only stone mappings change.
   if a.opening and best<10000:
    found=False
    for style in choices:
     for phase in ['30','31']:
      for v in flashes[style,phase]:
       mask=np.all(old==v,2)
       if mask.sum()>10000:
        assert np.array_equal(old[mask],im[mask]),(n,'flash background changed');unchanged_bg[phase]+=1;found=True;break
      if found:break
     if found:break
    if not found:missing.append([n,room,best])
   elif best<10000:missing.append([n,room,best])
   else:bgcounts.setdefault(beststyle,[]).append(best)
   if room not in styles:boundaries.append(dict(frame=n,rendered_room=previous,ram_room=room))
  if n%4==0 or (not a.opening and n<342):
   for name,ss in sources.items():
    if name in hits:continue
    for mirrored,item in enumerate(ss):
     found=matches(im,item)
     if found:hits[name]=dict(frame=n,mirrored=bool(mirrored),positions=found);break
 report.update(images=stats,rooms=roomstats,backgrounds={k:dict(samples=len(v),minimum_pixels=min(v))for k,v in bgcounts.items()},
  missing_backgrounds=missing,live_whole_source_matches=hits,sources_not_observed_whole=sorted(set(sources)-set(hits)),
  first_changed=min(changed),last_changed=max(changed),outgoing_room_boundaries=boundaries,
  opening_unchanged_background_samples=unchanged_bg,opening_flash_or_nonpanorama_frames=same_nonpanorama,live_new_room_spell_flash_coverage=False)
 Path(a.out).write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps({k:v for k,v in report.items()if k not in ['live_whole_source_matches','opening_flash_or_nonpanorama_frames']},indent=2));print('Whole sources:',sorted(hits));assert not missing,missing[:20]
 if a.opening:assert all(n in hits for n in ['cape_menu','skull','brick','cornice','one_up_FF300036','one_up_FF221136'])
 else:assert all(n in hits for n in ['amber_corridor_body','red_shaft_center','green_crypt_floor','crawler_rest','crawler_leap'])
if __name__=='__main__':main()
