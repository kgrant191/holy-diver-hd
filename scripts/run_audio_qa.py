"""Linux Mesen 2.1.1 / MesenCE 2.2.1: record native output during controller QA.

This recording helper is never installed in the HD pack. It does not replace
sound, change register values, or change the ROM.
"""
import argparse,os,subprocess
from pathlib import Path
p=argparse.ArgumentParser()
p.add_argument('--mesen',required=True);p.add_argument('--rom',required=True)
p.add_argument('--out',required=True);p.add_argument('--original',action='store_true')
p.add_argument('--legacy',action='store_true',help='Use the earlier 1,760-frame combat replay')
a=p.parse_args();out=Path(a.out).resolve();out.mkdir(parents=True,exist_ok=True)
for folder in ['frames','dumps']:(out/folder).mkdir(exist_ok=True)
scripts=Path(__file__).resolve().parent
subprocess.run(['c++','-shared','-fPIC','-O2',str(scripts/'record_audio.cpp'),'-o',str(out/'record_audio.so'),'-ldl'],check=True)
template='combat_qa_template.lua' if a.legacy else 'clean_audio_qa_template.lua'
script=(scripts/template).read_text().replace('__OUTPUT_DIR__',out.as_posix().replace("'","\\'"))
if a.legacy:
 script=script.replace('local oam={};local signatures={}',"local oam={};local signatures={};local apu={}\nemu.addMemoryCallback(function(addr,value) apu[#apu+1]=string.format('%d,%04X,%02X',frame,addr,value) end,emu.callbackType.write,0x4000,0x4017)")
 script=script.replace("if frame==1760 then save('oam.tsv'","if frame==1760 then save('apu.tsv',table.concat(apu,'\\n'));save('oam.tsv'")
(out/'replay.lua').write_text(script)
mesen=Path(a.mesen).resolve();env=os.environ.copy()
env.update(HOLY_DIVER_MESEN_CORE=str(mesen.parent/'MesenCore.so'),HOLY_DIVER_AUDIO_CAPTURE=str(out/'full.wav'),LD_PRELOAD=str(out/'record_audio.so')+':/usr/lib/x86_64-linux-gnu/libstdc++.so.6')
cmd=[str(mesen),'--testrunner','--timeout=180']
if a.original:cmd+=['--nes.enableHdPacks=false']
subprocess.run(cmd+[str(Path(a.rom).resolve()),str(out/'replay.lua')],env=env,check=True)
assert (out/'completed.txt').read_text().strip()==('1760' if a.legacy else '2400')
print('Completed Mesen gameplay and WAV capture:',out)
