"""Compare native state/audio and bound visual changes for the next cave rooms."""
from pathlib import Path
from collections import Counter
import argparse,json,wave,hashlib
import numpy as np
from PIL import Image
p=argparse.ArgumentParser()
for k in ('before','after','out'):p.add_argument('--'+k,required=True)
p.add_argument('--fish-only',action='store_true')
a=p.parse_args();b,c=Path(a.before),Path(a.after);root=Path(__file__).resolve().parents[1]
bi=json.loads((b/'result.json').read_text());ci=json.loads((c/'result.json').read_text())
for k in ('movie_sha256','rom_sha1','core_sha256','movie_frames','captured_frames','stride'):assert bi[k]==ci[k],k
assert bi['movie_completed']and ci['movie_completed'];stride=ci['stride']
frames=sorted(int(f.stem)for f in(c/'frames').glob('*.png'));data={k:{}for k in ('ram','ppu','oam','view')}
for n in frames:
 for k in data:
  f=f'{n:06}'+('.json'if k=='view'else'.bin');raw=(c/k/f).read_bytes();assert raw==(b/k/f).read_bytes(),(n,k);data[k][n]=json.loads(raw)if k=='view'else raw
apu=(b/'apu.tsv').read_bytes();assert apu==(c/'apu.tsv').read_bytes()
with wave.open(str(b/'full.wav'),'rb')as f:bp=f.readframes(f.getnframes());params=f.getparams()
with wave.open(str(c/'full.wav'),'rb')as f:cp=f.readframes(f.getnframes());assert f.getparams()==params
assert bp==cp
sources=[np.array(Image.open(root/f'art/level3_lava/fish_{i}.png').convert('RGBA'))for i in(0,1)]
rows=[[None,0xdd,0xde],[0xdf,0xe0,0xe1],[0xe2,0xe3,0xe4]]
counts=Counter();matches=Counter();positions=[];bad=[];roomcounts=Counter();creature_examples=[]
def room(n):return int.from_bytes(data['ram'][n][0x78:0x7a],'little')
def fish_cells(o):return [tuple(o[i:i+4])for i in range(0,256,4)if o[i]<239 and 0xdd<=o[i+1]<=0xe6 and o[i+2]&3==1]
def fits(im,n):
 o=data['oam'][n];cells=fish_cells(o);found=[]
 for yy,t,at,xx in cells:
  if t!=0xdd:continue
  flip=bool(at&64);X=(xx-8)*2;Y=(yy+1)*2
  if X<2 or X+50>512 or Y+48>480:continue
  local=[q for q in cells if q[0]in[yy,yy+8,yy+16]and q[3]in[xx-8,xx,xx+8]and q[2]==at]
  if len(local)!=8:continue
  phase=int(any(q[1]in(0xe5,0xe6)for q in local));src=sources[phase][:,::-1]if flip else sources[phase]
  excluded=np.zeros((480,512),bool)
  for j in(n-1,n,n+1):
   if j not in data['oam']:continue
   oo=data['oam'][j]
   for i in range(0,256,4):
    y,t,attr,x=oo[i:i+4]
    if y>=239 or 0xdd<=t<=0xe6:continue
    x,y=x*2,(y+1)*2;excluded[max(0,y-2):min(480,y+18),max(0,x-2):min(512,x+18)]=True
  mask=src[:,:,3]>0
  for dx in[-1,0,1]:mask &= ~excluded[Y:Y+48,X+dx:X+dx+48]
  if mask.sum()<80:continue
  best=max((float(np.all(im[Y:Y+48,X+dx:X+dx+48][mask]==src[:,:,:3][mask],axis=1).mean()),dx)for dx in[-1,0,1])
  found.append(dict(origin=[X,Y],x=X+best[1],y=Y,score=best[0],pixels=int(mask.sum()),phase=phase,mirror=flip))
 return found
creature=np.array(Image.open(root/'art/level3_caves/green_creature.png').convert('RGBA'))
for n in frames:
 f=f'{n:06}.png';pb=b/'frames'/f;pc=c/'frames'/f
 if not pb.stat().st_size or not pc.stat().st_size:assert n in[1,2]and pb.stat().st_size==pc.stat().st_size;counts['initial_empty']+=1;continue
 before=np.array(Image.open(pb).convert('RGB'));after=np.array(Image.open(pc).convert('RGB'));diff=np.any(before!=after,axis=2);eq=not diff.any();counts['changed_images'if not eq else'exact_images']+=1
 near=[j for j in(n-stride,n,n+stride)if j in data['ram']];allowed=np.zeros(diff.shape,bool)
 target={0x9b96,0x9c86,0x9cfe,0x9dee}
 if not a.fish_only and any(room(j)in target for j in near):allowed[:]=True
 for j in near:
  for yy,t,at,xx in fish_cells(data['oam'][j]):allowed[max(0,(yy+1)*2-2):min(480,(yy+1)*2+18),max(0,xx*2-2):min(512,xx*2+18)]=True
 assert not(diff&~allowed).any(),('outside authorized scope',n)
 if not before.any():assert not after.any(),('blackout',n);counts['exact_blackouts']+=1
 if all(room(j)==0xffff for j in near):assert eq,('pause menu',n);counts['exact_menu_images']+=1
 roomcounts[f'{room(n):04X}']+=1
 if stride==1 and n-1 in data['oam']:
  bf,cf=fits(before,n-1),fits(after,n-1)
  for old in bf:
   if old['score']!=1:continue
   new=next((q for q in cf if q['origin']==old['origin']),None)
   if new is None:continue
   if new['score']<.99:bad.append(dict(frame=n,before=old,after=new));continue
   if new['score']!=1:continue
   positions.append(dict(frame=n,before=old,after=new));matches[f"fish{new['phase']}/{'right'if new['mirror']else'left'}/dx{new['x']-new['origin'][0]}"]+=1
 if not a.fish_only and room(n)==0x9b96 and n%16==0:
  for flip in[False,True]:
   src=creature[:,::-1]if flip else creature;mask=src[:,:,3]>0;ys,xs=np.nonzero(mask);sy,sx=ys[len(ys)//2],xs[len(xs)//2];color=src[sy,sx,:3]
   for y,x in np.argwhere(np.all(after==color,axis=2)):
    X,Y=int(x-sx),int(y-sy)
    if 0<=X<=448 and 0<=Y<=416 and np.array_equal(after[Y:Y+64,X:X+64][mask],src[:,:,:3][mask]):matches['green_creature/'+str(flip)]+=1;creature_examples.append(dict(frame=n,box=[X,Y,X+64,Y+64],mirrored=flip));break
assert not bad,bad[:10]
windows=[]
if stride==1:
 specs=[(300,450,None),(780,840,None),(1000,1100,None)]if ci['movie_frames']==1200 else [(960,1020,None),(1960,2030,140),(1960,2030,-140)]
 for start,end,cut in specs:
  ps=[q for q in positions if start<=q['frame']<=end and(cut is None or(q['before']['y']<cut if cut>0 else q['before']['y']>=-cut))]
  if not ps:continue
  bx=[q['before']['x']for q in ps];ax=[q['after']['x']for q in ps]
  assert len(set(q['frame']for q in ps))>=(end-start+1)*.7,(start,end,len(ps))
  assert max(bx)-min(bx)==2 and max(ax)==min(ax),(start,end,Counter(bx),Counter(ax))
  assert all(q['before']['y']==q['after']['y']for q in ps)
  windows.append(dict(start=start,end=end,vertical_band=cut,matched_frames=len(ps),before_x=dict(Counter(bx)),after_x=dict(Counter(ax)),native_vertical_motion_preserved=True))
out=Path(a.out);out.parent.mkdir(parents=True,exist_ok=True)
report=dict(version='0.13.0',movie_sha256=ci['movie_sha256'],movie_frames=ci['movie_frames'],capture_stride=stride,paired_native_samples_per_type=len(frames),identical_apu_writes=len(apu.splitlines()),identical_pcm_bytes=len(bp),counts=dict(counts),rooms=dict(roomcounts),source_matches=dict(matches),creature_examples=creature_examples[:8],stability_windows=windows,source_failures=bad,native_gameplay_unchanged=True)
out.write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
