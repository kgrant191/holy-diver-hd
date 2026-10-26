"""Derive controller-only edge routes; retain the supplied starting state/settings."""
import argparse,hashlib,json,zipfile
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('movie');p.add_argument('out');a=p.parse_args()
src=Path(a.movie);out=Path(a.out);out.mkdir(parents=True,exist_ok=True)
with zipfile.ZipFile(src)as z:entries={n:z.read(n)for n in z.namelist()}
rows=entries['Input.txt'].decode().splitlines()
def line(buttons):return '|..|'+''.join(c if c in buttons else '.'for c in 'UDLRSsBA')+'|........'
routes={
 'entrance_left_stop':[line('L')]*90+[line('R')if n%4==0 else line('')for n in range(480)],
 'raised_ledge_slow_walkoff':rows[:640]+[line(('R'if n%16<12 else '')+('B'if n%12<6 else ''))for n in range(160)],
}
report={}
for name,inputs in routes.items():
 path=out/(name+'.mmo')
 with zipfile.ZipFile(path,'w',zipfile.ZIP_DEFLATED)as z:
  for key,value in entries.items():z.writestr(key,('\n'.join(inputs)+'\n').encode()if key=='Input.txt'else value)
 report[name]=dict(frames=len(inputs),sha256=hashlib.sha256(path.read_bytes()).hexdigest(),source_movie_sha256=hashlib.sha256(src.read_bytes()).hexdigest(),starting_state_sha256=hashlib.sha256(entries['SaveState.mss']).hexdigest(),input_only=True)
(out/'routes.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
