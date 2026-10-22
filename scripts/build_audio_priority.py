"""Keep weapon/Select priority fix while restoring native entrance thunder masking.

The extra pulse-1 voice of thunder $26 was originally masked by track $1E.
Only exclude that candidate when the entrance backing track is active.
All music/effect data are retained; the ROM on disk is untouched.
"""
from pathlib import Path
import json
root=Path(__file__).resolve().parents[1];pack=root/'build/Holy_Diver_(Tr)'
sha1='FE2FCD0AD334D792DB16535D09F3AB9FB2BEA3AC'
gate=bytes.fromhex('B9 30 01 30 2D 48 8A 48 A5 E5 D0 23 AD 33 01 30 1E AA BD 40 01 F0 18 BD B8 01 C9 1E D0 11 B9 30 01 AA BD B8 01 C9 26 D0 06 68 AA 68 A9 FF 60 68 AA 68 60')
assert len(gate)==51
edits=[(0x12D8A,b'\xC0',b'\xC3'),(0x12D95,b'\xC4',b'\xC7'),
       (0x12099,bytes.fromhex('B9 30 01'),bytes.fromhex('20 2A FD')),
       (0x1FD3A,b'\xff'*51,gate)]
patch=bytearray(b'PATCH')
for offset,before,after in edits:
 patch+=offset.to_bytes(3,'big')+len(after).to_bytes(2,'big')+after
patch+=b'EOF'
(pack/'Entrance_SFX_Priority.ips').write_bytes(patch)
p=pack/'hires.txt';s=p.read_text();assert '<patch>' not in s
s=s.replace('<scale>2','<scale>2\n<patch>Entrance_SFX_Priority.ips,'+sha1,1);p.write_text(s)
(root/'audio_priority_patch.json').write_text(json.dumps({'target_rom_sha1':sha1.lower(),
 'scope':'Entrance track $1E pulse priorities plus conditional thunder $26 pulse-1 exclusion',
 'edits':[{'file_offset_hex':f'{o:06X}','before_hex':b.hex().upper(),'after_hex':a.hex().upper()} for o,b,a in edits],
 'original_rom_file_modified':False,'replacement_audio':False,
 'v10_v11_compatible_save_state':True,'pre_v10_states_require_migration_or_fresh_start':True},indent=2)+'\n')
