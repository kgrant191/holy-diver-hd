local root='__OUTPUT_DIR__/'
local h=assert(io.open('__STATE_FILE__','rb'));local state=h:read('*a');h:close()
local loaded=false;local frame=0;local apu={};local commands={}
local function save(n,data) local h=assert(io.open(root..n,'wb'));h:write(data);h:close() end
local function bytes(kind,start,count) local t={};for i=start,start+count-1 do t[#t+1]=string.char(emu.read(i,kind)) end;return table.concat(t) end
emu.addMemoryCallback(function() if not loaded then loaded=true;emu.loadSavestate(state) end end,emu.callbackType.exec,0x8000,0xffff)
emu.addMemoryCallback(function(addr,value)
 if loaded and addr~=0x4014 and addr~=0x4016 then
  local s=emu.getState();local x=s['cpu.x'];local id=emu.read(0x1b8+x,emu.memType.nesInternalRam)
  apu[#apu+1]=string.format('%d,%04X,%02X,%04X,%02X,%02X',frame,addr,value,s['cpu.pc'],x,id)
 end
end,emu.callbackType.write,0x4000,0x4017)
emu.addMemoryCallback(function() if loaded then local s=emu.getState();commands[#commands+1]=string.format('%d,%02X',frame,s['cpu.a']) end end,emu.callbackType.exec,0xc1b9)
emu.addEventCallback(function()
 if not loaded or frame>=900 then return end
 frame=frame+1
 if frame%2==0 then
  save(string.format('frames/%04d.png',frame),emu.takeScreenshot())
  save(string.format('dumps/%04d.ram',frame),bytes(emu.memType.nesInternalRam,0,2048))
  save(string.format('dumps/%04d.oam',frame),bytes(emu.memType.nesSpriteRam,0,256))
 end
 if frame==900 then save('apu.tsv',table.concat(apu,'\n'));save('commands.tsv',table.concat(commands,'\n'));save('completed.txt','900');emu.stop(0) end
end,emu.eventType.endFrame)
emu.addEventCallback(function()
 emu.setInput({start=false,
 select=(frame>=300 and frame<303) or (frame>=560 and frame<563) or (frame>=710 and frame<713),
 b=(frame>=100 and frame<103) or (frame>=380 and frame<383) or (frame>=630 and frame<633) or (frame>=790 and frame<793),
 right=frame>=460 and frame<525,left=false,up=false,down=false,a=false},0)
end,emu.eventType.inputPolled)
