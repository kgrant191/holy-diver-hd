"""Verify reused Stage 2 artwork, the new dragon, native behavior and prior rooms."""
from pathlib import Path
from collections import Counter
import argparse,hashlib,json
import numpy as np
from PIL import Image
p=argparse.ArgumentParser()
for k in ['before','after','routes','out']:p.add_argument('--'+k,required=True)
a=p.parse_args();root=Path(__file__).resolve().parents[1]
old=json.loads((root/'evidence/0.8.3-pack-sha256.json').read_text());new=json.loads((root/'evidence/0.9.0-pack-sha256.json').read_text())
routes=json.loads(Path(a.routes).read_text())
assert sorted(k for k in old if old[k]!=new[k])==['README.txt','hires.txt']
assert sorted(set(new)-set(old))==['Stage2_Dragon_2x.png']
bg=np.array(Image.open(root/'build/Holy_Diver_(Tr)/Stage2_Crimson_Cave_Background.png').convert('RGB'))
sources=[('bat_folded',root/'art/screen2_2/bat_folded.png',0xb0,0),
         ('bat_open',root/'art/screen2_2/bat_open.png',0xa6,0),
         ('dragon_stride_0',root/'art/screen2_6/dragon_pose_0.png',0xc9,1),
         ('dragon_stride_1',root/'art/screen2_6/dragon_pose_1.png',0xcf,1),
         ('dragon_fireball',root/'art/screen2_6/dragon_fireball.png',0xd6,1)]
templates=[]
for name,path,t,pal in sources:
 src=np.array(Image.open(path).convert('RGBA'))
 for flip in [False,True]:
  im=src[:,::-1] if flip else src;mask=im[:,:,3]>0
  colors,counts=np.unique(im[:,:,:3][mask],axis=0,return_counts=True);color=colors[counts.argmin()]
  sy,sx=np.argwhere(mask & np.all(im[:,:,:3]==color,axis=2))[0]
  templates.append((name+('/mirrored' if flip else '/native'),im,mask,color,int(sx),int(sy),t,pal,flip))
matches=Counter();examples={}
def sprites(rgb,oams,case,n):
 for key,src,mask,color,sx,sy,t,pal,flip in templates:
  if not any(o[i]<239 and o[i+1]==t and o[i+2]&3==pal and bool(o[i+2]&64)==flip for o in oams for i in range(0,256,4)):continue
  h,w=src.shape[:2]
  for y,x in np.argwhere(np.all(rgb==color,axis=2)):
   X,Y=int(x-sx),int(y-sy)
   if X<0 or Y<0 or X+w>512 or Y+h>480:continue
   if np.array_equal(rgb[Y:Y+h,X:X+w][mask],src[:,:,:3][mask]):
    matches[key]+=1;examples.setdefault(key,dict(case=case,frame=n,box=[X,Y,X+w,Y+h]));break
report=dict(baseline='0.8.3',candidate='0.9.0',emulator='MesenCE 2.2.1',controller_only=True,ram_writes=False,capture_stride=2,cases={})
for case,route in routes.items():
 b,c=Path(a.before)/case,Path(a.after)/case;frames=route['frames']
 assert (b/'completed.txt').read_text()==(c/'completed.txt').read_text()==str(frames)
 assert (b/'input.json').read_bytes()==(c/'input.json').read_bytes()
 inputs=json.loads((c/'input.json').read_text())
 assert inputs['state_sha256']=='60945ccab9020ab3fdde2247161a5f119c5ac32d4ec5af3e6385f0aa187df0b2'
 assert inputs['controller_route']==route.get('input_code','emu.setInput({'+route.get('input','')+'},0)')
 for folder,expected in [(b,old),(c,new)]:
  for name in ['installed_pack_sha256.json','installed_pack_after_sha256.json']:assert json.loads((folder/name).read_text())==expected,(case,name)
 for ext in ['ram','ppu','oam','view']:
  files=list((b/'dumps').glob('*.'+ext));assert len(files)==frames//2
  for f in files:assert f.read_bytes()==(c/'dumps'/f.name).read_bytes(),(case,f.name)
 apu=(b/'apu.tsv').read_bytes();assert apu==(c/'apu.tsv').read_bytes()
 bp,cp=(b/'full.wav').read_bytes()[44:],(c/'full.wav').read_bytes()[44:];common=min(len(bp),len(cp));tail=abs(len(bp)-len(cp))
 assert common and bp[:common]==cp[:common] and tail<=3200,(case,'PCM',tail)
 black=outside=menu=changed=exact=panorama=0;rooms=Counter();palettes=Counter();identities=Counter();scrolls=[]
 for n in range(2,frames+1,2):
  ram=(c/f'dumps/{n:04}.ram').read_bytes();ppu=(c/f'dumps/{n:04}.ppu').read_bytes()
  before=np.array(Image.open(b/f'frames/{n:04}.png').convert('RGB'));after=np.array(Image.open(c/f'frames/{n:04}.png').convert('RGB'))
  equal=np.array_equal(before,after);exact+=int(equal);changed+=int(not equal)
  room=f'{ram[0x72]:02X}/'+ram[0x78:0x7a].hex().upper();rooms[room]+=1;target=room=='10/8D8E'
  if before.max()==0:assert after.max()==0,(case,n,'blackout');black+=1
  neighbors=[j for j in [n-2,n,n+2]if 2<=j<=frames]
  if not target and all((c/f'dumps/{j:04}.ram').read_bytes()[0x78:0x7a]!=bytes.fromhex('8d8e') for j in neighbors):
   assert equal,(case,n,'outside crimson cave');outside+=1
  if case=='menu' and 40<=n<=170:
   assert equal,(case,n,'menu');menu+=1
  if not target:continue
  palettes[ppu[0x3f08:0x3f10].hex().upper()]+=1
  if int.from_bytes(ram[0x60:0x62],'little')<768:scrolls.append(int.from_bytes(ram[0x60:0x62],'little'))
  # Full-color native red scenery distinguishes ordinary rendering from
  # native death grayscale/disabled-background frames with unchanged palette RAM.
  red=(before[:,:,0]>70)&(before[:,:,1]<before[:,:,0]*.25)&(before[:,:,2]<before[:,:,0]*.25)
  if n%20==0 and ppu[0x3f08:0x3f0c]==bytes.fromhex('0f061626') and red.sum()>2000:
   positions=[]
   for j in [max(2,n-2),n]:
    view=(c/f'dumps/{j:04}.view').read_text().split(',');tmp,fine=int(view[0]),int(view[1])
    positions.append((tmp&31)*8+fine+((tmp>>10)&1)*256)
   # The screenshot falls between the two sampled endFrame PPU positions.
   # Test only the integer positions traversed during that two-frame interval.
   delta=(positions[1]-positions[0]+256)%512-256
   offsets={2*q%1024 for q in positions}
   if abs(delta)<=8:
    offsets.update(2*(positions[0]+d)%1024 for d in range(min(0,delta),max(0,delta)+1))
   count=max(int(np.all(after==bg[:,x:x+512],axis=2).sum()) for x in offsets)
   assert count>min(10000,int(red.sum())),(case,n,'panorama source mismatch',count,sorted(offsets))
   panorama+=1
  if n%10==0:
   sprites(after,[(c/f'dumps/{j:04}.oam').read_bytes() for j in neighbors],case,n)
   # Inventory the native identities in the two active horizontal nametables.
   for base in [0x2000,0x2400]:
    for t in ppu[base:base+960]:identities[f'{t+0x300:04X}']+=1
  else:
   # The rightward shot survives only a few two-frame samples. At frame
   # 360 it overlaps another effect by one pixel; 364/366 show it whole.
   # Inspect every observed projectile sample instead of skipping this
   # short-lived native direction with the ordinary ten-frame stride.
   oams=[(c/f'dumps/{j:04}.oam').read_bytes() for j in neighbors]
   if any(o[i]<239 and o[i+1]==0xd6 and o[i+2]&3==1 for o in oams for i in range(0,256,4)):
    sprites(after,oams,case,n)
 report['cases'][case]=dict(frames=frames,**inputs,identical_samples_per_memory_type=frames//2,
  apu_sha256=hashlib.sha256(apu).hexdigest(),identical_pcm_bytes=common,shutdown_tail_bytes=tail,
  exact_black_images=black,exact_outside_room_images=outside,exact_menu_images=menu,
  changed_images=changed,exact_images=exact,exact_panorama_images=panorama,
  rooms=dict(rooms),native_palettes=dict(palettes),native_background_identities=dict(identities),
  ram_scroll_range_including_transition_values=[min(scrolls),max(scrolls)] if scrolls else None)
for required in ['bat_folded/native','bat_open/native','dragon_stride_0/native','dragon_stride_1/native','dragon_stride_0/mirrored','dragon_stride_1/mirrored','dragon_fireball/native','dragon_fireball/mirrored']:
 assert matches[required]>0,('missing complete live sprite match',required)
report.update(total_frames_per_build=sum(r['frames']for r in routes.values()),
 native_samples_per_type=sum(r['frames']//2 for r in routes.values()),
 exact_black_images=sum(r['exact_black_images']for r in report['cases'].values()),
 exact_outside_room_images=sum(r['exact_outside_room_images']for r in report['cases'].values()),
 exact_panorama_images=sum(r['exact_panorama_images']for r in report['cases'].values()),
 complete_sprite_matches=dict(matches),sprite_examples=examples,unchanged_prior_runtime_files=87,pack_files=90)
reg_before=root/'work/screen2_5_brown_roof/after';reg_after=root/'work/screen2_6/regression_after'
reg_routes=json.loads((root/'scripts/screen2_6_regression_routes.json').read_text());regression={}
figurine=np.array(Image.open(root/'art/screen1_4/one_up_FF300036.png').convert('RGBA'))
for case,route in reg_routes.items():
 b,c=reg_before/case,reg_after/case;frames=route['frames']
 assert (b/'completed.txt').read_text()==(c/'completed.txt').read_text()==str(frames)
 assert (b/'input.json').read_bytes()==(c/'input.json').read_bytes()
 for folder,expected in [(b,old),(c,new)]:
  for name in ['installed_pack_sha256.json','installed_pack_after_sha256.json']:assert json.loads((folder/name).read_text())==expected
 for ext in ['ram','ppu','oam','view']:
  files=list((b/'dumps').glob('*.'+ext));assert len(files)==frames//2
  for f in files:assert f.read_bytes()==(c/'dumps'/f.name).read_bytes(),(case,f.name)
 assert (b/'apu.tsv').read_bytes()==(c/'apu.tsv').read_bytes()
 bp,cp=(b/'full.wav').read_bytes()[44:],(c/'full.wav').read_bytes()[44:];common=min(len(bp),len(cp));tail=abs(len(bp)-len(cp))
 assert bp[:common]==cp[:common]and tail<=3200
 files=list((b/'frames').glob('*.png'));assert len(files)==frames//2
 exact=items=0
 for f in files:
  before=np.array(Image.open(f).convert('RGB'));after=np.array(Image.open(c/'frames'/f.name).convert('RGB'))
  difference=np.any(before!=after,axis=2)
  if not difference.any():exact+=1;continue
  # Shared item rules also finish a previously native 1-up over the 2-5
  # lava fall. Require the unchanged approved figurine's actual pixels,
  # native OAM footprint/palette and exact scenery everywhere outside it.
  n=int(f.stem);origins=set()
  for j in [max(2,n-2),n]:
   o=(c/f'dumps/{j:04}.oam').read_bytes();ppu=(c/f'dumps/{j:04}.ppu').read_bytes()
   if ppu[0x3f1d:0x3f20]!=bytes.fromhex('300036'):continue
   for i in range(0,256,4):
    if o[i]<239 and o[i+1]==0x4e and o[i+2]==3:
     # Actual screenshot is between the neighboring two-frame samples;
     # this route advances at most two native pixels per frame.
     origins.update((2*o[i+3]+dx,2*(o[i]+1))for dx in range(-8,9,2))
  valid=False
  for x,y in origins:
   x0,y0=max(0,x),max(0,y);x1,y1=min(512,x+16),min(480,y+32)
   if x0>=x1 or y0>=y1:continue
   allowed=np.zeros(difference.shape,dtype=bool);allowed[y0:y1,x0:x1]=True
   if (difference&~allowed).any():continue
   src=figurine[y0-y:y1-y,x0-x:x1-x];mask=src[:,:,3]>0
   if np.array_equal(after[y0:y1,x0:x1][mask],src[:,:,:3][mask]):valid=True;break
  assert valid,(case,f.name,'change outside newly shared 1-up')
  items+=1
 regression[case]=dict(frames=frames,exact_images=exact,shared_one_up_images=items,identical_samples_per_native_type=frames//2,identical_pcm_bytes=common,shutdown_tail_bytes=tail)
assert regression['stair_walk']['exact_images']==300
assert regression['extended_traversal']['shared_one_up_images']==59
report['prior_rooms_regression']=regression
report['total_including_regression']=sum(r['frames']for r in routes.values())+sum(r['frames']for r in reg_routes.values())
report['shared_fallback_rules']=json.loads((root/'art/shared_stage2/registration.json').read_text())['tile_rules']
out=Path(a.out);out.parent.mkdir(parents=True,exist_ok=True);out.write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({k:v for k,v in report.items()if k not in ['cases','sprite_examples']},indent=2))
