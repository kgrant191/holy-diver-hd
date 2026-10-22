local root='__OUTPUT_DIR__/'
local h=assert(io.open('__STATE_FILE__','rb'));local state=h:read('*a');h:close()
local loaded=false;local frame=0;local saved=false
local function save(n,data) local h=assert(io.open(root..n,'wb'));h:write(data);h:close() end
emu.addMemoryCallback(function()
 if not loaded then
  loaded=true;emu.loadSavestate(state)
  for voice=0,9 do
   if emu.read(0x1b8+voice,emu.memType.nesInternalRam)==0x1e then
    local ch=emu.read(0x17c+voice,emu.memType.nesInternalRam)
    if ch==0 or ch==4 then
     assert(emu.read(0x130+ch,emu.memType.nesInternalRam)==voice)
     emu.write(0x130+ch,0xff,emu.memType.nesInternalRam)
     emu.write(0x17c+voice,ch+3,emu.memType.nesInternalRam)
     emu.write(0x130+ch+3,voice,emu.memType.nesInternalRam)
    end
   end
  end
 elseif frame==1 and not saved then
  saved=true;save('Holy_Diver_HD_v10_Entrance.mss',emu.createSavestate())
 end
end,emu.callbackType.exec,0x8000,0xffff)
emu.addEventCallback(function()
 frame=frame+1
 if frame==2 then save('preview.png',emu.takeScreenshot());save('completed.txt','2');emu.stop(0) end
end,emu.eventType.endFrame)
emu.addEventCallback(function() emu.setInput({start=false,select=false,b=false,a=false,left=false,right=false,up=false,down=false},0) end,emu.eventType.inputPolled)
