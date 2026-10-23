"""Check paired gameplay/audio, native flashes, coverage and previous-art bounds."""
from pathlib import Path
import argparse
import hashlib
import json
from collections import Counter
import numpy as np
from PIL import Image

p=argparse.ArgumentParser()
for name in ['before','after','out']:p.add_argument('--'+name,required=True)
a=p.parse_args();root=Path(__file__).resolve().parents[1]
routes=json.loads((root/'scripts/screen2_1_routes.json').read_text())
old=json.loads((root/'evidence/0.3.5-pack-sha256.json').read_text())
expected=json.loads((root/'evidence/approved-pack-sha256.json').read_text())
report=dict(emulator='MesenCE 2.2.1',baseline='0.3.5',candidate='0.4.0',controller_only=True,cases={})
observed=set();palettes=Counter();max_scroll=0;all_black=0
for case,route in routes.items():
    b,c=Path(a.before)/case,Path(a.after)/case;frames=route['frames']
    assert (b/'completed.txt').read_text()==(c/'completed.txt').read_text()==str(frames)
    assert (b/'input.json').read_bytes()==(c/'input.json').read_bytes()
    assert json.loads((b/'installed_pack_sha256.json').read_text())==old
    assert json.loads((c/'installed_pack_sha256.json').read_text())==expected
    r=dict(emulated_frames=frames,**json.loads((c/'input.json').read_text()))
    assert r['controller_route']==route['input'],case+' stale controller route'
    for ext in ['ram','ppu','oam']:
        files=sorted((b/'dumps').glob('*.'+ext));assert len(files)==frames
        for f in files:assert f.read_bytes()==(c/'dumps'/f.name).read_bytes(),(case,ext,f.name)
        r[ext+'_identical_samples']=frames
    apu=(b/'apu.tsv').read_bytes();assert apu==(c/'apu.tsv').read_bytes(),case+' APU'
    r['apu_sha256']=hashlib.sha256(apu).hexdigest()
    bp,cp=(b/'full.wav').read_bytes()[44:],(c/'full.wav').read_bytes()[44:]
    common=min(len(bp),len(cp));assert common and bp[:common]==cp[:common],case+' PCM'
    assert abs(len(bp)-len(cp))<=3200,case+' PCM duration'
    r.update(identical_pcm_bytes=common,shutdown_tail_difference_bytes=abs(len(bp)-len(cp)))
    changed=black=unchanged=outside=0;pool_states=Counter();drops=Counter();rooms=Counter()
    for n in range(1,frames+1):
        stem=f'{n:04}';f=b/'frames'/f'{stem}.png';g=c/'frames'/f'{stem}.png'
        ram=(c/'dumps'/f'{stem}.ram').read_bytes();ppu=(c/'dumps'/f'{stem}.ppu').read_bytes();oam=(c/'dumps'/f'{stem}.oam').read_bytes()
        rooms[f'{ram[0x72]:02X}']+=1
        if ram[0x72]==0x18:
            max_scroll=max(max_scroll,int.from_bytes(ram[0x60:0x62],'little'))
            pool_states[ppu[0x3f04:0x3f08].hex().upper()]+=1
            for i in range(0,256,4):
                y,t,attr,x=oam[i:i+4]
                if y>=239:continue
                if t>=0x7a and t<=0x8d and attr&3==1:observed.add((t,bool(attr&64)))
                if t>=0xde and t<=0xf8 and attr&3==0:observed.add((t,bool(attr&64)))
                if t in [0x47,0x48,0x49,0x4a,0x4b,0x4c,0x4e,0x4f,0x74] and attr&3 in [2,3]:drops[f'{t:02X}']+=1
        if not f.stat().st_size or not g.stat().st_size:
            assert n==1
            continue
        original=np.array(Image.open(f).convert('RGB'))
        candidate=np.array(Image.open(g).convert('RGB'))
        equal=np.array_equal(original,candidate)
        changed+=not equal;unchanged+=equal
        if original.max()==0:
            black+=1;assert candidate.max()==0,(case,n,'native blackout lost')
        if ram[0x72]!=0x18 and 3<n<frames-3:
            neighbors=[(c/'dumps'/f'{v:04}.ram').read_bytes()[0x72]for v in range(n-2,n+3)]
            if all(v!=0x18 for v in neighbors):
                assert equal,(case,n,'outside-room artwork changed');outside+=1
        if case=='menu' and 40<n<175:
            assert equal,(case,n,'approved pause menu changed')
    r.update(changed_screenshots=changed,identical_screenshots=unchanged,
             exact_native_blackouts=black,exact_outside_room_screenshots=outside,
             pool_palette_samples=dict(pool_states),observed_drop_tiles=dict(drops),rooms=dict(rooms))
    if case=='cast_thaw':
        assert black==92
        assert set(pool_states)=={'0F161606','0F060616','0F122131'}
        assert '74' in drops
    report['cases'][case]=r;all_black+=black;palettes.update(pool_states)
assert max_scroll>=1280,max_scroll
for t in list(range(0x7a,0x8e))+list(range(0xde,0xf9)):
    assert any(v[0]==t for v in observed),f'unobserved enemy tile {t:02X}'
# The native tumbling creature uses three rotated poses, never OAM horizontal
# mirroring in these routes. Require every native tile rather than inventing a
# mirrored pose that the original gameplay does not produce.
assert {flip for t,flip in observed if 0xde<=t<=0xf8}=={False}
assert all(any(v[1]==flip and 0x7a<=v[0]<=0x8b for v in observed) for flip in [False,True])
assert sorted(expected.keys()-old.keys())==['Stage2_Exterior_Background.png','Stage2_Exterior_Tiles_2x.png']
assert sorted(k for k in old if old[k]!=expected[k])==['README.txt','hires.txt']
report.update(total_frames_per_build=sum(v['frames']for v in routes.values()),
              maximum_horizontal_scroll=max_scroll,exact_native_blackouts=all_black,
              unchanged_approved_runtime_files=78,pack_files=len(expected),
              lava_creature_coverage='All three native poses; no native OAM mirroring observed',
              imp_coverage='All animation/projectile tiles; both native directions',
              enemy_tiles_and_flips=[f'{t:02X}/'+('mirrored' if flip else 'native')for t,flip in sorted(observed)])
out=Path(a.out);out.parent.mkdir(parents=True,exist_ok=True);out.write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({k:v for k,v in report.items()if k not in ['cases','enemy_tiles_and_flips']},indent=2))
