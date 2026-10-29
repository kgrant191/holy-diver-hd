"""Prove changed pixels stay inside the face cells and green enemy OAM union."""
from pathlib import Path
from collections import Counter
import argparse,json,hashlib,wave
import numpy as np
from PIL import Image
from verify_level6_opening_replay import source,matches

def compare(root,before,after):
 infos=[json.loads((d/'result.json').read_text())for d in [before,after]]
 for k in ['movie_sha256','rom_sha1','core_sha256','movie_frames','captured_frames','stride']:assert infos[0][k]==infos[1][k],k
 assert all(i['movie_completed']for i in infos)
 for d,version in [(before,'0.29.0'),(after,'0.29.1')]:assert json.loads((d/'installed_pack.json').read_text())==json.loads((root/f'evidence/{version}-pack-sha256.json').read_text())
 frames=sorted(int(p.stem)for p in(after/'ram').glob('*.bin'));assert frames==list(range(1,4762));data={k:{}for k in ['ram','ppu','oam','view']}
 for n in frames:
  for kind in data:
   name=f'{n:06}'+('.json'if kind=='view'else'.bin');raw=(after/kind/name).read_bytes();assert raw==(before/kind/name).read_bytes(),(n,kind);data[kind][n]=json.loads(raw)if kind=='view'else raw
 apu=(after/'apu.tsv').read_bytes();assert apu==(before/'apu.tsv').read_bytes()
 with wave.open(str(before/'full.wav'))as f:params=f.getparams();pcm=f.readframes(f.getnframes())
 with wave.open(str(after/'full.wav'))as f:assert f.getparams()==params and f.readframes(f.getnframes())==pcm
 return frames,data,dict(movie=infos[1],native_samples_per_type=len(frames),native_exact=True,apu_exact=True,pcm_exact=True,apu_sha256=hashlib.sha256(apu).hexdigest(),pcm_sha256=hashlib.sha256(pcm).hexdigest(),delivered_runtime_exact=True)

def bounds(data,n,face_ids):
 out=np.zeros((480,512),bool)
 # endFrame dumps can lead video submission by one frame. Use only the two
 # measured positions, without a free motion margin or unrelated tile IDs.
 for j in [max(1,n-1),n]:
  ram,pp,o,v=[data[k][j]for k in ['ram','ppu','oam','view']]
  if ram[0x72]!=0x10 or ram[0x78:0x7a]!=bytes.fromhex('AFA3'):continue
  vv=v['vram'];sx=(vv&31)*8+v['xscroll']+(256 if vv&0x400 else 0);sy=((vv>>5)&31)*8+((vv>>12)&7)+(240 if vv&0x800 else 0)
  for yy in range(sy//8,(sy+239)//8+1):
   for xx in range(sx//8,(sx+255)//8+1):
    tx,ty=xx%32,yy%30;nt=0x2000+(xx//32%2)*0x400+(yy//30%2)*0x800;t=0x1b00+pp[nt+ty*32+tx]
    if t not in face_ids:continue
    x,y=(xx*8-sx)*2,(yy*8-sy)*2;out[max(0,y):min(480,y+16),max(0,x):min(512,x+16)]=True
  for k in range(0,256,4):
   y,t,attr,x=o[k:k+4];pal='FF'+pp[0x3f11+(attr&3)*4:0x3f14+(attr&3)*4].hex().upper()
   if y>=239 or not 0x9c<=t<=0xa3 or pal!='FF0A1930':continue
   x,y=x*2,(y+1)*2;out[y:min(480,y+16),x:min(512,x+16)]=True
 return out

def main():
 p=argparse.ArgumentParser()
 for k in ['before','after','out']:p.add_argument('--'+k,required=True)
 a=p.parse_args();root=Path(__file__).resolve().parents[1];b,c=Path(a.before),Path(a.after);frames,data,report=compare(root,b,c)
 reg=json.loads((root/'art/level6_enemy_revision/registration.json').read_text());ids={t for row in reg['face_layout']for t in row}
 sources={name:[source(root/f'art/level6_enemy_revision/{name}.png',mirror)for mirror in [False,True]]for name in ['wall_face','blob_0','blob_1']}
 stats=Counter();hits={};bad=[];menu=np.array(Image.open(b/'frames/000010.png').convert('RGB'))[106:136,60:480]
 for n in frames:
  paths=[d/'frames'/f'{n:06}.png'for d in [b,c]]
  if not all(p.stat().st_size for p in paths):assert paths[0].stat().st_size==paths[1].stat().st_size;stats['empty_initial']+=1;continue
  old,im=[np.array(Image.open(p).convert('RGB'))for p in paths];diff=np.any(old!=im,2)
  if not old.any():assert not im.any();stats['blackouts_exact']+=1
  if np.array_equal(old[106:136,60:480],menu):assert not diff.any(),(n,'menu changed');stats['menus_exact']+=1
  if diff.any():
   stats['changed_frames']+=1;outside=diff&~bounds(data,n,ids)
   if outside.any():bad.append(dict(frame=n,pixels=int(outside.sum()),box=[int(x)for x in [np.where(outside)[1].min(),np.where(outside)[0].min(),np.where(outside)[1].max(),np.where(outside)[0].max()]]))
  else:stats['identical_frames']+=1
  if len(hits)<len(sources):
   for name,ss in sources.items():
    if name in hits:continue
    for mirror,item in enumerate(ss):
     found=matches(im,item)
     if found:hits[name]=dict(frame=n,mirrored=bool(mirror),positions=found);break
 report.update(images=stats,changes_outside_enemy_bounds=bad,all_changes_confined_to_enemies=not bad,live_whole_source_matches=hits,source_names_not_observed=sorted(set(sources)-set(hits)),live_Thunder_or_dragon_flash_coverage=False)
 Path(a.out).write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2));assert not bad,bad[:10];assert set(hits)==set(sources)
if __name__=='__main__':main()
