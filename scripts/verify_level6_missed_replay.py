"""Verify every native/audio sample and actual room art through the missed-room movie."""
from pathlib import Path
from collections import Counter
import argparse,hashlib,json,wave
import numpy as np
from PIL import Image
from verify_level6_opening_replay import source,matches,variants

p=argparse.ArgumentParser()
for k in ['before','after','out']:p.add_argument('--'+k,required=True)
a=p.parse_args();root=Path(__file__).resolve().parents[1];b,c=Path(a.before),Path(a.after)
infos=[json.loads((d/'result.json').read_text())for d in [b,c]]
for k in ['movie_sha256','rom_sha1','core_sha256','movie_frames','captured_frames','stride']:assert infos[0][k]==infos[1][k],k
assert all(i['movie_completed']and i['movie_frames']==8998 and i['captured_frames']==8998 and i['stride']==1 for i in infos)
for d,version in [(b,'0.30.1'),(c,'0.31.0')]:assert json.loads((d/'installed_pack.json').read_text())==json.loads((root/f'evidence/{version}-pack-sha256.json').read_text())
apu=(b/'apu.tsv').read_bytes();assert apu==(c/'apu.tsv').read_bytes()
with wave.open(str(b/'full.wav'))as f:params=f.getparams();pcm=f.readframes(f.getnframes())
with wave.open(str(c/'full.wav'))as f:assert f.getparams()==params and f.readframes(f.getnframes())==pcm
reg=json.loads((root/'art/level6_missed/registration.json').read_text());scopes={'9CA7':0x0c,'9D5B':8,'9DD3':0x18}
pack=c/'mesen_home/HdPacks/Holy_Diver_(Tr)';backgrounds={}
for style,_ in reg['styles'].values():
    bg=np.array(Image.open(pack/f'Final_Citadel_{style}.png').convert('RGB'));backgrounds[style,'0F']=variants(bg)
    for phase,color in [('30',[255,254,255]),('31',[194,223,255])]:
        blend=(bg.astype(np.uint32)*176//255+np.array(color)*80//256).astype(np.uint8);backgrounds[style,phase]=variants(blend)
paths={n:root/f'art/level6_missed/{n}.png'for n in ['red_brick','violet_brick','violet_ceiling_body','violet_ceiling_lip','violet_ceiling_corner','violet_hanging_edge']}
paths.update({'eye':root/'art/screen2_3/eye_registered.png',**{f'tear_{t}':root/f'art/screen2_3/eye_shot_{t}.png'for t in ['02DC','02DD']}})
paths.update({f'dragon_{i}':root/f'art/level4_dragon/pose_{i}.png'for i in range(3)})
paths.update({f'thunder_{i}':root/f'art/level5/thunder_{i}.png'for i in range(3)})
paths.update({f'serpent_{s}':root/f'art/level5/serpent_{s}.png'for s in ['head','segment']})
sources={name:[source(path,m)for m in [False,True]]for name,path in paths.items()};hits={};stats=Counter();roomstats=Counter();bgstats={};missing=[];boundaries=[];flashhits=[]
menu_reference=np.array(Image.open(b/'frames/000020.png').convert('RGB'))[106:136,60:480];prev=None
for n in range(1,8999):
    d={}
    for kind in ['ram','ppu','oam','view']:
        name=f'{n:06}'+('.json'if kind=='view'else'.bin');raw=(c/kind/name).read_bytes();assert raw==(b/kind/name).read_bytes(),(n,kind)
        d[kind]=json.loads(raw)if kind=='view'else raw
    room=f'{int.from_bytes(d["ram"][0x78:0x7a],"little"):04X}';previous=prev or d;proom=f'{int.from_bytes(previous["ram"][0x78:0x7a],"little"):04X}';roomstats[room]+=1
    oldp,newp=b/f'frames/{n:06}.png',c/f'frames/{n:06}.png'
    if not oldp.stat().st_size:assert not newp.stat().st_size;stats['initial_empty']+=1;prev=d;continue
    old,im=[np.array(Image.open(f).convert('RGB'))for f in [oldp,newp]];different=not np.array_equal(old,im);stats['changed'if different else'identical']+=1
    menu=np.array_equal(old[106:136,60:480],menu_reference)
    blackout=not old.any()
    if menu:assert not different,(n,'menu changed');stats['menus_exact']+=1
    if blackout:assert not im.any(),(n,'blackout changed');stats['blackouts_exact']+=1
    active=[(rr,dd)for rr,dd in [(room,d),(proom,previous)]if rr in scopes and dd['ram'][0x72]==scopes[rr]]
    if not active:assert not different,(n,'outside requested rooms');stats['outside_scope_exact']+=1
    if room=='9F3B'and proom=='9F3B':assert not different,(n,'accepted next room');stats['accepted_next_room_exact']+=1
    if room=='0000'and proom=='0000':assert not different,(n,'death card');stats['death_card_exact']+=1
    if different:
        assert active and not menu and not blackout
        choices=[]
        for rr,dd in active:
            style=reg['styles'][rr][0];phase=f'{dd["ppu"][0x3f00]:02X}'
            if phase not in ['0F','30','31']:continue
            if rr=='9D5B'and dd['ppu'][0x3f01:0x3f04].hex()=='061636':style='Crimson_Gallery'
            choices.append((style,phase,dd['view']['grayscale']))
        best=0;bestkey=None
        for style,phase,gray in dict.fromkeys(choices):
            vs=backgrounds[style,phase];vs=vs[8:]if gray else vs[:8]
            for v in vs:
                count=int(np.all(im==v,2).sum())
                if count>best:best,bestkey=count,(style,phase)
                if best>5000:break
            if best>5000:break
        if best<5000:missing.append([n,room,best,choices])
        else:
            key='/'.join(bestkey);bgstats.setdefault(key,[]).append(best)
            if bestkey[1]!='0F':flashhits.append(n)
        if room not in scopes:boundaries.append([n,proom,room])
    if n%10==0 and active and not menu and not blackout:
        for name,ss in sources.items():
            if name in hits:continue
            for mirror,item in enumerate(ss):
                found=matches(im,item)
                if found:hits[name]=dict(frame=n,room=room,mirrored=bool(mirror),positions=found);break
    prev=d
    if n%2000==0:print('Verified',n,flush=True)
report=dict(movie=infos[1],native_samples_per_type=8998,native_exact=True,apu_exact=True,pcm_exact=True,apu_sha256=hashlib.sha256(apu).hexdigest(),pcm_sha256=hashlib.sha256(pcm).hexdigest(),render_assets_match_final_manifest=True,statistics=dict(stats),rooms=dict(roomstats),all_image_changes_within_requested_rooms=True,backgrounds={k:dict(samples=len(v),minimum_pixels=min(v))for k,v in bgstats.items()},missing_backgrounds=missing,flash_background_samples=len(flashhits),outgoing_boundaries=boundaries,whole_source_hits=hits,sources_not_observed_whole=sorted(set(sources)-set(hits)))
Path(a.out).write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
assert not missing,missing[:20]
assert all(k in hits for k in ['red_brick','violet_brick','violet_ceiling_body','violet_ceiling_lip','eye','serpent_head','serpent_segment'])
assert any(k.startswith('dragon_')for k in hits)and any(k.startswith('thunder_')for k in hits)
assert report['flash_background_samples']>0
