"""Controller-only dragon checks; embeds the supplied state byte for byte."""
from pathlib import Path
import argparse,zipfile,json,hashlib
p=argparse.ArgumentParser()
for k in ['state','template','out']:p.add_argument('--'+k,required=True)
a=p.parse_args();out=Path(a.out);out.mkdir(parents=True,exist_ok=True);state=Path(a.state).read_bytes()
with zipfile.ZipFile(a.template)as z:entries={n:z.read(n)for n in z.namelist()}
def hold(keys,n):return ['|..|'+''.join(k if k in keys else '.'for k in 'UDLRSsBA')+'|........']*n
def seq(parts):return sum((hold(k,n)for k,n in parts),[])
flight=seq([('',30),('R',40),('',160),('U',35)])
for keys,n in [('R',120),('L',100),('U',40),('D',70),('R',100),('L',100),('',100)]:
 for i in range(n):flight+=hold(keys+('B'if i%24<6 else''),1)
flight+=seq([('S',1),('',45),('S',1),('',45)])
routes={'flight':flight,'a_controls':seq([('',30),('R',40),('',160),('UA',40),('RA',80),('LA',80),('AB',80),('DA',40),('',60)])};report={}
for name,rows in routes.items():
 path=out/(name+'.mmo');inputs=('\n'.join(rows)+'\n').encode()
 with zipfile.ZipFile(path,'w',zipfile.ZIP_DEFLATED)as z:
  for n,v in entries.items():z.writestr(n,state if n=='SaveState.mss'else inputs if n=='Input.txt'else v)
 report[name]=dict(frames=len(rows),sha256=hashlib.sha256(path.read_bytes()).hexdigest(),input_sha256=hashlib.sha256(inputs).hexdigest(),state_sha256=hashlib.sha256(state).hexdigest(),controller_only=True)
(out/'routes.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
