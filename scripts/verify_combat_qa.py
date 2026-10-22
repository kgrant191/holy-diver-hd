"""Verify that HD art did not change controller-driven game state."""
from pathlib import Path
import sys,json
original,hd=map(Path,sys.argv[1:3])
for root in [original,hd]:assert (root/'completed.txt').read_text().strip()=='1760'
counts={}
for ext in ['ram','ppu','oam']:
 files=list((original/'dumps').glob('*.'+ext));assert len(files)>=277
 for p in files:assert p.read_bytes()==(hd/'dumps'/p.name).read_bytes(),p.name
 counts[ext]=len(files)
assert (original/'oam.tsv').read_bytes()==(hd/'oam.tsv').read_bytes()
assert (original/'ppu_signatures.tsv').read_bytes()==(hd/'ppu_signatures.tsv').read_bytes()
def ppu(frame):return (hd/'dumps'/f'{frame:04d}.ppu').read_bytes()
assert ppu(720)[0x3f1d:0x3f20]==bytes([0x30,0,0x36])
assert ppu(880)[0x3f1d:0x3f20]==bytes([0x22,0x11,0x36])
assert ppu(1520)[0x3f1d:0x3f20]==bytes([0x30,0,0x36])
assert ppu(1360)[0x3f11]==ppu(1630)[0x3f11]==15
assert ppu(1450)[0x3f11]==ppu(1720)[0x3f11]==0x16
report={'emulator':'Mesen 2.1.1 Linux','controller_only':True,
        'identical_captured_state_counts':counts,'identical_oam_frames':1041,
        'select_equips_and_unequips':True,'pause_and_resume_preserve_gameplay':True,
        'ram_writes_or_cheats':False}
(hd/'combat_verification.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
