"""Reach the green 1-up with controller input; preserve the original movie state."""
from pathlib import Path
import argparse,zipfile,json,hashlib
p=argparse.ArgumentParser();p.add_argument('--movie',required=True);p.add_argument('--out',required=True);a=p.parse_args()
source=Path(a.movie);out=Path(a.out)
assert hashlib.sha256(source.read_bytes()).hexdigest()=='197f7725772cb6a5540519616036fca047d3ac5b47a3b244cc0b3ea714347f49'
with zipfile.ZipFile(source)as z:data={n:z.read(n)for n in z.namelist()}
rows=data['Input.txt'].decode().splitlines()[:744]
rows+=['|..|U.......|........']*140+['|..|...R....|........']*480+['|..|........|........']*100
data['Input.txt']=('\n'.join(rows)+'\n').encode();out.parent.mkdir(parents=True,exist_ok=True)
with zipfile.ZipFile(out,'w',zipfile.ZIP_DEFLATED)as z:
 for n,b in data.items():z.writestr(n,b)
print(json.dumps(dict(movie=str(out),frames=len(rows),unchanged_embedded_state=True,ram_edits=False,segments=[dict(first=1,last=744,input='original'),dict(first=745,last=884,input='Up'),dict(first=885,last=1364,input='Right'),dict(first=1365,last=1464,input='neutral')]),indent=2))
