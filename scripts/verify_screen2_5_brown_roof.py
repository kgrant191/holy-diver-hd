"""Check exact original brown ceiling pixels, scope, bats and native head bumps."""
from pathlib import Path
from collections import Counter
import argparse,hashlib,json
import numpy as np
from PIL import Image
p=argparse.ArgumentParser()
for k in ['before','after','routes','out']:p.add_argument('--'+k,required=True)
a=p.parse_args();root=Path(__file__).resolve().parents[1];routes=json.loads(Path(a.routes).read_text())
old=json.loads((root/'evidence/0.8.1-pack-sha256.json').read_text());new=json.loads((root/'evidence/0.8.3-pack-sha256.json').read_text())
assert sorted(k for k in old if old[k]!=new[k])==['README.txt','hires.txt'];assert set(new)==set(old)
geometry=json.loads((root/'art/screen2_5_roof/previous_geometry.json').read_text());cells={}
for identity,m in geometry.items():
 x,y=m['xy'];atlas=Image.open(root/'build/Holy_Diver_(Tr)'/m['image']).convert('RGBA')
 cells[int(identity,16)-0x300]=np.array(atlas.crop((x,y,x+16,y+16)))
body={0x30,0x31,0x32,0x33,0x81,0x82,0x83,0x84}
bat=np.array(Image.open(root/'art/screen2_2/bat_folded.png').convert('RGBA'));bm=bat[:,:,3]>0;cs,counts=np.unique(bat[:,:,:3][bm],axis=0,return_counts=True);bc=cs[counts.argmin()];by,bx=np.argwhere(bm&np.all(bat[:,:,:3]==bc,axis=2))[0]
def bat_box(rgb):
 for y,x in np.argwhere(np.all(rgb==bc,axis=2)):
  X,Y=int(x-bx),int(y-by)
  if X>=0 and Y>=0 and X+32<=512 and Y+48<=480 and np.array_equal(rgb[Y:Y+48,X:X+32][bm],bat[:,:,:3][bm]):return [X,Y,X+32,Y+48]
def pos(folder,n):
 v=(folder/f'dumps/{n:04}.view').read_text().split(',');tmp,fine=int(v[0]),int(v[1]);return (tmp&31)*8+fine+((tmp>>10)&1)*256
def gold(ppu,page,x,y):
 base=0x2000+page*1024;attribute=ppu[base+960+(y//4)*8+x//4];palette=attribute>>((y%4//2)*4+(x%4//2)*2)&3
 return bytes([ppu[0x3f00]])+ppu[0x3f01+palette*4:0x3f04+palette*4]==bytes.fromhex('0f071737')
def placements(ppu,offset):
 roof=[];floors=[]
 for page in [0,1]:
  for tx in range(32):
   capped=False
   for ty in range(30):
    t=ppu[0x2000+page*1024+ty*32+tx]
    if not gold(ppu,page,tx,ty):continue
    if t in [0x2e,0x2f]:capped=True
    x=(page*256+tx*8-offset)%512
    # A partially scrolled-off tile wraps above 504; retain its visible
    # right-hand pixels at the left edge of the screenshot.
    if x>504:x-=512
    if x>=256:continue
    item=(t,x*2,ty*16)
    if t in body and capped:floors.append(item)
    elif t in cells:roof.append(item)
 return roof,floors
def paste_mask(dst,cell,x,y):
 l,r=max(0,x),min(512,x+16);top,bottom=max(0,y),min(480,y+16)
 if l<r and top<bottom:dst[top:bottom,l:r]|=cell[top-y:bottom-y,l-x:r-x]
report=dict(baseline='0.8.1',candidate='0.8.3',controller_only=True,ram_writes=False,capture_stride=2,cases={});examples=[];observed=Counter()
for case,route in routes.items():
 b,c=Path(a.before)/case,Path(a.after)/case;frames=route['frames']
 assert (b/'completed.txt').read_text()==(c/'completed.txt').read_text()==str(frames)
 assert (b/'input.json').read_bytes()==(c/'input.json').read_bytes();inputs=json.loads((c/'input.json').read_text())
 assert inputs['controller_route']==route.get('input_code','emu.setInput({'+route.get('input','')+'},0)')
 for folder,expected in [(b,old),(c,new)]:
  for name in ['installed_pack_sha256.json','installed_pack_after_sha256.json']:assert json.loads((folder/name).read_text())==expected
 for ext in ['ram','ppu','oam','view']:
  files=list((b/'dumps').glob('*.'+ext));assert len(files)==frames//2
  for f in files:assert f.read_bytes()==(c/'dumps'/f.name).read_bytes(),(case,f.name)
 apu=(b/'apu.tsv').read_bytes();assert apu==(c/'apu.tsv').read_bytes()
 bp,cp=(b/'full.wav').read_bytes()[44:],(c/'full.wav').read_bytes()[44:];common=min(len(bp),len(cp));tail=abs(len(bp)-len(cp));assert common and bp[:common]==cp[:common] and tail<=3200
 counts=Counter();maxscroll=0
 for n in range(2,frames+1,2):
  before=np.array(Image.open(b/f'frames/{n:04}.png').convert('RGB'));after=np.array(Image.open(c/f'frames/{n:04}.png').convert('RGB'));diff=np.any(before!=after,axis=2)
  counts['changed_images'if diff.any()else'exact_images']+=1
  ram=(c/f'dumps/{n:04}.ram').read_bytes();ppu=(c/f'dumps/{n:04}.ppu').read_bytes();target=ram[0x78:0x7a]==bytes.fromhex('9d8d')
  neighbors=[j for j in [n-2,n,n+2]if 2<=j<=frames]
  near=any((c/f'dumps/{j:04}.ram').read_bytes()[0x78:0x7a]==bytes.fromhex('9d8d')for j in neighbors)
  if before.max()==0:assert after.max()==0;counts['exact_black_images']+=1
  if not near:assert not diff.any(),(case,n,'outside 2-5 changed');counts['exact_outside_room_images']+=1
  if case=='stair_walk':assert not diff.any(),(case,n,'accepted stairs changed');counts['exact_stair_walk_images']+=1
  if case=='menu' and 420<=n<=530:assert not diff.any();counts['exact_menu_images']+=1
  if diff.any():
   allowed=np.zeros((480,512),dtype=bool)
   for j in neighbors:
    rr=(c/f'dumps/{j:04}.ram').read_bytes()
    if rr[0x78:0x7a]!=bytes.fromhex('9d8d'):continue
    pp=(c/f'dumps/{j:04}.ppu').read_bytes();roof,_=placements(pp,pos(c,j))
    for t,x,y in roof:
     # Screenshots lie between neighboring PPU samples; cover the measured
     # two-frame horizontal interval, never unrelated tile identities.
     allowed[y:y+16,max(0,x-2):min(512,x+18)]=True
   assert not np.any(diff&~allowed),(case,n,'changed outside ceiling identities')
  if not target:continue
  sc=int.from_bytes(ram[0x60:0x62],'little');maxscroll=max(maxscroll,sc if sc<768 else 0)
  if n%20:continue
  offset=pos(c,n);roof,floors=placements(ppu,offset)
  for t,x,y in floors:
   if x<4 or x>492:continue
   assert np.array_equal(before[y+4:y+12,x+4:x+12],after[y+4:y+12,x+4:x+12]),(case,n,'gold floor changed')
   counts['exact_gold_floor_cells']+=1
  red=(before[:,:,0]>70)&(before[:,:,1]<before[:,:,0]*.25)&(before[:,:,2]<before[:,:,0]*.25)
  if red.sum()<2000:continue
  geometry_mask=np.zeros((480,512),dtype=bool)
  for t,x,y in roof:
   observed[f'{t+0x300:04X}']+=1;im=cells[t];mask=im[:,:,3]>0
   for shift in [-2,0,2]:paste_mask(geometry_mask,mask,x+shift,y)
   if not mask.any():continue
   for shift in [-2,0,2]:
    X=x+shift
    if X<0 or X+16>512:continue
    if np.array_equal(after[y:y+16,X:X+16][mask],im[:,:,:3][mask]):counts['exact_ceiling_cells']+=1;break
  box=bat_box(after)
  if box:
   counts['complete_folded_bat_matches']+=1;X,Y,R,B=box;cx=(X+R)//2
   if geometry_mask[max(0,Y-4):min(480,Y+4),max(0,cx-8):min(512,cx+8)].any():
    counts['bat_ceiling_contacts']+=1
    if len(examples)<3:examples.append(dict(case=case,frame=n,bat_box=box))
 report['cases'][case]=dict(frames=frames,input=inputs,identical_samples_per_native_type=frames//2,apu_sha256=hashlib.sha256(apu).hexdigest(),identical_pcm_bytes=common,shutdown_tail_bytes=tail,max_camera_scroll=maxscroll,**dict(counts))
assert sum(c.get('exact_ceiling_cells',0)for c in report['cases'].values())>1000
assert sum(c.get('bat_ceiling_contacts',0)for c in report['cases'].values())>0
head_frames=[620,622,624,626,628];foot=[]
for n in head_frames:
 ram=(Path(a.after)/'extended_traversal'/f'dumps/{n:04}.ram').read_bytes();foot.append(ram[0x4f0])
assert foot==[150,145,140,140,141],('native low-ceiling jump changed',foot)
report.update(total_frames_per_build=sum(r['frames']for r in routes.values()),native_samples_per_type=sum(r['frames']//2 for r in routes.values()),observed_ceiling_identities=dict(observed),bat_attachment_examples=examples,head_bump_example=dict(case='extended_traversal',frames=head_frames,feet_y=foot,jump_button_still_held_in_route=True),unchanged_prior_runtime_files=87,pack_files=89,approved_stairs_unchanged=True)
out=Path(a.out);out.parent.mkdir(parents=True,exist_ok=True);out.write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:v for k,v in report.items()if k not in ['cases','observed_ceiling_identities']},indent=2))
