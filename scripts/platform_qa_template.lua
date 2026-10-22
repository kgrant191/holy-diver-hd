local root='__OUTPUT_DIR__/'
local frame=0
local special={[900]='upper_left',[1090]='upper_right',[1280]='middle_left',[1470]='lower_right',[1660]='lower_left'}
local function save(path,data) local h=assert(io.open(root..path,'wb'));h:write(data);h:close() end
local records=assert(io.open(root..'oam.tsv','w'));local states=assert(io.open(root..'state.tsv','w'))
emu.addEventCallback(function()
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
  records:write(table.concat(line,'\t'),'\n');records:flush()
 end
 if frame%30==0 then
  local line={frame};for _,addr in ipairs({0x2000,0x2800,0x2801,0x281c,0x3f01,0x3f11}) do line[#line+1]=emu.read(addr,emu.memType.nesPpuMemory) end
  states:write(table.concat(line,'\t'),'\n')
 end
 
 if frame>=1700 then records:close();states:close();save('completed.txt','1700\n');emu.stop(0) end
end,emu.eventType.endFrame)
emu.addEventCallback(function()
 local input={start=(frame>130 and frame<700 and frame%90<10),
 right=(frame>=730 and frame<820) or (frame>=940 and frame<1004) or (frame>=1320 and frame<1384),
 left=(frame>=1130 and frame<1194) or (frame>=1510 and frame<1574),
 a=(frame>=744 and frame<760) or (frame>=940 and frame<956) or (frame>=1130 and frame<1146) or (frame>=1320 and frame<1336) or (frame>=1510 and frame<1526)}
 emu.setInput(input,0)
end,emu.eventType.inputPolled)
