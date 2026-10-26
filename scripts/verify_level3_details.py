"""Check paired movies, requested pixel scope and actual registered sprites/branches."""
from pathlib import Path
from collections import Counter
import argparse,hashlib,json,wave
import numpy as np
from PIL import Image
p=argparse.ArgumentParser()
for k in ['before','after','out']:p.add_argument('--'+k,required=True)
a=p.parse_args();r=Path(__file__).resolve().parents[1];b,c=Path(a.before),Path(a.after)
info=json.loads((c/'result.json').read_text());oldinfo=json.loads((b/'result.json').read_text())
for key in ['movie_sha256','rom_sha1','core_sha256','movie_frames','captured_frames','stride']:assert info[key]==oldinfo[key],key
assert info['movie_completed']and oldinfo['movie_completed']
frames=sorted(int(f.stem)for f in(c/'frames').glob('*.png'));stride=info['stride']
data={k:{n:(c/k/f'{n:06}.bin').read_bytes()for n in frames}for k in ['ram','ppu','oam']}
views={n:json.loads((c/'view'/f'{n:06}.json').read_text())for n in frames}
for kind in ['ram','ppu','oam','view']:
 for n in frames:
  name=f'{n:06}'+('.json'if kind=='view'else'.bin');assert(b/kind/name).read_bytes()==(c/kind/name).read_bytes(),(kind,n)
apu=(c/'apu.tsv').read_bytes();assert apu==(b/'apu.tsv').read_bytes()
with wave.open(str(b/'full.wav'),'rb')as f:bp=f.readframes(f.getnframes());params=f.getparams()
with wave.open(str(c/'full.wav'),'rb')as f:cp=f.readframes(f.getnframes());assert f.getparams()==params
assert bp==cp
prior=json.loads((r/'evidence/0.11.1-pack-sha256.json').read_text());installed=json.loads((c/'installed_pack.json').read_text())
assert all(prior[k]==installed[k]for k in prior if k not in {'README.txt','hires.txt'})
assert sorted(set(installed)-set(prior))==['Stage3_Detail_Tiles_2x.png']
reg=json.loads((r/'art/level3_detail/registration.json').read_text());atlas=Image.open(r/'art/level3_detail/Stage3_Detail_Tiles_2x.png').convert('RGBA')
cells={int(m['tile'],16):np.array(atlas.crop((m['xy'][0],m['xy'][1],m['xy'][0]+16,m['xy'][1]+16)))for m in reg['mappings']if m['kind']=='branch'}
def room(n):return int.from_bytes(data['ram'][n][0x78:0x7a],'little')
def branch_image(n,dy=0):
 out=np.zeros((480,512,4),dtype=np.uint8)
 if room(n)!=0x997a:return out
 v=views[n]['vram'];y=((v&0x3e0)>>2)|((v&0x7000)>>12);y+=240 if v&0x800 else 0
 pp=data['ppu'][n]
 for ty in range(y//8,(y+239)//8+1):
  for tx in range(32):
   py=ty*8%480;nt=0x2000+(py//240)*0x800;yy=(py%240)//8;t=pp[nt+yy*32+tx]+0x700
   at=pp[nt+960+yy//4*8+tx//4];pa=at>>((yy%4)//2*4+(tx%4)//2*2)&3
   if t not in cells or pp[0x3f00+pa*4:0x3f04+pa*4].hex().upper()!='0F091929':continue
   Y=(ty*8-y)*2+dy;top,bottom=max(0,Y),min(480,Y+16)
   if bottom>top:out[top:bottom,tx*16:tx*16+16]=cells[t][top-Y:bottom-Y]
 return out
templates=[]
for name,t in [('round_shot',0x94),('boot',0x8a)]:
 src=np.array(Image.open(r/f'art/level3_detail/{name}.png').convert('RGBA'))
 for flip in [False,True]:
  im=src[:,::-1]if flip else src;mask=im[:,:,3]>0;colors,counts=np.unique(im[:,:,:3][mask],axis=0,return_counts=True);color=colors[counts.argmin()];sy,sx=np.argwhere(mask&np.all(im[:,:,:3]==color,axis=2))[0]
  templates.append((name+('/mirrored'if flip else'/native'),im,mask,color,int(sx),int(sy),t,flip))
counts=Counter();matches=Counter();examples={};branchchecks=[];branchids=set()
for n in frames:
 before=np.array(Image.open(b/'frames'/f'{n:06}.png').convert('RGB'));after=np.array(Image.open(c/'frames'/f'{n:06}.png').convert('RGB'));diff=np.any(before!=after,axis=2)
 counts['changed_images'if diff.any()else'exact_images']+=1
 if not before.any():assert not after.any(),('black',n);counts['exact_black_images']+=1;continue
 if info['movie_frames']==6883 and n>=6480:assert not diff.any(),('pause',n);counts['exact_pause_images']+=1
 near=[j for j in [n-stride,n,n+stride]if j in data['oam']];allowed=np.zeros((480,512),dtype=bool);actors=allowed.copy()
 for j in near:
  o=data['oam'][j]
  for i in range(0,256,4):
   if o[i]>=239:continue
   t=o[i+1];X,Y=2*o[i+3],2*(o[i]+1)
   actors[max(0,Y-12):min(480,Y+28),max(0,X-12):min(512,X+28)]=True
   if t==0x94 or 0x8a<=t<=0x8d:allowed[max(0,Y-12):min(480,Y+28),max(0,X-12):min(512,X+28)]=True
  for dy in range(-6,7):allowed|=branch_image(j,dy)[:,:,3]>0
 assert not(diff&~allowed).any(),('changes outside requested artwork',n,int((diff&~allowed).sum()))
 if n%16==0 and room(n)==0x997a:
  best=(0,0,0)
  for dy in range(-6,7):
   e=branch_image(n,dy);mask=(e[:,:,3]>0)&~actors
   if mask.sum()<100:continue
   hits=int(np.sum(np.all(e[:,:,:3]==after,axis=2)&mask));ratio=hits/int(mask.sum())
   if ratio>best[0]:best=(ratio,dy,int(mask.sum()))
  if best[2]:branchchecks.append(dict(frame=n,match_fraction=best[0],camera_delta_hd=best[1],pixels=best[2]))
 for key,src,mask,color,sx,sy,t,flip in templates:
  if not any(data['oam'][j][i]<239 and data['oam'][j][i+1]==t and bool(data['oam'][j][i+2]&64)==flip for j in near for i in range(0,256,4)):continue
  h,w=src.shape[:2]
  for Y,X in np.argwhere(np.all(after==color,axis=2)):
   X,Y=int(X-sx),int(Y-sy)
   if X<0 or Y<0 or X+w>512 or Y+h>480:continue
   if np.array_equal(after[Y:Y+h,X:X+w][mask],src[:,:,:3][mask]):matches[key]+=1;examples.setdefault(key,dict(frame=n,box=[X,Y,X+w,Y+h]));break
report=dict(baseline='0.11.1',candidate='0.11.2',movie_frames=info['movie_frames'],paired_native_samples_per_type=len(frames),apu_write_count=len(apu.splitlines()),apu_sha256=hashlib.sha256(apu).hexdigest(),identical_pcm_bytes=len(bp),pcm_sha256=hashlib.sha256(bp).hexdigest(),movie_sha256=info['movie_sha256'],rom_sha1=info['rom_sha1'],core_sha256=info['core_sha256'],controller_only=True,ram_writes=False,pack_files=99,unchanged_prior_runtime_files=96,counts=dict(counts),sprite_matches=dict(matches),sprite_examples=examples,branch_source_checks=branchchecks,limits=['Earlier levels and boss are not replayed afresh.','Original branch alpha contours remain exact; native collision and all gameplay are unchanged.'])
if info['movie_frames']==1796:
 def pos(n):
  ram=data['ram'][n];return [int.from_bytes(ram[0x74:0x76],'little'),int.from_bytes(ram[0x76:0x78],'little')]
 assert all(pos(n)==[90,368]for n in range(1665,1677))
 assert all(pos(n)[1]==368 for n in range(1677,1741))
 assert pos(1740)==[137,368]and pos(1741)==[138,369]
 xs=[pos(n)[0]for n in range(1677,1741)]
 assert all(x<=y for x,y in zip(xs,xs[1:]))and xs[0]==90 and xs[-1]==137
 report['branch_walk']=dict(left_stop_frames=[1665,1676],left_stop_position=[90,368],slow_right_walk_frames=[1677,1740],grounded_x_range=[90,137],grounded_y=368,first_fall_frame=1741,first_fall_position=[138,369])
Path(a.out).parent.mkdir(exist_ok=True,parents=True);Path(a.out).write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({k:v for k,v in report.items()if k not in ['branch_source_checks','sprite_examples']},indent=2))
if info['movie_frames']==6883:assert matches['boot/native']and matches['round_shot/native']and branchchecks
assert all(q['match_fraction']>.995 for q in branchchecks),[q for q in branchchecks if q['match_fraction']<=.995]
