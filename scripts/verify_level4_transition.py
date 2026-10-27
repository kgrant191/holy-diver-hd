"""Paired native/audio replay and tightly scoped stair/reward/fade differences."""
from pathlib import Path
from collections import Counter
import argparse,hashlib,json,wave
import numpy as np
from PIL import Image
p=argparse.ArgumentParser()
for k in ['before','after','out']:p.add_argument('--'+k,required=True)
p.add_argument('--stairs-only',action='store_true');p.add_argument('--after-manifest',help='Retained stair replay manifest, with exact final scope equivalence evidence');a=p.parse_args();r=Path(__file__).resolve().parents[1];b,c=Path(a.before),Path(a.after)
bi,ci=[json.loads((d/'result.json').read_text())for d in [b,c]]
for k in ['movie_sha256','rom_sha1','core_sha256','movie_frames','captured_frames','stride']:assert bi[k]==ci[k],k
assert bi['movie_completed']and ci['movie_completed']
for d,v in [(b,'0.20.1'),(c,'0.20.2')]:
 expected=Path(a.after_manifest)if d==c and a.after_manifest else r/f'evidence/{v}-pack-sha256.json'
 assert json.loads((d/'installed_pack.json').read_text())==json.loads(expected.read_text())
frames=sorted(int(p.stem)for p in (c/'frames').glob('*.png'));data={k:{}for k in ['ram','ppu','oam','view']}
for n in frames:
 for k in data:
  name=f'{n:06}'+('.json'if k=='view'else'.bin');raw=(c/k/name).read_bytes();assert raw==(b/k/name).read_bytes(),(n,k);data[k][n]=json.loads(raw)if k=='view'else raw
apu=(b/'apu.tsv').read_bytes();assert apu==(c/'apu.tsv').read_bytes(),'APU'
with wave.open(str(b/'full.wav'),'rb')as f:pcm=f.readframes(f.getnframes());params=f.getparams()
with wave.open(str(c/'full.wav'),'rb')as f:assert f.getparams()==params;assert f.readframes(f.getnframes())==pcm,'PCM'
rooms={n:int.from_bytes(v[0x78:0x7a],'little')for n,v in data['ram'].items()};temple={0xa865,0xaa09,0xaa81,0xaaf9,0xab71,0xac61,0xacd9,0xae41,0xaef5}
def mask(n):
 out=np.zeros((480,512),bool)
 for j in [n-ci['stride'],n,n+ci['stride']]:
  if j not in rooms:continue
  room=rooms[j];pp=data['ppu'][j]
  if room in temple:
   v=data['view'][j];vv=v['vram'];sx=(vv&31)*8+v['xscroll']+(256 if vv&0x400 else 0);sy=((vv>>5)&31)*8+((vv>>12)&7)+(240 if vv&0x800 else 0)
   for yy in range(sy//8,(sy+239)//8+1):
    for xx in range(sx//8,(sx+255)//8+1):
     nt=0x2000+xx//32%2*0x400+yy//30%2*0x800;t=pp[nt+(yy%30)*32+xx%32]
     if not 0x82<=t<=0x85:continue
     X,Y=(xx*8-sx)*2,(yy*8-sy)*2;out[max(0,Y-4):min(480,Y+20),max(0,X-4):min(512,X+20)]=True
  if a.stairs_only:continue
  if room==0xafa9:
   # Only native flash/fade palettes permit full background/foreground changes.
   if pp[0x3f00]==0x31 or pp[0x3f0f]in [0x20,0x10,0x00]:out[:]=True
   else:
    o=data['oam'][j]
    for i in range(0,256,4):
     y,t,at,x=o[i:i+4]
     if y<239 and (0x8f<=t<=0x92 or 0x60<=t<=0x63):out[max(0,(y+1)*2-2):min(480,(y+9)*2+2),max(0,x*2-2):min(512,(x+8)*2+2)]=True
  if room==0 and bytes(pp[0x21cd:0x21d4])==bytes([0x35,0x27,0x36,0x2d,0x23,0x24,0x33]):out[:]=True
  if room==0xafe5:
   o=data['oam'][j]
   for i in range(0,256,4):
    y,t,at,x=o[i:i+4];pal=pp[0x3f11+(at&3)*4:0x3f14+(at&3)*4]
    if y<239 and 0x93<=t<=0xae and pal==b'\x30\x30\x30':out[max(0,(y+1)*2-2):min(480,(y+9)*2+2),max(0,x*2-2):min(512,(x+8)*2+2)]=True
 return out
counts=Counter();changed=Counter();pixel_count=0
for n in frames:
 paths=[d/'frames'/f'{n:06}.png'for d in [b,c]]
 if not all(p.stat().st_size for p in paths):assert paths[0].stat().st_size==paths[1].stat().st_size;counts['empty_initial']+=1;continue
 old,im=[np.array(Image.open(p).convert('RGB'))for p in paths];diff=np.any(old!=im,2)
 if diff.any():
  outside=diff&~mask(n);assert not outside.any(),('outside requested scope',n,int(outside.sum()))
  counts['changed']+=1;changed[f'{rooms[n]:04X}']+=1;pixel_count+=int(diff.sum())
 else:counts['identical']+=1
 if not old.any():assert not im.any();counts['native_black_exact']+=1
 if rooms[n]==0x850a:assert not diff.any();counts['level5_arrival_exact']+=1
report=dict(movie_frames=ci['movie_frames'],stride=ci['stride'],native_samples_per_type=len(frames),native_exact=True,apu_exact=True,pcm_exact=True,pcm_bytes=len(pcm),pcm_sha256=hashlib.sha256(pcm).hexdigest(),apu_sha256=hashlib.sha256(apu).hexdigest(),movie_sha256=ci['movie_sha256'],image_checks=counts,changed_by_room=changed,changed_pixels=pixel_count,changes_confined_to_requested_scope=True)
Path(a.out).write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
