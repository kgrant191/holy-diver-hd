local root='__OUTPUT_DIR__/'
local frame=0
local specials={[900]='branch_idle',[980]='primary_right',[1040]='equipped',[1080]='secondary_right',[1200]='secondary_left',[1280]='normal_restored',[1310]='primary_left',[1410]='pause',[1510]='resumed',[1710]='reset_title'}
local oam={};local signatures={}
local function save(n,data) local h=assert(io.open(root..n,'wb'));h:write(data);h:close() end
local function bytes(kind,start,count) local t={};for i=start,start+count-1 do t[#t+1]=string.char(emu.read(i,kind)) end;return table.concat(t) end
emu.addEventCallback(function()
 if frame>=1760 then return end
 frame=frame+1
 local capture=(frame>=958 and frame<=1004 and frame%2==0) or (frame>=1058 and frame<=1104 and frame%2==0) or (frame>=1178 and frame<=1224 and frame%2==0) or (frame>=1288 and frame<=1334 and frame%2==0)
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
 if frame==1560 then emu.reset() end
 if frame==1760 then save('oam.tsv',table.concat(oam,'\n')..'\n');save('ppu_signatures.tsv',table.concat(signatures,'\n')..'\n');save('completed.txt','1760\n');emu.stop(0) end
end,emu.eventType.endFrame)
emu.addEventCallback(function()
 emu.setInput({start=(frame>130 and frame<700 and frame%90<10) or (frame>=1360 and frame<1363) or (frame>=1460 and frame<1463),
 select=(frame>=1020 and frame<1023) or (frame>=1260 and frame<1263),
 b=(frame>=960 and frame<963) or (frame>=1060 and frame<1063) or (frame>=1180 and frame<1183) or (frame>=1290 and frame<1293),
 right=frame>=730 and frame<820,left=frame>=1140 and frame<1142,a=frame>=744 and frame<760},0)
end,emu.eventType.inputPolled)
