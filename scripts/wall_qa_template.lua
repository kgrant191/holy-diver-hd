local root='__OUTPUT_DIR__/'
local frame=0
local special={[720]='start_ledge',[900]='tree_upper_left',[1120]='left_wall_ledge'}
local function save(path,data) local h=assert(io.open(root..path,'wb'));h:write(data);h:close() end
local records={};local states={}
emu.addEventCallback(function()
 if frame>=1160 then return end
 frame=frame+1
 if special[frame] then
 save(special[frame]..'.png',emu.takeScreenshot())
 local ram={};for i=0,2047 do ram[#ram+1]=string.char(emu.read(i,emu.memType.nesInternalRam)) end;save(special[frame]..'.ram',table.concat(ram))
 end
 if frame>=720 and frame%4==0 then save(string.format('ram/%04d.bin',frame),(function() local t={} for i=0,2047 do t[#t+1]=string.char(emu.read(i,emu.memType.nesInternalRam)) end return table.concat(t) end)()) end
 if frame>=720 then
  local line={tostring(frame)}
  for i=0,252,4 do
   local y=emu.read(i,emu.memType.nesSpriteRam);local t=emu.read(i+1,emu.memType.nesSpriteRam);local a=emu.read(i+2,emu.memType.nesSpriteRam);local x=emu.read(i+3,emu.memType.nesSpriteRam)
   if y<240 then line[#line+1]=table.concat({y,t,a,x},',') end
  end
  records[#records+1]=table.concat(line,'\t')
 end
 if frame%30==0 then
  local line={frame};for _,addr in ipairs({0x2000,0x2800,0x2801,0x281c,0x3f01,0x3f11}) do line[#line+1]=emu.read(addr,emu.memType.nesPpuMemory) end
  states[#states+1]=table.concat(line,'\t')
 end
 
 if frame>=1160 then save('oam.tsv',table.concat(records,'\n')..'\n');save('state.tsv',table.concat(states,'\n')..'\n');save('completed.txt','1160\n');emu.stop(0) end
end,emu.eventType.endFrame)
emu.addEventCallback(function()
 local input={start=(frame>130 and frame<700 and frame%90<10),
 right=(frame>=730 and frame<820) or (frame>=1100 and frame<1102),left=(frame>=940 and frame<1004),
 a=(frame>=744 and frame<760) or (frame>=940 and frame<956)}
 emu.setInput(input,0)
end,emu.eventType.inputPolled)
