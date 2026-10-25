import faulthandler
faulthandler.enable()
import argparse
import os
import ctypes as C
import hashlib
import json
import shutil
import time
import zipfile
from pathlib import Path

p=argparse.ArgumentParser()
for n in ['core','config','database','rom','movie','pack','out']:p.add_argument('--'+n,required=True)
p.add_argument('--stride',type=int,default=4)
p.add_argument('--capture-start',type=int,default=1)
p.add_argument('--capture-end',type=int,default=1000000)
a=p.parse_args()
args=a
OUT=Path(a.out).resolve()
OUT.mkdir(parents=True,exist_ok=True)
for name in ('frames','ram','ppu','oam','view'):(OUT/name).mkdir(exist_ok=True)
ROM=Path(a.rom).resolve()
MOVIE=Path(a.movie).resolve()
with zipfile.ZipFile(MOVIE)as movie_zip:movie_frames=len(movie_zip.read('Input.txt').splitlines())
replay_home=OUT/'mesen_home';replay_home.mkdir(exist_ok=True)
shutil.copyfile(a.database,replay_home/'MesenNesDB.txt')
pack=replay_home/'HdPacks'/ROM.stem
assert not pack.exists(), 'Use a fresh output directory'
shutil.copytree(a.pack,pack)
hashes=lambda folder:{p.name:hashlib.sha256(p.read_bytes()).hexdigest()for p in folder.iterdir()if p.is_file()}
expected=hashes(pack)
(OUT/'installed_pack.json').write_text(json.dumps(expected,indent=2))
C.CDLL('/usr/lib/x86_64-linux-gnu/libstdc++.so.6',mode=C.RTLD_GLOBAL)
cfg_path=a.config
a=C.CDLL(a.core,mode=C.RTLD_GLOBAL)
cfg=C.CDLL(cfg_path)
def declare(name,args=[],restype=None):
 f=getattr(a,name);f.argtypes=args;f.restype=restype;return f
declare('InitDll');declare('InitializeEmu',[C.c_char_p,C.c_void_p,C.c_void_p,C.c_bool,C.c_bool,C.c_bool,C.c_bool])
declare('LoadRom',[C.c_char_p,C.c_char_p],C.c_bool)
declare('MoviePlay',[C.c_char_p]);declare('MoviePlaying',restype=C.c_bool)
declare('LoadScript',[C.c_char_p,C.c_char_p,C.c_char_p,C.c_int],C.c_int)
declare('GetScriptLog',[C.c_int,C.c_void_p,C.c_uint32]);declare('GetLog',[C.c_void_p,C.c_uint32])
declare('SetEmulationFlag',[C.c_int,C.c_bool]);declare('IsRunning',restype=C.c_bool)
for name in ('Pause','Resume','Stop','Release','InitializeDebugger','TakeScreenshot'):declare(name)
script=r'''
local root='__OUT__/'
local frame=0
local apu={}
emu.addMemoryCallback(function(addr,value)
 if addr~=0x4014 and addr~=0x4016 then apu[#apu+1]=string.format('%d,%04X,%02X',frame,addr,value)end
end,emu.callbackType.write,0x4000,0x4017)
local function save(name,data)local f=assert(io.open(root..name,'wb'));f:write(data);f:close()end
local function bytes(kind,count)local t={};for i=0,count-1 do t[#t+1]=string.char(emu.read(i,kind))end;return table.concat(t)end
emu.addEventCallback(function()
 if frame>=__END__ then return end
 frame=frame+1
 if frame>=__START__ and frame<=__CAPTURE_END__ and (frame==2 or frame%__STRIDE__==0) then
  save(string.format('frames/%06d.png',frame),emu.takeScreenshot())
  save(string.format('ram/%06d.bin',frame),bytes(emu.memType.nesInternalRam,2048))
  save(string.format('ppu/%06d.bin',frame),bytes(emu.memType.nesPpuMemory,16384))
  save(string.format('oam/%06d.bin',frame),bytes(emu.memType.nesSpriteRam,256))
  local v=emu.getState()
  save(string.format('view/%06d.json',frame),string.format('{"vram":%d,"xscroll":%d,"frame":%d,"grayscale":%s}',v['ppu.tmpVideoRamAddr'],v['ppu.xScroll'],v['ppu.frameCount'],tostring(v['ppu.mask.grayscale'])))
 end
 if frame%60==0 or frame==__END__ then save('progress.txt',tostring(frame));save('apu.tsv',table.concat(apu,'\n'))end
end,emu.eventType.endFrame)
'''.replace('__OUT__',str(OUT)).replace('__STRIDE__',str(args.stride)).replace('__END__',str(movie_frames)).replace('__START__',str(args.capture_start)).replace('__CAPTURE_END__',str(args.capture_end))
(OUT/'capture.lua').write_text(script)
print('Initialize core',flush=True)
a.InitDll();a.InitializeEmu(str(replay_home).encode(),None,None,True,True,True,True)
cfg.ConfigureReplay();a.SetEmulationFlag(0x10,True);a.Pause()
print('Load ROM',flush=True)
assert a.LoadRom(str(ROM).encode(),b''),'ROM load failed'
print('Load movie',flush=True)
a.MoviePlay(str(MOVIE).encode());assert a.MoviePlaying(),'Movie failed to start'
print('Initialize observer',flush=True)
# ConsoleMode creates the debugger during LoadRom; reinitializing it while
# the restored movie is paused can deadlock the stock 2.2.1 native core.
a.Pause()
sid=a.LoadScript(b'movie_capture',str(OUT).encode(),script.encode(),-1)
print('script',sid,flush=True)
a.SetEmulationFlag(4,True);a.Resume()
started=time.monotonic()
try:
 while a.MoviePlaying() and time.monotonic()-started<240:time.sleep(.1)
 ended=not a.MoviePlaying();a.Pause();a.TakeScreenshot()
 b=C.create_string_buffer(50000);a.GetScriptLog(sid,b,len(b));(OUT/'script.log').write_bytes(b.value)
 a.GetLog(b,len(b));(OUT/'emulator.log').write_bytes(b.value)
 info={'movie_sha256':hashlib.sha256(MOVIE.read_bytes()).hexdigest(),'rom_sha1':hashlib.sha1(ROM.read_bytes()).hexdigest(),'emulator_version':'2.2.1','movie_completed':ended,'captured_frames':len(list((OUT/'frames').glob('*.png'))),'seconds_wall':time.monotonic()-started,'stride':args.stride,'core_sha256':hashlib.sha256(Path(args.core).read_bytes()).hexdigest()}
 (OUT/'result.json').write_text(json.dumps(info,indent=2)+'\n');print(json.dumps(info),flush=True);print((OUT/'script.log').read_text(),flush=True)
finally:a.Stop();a.Release()
info['movie_frames']=movie_frames
info['captured_frames']=len(list((OUT/'frames').glob('*.png')))
(OUT/'result.json').write_text(json.dumps(info,indent=2)+'\n')
assert ended, 'Movie did not finish'
assert hashes(pack)==expected, 'Installed pack changed during replay'
