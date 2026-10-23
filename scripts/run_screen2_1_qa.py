"""Replay the Stage 2 first screen and Blizzard lava cycle with native controller input; capture graphics, state and audio."""
from pathlib import Path
import argparse
import hashlib
import json
import os
import shutil
import subprocess

p = argparse.ArgumentParser()
for name in ['mesen', 'rom', 'pack', 'out', 'state1', 'state2', 'state3', 'state4']:
    p.add_argument('--' + name, required=True)
p.add_argument('--frames',type=int,default=720)
p.add_argument('--route',required=True,help='JSON file mapping route names to Lua controller fields')
p.add_argument('--stride', type=int, default=1)
p.add_argument('--native',action='store_true')
a = p.parse_args()
root = Path(__file__).resolve().parents[1]
mesen, rom, pack, out = [Path(v).resolve() for v in [a.mesen, a.rom, a.pack, a.out]]
assert not subprocess.run(['pgrep', '-x', 'Mesen'], capture_output=True).stdout.strip(), 'Close Mesen first'
out.mkdir(parents=True, exist_ok=True)
installed = mesen.parent / 'HdPacks' / rom.stem
hashes = lambda folder: {p.name: hashlib.sha256(p.read_bytes()).hexdigest()
                         for p in folder.iterdir() if p.is_file()}
expected = hashes(pack)
subprocess.run(['c++', '-shared', '-fPIC', '-O2', str(root/'scripts/record_audio.cpp'),
                '-o', str(out/'record_audio.so'), '-ldl'], check=True)
template = r'''
local root='__OUT__/'
local h=assert(io.open('__STATE__','rb'));local state=h:read('*a');h:close()
local loaded=false;local frame=0;local apu={}
local function save(name,data)local f=assert(io.open(root..name,'wb'));f:write(data);f:close()end
local function bytes(kind,count)local t={};for i=0,count-1 do t[#t+1]=string.char(emu.read(i,kind))end;return table.concat(t)end
emu.addMemoryCallback(function()
 if not loaded then loaded=true;emu.loadSavestate(state)end
end,emu.callbackType.exec,0x8000,0xffff)
emu.addMemoryCallback(function(addr,value)
 if loaded and addr~=0x4014 and addr~=0x4016 then apu[#apu+1]=string.format('%d,%04X,%02X',frame,addr,value)end
end,emu.callbackType.write,0x4000,0x4017)
emu.addEventCallback(function()
 if not loaded or frame>=__END__ then return end
 frame=frame+1
 if frame%__STRIDE__==0 then
 save(string.format('dumps/%04d.ram',frame),bytes(emu.memType.nesInternalRam,2048))
 save(string.format('dumps/%04d.ppu',frame),bytes(emu.memType.nesPpuMemory,16384))
 save(string.format('dumps/%04d.oam',frame),bytes(emu.memType.nesSpriteRam,256))
 end
 if frame%__STRIDE__==0 then
  save(string.format('frames/%04d.png',frame),emu.takeScreenshot())
 end
 if frame%20==0 then local lines={};for k,v in pairs(emu.getState())do lines[#lines+1]=tostring(k)..'='..tostring(v)end;table.sort(lines);save(string.format('dumps/%04d.state',frame),table.concat(lines,'\n'))end
 if frame==__END__ then save('apu.tsv',table.concat(apu,'\n'));save('completed.txt','__END__');emu.stop(0)end
end,emu.eventType.endFrame)
emu.addEventCallback(function()
 emu.setInput({__INPUT__},0)
end,emu.eventType.inputPolled)
'''
routes = json.loads(Path(a.route).read_text())
for case, route in routes.items():
    frames = route.get('frames',a.frames) if isinstance(route,dict) else a.frames
    state = getattr(a,'state'+str(route.get('state',1))) if isinstance(route,dict) else a.state1
    route = route['input'] if isinstance(route,dict) else route
    state = Path(state).resolve()
    d = out/case
    (d/'frames').mkdir(parents=True, exist_ok=True)
    (d/'dumps').mkdir(exist_ok=True)
    if installed.exists():
        shutil.rmtree(installed)
    shutil.copytree(pack, installed, copy_function=shutil.copyfile)
    assert hashes(installed) == expected
    (d/'installed_pack_sha256.json').write_text(json.dumps(expected, indent=2, sort_keys=True)+'\n')
    (d/'input.json').write_text(json.dumps({'state_sha256': hashlib.sha256(state.read_bytes()).hexdigest(),
                                         'rom_sha1': hashlib.sha1(rom.read_bytes()).hexdigest(), 'controller_route': route}, indent=2)+'\n')
    script = template.replace('__OUT__', str(d)).replace('__STATE__', str(state)).replace('__INPUT__', route).replace('__END__',str(frames)).replace('__STRIDE__',str(a.stride))
    (d/'replay.lua').write_text(script)
    env = os.environ.copy()
    env.update(LD_PRELOAD=str(out/'record_audio.so')+':/usr/lib/x86_64-linux-gnu/libstdc++.so.6',
               HOLY_DIVER_MESEN_CORE=str(mesen.parent/'MesenCore.so'),
               HOLY_DIVER_AUDIO_CAPTURE=str(d/'full.wav'))
    with (d/'run.log').open('w') as log:
        subprocess.run([str(mesen), '--testrunner', '--timeout=180', '--nes.enableHdPacks='+str(not a.native).lower(),
                        str(rom), str(d/'replay.lua')], env=env, stdout=log, stderr=subprocess.STDOUT, check=True)
    assert (d/'completed.txt').read_text() == str(frames)
    actual=hashes(installed)
    (d/'installed_pack_after_sha256.json').write_text(json.dumps(actual,indent=2,sort_keys=True)+'\n')
    assert actual == expected, 'Installed pack changed during replay: '+str(sorted(k for k in set(actual)|set(expected) if actual.get(k)!=expected.get(k)))
    print('Completed', case, flush=True)
