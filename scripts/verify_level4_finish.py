"""Compare actual replays: native/audio exact and door/stair-only pixels."""
from pathlib import Path
from collections import Counter
import argparse, hashlib, json, wave
import numpy as np
from PIL import Image

p=argparse.ArgumentParser()
for k in ['before','after','out']: p.add_argument('--'+k,required=True)
p.add_argument('--stairs-only',action='store_true')
p.add_argument('--after-manifest',help='Explicit frozen manifest for a retained replay; see scope-equivalence evidence')
a=p.parse_args();r=Path(__file__).resolve().parents[1];b,c=Path(a.before),Path(a.after)
bi,ci=[json.loads((d/'result.json').read_text()) for d in [b,c]]
for k in ['movie_sha256','rom_sha1','core_sha256','movie_frames','captured_frames','stride']: assert bi[k]==ci[k],k
assert bi['movie_completed'] and ci['movie_completed'] and ci['stride']==1
for d,v in [(b,'0.20.0'),(c,'0.20.1')]:
    expected=Path(a.after_manifest) if d==c and a.after_manifest else r/f'evidence/{v}-pack-sha256.json'
    assert json.loads((d/'installed_pack.json').read_text())==json.loads(expected.read_text())
frames=sorted(int(p.stem) for p in (c/'frames').glob('*.png'));data={k:{} for k in ['ram','ppu','oam','view']}
for n in frames:
    for k in data:
        name=f'{n:06}'+('.json' if k=='view' else '.bin');raw=(c/k/name).read_bytes()
        assert raw==(b/k/name).read_bytes(),(n,k)
        data[k][n]=json.loads(raw) if k=='view' else raw
apu=(b/'apu.tsv').read_bytes();assert apu==(c/'apu.tsv').read_bytes()
with wave.open(str(b/'full.wav'),'rb') as f: pcm=f.readframes(f.getnframes());params=f.getparams()
with wave.open(str(c/'full.wav'),'rb') as f: assert f.getparams()==params;assert f.readframes(f.getnframes())==pcm
rooms={n:int.from_bytes(v[0x78:0x7a],'little') for n,v in data['ram'].items()}
temple_rooms={0xa865,0xaa09,0xaa81,0xaaf9,0xab71,0xac61,0xacd9,0xae41,0xaef5}
crown={0xdf,0xe0,0xe1,0xe2,0x5b,0x5c,0x63,0x64,0x5d,0x5e,0x65,0x66,0x5f,0x60,0x67,0x68}
def allowed(n):
    mask=np.zeros((480,512),bool)
    for j in [n-1,n,n+1]:
        if j not in data['ram'] or rooms[j] not in temple_rooms: continue
        pp,v=data['ppu'][j],data['view'][j];vv=v['vram']
        sx=(vv&31)*8+v['xscroll']+(256 if vv&0x400 else 0)
        sy=((vv>>5)&31)*8+((vv>>12)&7)+(240 if vv&0x800 else 0)
        def cell(xx,yy):
            nt=0x2000+xx//32%2*0x400+yy//30%2*0x800
            return pp[nt+(yy%30)*32+xx%32]
        for yy in range(sy//8,(sy+239)//8+1):
            for xx in range(sx//8,(sx+255)//8+1):
                t=cell(xx,yy);ok=0x7c<=t<=0x7f
                if not a.stairs_only and rooms[j]==0xaef5:
                    ok |= t in crown
                    if t==0: ok |= any(cell(xx,yy-d) in {0x5f,0x60,0x67,0x68} for d in range(1,7))
                if not ok:continue
                X,Y=(xx*8-sx)*2,(yy*8-sy)*2
                # endFrame can describe the adjacent submitted scrolling frame.
                mask[max(0,Y-4):min(480,Y+20),max(0,X-4):min(512,X+20)]=True
    return mask

def source(path):
    src=np.array(Image.open(path).convert('RGBA'));mask=src[:,:,3]==255
    colors,counts=np.unique(src[mask,:3],axis=0,return_counts=True)
    color=colors[np.argmax(colors.sum(1)/(1+counts))]
    yy,xx=np.where(mask&np.all(src[:,:,:3]==color,2));pts=np.argwhere(mask)
    return src,mask,int(yy[0]),int(xx[0]),pts[np.linspace(0,len(pts)-1,8,dtype=int)]
def matches(im,item):
    src,mask,ay,ax,probes=item;h,w=mask.shape
    yy,xx=np.where(np.all(im==src[ay,ax,:3],2));yy-=ay;xx-=ax
    valid=(yy>=0)&(xx>=0)&(yy+h<=480)&(xx+w<=512);yy,xx=yy[valid],xx[valid]
    for py,px in probes:
        valid=np.all(im[yy+py,xx+px]==src[py,px,:3],1);yy,xx=yy[valid],xx[valid]
        if not len(yy):return []
    return [[int(x),int(y)] for y,x in zip(yy,xx) if np.array_equal(im[y:y+h,x:x+w][mask],src[:,:,:3][mask])]
sources={'stairs':source(r/'art/level4_finish/descending_step.png')}
if not a.stairs_only:sources['portal']=source(r/'art/level4_finish/boss_portal.png')
counts=Counter();hits=Counter();examples={};pixel_count=0
for n in frames:
    paths=[d/'frames'/f'{n:06}.png' for d in [b,c]]
    if not all(p.stat().st_size for p in paths):
        assert paths[0].stat().st_size==paths[1].stat().st_size;counts['empty_initial']+=1;continue
    old,im=[np.array(Image.open(p).convert('RGB')) for p in paths]
    diff=np.any(old!=im,2);pixel_count+=int(diff.sum())
    if diff.any():
        assert not diff[~allowed(n)].any(),('outside door/stairs',n,int(diff[~allowed(n)].sum()))
        counts['door_or_stair_only']+=1
    else:counts['identical']+=1
    if rooms[n]==0xafa9:assert not diff.any();counts['boss_room_exact']+=1
    if not old.any():assert not im.any();counts['native_black_exact']+=1
    if n%20:continue
    for name,src in sources.items():
        if name=='portal' and rooms[n]!=0xaef5:continue
        positions=matches(im,src)
        if positions:
            hits[name]+=len(positions)
            if name not in examples:examples[name]=dict(frame=n,positions=positions)
assert hits['stairs']>0
if not a.stairs_only:assert hits['portal']>0
report=dict(movie_frames=ci['movie_frames'],native_samples_per_type=len(frames),
    native_exact=True,apu_exact=True,pcm_exact=True,pcm_bytes=len(pcm),
    pcm_sha256=hashlib.sha256(pcm).hexdigest(),apu_sha256=hashlib.sha256(apu).hexdigest(),
    movie_sha256=ci['movie_sha256'],image_checks=counts,changed_pixels=pixel_count,
    changes_confined_to_door_and_stairs=True,complete_source_matches=hits,examples=examples)
Path(a.out).write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
