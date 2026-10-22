"""Verify stationary cliff/tree landings against an original-graphics replay."""
from pathlib import Path
import json, sys
original, hd = map(Path, sys.argv[1:3])
assert (hd/'completed.txt').read_text().strip()=='1160'
# Mesen may deliver one additional callback after emu.stop(). Compare the
# complete requested interval explicitly, excluding any post-stop callback.
def measured_oam(path):
    return [line for line in (path/'oam.tsv').read_text().splitlines()
            if 720<=int(line.split('\t')[0])<=1160]
assert len(measured_oam(original))==len(measured_oam(hd))==441
assert measured_oam(original)==measured_oam(hd)
assert (original/'state.tsv').read_bytes()==(hd/'state.tsv').read_bytes()
samples=list((hd/'ram').glob('*.bin'))
assert len(samples)==111
for p in samples:assert p.read_bytes()==(original/'ram'/p.name).read_bytes(),p.name
oam={}
for line in (hd/'oam.tsv').read_text().splitlines():
    fields=line.split('\t')
    oam[int(fields[0])]=[tuple(map(int,v.split(','))) for v in fields[1:]]
results=[]
for name,frame,world_y in [('start_ledge',720,96),('tree_upper_left',900,192),('left_wall_ledge',1120,272)]:
    assert (original/(name+'.ram')).read_bytes()==(hd/(name+'.ram')).read_bytes()
    stable=[]
    # Start moves after ten frames; the other two checkpoints hold for 29+ frames.
    for f in range(frame, frame+(9 if frame==720 else 29),4):
        ram=(hd/'ram'/f'{f:04d}.bin').read_bytes()
        player=[v for v in oam[f] if v[2]&3==3 and 1<=v[1]<64]
        assert player and all(v[1]<=9 for v in player)
        feet=max(v[0]+9 for v in player)+ram[0x3cf]
        assert feet==world_y,(name,f,feet)
        stable.append(f)
    results.append({'location':name,'capture_frame':frame,'nes_world_surface_y':world_y,
                    'hd_world_surface_y':2*world_y,'stationary_frames':stable})
report={'emulator':'Mesen 2.1.1','controller_only':True,'ram_writes_or_cheats':False,
        'all_ram_oam_and_ppu_samples_match_original':True,'ram_samples':len(samples),'landings':results}
(hd/'wall_verification.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
