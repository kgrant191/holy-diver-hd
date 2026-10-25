"""Paired native movie, scoped pixel changes, complete sprites and wood geometry."""
from pathlib import Path
import argparse,json,hashlib,wave
from collections import Counter
import numpy as np
from PIL import Image
p=argparse.ArgumentParser()
for k in ['before','after','out']:p.add_argument('--'+k,required=True)
a=p.parse_args();r=Path(__file__).resolve().parents[1];b,c=Path(a.before),Path(a.after)
info=json.loads((c/'result.json').read_text());oldinfo=json.loads((b/'result.json').read_text())
for key in ['movie_sha256','rom_sha1','core_sha256','movie_frames','captured_frames','stride']:assert info[key]==oldinfo[key],key
assert info['movie_completed']and oldinfo['movie_completed']and info['movie_frames']==6883
frames=sorted(int(f.stem)for f in(c/'frames').glob('*.png'));assert len(frames)==1721
ram={n:(c/'ram'/f'{n:06}.bin').read_bytes()for n in frames};ppu={n:(c/'ppu'/f'{n:06}.bin').read_bytes()for n in frames};oam={n:(c/'oam'/f'{n:06}.bin').read_bytes()for n in frames};views={n:json.loads((c/'view'/f'{n:06}.json').read_text())for n in frames}
for kind in ['ram','ppu','oam','view']:
 for n in frames:
  name=f'{n:06}'+('.json'if kind=='view'else'.bin');assert(b/kind/name).read_bytes()==(c/kind/name).read_bytes(),(kind,n)
apu=(c/'apu.tsv').read_bytes();assert apu==(b/'apu.tsv').read_bytes()
with wave.open(str(b/'full.wav'),'rb')as f:bp=f.readframes(f.getnframes());params=f.getparams()
with wave.open(str(c/'full.wav'),'rb')as f:cp=f.readframes(f.getnframes());assert f.getparams()==params
assert bp==cp
prior=json.loads((r/'evidence/0.11.0-pack-sha256.json').read_text());installed=json.loads((c/'installed_pack.json').read_text())
assert sorted(k for k in prior if prior[k]!=installed[k])==['README.txt','hires.txt']
assert sorted(set(installed)-set(prior))==['Stage3_Forest_Wood.png','Stage3_Review_Tiles_2x.png','Stage3_Tree_Wood.png']
assert 'error'not in(c/'emulator.log').read_text().lower()
oldreg=json.loads((r/'art/level3_opening/registration.json').read_text());wood={name:Image.open(r/f'art/level3_review/Stage3_{name.title()}_Wood.png').convert('RGBA')for name in ['forest','tree']}
templates=[]
for pose in json.loads((r/'art/level3_review/poses.json').read_text()):
 src=np.array(Image.open(r/f"art/level3_review/{pose['name']}.png").convert('RGBA'))
 for flip in [False,True]:
  im=src[:,::-1]if flip else src;mask=im[:,:,3]>0;colors,counts=np.unique(im[:,:,:3][mask],axis=0,return_counts=True);color=colors[counts.argmin()];sy,sx=np.argwhere(mask&np.all(im[:,:,:3]==color,axis=2))[0]
  templates.append((pose['name']+('/mirrored'if flip else'/native'),im,mask,color,int(sx),int(sy),pose['rows'][0][0]&255,flip))
def room(n):return int.from_bytes(ram[n][0x78:0x7a],'little')
def camera(n):
 v=views[n];t=v['vram'];x=((t&31)<<3)|v['xscroll']|(256 if t&0x400 else 0);y=((t&0x3e0)>>2)|((t&0x7000)>>12);y+=240 if t&0x800 else 0
 if room(n)==0x988a:x+=round((int.from_bytes(ram[n][0x60:0x62],'little')-x)/512)*512;return 'forest',x,0
 if room(n)==0x997a:return 'tree',0,y
 return None,0,0
def surface(name,x,y):return np.array(wood[name].crop((x*2,y*2,x*2+512,y*2+480)))
def native_wood(n,name,x,y):
 out=np.zeros((480,512),dtype=bool);pp=ppu[n]
 for ty in range(y//8,(y+239)//8+1):
  for tx in range(x//8,(x+255)//8+1):
   px,py=(tx*8)%512,(ty*8)%480;nt=0x2000+(px//256)*0x400+(py//240)*0x800;xx,yy=(px%256)//8,(py%240)//8;t=pp[nt+yy*32+xx]+0x700
   at=pp[nt+960+yy//4*8+xx//4];pa=(at>>(((yy%4)//2)*4+((xx%4)//2)*2))&3;pal=pp[0x3f00+pa*4:0x3f04+pa*4].hex().upper()
   key=f'{name}:{t:04X}:{pal}'
   if not(0x752<=t<=0x767 and key in oldreg['terrain_masks']):continue
   m=np.array(oldreg['terrain_masks'][key])>0;X,Y=(tx*8-x)*2,(ty*8-y)*2;left,top=max(0,X),max(0,Y);right,bottom=min(512,X+16),min(480,Y+16)
   out[top:bottom,left:right]=m[top-Y:bottom-Y,left-X:right-X]
 return out
matches=Counter();examples={};counts=Counter();woodchecks=[];geometry_errors=[]
for n in frames:
 before=np.array(Image.open(b/'frames'/f'{n:06}.png').convert('RGB'));after=np.array(Image.open(c/'frames'/f'{n:06}.png').convert('RGB'));diff=np.any(before!=after,axis=2);counts['changed_images'if diff.any()else'exact_images']+=1
 if not before.any():assert not after.any(),('black',n);counts['exact_black_images']+=1;continue
 if n>=6480:assert not diff.any(),('pause',n);counts['exact_pause_images']+=1
 near=[j for j in [n-4,n,n+4]if j in oam];allowed=np.zeros((480,512),dtype=bool);actors=allowed.copy()
 for j in near:
  o=oam[j]
  for i in range(0,256,4):
   if o[i]>=239:continue
   t=o[i+1];X,Y=2*o[i+3],2*(o[i]+1)
   actors[max(0,Y-16):min(480,Y+32),max(0,X-16):min(512,X+32)]=True
   if 0x95<=t<=0xaf or 0xb6<=t<=0xb9 or 0xe7<=t<=0xee:allowed[max(0,Y-32):min(480,Y+48),max(0,X-32):min(512,X+48)]=True
 name,x,y=camera(n)
 # The screenshot is the previously decoded frame; room-pointer changes
 # can therefore precede the last visible image of the departing room.
 for j in near:
  nm,xx,yy=camera(j)
  if nm:
   for delta in range(-2,3):allowed|=surface(nm,xx+(delta if nm=='forest'else 0),yy+(delta if nm=='tree'else 0))[:,:,3]>0
 if name:
  # Fixed image masks are required to agree with the measured native cells.
  if all(room(j)==room(n)for j in near):
   expected=surface(name,x,y);native=native_wood(n,name,x,y)
   if not np.array_equal(expected[:,:,3]>0,native):geometry_errors.append([n,int(np.sum((expected[:,:,3]>0)!=native))])
   elif native.any():counts['exact_wood_geometry_images']+=1
  if n%16==0 and np.any(surface(name,x,y)[:,:,3]):
   rx=int.from_bytes(ram[n][0x74:0x76],'little')-x;ry=int.from_bytes(ram[n][0x76:0x78],'little')-y
   actors[max(0,ry*2-48):min(480,ry*2+48),max(0,rx*2-40):min(512,rx*2+40)]=True
   best=(0,0,0)
   for delta in range(-3,4):
    e=surface(name,x+(delta if name=='forest'else 0),y+(delta if name=='tree'else 0));mask=(e[:,:,3]>0)&~actors
    if mask.sum()<200:continue
    hit=int(np.sum(np.all(e[:,:,:3]==after,axis=2)&mask));ratio=hit/int(mask.sum())
    if ratio>best[0]:best=(ratio,delta,int(mask.sum()))
   woodchecks.append(dict(frame=n,room=name,match_fraction=best[0],camera_delta=best[1],pixels=best[2]))
 assert not(diff&~allowed).any(),('changes outside requested artwork',n,int((diff&~allowed).sum()))
 for key,src,mask,color,sx,sy,t,flip in templates:
  if not any(oam[j][i]<239 and oam[j][i+1]==t and bool(oam[j][i+2]&64)==flip for j in near for i in range(0,256,4)):continue
  h,w=src.shape[:2]
  for Y,X in np.argwhere(np.all(after==color,axis=2)):
   X,Y=int(X-sx),int(Y-sy)
   if X<0 or Y<0 or X+w>512 or Y+h>480:continue
   if np.array_equal(after[Y:Y+h,X:X+w][mask],src[:,:,:3][mask]):matches[key]+=1;examples.setdefault(key,dict(frame=n,box=[X,Y,X+w,Y+h]));break
required=[f'{name}/native'for name in ['spinner_0','spinner_1','spinner_2','ember_shot_0','ember_shot_1','insect_0','insect_1']]
missing=[k for k in required if not matches[k]]
report=dict(baseline='0.11.0',candidate='0.11.1',movie_frames=6883,paired_native_samples_per_type=1721,apu_write_count=len(apu.splitlines()),apu_sha256=hashlib.sha256(apu).hexdigest(),identical_pcm_bytes=len(bp),pcm_sha256=hashlib.sha256(bp).hexdigest(),movie_sha256=info['movie_sha256'],rom_sha1=info['rom_sha1'],core_sha256=info['core_sha256'],controller_only=True,ram_writes=False,pack_files=98,unchanged_prior_runtime_files=93,counts=dict(counts),sprite_matches=dict(matches),sprite_examples=examples,missing_templates=missing,wood_source_checks=woodchecks,wood_geometry_errors=geometry_errors,limits=['Supplied route covers the three opening rooms and following corridor; no boss coverage.','Earlier levels retain exact assets and mapping bytes; not replayed afresh.'])
Path(a.out).parent.mkdir(exist_ok=True,parents=True);Path(a.out).write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({k:v for k,v in report.items()if k not in ['wood_source_checks','sprite_examples']},indent=2))
assert not missing,missing
assert not geometry_errors,geometry_errors[:10]
assert woodchecks and all(q['match_fraction']>.99 for q in woodchecks),[q for q in woodchecks if q['match_fraction']<=.99]
