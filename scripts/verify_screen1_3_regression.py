"""Require byte-identical title/reset and earlier crypt visuals and behavior."""
from pathlib import Path
import argparse
import hashlib
import json

p=argparse.ArgumentParser()
for name in ['before','after','out']:p.add_argument('--'+name,required=True)
a=p.parse_args()
result={}
for case,frames,samples in [('title',1800,450),('enemy',360,180)]:
    b,c=Path(a.before)/case,Path(a.after)/case
    assert (b/'completed.txt').read_text()==(c/'completed.txt').read_text()==str(frames)
    report={'emulated_frames':frames}
    for ext in ['ram','ppu','oam']:
        files=sorted((b/'dumps').glob('*.'+ext))
        assert len(files)==samples,(case,ext,len(files))
        assert all(v.read_bytes()==(c/'dumps'/v.name).read_bytes() for v in files),(case,ext)
        report[ext+'_identical_samples']=len(files)
    images=list((b/'frames').glob('*.png'))
    assert images and all(v.read_bytes()==(c/'frames'/v.name).read_bytes() for v in images),case+' image mismatch'
    report['identical_screenshots']=len(images)
    assert (b/'apu.tsv').read_bytes()==(c/'apu.tsv').read_bytes()
    report['apu_sha256']=hashlib.sha256((c/'apu.tsv').read_bytes()).hexdigest()
    bp,cp=(b/'full.wav').read_bytes()[44:],(c/'full.wav').read_bytes()[44:]
    # Fresh/reset runs can flush one additional final audio buffer at shutdown.
    # Every overlapping byte must agree; never align, skip or resample audio.
    common=min(len(bp),len(cp))
    assert common>0 and bp[:common]==cp[:common],case+' PCM mismatch'
    assert abs(len(bp)-len(cp))<=3200,case+' audio duration mismatch'
    report.update(identical_pcm_bytes=common,before_pcm_bytes=len(bp),after_pcm_bytes=len(cp),
                  shutdown_tail_difference_bytes=abs(len(bp)-len(cp)))
    result[case]=report
out=Path(a.out);out.parent.mkdir(parents=True,exist_ok=True)
out.write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
