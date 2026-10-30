"""Controller-only stop at the hall platform's left edge, then slow right walk-off."""
from pathlib import Path
import argparse,zipfile,json,hashlib
p=argparse.ArgumentParser();p.add_argument('--movie',required=True);p.add_argument('--out',required=True);a=p.parse_args();source=Path(a.movie);out=Path(a.out)
assert hashlib.sha256(source.read_bytes()).hexdigest()=='30efe77656e6b464c92d1dd7f9dda448f1eb69ccc96bac1710a2ad7fa7e2d067'
with zipfile.ZipFile(source)as z:entries={n:z.read(n)for n in z.namelist()}
neutral='|..|........|........';left='|..|..L.....|........';right='|..|...R....|........'
rows=entries['Input.txt'].decode().splitlines()[:548]+[left]*17+[neutral]*10+([right]*3+[neutral])*34+[neutral]*20
with zipfile.ZipFile(out,'w',zipfile.ZIP_DEFLATED)as z:
 for n,b in entries.items():z.writestr(n,('\n'.join(rows)+'\n').encode()if n=='Input.txt'else b)
out.with_suffix('.json').write_text(json.dumps(dict(frames=len(rows),original_prefix=548,left_walk=[549,565],left_stop=[566,575],slow_right=[576,711],source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),sha256=hashlib.sha256(out.read_bytes()).hexdigest(),controller_only=True,unchanged_embedded_state=True,no_jump_after_branch=True),indent=2)+'\n')
