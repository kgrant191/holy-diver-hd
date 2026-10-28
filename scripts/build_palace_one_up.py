"""Reuse the approved complete 1-up figurines in both Palace sprite banks."""
from pathlib import Path
import hashlib,json

R=Path(__file__).resolve().parents[1];P=R/'build/Holy_Diver_(Tr)';A=R/'art/level5_one_up'
text=(P/'hires.txt').read_text();previous=json.loads((R/'evidence/0.22.1-pack-sha256.json').read_text())
assert hashlib.sha256(text.encode()).hexdigest()==previous['hires.txt']
patterns=json.loads((A/'native_patterns.json').read_text());lines=text.splitlines();rules=[];records=[]
for bank in [0x1000,0x1200]:
 for palette,source_palette in [('FF300036','FF300036'),('FF221136','FF221136'),('FF190927','FF300036')]:
  for offset in [0x4e,0x4f]:
   target=bank+offset;source=0x200+offset
   assert patterns[f'{target:04X}']==patterns[f'{source:04X}']
   candidates=[l for l in lines if l.startswith(f'<tile>29,{source:04X},{source_palette},')]
   assert len(candidates)==1
   source_rule=candidates[0];f=source_rule[6:].split(',');f[1]=f'{target:04X}';f[2]=palette
   rule='<tile>'+','.join(f);assert not any(f',{target:04X},{palette},'in l and '<tile>'in l for l in lines)
   rules.append(rule);records.append(dict(source_rule=source_rule,rule=rule,native_source=f'{source:04X}',native_target=f'{target:04X}',palette=palette,source_palette=source_palette))
# Exact tile/palette fallbacks follow existing specific rules. No new image,
# neighbor lookup, palette mutation or change to the native pickup is needed.
text+='# BEGIN PALACE_ONE_UP MAPPINGS\n'+'\n'.join(rules)+'\n# END PALACE_ONE_UP MAPPINGS\n'
(P/'hires.txt').write_text(text)
(A/'registration.json').write_text(json.dumps(dict(mappings=records,new_artwork=False,dragon_form_uses='approved ivory figurine'),indent=2)+'\n')
print('Palace 1-up:',len(rules),'aliases; exact approved figurines and native 8x16 footprint')
