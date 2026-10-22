"""Land on every entrance branch using only ordinary controller input."""
import argparse, os, subprocess
from pathlib import Path
p=argparse.ArgumentParser()
p.add_argument('--mesen',required=True)
p.add_argument('--rom',required=True)
p.add_argument('--out',required=True)
p.add_argument('--original',action='store_true')
p.add_argument('--linux-cxx-preload',action='store_true')
a=p.parse_args()
out=Path(a.out).resolve();(out/'ram').mkdir(parents=True,exist_ok=True)
template=Path(__file__).with_name('platform_qa_template.lua').read_text()
script=out/'replay.lua'
script.write_text(template.replace('__OUTPUT_DIR__',out.as_posix().replace("'","\\'")))
env=os.environ.copy()
if a.linux_cxx_preload:
    env['LD_PRELOAD']='/usr/lib/x86_64-linux-gnu/libstdc++.so.6'
args=[str(Path(a.mesen).resolve()),'--testrunner','--timeout=90']
if a.original:args.append('--nes.enableHdPacks=false')
args += [str(Path(a.rom).resolve()),str(script)]
subprocess.run(args,env=env,check=True)
print('Five stationary branch captures saved:',out)
