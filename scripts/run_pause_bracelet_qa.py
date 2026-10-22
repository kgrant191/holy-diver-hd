from pathlib import Path
import argparse,subprocess,os
p=argparse.ArgumentParser();p.add_argument('--out',required=True);p.add_argument('--original',action='store_true');p.add_argument('--mesen',default='mesence/Mesen');p.add_argument('--rom',default='upload/Holy_Diver_(Tr).nes');a=p.parse_args()
root=Path(__file__).resolve().parents[1];out=Path(a.out).resolve();out.mkdir(parents=True,exist_ok=True)
for d in ['frames','dumps']:(out/d).mkdir(exist_ok=True)
s=(root/'scripts/room2_qa_template.lua').read_text();s=s[:s.index('emu.addEventCallback(function()\n local state=')]
s=s.replace('__OUTPUT_DIR__',str(out)).replace('__STATE_FILE__',str(root/'test_states/room2/Holy_Diver_HD_3.mss')).replace("frame==360","frame==900").replace("'completed.txt','360'","'completed.txt','900'")
s=s.replace('local loaded=false;', 'local saved=false;local loaded=false;').replace('if not loaded then loaded=true;emu.loadSavestate(state)end end', "if not loaded then loaded=true;emu.loadSavestate(state)end;if loaded and frame==720 and not saved then saved=true;local h=assert(io.open(root..'owned_before_pause.mss','wb'));h:write(emu.createSavestate());h:close()end end")
s+='''emu.addEventCallback(function()
 emu.setInput({left=frame>=10 and frame<300,right=frame>=300 and frame<725,b=false,a=(frame>=340 and frame<365)or(frame>=440 and frame<465)or(frame>=540 and frame<565),up=false,down=false,select=false,start=(frame>=725 and frame<728)or(frame>=845 and frame<848)},0)
end,emu.eventType.inputPolled)
'''
(out/'replay.lua').write_text(s);mesen=Path(a.mesen).resolve();env=os.environ.copy();subprocess.run(['c++','-shared','-fPIC','-O2',str(root/'scripts/record_audio.cpp'),'-o',str(out/'record_audio.so'),'-ldl'],check=True);env.update(LD_PRELOAD=str(out/'record_audio.so')+':/usr/lib/x86_64-linux-gnu/libstdc++.so.6',HOLY_DIVER_MESEN_CORE=str(mesen.parent/'MesenCore.so'),HOLY_DIVER_AUDIO_CAPTURE=str(out/'full.wav'))
with(out/'run.log').open('w')as log:subprocess.run([str(mesen),'--testrunner','--timeout=180','--nes.enableHdPacks='+str(not a.original).lower(),str(Path(a.rom).resolve()),str(out/'replay.lua')],env=env,stdout=log,stderr=subprocess.STDOUT,check=True)
assert(out/'completed.txt').read_text()=='900';print('Done',out)
