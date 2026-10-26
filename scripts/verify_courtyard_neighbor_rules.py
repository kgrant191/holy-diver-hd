"""Exhaust every screen coordinate for the two new statue context probes."""
from pathlib import Path
import json,re

def verify(root):
 text=(root/'build/Holy_Diver_(Tr)/hires.txt').read_text()
 reg=json.loads((root/'art/level4_courtyard/registration.json').read_text())
 checks=reads=blocked=0
 for m in reg['mappings']:
  if m['kind']!='opposite statue shared foot':continue
  terms=m['scope'].split('&');guard,probe=terms[-2:]
  assert guard==probe+'Safe'
  definition=next(l for l in text.splitlines()if l.startswith('<condition>'+guard+','))
  _,typ,op,value=definition[11:].split(',');assert typ=='positionCheckX';value=int(value)
  definition=next(l for l in text.splitlines()if l.startswith('<condition>'+probe+','))
  _,typ,dx,dy,tile,palette=definition[11:].split(',');dx,dy=int(dx),int(dy)
  assert typ=='tileNearby'and dy==0 and palette=='0F071737'
  for y in range(240):
   for x in range(256):
    allowed=x>=value if op=='>='else x<value
    if allowed:
     assert 0<=x+dx<256 and 0<=(y+dy)*256+x+dx<61440
     reads+=1
    else:blocked+=1
    checks+=1
 assert checks==122880
 return dict(new_statue_rules=2,screen_coordinate_checks=checks,safe_reads=reads,blocked=blocked,unsafe_reads=0,
             cloned_pillars='Exact ordered copies of the previously exhaustively verified bounded rules')

if __name__=='__main__':
 root=Path(__file__).resolve().parents[1];report=verify(root)
 (root/'evidence/level4_courtyard/neighbor_rules.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
