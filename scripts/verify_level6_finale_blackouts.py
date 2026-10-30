"""Verify the final, narrowly scoped blackout repair against the full capture."""
from pathlib import Path
import argparse,json,hashlib,re,wave
import numpy as np
from PIL import Image

def verify(root,full,repair):
 old=json.loads((root/'evidence/level6_finale/pre_blackout_fix-pack-sha256.json').read_text());new=json.loads((root/'evidence/0.30.0-pack-sha256.json').read_text())
 assert json.loads((full/'installed_pack.json').read_text())==old
 assert json.loads((repair/'installed_pack.json').read_text())==new
 assert set(old)==set(new)and [n for n in old if old[n]!=new[n]]==['hires.txt']
 packs=[d/'mesen_home/HdPacks/Holy_Diver_(Tr)'for d in [full,repair]];a,b=[(p/'hires.txt').read_text()for p in packs]
 removed=[l for l in a.splitlines()if l.startswith('[finaleB01CMode&finaleB01CLo&finaleB01CHi]<tile>69,')and ',FF0F0F07,'in l]
 assert len(removed)==31
 for l in removed:
  f=l.split('<tile>')[1].split(',');assert 0x1ecd<=int(f[1],16)<=0x1eeb and float(f[5])==.12
  a=a.replace(l+'\n','')
 normalized=[];new_conditions=[];guarded=0
 for l in b.splitlines():
  if l.startswith('<condition>finaleDetachedRendered'):
   assert l in ['<condition>finaleDetachedRendered1D00,tileAtPosition,128,16,1D00,0F061628,Y','<condition>finaleDetachedRendered1DC7,tileAtPosition,128,16,1DC7,0F061628,Y'];new_conditions.append(l);continue
  if '&finaleDetachedRendered'in l:
   assert l.startswith('[finaleA58FMode&finaleA58FLo&finaleA58FHi&')and '<background>Final_Citadel_Last_Void'in l
   l=re.sub(r'&finaleDetachedRendered1D(?:00|C7)','',l);guarded+=1
   if normalized and normalized[-1]==l:continue
  normalized.append(l)
 assert len(new_conditions)==2 and guarded==240
 assert '\n'.join(normalized)+'\n'==a
 info=json.loads((repair/'result.json').read_text());assert info['movie_completed']and info['movie_frames']==19215 and info['capture_windows']==[[7400,9200]]
 frames=sorted(int(p.stem)for p in(repair/'frames').glob('*.png'));assert frames==list(range(7400,9201))
 for name in ['apu.tsv']:assert (repair/name).read_bytes()==(full/name).read_bytes()
 with wave.open(str(full/'full.wav'))as f:params=f.getparams();pcm=f.readframes(f.getnframes())
 with wave.open(str(repair/'full.wav'))as f:assert f.getparams()==params and f.readframes(f.getnframes())==pcm
 changes=[]
 for n in frames:
  for kind in ['ram','ppu','oam','view']:
   name=f'{n:06}'+('.json'if kind=='view'else'.bin');assert (repair/kind/name).read_bytes()==(full/kind/name).read_bytes(),(kind,n)
  oldimage=np.array(Image.open(full/f'frames/{n:06}.png').convert('RGB'));newimage=np.array(Image.open(repair/f'frames/{n:06}.png').convert('RGB'))
  if not np.array_equal(oldimage,newimage):assert not newimage.any(),n;changes.append(n)
 assert changes==list(range(7856,7861))+list(range(9146,9154)),changes
 room_frames=0;fade_frames=0
 # Exhaustively prove that every native occurrence of either changed scope
 # is within the new capture window. All other installed bytes/rules are exact.
 for n in range(1,19216):
  ram=(full/f'ram/{n:06}.bin').read_bytes();room=int.from_bytes(ram[0x78:0x7a],'little')
  if ram[0x72]==4 and room==0xa58f:assert 7400<=n<=9200;room_frames+=1
  if ram[0x72]==4 and room==0xb01c:
   pp=(full/f'ppu/{n:06}.bin').read_bytes();o=(full/f'oam/{n:06}.bin').read_bytes()
   if any(o[j]<239 and 0xcd<=o[j+1]<=0xeb and pp[0x3f11+(o[j+2]&3)*4:0x3f14+(o[j+2]&3)*4]==bytes.fromhex('0F0F07')for j in range(0,256,4)):
    assert 7400<=n<=9200;fade_frames+=1
 return dict(final_manifest_verified=True,only_changed_install_file='hires.txt',exact_rule_delta_verified=True,changed_rule_scopes=['A58F background visibility','B01C FF0F0F07 ending dragon blackout'],full_candidate_capture_frames=19215,final_scope_capture_frames=len(frames),all_affected_room_frames_covered=room_frames,all_affected_ending_fade_frames_covered=fade_frames,changed_images=changes,all_other_scope_images_exact=True,native_scope_samples_exact=True,full_APU_and_PCM_exact=True,final_scope_movie=info,preview_method='Unmodified actual PNGs from the full capture, with the 1801 affected-window frames replaced by actual final-pack captures; exactly 13 images change.')

if __name__=='__main__':
 p=argparse.ArgumentParser()
 for k in ['full','repair','out']:p.add_argument('--'+k,required=True)
 a=p.parse_args();root=Path(__file__).resolve().parents[1];result=verify(root,Path(a.full),Path(a.repair));Path(a.out).write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
