"""Check earlier title/crypt plus the approved nave against the candidate."""
from pathlib import Path
import argparse
import hashlib
import json
import subprocess
import sys

p=argparse.ArgumentParser()
for name in ['before','after','nave-before','nave-after','out']:
    p.add_argument('--'+name,required=True)
a=p.parse_args()
root=Path(__file__).resolve().parents[1]
subprocess.run([sys.executable,str(root/'scripts/verify_screen1_3_regression.py'),
                '--before',a.before,'--after',a.after,'--out',a.out],check=True)
b,c=Path(a.nave_before)/'state1',Path(a.nave_after)/'state1'
assert (b/'completed.txt').read_text()==(c/'completed.txt').read_text()=='720'
assert (b/'input.json').read_bytes()==(c/'input.json').read_bytes()
r={'emulated_frames':720}
for ext in ['ram','ppu','oam']:
    files=list((b/'dumps').glob('*.'+ext))
    assert len(files)==360
    assert all(f.read_bytes()==(c/'dumps'/f.name).read_bytes() for f in files),ext
    r[ext+'_identical_samples']=len(files)
files=list((b/'frames').glob('*.png'))
assert files and all(f.read_bytes()==(c/'frames'/f.name).read_bytes() for f in files)
r['identical_screenshots']=len(files)
assert (b/'apu.tsv').read_bytes()==(c/'apu.tsv').read_bytes()
r['apu_sha256']=hashlib.sha256((c/'apu.tsv').read_bytes()).hexdigest()
bp,cp=(b/'full.wav').read_bytes()[44:],(c/'full.wav').read_bytes()[44:]
common=min(len(bp),len(cp))
assert common and bp[:common]==cp[:common]
assert abs(len(bp)-len(cp))<=3200
r.update(identical_pcm_bytes=common,before_pcm_bytes=len(bp),after_pcm_bytes=len(cp),
         shutdown_tail_difference_bytes=abs(len(bp)-len(cp)))
out=Path(a.out);report=json.loads(out.read_text());report['nave_state1']=r
out.write_text(json.dumps(report,indent=2)+'\n')
print('Nave regression:',json.dumps(r))
