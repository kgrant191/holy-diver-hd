"""Exhaust screen coordinates for all copied dragon pickup-flash neighbor probes."""
from pathlib import Path
import json

def verify(root):
 lines=(root/'build/Holy_Diver_(Tr)/hires.txt').read_text().splitlines()
 defs={line[11:].split(',')[0]:line[11:].split(',')[1:]for line in lines if line.startswith('<condition>')}
 reg=json.loads((root/'art/level4_dragon/registration.json').read_text())
 chains=set()
 for m in reg['clones']:
  if not m['rule'].startswith('['):continue
  terms=m['rule'].split(']')[0][1:].split('&')
  selected=tuple(t for t in terms if defs[t.lstrip('!')][0]in ['positionCheckX','positionCheckY','tileNearby'])
  if any(defs[t.lstrip('!')][0]=='tileNearby'for t in selected):chains.add(selected)
 checks=reads=blocked=0
 for terms in sorted(chains):
  for y in range(240):
   for x in range(256):
    checks+=1
    for term in terms:
     neg=term.startswith('!');typ,*args=defs[term.lstrip('!')]
     if typ=='tileNearby':
      dx,dy=map(int,args[:2]);assert 0<=x+dx<256 and 0<=y+dy<240,(term,x,y)
      assert 0<=(y+dy)*256+x+dx<61440;reads+=1
      # Assume this native identity matches (or fails for an inverted probe),
      # so every subsequent read receives the strictest reachability check.
     else:
      op,value=args;value=int(value);actual=x if typ=='positionCheckX'else y
      ok={'>=':actual>=value,'<':actual<value,'==':actual==value}[op]
      if neg:ok=not ok
      if not ok:blocked+=1;break
 assert chains and reads
 return dict(unique_ordered_chains=len(chains),screen_coordinate_cases=checks,safe_reads=reads,blocked_branches=blocked,unsafe_reads=0)

if __name__=='__main__':
 root=Path(__file__).resolve().parents[1];report=verify(root)
 (root/'evidence/level4_dragon/neighbor_rules.json').write_text(json.dumps(report,indent=2)+'\n');print(report)
