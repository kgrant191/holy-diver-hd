"""Replay both user-supplied ledges: full left travel, then slow right walk-off."""
from pathlib import Path
import argparse
import hashlib
import json
import os
import shutil
import subprocess

p = argparse.ArgumentParser()
for name in ['mesen', 'rom', 'pack', 'out', 'upper-state', 'lower-state']:
    p.add_argument('--' + name, required=True)
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
 if not loaded or frame>=460 then return end
 frame=frame+1
 save(string.format('dumps/%04d.ram',frame),bytes(emu.memType.nesInternalRam,2048))
 save(string.format('dumps/%04d.ppu',frame),bytes(emu.memType.nesPpuMemory,16384))
 save(string.format('dumps/%04d.oam',frame),bytes(emu.memType.nesSpriteRam,256))
 if frame%4==0 or (frame>=__EDGE__-12 and frame<=__EDGE__+20)then
  save(string.format('frames/%04d.png',frame),emu.takeScreenshot())
 end
 if frame==460 then save('apu.tsv',table.concat(apu,'\n'));save('completed.txt','460');emu.stop(0)end
end,emu.eventType.endFrame)
emu.addEventCallback(function()
 emu.setInput({left=(frame>=10 and frame<130),right=(frame>=160 and frame<440 and frame%8<2),
 a=false,b=false,up=false,down=false,start=false,select=false},0)
end,emu.eventType.inputPolled)
'''
for case, state, edge in [('upper', a.upper_state, 353), ('lower', a.lower_state, 417)]:
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
                                         'rom_sha1': hashlib.sha1(rom.read_bytes()).hexdigest()}, indent=2)+'\n')
    script = template.replace('__OUT__', str(d)).replace('__STATE__', str(state)).replace('__EDGE__', str(edge))
    (d/'replay.lua').write_text(script)
    env = os.environ.copy()
    env.update(LD_PRELOAD=str(out/'record_audio.so')+':/usr/lib/x86_64-linux-gnu/libstdc++.so.6',
               HOLY_DIVER_MESEN_CORE=str(mesen.parent/'MesenCore.so'),
               HOLY_DIVER_AUDIO_CAPTURE=str(d/'full.wav'))
    with (d/'run.log').open('w') as log:
        subprocess.run([str(mesen), '--testrunner', '--timeout=180', '--nes.enableHdPacks=true',
                        str(rom), str(d/'replay.lua')], env=env, stdout=log, stderr=subprocess.STDOUT, check=True)
    assert (d/'completed.txt').read_text() == '460'
    assert hashes(installed) == expected, 'Installed pack changed during replay'
    print('Completed', case, flush=True)
