local root='__OUTPUT_DIR__/'
local frame=0
local special={[120]='publisher',[240]='title',[400]='stage_card',[600]='early_pause',[720]='first_screen',[748]='walk',[762]='jump_attack',[790]='airborne',[852]='cast',[1008]='pause',[1075]='resume',[1120]='left',[1230]='landing',[1400]='exit',[1600]='next_area',[1900]='reset_title'}
local function save(path,data) local h=assert(io.open(root..path,'wb'));h:write(data);h:close() end
local records=assert(io.open(root..'oam.tsv','w'));local states=assert(io.open(root..'state.tsv','w'))
emu.addEventCallback(function()
 frame=frame+1
 if special[frame] then
 save(special[frame]..'.png',emu.takeScreenshot())
 local ram={};for i=0,2047 do ram[#ram+1]=string.char(emu.read(i,emu.memType.nesInternalRam)) end;save(special[frame]..'.ram',table.concat(ram))
 end
 if frame>=720 and frame<=1680 and frame%3==0 then save(string.format('frames/%04d.png',frame),emu.takeScreenshot()) end
 if frame>=720 then
  local line={tostring(frame)}
  for i=0,252,4 do
   local y=emu.read(i,emu.memType.nesSpriteRam);local t=emu.read(i+1,emu.memType.nesSpriteRam);local a=emu.read(i+2,emu.memType.nesSpriteRam);local x=emu.read(i+3,emu.memType.nesSpriteRam)
   if y<240 then line[#line+1]=table.concat({y,t,a,x},',') end
  end
  records:write(table.concat(line,'\t'),'\n')
 end
 if frame%30==0 then
  local line={frame};for _,addr in ipairs({0x2000,0x2800,0x2801,0x281c,0x3f01,0x3f11}) do line[#line+1]=emu.read(addr,emu.memType.nesPpuMemory) end
  states:write(table.concat(line,'\t'),'\n')
 end
 if frame==1750 then emu.reset() end
 if frame>=1920 then records:close();states:close();emu.stop(0) end
end,emu.eventType.endFrame)
emu.addEventCallback(function()
 local input={start=(frame>130 and frame<700 and frame%90<10) or (frame>=1000 and frame<1003) or (frame>=1060 and frame<1063),right=(frame>=730 and frame<930) or (frame>=1200 and frame<1680),left=frame>=1080 and frame<1150,a=(frame>=744 and frame<760) or (frame>=1140 and frame<1155),b=(frame>=760 and frame<990 and frame%36<12) or(frame>=1200 and frame%48<12)}
 emu.setInput(input,0)
end,emu.eventType.inputPolled)
