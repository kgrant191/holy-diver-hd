"""Reach the corridor floor's left edge, stop, then slowly walk right off it."""
from pathlib import Path
import argparse,zipfile,json,hashlib
p=argparse.ArgumentParser();p.add_argument('--movie',required=True);p.add_argument('--out',required=True);a=p.parse_args()
source=Path(a.movie);out=Path(a.out)
assert hashlib.sha256(source.read_bytes()).hexdigest()=='298aa05c6ec3073d4db22596b5072721836d008a591e527b69e85b5d687c6bb9'
with zipfile.ZipFile(source)as z:entries={n:z.read(n)for n in z.namelist()}
neutral='|..|........|........';left='|..|..L.....|........';right='|..|...R....|........'
rows=entries['Input.txt'].decode().splitlines()[:1400]+[left]*26+[neutral]*60+([right]*3+[neutral])*55+[neutral]*60
raw=('\n'.join(rows)+'\n').encode();out.parent.mkdir(parents=True,exist_ok=True)
with zipfile.ZipFile(out,'w',zipfile.ZIP_DEFLATED)as z:
 for name,value in entries.items():z.writestr(name,raw if name=='Input.txt'else value)
out.with_suffix('.json').write_text(json.dumps(dict(frames=len(rows),sha256=hashlib.sha256(out.read_bytes()).hexdigest(),
 source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),controller_only=True,unchanged_embedded_state=True,
 original_prefix=1400,left_walk=[1401,1426],left_stop=[1427,1486],slow_right=[1487,1706],no_jump_after_branch=True),indent=2)+'\n')
