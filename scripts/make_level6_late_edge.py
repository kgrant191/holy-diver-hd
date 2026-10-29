"""Controller-only left-stop and slow right walk-off of the green entry floor."""
from pathlib import Path
import argparse,zipfile,json,hashlib
p=argparse.ArgumentParser();p.add_argument('--movie',required=True);p.add_argument('--out',required=True);a=p.parse_args();source=Path(a.movie);out=Path(a.out)
assert hashlib.sha256(source.read_bytes()).hexdigest()=='c5451de99dfbadd8002cb88ca0b10ea6ec105870df7cf827d385c4fb7dc7ba05'
with zipfile.ZipFile(source)as z:entries={n:z.read(n)for n in z.namelist()}
neutral='|..|........|........';left='|..|..L.....|........';right='|..|...R....|........'
rows=entries['Input.txt'].decode().splitlines()[:280]+[left]*60+[neutral]*40+([right]*3+[neutral])*65+[neutral]*60
with zipfile.ZipFile(out,'w',zipfile.ZIP_DEFLATED)as z:
 for name,value in entries.items():z.writestr(name,('\n'.join(rows)+'\n').encode()if name=='Input.txt'else value)
out.with_suffix('.json').write_text(json.dumps(dict(frames=len(rows),sha256=hashlib.sha256(out.read_bytes()).hexdigest(),source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),original_prefix=280,left_walk=[281,340],left_stop=[341,380],slow_right=[381,640],controller_only=True,unchanged_embedded_state=True,no_jump_after_branch=True),indent=2)+'\n')
