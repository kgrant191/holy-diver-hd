local root='__OUTPUT_DIR__/'
local frame=0;local apu={};local hud={};local commands={}
local function save(n,data) local h=assert(io.open(root..n,'wb'));h:write(data);h:close() end
local function bytes(kind,start,count) local t={};for i=start,start+count-1 do t[#t+1]=string.char(emu.read(i,kind)) end;return table.concat(t) end
emu.addMemoryCallback(function(addr,value)
 if addr==0x4014 or addr==0x4016 then return end
 local s=emu.getState();apu[#apu+1]=string.format('%d,%04X,%02X,%04X',frame,addr,value,s['cpu.pc'])
end,emu.callbackType.write,0x4000,0x4017)
emu.addMemoryCallback(function(addr,value)
 if frame==1580 and value==0x51 then local s=emu.getState();hud[#hud+1]=string.format('%d,%04X,%02X,%04X',frame,addr,value,s['cpu.pc']) end
end,emu.callbackType.write,0x200,0x2ff)
emu.addMemoryCallback(function(addr,value)
 local s=emu.getState();commands[#commands+1]=string.format('%d,%02X',frame,s['cpu.a'])
end,emu.callbackType.exec,0xc1b9)
emu.addEventCallback(function()
 if frame>=2400 then return end
 frame=frame+1
 if frame%2==0 and ((frame>=480 and frame<=660) or frame>=1540) then
  save(string.format('frames/%04d.png',frame),emu.takeScreenshot())
  save(string.format('dumps/%04d.ram',frame),bytes(emu.memType.nesInternalRam,0,2048))
  save(string.format('dumps/%04d.oam',frame),bytes(emu.memType.nesSpriteRam,0,256))
 end
 if frame==2400 then save('apu.tsv',table.concat(apu,'\n'));save('hud.tsv',table.concat(hud,'\n'));save('commands.tsv',table.concat(commands,'\n'));save('completed.txt','2400');emu.stop(0) end
end,emu.eventType.endFrame)
emu.addEventCallback(function()
 emu.setInput({start=frame>=1100 and frame<1103,
 select=(frame>=1900 and frame<1903) or (frame>=2150 and frame<2153),
 b=(frame>=1600 and frame<1603) or (frame>=1800 and frame<1803) or (frame>=1950 and frame<1953) or (frame>=2050 and frame<2053) or (frame>=2200 and frame<2203),
 a=false,left=false,right=false,up=false,down=false},0)
end,emu.eventType.inputPolled)
