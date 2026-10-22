"""Remove the temporary entrance restriction from the approved player, weapons and HUD.
Native palette identities, CHR indices and measured neighboring-sprite signatures
remain. Native CHR/palette identities and earlier menu rules protect UI transitions.
"""
from pathlib import Path
import re,json
root=Path(__file__).resolve().parents[1];p=root/'build/Holy_Diver_(Tr)/hires.txt';s=p.read_text();lines=s.splitlines();count=0
for i,l in enumerate(lines):
 m=re.match(r'\[([^]]+)\]<tile>(18|19|20|21|22|23),',l)
 if m and 'entranceLowerA' in m[1]:
  terms=[t for t in m[1].split('&') if t not in ['gameplay','entranceLowerA','entranceLowerB','entrancePillar','litPalette']]
  # The fixed CHR addresses/palettes and pose signatures identify these sprites.
  # A single nametable menu probe can also occur in real stage geometry.
  lines[i]=('['+'&'.join(terms)+']' if terms else '')+l.split(']',1)[1];count+=1
p.write_text('\n'.join(lines)+'\n');(root/'art/global_player_scope.json').write_text(json.dumps({'broadened_rules':count,'preserved':'CHR indices, palettes, native pose signatures, animation frame ranges and all approved PNGs','ui_protection':'Native CHR bank/palette identities and existing earlier menu rules','later_gameplay_coverage':'Rules apply throughout gameplay for known normal/Twin Fire palettes; later forms and new palettes require coverage testing.'},indent=2)+'\n');print('Global player/HUD/weapon rules:',count)
