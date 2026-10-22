import argparse,os,subprocess
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--out',required=True);p.add_argument('--original',action='store_true');p.add_argument('--state-index',type=int)
p.add_argument('--mesen',default='mesence/Mesen');p.add_argument('--rom',default='upload/Holy_Diver_(Tr).nes');p.add_argument('--state-dir',default=str(Path(__file__).resolve().parents[1]/'test_states/room2'));a=p.parse_args()
base=Path.cwd();scripts=Path(__file__).resolve().parent;out=Path(a.out).resolve();out.mkdir(parents=True,exist_ok=True)
subprocess.run(['c++','-shared','-fPIC','-O2',str(scripts/'record_audio.cpp'),'-o',str(out/'record_audio.so'),'-ldl'],check=True)
for i in ([a.state_index] if a.state_index else range(1,5)):
 state=Path(a.state_dir).resolve()/(['Holy_Diver_HD_1(1).mss','Holy_Diver_HD_2.mss','Holy_Diver_HD_3.mss','Holy_Diver_HD_4.mss'][i-1])
 dest=out/f'state{i}';(dest/'frames').mkdir(parents=True,exist_ok=True);(dest/'dumps').mkdir(exist_ok=True)
 s=(scripts/'room2_qa_template.lua').read_text().replace('__OUTPUT_DIR__',str(dest)).replace('__STATE_FILE__',str(state)).replace('__STATE_INDEX__',str(i));(dest/'replay.lua').write_text(s)
 mesen=Path(a.mesen).resolve()
 env=os.environ.copy();env.update(LD_PRELOAD=str(out/'record_audio.so')+':/usr/lib/x86_64-linux-gnu/libstdc++.so.6',HOLY_DIVER_MESEN_CORE=str(mesen.parent/'MesenCore.so'),HOLY_DIVER_AUDIO_CAPTURE=str(dest/'full.wav'))
 cmd=[str(mesen),'--testrunner','--timeout=180','--nes.enableHdPacks='+str(not a.original).lower(),str(Path(a.rom).resolve()),str(dest/'replay.lua')]
 with (dest/'run.log').open('w')as log:subprocess.run(cmd,env=env,stdout=log,stderr=subprocess.STDOUT,check=True)
 assert (dest/'completed.txt').read_text()=='360';print('Completed state',i,flush=True)
