"""Verify previous boss/reward/recovery scenes remain exact outside Stage 2."""
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
routes=json.loads((root/'scripts/screen2_1_regression_routes.json').read_text())
old=json.loads((root/'evidence/0.3.5-pack-sha256.json').read_text())
expected=json.loads((root/'evidence/approved-pack-sha256.json').read_text())
report=dict(baseline='0.3.5',candidate='0.4.0',controller_only=True,capture_interval_frames=2,cases={})
for case,route in routes.items():
    b,c=Path(a.before)/case,Path(a.after)/case;frames=route['frames']
    assert (b/'completed.txt').read_text()==(c/'completed.txt').read_text()==str(frames)
    assert (b/'input.json').read_bytes()==(c/'input.json').read_bytes()
    assert json.loads((b/'installed_pack_sha256.json').read_text())==old
    assert json.loads((c/'installed_pack_sha256.json').read_text())==expected
    r=dict(emulated_frames=frames,**json.loads((c/'input.json').read_text()))
    assert r['controller_route']==route['input']
    for ext in ['ram','ppu','oam']:
        files=sorted((b/'dumps').glob('*.'+ext));assert len(files)==frames//2
        for f in files:assert f.read_bytes()==(c/'dumps'/f.name).read_bytes(),(case,ext,f.name)
        r[ext+'_identical_samples']=len(files)
    apu=(b/'apu.tsv').read_bytes();assert apu==(c/'apu.tsv').read_bytes(),case+' APU'
    r['apu_sha256']=hashlib.sha256(apu).hexdigest()
    bp,cp=(b/'full.wav').read_bytes()[44:],(c/'full.wav').read_bytes()[44:]
    common=min(len(bp),len(cp));assert common and bp[:common]==cp[:common],case+' PCM'
    assert abs(len(bp)-len(cp))<=3200,case+' PCM duration'
    r.update(identical_pcm_bytes=common,shutdown_tail_difference_bytes=abs(len(bp)-len(cp)))
    unchanged=changed=outside=0;rooms=Counter()
    room={n:(c/'dumps'/f'{n:04}.ram').read_bytes()[0x72]for n in range(2,frames+1,2)}
    for n in range(2,frames+1,2):
        f=b/'frames'/f'{n:04}.png';g=c/'frames'/f'{n:04}.png'
        equal=np.array_equal(np.array(Image.open(f)),np.array(Image.open(g)))
        unchanged+=equal;changed+=not equal;rooms[f'{room[n]:02X}']+=1
        neighboring=[room[v]for v in [n-2,n,n+2]if v in room]
        if 0x18 not in neighboring:
            assert equal,(case,n,'previous scene changed');outside+=1
    if case!='blizzard_reward':assert changed==0
    r.update(identical_screenshots=unchanged,changed_screenshots=changed,
             exact_previous_scene_screenshots=outside,rooms=dict(rooms))
    report['cases'][case]=r
report.update(total_frames_per_build=sum(v['frames']for v in routes.values()),
              paired_samples_per_memory_type=sum(v['frames']//2 for v in routes.values()),
              exact_previous_scene_screenshots=sum(v['exact_previous_scene_screenshots']for v in report['cases'].values()))
out=Path(a.out);out.parent.mkdir(parents=True,exist_ok=True);out.write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({k:v for k,v in report.items()if k!='cases'},indent=2))
