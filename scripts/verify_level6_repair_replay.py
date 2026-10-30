"""Prove native/audio equality and ceiling/1-up-only rendered changes."""
from pathlib import Path
from collections import Counter
import argparse,hashlib,json,wave
import numpy as np
from PIL import Image
from verify_level6_opening_replay import source,matches

p=argparse.ArgumentParser()
for key in ['before','after','out']:p.add_argument('--'+key,required=True)
p.add_argument('--regression',action='store_true');a=p.parse_args()
root=Path(__file__).resolve().parents[1];b,c=Path(a.before),Path(a.after)
infos=[json.loads((d/'result.json').read_text())for d in [b,c]]
for key in ['movie_sha256','rom_sha1','core_sha256','movie_frames','captured_frames','stride']:assert infos[0][key]==infos[1][key],key
assert all(i['movie_completed']for i in infos)
note_differences=[]
for d,version in [(b,'0.25.0'),(c,'0.25.1')]:
 expected=json.loads((root/f'evidence/{version}-pack-sha256.json').read_text());actual=json.loads((d/'installed_pack.json').read_text())
 different=[k for k in expected if expected[k]!=actual.get(k)];assert set(actual)==set(expected)
 if d==b and a.regression:assert set(different)<= {'README.txt'};note_differences=different
 else:assert not different,different
frames=sorted(int(f.stem)for f in(c/'frames').glob('*.png'));native={}
for n in frames:
 native[n]={}
 for kind in ['ram','ppu','oam','view']:
  name=f'{n:06}'+('.json'if kind=='view'else'.bin');raw=(c/kind/name).read_bytes();assert raw==(b/kind/name).read_bytes(),(kind,n)
  native[n][kind]=json.loads(raw)if kind=='view'else raw
apu=(c/'apu.tsv').read_bytes();assert apu==(b/'apu.tsv').read_bytes()
with wave.open(str(b/'full.wav'))as f:params=f.getparams();pcm=f.readframes(f.getnframes())
with wave.open(str(c/'full.wav'))as f:assert f.getparams()==params and f.readframes(f.getnframes())==pcm

unit=np.array(Image.open(root/'art/level6_repair/ceiling_unit.png').convert('RGBA'));unit_source=source(root/'art/level6_repair/ceiling_unit.png')
figurines={pal:np.array(Image.open(root/f'art/screen1_4/one_up_{src}.png').convert('RGBA'))for pal,src in [('FF300036','FF300036'),('FF221136','FF221136'),('FF190927','FF300036')]}
pack=c/'mesen_home/HdPacks/Holy_Diver_(Tr)';ui=np.array(Image.open(pack/'Screen_UI_2x.png').convert('RGBA'));hud_cells={}
for line in (pack/'hires.txt').read_text().splitlines():
 if line.startswith('<tile>21,'):
  fields=line[6:].split(',');tile=int(fields[1],16)
  if 0x1650<=tile<=0x165f and fields[2]=='FF301116':
   x,y=map(int,fields[3:5]);hud_cells[tile&255]=ui[y:y+16,x:x+16]
counts=Counter();ceiling_hits=[];item_hits=[]
def through_hud(src,x,y,frame):
 """Use actual OAM priority and unchanged HUD alpha, including soft edges."""
 out=src[:,:,:3].astype(np.uint32).copy();o=native[frame]['oam'];pp=native[frame]['ppu'];indices={}
 for i in range(0,256,4):
  yy,t,at,xx=o[i:i+4]
  if t in [0x4e,0x4f]and yy<239 and xx*2==x:indices[t]=i//4
 if set(indices)!={0x4e,0x4f}:return None
 for i in range(252,-1,-4):
  yy,t,at,xx=o[i:i+4]
  if yy>=239 or t not in hud_cells or pp[0x3f11+4*(at&3):0x3f14+4*(at&3)]!=bytes.fromhex('301116'):continue
  cell=hud_cells[t]
  if at&0x40:cell=cell[:,::-1]
  if at&0x80:cell=cell[::-1]
  hx,hy=xx*2,(yy+1)*2
  x0,y0=max(x,hx),max(y,hy);x1,y1=min(x+16,hx+16),min(y+32,hy+16)
  if x0>=x1 or y0>=y1:continue
  fg=cell[y0-hy:y1-hy,x0-hx:x1-hx].astype(np.uint32);target=out[y0-y:y1-y,x0-x:x1-x];alpha=fg[:,:,3]
  priority=np.array([i//4<indices[0x4e if row-y<16 else 0x4f]for row in range(y0,y1)])[:,None]
  active=(alpha>0)&priority
  # Mesen HdData::PremultiplyAlpha and HdNesPack::BlendColors.
  blended=fg[:,:,:3]*(alpha[:,:,None]+1)//256+target*(256-alpha[:,:,None])//256
  blended=np.where((alpha==255)[:,:,None],fg[:,:,:3],blended)
  target[active]=blended[active]
 return out.astype(np.uint8)
def scroll(n):
 v=native[n]['view'];vv=v['vram']
 return (vv&31)*8+v['xscroll']+(256 if vv&0x400 else 0),((vv>>5)&31)*8+((vv>>12)&7)+(240 if vv&0x800 else 0)
def ceiling_mask(n):
 sx,sy=scroll(n);pp=native[n]['ppu'];mask=np.zeros((480,512),bool)
 for y in range(sy//8,(sy+239)//8+1):
  for x in range(sx//8,(sx+255)//8+1):
   tx,ty=x%32,y%30;nt=0x2000+(x//32%2)*0x400+(y//30%2)*0x800;t=0x1700+pp[nt+ty*32+tx]
   if t not in range(0x17b4,0x17b8):continue
   palidx=(pp[nt+960+ty//4*8+tx//4]>>((ty%4)//2*4+(tx%4)//2*2))&3
   pal=(bytes([pp[0x3f00]])+pp[0x3f01+4*palidx:0x3f04+4*palidx]).hex().upper();assert pal=='0F061636'
   x0,y0=(x*8-sx)*2,(y*8-sy)*2;mask[max(0,y0):min(480,y0+16),max(0,x0):min(512,x0+16)]=True
 return mask
for n in frames:
 bp,cp=[d/'frames'/f'{n:06}.png'for d in [b,c]]
 if bp.read_bytes()==cp.read_bytes():counts['identical_images']+=1;continue
 before,after=[np.array(Image.open(f).convert('RGB'))for f in [bp,cp]];diff=np.any(before!=after,2)
 if not diff.any():counts['identical_images']+=1;continue
 counts['corrected_images']+=1;ys,xs=np.where(diff);near=[j for j in [n-1,n,n+1]if j in native]
 allowed=np.logical_or.reduce([ceiling_mask(j)for j in near])if ys.max()<64 else np.zeros(diff.shape,bool)
 if not(diff&~allowed).any():
  assert not a.regression,(n,'unexpected ceiling in original recording')
  phases={(-2*scroll(j)[1])%32 for j in near};phase_matches=[]
  for phase in phases:
   if np.array_equal(after[ys,xs],unit[(ys-phase)%32,xs%32,:3]):phase_matches.append(phase)
  assert phase_matches,(n,'ceiling source pixels differ')
  found=matches(after,unit_source)
  ceiling_hits.append(dict(frame=n,changed_pixels=len(xs),source_vertical_phases=phase_matches,complete_source_positions=found))
  counts['ceiling_frames']+=1;continue
 origins=set();occluders=np.zeros(diff.shape,bool)
 for j in near:
  pp=native[j]['ppu'];o=native[j]['oam']
  for i in range(0,256,4):
   y,t,at,x=o[i:i+4];pal='FF'+pp[0x3f11+4*(at&3):0x3f14+4*(at&3)].hex().upper()
   if y<239 and t==0x4e and pal in figurines:
    origins.update((2*x+dx,2*(y+1)+dy,pal,at)for dx in range(-8,9,2)for dy in range(-8,9,2))
   elif y<239 and t not in [0x4e,0x4f]:
    occluders[max(0,2*(y+1)-2):min(480,2*(y+1)+18),max(0,2*x-2):min(512,2*x+18)]=True
 found=None
 for x,y,pal,at in sorted(origins):
  x0,y0=max(0,x),max(0,y);x1,y1=min(512,x+16),min(480,y+32)
  if x0>=x1 or y0>=y1:continue
  allowed=np.zeros(diff.shape,bool);allowed[y0:y1,x0:x1]=True
  if(diff&~allowed).any():continue
  src=figurines[pal]
  if at&0x40:src=src[:,::-1]
  if at&0x80:src=np.concatenate([src[:16][::-1],src[16:][::-1]])
  full_src=src;src=src[y0-y:y1-y,x0-x:x1-x];mask=src[:,:,3]>0;equal=np.all(after[y0:y1,x0:x1]==src[:,:,:3],2);mismatch=mask&~equal
  whole=not mismatch.any();visible_changed=mask&diff[y0:y1,x0:x1]
  overlap=visible_changed.sum()>=30 and not(mismatch&diff[y0:y1,x0:x1]).any()and not(mismatch&~occluders[y0:y1,x0:x1]).any()
  hud=False
  if not(whole or overlap):
   for j in near:
    composite=through_hud(full_src,x,y,j)
    if composite is not None and np.array_equal(after[y0:y1,x0:x1][mask],composite[y0-y:y1-y,x0-x:x1-x][mask]):hud=True;break
  if whole or overlap or hud:
   found=dict(frame=n,palette=pal,origin=[x,y],complete=whole and [x0,y0,x1,y1]==[x,y,x+16,y+32],native_overlap=not whole,hud_alpha_composite=hud);break
 assert found,(n,'outside complete 1-up or native bounds')
 item_hits.append(found);counts['one_up_frames']+=1
events=[dict(frame=n,before=native[prev]['ram'][0x48f],after=native[n]['ram'][0x48f])for prev,n in zip(frames,frames[1:])if native[prev]['ram'][0x48f]!=native[n]['ram'][0x48f]]
if not a.regression:
 assert ceiling_hits and item_hits
 assert any(h['complete_source_positions']for h in ceiling_hits)and any(h['complete']for h in item_hits)
 assert events==[dict(frame=858,before=2,after=3)]
report=dict(movie=infos[1],regression=a.regression,native_samples_per_type=len(frames),native_ram_ppu_oam_scroll_exact=True,
 apu_exact=True,full_pcm_exact=True,apu_sha256=hashlib.sha256(apu).hexdigest(),pcm_sha256=hashlib.sha256(pcm).hexdigest(),
 baseline_note_only_differences=note_differences,images=counts,every_changed_pixel_inside_requested_native_cells=True,
 every_changed_ceiling_pixel_matches_existing_stone=True,complete_one_up_source_matches=sum(h['complete']for h in item_hits),
 life_events=events,ceiling_matches=ceiling_hits,one_up_matches=item_hits)
Path(a.out).write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({k:v for k,v in report.items()if k not in ['ceiling_matches','one_up_matches']},indent=2))
