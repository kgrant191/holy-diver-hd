"""Pair native execution and restrict rendered changes to requested surfaces."""
from pathlib import Path
from collections import Counter
import argparse,hashlib,json,wave
import numpy as np
from PIL import Image
from verify_level6_opening_replay import source,matches
p=argparse.ArgumentParser()
for k in ['before','after','out']:p.add_argument('--'+k,required=True)
a=p.parse_args();R=Path(__file__).resolve().parents[1];b,c=Path(a.before),Path(a.after)
infos=[json.loads((d/'result.json').read_text())for d in [b,c]]
for k in ['movie_sha256','rom_sha1','core_sha256','movie_frames']:assert infos[0][k]==infos[1][k],k
assert all(i['movie_completed']for i in infos)
for d,v in [(b,'0.31.0'),(c,'0.32.0')]:assert json.loads((d/'installed_pack.json').read_text())==json.loads((R/f'evidence/{v}-pack-sha256.json').read_text())
apu=(b/'apu.tsv').read_bytes();assert apu==(c/'apu.tsv').read_bytes()
with wave.open(str(b/'full.wav'))as f:params=f.getparams();pcm=f.readframes(f.getnframes())
with wave.open(str(c/'full.wav'))as f:assert params==f.getparams()and pcm==f.readframes(f.getnframes())
reg=json.loads((R/'art/palace_surfaces/registration.json').read_text());rooms=set(reg['rooms']);scenery={};atlas=Image.open(c/'mesen_home/HdPacks/Holy_Diver_(Tr)/Palace_Surfaces_Book_2x.png').convert('RGBA')
for e in reg['substitutions']:
    f=e['new'].split('<tile>')[1].split(',');t=int(f[1],16)
    if e['kind']in ['masonry','boss masonry']:
        x,y=map(int,f[3:5]);scenery.setdefault(e['room'],{})[(t%256,f[2])]=np.array(atlas.crop((x,y,x+16,y+16)))[:,:,3]>0
frames=sorted(int(p.stem)for p in(c/'frames').glob('*.png'));data={}
for n in frames:
    dd={}
    for kind in ['ram','ppu','oam','view']:
        name=f'{n:06}'+('.json'if kind=='view'else'.bin');raw=(c/kind/name).read_bytes();assert raw==(b/kind/name).read_bytes(),(n,kind)
        dd[kind]=json.loads(raw)if kind=='view'else raw
    dd['room']=f'{int.from_bytes(dd["ram"][0x78:0x7a],"little"):04X}';data[n]=dd
def scroll(dd):
    t=dd['view']['vram'];return (t&31)*8+dd['view']['xscroll']+(256 if t&0x400 else 0),((t>>5)&31)*8+((t>>12)&7)+(240 if t&0x800 else 0)
def allowed(dd):
    mask=np.zeros((480,512),np.uint8);pp=dd['ppu'];room=dd['room'];sx,sy=scroll(dd)
    if room in scenery:
        for yy in range(sy//8,(sy+239)//8+1):
            for xx in range(sx//8,(sx+255)//8+1):
                tx,ty=xx%32,yy%30;nt=0x2000+(xx//32%2)*0x400+(yy//30%2)*0x800;t=pp[nt+ty*32+tx];at=pp[nt+960+ty//4*8+tx//4];pi=at>>((ty%4)//2*4+(tx%4)//2*2)&3
                pal=(bytes([pp[0x3f00]])+pp[0x3f01+pi*4:0x3f04+pi*4]).hex().upper();tile=scenery[room].get((t,pal))
                if tile is None:continue
                X,Y=(xx*8-sx)*2,(yy*8-sy)*2;l,rr=max(0,X),min(512,X+16);top,bot=max(0,Y),min(480,Y+16)
                if rr>l and bot>top:mask[top:bot,l:rr]|=tile[top-Y:bot-Y,l-X:rr-X]
    o=dd['oam']
    for i in range(0,256,4):
        yy,t,at,xx=o[i:i+4]
        eligible=(room=='9F92'and 0x8b<=t<=0x8e)or(room in ['8BD6','8D3E']and 0xf7<=t<=0xfa)
        if eligible and yy<239:
            x,y=xx*2,(yy+1)*2;mask[y:min(480,y+16),x:min(512,x+16)]=1
    return mask
def exact_boss_source_pairs(old,im,dd):
    # Boss camera effects can change rendered vertical scroll after the observer's
    # sample. Do not widen the spatial mask: require EVERY changed pixel to be an
    # exact old/new opaque source pair at one common 16-pixel tile-grid phase.
    if dd['room']!='8E6A':return None
    pack=c/'mesen_home/HdPacks/Holy_Diver_(Tr)'
    names=[s.split('>')[1]for s in(pack/'hires.txt').read_text().splitlines()if s.startswith('<img>')]
    atlases={};pairs=[];seen=set()
    for e in reg['substitutions']:
        if e['room']!=dd['room']:continue
        fields=[e[k].split('<tile>')[1].split(',')for k in ['old','new']]
        if any(f[5]!='1'for f in fields):continue
        key=tuple(tuple(f[0:1]+f[3:5])for f in fields)
        if key in seen:continue
        seen.add(key);cells=[]
        for f in fields:
            i=int(f[0]);x,y=map(int,f[3:5])
            if i not in atlases:atlases[i]=Image.open(pack/names[i]).convert('RGBA')
            cells.append(np.array(atlases[i].crop((x,y,x+16,y+16))))
        pairs.append(cells)
    yy,xx=np.where(np.any(old!=im,2));aa,bb=old[yy,xx],im[yy,xx]
    xphase=(-2*scroll(dd)[0])%16
    for yphase in range(16):
        Y,X=(yy-yphase)%16,(xx-xphase)%16;ok=np.zeros(len(yy),bool)
        for before,after in pairs:
            ok|=(before[Y,X,3]==255)&(after[Y,X,3]==255)&np.all(aa==before[Y,X,:3],1)&np.all(bb==after[Y,X,:3],1)
        if ok.all():return dict(changed_pixels=len(yy),tile_grid_phase=[xphase,yphase],every_changed_pixel_exact_old_and_new_source=True)
    return None
stats=Counter();roomstats=Counter();failures=[];bookhits=[];camera_source_checks=[];book=source(R/'art/palace_surfaces/overdrive_book.png')
for idx,n in enumerate(frames):
    dd=data[n];roomstats[dd['room']]+=1;paths=[d/f'frames/{n:06}.png'for d in [b,c]]
    if not paths[0].stat().st_size:assert not paths[1].stat().st_size;stats['empty_initial']+=1;continue
    old,im=[np.array(Image.open(f).convert('RGB'))for f in paths];diff=np.any(old!=im,2)
    if not diff.any():stats['identical_images']+=1
    else:
        stats['changed_images']+=1
        near=[data[frames[j]]for j in range(max(0,idx-1),min(len(frames),idx+2))]
        assert any(d['room']in rooms|{'9F92'}for d in near),(n,'outside requested rooms')
        # The endFrame observer can sample the next submitted video's camera.
        # Union the adjacent native samples and measured interval of movement.
        mask=np.zeros((480,512),np.uint8)
        for d in near:mask|=allowed(d)
        if dd['room']=='9F92':radius=8
        else:radius=max(4,int(infos[1]['stride'])*4)
        integral=np.pad(np.pad(mask,radius),((1,0),(1,0))).astype(np.int32).cumsum(0).cumsum(1);width=radius*2+1
        mask=(integral[width:,width:]-integral[:-width,width:]-integral[width:,:-width]+integral[:-width,:-width])>0
        outside=int((diff&~mask).sum())
        if outside:
            exact=exact_boss_source_pairs(old,im,dd)
            if exact:
                camera_source_checks.append(dict(frame=n,**exact));stats['exact_surface_source_pair_pass']+=1
            else:failures.append(dict(frame=n,room=dd['room'],pixels=outside))
        else:stats['surface_bounds_pass']+=1
    if not old.any():assert not im.any();stats['blackouts_exact']+=1
    if dd['room']in ['FFFF','0000']and all(data[frames[j]]['room']==dd['room']for j in range(max(0,idx-1),min(len(frames),idx+2))):assert not diff.any();stats['menus_cards_exact']+=1
    if dd['room']in ['850A','8672','86EA','8762']and all(data[frames[j]]['room']==dd['room']for j in range(max(0,idx-1),min(len(frames),idx+2))):assert not diff.any();stats['opening_images_exact']+=1
    if dd['room']=='9F92'and diff.any():
        hits=matches(im,book)
        if hits:bookhits.append(dict(frame=n,positions=hits))
report=dict(movie=infos[1],native_samples_per_type=len(frames),native_exact=True,apu_exact=True,pcm_exact=True,apu_sha256=hashlib.sha256(apu).hexdigest(),pcm_sha256=hashlib.sha256(pcm).hexdigest(),statistics=dict(stats),rooms=dict(roomstats),book_source_matches=bookhits,camera_source_pair_checks=camera_source_checks,changed_pixel_bounds_failures=failures)
Path(a.out).write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:v for k,v in report.items()if k!='book_source_matches'},indent=2))
assert not failures,failures[:20]
if '9F92'in roomstats:assert len(bookhits)>5,'Book needs visible whole-source matches'
