"""Test the opening platform from its original left-edge standing position."""
from pathlib import Path
import argparse,zipfile,json,hashlib
p=argparse.ArgumentParser();p.add_argument('--movie',required=True);p.add_argument('--out',required=True);a=p.parse_args()
source=Path(a.movie);out=Path(a.out)
assert hashlib.sha256(source.read_bytes()).hexdigest()=='dc34b2903fe282ebe33c115f845803638dca33f4b6bbb2cc67e852f1ecdcbeed'
with zipfile.ZipFile(source)as z:entries={n:z.read(n)for n in z.namelist()}
neutral='|..|........|........';right='|..|...R....|........'
rows=[neutral]*60+([right]*3+[neutral])*20+[neutral]*40
raw=('\n'.join(rows)+'\n').encode();out.parent.mkdir(parents=True,exist_ok=True)
with zipfile.ZipFile(out,'w',zipfile.ZIP_DEFLATED)as z:
 for name,value in entries.items():z.writestr(name,raw if name=='Input.txt'else value)
report=dict(frames=len(rows),sha256=hashlib.sha256(out.read_bytes()).hexdigest(),
 source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),controller_only=True,
 unchanged_embedded_state=True,left_edge_stop=[1,60],slow_right=[61,140],no_jump=True)
out.with_suffix('.json').write_text(json.dumps(report,indent=2)+'\n')
