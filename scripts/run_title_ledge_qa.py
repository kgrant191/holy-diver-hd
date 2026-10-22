"""Replay title/reset and both cliff edges in both directions, without RAM writes."""
from pathlib import Path
import argparse
import hashlib
import json
import os
import shutil
import subprocess

parser = argparse.ArgumentParser()
parser.add_argument('--mesen', required=True)
parser.add_argument('--rom', required=True)
parser.add_argument('--pack', required=True)
parser.add_argument('--out', required=True)
parser.add_argument('--case', choices=['title', 'ledges', 'upper_right', 'upper_left', 'lower_right', 'lower_left'])
args = parser.parse_args()
root = Path(__file__).resolve().parents[1]
mesen, rom, pack, out = [Path(v).resolve() for v in (args.mesen, args.rom, args.pack, args.out)]
assert not subprocess.run(['pgrep', '-x', 'Mesen'], capture_output=True).stdout.strip(), 'Close Mesen before installing the test pack'
out.mkdir(parents=True, exist_ok=True)
installed = mesen.parent / 'HdPacks' / rom.stem
expected_pack = {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in pack.iterdir() if p.is_file()}
subprocess.run(['c++', '-shared', '-fPIC', '-O2', str(root/'scripts/record_audio.cpp'),
                '-o', str(out/'record_audio.so'), '-ldl'], check=True)
template = r'''
local root='__OUT__/'
local frame=0;local apu={}
local function save(name,data)local f=assert(io.open(root..name,'wb'));f:write(data);f:close()end
local function bytes(kind,start,count)local t={};for i=start,start+count-1 do t[#t+1]=string.char(emu.read(i,kind))end;return table.concat(t)end
emu.addMemoryCallback(function(addr,value)
 if addr~=0x4014 and addr~=0x4016 then apu[#apu+1]=string.format('%d,%04X,%02X',frame,addr,value)end
end,emu.callbackType.write,0x4000,0x4017)
emu.addEventCallback(function()
 if frame>=__END__ then return end
 frame=frame+1
 if frame%4==0 then
  save(string.format('dumps/%04d.ram',frame),bytes(emu.memType.nesInternalRam,0,2048))
  save(string.format('dumps/%04d.ppu',frame),bytes(emu.memType.nesPpuMemory,0,16384))
  save(string.format('dumps/%04d.oam',frame),bytes(emu.memType.nesSpriteRam,0,256))
 end
 if frame%20==0 then save(string.format('frames/%04d.png',frame),emu.takeScreenshot())end
 __RESET__
 if frame==__END__ then save('apu.tsv',table.concat(apu,'\n'));save('completed.txt',tostring(frame));emu.stop(0)end
end,emu.eventType.endFrame)
emu.addEventCallback(function()
 emu.setInput({__CONTROLS__,b=false,select=false,up=false,down=false},0)
end,emu.eventType.inputPolled)
'''
cases = ['title', 'upper_right', 'upper_left', 'lower_right', 'lower_left']
if args.case == 'ledges':
    cases = cases[1:]
elif args.case:
    cases = [args.case]
for case in cases:
    case_out = out / case
    (case_out/'frames').mkdir(parents=True, exist_ok=True)
    (case_out/'dumps').mkdir(exist_ok=True)
    # Do not restore old timestamps: workspace sync can otherwise replace a
    # freshly installed baseline with a newer candidate from another replica.
    shutil.copytree(pack, installed, dirs_exist_ok=True, copy_function=shutil.copyfile)
    assert all(hashlib.sha256((installed/name).read_bytes()).hexdigest() == sha for name, sha in expected_pack.items())
    (case_out/'installed_pack_sha256.json').write_text(json.dumps(expected_pack, indent=2, sort_keys=True)+'\n')
    reset = ''
    if case == 'title':
        end = 1800
        controls = 'start=(frame>=300 and frame<303)or(frame>=480 and frame<483)or(frame>=1200 and frame<1203)or(frame>=1380 and frame<1383),right=false,left=false,a=false'
        reset = 'if frame==900 then emu.reset()end'
    elif case.startswith('upper'):
        end = 1000
        turn = '(frame>=780 and frame<784)' if case.endswith('left') else 'false'
        controls = 'start=(frame>130 and frame<700 and frame%90<10),right=(frame>=730 and frame<758)or(frame>=900 and frame<960),left='+turn+',a=false'
    else:
        end = 1320
        turn = 'or(frame>=1140 and frame<1144)' if case.endswith('left') else ''
        controls = 'start=(frame>130 and frame<700 and frame%90<10),right=(frame>=730 and frame<820)or(frame>=1100 and frame<1120)or(frame>=1220 and frame<1260),left=(frame>=940 and frame<1004)'+turn+',a=(frame>=744 and frame<760)or(frame>=940 and frame<956)'
    script = (template.replace('__OUT__', str(case_out).replace("'", "\\'"))
              .replace('__END__', str(end)).replace('__RESET__', reset)
              .replace('__CONTROLS__', controls))
    (case_out/'replay.lua').write_text(script)
    env = os.environ.copy()
    env.update(LD_PRELOAD=str(out/'record_audio.so')+':/usr/lib/x86_64-linux-gnu/libstdc++.so.6',
               HOLY_DIVER_MESEN_CORE=str(mesen.parent/'MesenCore.so'),
               HOLY_DIVER_AUDIO_CAPTURE=str(case_out/'full.wav'))
    with (case_out/'run.log').open('w') as log:
        subprocess.run([str(mesen), '--testrunner', '--timeout=180', '--nes.enableHdPacks=true',
                        str(rom), str(case_out/'replay.lua')], env=env, stdout=log,
                       stderr=subprocess.STDOUT, check=True)
    assert (case_out/'completed.txt').read_text() == str(end)
    assert all(hashlib.sha256((installed/name).read_bytes()).hexdigest() == sha for name, sha in expected_pack.items()), 'Installed pack changed during replay'
    print('Completed', case, flush=True)
