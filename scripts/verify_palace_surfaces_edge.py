"""Compare the controller-only platform traversal and its complete stone span."""
from pathlib import Path
import argparse,json,hashlib,wave,tempfile
import numpy as np
from PIL import Image
p=argparse.ArgumentParser()
for key in ['before','after','out']:p.add_argument('--'+key,required=True)
a=p.parse_args();r=Path(__file__).resolve().parents[1];b,c=Path(a.before),Path(a.after)
infos=[json.loads((d/'result.json').read_text())for d in [b,c]]
for key in ['movie_sha256','rom_sha1','core_sha256','movie_frames','captured_frames','stride']:assert infos[0][key]==infos[1][key]
assert all(i['movie_completed']for i in infos)
for d,ver in [(b,'0.31.0'),(c,'0.32.0')]:assert json.loads((d/'installed_pack.json').read_text())==json.loads((r/f'evidence/{ver}-pack-sha256.json').read_text())
frames=sorted(int(p.stem)for p in(c/'ram').glob('*.bin'));assert frames==list(range(1800,2001));positions={};states={}
for n in frames:
 for kind in ['ram','ppu','oam','view']:
  name=f'{n:06}'+('.json'if kind=='view'else'.bin');assert(b/kind/name).read_bytes()==(c/kind/name).read_bytes(),(kind,n)
 ram=(c/'ram'/f'{n:06}.bin').read_bytes();positions[n]=[int.from_bytes(ram[o:o+2],'little')for o in [0x74,0x76]];states[n]=ram[0x300]
apu=(b/'apu.tsv').read_bytes();assert apu==(c/'apu.tsv').read_bytes()
with wave.open(str(b/'full.wav'))as f:params=f.getparams();pcm=f.readframes(f.getnframes())
with wave.open(str(c/'full.wav'))as f:assert f.getparams()==params and f.readframes(f.getnframes())==pcm
assert all(positions[n]==[607,80]and states[n]==0 for n in range(1840,1851))
assert all(positions[n][1]==80 and positions[n+1][0]-positions[n][0]in [0,1]for n in range(1851,1905))
assert positions[1904]==[647,80]and states[1904]==1
assert positions[1905]==[648,80]and states[1905]==2
assert positions[1909]==[652,81]
assert all(positions[n+1][1]>=positions[n][1]for n in range(1905,1931))
def source(path,mirror=False):
 src=np.array(Image.open(path).convert('RGBA'))
 if mirror:src=src[:,::-1]
 mask=src[:,:,3]==255;colors,counts=np.unique(src[mask,:3],axis=0,return_counts=True);color=colors[np.argmax(colors.sum(1)/(1+counts))];yy,xx=np.where(mask&np.all(src[:,:,:3]==color,2));pts=np.argwhere(mask)
 return src,mask,int(yy[0]),int(xx[0]),pts[np.linspace(0,len(pts)-1,8,dtype=int)]
def matches(im,item):
 src,mask,ay,ax,probes=item;h,w=mask.shape;yy,xx=np.where(np.all(im==src[ay,ax,:3],2));yy-=ay;xx-=ax;v=(yy>=0)&(xx>=0)&(yy+h<=480)&(xx+w<=512);yy,xx=yy[v],xx[v]
 for py,px in probes:
  v=np.all(im[yy+py,xx+px]==src[py,px,:3],1);yy,xx=yy[v],xx[v]
  if not len(yy):return []
 return [[int(x),int(y)]for y,x in zip(yy,xx)if np.array_equal(im[y:y+h,x:x+w][mask],src[:,:,:3][mask])]


reg=json.loads((r/'art/palace_surfaces/registration.json').read_text());atlas=Image.open(c/'mesen_home/HdPacks/Holy_Diver_(Tr)/Palace_Surfaces_Book_2x.png').convert('RGBA')
entries={}
for entry in reg['substitutions']:
 f=entry['new'].split('<tile>')[1].split(',')
 if entry['room']=='8AE6'and f[2]=='0F040F24':entries.setdefault(f[1],{'xy':list(map(int,f[3:5]))})
whole=Image.new('RGBA',(64,32))
for row,tiles in enumerate([['1168','1169','1168','1169'],['1197','1198','1197','1198']]):
 for col,t in enumerate(tiles):
  x,y=entries[t]['xy'];whole.paste(atlas.crop((x,y,x+16,y+16)),(col*16,row*16))
hits=[]
with tempfile.TemporaryDirectory()as temporary:
 path=Path(temporary)/'platform.png';whole.save(path);item=source(path)
 for n in range(1905,1951):
  im=np.array(Image.open(c/'frames'/f'{n:06}.png').convert('RGB'));found=[xy for xy in matches(im,item)if xy[1]==192]
  if found:hits.append(dict(frame=n,positions=found))
assert hits
report=dict(movie=infos[1],paired_native_samples=201,native_exact=True,apu_exact=True,pcm_exact=True,apu_sha256=hashlib.sha256(apu).hexdigest(),pcm_sha256=hashlib.sha256(pcm).hexdigest(),controller_only=True,left_stop=dict(frames=[1840,1850],world_position=[607,80]),platform_native_world_bounds=dict(left=608,right_exclusive=640,screen_y=96),native_fall_start=dict(frame=1905,world_position=[648,80]),native_first_descent=dict(frame=1909,world_position=[652,81]),complete_platform_source_matches=hits)
Path(a.out).write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:v for k,v in report.items()if k!='complete_platform_source_matches'},indent=2));print('Complete platform matches:',len(hits))
