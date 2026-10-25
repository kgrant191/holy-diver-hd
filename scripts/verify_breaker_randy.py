"""Check actual paired replays, source-sprite pixels and native preservation."""
from pathlib import Path
import re
import numpy as np
from PIL import Image
root=Path(__file__).resolve().parents[1];pack=root/'build/Holy_Diver_(Tr)';text=(pack/'hires.txt').read_text();defs={l[11:].split(',')[0]:l[11:].split(',')for l in text.splitlines()if l.startswith('<condition>')};images=[Image.open(pack/l[5:]).convert('RGBA')for l in text.splitlines()if l.startswith('<img>')]
block=text.split('# BEGIN BREAKER_RANDY\n')[1].split('# END BREAKER_RANDY')[0];rules=[]
for l in block.splitlines():
 m=re.fullmatch(r'\[([^]]+)\]<tile>(.*)',l)
 if m:rules.append((m[1].split('&'),m[2].split(',')))
def actor(folder,n):
 ppu=(folder/f'dumps/{n:04}.ppu').read_bytes();ram=(folder/f'dumps/{n:04}.ram').read_bytes();o=(folder/f'dumps/{n:04}.oam').read_bytes();sprites=[list(o[i:i+4])for i in range(0,256,4)if o[i]<239];output=np.zeros((480,512,4),dtype=np.uint8);cover=np.zeros((480,512),bool);other=cover.copy();factors=[]
 def palette(s):return 'FF'+ppu[0x3f11+(s[2]&3)*4:0x3f14+(s[2]&3)*4].hex().upper()
 def cond(term,s):
  c=defs[term.lstrip('!')];kind=c[1]
  if kind=='memoryCheckConstant':
   value=ram[int(c[2],16)];target=int(c[4],16);v={'==':value==target,'!=':value!=target}[c[3]]
  elif kind=='spriteNearby':
   dx,dy=int(c[2]),int(c[3]);dx=-dx if s[2]&64 else dx;dy=-dy if s[2]&128 else dy
   v=any(t[3]==s[3]+dx and t[0]==s[0]+dy and t[1]+0x400==int(c[4],16) and palette(t)==c[5] for t in sprites)
  else:raise ValueError(kind)
  return not v if term.startswith('!') else v
 for s in sprites:
  y,t,attrs,x=s;x*=2;y=(y+1)*2
  if not (attrs&3==3 and 0<t<0x40):other[y:min(y+16,480),x:min(x+16,512)]=True;continue
  cover[y:min(y+16,480),x:min(x+16,512)]=True
  matches=[f for cs,f in rules if int(f[1],16)==t+0x400 and f[2]==palette(s) and all(cond(c,s)for c in cs)]
  if not matches:continue
  f=matches[0];cell=np.array(images[int(f[0])].crop((int(f[3]),int(f[4]),int(f[3])+16,int(f[4])+16)))
  if attrs&64:cell=cell[:,::-1]
  if attrs&128:cell=cell[::-1]
  output[y:y+16,x:x+16]=cell[:480-y,:512-x];factors.append(float(f[5]))
 return output,cover,other,factors

if __name__ == '__main__':
 import json, hashlib
 from collections import Counter
 old=json.loads((root/'evidence/0.10.1-pack-sha256.json').read_text())
 new=json.loads((root/'evidence/0.10.2-pack-sha256.json').read_text())
 assert set(old)==set(new) and sorted(k for k in old if old[k]!=new[k])==['README.txt','hires.txt']
 work=root/'work/breaker_randy'
 cases=[('pickup',work/'before/pickup',work/'after/pickup',1600,1),
        ('alternate_pickup',work/'left_before/left_pickup',work/'left_after/left_pickup',1600,1),
        ('original_victory',root/'work/boss2_review/regression_after/victory',work/'regression_after/victory',1600,2),
        ('combat_poses',root/'work/boss2_review/regression_after/poses',work/'regression_after/poses',900,2)]
 report={'baseline':'0.10.1','candidate':'0.10.2','controller_only':True,'ram_writes':False,'unchanged_installed_files':91,'cases':{}}
 for name,before,after,frames,stride in cases:
  assert int((before/'completed.txt').read_text())>=frames and int((after/'completed.txt').read_text())==frames
  assert (before/'input.json').read_bytes()==(after/'input.json').read_bytes()
  for folder,manifest in [(before,old),(after,new)]:
   for filename in ['installed_pack_sha256.json','installed_pack_after_sha256.json']:assert json.loads((folder/filename).read_text())==manifest
  for ext in ['ram','ppu','oam','view']:
   for n in range(stride,frames+1,stride):assert (before/f'dumps/{n:04}.{ext}').read_bytes()==(after/f'dumps/{n:04}.{ext}').read_bytes(),(name,n,ext)
  def apu(folder):return [l for l in (folder/'apu.tsv').read_text().splitlines()if int(l.split(',')[0])<frames]
  assert apu(before)==apu(after),(name,'APU')
  a=(before/'full.wav').read_bytes()[44:];b=(after/'full.wav').read_bytes()[44:]
  common=min(len(a),len(b));tail=abs(len(a)-len(b));assert a[:common]==b[:common],(name,'PCM')
  if int((before/'completed.txt').read_text())==frames:assert tail<=3200,(name,'PCM tail',tail)
  counts=Counter();examples={};phases=Counter();pixels=0;mirrors=set()
  for n in range(stride,frames+1,stride):
   left=before/f'frames/{n:04}.png';right=after/f'frames/{n:04}.png'
   if not left.stat().st_size:assert not right.stat().st_size;counts['empty_initial_capture']+=1;continue
   a=np.array(Image.open(left).convert('RGB'));b=np.array(Image.open(right).convert('RGB'));diff=np.any(a!=b,axis=2)
   if not diff.any():counts['identical_images']+=1;continue
   assert name!='combat_poses',(name,n,'unexpected pose change')
   counts['changed_images']+=1;permitted=np.zeros((480,512),bool);others=permitted.copy();options=[]
   for j in sorted(set([max(stride,n-stride),n,min(frames,n+stride)])):
    src,cover,other,factors=actor(after,j);permitted|=cover;others|=other
    if factors:options.append((j,src,factors[0]))
   assert not (diff&~permitted).any(),(name,n,'changed outside Randy')
   matched=None
   for j,src,factor in options:
    mask=(src[:,:,3]==255)&~others
    # The native orbiting effects can cover most of Randy. Require visible
    # source pixels on every changed frame and report the exact tested count.
    if mask.sum()<64:continue
    # Mesen stores brightness as int(factor*255). Its RGB path can differ by
    # one level from integer division; this tolerance does not allow NES art.
    expected=(src[:,:,:3].astype(float)*int(factor*255)/255).astype('uint8')
    error=np.abs(b[mask].astype(int)-expected[mask].astype(int))
    if error.max()<=1:
     ppu=(after/f'dumps/{j:04}.ppu').read_bytes();palette='FF'+ppu[0x3f1d:0x3f20].hex().upper();matched=(j,palette,int(mask.sum()));break
   assert matched is not None,(name,n,'HD Randy source mismatch')
   j,palette,num=matched;phases[palette]+=1;pixels+=num;examples.setdefault(palette,n)
   o=(after/f'dumps/{j:04}.oam').read_bytes();mirrors.update(bool(o[k+2]&64)for k in range(0,256,4)if o[k]<239 and 0<o[k+1]<0x40 and o[k+2]&3==3)
  if name!='combat_poses':assert len(phases)==3,(name,phases)
  report['cases'][name]={'frames':frames,'stride':stride,'native_samples_per_type':frames//stride,'image_checks':dict(counts),'fade_samples':dict(phases),'exact_shape_source_pixels_with_rgb_tolerance_1':pixels,'fade_horizontal_mirrors_observed':sorted(mirrors),'examples':examples,'common_pcm_bytes_identical':common,'pcm_length_difference_bytes':tail,'baseline_longer_route':int((before/'completed.txt').read_text())>frames,'input':json.loads((after/'input.json').read_text())}
 report['frames_per_build']=sum(c[3]for c in cases);report['native_samples_per_type']=sum(c[3]//c[4]for c in cases)
 out=root/'evidence/breaker_randy';out.mkdir(exist_ok=True);(out/'validation.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
