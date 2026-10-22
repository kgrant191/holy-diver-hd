local root='__OUTPUT_DIR__/'
local frame=0
local specials={[120]='publisher',[160]='title_fade',[190]='title_ready',[240]='title',[400]='stage',[720]='normal_idle',[790]='primary_fire',[880]='equipped_idle',[950]='secondary_fire',[1100]='equipped_walk',[1190]='equipped_air',[1360]='pause_equipped',[1450]='resume_equipped',[1520]='normal_again',[1630]='pause_normal',[1720]='resume_normal'}
local oam={};local signatures={}
local function save(n,data) local h=assert(io.open(root..n,'wb'));h:write(data);h:close() end
local function bytes(kind,start,count) local t={};for i=start,start+count-1 do t[#t+1]=string.char(emu.read(i,kind)) end;return table.concat(t) end
emu.addEventCallback(function()
 if frame>=1760 then return end
 frame=frame+1
 local capture=(frame>=720 and frame<=1000 and frame%2==0) or (frame>=1040 and frame<=1260 and frame%2==0) or (frame>=1298 and frame<=1330 and frame%2==0)
 if capture or specials[frame] then
  local name=specials[frame] or string.format('frames/%04d',frame)
  save(name..'.png',emu.takeScreenshot())
  save(string.format('dumps/%04d.ram',frame),bytes(emu.memType.nesInternalRam,0,2048))
  save(string.format('dumps/%04d.ppu',frame),bytes(emu.memType.nesPpuMemory,0,16384))
  save(string.format('dumps/%04d.oam',frame),bytes(emu.memType.nesSpriteRam,0,256))
 end
 if frame>=720 then
  local line={frame}
  for i=0,252,4 do
   local y=emu.read(i,emu.memType.nesSpriteRam);local t=emu.read(i+1,emu.memType.nesSpriteRam);local a=emu.read(i+2,emu.memType.nesSpriteRam);local x=emu.read(i+3,emu.memType.nesSpriteRam)
   if y<240 then line[#line+1]=table.concat({y,t,a,x},',') end
  end
  oam[#oam+1]=table.concat(line,'\t')
 end
 if frame%10==0 then
  local line={frame};for _,addr in ipairs({0x2000,0x2800,0x2801,0x281c,0x3f01,0x3f11,0x3f1d,0x3f1e,0x3f1f}) do line[#line+1]=emu.read(addr,emu.memType.nesPpuMemory) end
  signatures[#signatures+1]=table.concat(line,'\t')
 end
 if frame==1760 then save('oam.tsv',table.concat(oam,'\n')..'\n');save('ppu_signatures.tsv',table.concat(signatures,'\n')..'\n');save('completed.txt','1760\n');emu.stop(0) end
end,emu.eventType.endFrame)
emu.addEventCallback(function()
 emu.setInput({start=(frame>130 and frame<700 and frame%90<10) or (frame>=1300 and frame<1303) or (frame>=1400 and frame<1403) or (frame>=1580 and frame<1583) or (frame>=1680 and frame<1683),
 select=(frame>=850 and frame<853) or (frame>=1480 and frame<1483),
 b=(frame>=730 and frame<815) or (frame>=900 and frame<1000) or (frame>=1200 and frame<1240),
 right=(frame>=1040 and frame<1080),left=(frame>=1100 and frame<1140),a=frame>=1160 and frame<1176},0)
end,emu.eventType.inputPolled)
