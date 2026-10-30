"""Controller-only right wall stop and slow left walk-off of the violet ledge."""
from pathlib import Path
import argparse,zipfile,json,hashlib
p=argparse.ArgumentParser();p.add_argument('--movie',required=True);p.add_argument('--out',required=True);a=p.parse_args();src=Path(a.movie);out=Path(a.out)
assert hashlib.sha256(src.read_bytes()).hexdigest()=='247df46f062af5a8d12e27aa0123e703aedf1e1e7bf7cd8e302bb410b8e877fa'
with zipfile.ZipFile(src)as z:entries={n:z.read(n)for n in z.namelist()}
neutral='|..|........|........';left='|..|..L.....|........';right='|..|...R....|........'
rows=entries['Input.txt'].decode().splitlines()[:1610]+[right]*80+[neutral]*30+([left]*3+[neutral])*40+[neutral]*50
with zipfile.ZipFile(out,'w',zipfile.ZIP_DEFLATED)as z:
    for n,value in entries.items():z.writestr(n,('\n'.join(rows)+'\n').encode()if n=='Input.txt'else value)
out.with_suffix('.json').write_text(json.dumps(dict(frames=len(rows),sha256=hashlib.sha256(out.read_bytes()).hexdigest(),original_prefix=1610,right_walk=[1611,1690],right_stop=[1691,1720],slow_left=[1721,1880],controller_only=True,unchanged_embedded_state=True,no_jump_after_branch=True),indent=2)+'\n')
