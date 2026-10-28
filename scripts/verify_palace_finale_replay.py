"""Validate paired finale captures without altering native game execution."""
from pathlib import Path
from collections import Counter
import argparse,json,hashlib,wave
import numpy as np
from PIL import Image
p=argparse.ArgumentParser()
for key in ['before','after','out']:p.add_argument('--'+key,required=True)
p.add_argument('--candidate-manifest',default='evidence/0.24.0-pack-sha256.json')
a=p.parse_args();r=Path(__file__).resolve().parents[1];b,c=Path(a.before),Path(a.after)
infos=[json.loads((d/'result.json').read_text())for d in [b,c]]
for k in ['movie_sha256','rom_sha1','core_sha256','movie_frames','captured_frames','stride']:assert infos[0][k]==infos[1][k],k
assert all(v['movie_completed']for v in infos)
for d,manifest in [(b,'evidence/0.23.0-pack-sha256.json'),(c,a.candidate_manifest)]:assert json.loads((d/'installed_pack.json').read_text())==json.loads((r/manifest).read_text())
frames=sorted(int(f.stem)for f in(c/'frames').glob('*.png'));data={k:{}for k in ['ram','ppu','oam','view']}
for n in frames:
 for k in data:
  name=f'{n:06}'+('.json'if k=='view'else'.bin');raw=(c/k/name).read_bytes();assert raw==(b/k/name).read_bytes(),(n,k);data[k][n]=json.loads(raw)if k=='view'else raw
apu=(c/'apu.tsv').read_bytes();assert apu==(b/'apu.tsv').read_bytes()
with wave.open(str(b/'full.wav'),'rb')as f:pcm=f.readframes(f.getnframes());params=f.getparams()
with wave.open(str(c/'full.wav'),'rb')as f:assert f.getparams()==params and f.readframes(f.getnframes())==pcm
def source(path,mirror=False):
 src=np.array(Image.open(path).convert('RGBA'))
 if mirror:src=src[:,::-1]
 mask=src[:,:,3]==255;colors,counts=np.unique(src[mask,:3],axis=0,return_counts=True);color=colors[np.argmax(colors.sum(1)/(1+counts))];yy,xx=np.where(mask&np.all(src[:,:,:3]==color,2));pts=np.argwhere(mask)
 return src,mask,int(yy[0]),int(xx[0]),pts[np.linspace(0,len(pts)-1,8,dtype=int)]
def matches(im,item):
 src,mask,ay,ax,probes=item;h,w=mask.shape;yy,xx=np.where(np.all(im==src[ay,ax,:3],2));yy-=ay;xx-=ax;v=(yy>=0)&(xx>=0)&(yy+h<=480)&(xx+w<=512);yy,xx=yy[v],xx[v]
 for py,px in probes:
  v=np.all(im[yy+py,xx+px]==src[py,px,:3],1);yy,xx=yy[v],xx[v]
  if not len(yy):return []
 return [[int(x),int(y)]for y,x in zip(yy,xx)if np.array_equal(im[y:y+h,x:x+w][mask],src[:,:,:3][mask])]

paths={name:r/'art/level5_finale'/(name+'.png')for name in ['skull0','skull1','claw0','claw1','fist0','fist1','idol','effigy','effigy_sprite']}
unit=Image.open(r/'art/level5_continuation/lift_unit.png').convert('RGBA');lift=Image.new('RGBA',(64,32));lift.paste(unit,(0,0));lift.paste(unit,(32,0));tmp=Path(a.out).parent/'lift_source.png';lift.save(tmp);paths['lift']=tmp
sources={name:[source(path,mirror)for mirror in [False,True]]for name,path in paths.items()};hits={};counts=Counter();rooms=Counter();changed=[];bgstats={}
rooms_by_frame={n:f'{int.from_bytes(data["ram"][n][0x78:0x7a],"little"):04X}'for n in frames}
bg=np.array(Image.open(c/'mesen_home/HdPacks/Holy_Diver_(Tr)/Demonic_Palace_Interior.png').convert('RGB'))[:,:512]
flash=np.array(Image.open(c/'mesen_home/HdPacks/Holy_Diver_(Tr)/Demonic_Palace_Boss_Flash.png').convert('RGBA'))[:,:512].astype(np.int32)
flash_target=((flash[:,:,:3]*176+np.array([255,254,255])*79)//255).astype(np.uint8)
missing_backgrounds=[];flash_checks=[]
def variants(target):
 result=[]
 for gray in [False,True]:
  base=np.repeat((target.astype(np.uint16).sum(2)//3)[:,:,None],3,2)if gray else target
  for bits in range(8):
   factors=np.ones(3)
   for bit in range(3):
    if bits&(1<<bit):factors*=np.array([1.1 if channel==bit else .9 for channel in range(3)])
   result.append(np.minimum(base.astype(float)*factors,255).astype(np.uint8))
 return result
normal_variants={'8D3E':variants(bg),'8E6A':variants((bg*.5).astype(np.uint8)),'8EE2':variants((bg*.5).astype(np.uint8))}
flash_variants=variants(flash_target)
for n in frames:
 ps=[d/'frames'/f'{n:06}.png'for d in [b,c]]
 if not all(v.stat().st_size for v in ps):assert ps[0].stat().st_size==ps[1].stat().st_size;counts['empty_initial']+=1;continue
 old,im=[np.array(Image.open(v).convert('RGB'))for v in ps];different=not np.array_equal(old,im);counts['changed'if different else'identical']+=1
 if different:changed.append(n)
 room=rooms_by_frame[n];rooms[room]+=1
 if not old.any():assert not im.any(),(n,'native blackout');counts['native_black_exact']+=1;continue
 if room in ['FFFF','0000','8C4E']:
  if all(rooms_by_frame.get(j,room)==room for j in [n-2,n+2]):assert not different,(n,room);counts['prior_room_menu_lives_exact']+=1
  continue
 assert room in ['8D3E','8E6A','8EE2','9A8B']
 # Report measured panorama samples; native death/fade phases are reviewed
 # separately, never exempted from the state and audio comparisons above.
 if room!='9A8B':
  target=bg if room=='8D3E'else(bg*.5).astype(np.uint8)
  pixels=int(np.all(im==target,2).sum())
  if pixels<=10000:
   for v in normal_variants[room]:
    pixels=max(pixels,int(np.all(im==v,2).sum()))
    if pixels>10000:break
  if pixels>10000:bgstats.setdefault(room,[]).append(pixels)
  pal=data['ppu'][n][0x3f00:0x3f04].hex()
  normal={'8D3E':'0f0f0111','8E6A':'0f072737','8EE2':'0f011121'}[room]
  stable=all(rooms_by_frame.get(j)==room for j in [n-2,n+2])
  # Screenshot submission can lag PPU palette writes; the actual native
  # rendered field, including grayscale/emphasis, decides the flash phase.
  native_bright=int((old.max(2)>150).sum())
  rendered_flash=room=='8E6A' and native_bright>150000
  if rendered_flash:
   count=0
   for v in flash_variants:
    count=max(count,int(np.all(im==v,2).sum()))
    if count>10000:break
   assert count>10000,(n,'flash backdrop',count);flash_checks.append([n,count])
  elif pal==normal and stable and pixels<=10000 and np.any(old!=0,2).sum()>15000:
   missing_backgrounds.append([n,room,pal,pixels])
 if n%10==0:
  for name,variants in sources.items():
   if name in hits:continue
   if (name=='lift')!=(room=='8D3E'):continue
   for mirror,item in enumerate(variants):
    positions=matches(im,item)
    if positions:hits[name]=dict(frame=n,mirrored=bool(mirror),positions=positions);break
missing=set(sources)-set(hits)
report=dict(candidate_manifest=a.candidate_manifest,movie=infos[1],native_samples_per_type=len(frames),native_exact=True,apu_exact=True,pcm_exact=True,apu_sha256=hashlib.sha256(apu).hexdigest(),pcm_sha256=hashlib.sha256(pcm).hexdigest(),images=counts,rooms=rooms,backgrounds={k:dict(samples=len(v),minimum_pixels=min(v))for k,v in bgstats.items()},live_whole_source_matches=hits,missing_whole_sources=sorted(missing),missing_backgrounds=missing_backgrounds,flash_backdrop_checks=flash_checks,changed_frames=changed)
Path(a.out).write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:v for k,v in report.items()if k!='changed_frames'},indent=2));tmp.unlink()
assert not missing,missing
assert not missing_backgrounds,missing_backgrounds[:30]
assert len(flash_checks)>=30,len(flash_checks)
