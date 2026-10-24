"""Paired controller verification of Level 2 boss, Breaker and preserved scenes."""
from pathlib import Path
from collections import Counter
import argparse,hashlib,json
import numpy as np
from PIL import Image
p=argparse.ArgumentParser()
for k in ['before','after','out']:p.add_argument('--'+k,required=True)
a=p.parse_args();root=Path(__file__).resolve().parents[1];old=json.loads((root/'evidence/0.9.0-pack-sha256.json').read_text());new=json.loads((root/'evidence/0.10.0-pack-sha256.json').read_text());routes=json.loads((root/'scripts/boss2_routes.json').read_text())
assert sorted(k for k in old if old[k]!=new[k])==['README.txt','hires.txt']
assert set(new)-set(old)=={'Boss2_Tiles_2x.png','Boss2_Cave_Flash.png','Breaker_Acquired.png'}
wall={f.stem[5:]:np.array(Image.open(f).convert('RGBA'))for f in (root/'art/boss2').glob('wall_????????.png')}
bg=np.array(Image.open(root/'build/Holy_Diver_(Tr)/Stage2_Crimson_Cave_Background.png').convert('RGB'));card=np.array(Image.open(root/'build/Holy_Diver_(Tr)/Breaker_Acquired.png').convert('RGB'))
flash_bg=np.array(Image.open(root/'build/Holy_Diver_(Tr)/Boss2_Cave_Flash.png').convert('RGB'))
templates=[]
for name in ['breaker','fireball']:
 src=np.array(Image.open(root/f'art/boss2/{name}_registered.png').convert('RGBA'));mask=src[:,:,3]>0
 colors,counts=np.unique(src[:,:,:3][mask],axis=0,return_counts=True);eligible=np.flatnonzero(colors.max(axis=1)>=80);color=colors[eligible[counts[eligible].argmin()]];sy,sx=np.argwhere(mask&np.all(src[:,:,:3]==color,axis=2))[0];templates.append((name,src,mask,color,int(sx),int(sy)))
# A bright source-pixel probe avoids scanning every black background pixel.
# Every opaque source pixel is still compared exactly for the final match.
def sprite_matches(rgb):
 found=[]
 for name,src,mask,color,sx,sy in templates:
  for y,x in np.argwhere(np.all(rgb==color,axis=2)):
   X,Y=int(x-sx),int(y-sy)
   if X<0 or Y<0 or X+32>512 or Y+32>480:continue
   if np.array_equal(rgb[Y:Y+32,X:X+32][mask],src[:,:,:3][mask]):found.append(name);break
 return found
def native(b,c,frames,expected_old,expected_new):
 assert(b/'completed.txt').read_text()==(c/'completed.txt').read_text()==str(frames)
 assert(b/'input.json').read_bytes()==(c/'input.json').read_bytes()
 for folder,h in [(b,expected_old),(c,expected_new)]:
  for f in ['installed_pack_sha256.json','installed_pack_after_sha256.json']:assert json.loads((folder/f).read_text())==h,(folder,f)
 for ext in ['ram','ppu','oam','view']:
  files=list((b/'dumps').glob('*.'+ext));assert len(files)==frames//2
  for f in files:assert f.read_bytes()==(c/'dumps'/f.name).read_bytes(),(b.name,f.name)
 apu=(b/'apu.tsv').read_bytes();assert apu==(c/'apu.tsv').read_bytes()
 bp,cp=(b/'full.wav').read_bytes()[44:],(c/'full.wav').read_bytes()[44:];common=min(len(bp),len(cp));tail=abs(len(bp)-len(cp));assert common and bp[:common]==cp[:common]and tail<=3200,(b.name,'PCM',tail)
 return dict(frames=frames,samples_per_native_type=frames//2,apu_sha256=hashlib.sha256(apu).hexdigest(),identical_common_pcm_bytes=common,shutdown_tail_bytes=tail)
report=dict(baseline='0.9.0',candidate='0.10.0',controller_only=True,ram_writes=False,emulator='MesenCE 2.2.1',capture_stride=2,cases={});matches=Counter();examples={};wall_matches=Counter();full_wall_matches=0
for case,route in routes.items():
 b,c=Path(a.before)/case,Path(a.after)/case;frames=route['frames'];r=native(b,c,frames,old,new);r['input']=json.loads((c/'input.json').read_text());assert r['input']['state_sha256']=='3dc10e1f35dda26171678ca6548fc3f974635b6e9face870525398c1a658f7e6';assert r['input']['controller_route']=='emu.setInput({'+route['input']+'},0)'
 black=outside=cards=changed=removed=0;rooms=Counter();palettes=Counter();sprite_palettes=Counter();new_bank_frames=0
 for n in range(2,frames+1,2):
  before=np.array(Image.open(b/f'frames/{n:04}.png').convert('RGB'));after=np.array(Image.open(c/f'frames/{n:04}.png').convert('RGB'));same=np.array_equal(before,after);changed+=int(not same)
  ram=(c/f'dumps/{n:04}.ram').read_bytes();ppu=(c/f'dumps/{n:04}.ppu').read_bytes();room=ram[0x78:0x7a].hex();rooms[room]+=1
  if before.max()==0:assert after.max()==0,(case,n,'native blackout');black+=1
  breaker=all(ppu[addr]==value for addr,value in [(0x21cc,0x21),(0x21cd,0x33),(0x21cf,0x20),(0x21d0,0x2a),(0x21d2,0x33)]) and ppu[0x3f00:0x3f04]==bytes.fromhex('0f213029')
  neighbors=[max(2,n-2),n,min(frames,n+2)]
  if room!='7d8f' and not breaker and all((c/f'dumps/{j:04}.ram').read_bytes()[0x78:0x7a]!=bytes.fromhex('7d8f')for j in neighbors):
   assert same,(case,n,'outside boss / Breaker');outside+=1
  if breaker and n%20==0 and not same:
   assert np.all(after==card,axis=2).sum()>220000,(case,n,'Breaker card source');cards+=1
  if room!='7d8f':continue
  pal=ppu[0x3f0c:0x3f10].hex().upper();palettes[pal]+=1;sprite_palettes[ppu[0x3f1c:0x3f20].hex().upper()]+=1
  # The screenshot precedes the endFrame dump: the native pickup flash can
  # already be reset to 0F in the dump. Verify that phase from exact rendered
  # silhouette AND pale cave pixels, never from an all-black image alone.
  rendered_pal='310F0F0F' if pal=='0F0F0F0F' else pal
  if n%20==0 and rendered_pal in wall:
   src=wall[rendered_pal]
   offsets=[]
   for j in neighbors:
    vals=(c/f'dumps/{j:04}.view').read_text().split(',');tmp,fine=int(vals[0]),int(vals[1]);offsets.append((tmp&31)*8+fine+((tmp>>10)&1)*256)
   positions=set(offsets)
   for start,end in zip(offsets,offsets[1:]):
    if abs(end-start)<=8:positions.update(range(min(start,end),max(start,end)+1))
   for scroll in positions:
    X=2*(208-scroll);Y=64;x0=max(0,X);x1=min(512,X+192)
    if x0>=x1:continue
    crop=src[:,x0-X:x1-X];mask=crop[:,:,3]>0
    if mask.sum()>4000 and np.array_equal(after[Y:Y+256,x0:x1][mask],crop[:,:,:3][mask]):
     flash_pixels=0
     if rendered_pal=='310F0F0F':
      flash_pixels=int((np.all(after[Y:Y+256,x0:x1]==flash_bg[Y:Y+256,2*scroll+x0:2*scroll+x1],axis=2)&~mask).sum())
      if flash_pixels<10000:continue
     wall_matches[rendered_pal]+=1;full_wall_matches+=int(x0==X and x1==X+192);examples.setdefault('wall/'+rendered_pal,dict(case=case,frame=n,scroll=scroll,end_frame_palette=pal,exact_flash_background_pixels=flash_pixels));break
  if n%10==0:
   for name in sprite_matches(after):matches[name]+=1;examples.setdefault(name,dict(case=case,frame=n))
  if case=='victory' and n==1040:
   assert pal=='0F0F0F0F';vals=(c/f'dumps/{n:04}.view').read_text().split(',');tmp,fine=int(vals[0]),int(vals[1]);scroll=(tmp&31)*8+fine+((tmp>>10)&1)*256;X=2*(208-scroll);src=wall['0F121626'][:,:min(192,512-X)];mask=src[:,:,3]>0
   assert np.array_equal(after[64:320,X:X+src.shape[1]][mask],bg[64:320,2*scroll+X:2*scroll+X+src.shape[1]][mask]);removed=int(mask.sum())
 r.update(exact_black_images=black,exact_outside_images=outside,exact_breaker_card_samples=cards,changed_images=changed,boss_removed_source_pixels=removed,rooms=dict(rooms),boss_palettes=dict(palettes),player_palettes=dict(sprite_palettes));report['cases'][case]=r
for pal in ['0F121626','0F270027','310F0F0F']:assert wall_matches[pal]>0,('missing whole visible boss',pal)
assert full_wall_matches>0
for name in ['breaker','fireball']:assert matches[name]>0,('missing sprite',name)
reg={};reg_routes=json.loads((root/'scripts/boss2_regression_routes.json').read_text())
for case,route in reg_routes.items():
 b=root/'work/screen2_6/after'/case;c=root/'work/boss2/regression_after'/case;frames=route['frames'];r=native(b,c,frames,old,new)
 files=list((b/'frames').glob('*.png'));assert len(files)==frames//2
 for f in files:assert np.array_equal(np.array(Image.open(f)),np.array(Image.open(c/'frames'/f.name))),(case,f.name,'approved 2-6 artwork changed')
 r['exact_images']=len(files);reg[case]=r
report.update(regression=reg,whole_visible_boss_matches=dict(wall_matches),full_unclipped_boss_matches=full_wall_matches,complete_sprite_matches=dict(matches),examples=examples,unchanged_prior_runtime_assets=88,pack_files=93,total_frames_per_build=sum(r['frames']for r in routes.values())+sum(r['frames']for r in reg_routes.values()))
out=Path(a.out);out.parent.mkdir(parents=True,exist_ok=True);out.write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:v for k,v in report.items()if k not in ['cases','examples']},indent=2))
