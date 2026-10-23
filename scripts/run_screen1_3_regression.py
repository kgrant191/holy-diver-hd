"""Run the existing title/reset and earlier crypt routes with a pinned pack."""
from pathlib import Path
import argparse
import hashlib
import json
import shutil
import subprocess
import sys

p=argparse.ArgumentParser()
for name in ['mesen','rom','pack','out']:
    p.add_argument('--'+name,required=True)
p.add_argument('--case',choices=['title','enemy'])
a=p.parse_args()
root=Path(__file__).resolve().parents[1]
mesen,rom,pack,out=[Path(v).resolve() for v in [a.mesen,a.rom,a.pack,a.out]]
assert not subprocess.run(['pgrep','-x','Mesen'],capture_output=True).stdout.strip()
installed=mesen.parent/'HdPacks'/rom.stem
hashes=lambda folder:{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in folder.iterdir() if p.is_file()}
expected=hashes(pack)
if a.case in [None,'title']:
    subprocess.run([sys.executable,str(root/'scripts/run_title_ledge_qa.py'),'--mesen',str(mesen),
                    '--rom',str(rom),'--pack',str(pack),'--out',str(out),'--case','title'],check=True)
if a.case in [None,'enemy']:
    if installed.exists():shutil.rmtree(installed)
    shutil.copytree(pack,installed,copy_function=shutil.copyfile)
    assert hashes(installed)==expected
    subprocess.run([sys.executable,str(root/'scripts/run_v15_qa.py'),'--mesen',str(mesen),
                    '--rom',str(rom),'--out',str(out),'--case','enemy'],check=True)
    assert hashes(installed)==expected
    (out/'enemy/installed_pack_sha256.json').write_text(json.dumps(expected,indent=2,sort_keys=True)+'\n')
