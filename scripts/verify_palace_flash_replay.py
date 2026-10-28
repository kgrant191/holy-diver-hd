"""Check every consecutive Thunder/pickup frame and native flash blending."""
from pathlib import Path
from collections import Counter
import argparse,json,hashlib,wave
import numpy as np
from PIL import Image
p=argparse.ArgumentParser();p.add_argument('--captures',required=True);p.add_argument('--out',required=True);a=p.parse_args();r=Path(__file__).resolve().parents[1];c=Path(a.captures)
def digest(path):
 h=hashlib.sha256()
 with path.open('rb')as f:
  for chunk in iter(lambda:f.read(1024*1024),b''):h.update(chunk)
 return h.hexdigest()
bg=np.array(Image.open(c/'candidate_pack/Demonic_Palace_Interior.png').convert('RGB'))[:,:512]
base={'normal':bg}
for phase,color in [('30',[255,254,255]),('31',[192,223,255])]:base[phase]=((bg.astype(np.uint16)*177>>8)+(np.array(color,dtype=np.uint16)*80>>8)).astype(np.uint8)
variants=[]
for name,v in base.items():variants.append((name,v))
for gray in [False,True]:
 for bits in range(8):
  if not gray and not bits:continue
  factors=np.ones(3)
  for bit in range(3):
   if bits&(1<<bit):factors*=np.array([1.1 if j==bit else .9 for j in range(3)])
  for name,v in base.items():
   raw=np.repeat((v.astype(np.uint16).sum(2)//3)[:,:,None],3,2)if gray else v
   variants.append((f'{name}/gray{int(gray)}/emphasis{bits}',np.minimum(raw.astype(float)*factors,255).astype(np.uint8)))
reports={}
for case in ['opening','hall']:
 b,d=[c/f'{case}_{phase}'for phase in ['before','after']];before,after=[json.loads((folder/'result.json').read_text())for folder in [b,d]]
 for key in ['movie_sha256','rom_sha1','core_sha256','movie_frames','captured_frames','stride']:assert before[key]==after[key],(case,key)
 assert before['movie_completed']and after['movie_completed']and after['stride']==1
 for folder,version in [(b,'0.22.0'),(d,'0.22.1')]:assert json.loads((folder/'installed_pack.json').read_text())==json.loads((r/f'evidence/{version}-pack-sha256.json').read_text())
 frames=sorted(int(f.stem)for f in(d/'frames').glob('*.png'));palettes={};rooms={}
 for n in frames:
  for kind in ['ram','ppu','oam','view']:
   file=f'{n:06}'+('.json'if kind=='view'else'.bin');raw=(d/kind/file).read_bytes();assert raw==(b/kind/file).read_bytes(),(case,n,kind)
   if kind=='ppu':palettes[n]=raw[0x3f00]
   if kind=='ram':rooms[n]=raw[0x78:0x7a][::-1].hex().upper()
 assert digest(b/'apu.tsv')==digest(d/'apu.tsv')
 assert digest(b/'full.wav')==digest(d/'full.wav')
 counts=Counter();changed=[];matches=[]
 for n in frames:
  old,im=[np.array(Image.open(folder/'frames'/f'{n:06}.png').convert('RGB'))for folder in [b,d]]
  if np.array_equal(old,im):counts['identical']+=1;continue
  changed.append(n);assert rooms[n]in ['8762','888E'];assert any(palettes.get(j)in [0x30,0x31]for j in [n-1,n,n+1]),(case,n,'outside native flash')
  assert old.any()and im.any()
  hit=None
  for name,variant in variants:
   pixels=int(np.all(im==variant,2).sum())
   if pixels>40000:hit=dict(frame=n,variant=name,exact_source_pixels=pixels);break
  assert hit,(case,n,'HD panorama absent during flash')
  matches.append(hit);counts['corrected_flash_frames']+=1;counts['phase_'+hit['variant']]+=1
 assert len(changed)>=30 and counts['identical']>100
 reports[case]=dict(movie=after,consecutive_samples=len(frames),native_ram_ppu_oam_scroll_exact=True,full_movie_apu_and_pcm_exact=True,apu_sha256=digest(d/'apu.tsv'),wav_sha256=digest(d/'full.wav'),images=counts,changed_frames=changed,flash_source_matches=matches,minimum_flash_source_pixels=min(v['exact_source_pixels']for v in matches))
Path(a.out).write_text(json.dumps(reports,indent=2)+'\n');print(json.dumps({k:{n:v for n,v in info.items()if n not in ['changed_frames','flash_source_matches']}for k,info in reports.items()},indent=2))
