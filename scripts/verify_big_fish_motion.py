"""Verify graphics-only hover stabilization in consecutive native captures."""
from pathlib import Path
from collections import Counter
import argparse,json,wave,hashlib
import numpy as np
from PIL import Image
p=argparse.ArgumentParser()
for k in ('before','after','out'):p.add_argument('--'+k,required=True)
a=p.parse_args();b,c=Path(a.before),Path(a.after);root=Path(__file__).resolve().parents[1]
bi=json.loads((b/'result.json').read_text());ci=json.loads((c/'result.json').read_text())
for k in ('movie_sha256','rom_sha1','core_sha256','movie_frames','captured_frames','stride'):assert bi[k]==ci[k],k
assert bi['movie_completed']and ci['movie_completed']
frames=sorted(int(f.stem)for f in(c/'frames').glob('*.png'));data={k:{}for k in ('ram','ppu','oam','view')}
for n in frames:
 for k in data:
  f=f'{n:06}'+('.json'if k=='view'else'.bin');raw=(c/k/f).read_bytes();assert raw==(b/k/f).read_bytes(),(n,k);data[k][n]=raw
apu=(b/'apu.tsv').read_bytes();assert apu==(c/'apu.tsv').read_bytes()
with wave.open(str(b/'full.wav'),'rb')as f:bp=f.readframes(f.getnframes());params=f.getparams()
with wave.open(str(c/'full.wav'),'rb')as f:cp=f.readframes(f.getnframes());assert f.getparams()==params
assert bp==cp
sources=[np.array(Image.open(root/f'art/level3_lava/fish_{i}.png').convert('RGBA'))for i in (0,1)]
counts=Counter();matches=Counter();positions={};bad=[]
def fish_cells(o):return [tuple(o[i:i+4])for i in range(0,256,4)if o[i]<239 and 0xdd<=o[i+1]<=0xe6 and o[i+2]&3==1]
def fit(im,n):
 o=data['oam'][n];cells=fish_cells(o)
 if len(cells)!=8:return None
 x=min(v[3]for v in cells)*2;y=(min(v[0]for v in cells)+1)*2
 if x<1 or x+49>512 or y+48>480:return None
 phase=int(any(v[1]in (0xe5,0xe6)for v in cells));flip=bool(cells[0][2]&64);src=sources[phase][:,::-1]if flip else sources[phase]
 # Other sprites may occlude the fish. Adjacent OAM samples and a one-NES-
 # pixel margin cover motion and the half-pixel registration adjustment.
 excluded=np.zeros((480,512),bool)
 for j in (n-1,n,n+1):
  if j not in data['oam']:continue
  oo=data['oam'][j]
  for i in range(0,256,4):
   yy,t,at,xx=oo[i:i+4]
   if yy>=239 or 0xdd<=t<=0xe6:continue
   X,Y=xx*2,(yy+1)*2;excluded[max(0,Y-2):min(480,Y+18),max(0,X-2):min(512,X+18)]=True
 # Compare every offset on the same exposed source pixels. Different masks
 # would otherwise discard the correct offset near an occluding sprite.
 mask=src[:,:,3]>0
 for dx in (-1,0,1):mask &= ~excluded[y:y+48,x+dx:x+dx+48]
 if mask.sum()<80:return None
 best=None
 for dx in (-1,0,1):
  score=float(np.mean(np.all(im[y:y+48,x+dx:x+dx+48][mask]==src[:,:,:3][mask],axis=1)))
  item=(score,dx,int(mask.sum()),x+dx,y,phase,flip)
  if best is None or item[0]>best[0]:best=item
 return best
stride=ci['stride']
for n in frames:
 f=f'{n:06}.png';pb=b/'frames'/f;pc=c/'frames'/f
 if not pb.stat().st_size or not pc.stat().st_size:
  assert n==1 and pb.stat().st_size==pc.stat().st_size;counts['initial_empty']+=1;continue
 before=np.array(Image.open(pb).convert('RGB'));after=np.array(Image.open(pc).convert('RGB'));diff=np.any(before!=after,axis=2)
 counts['changed_images'if diff.any()else'exact_images']+=1;allowed=np.zeros(diff.shape,bool)
 for j in (n-stride,n,n+stride):
  if j not in data['oam']:continue
  for yy,t,at,xx in fish_cells(data['oam'][j]):allowed[(yy+1)*2:min(480,(yy+1)*2+16),xx*2:min(512,xx*2+16)]=True
 assert not(diff&~allowed).any(),('change outside large fish',n)
 eligible=False;has_attack=False
 for j in (n-stride,n,n+stride):
  if j not in data['ram']:continue
  ram=data['ram'][j];slots=[i for i in range(16)if ram[0x300+i]==0x26]
  if len(slots)!=1:continue
  i=slots[0]
  eligible|=(ram[0x72]==0x10 and ram[0x78:0x7a]==bytes([0xa6,0x9a]) and ram[0x3c0+i]==0xcc and ram[0x3d0+i]in (0,0x80) and ram[0x330+i]==0)
  has_attack|=ram[0x3c0+i]not in (0,0xcc) or ram[0x330+i]!=0
 if not eligible:
  assert not diff.any(),('changed outside hover state',n)
  if has_attack:counts['exact_attack_or_damage_images']+=1
 # Exact previous-frame OAM is available in consecutive runs.
 if stride!=1 or n-1 not in data['oam']:continue
 bf,cf=fit(before,n-1),fit(after,n-1)
 if bf and cf and bf[0]==1 and cf[0]==1:
  matches[f"pose{cf[5]}/{'right'if cf[6]else'left'}/offset{cf[1]}"]+=1
  positions[n]=dict(before_x=bf[3],after_x=cf[3],before_y=bf[4],after_y=cf[4],visible_pixels=cf[2])
 elif bf and cf and bf[0]==1 and cf[0]<.99:bad.append(dict(frame=n,before=bf[0],after=cf[0]))
assert not bad,bad[:10]
windows=[]
if ci['movie_frames']==1200:
 for start,end in ((300,450),(780,840),(1000,1100)):
  ps=[(n,positions[n])for n in range(start,end+1)if n in positions]
  assert len(ps)>.85*(end-start+1),(start,len(ps))
  xs=[d['before_x']for n,d in ps];ys=[d['after_x']for n,d in ps]
  assert max(xs)-min(xs)==2 and max(ys)==min(ys),(start,Counter(xs),Counter(ys))
  assert all(d['before_y']==d['after_y']for n,d in ps)
  windows.append(dict(first_frame=start,last_frame=end,pixel_proven_frames=len(ps),before_x_counts=dict(Counter(xs)),after_x_counts=dict(Counter(ys)),native_horizontal_shake_hd_pixels=2,corrected_horizontal_shake_hd_pixels=0,vertical_motion_unchanged=True))
 assert all(any(f'pose{phase}/{direction}/offset{dx}'in k for k in matches)for phase in (0,1)for direction in ('left','right')for dx in (-1,1))
installed=json.loads((c/'installed_pack.json').read_text());prior=json.loads((root/'evidence/0.12.1-pack-sha256.json').read_text());changed=sorted(k for k in prior if prior[k]!=installed[k]);assert changed==['README.txt','Stage3_Lava_Tiles_2x.png','hires.txt']
report=dict(version='0.12.2',movie_sha256=ci['movie_sha256'],frames=ci['movie_frames'],stride=stride,paired_samples_per_type=len(frames),identical_apu_writes=len(apu.splitlines()),identical_pcm_bytes=len(bp),counts=dict(counts),pixel_proven_pose_offsets=dict(matches),stability_windows=windows,source_failures=bad,changed_files=changed,unchanged_runtime_files=97,native_state_unchanged=True)
out=Path(a.out);out.parent.mkdir(parents=True,exist_ok=True);out.write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
