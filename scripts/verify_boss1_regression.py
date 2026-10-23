"""Require unchanged title, crypt, nave and tree-court replay images and behavior."""
from pathlib import Path
import argparse
import hashlib
import json

p=argparse.ArgumentParser()
for name in ['before','after','out']:p.add_argument('--'+name,required=True)
a=p.parse_args();report={}
root=Path(__file__).resolve().parents[1]
expected=json.loads((root/'evidence/approved-pack-sha256.json').read_text())
baseline=json.loads((root/'evidence/0.2.1-pack-sha256.json').read_text())
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
    for f in images:assert f.read_bytes()==(c/'frames'/f.name).read_bytes(),(case,'image',f.name)
    r['identical_screenshots']=len(images)
    apu=(b/'apu.tsv').read_bytes();assert apu==(c/'apu.tsv').read_bytes()
    r['apu_sha256']=hashlib.sha256(apu).hexdigest()
    bp,cp=(b/'full.wav').read_bytes()[44:],(c/'full.wav').read_bytes()[44:]
    common=min(len(bp),len(cp));assert common and bp[:common]==cp[:common]
    assert abs(len(bp)-len(cp))<=3200,(case,'audio duration')
    r.update(identical_pcm_bytes=common,before_pcm_bytes=len(bp),after_pcm_bytes=len(cp),shutdown_tail_difference_bytes=abs(len(bp)-len(cp)))
    report[case]=r
out=Path(a.out);out.parent.mkdir(parents=True,exist_ok=True);out.write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
