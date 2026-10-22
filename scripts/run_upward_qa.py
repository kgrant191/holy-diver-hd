"""Capture the user's upward-fire route with native Mesen audio, without RAM edits."""
import argparse,os,subprocess
from pathlib import Path
p=argparse.ArgumentParser()
for name in ['mesen','rom','state','out']:p.add_argument('--'+name,required=True)
p.add_argument('--original',action='store_true');a=p.parse_args()
out=Path(a.out).resolve();out.mkdir(parents=True,exist_ok=True)
for folder in ['frames','dumps']:(out/folder).mkdir(exist_ok=True)
scripts=Path(__file__).resolve().parent
subprocess.run(['c++','-shared','-fPIC','-O2',str(scripts/'record_audio.cpp'),'-o',str(out/'record_audio.so'),'-ldl'],check=True)
def lua_path(p):return str(Path(p).resolve()).replace('\\','/').replace("'","\\'")
s=(scripts/'upward_qa_template.lua').read_text().replace('__OUTPUT_DIR__',lua_path(out)).replace('__STATE_FILE__',lua_path(a.state))
(out/'replay.lua').write_text(s)
mesen=Path(a.mesen).resolve();env=os.environ.copy()
env.update(HOLY_DIVER_MESEN_CORE=str(mesen.parent/'MesenCore.so'),HOLY_DIVER_AUDIO_CAPTURE=str(out/'full.wav'),LD_PRELOAD=str(out/'record_audio.so')+':/usr/lib/x86_64-linux-gnu/libstdc++.so.6')
cmd=[str(mesen),'--testrunner','--timeout=180']
if a.original:cmd+=['--nes.enableHdPacks=false']
subprocess.run(cmd+[str(Path(a.rom).resolve()),str(out/'replay.lua')],env=env,check=True)
assert (out/'completed.txt').read_text()=='960'
print('Completed upward-fire replay:',out)
