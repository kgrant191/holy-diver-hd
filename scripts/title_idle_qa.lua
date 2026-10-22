local root='__OUTPUT_DIR__/'
local frame=0
local rows={}
local function save(n,data) local h=assert(io.open(root..n,'wb'));h:write(data);h:close() end
emu.addEventCallback(function()
 if frame>=2400 then return end
 frame=frame+1
 if frame%12==0 then
  save(string.format('frames/%04d.png',frame),emu.takeScreenshot())
  local row={frame}
  for _,a in ipairs({0x2084,0x20a4,0x3f01,0x3f11}) do row[#row+1]=emu.read(a,emu.memType.nesPpuMemory) end
  local count=0;for i=0,252,4 do if emu.read(i,emu.memType.nesSpriteRam)<240 then count=count+1 end end
  row[#row+1]=count;rows[#rows+1]=table.concat(row,',')
 end
 if frame==2400 then save('title.tsv',table.concat(rows,'\n'));save('completed.txt','2400');emu.stop(0) end
end,emu.eventType.endFrame)
emu.addEventCallback(function() emu.setInput({start=false,select=false,a=false,b=false,left=false,right=false,up=false,down=false},0) end,emu.eventType.inputPolled)
