"""Branch at the new carved-cap entrance for a controller-only edge traversal."""
from pathlib import Path
import argparse,zipfile,json,hashlib
p=argparse.ArgumentParser();p.add_argument('movie');p.add_argument('out');a=p.parse_args()
src=Path(a.movie);out=Path(a.out);out.parent.mkdir(parents=True,exist_ok=True)
with zipfile.ZipFile(src)as z:entries={n:z.read(n)for n in z.namelist()}
rows=entries['Input.txt'].decode().splitlines()
def line(buttons):return '|..|'+''.join(c if c in buttons else '.'for c in 'UDLRSsBA')+'|........'
def hold(buttons,n):return [line(buttons)]*n
inputs=rows[:5470]+hold('L',60)+hold('',30)+(hold('R',2)+hold('',2))*100+hold('',40)
raw=('\n'.join(inputs)+'\n').encode()
with zipfile.ZipFile(out,'w',zipfile.ZIP_DEFLATED)as z:
 for key,value in entries.items():z.writestr(key,raw if key=='Input.txt'else value)
out.with_suffix('.json').write_text(json.dumps(dict(frames=len(inputs),movie_sha256=hashlib.sha256(out.read_bytes()).hexdigest(),input_sha256=hashlib.sha256(raw).hexdigest(),source_movie_sha256=hashlib.sha256(src.read_bytes()).hexdigest(),state_sha256=hashlib.sha256(entries['SaveState.mss']).hexdigest(),controller_only=True),indent=2)+'\n')
