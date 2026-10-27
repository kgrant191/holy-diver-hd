"""Exhaustive short-circuit bounds and truth-table check for column rules."""
from pathlib import Path
import itertools,json,re

def verify(root):
 reg=json.loads((root/'art/level4_repairs/registration.json').read_text())
 guards={}
 for l in reg['position_conditions']:
  name,typ,op,value=l[len('<condition>'):].split(',');assert typ=='positionCheckY'
  guards[name]=(op,int(value))
 cases=0;safe_reads=0;blocked_branches=0
 for change in reg['neighbor_rewrites']:
  original=change['original'].split(']')[0][1:].split('&')
  replacements=[l.split(']')[0][1:].split('&')for l in change['replacements']]
  names=sorted({t.lstrip('!')for t in original if t.lstrip('!')in reg['nearby_conditions']})
  for y in range(240):
   for values in itertools.product([False,True],repeat=len(names)):
    neighbors=dict(zip(names,values))
    def evaluate(terms,require_bounds):
     nonlocal safe_reads,blocked_branches
     for term in terms:
      neg=term.startswith('!');name=term.lstrip('!')
      if name in guards:
       op,v=guards[name];value=y>=v if op=='>='else y<v
      elif name in neighbors:
       target_y=y+reg['nearby_conditions'][name]
       if require_bounds:
        assert 0<=target_y<240,(name,y,terms)
        safe_reads+=1
       value=neighbors[name] if 0<=target_y<240 else False
      else:value=True # Room identity is held true to exercise all probes.
      if neg:value=not value
      if not value:
       if name in guards:blocked_branches+=1
       return False
     return True
    expected=evaluate(original,False)
    actual=any(evaluate(terms,True)for terms in replacements)
    assert expected==actual,(change,y,values)
    cases+=1
 return dict(rules=len(reg['neighbor_rewrites']),truth_table_cases=cases,safe_neighbor_evaluations=safe_reads,
             blocked_out_of_range_branches=blocked_branches,all_screen_x_values_covered='dx=0; bounds depend only on y',
             native_no_neighbor_semantics_preserved=True,unsafe_evaluations=0)

if __name__=='__main__':
 root=Path(__file__).resolve().parents[1];report=verify(root)
 (root/'evidence/level4_repairs/neighbor_rules.json').write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps(report,indent=2))
