"""Retain the recorded platform landing, then slowly walk off its right edge."""
from pathlib import Path
import argparse,zipfile,json,hashlib
p=argparse.ArgumentParser();p.add_argument('--movie',required=True);p.add_argument('--out',required=True);a=p.parse_args()
source=Path(a.movie);out=Path(a.out);assert hashlib.sha256(source.read_bytes()).hexdigest()=='36de8a08dcc84610fe5567c01530cf8038816c4607536b304a38929ce3cf9699'
with zipfile.ZipFile(source)as z:entries={n:z.read(n)for n in z.namelist()}
rows=entries['Input.txt'].decode().splitlines()[:1840]
rows+=['|..|........|........']*10
rows+=(['|..|...R....|........']*3+['|..|........|........'])*30
rows+=['|..|........|........']*30
raw=('\n'.join(rows)+'\n').encode();out.parent.mkdir(parents=True,exist_ok=True)
with zipfile.ZipFile(out,'w',zipfile.ZIP_DEFLATED)as z:
 for name,value in entries.items():z.writestr(name,raw if name=='Input.txt'else value)
report=dict(frames=len(rows),sha256=hashlib.sha256(out.read_bytes()).hexdigest(),source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),controller_only=True,unchanged_embedded_state=True,neutral_stop=[1841,1850],slow_right=[1851,1970],no_jump_after=1840)
out.with_suffix('.json').write_text(json.dumps(report,indent=2)+'\n')
