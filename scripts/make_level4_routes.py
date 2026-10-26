"""Controller-only Overdrive direction and slow platform routes."""
from pathlib import Path
import argparse,zipfile,json,hashlib
p=argparse.ArgumentParser();p.add_argument('movie');p.add_argument('out');a=p.parse_args();out=Path(a.out);out.mkdir(parents=True,exist_ok=True)
with zipfile.ZipFile(a.movie)as z:entries={n:z.read(n)for n in z.namelist()}
rows=entries['Input.txt'].decode().splitlines()
def hold(buttons,n):return ['|..|'+''.join(c if c in buttons else '.'for c in 'UDLRSsBA')+'|........']*n
# The original first menu selects Overdrive with one down press. Return from
# that menu, then enable the selected magic with Select for the cast route.
base=rows[:213]
cast=hold('B',2)+hold('',75)+hold('L',2)+hold('',8)+hold('B',2)+hold('',75)+hold('R',2)+hold('',8)+hold('UB',2)+hold('',75)
routes={'normal_fire':base+cast,'overdrive_cast':base+hold('s',2)+hold('',20)+cast,
'ledge':rows[:1048]+hold('L',8)+hold('',24)+(hold('R',2)+hold('',2))*90+hold('',45)}
result={}
for name,ls in routes.items():
 path=out/(name+'.mmo');raw=('\n'.join(ls)+'\n').encode()
 with zipfile.ZipFile(path,'w',zipfile.ZIP_DEFLATED)as z:
  for k,v in entries.items():z.writestr(k,raw if k=='Input.txt'else v)
 result[name]={'frames':len(ls),'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'input_sha256':hashlib.sha256(raw).hexdigest(),'controller_only':True,'source_movie_sha256':hashlib.sha256(Path(a.movie).read_bytes()).hexdigest(),'state_sha256':hashlib.sha256(entries['SaveState.mss']).hexdigest()}
(out/'routes.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
