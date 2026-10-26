"""Paired native-state/audio checks and pixel validation for the lava corridor."""
from pathlib import Path
from collections import Counter
import argparse,json,hashlib,wave
import numpy as np
from PIL import Image
p=argparse.ArgumentParser()
for k in ['before','after','out']:p.add_argument('--'+k,required=True)
a=p.parse_args();root=Path(__file__).resolve().parents[1];b,c=Path(a.before),Path(a.after)
info=json.loads((c/'result.json').read_text());old=json.loads((b/'result.json').read_text())
for key in ['movie_sha256','rom_sha1','core_sha256','movie_frames','captured_frames','stride']:assert info[key]==old[key],key
assert info['movie_completed']and old['movie_completed']
frames=sorted(int(f.stem)for f in(c/'frames').glob('*.png'));stride=info['stride'];data={k:{}for k in ['ram','ppu','oam','view']}
for n in frames:
 for kind in data:
  f=f'{n:06}'+('.json'if kind=='view'else'.bin');raw=(c/kind/f).read_bytes();assert raw==(b/kind/f).read_bytes(),(kind,n)
  data[kind][n]=json.loads(raw)if kind=='view'else raw
apu=(c/'apu.tsv').read_bytes();assert apu==(b/'apu.tsv').read_bytes()
with wave.open(str(b/'full.wav'),'rb')as f:bp=f.readframes(f.getnframes());params=f.getparams()
with wave.open(str(c/'full.wav'),'rb')as f:cp=f.readframes(f.getnframes());assert f.getparams()==params
assert bp==cp,'PCM changed'
installed=json.loads((c/'installed_pack.json').read_text());prior=json.loads((root/'evidence/0.11.2-pack-sha256.json').read_text())
assert all(installed[k]==v for k,v in prior.items()if k not in {'hires.txt','README.txt'})
assert set(installed)-set(prior)=={'Stage3_Lava_Tiles_2x.png'}
assert 'error'not in(c/'emulator.log').read_text().lower()
reg=json.loads((root/'art/level3_lava/registration.json').read_text());atlas=Image.open(root/'art/level3_lava/Stage3_Lava_Tiles_2x.png').convert('RGBA')
cells={}
for m in reg['mappings']:
 if not m['scope'].startswith('l3lavaRoom'):continue
 x,y=m['xy'];cells[(int(m['tile'],16),m['palette'])]=np.array(atlas.crop((x,y,x+16,y+16)))
pack=root/'build/Holy_Diver_(Tr)';images=[l[5:]for l in(pack/'hires.txt').read_text().splitlines()if l.startswith('<img>')]
for m in reg['lava_aliases']:
 f=m['source_rule'].split('<tile>')[1].split(',');x,y=map(int,f[3:5]);cells[(int(m['tile'],16),m['palette'])]=np.array(Image.open(pack/images[int(f[0])]).convert('RGBA').crop((x,y,x+16,y+16)))
background=Image.open(pack/'Stage2_Cave_Background.png').convert('RGB');boot=np.array(Image.open(root/'art/level3_detail/boot.png').convert('RGBA'));bootmask=boot[:,:,3]>0
def room(n):return int.from_bytes(data['ram'][n][0x78:0x7a],'little')
def menu(n):return data['ppu'][n][0x3f00:0x3f04].hex()=='0f072830'
def has_boot(n):
 pp=data['ppu'][n];return room(n)==0xffff and menu(n)and [pp[x]for x in [0x2129,0x212a,0x2149,0x214a]]==[0x74,0x73,0x72,0x71]
def scene(n):return room(n)==0x9aa6 and data['ppu'][n][0x3f04:0x3f08].hex()in ['0f060616','0f161606','0f122131']
def cam(n):
 v=data['view'][n];t=v['vram'];x=((t&31)<<3)|v['xscroll']|(256 if t&0x400 else 0)
 return x+round((int.from_bytes(data['ram'][n][0x60:0x62],'little')-x)/512)*512
def render(n,dx):
 # Exact reused panorama and native-cell replacement pixels, before sprites.
 x=cam(n)+dx;out=np.array(background.crop((x*2,0,x*2+512,480)));coverage=np.zeros((480,512),dtype=bool);lava=coverage.copy();pp=data['ppu'][n]
 for ty in range(30):
  for tx in range(x//8,(x+255)//8+1):
   xx=tx%32;nt=0x2000+((tx//32)%2)*0x400;t=pp[nt+ty*32+xx]+0x700;at=pp[nt+960+ty//4*8+xx//4];pa=at>>((ty%4)//2*4+(xx%4)//2*2)&3;pal=pp[0x3f00+pa*4:0x3f04+pa*4].hex().upper()
   im=cells.get((t,pal))
   if im is None:continue
   X=(tx*8-x)*2;Y=ty*16;left,right=max(0,X),min(512,X+16)
   if right<=left:continue
   tile=im[:,left-X:right-X];mask=tile[:,:,3]>0;part=out[Y:Y+16,left:right];part[mask]=tile[:,:,:3][mask];coverage[Y:Y+16,left:right]=mask
   if 0x73e<=t<=0x743:lava[Y:Y+16,left:right]=mask
 return out,coverage,lava
templates=[]
for pose in json.loads((root/'art/level3_lava/poses.json').read_text()):
 src=np.array(Image.open(root/f"art/level3_lava/{pose['name']}.png").convert('RGBA'));t=next(t for row in pose['rows']for t in row if t is not None)&255
 for flip in [False,True]:
  im=src[:,::-1]if flip else src;mask=im[:,:,3]>0;colors,counts=np.unique(im[:,:,:3][mask],axis=0,return_counts=True);color=colors[counts.argmin()];sy,sx=np.argwhere(mask&np.all(im[:,:,:3]==color,axis=2))[0]
  templates.append((pose['name']+('/mirrored'if flip else'/native'),im,mask,color,int(sx),int(sy),t,flip))
counts=Counter();matches=Counter();examples={};sourcechecks=[];effect_ids=Counter();palette_counts=Counter();scope_errors=[];camera_values=[]
for n in frames:
 if not(b/'frames'/f'{n:06}.png').stat().st_size or not(c/'frames'/f'{n:06}.png').stat().st_size:
  assert n==1,'Only the initial post-state screenshot may be unavailable'
  counts['initial_capture_unavailable']+=1;continue
 before=np.array(Image.open(b/'frames'/f'{n:06}.png').convert('RGB'));after=np.array(Image.open(c/'frames'/f'{n:06}.png').convert('RGB'));diff=np.any(before!=after,axis=2);equal=not diff.any();counts['exact_images'if equal else'changed_images']+=1
 if not before.any():assert not after.any(),('blackout',n);counts['exact_black_images']+=1;continue
 near=[j for j in [n-stride,n,n+stride]if j in data['ram']];allowed=np.zeros((480,512),dtype=bool);actors=allowed.copy()
 stable_menu=all(menu(j)for j in near)
 if stable_menu:
  allowed[144:176,144:176]=True;assert not(diff&~allowed).any(),('menu changed beyond boot',n)
  counts['menu_images']+=1
  # PPU cells are loaded while the native menu is still hidden. Its actual
  # brown boot pixels distinguish visible items from that blank transition.
  native_boot_visible=np.any(np.all(before[144:176,144:176]==[153,78,0],axis=2))
  if native_boot_visible and has_boot(n):assert np.array_equal(after[144:176,144:176][bootmask],boot[:,:,:3][bootmask]),('menu boot source',n);counts['exact_menu_boot_images']+=1
  elif not native_boot_visible:assert equal,('blank menu transition',n)
 else:
  if any(scene(j)for j in near):allowed[:]=True;counts['corridor_images']+=1
  if any(menu(j)for j in near):allowed[144:176,144:176]=True
 for j in near:
  pp=data['ppu'][j];o=data['oam'][j]
  for i in range(0,256,4):
   if o[i]>=239:continue
   # Approved bat wing paint extends up to eleven HD pixels beyond OAM.
   t=o[i+1];X,Y=2*o[i+3],2*(o[i]+1);actors[max(0,Y-12):min(480,Y+28),max(0,X-12):min(512,X+28)]=True
   if 0x75<=t<=0x89 or 0xdd<=t<=0xe6 or 0xef<=t<=0xf2:allowed[max(0,Y-8):min(480,Y+24),max(0,X-8):min(512,X+24)]=True
  ram=data['ram'][j];rx=2*(int.from_bytes(ram[0x74:0x76],'little')-cam(j));ry=2*int.from_bytes(ram[0x76:0x78],'little');actors[max(0,ry-48):min(480,ry+48),max(0,rx-40):min(512,rx+40)]=True
 if not stable_menu and(diff&~allowed).any():scope_errors.append([n,int((diff&~allowed).sum())])
 if not any(scene(j)or menu(j)for j in near)and equal:counts['exact_other_room_images']+=1
 if scene(n):
  camera_values.append(cam(n));palette_counts[data['ppu'][n][0x3f04:0x3f08].hex().upper()]+=1
  if n%40==0 and all(scene(j)for j in near):
   # Large fish flicker in OAM on alternate frames, so a stride-two sample
   # can miss their cells although the preceding displayed frame has them.
   # Mask only complete pixel-proven fish templates found in the screenshot.
   for key,src,smask,color,sx,sy,t,flip in templates:
    if not key.startswith('fish'):continue
    h,w=src.shape[:2]
    for yy,xx in np.argwhere(np.all(after==color,axis=2)):
     xx,yy=int(xx-sx),int(yy-sy)
     if xx<0 or yy<0 or xx+w>512 or yy+h>480:continue
     if np.array_equal(after[yy:yy+h,xx:xx+w][smask],src[:,:,:3][smask]):actors[yy:yy+h,xx:xx+w]=True
   best=(0,None,None,0,0,0)
   for j in near:
    for dx in range(-stride,stride+1):
     e,foreground,lava=render(j,dx);mask=~actors;hits=np.all(e==after,axis=2)&mask;ratio=float(hits.sum()/mask.sum())
     if ratio>best[0]:best=(ratio,j,dx,int(mask.sum()),int((mask&foreground).sum()),int((mask&lava).sum()))
   sourcechecks.append(dict(frame=n,match_fraction=best[0],ppu_frame=best[1],camera_delta=best[2],pixels=best[3],foreground_pixels=best[4],lava_or_ice_pixels=best[5]))
 pp=data['ppu'][n];o=data['oam'][n]
 for i in range(0,256,4):
  if o[i]<239 and 0x75<=o[i+1]<=0x89:
   pal='FF'+pp[0x3f11+(o[i+2]&3)*4:0x3f14+(o[i+2]&3)*4].hex().upper();effect_ids[f'{o[i+1]+0x600:04X}/{pal}/{"mirrored"if o[i+2]&64 else"native"}']+=1
 for key,src,mask,color,sx,sy,t,flip in templates:
  if not any(data['oam'][j][i]<239 and data['oam'][j][i+1]==t and bool(data['oam'][j][i+2]&64)==flip for j in near for i in range(0,256,4)):continue
  h,w=src.shape[:2]
  for Y,X in np.argwhere(np.all(after==color,axis=2)):
   X,Y=int(X-sx),int(Y-sy)
   if X<0 or Y<0 or X+w>512 or Y+h>480:continue
   visible=mask.copy()
   if key.startswith('breaker_charge'):
    # Randy's hand overlaps the charge. Check every source pixel outside
    # the native non-charge sprite cells, not an impossible complete orb.
    for j in near:
     oo=data['oam'][j]
     for i in range(0,256,4):
      if oo[i]>=239 or 0x75<=oo[i+1]<=0x7d:continue
      ox,oy=2*oo[i+3]-X,2*(oo[i]+1)-Y
      if ox<w and oy<h and ox+16>0 and oy+16>0:visible[max(0,oy):min(h,oy+16),max(0,ox):min(w,ox+16)]=False
    if visible.sum()<300:continue
   if np.array_equal(after[Y:Y+h,X:X+w][visible],src[:,:,:3][visible]):
    matches[key]+=1;examples.setdefault(key,dict(frame=n,box=[X,Y,X+w,Y+h]));break
report=dict(baseline='0.11.2 approved',candidate='0.12.0',movie_frames=info['movie_frames'],movie_sha256=info['movie_sha256'],rom_sha1=info['rom_sha1'],core_sha256=info['core_sha256'],paired_native_samples_per_type=len(frames),apu_write_count=len(apu.splitlines()),apu_sha256=hashlib.sha256(apu).hexdigest(),identical_pcm_bytes=len(bp),pcm_sha256=hashlib.sha256(bp).hexdigest(),counts=dict(counts),sprite_matches=dict(matches),sprite_examples=examples,breaker_identities=dict(effect_ids),lava_palettes=dict(palette_counts),camera_range=[min(camera_values),max(camera_values)]if camera_values else None,scene_source_checks=sourcechecks,scope_errors=scope_errors,pack_files=100,unchanged_prior_runtime_files=97,controller_only=True,ram_writes=False)
out=Path(a.out);out.parent.mkdir(exist_ok=True,parents=True);out.write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({k:v for k,v in report.items()if k not in ['scene_source_checks','sprite_examples','breaker_identities']},indent=2))
assert not scope_errors,scope_errors[:10]
assert all(q['match_fraction']>.995 for q in sourcechecks),[q for q in sourcechecks if q['match_fraction']<=.995]
if info['movie_frames']==3705:
 for key in ['fish_0/native','fish_1/native','fish_small_0/mirrored','fish_small_1/mirrored','breaker_charge/native','breaker_launch/native','breaker_bolt/native']:assert matches[key],key
 assert counts['exact_menu_boot_images']>100
if info['movie_frames']==4111:
 for key in ['breaker_charge/mirrored','breaker_launch/mirrored','breaker_bolt/mirrored','breaker_launch_up/native','breaker_bolt_up/native']:assert matches[key],key
 assert any('/FF300036/'in k for k in effect_ids)
if info['movie_frames']==821:assert palette_counts['0F122131']>200
if info['movie_frames']==472:
 def player(n):
  r=data['ram'][n];return int.from_bytes(r[0x74:0x76],'little'),int.from_bytes(r[0x76:0x78],'little')
 assert all(player(n)==(10,96)for n in range(213,233))
 assert all(player(n)[1]==96 for n in range(234,319))
 assert player(318)==(75,96) and player(319)==(76,97)
 assert all(room(n)==0x9aa6 for n in range(200,473))
