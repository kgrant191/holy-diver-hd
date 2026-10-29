"""Compare native execution/audio and inspect actual Level 6 rendered sources."""
from pathlib import Path
from collections import Counter
import argparse,json,hashlib,wave
import numpy as np
from PIL import Image

def source(path,mirror=False):
 src=np.array(Image.open(path).convert('RGBA'))
 if mirror:src=src[:,::-1]
 mask=src[:,:,3]==255;colors,counts=np.unique(src[mask,:3],axis=0,return_counts=True)
 color=colors[np.argmax(colors.sum(1)/(1+counts))];yy,xx=np.where(mask&np.all(src[:,:,:3]==color,2));pts=np.argwhere(mask)
 return src,mask,int(yy[0]),int(xx[0]),pts[np.linspace(0,len(pts)-1,8,dtype=int)]

def matches(im,item):
 src,mask,ay,ax,probes=item;h,w=mask.shape;yy,xx=np.where(np.all(im==src[ay,ax,:3],2));yy-=ay;xx-=ax
 valid=(yy>=0)&(xx>=0)&(yy+h<=480)&(xx+w<=512);yy,xx=yy[valid],xx[valid]
 for py,px in probes:
  valid=np.all(im[yy+py,xx+px]==src[py,px,:3],1);yy,xx=yy[valid],xx[valid]
  if not len(yy):return []
 return [[int(x),int(y)]for y,x in zip(yy,xx)if np.array_equal(im[y:y+h,x:x+w][mask],src[:,:,:3][mask])]

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

def compare_native(root,before,after):
 infos=[json.loads((d/'result.json').read_text())for d in [before,after]]
 for key in ['movie_sha256','rom_sha1','core_sha256','movie_frames','captured_frames','stride']:assert infos[0][key]==infos[1][key],key
 assert all(i['movie_completed']for i in infos)
 assert json.loads((before/'installed_pack.json').read_text())==json.loads((root/'evidence/0.24.0-pack-sha256.json').read_text())
 expected=json.loads((root/'evidence/0.25.0-pack-sha256.json').read_text())
 actual=json.loads((after/'installed_pack.json').read_text())
 # Full movie was captured before the versioned install note was written.
 # The delivered runtime is byte-identical; the edge test uses the final README.
 differences=[k for k in expected if expected[k]!=actual.get(k)]
 assert set(actual)==set(expected)and set(differences)<= {'README.txt'}
 frames=sorted(int(p.stem)for p in(after/'ram').glob('*.bin'));data={k:{}for k in ['ram','ppu','oam','view']}
 for n in frames:
  for kind in data:
   name=f'{n:06}'+('.json'if kind=='view'else'.bin');raw=(after/kind/name).read_bytes()
   assert raw==(before/kind/name).read_bytes(),(n,kind);data[kind][n]=json.loads(raw)if kind=='view'else raw
 apu=(after/'apu.tsv').read_bytes();assert apu==(before/'apu.tsv').read_bytes()
 with wave.open(str(before/'full.wav'))as f:params=f.getparams();pcm=f.readframes(f.getnframes())
 with wave.open(str(after/'full.wav'))as f:assert f.getparams()==params and f.readframes(f.getnframes())==pcm
 return frames,data,dict(movie=infos[1],native_samples_per_type=len(frames),native_exact=True,apu_exact=True,pcm_exact=True,
  apu_sha256=hashlib.sha256(apu).hexdigest(),pcm_sha256=hashlib.sha256(pcm).hexdigest(),
  candidate_installed_manifest_sha256=hashlib.sha256((after/'installed_pack.json').read_bytes()).hexdigest(),
  delivered_runtime_exact=True,delivery_note_only_differences=differences)

def main():
 p=argparse.ArgumentParser()
 for key in ['before','after','out']:p.add_argument('--'+key,required=True)
 a=p.parse_args();root=Path(__file__).resolve().parents[1];b,c=Path(a.before),Path(a.after)
 frames,data,report=compare_native(root,b,c);assert frames==list(range(1,6428))
 pack=c/'mesen_home/HdPacks/Holy_Diver_(Tr)';art=root/'art/level6_opening'
 backgrounds={};flashes={}
 for style in ['Exterior','Interior']:
  bg=np.array(Image.open(pack/f'Final_Citadel_{style}.png').convert('RGB'));backgrounds[style]=variants(bg)
  for phase,color in [('30',[255,254,255]),('31',[194,223,255])]:
   # Stock Mesen premultiplies PNG RGB then adds the retained native color.
   target=(bg.astype(np.uint32)*176//255+np.array(color)*80//256).astype(np.uint8)
   flashes[style,phase]=variants(target)
 paths={n:art/(n+'.png')for n in ['cape_menu','skull','brick','cornice']}
 paths.update({'dragon_'+str(i):root/f'art/level4_dragon/pose_{i}.png'for i in range(3)})
 paths.update({'sentry':root/'art/level5_next/sentry.png','eye':root/'art/screen2_3/eye_registered.png'})
 paths.update({'thunder_'+str(i):root/f'art/level5/thunder_{i}.png'for i in range(3)})
 sources={n:[source(path,m)for m in [False,True]]for n,path in paths.items()};hits={};stats=Counter();rooms=Counter();bgstats={};missing=[];flashhits=[];menu_changes=[];transitions=[]
 menu_reference=np.array(Image.open(b/'frames/002800.png').convert('RGB'))[106:136,60:480]
 submission_transitions=[]
 for n in frames:
  fs=[d/'frames'/f'{n:06}.png'for d in [b,c]]
  if not all(f.stat().st_size for f in fs):assert fs[0].stat().st_size==fs[1].stat().st_size;stats['empty_initial']+=1;continue
  old,im=[np.array(Image.open(f).convert('RGB'))for f in fs];difference=np.any(old!=im,2);stats['changed'if difference.any()else'identical']+=1
  room=f'{int.from_bytes(data["ram"][n][0x78:0x7a],"little"):04X}';rooms[room]+=1
  if not old.any():assert not im.any(),(n,'native blackout');stats['native_black_exact']+=1;continue
  menu=np.array_equal(old[106:136,60:480],menu_reference)
  if menu:
   outside=difference.copy();outside[208:240,144:176]=False;assert not outside.any(),(n,'change outside cape')
   stats['menu_only_cape']+=1
   if difference.any():menu_changes.append(n)
  else:
   style='Interior'if room=='9BB7'else'Exterior';best=0;kind='normal'
   choices=[('normal',backgrounds[style])]+[(phase,flashes[style,phase])for phase in ['30','31']]
   for phase,vs in choices:
    for v in vs:
     count=int(np.all(im==v,2).sum())
     if count>best:best=count;kind=phase
     if best>10000:break
    if best>10000:break
   if best<=10000 and n>1:
    previous_room=f'{int.from_bytes(data["ram"][n-1][0x78:0x7a],"little"):04X}'
    previous_style='Interior'if previous_room=='9BB7'else'Exterior'
    # endFrame RAM can advance before the previously submitted HD image.
    # Accept the outgoing panorama only on this exact room-change frame.
    if previous_room!=room and previous_room in ['9A8B','9BB7','9CA7']:
     for v in backgrounds[previous_style]:
      count=int(np.all(im==v,2).sum())
      if count>10000:
       best=count;kind='normal';style=previous_style
       submission_transitions.append(dict(frame=n,rendered_room=previous_room,ram_room=room,pixels=count));break
   if best>10000:
    bgstats.setdefault(style,[]).append(best)
    if kind!='normal':flashhits.append([n,style,kind,best])
   elif not difference.any():transitions.append(n)
   else:missing.append([n,room,best])
  if n%8==0:
   for name,vs in sources.items():
    if name in hits or (name=='cape_menu')!=menu:continue
    for mirrored,item in enumerate(vs):
     found=matches(im,item)
     if found:hits[name]=dict(frame=n,mirrored=bool(mirrored),positions=found);break
 report.update(images=stats,rooms=rooms,backgrounds={k:dict(samples=len(v),minimum_pixels=min(v))for k,v in bgstats.items()},
  missing_backgrounds=missing,flash_backdrop_checks=flashhits,live_whole_source_matches=hits,
  sources_not_observed_as_complete_unoccluded_units=sorted(set(sources)-set(hits)),
  menu_changed_frames=menu_changes,identical_nonpanorama_transition_frames=transitions,
  outgoing_panorama_on_room_change_frames=submission_transitions)
 Path(a.out).write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps({k:v for k,v in report.items()if k not in ['menu_changed_frames','flash_backdrop_checks','identical_nonpanorama_transition_frames']},indent=2))
 assert not missing,missing[:30]
 assert all(n in hits for n in ['cape_menu','skull','brick','cornice']),hits.keys()
 assert len(flashhits)>20 and len(menu_changes)>100

if __name__=='__main__':main()
