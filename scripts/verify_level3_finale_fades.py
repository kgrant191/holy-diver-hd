"""Reconstruct visible HD Randy cells during every recorded final pickup fade."""
from pathlib import Path
import argparse,json,re
import numpy as np
from PIL import Image
p=argparse.ArgumentParser();p.add_argument('--capture',required=True);p.add_argument('--out',required=True);a=p.parse_args()
r=Path(__file__).resolve().parents[1];c=Path(a.capture);pack=c/'mesen_home/HdPacks/Holy_Diver_(Tr)';text=(pack/'hires.txt').read_text()
defs={l[11:].split(',')[0]:l[11:].split(',')for l in text.splitlines()if l.startswith('<condition>')};images=[Image.open(pack/l[5:]).convert('RGBA')for l in text.splitlines()if l.startswith('<img>')]
block=text.split('# BEGIN LEVEL3_FINALE ALIASES\n')[1].split('# END LEVEL3_FINALE ALIASES')[0];rules=[]
for l in block.splitlines():
 m=re.fullmatch(r'\[([^]]+)\]<tile>(.*)',l)
 if m and m[1].startswith('l3f9F92'):rules.append((m[1].split('&'),m[2].split(',')))
def actor(n):
 pp=(c/'ppu'/f'{n:06}.bin').read_bytes();ram=(c/'ram'/f'{n:06}.bin').read_bytes();o=(c/'oam'/f'{n:06}.bin').read_bytes();sprites=[list(o[i:i+4])for i in range(0,256,4)if o[i]<239]
 output=np.zeros((480,512,4),np.uint8);other=np.zeros((480,512),bool);factors=[]
 def palette(s):return 'FF'+pp[0x3f11+(s[2]&3)*4:0x3f14+(s[2]&3)*4].hex().upper()
 def cond(term,s):
  d=defs[term.lstrip('!')];kind=d[1]
  if kind in ['memoryCheckConstant','ppuMemoryCheckConstant']:
   value=(ram if kind=='memoryCheckConstant'else pp)[int(d[2],16)];target=int(d[4],16);v={'==':value==target,'!=':value!=target}[d[3]]
  elif kind=='spriteNearby':
   dx,dy=int(d[2]),int(d[3]);dx=-dx if s[2]&64 else dx;dy=-dy if s[2]&128 else dy
   v=any(t[3]==s[3]+dx and t[0]==s[0]+dy and t[1]+0x800==int(d[4],16) and palette(t)==d[5]for t in sprites)
  else:raise ValueError(kind)
  return not v if term.startswith('!')else v
 for s in sprites:
  y,t,at,x=s;x*=2;y=(y+1)*2
  if not(at&3==3 and 0<t<0x40):other[y:min(y+16,480),x:min(x+16,512)]=True;continue
  matches=[f for cs,f in rules if int(f[1],16)==t+0x800 and f[2]==palette(s)and all(cond(k,s)for k in cs)]
  if not matches:continue
  f=matches[0];im=np.array(images[int(f[0])].crop((int(f[3]),int(f[4]),int(f[3])+16,int(f[4])+16)))
  if at&64:im=im[:,::-1]
  if at&128:im=im[::-1]
  output[y:y+16,x:x+16]=im[:480-y,:512-x];factors.append(float(f[5]))
 return output,other,factors
checks=[]
for n in range(4356,4377,2):
 actual=np.array(Image.open(c/'frames'/f'{n:06}.png').convert('RGB'));options=[(j,*actor(j))for j in[n-2,n,n+2]];other=np.logical_or.reduce([v[2]for v in options]);found=None
 for j,src,_,factors in options:
  mask=(src[:,:,3]==255)&~other
  if not factors or mask.sum()<64:continue
  expected=(src[:,:,:3].astype(float)*int(factors[0]*255)/255).astype('uint8')
  # End-frame OAM can describe the next picture. Bound the whole-sprite
  # translation by actual adjacent native positions; never move cells alone.
  def anchor(k):
   o=(c/'oam'/f'{k:06}.bin').read_bytes();s=next(o[i:i+4]for i in range(0,256,4)if o[i]<239 and 0<o[i+1]<0x40 and o[i+2]&3==3);return s[3],s[0]
  positions=[anchor(k)for k in[n-2,n,n+2]];origin=anchor(j)
  bounds=[range(2*(min(v[axis]for v in positions)-origin[axis]),2*(max(v[axis]for v in positions)-origin[axis])+1,2)for axis in[0,1]]
  for dx in bounds[0]:
   for dy in bounds[1]:
    e=np.roll(expected,(dy,dx),(0,1));m=np.roll(mask,(dy,dx),(0,1))&~other;err=np.abs(actual[m].astype(int)-e[m].astype(int))
    if m.sum()>=64 and err.max()<=1:
     pp=(c/'ppu'/f'{j:06}.bin').read_bytes();found=dict(frame=n,oam_frame=j,hd_offset=[dx,dy],palette='FF'+pp[0x3f1d:0x3f20].hex().upper(),source_pixels=int(m.sum()),maximum_rgb_error=int(err.max()));break
   if found:break
  if found:break
 assert found is not None,('Missing HD Randy during fade',n);checks.append(found)
assert {q['palette']for q in checks}=={'FF200F26','FF100F16','FF000F06'}
out=Path(a.out);out.parent.mkdir(parents=True,exist_ok=True);out.write_text(json.dumps(dict(checks=checks),indent=2)+'\n');print(json.dumps(dict(samples=len(checks),source_pixels=sum(q['source_pixels']for q in checks))))
