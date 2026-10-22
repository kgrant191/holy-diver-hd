"""Reuse the approved bracelet atlas for its native owned-item pause icon."""
from pathlib import Path
import json
root=Path(__file__).resolve().parents[1];p=root/'build/Holy_Diver_(Tr)/hires.txt';s=p.read_text()
scope='pauseScreen&pauseMagicRow&pausedPalette'
# Native nametable layout after collection: 78 77 / 76 75, background palette3.
# These CHR tiles also occur in the old menu border with a different palette.
# Exact menu signature + palette preserves borders and unowned inventory slots.
layout=[(0x978,0,0),(0x977,16,0),(0x976,0,16),(0x975,16,16)]
rules=[f'[{scope}]<tile>26,{t:04X},0F172737,{x},{y},1,N'for t,x,y in layout]
assert all(r not in s for r in rules)
pos=s.index('#Chr_00_0.png');s=s[:pos]+'\n'.join(rules)+'\n'+s[pos:];p.write_text(s)
(root/'art/v14_menu_registration.json').write_text(json.dumps({'atlas':'Bracelet_2x.png','native_chr_tiles':['0978','0977','0976','0975'],'native_palette':'0F172737','scope':scope,'source':'same approved gameplay bracelet, no new image','position':'native item slot, only present after collection'},indent=2)+'\n')
print('Added four owned-bracelet pause-menu mappings')
