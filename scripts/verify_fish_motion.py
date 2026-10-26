"""Consecutive-frame fish repair checks, with unchanged native gameplay/audio."""
from pathlib import Path
from collections import Counter
import argparse, hashlib, json, wave
import numpy as np
from PIL import Image

p=argparse.ArgumentParser()
for name in ('before','after','out'):p.add_argument('--'+name,required=True)
a=p.parse_args();b=Path(a.before);c=Path(a.after);root=Path(__file__).resolve().parents[1]
bi=json.loads((b/'result.json').read_text());ci=json.loads((c/'result.json').read_text())
for key in ('movie_sha256','rom_sha1','core_sha256','movie_frames','stride','captured_frames'):assert bi[key]==ci[key],key
assert bi['movie_completed'] and ci['movie_completed'] and ci['stride']==1
frames=sorted(int(f.stem)for f in(c/'frames').glob('*.png'));assert len(frames)==ci['movie_frames']==3705
oam={};counts=Counter();matches=Counter();examples={}
for n in frames:
 for kind in ('ram','ppu','oam','view'):
  f=f'{n:06}'+('.json'if kind=='view'else'.bin');raw=(c/kind/f).read_bytes();assert raw==(b/kind/f).read_bytes(),(kind,n)
  if kind=='oam':oam[n]=raw
assert (b/'apu.tsv').read_bytes()==(c/'apu.tsv').read_bytes()
with wave.open(str(b/'full.wav'),'rb')as f:bp=f.readframes(f.getnframes());params=f.getparams()
with wave.open(str(c/'full.wav'),'rb')as f:cp=f.readframes(f.getnframes());assert f.getparams()==params
assert bp==cp
old=json.loads((b/'installed_pack.json').read_text());new=json.loads((c/'installed_pack.json').read_text())
assert old==json.loads((root/'evidence/0.12.0-pack-sha256.json').read_text())
changed_files=sorted(k for k in old if old[k]!=new[k]);assert changed_files==['README.txt','Stage3_Lava_Tiles_2x.png']
assert set(old)==set(new)
art=root/'art/level3_lava';s0=np.array(Image.open(art/'fish_small_0.png'));s1=np.array(Image.open(art/'fish_small_1.png'))
static_mask=np.zeros(s0.shape[:2],bool);static_mask[:,9:]=True
assert np.array_equal(s0[static_mask],s1[static_mask]),'Small-fish head/body changes between poses'
phase_delta=np.any(s0!=s1,axis=2)&((s0[:,:,3]>0)|(s1[:,:,3]>0))
assert not phase_delta[:,9:].any() and phase_delta.any()
templates=[]
for name in ('fish_0','fish_1','fish_small_0','fish_small_1'):
 src=np.array(Image.open(art/(name+'.png')).convert('RGBA'))
 for flip in (False,True):
  im=src[:,::-1]if flip else src;mask=im[:,:,3]>0;colors,cs=np.unique(im[:,:,:3][mask],axis=0,return_counts=True);color=colors[cs.argmin()]
  sy,sx=np.argwhere(mask&np.all(im[:,:,:3]==color,axis=2))[0]
  templates.append((name+('/mirrored'if flip else'/native'),im,mask,color,int(sx),int(sy)))
for n in frames:
 pf=b/'frames'/f'{n:06}.png';qf=c/'frames'/f'{n:06}.png'
 if not pf.stat().st_size or not qf.stat().st_size:
  assert n==1 and pf.stat().st_size==qf.stat().st_size;counts['initial_empty']+=1;continue
 before=np.array(Image.open(pf).convert('RGB'));after=np.array(Image.open(qf).convert('RGB'))
 diff=np.any(before!=after,axis=2);counts['changed_images'if diff.any()else'exact_images']+=1
 allowed=np.zeros(diff.shape,bool);small_present=False;large_present=False
 for j in (n-1,n,n+1):
  if j not in oam:continue
  oo=oam[j]
  for i in range(0,256,4):
   y,t,at,x=oo[i:i+4]
   if y>=239:continue
   large_present|=0xdd<=t<=0xe6;small_present|=0xef<=t<=0xf2
   if t in (0xf1,0xf2):allowed[2*(y+1):min(480,2*(y+1)+16),2*x:min(512,2*x+16)]=True
 assert not(diff&~allowed).any(),('pixels changed outside small alternate pose',n)
 if not small_present and not large_present:continue
 for key,src,mask,color,sx,sy in templates:
  if ('small'in key and not small_present)or('small'not in key and not large_present):continue
  h,w=src.shape[:2]
  for yy,xx in np.argwhere(np.all(after==color,axis=2)):
   X,Y=int(xx)-sx,int(yy)-sy
   if X<0 or Y<0 or X+w>512 or Y+h>480:continue
   if np.array_equal(after[Y:Y+h,X:X+w][mask],src[:,:,:3][mask]):
    matches[key]+=1;examples.setdefault(key,dict(frame=n,box=[X,Y,X+w,Y+h]));break
for key in ('fish_0/native','fish_1/native','fish_small_0/native','fish_small_1/native','fish_small_0/mirrored','fish_small_1/mirrored'):assert matches[key],key
assert counts['changed_images']>0
# The large fish is deliberately omitted by the game on alternating hit frames.
hit_presence={str(n):sum(1 for i in range(0,256,4)if oam[n][i]<239 and 0xdd<=oam[n][i+1]<=0xe6)for n in range(374,382)}
assert list(hit_presence.values())==[8,0,8,0,8,0,8,0]
report=dict(candidate='0.12.1',baseline='0.12.0 review',movie_frames=ci['movie_frames'],movie_sha256=ci['movie_sha256'],paired_native_samples_per_type=len(frames),apu_writes=len((c/'apu.tsv').read_text().splitlines()),identical_pcm_bytes=len(bp),counts=dict(counts),sprite_matches=dict(matches),sprite_examples=examples,small_pose_changed_visible_pixels=int(phase_delta.sum()),small_static_head_body_exact=True,large_hit_native_oam_cells=hit_presence,changed_pack_files=changed_files,unchanged_pack_files=len(old)-len(changed_files),native_gameplay_modified=False,art_design_unchanged=True)
out=Path(a.out);out.parent.mkdir(parents=True,exist_ok=True);out.write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
