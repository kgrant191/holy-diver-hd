"""Verify consecutive finale footage against the full paired run and source art."""
from pathlib import Path
import argparse,json,wave,hashlib
import numpy as np
from PIL import Image
p=argparse.ArgumentParser()
for key in ['full','capture','out']:p.add_argument('--'+key,required=True)
a=p.parse_args();full,capture=Path(a.full),Path(a.capture)
info=json.loads((capture/'result.json').read_text());other=json.loads((full/'result.json').read_text());assert info['movie_completed']
for key in ['movie_sha256','rom_sha1','core_sha256','movie_frames']:assert info[key]==other[key]
assert (capture/'installed_pack.json').read_bytes()==(full/'installed_pack.json').read_bytes()
frames=sorted(int(p.stem)for p in(capture/'frames').glob('*.png'))
assert frames==[n for start,end in info['capture_windows']for n in range(start,end+1)]
matched=0
for n in frames:
 if n%2:continue
 for kind,ext in [('ram','bin'),('ppu','bin'),('oam','bin'),('view','json')]:assert(capture/kind/f'{n:06}.{ext}').read_bytes()==(full/kind/f'{n:06}.{ext}').read_bytes(),(n,kind)
 assert np.array_equal(np.array(Image.open(capture/'frames'/f'{n:06}.png')),np.array(Image.open(full/'frames'/f'{n:06}.png'))),(n,'render repeat')
 matched+=1
assert(capture/'apu.tsv').read_bytes()==(full/'apu.tsv').read_bytes()
with wave.open(str(full/'full.wav'),'rb')as w:params=w.getparams();pcm=w.readframes(w.getnframes())
with wave.open(str(capture/'full.wav'),'rb')as w:assert w.getparams()==params and w.readframes(w.getnframes())==pcm
pack=capture/'mesen_home/HdPacks/Holy_Diver_(Tr)';bg=np.array(Image.open(pack/'Demonic_Palace_Interior.png').convert('RGB'))[:,:512]
flash=np.array(Image.open(pack/'Demonic_Palace_Boss_Flash.png').convert('RGBA'))[:,:512].astype(np.int32)
flash=((flash[:,:,:3]*176+np.array([255,254,255])*79)//255).astype(np.uint8)
def variants(target):
 out=[]
 for gray in [False,True]:
  base=np.repeat((target.astype(np.uint16).sum(2)//3)[:,:,None],3,2)if gray else target
  for bits in range(8):
   factors=np.ones(3)
   for bit in range(3):
    if bits&(1<<bit):factors*=np.array([1.1 if ch==bit else .9 for ch in range(3)])
   out.append(np.minimum(base.astype(float)*factors,255).astype(np.uint8))
 return out
normal=variants((bg*.5).astype(np.uint8));flashes=variants(flash);checked=[];flash_frames=[]
for n in frames:
 ram=(capture/'ram'/f'{n:06}.bin').read_bytes()
 if int.from_bytes(ram[0x78:0x7a],'little')!=0x8e6a:continue
 im=np.array(Image.open(capture/'frames'/f'{n:06}.png').convert('RGB'));count=0;kind=None
 for label,items in [('normal',normal),('flash',flashes)]:
  for source in items:
   count=max(count,int(np.all(im==source,2).sum()))
   if count>10000:kind=label;break
  if kind:break
 assert kind,(n,'missing HD boss backdrop',count)
 checked.append([n,count])
 if kind=='flash':flash_frames.append(n)
assert len(flash_frames)>20
report=dict(movie=info,consecutive_frames=len(frames),exact_even_native_and_picture_samples=matched,apu_exact=True,full_pcm_exact=True,pcm_sha256=hashlib.sha256(pcm).hexdigest(),boss_backdrop_samples=len(checked),minimum_boss_panorama_pixels=min(n for _,n in checked),flash_frames=flash_frames)
Path(a.out).write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
