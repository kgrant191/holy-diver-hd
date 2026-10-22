#!/usr/bin/env python3
"""Replay actual controller inputs and capture Mesen's own HD framebuffer.
Requires a configured Mesen 2.1.1 installation with this pack installed, with
Debug > ScriptWindow > AllowIoOsAccess enabled to write evidence files.
"""
import argparse,os,subprocess
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--mesen',required=True);p.add_argument('--rom',required=True);p.add_argument('--out',default='qa-output');p.add_argument('--linux-cxx-preload',action='store_true');a=p.parse_args()
out=Path(a.out).resolve();(out/'frames').mkdir(parents=True,exist_ok=True)
template=Path(__file__).with_name('qa_template.lua').read_text();path=out/'replay.lua';path.write_text(template.replace('__OUTPUT_DIR__',out.as_posix().replace("'","\\'")))
env=os.environ.copy()
if a.linux_cxx_preload:env['LD_PRELOAD']='/usr/lib/x86_64-linux-gnu/libstdc++.so.6'
subprocess.run([str(Path(a.mesen).resolve()),'--testrunner','--timeout=45',str(Path(a.rom).resolve()),str(path)],env=env,check=True)
print('Mesen captures:',out)
