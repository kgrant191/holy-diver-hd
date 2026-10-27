"""Pair actual replays; require native/audio equality and local join/item changes."""
from pathlib import Path
from collections import Counter
import argparse,hashlib,json,wave
import numpy as np
from PIL import Image
p=argparse.ArgumentParser()
for k in ['before','after','out']:p.add_argument('--'+k,required=True)
a=p.parse_args();r=Path(__file__).resolve().parents[1];before,after=Path(a.before),Path(a.after)
bi,ai=[json.loads((d/'result.json').read_text())for d in [before,after]]
for k in ['movie_sha256','rom_sha1','core_sha256','movie_frames','captured_frames','stride']:assert bi[k]==ai[k],k
assert bi['movie_completed']and ai['movie_completed']and ai['stride']==1
for d,v in [(before,'0.20.2'),(after,'0.20.3')]:assert json.loads((d/'installed_pack.json').read_text())==json.loads((r/f'evidence/{v}-pack-sha256.json').read_text())
frames=sorted(int(p.stem)for p in (after/'frames').glob('*.png'));data={k:{}for k in ['ram','ppu','oam','view']}
for n in frames:
 for k in data:
  name=f'{n:06}'+('.json'if k=='view'else'.bin');raw=(after/k/name).read_bytes();assert raw==(before/k/name).read_bytes(),(n,k);data[k][n]=json.loads(raw)if k=='view'else raw
apu=(before/'apu.tsv').read_bytes();assert apu==(after/'apu.tsv').read_bytes()
with wave.open(str(before/'full.wav'),'rb')as f:pcm=f.readframes(f.getnframes());params=f.getparams()
with wave.open(str(after/'full.wav'),'rb')as f:assert f.getparams()==params;assert f.readframes(f.getnframes())==pcm
trunk=[[0x3f,0x40,0x47,0x48],[0x41,0x42,0x49,0x4a],[0x43,0x44,0x4b,0x4c],[0x4f,0x50,0x51,0x52]];columns={t:x for row in trunk for x,t in enumerate(row)}
jug_patterns={bytes.fromhex(v)for v in json.loads((r/'art/screen2_5_review/native_jug.json').read_text())['patterns'].values()}
def allowed(n):
 mask=np.zeros((480,512),bool);jug=False
 for j in [n-1,n,n+1]:
  if j not in data['ram']:continue
  ram,pp,v,o=[data[k][j]for k in ['ram','ppu','view','oam']]
  if ram[0x72]==4 and ram[0x78:0x7a]==b'\xc2\x84':
   vv=v['vram'];sx=(vv&31)*8+v['xscroll']+(256 if vv&0x400 else 0);sy=((vv>>5)&31)*8+((vv>>12)&7)+(240 if vv&0x800 else 0)
   def cell(x,y):return pp[0x2000+x//32%2*0x400+y//30%2*0x800+(y%30)*32+x%32]
   for y in range(sy//8,(sy+239)//8+1):
    for x in range(sx//8,(sx+255)//8+1):
     t=cell(x,y)
     if t not in columns:continue
     col=columns[t];ok=any(cell(x-col-1,y+dy)==0x4e for dy in [-1,0,1])if col<2 else any(cell(x+4-col,y+dy)==0x5b for dy in [-1,0,1])
     if ok:
      X,Y=(x*8-sx)*2,(y*8-sy)*2;mask[max(0,Y-4):min(480,Y+20),max(0,X-4):min(512,X+20)]=True
  for k in range(0,256,4):
   y,t,at,x=o[k:k+4]
   if y>=239 or pp[t*16:(t+1)*16]not in jug_patterns:continue
   if pp[0x3f11+(at&3)*4:0x3f14+(at&3)*4]!=b'\x30\x11\x16':continue
   jug=True;X,Y=x*2,(y+1)*2;mask[max(0,Y-2):min(480,Y+18),max(0,X-2):min(512,X+18)]=True
 return mask,jug
counts=Counter();rooms=Counter();pixels=0
for n in frames:
 paths=[d/'frames'/f'{n:06}.png'for d in [before,after]]
 if not all(p.stat().st_size for p in paths):assert paths[0].stat().st_size==paths[1].stat().st_size;counts['empty_initial']+=1;continue
 old,new=[np.array(Image.open(p).convert('RGB'))for p in paths];diff=np.any(old!=new,2)
 if diff.any():
  mask,jug=allowed(n);assert not (diff&~mask).any(),(n,'outside joins/jug',int((diff&~mask).sum()))
  counts['changed']+=1;pixels+=int(diff.sum());rooms[data['ram'][n][0x78:0x7a][::-1].hex().upper()]+=1
  if jug:counts['jug_observed']+=1
 else:counts['identical']+=1
 if not old.any():assert not new.any();counts['native_black_exact']+=1
report=dict(movie_frames=ai['movie_frames'],native_samples_per_type=len(frames),native_exact=True,apu_exact=True,pcm_exact=True,pcm_bytes=len(pcm),pcm_sha256=hashlib.sha256(pcm).hexdigest(),movie_sha256=ai['movie_sha256'],image_checks=counts,changed_rooms=rooms,changed_pixels=pixels,changes_confined_to_branch_shoulders_and_jug=True)
Path(a.out).write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
