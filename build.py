#!/usr/bin/env python3
"""Build the current development version from approved art and registered sources."""
from pathlib import Path
import subprocess,sys,shutil,zipfile,re
r=Path(__file__).resolve().parent
version=(r/'VERSION').read_text().strip()
if not re.fullmatch(r'(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)',version):
 raise SystemExit('VERSION must contain a semantic version such as 0.0.1')
subprocess.run([sys.executable,str(r/'scripts/build_v15_polish.py')],cwd=r,check=True)
subprocess.run([sys.executable,str(r/'scripts/build_arm_repair.py')],cwd=r,check=True)
pack=r/'build/Holy_Diver_(Tr)';shutil.copy2(r/'INSTALL.txt',pack/'README.txt')
subprocess.run([sys.executable,str(r/'scripts/validate_pack.py'),str(pack)],check=True)
archive=r/f'build/Holy_Diver_HD_v{version}.zip'
with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED)as z:
 for p in sorted(pack.iterdir()):
  if p.is_file():z.write(p,p.name)
print('Rebuilt:',archive)
