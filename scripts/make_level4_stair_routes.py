"""Wrap the unchanged user stair state in controller-only Mesen movies."""
from pathlib import Path
import argparse,zipfile,json,hashlib
p=argparse.ArgumentParser()
for k in ['state','template','out']:p.add_argument('--'+k,required=True)
a=p.parse_args();out=Path(a.out);out.mkdir(exist_ok=True,parents=True)
state=Path(a.state).read_bytes()
with zipfile.ZipFile(a.template)as z:entries={n:z.read(n)for n in z.namelist()}
def hold(keys,n):return ['|..|'+''.join(k if k in keys else '.'for k in 'UDLRSsBA')+'|........']*n
routes={'inspect':hold('',120),
 'walk':hold('',30)+hold('L',100)+hold('',30)+hold('R',100)+hold('',30),
 'jump':hold('',30)+(hold('LA',25)+hold('L',12))*4+hold('',30)+hold('R',120)+hold('',30)}
routes['edge']=routes['jump'][:120]+hold('L',12)+hold('',16)+(hold('R',2)+hold('',2))*30+hold('',30)
report={}
for name,rows in routes.items():
 path=out/(name+'.mmo');inputs=('\n'.join(rows)+'\n').encode()
 with zipfile.ZipFile(path,'w',zipfile.ZIP_DEFLATED)as z:
  for n,v in entries.items():z.writestr(n,state if n=='SaveState.mss'else inputs if n=='Input.txt'else v)
 report[name]=dict(frames=len(rows),sha256=hashlib.sha256(path.read_bytes()).hexdigest(),
  input_sha256=hashlib.sha256(inputs).hexdigest(),state_sha256=hashlib.sha256(state).hexdigest(),controller_only=True)
(out/'routes.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
