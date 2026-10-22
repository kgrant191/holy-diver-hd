local root='__OUTPUT_DIR__/'
local f=assert(io.open('__STATE_FILE__','rb'));local state=f:read('*a');f:close()
local loaded=false;local frame=0;local apu={};local commands={};local poses={};local samples={}
local function save(n,data)local h=assert(io.open(root..n,'wb'));h:write(data);h:close()end
local function bytes(kind,start,count)local t={};for i=start,start+count-1 do t[#t+1]=string.char(emu.read(i,kind))end;return table.concat(t)end
emu.addMemoryCallback(function()if not loaded then loaded=true;emu.loadSavestate(state)end end,emu.callbackType.exec,0x8000,0xffff)
emu.addMemoryCallback(function(addr,value)if loaded and addr~=0x4014 and addr~=0x4016 then apu[#apu+1]=string.format('%d,%04X,%02X',frame,addr,value)end end,emu.callbackType.write,0x4000,0x4017)
emu.addMemoryCallback(function()if loaded then local s=emu.getState();commands[#commands+1]=string.format('%d,%02X',frame,s['cpu.a'])end end,emu.callbackType.exec,0xc1b9)
emu.addEventCallback(function()
 if not loaded then return end;frame=frame+1
 if frame%2==0 then
  save(string.format('frames/%04d.png',frame),emu.takeScreenshot())
  save(string.format('dumps/%04d.ram',frame),bytes(emu.memType.nesInternalRam,0,2048))
  save(string.format('dumps/%04d.ppu',frame),bytes(emu.memType.nesPpuMemory,0,16384))
  save(string.format('dumps/%04d.oam',frame),bytes(emu.memType.nesSpriteRam,0,256))
 end
 if frame==360 then save('apu.tsv',table.concat(apu,'\n'));save('commands.tsv',table.concat(commands,'\n'));save('completed.txt','360');emu.stop(0)end
end,emu.eventType.endFrame)
emu.addEventCallback(function()
 local state=__STATE_INDEX__
 local right=(state==1 and frame>=4 and frame<220)or(state==2 and frame>=4 and frame<32)or(state==2 and frame>=170 and frame<250)or(state==4 and frame>=120 and frame<230)
 local left=(state==3 and frame>=12 and frame<180)or(state==4 and frame>=4 and frame<40)
 local up=(frame>=65 and frame<95)or(frame>=130 and frame<160)
 local b=(frame>=40 and frame<43)or(frame>=75 and frame<78)or(frame>=115 and frame<118)or(frame>=145 and frame<148)or(frame>=205 and frame<208)
 local select=(frame>=100 and frame<103)or(frame>=245 and frame<248)
 local a=(state==1 and frame>=82 and frame<103)or(frame>=180 and frame<200)
 local start=(frame>=275 and frame<278)or(frame>=305 and frame<308)
 emu.setInput({right=right,left=left,up=up,b=b,a=a,select=select,start=start,down=false},0)
end,emu.eventType.inputPolled)
