"""Controller-only traversal of the final climb's left platform, ending in a walk-off."""
from pathlib import Path
import argparse,zipfile,json,hashlib
p=argparse.ArgumentParser();p.add_argument('movie');p.add_argument('out');a=p.parse_args()
src,out=Path(a.movie),Path(a.out);out.parent.mkdir(parents=True,exist_ok=True)
with zipfile.ZipFile(src)as z:entries={n:z.read(n)for n in z.namelist()}
rows=entries['Input.txt'].decode().splitlines()
def hold(keys,n):return ['|..|'+''.join(c if c in keys else '.'for c in 'UDLRSsBA')+'|........']*n
inputs=rows[:1240]+hold('L',100)+hold('',30)+(hold('R',2)+hold('',2))*80+hold('',50)
raw=('\n'.join(inputs)+'\n').encode()
with zipfile.ZipFile(out,'w',zipfile.ZIP_DEFLATED)as z:
 for key,val in entries.items():z.writestr(key,raw if key=='Input.txt'else val)
out.with_suffix('.json').write_text(json.dumps(dict(frames=len(inputs),movie_sha256=hashlib.sha256(out.read_bytes()).hexdigest(),input_sha256=hashlib.sha256(raw).hexdigest(),source_movie_sha256=hashlib.sha256(src.read_bytes()).hexdigest(),state_sha256=hashlib.sha256(entries['SaveState.mss']).hexdigest(),controller_only=True),indent=2)+'\n')
