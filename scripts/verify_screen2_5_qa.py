"""Pair crimson-cave replays: native behavior/audio, transitions and rendered art."""
from pathlib import Path
from collections import Counter
import argparse,hashlib,json
import numpy as np
from PIL import Image
p=argparse.ArgumentParser()
for k in ['before','after','routes','out']:p.add_argument('--'+k,required=True)
a=p.parse_args();root=Path(__file__).resolve().parents[1]
old=json.loads((root/'evidence/0.7.1-pack-sha256.json').read_text());new=json.loads((root/'evidence/0.8.0-pack-sha256.json').read_text())
routes=json.loads(Path(a.routes).read_text())
assert sorted(k for k in old if old[k]!=new[k])==['README.txt','hires.txt']
assert sorted(set(new)-set(old))==['Stage2_Crimson_Cave_Background.png','Stage2_Crimson_Cave_Tiles_2x.png']
bg=np.array(Image.open(root/'build/Holy_Diver_(Tr)/Stage2_Crimson_Cave_Background.png').convert('RGB'))
sources=[('bat_folded',root/'art/screen2_2/bat_folded.png',0xb0,0),
         ('bat_open',root/'art/screen2_2/bat_open.png',0xa6,0),
         ('eye',root/'art/screen2_3/eye_registered.png',0xd8,1),
         ('tear_DC',root/'art/screen2_3/eye_shot_02DC.png',0xdc,2),
         ('tear_DD',root/'art/screen2_3/eye_shot_02DD.png',0xdd,2)]
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
report=dict(baseline='0.7.1',candidate='0.8.0',emulator='MesenCE 2.2.1',controller_only=True,ram_writes=False,capture_stride=2,cases={})
for case,route in routes.items():
 b,c=Path(a.before)/case,Path(a.after)/case;frames=route['frames']
 assert (b/'completed.txt').read_text()==(c/'completed.txt').read_text()==str(frames)
 assert (b/'input.json').read_bytes()==(c/'input.json').read_bytes()
 inputs=json.loads((c/'input.json').read_text())
 assert inputs['state_sha256']=='8a67bbf57e6d756e36f4f6f42934d27b40c6266d95f6fc24118244c89e53ee40'
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
  room=f'{ram[0x72]:02X}/'+ram[0x78:0x7a].hex().upper();rooms[room]+=1;target=room=='10/9D8D'
  if before.max()==0:assert after.max()==0,(case,n,'blackout');black+=1
  neighbors=[j for j in [n-2,n,n+2]if 2<=j<=frames]
  if not target and all((c/f'dumps/{j:04}.ram').read_bytes()[0x78:0x7a]!=bytes.fromhex('9d8d') for j in neighbors):
   assert equal,(case,n,'outside crimson cave');outside+=1
  if case=='menu' and 420<=n<=530:
   assert equal,(case,n,'menu');menu+=1
  if not target:continue
  palettes[ppu[0x3f08:0x3f10].hex().upper()]+=1
  if n>350:scrolls.append(int.from_bytes(ram[0x60:0x62],'little'))
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
   assert count>10000,(case,n,'panorama source mismatch',count,sorted(offsets))
   panorama+=1
  if n%20==0:
   sprites(after,[(c/f'dumps/{j:04}.oam').read_bytes() for j in neighbors],case,n)
   # Inventory the native identities in the two active horizontal nametables.
   for base in [0x2000,0x2400]:
    for t in ppu[base:base+960]:identities[f'{t+0x300:04X}']+=1
 report['cases'][case]=dict(frames=frames,**inputs,identical_samples_per_memory_type=frames//2,
  apu_sha256=hashlib.sha256(apu).hexdigest(),identical_pcm_bytes=common,shutdown_tail_bytes=tail,
  exact_black_images=black,exact_outside_room_images=outside,exact_menu_images=menu,
  changed_images=changed,exact_images=exact,exact_panorama_images=panorama,
  rooms=dict(rooms),native_palettes=dict(palettes),native_background_identities=dict(identities),
  ram_scroll_range_including_transition_values=[min(scrolls),max(scrolls)] if scrolls else None)
for required in ['bat_folded/native','eye/native','tear_DC/native']:
 assert matches[required]>0,('missing complete live sprite match',required)
report.update(total_frames_per_build=sum(r['frames']for r in routes.values()),
 native_samples_per_type=sum(r['frames']//2 for r in routes.values()),
 exact_black_images=sum(r['exact_black_images']for r in report['cases'].values()),
 exact_outside_room_images=sum(r['exact_outside_room_images']for r in report['cases'].values()),
 exact_panorama_images=sum(r['exact_panorama_images']for r in report['cases'].values()),
 complete_sprite_matches=dict(matches),sprite_examples=examples,unchanged_prior_runtime_files=84,pack_files=88)
out=Path(a.out);out.parent.mkdir(parents=True,exist_ok=True);out.write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({k:v for k,v in report.items()if k not in ['cases','sprite_examples']},indent=2))
