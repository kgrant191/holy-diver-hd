"""Bound temple column lookups and reuse the finished small recovery pickups."""
from pathlib import Path
import hashlib, itertools, json, re

r=Path(__file__).resolve().parents[1]
p=r/'build/Holy_Diver_(Tr)'; a=r/'art/level4_repairs'; a.mkdir(exist_ok=True)
text=(p/'hires.txt').read_text()
previous=json.loads((r/'evidence/0.16.1-pack-sha256.json').read_text())
assert hashlib.sha256(text.encode()).hexdigest()==previous['hires.txt']

# Mesen 2.2.1's tileNearby bounds check accepts pixel index 61440, one past
# its 256x240 array. A +16 query at (0,224), or +8 at (0,232), can crash.
# Short-circuit position guards precede EVERY new neighbor evaluation.
# Explicit off-screen alternatives retain the intended "no neighbor" result,
# including inverted conditions, instead of changing the column silhouettes.
guards={-8:('templeSafeAbove8','>=',8),-16:('templeSafeAbove16','>=',16),
         8:('templeSafeBelow8','<',232),16:('templeSafeBelow16','<',224)}
conditions=[f'<condition>{name},positionCheckY,{op},{value}'for name,op,value in guards.values()]
near={}
for line in text.splitlines():
    m=re.fullmatch(r'<condition>(masonry[^,]+),tileNearby,0,(-?\d+),[^,]+,[^,]+',line)
    if m:near[m[1]]=int(m[2])
assert near
changes=[]
for line in text.splitlines():
    m=re.fullmatch(r'\[([^]]+)\]<tile>(.*)',line)
    if not m:continue
    terms=m[1].split('&')
    if not any(t.lstrip('!') in near for t in terms):continue
    alternatives=[]
    for t in terms:
        if t.lstrip('!') not in near:alternatives.append([[t]]);continue
        guard=guards[near[t.lstrip('!')]][0]
        alternatives.append([['!'+guard],[guard,t]] if t.startswith('!') else [[guard,t]])
    replacements=['['+'&'.join(itertools.chain.from_iterable(parts))+']<tile>'+m[2]
                  for parts in itertools.product(*alternatives)]
    assert text.count(line+'\n')==1
    text=text.replace(line+'\n','\n'.join(replacements)+'\n')
    changes.append(dict(original=line,replacements=replacements))
marker='# BEGIN TEMPLE_MASONRY CONDITIONS'
text=text.replace(marker,'# BEGIN TEMPLE_REPAIRS CONDITIONS\n'+'\n'.join(conditions)+
                  '\n# END TEMPLE_REPAIRS CONDITIONS\n'+marker)

# The two small pickup patterns are byte-identical in all sixteen CHR banks.
# Earlier gameplay/pause-specific rules retain priority. No palette guessing
# and no new art: exact Stage 2 heart/crystal atlas cells follow existing rules.
patterns={'heart':'0066ffffff7e3c180000667e7e3c1800',
          'magic':'3c4291818181423c003c6e7e7e7e3c00'}
records=[];rules=[]
for name,base in [('heart',0x47),('magic',0x48)]:
    source=next(l for l in text.splitlines() if l.startswith('<tile>25,') and
                l.split(',')[1]==f'{0x200+base:04X}' and l.split(',')[2]=='FF301116')
    fields=source[len('<tile>'):].split(',')
    for bank in range(0,0x2000,0x200):
        target=bank+base
        if any(re.fullmatch(r'<tile>\d+,0*'+f'{target:X}'+r',FF301116,.*',l)
               for l in text.splitlines()):continue
        f=fields.copy();f[1]=f'{target:04X}';rule='<tile>'+','.join(f)
        rules.append(rule)
        records.append(dict(name=name,tile=f[1],source_rule=source,rule=rule,
                            native_pattern=patterns[name]))
text+='# BEGIN TEMPLE_REPAIRS PICKUPS\n'+'\n'.join(rules)+'\n# END TEMPLE_REPAIRS PICKUPS\n'
(p/'hires.txt').write_text(text)
(a/'registration.json').write_text(json.dumps(dict(neighbor_rewrites=changes,
    position_conditions=conditions,nearby_conditions=near,pickups=records,
    extra_tile_rules=sum(len(c['replacements'])-1 for c in changes)+len(rules),
    extra_conditions=len(conditions),artwork_changed=False),indent=2)+'\n')
print('Temple repair:',len(changes),'bounded column rules;',len(rules),'shared pickup mappings; artwork unchanged')
