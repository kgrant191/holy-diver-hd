"""Verify earlier rooms; allow only restored sprites on overflowing nave scanlines."""
from pathlib import Path
import argparse
import hashlib
import json
import numpy as np
from PIL import Image

p=argparse.ArgumentParser()
for name in ['before','after','out']:p.add_argument('--'+name,required=True)
a=p.parse_args();report={}
root=Path(__file__).resolve().parents[1]
expected=json.loads((root/'evidence/approved-pack-sha256.json').read_text())
baseline=json.loads((root/'evidence/0.3.0-pack-sha256.json').read_text())
for case,frames,samples in [('title',1800,450),('enemy',360,180),('nave',500,500),('tree',700,700)]:
    b,c=Path(a.before)/case,Path(a.after)/case
    assert (b/'completed.txt').read_text()==(c/'completed.txt').read_text()==str(frames)
    assert json.loads((b/'installed_pack_sha256.json').read_text())==baseline
    assert json.loads((c/'installed_pack_sha256.json').read_text())==expected
    r={'emulated_frames':frames}
    for ext in ['ram','ppu','oam']:
        files=sorted((b/'dumps').glob('*.'+ext));assert len(files)==samples
        for f in files:assert f.read_bytes()==(c/'dumps'/f.name).read_bytes(),(case,ext,f.name)
        r[ext+'_identical_samples']=samples
    images=sorted((b/'frames').glob('*.png'));assert images
    changed=[]
    for f in images:
        after=c/'frames'/f.name
        if f.read_bytes()==after.read_bytes():continue
        assert case=='nave',(case,'unexpected visual change',f.name)
        before_im=np.array(Image.open(f).convert('RGB'))
        after_im=np.array(Image.open(after).convert('RGB'))
        diff=np.any(before_im!=after_im,axis=2)
        o=(c/'dumps'/f'{int(f.stem)-1:04}.oam').read_bytes()
        native=np.zeros(diff.shape,bool);counts=np.zeros(240,int)
        for i in range(0,256,4):
            y,t,attr,x=o[i:i+4]
            if y<239:
                counts[y+1:min(240,y+9)]+=1
                native[(y+1)*2:min(480,(y+9)*2),x*2:min(512,(x+8)*2)]=True
        overflow=np.repeat(counts>8,2)[:,None]
        assert not np.any(diff&~(native&overflow)),f.name+' changed outside native sprite overflow'
        changed.append(int(f.stem))
    r.update(identical_screenshots=len(images)-len(changed),restored_sprite_screenshots=len(changed))
    if changed:
        r['restored_sprite_frames']=changed
        r['changes_only_on_native_overflow_scanlines']=True
    apu=(b/'apu.tsv').read_bytes();assert apu==(c/'apu.tsv').read_bytes()
    r['apu_sha256']=hashlib.sha256(apu).hexdigest()
    bp,cp=(b/'full.wav').read_bytes()[44:],(c/'full.wav').read_bytes()[44:]
    common=min(len(bp),len(cp));assert common and bp[:common]==cp[:common]
    assert abs(len(bp)-len(cp))<=3200,(case,'audio duration')
    r.update(identical_pcm_bytes=common,before_pcm_bytes=len(bp),after_pcm_bytes=len(cp),shutdown_tail_difference_bytes=abs(len(bp)-len(cp)))
    report[case]=r
assert report['nave']['restored_sprite_screenshots']==39
out=Path(a.out);out.parent.mkdir(parents=True,exist_ok=True);out.write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
