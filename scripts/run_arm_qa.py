"""Native-input arm coverage in both palettes, both directions, air and ground."""
from pathlib import Path
import argparse, subprocess, os
p=argparse.ArgumentParser();p.add_argument('--out',required=True);p.add_argument('--mesen',default='mesence/Mesen');p.add_argument('--rom',default='upload/Holy_Diver_(Tr).nes');a=p.parse_args()
r=Path(__file__).resolve().parents[1];out=Path(a.out).resolve();out.mkdir(parents=True,exist_ok=True)
subprocess.run(['c++','-shared','-fPIC','-O2',str(r/'scripts/record_audio.cpp'),'-o',str(out/'record_audio.so'),'-ldl'],check=True)
for mode in ['normal','twin']:
 d=out/mode;(d/'frames').mkdir(parents=True,exist_ok=True);(d/'dumps').mkdir(exist_ok=True)
 s=(r/'scripts/upward_qa_template.lua').read_text();s=s[:s.index('emu.addEventCallback(function()\n emu.setInput')]
 s=s.replace('__OUTPUT_DIR__',str(d)).replace('__STATE_FILE__',str(r/'test_states/Holy_Diver_HD_v10_Entrance.mss')).replace('960','480')
 select='frame>=5 and frame<8' if mode=='twin' else 'false'
 s+='''emu.addEventCallback(function()
 emu.setInput({start=false,down=false,select=SELECT,
 right=(frame>=10 and frame<12)or(frame>=300 and frame<320),
 left=(frame>=150 and frame<152)or(frame>=330 and frame<350),
 a=(frame>=85 and frame<100)or(frame>=225 and frame<240),
 b=(frame>=40 and frame<43)or(frame>=95 and frame<98)or(frame>=180 and frame<183)or(frame>=235 and frame<238)or(frame>=390 and frame<393),
 up=frame>=380 and frame<420},0)
end,emu.eventType.inputPolled)
'''.replace('SELECT',select)
 (d/'replay.lua').write_text(s);mesen=Path(a.mesen).resolve();env=os.environ.copy();env.update(LD_PRELOAD=str(out/'record_audio.so')+':/usr/lib/x86_64-linux-gnu/libstdc++.so.6',HOLY_DIVER_MESEN_CORE=str(mesen.parent/'MesenCore.so'),HOLY_DIVER_AUDIO_CAPTURE=str(d/'full.wav'))
 with(d/'run.log').open('w')as log:subprocess.run([str(mesen),'--testrunner','--timeout=120','--nes.enableHdPacks=true',str(Path(a.rom).resolve()),str(d/'replay.lua')],env=env,stdout=log,stderr=subprocess.STDOUT,check=True)
 assert(d/'completed.txt').read_text()=='480';print('Completed',mode,flush=True)
