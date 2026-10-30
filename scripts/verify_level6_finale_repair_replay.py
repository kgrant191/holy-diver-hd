"""Compare full movie state/audio and constrain actual image changes to repairs."""
from pathlib import Path
import argparse,json,hashlib,wave
from collections import Counter
import numpy as np
from PIL import Image
from verify_level6_opening_replay import source,matches

def visible(data):
    p=data['ppu'];v=data['view'];vv=v['vram'];sx=(vv&31)*8+v['xscroll']+(256 if vv&0x400 else 0);sy=((vv>>5)&31)*8+((vv>>12)&7)+(240 if vv&0x800 else 0)
    cells={}
    for yy in range(sy//8,(sy+239)//8+1):
        for xx in range(sx//8,(sx+255)//8+1):
            tx,ty=xx%32,yy%30;nt=0x2000+(xx//32%2)*0x400+(yy//30%2)*0x800
            cells[(xx*8-sx,yy*8-sy)]=p[nt+ty*32+tx]
    return cells

def rectangle(mask,x,y,w,h):
    x0,y0=max(0,x*2),max(0,y*2);x1,y1=min(512,(x+w)*2),min(480,(y+h)*2)
    if x0<x1 and y0<y1:mask[y0:y1,x0:x1]=True

def native_dragon_visible(d):
    """Prove a nonblack native dragon pixel survives native BG priority."""
    cells=visible(d);ppu=d['ppu'];v=d['view'];vv=v['vram'];sx=(vv&31)*8+v['xscroll'];sy=((vv>>5)&31)*8+((vv>>12)&7)
    black={0x0d,0x0e,0x0f,0x1d,0x1e,0x1f,0x2e,0x2f,0x3e,0x3f}
    for j in range(0,256,4):
        y,t,attr,x=d['oam'][j:j+4]
        if y>=239 or not 0xcd<=t<=0xeb:continue
        pattern=ppu[t*16:t*16+16]
        for py in range(8):
            for px in range(8):
                xx,yy=x+px,y+1+py
                if xx>=256 or yy>=240:continue
                tx=7-px if attr&64 else px;ty=7-py if attr&128 else py
                ink=((pattern[ty]>>(7-tx))&1)+2*((pattern[ty+8]>>(7-tx))&1)
                if not ink or ppu[0x3f10+(attr&3)*4+ink]&63 in black:continue
                gx=xx-(xx+sx)%8;gy=yy-(yy+sy)%8;bt=cells.get((gx,gy))
                if bt is None:continue
                bp=ppu[0x1000+bt*16:0x1000+bt*16+16];bx,by=xx-gx,yy-gy
                bg=((bp[by]>>(7-bx))&1)+2*((bp[by+8]>>(7-bx))&1)
                if not attr&32 or bg==0:return True
    return False

def main():
    p=argparse.ArgumentParser()
    for k in ['before','after','out']:p.add_argument('--'+k,required=True)
    p.add_argument('--baseline-images');p.add_argument('--earlier',action='store_true');a=p.parse_args()
    root=Path(__file__).resolve().parents[1];b,c=Path(a.before),Path(a.after);bi=Path(a.baseline_images)if a.baseline_images else b/'frames'
    infos=[json.loads((d/'result.json').read_text())for d in [b,c]]
    for k in ['movie_sha256','rom_sha1','core_sha256','movie_frames','captured_frames','stride']:assert infos[0][k]==infos[1][k],k
    count=4761 if a.earlier else 19215;assert infos[1]['movie_completed']and infos[1]['movie_frames']==count and infos[1]['stride']==1
    expected=json.loads((root/'evidence/0.30.1-pack-sha256.json').read_text());installed=json.loads((c/'installed_pack.json').read_text())
    scoped_delta=False
    if installed!=expected:
        assert not a.earlier
        assert set(installed)==set(expected)and [k for k in expected if installed[k]!=expected[k]]==['hires.txt']
        current=(root/'build/Holy_Diver_(Tr)/hires.txt').read_text();captured=(c/'mesen_home/HdPacks/Holy_Diver_(Tr)/hires.txt').read_text()
        assert current.replace('# LEVEL6_FINALE_REPAIR SUPERSEDED ','')==captured
        marked=[l for l in current.splitlines()if l.startswith('# LEVEL6_FINALE_REPAIR SUPERSEDED ')]
        assert len(marked)==171 and all(l.startswith('# LEVEL6_FINALE_REPAIR SUPERSEDED [organicMode&organicLo&organicHi]')for l in marked)
        scoped_delta=True
    assert (b/'apu.tsv').read_bytes()==(c/'apu.tsv').read_bytes()
    with wave.open(str(b/'full.wav'))as f:params=f.getparams();pcm=f.readframes(f.getnframes())
    with wave.open(str(c/'full.wav'))as f:assert f.getparams()==params and f.readframes(f.getnframes())==pcm
    stats=Counter();prev=None;hits={};art=root/'art/level6_finale_repair';reg=json.loads((art/'registration.json').read_text());faceids={t&255 for row in reg['face_layout']for t in row}
    names=['wall_face']if a.earlier else ['blue_blob0','blue_blob1','portal','ending_dragon0','ending_dragon1']
    sources={name:source(art/(name+'.png'),False)for name in names}
    for n in range(1,count+1):
        data={}
        for kind in ['ram','ppu','oam','view']:
            file=f'{n:06}'+('.json'if kind=='view'else'.bin');raw=(c/kind/file).read_bytes();assert raw==(b/kind/file).read_bytes(),(n,kind);data[kind]=json.loads(raw)if kind=='view'else raw
        oldpath,newpath=bi/f'{n:06}.png',c/f'frames/{n:06}.png'
        if not oldpath.stat().st_size:assert not newpath.stat().st_size;prev=data;stats['initial_empty']+=1;continue
        old,im=[np.array(Image.open(f).convert('RGB'))for f in [oldpath,newpath]];diff=np.any(old!=im,2)
        room=int.from_bytes(data['ram'][0x78:0x7a],'little');stats['changed'if diff.any()else'identical']+=1
        if scoped_delta:assert room!=0xa3af
        if not old.any():
            if room==0xb01c and n>=9805 and im.any():
                assert native_dragon_visible(prev or data)or native_dragon_visible(data),(n,'native ending visibility')
                stats['restored_previously_occluded_ending_frames']+=1
            else:assert not im.any(),(n,'blackout');stats['blackouts_exact']+=1
        if room in [0xa553,0xa58f]and int.from_bytes((prev or data)['ram'][0x78:0x7a],'little')==room:assert not diff.any(),(n,'boss room');stats['boss_images_exact']+=1
        if diff.any():
            mask=np.zeros((480,512),bool)
            for d in [prev or data,data]:
                rr=int.from_bytes(d['ram'][0x78:0x7a],'little');mode=d['ram'][0x72]
                if (rr==0xa3af and mode==0x10)or(rr==0xa49f and mode==4):
                    cells=visible(d)
                    for(x,y),t in cells.items():
                        if t in faceids:rectangle(mask,x,y,8,8)
                        if rr==0xa49f and t==0xd3 and cells.get((x-16,y+16))==0x2d:rectangle(mask,x,y+16,32,48)
                if rr==0xa49f and mode==4:
                    for j in range(0,256,4):
                        y,t,attr,x=d['oam'][j:j+4]
                        if y<239 and(0x9c<=t<=0xa3 or 0xa9<=t<=0xac):rectangle(mask,x,y+1,8,8)
                if rr==0xb01c and mode==4:
                    for j in range(0,256,4):
                        y,t,attr,x=d['oam'][j:j+4]
                        if y<239 and 0xcd<=t<=0xeb:rectangle(mask,x,y+1,8,8)
            assert not(diff&~mask).any(),(n,'change outside requested actors/entrance',int((diff&~mask).sum()))
            stats['bounded_changed_frames']+=1
        # Search representative unoccluded source poses in the actual render.
        if n%10==0:
            for name,item in sources.items():
                if name in hits:continue
                if name.startswith('ending')!=(room==0xb01c):continue
                if name=='portal'and not 3800<=n<=4050:continue
                found=matches(im,item)
                if found:hits[name]=dict(frame=n,positions=found)
        if n%3000==0:print('Verified',n,flush=True)
        prev=data
    assert set(hits)==set(names),(hits,names)
    report=dict(movie=infos[1],native_samples_per_type=count,native_exact=True,apu_exact=True,pcm_exact=True,pcm_sha256=hashlib.sha256(pcm).hexdigest(),render_assets_match_final_manifest=True,final_runtime_verified=True,earlier_room_only_rule_delta=scoped_delta,statistics=dict(stats),all_image_changes_within_requested_scope=True,whole_source_hits=hits)
    Path(a.out).write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
if __name__=='__main__':main()
