"""Require native/audio equality and complete figurines inside the actual OAM footprint."""
from pathlib import Path
from collections import Counter
import argparse,hashlib,json
import numpy as np
from PIL import Image

p=argparse.ArgumentParser();p.add_argument('--before',required=True);p.add_argument('--after',required=True);p.add_argument('--out',required=True);a=p.parse_args()
root=Path(__file__).resolve().parents[1];b=Path(a.before);c=Path(a.after)
def digest(path):
 h=hashlib.sha256()
 with path.open('rb')as f:
  for chunk in iter(lambda:f.read(1024*1024),b''):h.update(chunk)
 return h.hexdigest()
old,new=[json.loads((d/'result.json').read_text())for d in [b,c]]
for key in ['movie_sha256','rom_sha1','core_sha256','movie_frames','captured_frames','stride']:assert old[key]==new[key],key
assert old['movie_completed']and new['movie_completed']
for d,version in [(b,'0.22.1'),(c,'0.22.2')]:assert json.loads((d/'installed_pack.json').read_text())==json.loads((root/f'evidence/{version}-pack-sha256.json').read_text())
frames=sorted(int(f.stem)for f in(c/'frames').glob('*.png'));native={};counts=Counter();matches=[]
for n in frames:
 native[n]={}
 for kind in ['ram','ppu','oam','view']:
  file=f'{n:06}'+('.json'if kind=='view'else'.bin');raw=(c/kind/file).read_bytes();assert raw==(b/kind/file).read_bytes(),(n,kind);native[n][kind]=raw
assert digest(b/'apu.tsv')==digest(c/'apu.tsv')
assert digest(b/'full.wav')==digest(c/'full.wav')
sources={pal:np.array(Image.open(root/f'art/screen1_4/one_up_{src}.png').convert('RGBA'))for pal,src in [('FF300036','FF300036'),('FF221136','FF221136'),('FF190927','FF300036')]}
for n in frames:
 bp,cp=[d/'frames'/f'{n:06}.png'for d in [b,c]]
 if bp.read_bytes()==cp.read_bytes():counts['identical_images']+=1;continue
 before,after=[np.array(Image.open(f).convert('RGB'))for f in [bp,cp]];diff=np.any(before!=after,2)
 if not diff.any():counts['identical_images']+=1;continue
 origins=set();occluders=np.zeros(diff.shape,dtype=bool)
 for j in [n-new['stride'],n,n+new['stride']]:
  if j not in native:continue
  o=native[j]['oam'];pp=native[j]['ppu']
  for i in range(0,256,4):
   y,t,at,x=o[i:i+4];pal='FF'+pp[0x3f11+(at&3)*4:0x3f14+(at&3)*4].hex().upper()
   if y<239 and t==0x4e and pal in sources:
    origins.update((2*x+dx,2*(y+1)+dy,pal,at)for dx in range(-8,9,2)for dy in range(-8,9,2))
   elif y<239 and t not in [0x4e,0x4f]:
    # Randy and Overdrive can overlap the collectible immediately before
    # collection. Only actual neighboring OAM cell bounds may occlude it.
    x0,y0=max(0,2*x-2),max(0,2*(y+1)-2);x1,y1=min(512,2*x+18),min(480,2*(y+1)+18)
    if x0<x1 and y0<y1:occluders[y0:y1,x0:x1]=True
 found=None
 for x,y,pal,at in sorted(origins):
  x0,y0=max(0,x),max(0,y);x1,y1=min(512,x+16),min(480,y+32)
  if x0>=x1 or y0>=y1:continue
  allowed=np.zeros(diff.shape,dtype=bool);allowed[y0:y1,x0:x1]=True
  if (diff&~allowed).any():continue
  src=sources[pal]
  if at&0x40:src=src[:,::-1]
  # Native vertical flip applies independently to each 8x8 sprite cell.
  if at&0x80:src=np.concatenate([src[:16][::-1],src[16:][::-1]])
  src=src[y0-y:y1-y,x0-x:x1-x];mask=src[:,:,3]>0
  equal=np.all(after[y0:y1,x0:x1]==src[:,:,:3],2);mismatch=mask&~equal;whole=not mismatch.any()
  visible_changed=mask&diff[y0:y1,x0:x1]
  # Every changed opaque pixel must be the exact source pixel. Any missing
  # source pixel must be unchanged between packs AND under another native
  # sprite; this retains actual transparent gaps inside OAM cell bounds.
  overlapped=(visible_changed.sum()>=30 and not(mismatch&diff[y0:y1,x0:x1]).any()and not(mismatch&~occluders[y0:y1,x0:x1]).any())
  if whole or overlapped:
   found=dict(frame=n,palette=pal,origin=[x,y],opaque_source_pixels=int(mask.sum()if whole else (mask&equal).sum()),complete=(whole and x0==x and y0==y and x1==x+16 and y1==y+32),native_overlap=not whole);break
 assert found,(n,'changed pixels outside complete approved figurine / native bounds')
 matches.append(found);counts['corrected_images']+=1;counts[pal]+=1
assert matches,'No affected 1-up in this route'
life_events=[dict(frame=n,before=native[prev]['ram'][0x48f],after=native[n]['ram'][0x48f])for prev,n in zip(frames,frames[1:])if native[prev]['ram'][0x48f]!=native[n]['ram'][0x48f]]
report=dict(movie=new,images=dict(counts),native_ram_ppu_oam_scroll_exact=True,full_movie_apu_pcm_exact=True,apu_sha256=digest(c/'apu.tsv'),wav_sha256=digest(c/'full.wav'),every_changed_pixel_inside_native_one_up=True,complete_source_matches=sum(m['complete']for m in matches),life_events=life_events,matches=matches)
Path(a.out).write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:v for k,v in report.items()if k!='matches'},indent=2))
