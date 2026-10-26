"""Verify paired native playback and actual Golden Temple source sprites."""
from pathlib import Path
from collections import Counter
import argparse, json, hashlib, wave
import numpy as np
from PIL import Image

p=argparse.ArgumentParser()
for key in ['before','after','out']:p.add_argument('--'+key,required=True)
a=p.parse_args();r=Path(__file__).resolve().parents[1];b,c=Path(a.before),Path(a.after)
bi,ci=[json.loads((f/'result.json').read_text())for f in [b,c]]
for key in ['movie_sha256','rom_sha1','core_sha256','movie_frames','captured_frames','stride']:assert bi[key]==ci[key],key
assert bi['movie_completed'] and ci['movie_completed']
for capture,version in [(b,'0.15.0'),(c,'0.16.0')]:
 assert json.loads((capture/'installed_pack.json').read_text())==json.loads((r/f'evidence/{version}-pack-sha256.json').read_text()),'Incorrect installed pack'
frames=sorted(int(f.stem)for f in(c/'frames').glob('*.png'));rooms=Counter();unchanged=Counter();menus=0;native={}
for n in frames:
 for key in ['ram','ppu','oam','view']:
  name=f'{n:06}'+('.json'if key=='view'else'.bin');raw=(c/key/name).read_bytes();assert raw==(b/key/name).read_bytes(),(n,key)
  if key=='ram':native[n]=raw
apu=(b/'apu.tsv').read_bytes();assert apu==(c/'apu.tsv').read_bytes()
with wave.open(str(b/'full.wav'),'rb')as f:pcm=f.readframes(f.getnframes());params=f.getparams()
with wave.open(str(c/'full.wav'),'rb')as f:assert f.getparams()==params;assert f.readframes(f.getnframes())==pcm
sources={}
for name in ['overdrive_orb','boulder_0','boulder_1','boulder_2','gargoyle_0','gargoyle_1','guardian']:
 im=np.array(Image.open(r/f'art/level4/{name}.png').convert('RGBA'))
 for h in [False,True]:
  for v in [False,True]if name.startswith('boulder')else[False]:
   src=im[:,::-1]if h else im;src=src[::-1]if v else src;mask=src[:,:,3]==255;ys,xs=np.nonzero(mask)
   # Use a rare bright source pixel as an anchor, then compare the whole opaque silhouette.
   j=np.argmax(src[ys,xs,:3].sum(1));sources[f'{name}/h{int(h)}v{int(v)}']=(src,mask,int(ys[j]),int(xs[j]))
hits=Counter();examples={};glyph_checks=Counter()
menu_reference=np.array(Image.open(b/'frames/000160.png').convert('RGB'))[120:160,240:440]
registration=json.loads((r/'art/level4/registration.json').read_text())
atlas=Image.open(r/'art/level4/Golden_Temple_Tiles_2x.png').convert('RGBA');letters={}
for letter in ['O','V']:
 m=next(m for m in registration['mappings']if m['kind']=='Overdrive menu '+letter);x,y=m['xy']
 letters[letter]=np.array(atlas.crop((x,y,x+16,y+16)))
def find(im,src,mask,ay,ax):
 ys,xs=np.where(np.all(im==src[ay,ax,:3],axis=2));hh,ww=src.shape[:2]
 for yy,xx in zip(ys-ay,xs-ax):
  if yy<0 or xx<0 or yy+hh>480 or xx+ww>512:continue
  if np.array_equal(im[yy:yy+hh,xx:xx+ww][mask],src[:,:,:3][mask]):return [int(xx),int(yy)]
 return None
for n in frames:
 bp,cp=[f/'frames'/f'{n:06}.png'for f in [b,c]]
 if not bp.stat().st_size or not cp.stat().st_size:
  assert bp.stat().st_size==cp.stat().st_size;unchanged['empty_initial']+=1;continue
 old,im=[np.array(Image.open(f).convert('RGB'))for f in [bp,cp]]
 room=int.from_bytes(native[n][0x78:0x7a],'little');rooms[f'{room:04X}']+=1;diff=np.any(old!=im,axis=2)
 if not diff.any():unchanged['all']+=1
 if not old.any():assert not im.any();unchanged['black']+=1
 rendered_menu=np.array_equal(old[120:160,240:440],menu_reference)
 if rendered_menu:
  allowed=np.zeros((480,512),bool)
  for x in [240,256,352]:allowed[240:256,x:x+16]=True
  assert not diff[~allowed].any(),('menu scope',n);menus+=1
  for x,letter in [(240,'O'),(256,'V'),(352,'V')]:
   src=letters[letter];mask=(src[:,:,3]==255).copy();visible=np.ones((480,512),bool)
   # Native sprites can persist over the first pause picture, obscuring letters.
   # Exclude only their measured OAM cells in the adjacent capture interval.
   for j in [n-ci['stride'],n,n+ci['stride']]:
    op=c/'oam'/f'{j:06}.bin'
    if not op.exists():continue
    o=op.read_bytes()
    for i in range(0,256,4):
     yy,t,at,xx=o[i:i+4]
     if yy>=239:continue
     X,Y=xx*2,(yy+1)*2;visible[max(0,Y-2):min(480,Y+18),max(0,X-2):min(512,X+18)]=False
   mask&=visible[240:256,x:x+16]
   if np.array_equal(mask,src[:,:,3]==255):glyph_checks['complete_'+letter]+=1
   glyph_checks['visible_pixels']+=int(mask.sum())
   assert np.array_equal(im[240:256,x:x+16][mask],src[:,:,:3][mask]),('complete menu glyph',letter,n)
 elif room not in [0xa865,0xaa09,0xaa81]:
  previous=n-ci['stride'];prior_room=int.from_bytes(native[previous][0x78:0x7a],'little')if previous in native else None
  if diff.any():
   # Native endFrame may advance to the menu before the last play image submits.
   assert prior_room in [0xa865,0xaa09,0xaa81],('outside rooms',n)
   unchanged['rendered_last_play_frame']+=1
  else:unchanged['outside_room']+=1
 if n%20:continue
 for name,args in sources.items():
  pos=find(im,*args)
  if pos is not None:hits[name]+=1;examples.setdefault(name,dict(frame=n,xy=pos))
assert hits,'No complete painted source matched playback'
assert glyph_checks['complete_O'] and glyph_checks['complete_V']
report=dict(native_samples_per_type=len(frames),movie_frames=ci['movie_frames'],movie_sha256=ci['movie_sha256'],rom_sha1=ci['rom_sha1'],core_sha256=ci['core_sha256'],native_types=['RAM','PPU','OAM','PPU view'],native_exact=True,apu_exact=True,pcm_exact=True,pcm_bytes=len(pcm),apu_sha256=hashlib.sha256(apu).hexdigest(),pcm_sha256=hashlib.sha256(pcm).hexdigest(),room_samples=rooms,unchanged=unchanged,menu_samples=menus,menu_changes_confined_to_overdrive=True,complete_sprite_matches=hits,examples=examples)
report['menu_glyph_source_checks']=glyph_checks
Path(a.out).parent.mkdir(parents=True,exist_ok=True);Path(a.out).write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
