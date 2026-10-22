from pathlib import Path
from PIL import Image
import shutil
root=Path(__file__).resolve().parents[1]
base=root/'rollback/stable_v2';out=root/'build/Holy_Diver_(Tr)'
shutil.copytree(base,out,dirs_exist_ok=True)
im=Image.open(root/'art/EntranceScene_registered.png').convert('RGBA');im.save(out/'EntranceScene.png')
s=(base/'hires.txt').read_text()
s+='''
# First entrance chamber, observed live in Mesen 2.1.1.
<condition>gameplay,ppuMemoryCheckConstant,3F11,==,16
<condition>entranceLowerA,ppuMemoryCheckConstant,2800,==,01
<condition>entranceLowerB,ppuMemoryCheckConstant,2801,==,02
<condition>entrancePillar,ppuMemoryCheckConstant,281C,==,24
<condition>litPalette,ppuMemoryCheckConstant,3F01,==,07
[gameplay&entranceLowerA&entranceLowerB&entrancePillar&litPalette]<background>EntranceScene.png,1,1,1,20,0,0
'''
lines=s.splitlines();conds=[l for l in lines if l.startswith('<condition>')];s='\n'.join(l for l in lines if not l.startswith('<condition>'))+'\n';pos=s.index('#Chr_00_0.png');s=s[:pos]+'\n'.join(conds)+'\n'+s[pos:]
(out/'hires.txt').write_text(s)

