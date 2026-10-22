"""Replay actual Select, B, movement and Start inputs in Mesen 2.1.1."""
from pathlib import Path
import argparse, subprocess, os
p=argparse.ArgumentParser();p.add_argument('--mesen',required=True);p.add_argument('--rom',required=True);p.add_argument('--out',required=True)
p.add_argument('--original',action='store_true');p.add_argument('--branch-attacks',action='store_true');p.add_argument('--linux-cxx-preload',action='store_true');a=p.parse_args()
out=Path(a.out).resolve();(out/'frames').mkdir(parents=True,exist_ok=True);(out/'dumps').mkdir(exist_ok=True)
template=Path(__file__).with_name('branch_attacks_qa_template.lua' if a.branch_attacks else 'combat_qa_template.lua').read_text()
script=out/'replay.lua';script.write_text(template.replace('__OUTPUT_DIR__',out.as_posix().replace("'","\\'")))
env=os.environ.copy()
if a.linux_cxx_preload:env['LD_PRELOAD']='/usr/lib/x86_64-linux-gnu/libstdc++.so.6'
cmd=[str(Path(a.mesen).resolve()),'--testrunner','--timeout=180']
if a.original:cmd.append('--nes.enableHdPacks=false')
subprocess.run(cmd+[str(Path(a.rom).resolve()),str(script)],env=env,check=True)
assert (out/'completed.txt').read_text().strip()=='1760'
print('Mesen replay completed:',out)
