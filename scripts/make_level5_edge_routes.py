"""Controller-only platform checks from the exact supplied movie state."""
from pathlib import Path
import argparse,zipfile,json,hashlib
p=argparse.ArgumentParser();p.add_argument('--movie',required=True);p.add_argument('--out',required=True);a=p.parse_args();out=Path(a.out);out.mkdir(parents=True,exist_ok=True)
with zipfile.ZipFile(a.movie)as z:entries={n:z.read(n)for n in z.namelist()}
original=entries['Input.txt'].decode().splitlines()
def hold(keys,n):return ['|..|'+''.join(k if k in keys else '.'for k in 'UDLRSsBA')+'|........']*n
routes={'left_stop_span':hold('L',80)+hold('',20)+(hold('R',2)+hold('',2))*140,
        'right_walkoff':original[:650]+hold('',20)+(hold('R',2)+hold('',2))*70}
report={}
for name,rows in routes.items():
 path=out/(name+'.mmo');inputs=('\n'.join(rows)+'\n').encode()
 with zipfile.ZipFile(path,'w',zipfile.ZIP_DEFLATED)as z:
  for n,v in entries.items():z.writestr(n,inputs if n=='Input.txt'else v)
 report[name]=dict(frames=len(rows),sha256=hashlib.sha256(path.read_bytes()).hexdigest(),input_sha256=hashlib.sha256(inputs).hexdigest(),state_sha256=hashlib.sha256(entries['SaveState.mss']).hexdigest(),controller_only=True)
(out/'routes.json').write_text(json.dumps(report,indent=2)+'\n')
