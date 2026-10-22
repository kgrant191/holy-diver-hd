local root='__OUTPUT_DIR__/'
local frame=0;local rows={};local commands={}
local function save(n,data) local h=assert(io.open(root..n,'wb'));h:write(data);h:close() end
emu.addMemoryCallback(function()
 local s=emu.getState();commands[#commands+1]=string.format('%d,%02X',frame,s['cpu.a'])
end,emu.callbackType.exec,0xc1b9)
emu.addEventCallback(function()
 if frame>=2500 then return end
 frame=frame+1
 local phase=emu.read(0x4af,emu.memType.nesInternalRam)
 local time=emu.read(0x9f,emu.memType.nesInternalRam)
 local sound=emu.read(0x1bc,emu.memType.nesInternalRam)
 local title=emu.read(0x2084,emu.memType.nesPpuMemory)==0x40 and emu.read(0x20a4,emu.memType.nesPpuMemory)==0x43
 rows[#rows+1]=table.concat({frame,phase,time,sound,title and 1 or 0},',')
 if frame%2==0 and (phase==8 or frame%24==0) then save(string.format('frames/%04d.png',frame),emu.takeScreenshot()) end
 if frame==2500 then save('events.tsv',table.concat(rows,'\n'));save('commands.tsv',table.concat(commands,'\n'));save('completed.txt','2500');emu.stop(0) end
end,emu.eventType.endFrame)
emu.addEventCallback(function() emu.setInput({start=false,select=false,a=false,b=false,left=false,right=false,up=false,down=false},0) end,emu.eventType.inputPolled)
