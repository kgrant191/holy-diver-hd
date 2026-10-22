"""Repeatable native input/audio capture for title prompt and idle entrance thunder."""
import argparse,os,subprocess
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--mode',choices=['title','idle'],required=True)
p.add_argument('--out',required=True);p.add_argument('--state');p.add_argument('--original',action='store_true')
p.add_argument('--mesen',default='mesence/Mesen');p.add_argument('--rom',default='upload/Holy_Diver_(Tr).nes')
a=p.parse_args();out=Path(a.out).resolve();(out/'frames').mkdir(parents=True,exist_ok=True);(out/'dumps').mkdir(exist_ok=True)
base=Path(__file__).resolve().parent
s="""local root='__ROOT__/'
local frame=0;local rows={};local commands={};local apu={}
local function save(n,data) local f=assert(io.open(root..n,'wb'));f:write(data);f:close() end
local function bytes(kind,start,count) local t={};for i=start,start+count-1 do t[#t+1]=string.char(emu.read(i,kind)) end;return table.concat(t) end
__LOAD__
emu.addMemoryCallback(function()
 local s=emu.getState();commands[#commands+1]=string.format('%d,%02X',frame,s['cpu.a'])
end,emu.callbackType.exec,0xc1b9)
emu.addMemoryCallback(function(addr,value)
 if addr~=0x4014 and addr~=0x4016 then
  local s=emu.getState();local x=s['cpu.x'];local id=emu.read(0x1b8+x,emu.memType.nesInternalRam)
  apu[#apu+1]=string.format('%d,%04X,%02X,%04X,%02X,%02X',frame,addr,value,s['cpu.pc'],x,id)
 end
end,emu.callbackType.write,0x4000,0x4017)
emu.addEventCallback(function()
 frame=frame+1
 local row={frame}
 for _,addr in ipairs({0x4af,0x9f,0x1bc,0x30f,0x63}) do row[#row+1]=emu.read(addr,emu.memType.nesInternalRam) end
 for _,addr in ipairs({0x2084,0x20a4,0x3f11}) do row[#row+1]=emu.read(addr,emu.memType.nesPpuMemory) end
 rows[#rows+1]=table.concat(row,',')
 if frame%4==0 then
  save(string.format('frames/%04d.png',frame),emu.takeScreenshot())
  save(string.format('dumps/%04d.ram',frame),bytes(emu.memType.nesInternalRam,0,2048))
  save(string.format('dumps/%04d.oam',frame),bytes(emu.memType.nesSpriteRam,0,256))
 end
 if frame==__END__ then save('events.tsv',table.concat(rows,'\\n'));save('commands.tsv',table.concat(commands,'\\n'));save('apu.tsv',table.concat(apu,'\\n'));save('completed.txt',tostring(frame));emu.stop(0) end
end,emu.eventType.endFrame)
emu.addEventCallback(function()
 emu.setInput({start=__START__,select=false,a=false,b=false,left=false,right=false,up=false,down=false},0)
end,emu.eventType.inputPolled)
"""
load=''
if a.state:
 load="local h=assert(io.open('"+str(Path(a.state).resolve())+"','rb'));local state=h:read('*a');h:close();local loaded=false\nemu.addMemoryCallback(function() if not loaded then loaded=true;emu.loadSavestate(state) end end,emu.callbackType.exec,0x8000,0xffff)"
s=s.replace('__ROOT__',str(out)).replace('__LOAD__',load).replace('__END__','3000' if a.mode=='title' else '1200').replace('__START__','(frame>=2100 and frame<2103) or (frame>=2400 and frame<2403)' if a.mode=='title' else 'false')
(out/'replay.lua').write_text(s)
subprocess.run(['c++','-shared','-fPIC','-O2',str(base/'record_audio.cpp'),'-o',str(out/'record_audio.so'),'-ldl'],check=True)
mesen=Path(a.mesen).resolve();env=os.environ.copy();env.update(LD_PRELOAD=str(out/'record_audio.so')+':/usr/lib/x86_64-linux-gnu/libstdc++.so.6',HOLY_DIVER_MESEN_CORE=str(mesen.parent/'MesenCore.so'),HOLY_DIVER_AUDIO_CAPTURE=str(out/'full.wav'))
cmd=[str(mesen),'--testrunner','--timeout=180']
if a.original:cmd+=['--nes.enableHdPacks=false']
with (out/'run.log').open('w') as log:subprocess.run(cmd+[str(Path(a.rom).resolve()),str(out/'replay.lua')],env=env,stdout=log,stderr=subprocess.STDOUT,check=True)
assert (out/'completed.txt').is_file();print('Completed',a.mode,str(out))
