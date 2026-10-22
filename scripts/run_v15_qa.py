from pathlib import Path
import argparse,subprocess,os
p=argparse.ArgumentParser();p.add_argument('--out',required=True);p.add_argument('--capture-every-frame',action='store_true');p.add_argument('--case',choices=['title','normal','twin','enemy','menu']);p.add_argument('--mesen',default='mesence/Mesen');p.add_argument('--rom',default='upload/Holy_Diver_(Tr).nes');a=p.parse_args()
r=Path(__file__).resolve().parents[1];out=Path(a.out).resolve();out.mkdir(parents=True,exist_ok=True)
subprocess.run(['c++','-shared','-fPIC','-O2',str(r/'scripts/record_audio.cpp'),'-o',str(out/'record_audio.so'),'-ldl'],check=True)
for case in [a.case]if a.case else ['title','normal','twin','enemy','menu']:
 d=out/case;(d/'frames').mkdir(parents=True,exist_ok=True);(d/'dumps').mkdir(exist_ok=True)
 end={'title':1800,'normal':720,'twin':720,'enemy':360,'menu':180}[case]
 template=(r/'scripts/room2_qa_template.lua').read_text();template=template[:template.index('emu.addEventCallback(function()\n local state=')]
 state=(r/'test_states/Holy_Diver_Before_Death.mss')if case in ['normal','twin']else(r/'test_states/room2/Holy_Diver_HD_1(1).mss')if case=='enemy'else(r/'test_states/Holy_Diver_Bracelet_Owned_Before_Pause.mss')
 s=template.replace('__OUTPUT_DIR__',str(d)).replace('__STATE_FILE__',str(state)).replace('frame==360',f'frame=={end}').replace("'completed.txt','360'",f"'completed.txt','{end}'")
 if case=='title':
  s=s.replace("local f=assert(io.open('"+str(state)+"','rb'));local state=f:read('*a');f:close()",'').replace('local loaded=false','local loaded=true')
  s=s.replace('emu.addMemoryCallback(function()if not loaded then loaded=true;emu.loadSavestate(state)end end,emu.callbackType.exec,0x8000,0xffff)','')
  s=s.replace('if frame==1800 then','if frame==900 then emu.reset()end\n if frame==1800 then')
  controls='start=(frame>=300 and frame<303)or(frame>=480 and frame<483)or(frame>=1200 and frame<1203)or(frame>=1380 and frame<1383),left=false,right=false,a=false,b=false,select=false,up=false,down=false'
 elif case=='normal':controls='start=false,left=false,right=false,a=false,b=false,select=false,up=false,down=false'
 elif case=='twin':controls='start=false,left=frame>=10 and frame<150,right=false,a=false,b=false,select=frame>=5 and frame<8,up=false,down=false'
 elif case=='menu':controls='start=(frame>=5 and frame<8)or(frame>=125 and frame<128),left=false,right=false,a=false,b=false,select=false,up=false,down=false'
 else:
  source=(r/'scripts/room2_qa_template.lua').read_text();s+=source[source.index('emu.addEventCallback(function()\n local state='):].replace('__STATE_INDEX__','1');controls=None
 if a.capture_every_frame:s=s.replace('if frame%2==0 then', 'if frame>1 then')
 if controls:s+='emu.addEventCallback(function()emu.setInput({'+controls+'},0)end,emu.eventType.inputPolled)\n'
 (d/'replay.lua').write_text(s);mesen=Path(a.mesen).resolve();env=os.environ.copy();env.update(LD_PRELOAD=str(out/'record_audio.so')+':/usr/lib/x86_64-linux-gnu/libstdc++.so.6',HOLY_DIVER_MESEN_CORE=str(mesen.parent/'MesenCore.so'),HOLY_DIVER_AUDIO_CAPTURE=str(d/'full.wav'))
 with(d/'run.log').open('w')as log:subprocess.run([str(mesen),'--testrunner','--timeout=180','--nes.enableHdPacks=true',str(Path(a.rom).resolve()),str(d/'replay.lua')],env=env,stdout=log,stderr=subprocess.STDOUT,check=True)
 assert(d/'completed.txt').read_text()==str(end);print('Completed',case,flush=True)
