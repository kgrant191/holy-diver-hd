local root='__OUTPUT_DIR__/'
local h=assert(io.open('__STATE_FILE__','rb'));local state=h:read('*a');h:close()
local loaded=false;local frame=0;local apu={};local commands={}
local function save(n,data) local h=assert(io.open(root..n,'wb'));h:write(data);h:close() end
local function bytes(kind,start,count) local t={};for i=start,start+count-1 do t[#t+1]=string.char(emu.read(i,kind)) end;return table.concat(t) end
emu.addMemoryCallback(function() if not loaded then loaded=true;emu.loadSavestate(state) end end,emu.callbackType.exec,0x8000,0xffff)
emu.addMemoryCallback(function(addr,value)
 if loaded and addr~=0x4014 and addr~=0x4016 then local s=emu.getState();apu[#apu+1]=string.format('%d,%04X,%02X,%04X',frame,addr,value,s['cpu.pc']) end
end,emu.callbackType.write,0x4000,0x4017)
emu.addMemoryCallback(function() if loaded then local s=emu.getState();commands[#commands+1]=string.format('%d,%02X',frame,s['cpu.a']) end end,emu.callbackType.exec,0xc1b9)
emu.addEventCallback(function()
 if not loaded or frame>=300 then return end
 frame=frame+1
 if frame%2==0 then
  save(string.format('frames/%04d.png',frame),emu.takeScreenshot())
  save(string.format('dumps/%04d.ram',frame),bytes(emu.memType.nesInternalRam,0,2048))
  save(string.format('dumps/%04d.oam',frame),bytes(emu.memType.nesSpriteRam,0,256))
  save(string.format('dumps/%04d.ppu',frame),bytes(emu.memType.nesPpuMemory,0,16384))
 end
 if frame==300 then save('apu.tsv',table.concat(apu,'\n'));save('commands.tsv',table.concat(commands,'\n'));save('completed.txt','300');emu.stop(0) end
end,emu.eventType.endFrame)
emu.addEventCallback(function()
 emu.setInput({start=false,select=frame>=180 and frame<183,
 b=(frame>=30 and frame<33) or (frame>=110 and frame<113) or (frame>=210 and frame<213) or (frame>=250 and frame<253),
 up=(frame>=100 and frame<160) or (frame>=240 and frame<300),left=false,right=false,down=false,
 a=(frame>=100 and frame<115) or (frame>=240 and frame<255)},0)
end,emu.eventType.inputPolled)
