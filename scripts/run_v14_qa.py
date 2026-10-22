from pathlib import Path
import argparse,subprocess,os
p=argparse.ArgumentParser();p.add_argument('--out',required=True);p.add_argument('--mesen',default='mesence/Mesen');p.add_argument('--rom',default='upload/Holy_Diver_(Tr).nes');p.add_argument('--case',choices=['bracelet','normal','twin']);a=p.parse_args()
root=Path(__file__).resolve().parents[1];out=Path(a.out).resolve();out.mkdir(parents=True,exist_ok=True)
subprocess.run(['c++','-shared','-fPIC','-O2',str(root/'scripts/record_audio.cpp'),'-o',str(out/'record_audio.so'),'-ldl'],check=True)
template=(root/'scripts/room2_qa_template.lua').read_text();template=template[:template.index('emu.addEventCallback(function()\n local state=')]
for case in ([a.case]if a.case else ['bracelet','normal','twin']):
 dest=out/case;(dest/'frames').mkdir(parents=True,exist_ok=True);(dest/'dumps').mkdir(exist_ok=True)
 state=root/'test_states/room2/Holy_Diver_HD_3.mss'if case=='bracelet'else root/'test_states/Holy_Diver_Before_Death.mss'
 controls="left=frame>=10 and frame<120,right=frame>=120 and frame<350,b=frame%16<3,select=false"if case=='bracelet'else('left=false,right=false,b=false,select=false'if case=='normal'else'left=frame>=10 and frame<150,right=false,b=false,select=frame>=5 and frame<8')
 s=template.replace('frame%2==0','true').replace('__OUTPUT_DIR__',str(dest)).replace('__STATE_FILE__',str(state))
 s+='emu.addEventCallback(function()\n emu.setInput({'+controls+',start=false,up=false,down=false,a=false},0)\nend,emu.eventType.inputPolled)\n';(dest/'replay.lua').write_text(s)
 mesen=Path(a.mesen).resolve();env=os.environ.copy();env.update(LD_PRELOAD=str(out/'record_audio.so')+':/usr/lib/x86_64-linux-gnu/libstdc++.so.6',HOLY_DIVER_MESEN_CORE=str(mesen.parent/'MesenCore.so'),HOLY_DIVER_AUDIO_CAPTURE=str(dest/'full.wav'))
 with(dest/'run.log').open('w')as log:subprocess.run([str(mesen),'--testrunner','--timeout=180','--nes.enableHdPacks=true',str(Path(a.rom).resolve()),str(dest/'replay.lua')],env=env,stdout=log,stderr=subprocess.STDOUT,check=True)
 assert(dest/'completed.txt').read_text()=='360';print('Completed',case,flush=True)
