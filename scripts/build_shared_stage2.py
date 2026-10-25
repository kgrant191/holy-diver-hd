"""Make finished Stage 2 assets available as last-match room-independent fallbacks."""
from pathlib import Path
import json,re

root=Path(__file__).resolve().parents[1];pack=root/'build/Holy_Diver_(Tr)'
text=(pack/'hires.txt').read_text();rules=[];records=[];seen=set()
sources=[
 ('screen2_5_brown_roof','s25Room&s25DataLo&s25DataHi',lambda t: t in brown),
 ('screen2_4','s24Room&s24DataLo&s24DataHi',lambda t: 0x32e<=t<=0x35e or 0x369<=t<=0x36c or 0x375<=t<=0x39a or t in [0x3a1,0x3a2]),
 ('screen2_2','s22Room&s22DataLo&s22DataHi',lambda t: 0x28e<=t<=0x2b6),
 ('screen2_1','s21Room&s21DataLo&s21DataHi',lambda t: 0x200<=t<0x300),
 ('screen2_3','s23Room&s23DataLo&s23DataHi',lambda t: 0x2d8<=t<=0x2dd),
]
brown={int(t,16) for t in json.loads((root/'art/screen2_5_roof/previous_geometry.json').read_text())}
for source,scope,include in sources:
 for line in text.splitlines():
  m=re.fullmatch(r'\[([^]]+)\]<tile>(.*)',line)
  if not m or not (m[1]==scope or m[1].startswith(scope+'&')):continue
  fields=m[2].split(',');tile=int(fields[1],16)
  if not include(tile):continue
  # Original brown rules are first. Do not import the rejected 0.8.1
  # ceiling-removal/floor-probe rules that share the old room scope.
  remainder=m[1][len(scope):].lstrip('&')
  if source=='screen2_5_brown_roof' and remainder:continue
  if source=='screen2_4' and fields[2] not in {'0F071737','0F161606','0F060616','0F122131'}:continue
  palettes=[fields[2]]
  if fields[2]=='0F071737':palettes.append('0F081737')
  for palette in palettes:
   f=fields.copy();f[2]=palette
   key=(remainder,f[1],palette)
   if key in seen:continue
   seen.add(key)
   prefix='['+remainder+']' if remainder else ''
   rule=prefix+'<tile>'+','.join(f)
   rules.append(rule)
   records.append(dict(source=source,source_rule=line,rule=rule,palette_alias=palette!=fields[2]))
# Append after every room-specific rule. Native tile ID and palette still
# have to match exactly; this does not guess a replacement by appearance.
block='# BEGIN SCREEN2_SHARED\n'+'\n'.join(rules)+'\n# END SCREEN2_SHARED\n'
(pack/'hires.txt').write_text(text+block)
out=root/'art/shared_stage2';out.mkdir(exist_ok=True)
(out/'registration.json').write_text(json.dumps(dict(tile_rules=len(rules),room_overrides_first=True,new_artwork=False,records=records),indent=2)+'\n')
print('Shared Stage 2 fallbacks:',len(rules),'rules using existing artwork; room overrides stay first.')
