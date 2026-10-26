"""Input-only Breaker direction/palette and Blizzard pool checks."""
from pathlib import Path
import argparse,zipfile,json,hashlib
p=argparse.ArgumentParser();p.add_argument('movie');p.add_argument('out');a=p.parse_args()
src=Path(a.movie);out=Path(a.out);out.mkdir(exist_ok=True,parents=True)
with zipfile.ZipFile(src)as z:entries={n:z.read(n)for n in z.namelist()}
rows=entries['Input.txt'].decode().splitlines()
def line(buttons):return '|..|'+''.join(c if c in buttons else '.'for c in 'UDLRSsBA')+'|........'
def hold(buttons,n):return [line(buttons)]*n
routes={
 'breaker':rows+hold('s',2)+hold('',10)+hold('B',1)+hold('',90)+hold('L',2)+hold('',10)+hold('B',1)+hold('',90)+hold('UB',1)+hold('',90)+hold('R',2)+hold('',10)+hold('B',1)+hold('',5)+hold('s',1)+hold('',90),
 'blizzard':rows[:200]+hold('B',1)+hold('',620),
 'edge':rows[:200]+hold('L',12)+hold('',20)+(hold('R',3)+hold('',1))*45+hold('',60),
}
report={}
for name,inputs in routes.items():
 raw=('\n'.join(inputs)+'\n').encode();path=out/(name+'.mmo')
 with zipfile.ZipFile(path,'w',zipfile.ZIP_DEFLATED)as z:
  for key,value in entries.items():z.writestr(key,raw if key=='Input.txt'else value)
 report[name]=dict(frames=len(inputs),movie_sha256=hashlib.sha256(path.read_bytes()).hexdigest(),input_sha256=hashlib.sha256(raw).hexdigest(),source_movie_sha256=hashlib.sha256(src.read_bytes()).hexdigest(),starting_state_sha256=hashlib.sha256(entries['SaveState.mss']).hexdigest(),controller_only=True)
(out/'routes.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
