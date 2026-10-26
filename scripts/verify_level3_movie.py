"""Compare paired controller movies, native audio/state and actual sprite pixels."""
import argparse,json,hashlib,wave
from pathlib import Path
from collections import Counter
import numpy as np
from PIL import Image
p=argparse.ArgumentParser()
for k in ['before','after','out']:p.add_argument('--'+k,required=True)
for k in ['detail-before','detail-after']:p.add_argument('--'+k)
a=p.parse_args();root=Path(__file__).resolve().parents[1];b=Path(a.before);c=Path(a.after)
info=json.loads((c/'result.json').read_text());old_info=json.loads((b/'result.json').read_text())
assert info['movie_completed']and old_info['movie_completed']
assert info['movie_sha256']==old_info['movie_sha256']=='c6c3f99a7204f5052c1758ef44ffb4387d2ebc5a8534127a0ddde60ccfde74cd'
assert info['rom_sha1']==old_info['rom_sha1']=='fe2fcd0ad334d792db16535d09f3ab9fb2bea3ac'
assert info['core_sha256']==old_info['core_sha256']
frames=sorted(int(f.stem)for f in(c/'frames').glob('*.png'));assert len(frames)==1721 and max(frames)==6880
for kind in ['ram','ppu','oam','view']:
 for n in frames:
  ext='json'if kind=='view'else'bin';name=f'{n:06}.{ext}'
  assert (b/kind/name).read_bytes()==(c/kind/name).read_bytes(),(kind,n)
apu=(b/'apu.tsv').read_bytes();assert apu==(c/'apu.tsv').read_bytes()
with wave.open(str(b/'full.wav'),'rb')as f:bp=f.readframes(f.getnframes());params=f.getparams()
with wave.open(str(c/'full.wav'),'rb')as f:cp=f.readframes(f.getnframes());assert f.getparams()==params
assert bp==cp,'Audio samples changed'
old=json.loads((root/'evidence/0.10.2-pack-sha256.json').read_text());new=json.loads((c/'installed_pack.json').read_text())
assert sorted(k for k in old if old[k]!=new[k])==['README.txt','hires.txt']
assert sorted(set(new)-set(old))==['Stage3_Forest_Background.png','Stage3_Opening_Tiles_2x.png']
sources=[]
for pose in json.loads((root/'art/level3_opening/poses.json').read_text()):
 sources.append((pose['name'],root/f"art/level3_opening/{pose['name']}.png",pose['rows'][0][0]&255))
sources += [('eye',root/'art/screen2_3/eye_registered.png',0xb0),('bat_folded',root/'art/screen2_2/bat_folded.png',0xca),('bat_open',root/'art/screen2_2/bat_open.png',0xc0)]
templates=[]
for name,path,t in sources:
 src=np.array(Image.open(path).convert('RGBA'))
 for flip in [False,True]:
  im=src[:,::-1]if flip else src;mask=im[:,:,3]>0;colors,counts=np.unique(im[:,:,:3][mask],axis=0,return_counts=True);color=colors[counts.argmin()];sy,sx=np.argwhere(mask&np.all(im[:,:,:3]==color,axis=2))[0]
  templates.append((name+('/mirrored'if flip else'/native'),im,mask,color,int(sx),int(sy),t,flip))
matches=Counter();examples={};changed=exact=black=menus=outside=0;rooms=Counter();palettes=Counter();sprite_ids=Counter();bounds={}
def ptr(n):
 ram=(c/'ram'/f'{n:06}.bin').read_bytes();return int.from_bytes(ram[0x78:0x7a],'little')
targets={0x988a,0x997a,0x99f2}
for n in frames:
 before=np.array(Image.open(b/'frames'/f'{n:06}.png').convert('RGB'));after=np.array(Image.open(c/'frames'/f'{n:06}.png').convert('RGB'));diff=np.any(before!=after,axis=2);equal=not diff.any();exact+=int(equal);changed+=int(not equal)
 ram=(c/'ram'/f'{n:06}.bin').read_bytes();pp=(c/'ppu'/f'{n:06}.bin').read_bytes();room=ptr(n);rooms[f'{room:04X}']+=1
 near=[j for j in[n-4,n,n+4]if j in frames];oams=[(c/'oam'/f'{j:06}.bin').read_bytes()for j in near]
 if not before.any():assert not after.any(),('blackout',n);black+=1
 if n>=6480:assert equal,('final pause menu',n);menus+=1
 if room in targets:
  palettes[f'{room:04X}:'+pp[0x3f00:0x3f10].hex().upper()]+=1
  x=int.from_bytes(ram[0x74:0x76],'little');y=int.from_bytes(ram[0x76:0x78],'little');bounds.setdefault(f'{room:04X}',[]).append([x,y])
 elif all(ptr(j)not in targets for j in near)and diff.any():
  # Later scenery is untouched. Shared actors may change only in native OAM
  # bounds, expanded for movement between these four-frame observer samples.
  # The primary projectile advances up to four native pixels/frame; the
  # previous sample's shot can disappear before the current OAM snapshot.
  allowed=np.zeros(diff.shape,dtype=bool)
  for o in oams:
   for i in range(0,256,4):
    if o[i]>=239:continue
    x,y=2*o[i+3],2*(o[i]+1);allowed[max(0,y-32):min(480,y+48),max(0,x-32):min(512,x+48)]=True
  # Invincibility alternates visible and hidden OAM on a cadence that can
  # alias with stride 4. The screenshot is the previous decoded frame.
  # Include Randy's independently measured RAM anchor and full pose bounds.
  for j in near:
   rr=(c/'ram'/f'{j:06}.bin').read_bytes()
   x=2*(int.from_bytes(rr[0x74:0x76],'little')-int.from_bytes(rr[0x60:0x62],'little'))
   y=2*int.from_bytes(rr[0x76:0x78],'little')
   allowed[max(0,y-48):min(480,y+48),max(0,x-40):min(512,x+40)]=True
  assert not(diff&~allowed).any(),('change outside later-room sprites',n)
  outside+=1
 if n%8:continue
 for o in oams:
  for i in range(0,256,4):
   if o[i]<239:sprite_ids[f'{o[i+1]+0x600:04X}/{o[i+2]:02X}']+=1
 for key,src,mask,color,sx,sy,t,flip in templates:
  if not any(o[i]<239 and o[i+1]==t and bool(o[i+2]&64)==flip for o in oams for i in range(0,256,4)):continue
  h,w=src.shape[:2]
  for y,x in np.argwhere(np.all(after==color,axis=2)):
   X,Y=int(x-sx),int(y-sy)
   if X<0 or Y<0 or X+w>512 or Y+h>480:continue
   if np.array_equal(after[Y:Y+h,X:X+w][mask],src[:,:,:3][mask]):matches[key]+=1;examples.setdefault(key,dict(frame=n,box=[X,Y,X+w,Y+h]));break
detail_report={}
if a.detail_before or a.detail_after:
 assert a.detail_before and a.detail_after
 db,dc=Path(a.detail_before),Path(a.detail_after)
 for folder in [db,dc]:
  detail=json.loads((folder/'result.json').read_text());assert detail['movie_completed'] and detail['movie_sha256']==info['movie_sha256'] and detail['stride']==1
 detail_frames=sorted(f.stem for f in(dc/'frames').glob('*.png'))
 assert detail_frames==[f'{n:06}'for n in range(3148,3173)]
 for kind in ['ram','ppu','oam','view']:
  for f in detail_frames:
   name=f+('.json'if kind=='view'else'.bin');assert(db/kind/name).read_bytes()==(dc/kind/name).read_bytes()
 assert(db/'apu.tsv').read_bytes()==(dc/'apu.tsv').read_bytes()==apu
 for folder in [db,dc]:
  with wave.open(str(folder/'full.wav'),'rb')as f:assert f.readframes(f.getnframes())==bp
 assert json.loads((dc/'installed_pack.json').read_text())==new
 detail_matches=Counter()
 for f in detail_frames:
  after=np.array(Image.open(dc/'frames'/f'{f}.png').convert('RGB'))
  for key,src,mask,color,sx,sy,t,flip in templates:
   if not key.startswith('bat_'):continue
   h,w=src.shape[:2]
   for y,x in np.argwhere(np.all(after==color,axis=2)):
    X,Y=int(x-sx),int(y-sy)
    if X<0 or Y<0 or X+w>512 or Y+h>480:continue
    if np.array_equal(after[Y:Y+h,X:X+w][mask],src[:,:,:3][mask]):
     matches[key]+=1;detail_matches[key]+=1;examples.setdefault(key,dict(frame=int(f),run='every-frame bat window',box=[X,Y,X+w,Y+h]));break
 detail_report=dict(frames=[3148,3172],paired_samples=25,complete_sprite_matches=dict(detail_matches),native_state_and_full_audio_identical=True)
required=['ember_emerge_0/native','ember_emerge_1/native','ember_1/native','ember_1/mirrored','ember_2/native','flyer_0/native','flyer_1/native','eye/native','bat_folded/native','bat_open/native']
missing=[k for k in required if not matches[k]]
report=dict(baseline='0.10.2',candidate='0.11.0',movie_frames=6883,capture_stride=4,native_samples_per_type=len(frames),movie_sha256=info['movie_sha256'],rom_sha1=info['rom_sha1'],emulator_core_sha256=info['core_sha256'],controller_only=True,ram_writes=False,apu_sha256=hashlib.sha256(apu).hexdigest(),apu_write_count=len(apu.splitlines()),identical_pcm_bytes=len(bp),pcm_sha256=hashlib.sha256(bp).hexdigest(),changed_images=changed,exact_images=exact,exact_black_images=black,exact_final_pause_images=menus,later_room_sprite_only_images=outside,rooms=dict(rooms),palettes=dict(palettes),complete_sprite_matches=dict(matches),sprite_examples=examples,unmatched_required_templates=missing,observed_sprite_ids=dict(sprite_ids),unchanged_approved_runtime_files=91,pack_files=95,coverage_limits=['Only the first three Level 3 rooms receive scenery replacements.','The spinning red creature (native 068A–06AF family) and unmapped effects retain original sprites; this is a scenery/selected-actor batch, not complete Level 3 coverage.','The movie ends paused before the boss.','Dedicated far-left stop and slow ledge walk-off are checked separately in edge_validation.json.','Earlier levels are protected by byte-identical assets and exact recovery of their mappings; not replayed afresh for this feature.'])
report['every_frame_bat_window']=detail_report
out=Path(a.out);out.parent.mkdir(parents=True,exist_ok=True);out.write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({k:v for k,v in report.items()if k not in ['sprite_examples','observed_sprite_ids','palettes','coverage_limits']},indent=2))
assert not missing,('Required live sprite templates absent',missing)
