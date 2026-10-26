"""Pair the final climb/boss movie: native state/audio, scope and painted sources."""
from pathlib import Path
from collections import Counter
import argparse,json,wave
import numpy as np
from PIL import Image

p=argparse.ArgumentParser()
for key in ['before','after','out']:p.add_argument('--'+key,required=True)
p.add_argument('--edge',action='store_true');p.add_argument('--flashes',action='store_true');a=p.parse_args()
r=Path(__file__).resolve().parents[1];b,c=Path(a.before),Path(a.after)
bi,ci=[json.loads((f/'result.json').read_text())for f in [b,c]]
for key in ['movie_sha256','rom_sha1','core_sha256','movie_frames','captured_frames','stride']:assert bi[key]==ci[key],key
assert bi['movie_completed'] and ci['movie_completed'];stride=ci['stride']
for capture,version in [(b,'0.14.0'),(c,'0.15.0')]:
 assert json.loads((capture/'installed_pack.json').read_text())==json.loads((r/f'evidence/{version}-pack-sha256.json').read_text()),'Incorrect installed pack'
frames=sorted(int(f.stem)for f in(c/'frames').glob('*.png'));ram={};oam={}
for n in frames:
 for key in ['ram','ppu','oam','view']:
  name=f'{n:06}'+('.json'if key=='view'else'.bin');raw=(c/key/name).read_bytes();assert raw==(b/key/name).read_bytes(),(n,key)
  if key=='ram':ram[n]=raw
  if key=='oam':oam[n]=raw
apu=(b/'apu.tsv').read_bytes();assert apu==(c/'apu.tsv').read_bytes()
with wave.open(str(b/'full.wav'),'rb')as f:pcm=f.readframes(f.getnframes());params=f.getparams()
with wave.open(str(c/'full.wav'),'rb')as f:assert f.getparams()==params;assert f.readframes(f.getnframes())==pcm
def room(n):return int.from_bytes(ram[n][0x78:0x7a],'little')
sources={}
for name in ['boss_head','shot_0','shot_1','shot_2','overdrive']:
 src=np.array(Image.open(r/f'art/level3_finale/{name}.png').convert('RGBA'))
 for h in [False,True]if name.startswith('shot')else[False]:
  for v in [False,True]if name in ['boss_head','shot_0','shot_1','shot_2']else[False]:
   im=src[::-1]if v else src;im=im[:,::-1]if h else im;mask=im[:,:,3]==255;ys,xs=np.nonzero(mask);j=len(ys)//2
   sources[f'{name}/h{int(h)}v{int(v)}']=(im,mask,int(ys[j]),int(xs[j]))
roundshot=np.array(Image.open(r/'art/level3_detail/round_shot.png').convert('RGBA'));mask=roundshot[:,:,3]==255;ys,xs=np.nonzero(mask);sources['reused_round_shot']=(roundshot,mask,int(ys[len(ys)//2]),int(xs[len(xs)//2]))
counts=Counter();rooms=Counter();matches=Counter();examples={};cards={};flashes=Counter()
pack=c/'mesen_home/HdPacks/Holy_Diver_(Tr)'
card_sources={'Overdrive':np.array(Image.open(pack/'Overdrive_Acquired.png').convert('RGB')),'Stage4':np.array(Image.open(pack/'Intermission_HD.png').convert('RGB'))}
for name in ['Stage_Title_4.png','Stage_Lives_3.png']:
 # Match stock Mesen's premultiply/256 blend rather than Pillow's /255 rounding.
 src=np.array(Image.open(pack/name).convert('RGBA')).astype(np.uint32);alpha=src[:,:,3:4];dst=card_sources['Stage4'].astype(np.uint32)
 blended=((src[:,:,:3]*(alpha+1))>>8)+(((256-alpha)*dst)>>8)
 card_sources['Stage4']=np.where(alpha==255,src[:,:,:3],np.where(alpha==0,dst,blended)).astype('uint8')
for n in frames:
 name=f'{n:06}.png';pb,pc=b/'frames'/name,c/'frames'/name
 if not pb.stat().st_size:assert not pc.stat().st_size;counts['initial_empty']+=1;continue
 before=np.array(Image.open(pb).convert('RGB'));after=np.array(Image.open(pc).convert('RGB'));diff=np.any(before!=after,axis=2);eq=not diff.any()
 counts['exact_images'if eq else'changed_images']+=1;rooms[f'{room(n):04X}']+=1
 near=[j for j in[n-stride,n,n+stride]if j in ram]
 if all(room(j)not in[0x9f1a,0x9f92,0,0xa865]for j in near):assert eq,('outside scope',n);counts['exact_prior_room_or_pause']+=1
 if not before.any():assert not after.any(),('blackout',n);counts['exact_blackouts']+=1
 if not a.edge and room(n)==0x9f92 and 3300<n<4350:
  # Compare each colored native flash against the original replay, excluding
  # the new boss art and conservative adjacent sprite bounds.
  pixels=before[128:360,80:432];colors=[pixels[y,x]for y,x in[(50,50),(50,250),(150,50),(150,250)]];amounts=[int(np.all(pixels==v,axis=2).sum())for v in colors];color=colors[int(np.argmax(amounts))]
  if color.any()and max(amounts)>pixels.shape[0]*pixels.shape[1]*.7:
   mask=np.zeros((480,512),bool);mask[128:360,80:432]=True
   for j in near:
    for i in range(0,256,4):
     y,t,at,x=oam[j][i:i+4]
     if y<239:mask[max(0,y*2-12):min(480,y*2+32),max(0,x*2-12):min(512,x*2+28)]=False
   assert np.all(after[mask]==color),('native flash differs',n,color.tolist());flashes[','.join(map(str,color))]+=1
 if all(room(j)==0xa865 for j in near):
  permitted=np.zeros((480,512),bool)
  for j in near:
   for i in range(0,256,4):
    y,t,at,x=oam[j][i:i+4]
    if y<239 and t<0x74:permitted[max(0,y*2-8):min(480,y*2+30),max(0,x*2-8):min(512,x*2+24)]=True
  assert not(diff&~permitted).any(),('Stage 4 scenery changed',n);counts['Stage4_sprite_only_images']+=1
 if not a.edge and room(n)==0 and n%20==0:
  expected=card_sources['Overdrive'if n<4540 else'Stage4'];mask=np.ones((480,512),bool);mask[:112]=False
  for j in near:
   for i in range(0,256,4):
    y,t,at,x=oam[j][i:i+4]
    if y<239:mask[max(0,y*2-8):min(480,y*2+28),max(0,x*2-8):min(512,x*2+24)]=False
  if after.any()and np.array_equal(after[mask],expected[mask]):
   key='Overdrive'if n<4540 else'Stage4';cards.setdefault(key,dict(frame=n,exact_source_pixels=int(mask.sum())))
 if a.edge or room(n)!=0x9f92 or n%8:continue
 for key,(src,mask,sy,sx)in sources.items():
  h,w=mask.shape
  for y,x in np.argwhere(np.all(after==src[sy,sx,:3],axis=2)):
   X,Y=int(x-sx),int(y-sy)
   if X<0 or Y<0 or X+w>512 or Y+h>480:continue
   if np.array_equal(after[Y:Y+h,X:X+w][mask],src[:,:,:3][mask]):
    matches[key]+=1;examples.setdefault(key,dict(frame=n,xy=[X,Y],opaque_pixels=int(mask.sum())));break
if not a.edge and not a.flashes:
 for key in ['boss_head/h0v0','boss_head/h0v1','overdrive/h0v0','reused_round_shot']:assert matches[key]>0,key
 for i in range(3):assert any(v for k,v in matches.items()if k.startswith(f'shot_{i}/')),i
 assert set(cards)=={'Overdrive','Stage4'},cards
 assert len(flashes)>=2,flashes
if a.flashes:assert len(flashes)==4,flashes
out=Path(a.out);out.parent.mkdir(parents=True,exist_ok=True)
report=dict(version='0.15.0',movie_sha256=ci['movie_sha256'],movie_frames=ci['movie_frames'],capture_stride=stride,paired_native_samples_per_type=len(frames),identical_apu_writes=len(apu.splitlines()),identical_pcm_bytes=len(pcm),counts=dict(counts),rooms=dict(rooms),source_matches=dict(matches),source_examples=examples,cards=cards,preserved_native_flash_colors=dict(flashes),native_gameplay_unchanged=True)
out.write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
