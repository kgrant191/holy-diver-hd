"""Replay three chapel states with native movement, combat and death transitions."""
from pathlib import Path
import argparse
import hashlib
import json
import os
import shutil
import subprocess

p = argparse.ArgumentParser()
for name in ['mesen', 'rom', 'pack', 'out', 'state1', 'state2', 'state3']:
    p.add_argument('--' + name, required=True)
p.add_argument('--case', choices=['state1','state2','state3'])
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
 if not loaded or frame>=720 then return end
 frame=frame+1
 if frame%2==0 then
 save(string.format('dumps/%04d.ram',frame),bytes(emu.memType.nesInternalRam,2048))
 save(string.format('dumps/%04d.ppu',frame),bytes(emu.memType.nesPpuMemory,16384))
 save(string.format('dumps/%04d.oam',frame),bytes(emu.memType.nesSpriteRam,256))
 end
 if frame%4==0 or(frame>=180 and frame<=250 and frame%2==0)then
  save(string.format('frames/%04d.png',frame),emu.takeScreenshot())
 end
 if frame==720 then save('apu.tsv',table.concat(apu,'\n'));save('completed.txt','720');emu.stop(0)end
end,emu.eventType.endFrame)
emu.addEventCallback(function()
 emu.setInput({__INPUT__},0)
end,emu.eventType.inputPolled)
'''
routes = [
    'right=(frame>=40 and frame<400)or(frame>=480 and frame<650),left=(frame>=410 and frame<450),a=(frame>=62 and frame<88)or(frame>=180 and frame<205)or(frame>=300 and frame<325)or(frame>=500 and frame<525),b=(frame>=120 and frame<400 and frame%32<3),up=false,down=false,start=false,select=false',
    'right=(frame>=40 and frame<220)or(frame>=400 and frame<600),left=(frame>=240 and frame<350),a=(frame>=55 and frame<80)or(frame>=165 and frame<190)or(frame>=410 and frame<435),b=(frame>=85 and frame<600 and frame%32<3),up=false,down=false,start=false,select=(frame>=360 and frame<364)',
    'left=(frame>=40 and frame<170),right=(frame>=210 and frame<500),a=(frame>=270 and frame<295)or(frame>=390 and frame<415),b=(frame>=55 and frame<500 and frame%32<3),up=(frame>=100 and frame<135),down=false,start=(frame>=550 and frame<554)or(frame>=590 and frame<594),select=(frame>=180 and frame<184)',
]
for i, state in enumerate([a.state1, a.state2, a.state3]):
    case = f'state{i+1}'
    if a.case and a.case != case:
        continue
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
                                         'rom_sha1': hashlib.sha1(rom.read_bytes()).hexdigest(), 'controller_route': routes[i]}, indent=2)+'\n')
    script = template.replace('__OUT__', str(d)).replace('__STATE__', str(state)).replace('__INPUT__', routes[i])
    (d/'replay.lua').write_text(script)
    env = os.environ.copy()
    env.update(LD_PRELOAD=str(out/'record_audio.so')+':/usr/lib/x86_64-linux-gnu/libstdc++.so.6',
               HOLY_DIVER_MESEN_CORE=str(mesen.parent/'MesenCore.so'),
               HOLY_DIVER_AUDIO_CAPTURE=str(d/'full.wav'))
    with (d/'run.log').open('w') as log:
        subprocess.run([str(mesen), '--testrunner', '--timeout=180', '--nes.enableHdPacks=true',
                        str(rom), str(d/'replay.lua')], env=env, stdout=log, stderr=subprocess.STDOUT, check=True)
    assert (d/'completed.txt').read_text() == '720'
    assert hashes(installed) == expected, 'Installed pack changed during replay'
    print('Completed', case, flush=True)
