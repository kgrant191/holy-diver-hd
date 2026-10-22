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
 if not loaded or frame>=960 then return end
 frame=frame+1
 if frame%2==0 then
  save(string.format('frames/%04d.png',frame),emu.takeScreenshot())
  save(string.format('dumps/%04d.ram',frame),bytes(emu.memType.nesInternalRam,0,2048))
  save(string.format('dumps/%04d.oam',frame),bytes(emu.memType.nesSpriteRam,0,256))
  save(string.format('dumps/%04d.ppu',frame),bytes(emu.memType.nesPpuMemory,0,16384))
 end
 if frame==960 then save('apu.tsv',table.concat(apu,'\n'));save('commands.tsv',table.concat(commands,'\n'));save('completed.txt','960');emu.stop(0) end
end,emu.eventType.endFrame)
emu.addEventCallback(function()
 emu.setInput({start=false,select=(frame>=160 and frame<163) or (frame>=500 and frame<503) or (frame>=800 and frame<803),
 b=(frame>=30 and frame<33) or (frame>=60 and frame<63) or (frame>=90 and frame<93) or (frame>=120 and frame<123) or (frame>=190 and frame<193) or (frame>=220 and frame<223) or (frame>=250 and frame<253) or (frame>=280 and frame<283) or (frame>=370 and frame<373) or (frame>=400 and frame<403) or (frame>=430 and frame<433) or (frame>=460 and frame<463) or (frame>=530 and frame<533) or (frame>=560 and frame<563) or (frame>=590 and frame<593) or (frame>=620 and frame<623) or (frame>=720 and frame<723) or (frame>=740 and frame<743) or (frame>=860 and frame<863) or (frame>=880 and frame<883),
 up=(frame>=20 and frame<145) or (frame>=180 and frame<305) or (frame>=360 and frame<485) or (frame>=520 and frame<645) or (frame>=700 and frame<780) or (frame>=840 and frame<920),
 left=frame>=340 and frame<343,right=false,down=false,a=(frame>=710 and frame<725) or (frame>=850 and frame<865)},0)
end,emu.eventType.inputPolled)
