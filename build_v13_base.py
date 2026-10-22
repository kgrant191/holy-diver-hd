#!/usr/bin/env python3
"""Rebuild the entrance and crypt pack from retained art and registration sources."""
from pathlib import Path
import subprocess,sys,zipfile,shutil
root=Path(__file__).resolve().parent
for script in ['register_art.py','build_environment.py','build_hero.py','build_equipped.py','build_weapons.py','build_screens.py','build_lightning.py','build_audio_priority.py','build_upward.py','build_title_prompt.py','build_global_player.py','build_room2_environment.py','build_room2_entities.py']:
 subprocess.run([sys.executable,str(root/'scripts'/script)],cwd=root,check=True)
pack=root/'build/Holy_Diver_(Tr)'
# Freeze the approved v12 rendered assets after rebuilding their mappings.
# New screen-2 work only adds images; historical art is byte-for-byte retained.
for approved in (root/'rollback/entrance_v12').glob('*.png'):
 shutil.copy2(approved,pack/approved.name)
# Exclude the retired fixed-width gameplay panel from every packaged rebuild.
(pack/'Gameplay_HUD.png').unlink(missing_ok=True)
shutil.copy2(root/'INSTALL.txt',pack/'README.txt')
subprocess.run([sys.executable,str(root/'scripts/validate_v13_pack.py'),str(pack)],check=True)
with zipfile.ZipFile(root/'build/Holy_Diver_HD_v13_Crypt.zip','w',zipfile.ZIP_DEFLATED) as z:
 for p in sorted(pack.iterdir()):
  if p.is_file():z.write(p,p.name)
print('Rebuilt:',root/'build/Holy_Diver_HD_v13_Crypt.zip')
