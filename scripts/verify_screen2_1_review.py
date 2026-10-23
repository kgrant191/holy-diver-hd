"""Pair 0.4.0/0.4.1 captures; constrain changes to enemies and cave opening."""
from pathlib import Path
import argparse, hashlib, json, re
from collections import Counter
import numpy as np
from PIL import Image

p=argparse.ArgumentParser()
for n in ['before','after','cave-before','cave-after','out']:p.add_argument('--'+n,required=True)
a=p.parse_args();root=Path(__file__).resolve().parents[1]
old=json.loads((root/'evidence/0.4.0-pack-sha256.json').read_text())
new=json.loads((root/'evidence/approved-pack-sha256.json').read_text())
routes=json.loads((root/'scripts/screen2_1_routes.json').read_text())
routes['walk_right']={'frames':420,'input':'right=frame>=20'}
report={'baseline':'0.4.0','candidate':'0.4.1','controller_only':True,'cases':{}}
observed=set();movement=Counter();cave_clear_samples=0
def enemy(t,attr):
    return (0x7a<=t<=0x8d and attr&3==1) or (0xde<=t<=0xf8 and attr&3==0)
for case,route in routes.items():
    b,c=(Path(a.cave_before)/case,Path(a.cave_after)/case) if case=='walk_right' else (Path(a.before)/case,Path(a.after)/case)
    frames=route['frames']
    assert (b/'completed.txt').read_text()==(c/'completed.txt').read_text()==str(frames)
    assert (b/'input.json').read_bytes()==(c/'input.json').read_bytes()
    assert json.loads((b/'installed_pack_sha256.json').read_text())==old
    assert json.loads((c/'installed_pack_sha256.json').read_text())==new
    r=dict(frames=frames,**json.loads((c/'input.json').read_text()))
    assert r['controller_route']==route['input']
    for ext in ['ram','ppu','oam']:
        files=sorted((b/'dumps').glob('*.'+ext));assert len(files)==frames
        for f in files:assert f.read_bytes()==(c/'dumps'/f.name).read_bytes(),(case,f.name)
        r[ext+'_identical_samples']=len(files)
    apu=(b/'apu.tsv').read_bytes();assert apu==(c/'apu.tsv').read_bytes()
    r['apu_sha256']=hashlib.sha256(apu).hexdigest()
    bp,cp=(b/'full.wav').read_bytes()[44:],(c/'full.wav').read_bytes()[44:]
    common=min(len(bp),len(cp));assert common and bp[:common]==cp[:common],(case,'PCM')
    tail=abs(len(bp)-len(cp));assert tail<=3200,(case,'audio tail',tail)
    r.update(identical_pcm_bytes=common,shutdown_tail_bytes=tail)
    changed=exact=black=outside=0;previous=None;opened=0
    for n in range(2,frames+1):
        name=f'{n:04}'
        before=np.array(Image.open(b/'frames'/f'{name}.png').convert('RGB'))
        after=np.array(Image.open(c/'frames'/f'{name}.png').convert('RGB'))
        diff=np.any(before!=after,axis=2)
        ram=(c/'dumps'/f'{name}.ram').read_bytes();room=ram[0x72]
        scroll=int.from_bytes(ram[0x60:0x62],'little')
        mask=np.zeros(diff.shape,dtype=bool);sprites=np.zeros(diff.shape,dtype=bool)
        # Screenshots are authoritative; endFrame OAM can describe the next
        # pose. Include adjacent native OAM samples for the changed-pixel bound.
        for j in range(max(1,n-1),min(frames,n+1)+1):
            rr=(c/'dumps'/f'{j:04}.ram').read_bytes()
            oo=(c/'dumps'/f'{j:04}.oam').read_bytes()
            for i in range(0,256,4):
                y,t,attr,x=oo[i:i+4]
                if y>=239:continue
                box=(slice(max(0,2*(y+1)-2),min(480,2*(y+9)+2)),slice(max(0,2*x-2),min(512,2*(x+8)+2)))
                sprites[box]=True
                if rr[0x72]==0x18 and enemy(t,attr):mask[box]=True
        if room==0x18:
            # World-space doorway, four native columns and six blank rows.
            x1,x2=2*(1488-scroll),2*(1520-scroll)
            mask[286:386,max(0,x1-4):max(0,min(512,x2+4))]=True
            oo=(c/'dumps'/f'{name}.oam').read_bytes()
            flyers=[]
            for i in range(0,256,4):
                y,t,attr,x=oo[i:i+4]
                if y<239 and enemy(t,attr):observed.add((t,bool(attr&64)))
                if y<239 and t==0x7c and attr&3==1:flyers.append((x,bool(attr&64),scroll))
            if len(flyers)==1:
                now=flyers[0]
                # Compare direction only with a stable camera. endFrame RAM
                # scroll and rendered OAM have different phases while scrolling.
                stable_camera=all(int.from_bytes((c/'dumps'/f'{j:04}.ram').read_bytes()[0x60:0x62],'little')==scroll
                                  for j in range(max(1,n-2),min(frames,n+2)+1))
                if previous and previous[1:]==now[1:] and stable_camera:
                    dx=now[0]-previous[0]
                    if abs(dx) in [1,2]:movement[('right' if dx>0 else 'left')+('/mirrored' if now[1] else '/native')]+=1
                previous=now
            else:previous=None
            # On the new approach, test the visible interior while Randy is
            # still outside, before the fade/room transition begins.
            if case=='walk_right' and n<=130 and x1<512:
                # The displayed camera lags the endFrame RAM sample by two
                # frames; use that rendered scroll, verified at the jamb edge.
                rendered=(c/'dumps'/f'{max(1,n-2):04}.ram').read_bytes()
                rendered_scroll=int.from_bytes(rendered[0x60:0x62],'little')
                rx1,rx2=2*(1488-rendered_scroll),2*(1520-rendered_scroll)
                region=np.zeros(diff.shape,dtype=bool)
                region[290:382,max(0,rx1):min(512,rx2)]=True
                region &= ~sprites
                if region.any():
                    assert after[region].max()==0,(case,n,'cloud inside cave')
                    opened+=1;cave_clear_samples+=1
        else:
            # A one-frame room switch may still display the previous room.
            neighbors=[(c/'dumps'/f'{j:04}.ram').read_bytes()[0x72] for j in range(max(1,n-2),min(frames,n+2)+1)]
            if all(v!=0x18 for v in neighbors):assert not diff.any(),(case,n,'outside room changed');outside+=1
            else:mask[:]=True
        assert not (diff&~mask).any(),(case,n,'changed pixels outside requested scope',int((diff&~mask).sum()))
        if before.max()==0:assert after.max()==0;black+=1
        changed+=bool(diff.any());exact+=not diff.any()
    r.update(changed_screenshots=changed,exact_screenshots=exact,exact_black_frames=black,exact_outside_room=outside,cave_dark_samples=opened)
    report['cases'][case]=r
for t in list(range(0x7a,0x8e))+list(range(0xde,0xf9)):
    assert any(v[0]==t for v in observed),f'missing enemy tile {t:02X}'
assert movement['left/native']>30 and movement['right/mirrored']>30
assert not movement['right/native'] and not movement['left/mirrored'],movement
assert cave_clear_samples>50
assert sorted(k for k in new if new[k]!=old.get(k))==['README.txt','Stage2_Exterior_Tiles_2x.png','hires.txt']
report.update(total_frames_per_build=sum(v['frames'] for v in routes.values()),unchanged_pack_files=79,
              cave_dark_samples=cave_clear_samples,demon_motion_static_camera=dict(movement),
              enemy_tiles_and_flips=[f'{t:02X}/'+('mirrored' if f else 'native') for t,f in sorted(observed)])
out=Path(a.out);out.parent.mkdir(parents=True,exist_ok=True);out.write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({k:v for k,v in report.items() if k not in ['cases','enemy_tiles_and_flips']},indent=2))
