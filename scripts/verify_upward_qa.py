"""Compare identical v10/v11 Mesen replays: graphics-only upward fix."""
from pathlib import Path
import argparse,hashlib,json,wave
import numpy as np
from PIL import Image

p=argparse.ArgumentParser()
p.add_argument('--before',required=True);p.add_argument('--after',required=True)
p.add_argument('--report',required=True)
a=p.parse_args();before=Path(a.before);after=Path(a.after)
assert (before/'completed.txt').read_text()==(after/'completed.txt').read_text()=='960'
counts={}
for extension in ['ram','oam','ppu']:
    files=list((before/'dumps').glob('*.'+extension));assert len(files)==480
    assert all(f.read_bytes()==(after/'dumps'/f.name).read_bytes() for f in files),extension
    counts[extension]=len(files)
assert (before/'apu.tsv').read_bytes()==(after/'apu.tsv').read_bytes()
assert (before/'commands.tsv').read_bytes()==(after/'commands.tsv').read_bytes()
with wave.open(str(before/'full.wav')) as x,wave.open(str(after/'full.wav')) as y:
    assert x.getparams()[:3]==y.getparams()[:3]
    n=min(x.getnframes(),y.getnframes());assert x.readframes(n)==y.readframes(n)
    audio={'sample_frames_compared':n,'sample_rate':x.getframerate(),'channels':x.getnchannels(),'pcm_identical':True}
cases={'primary_right':40,'twin_right':200,'twin_left':380,'primary_left':540,'air_primary_left':730,'air_twin_left':870}
details={}
for case,frame in cases.items():
    old=np.array(Image.open(before/'frames'/f'{frame:04}.png').convert('RGB'))
    new=np.array(Image.open(after/'frames'/f'{frame:04}.png').convert('RGB'))
    d=np.any(old!=new,axis=2);yy,xx=np.where(d)
    assert len(xx)>300,(case,len(xx))
    assert xx.min()>360 and xx.max()<470,(case,xx.min(),xx.max())
    details[case]={'frame':frame,'changed_pixels':len(xx),'changed_bbox':[int(xx.min()),int(yy.min()),int(xx.max()+1),int(yy.max()+1)]}
# Idle, existing cast wind-up and jump frames must remain pixel-identical.
unchanged=[2,20,34,36,162,194,196,344,346,374,376,534,536,714,724,726,864,866]
for frame in unchanged:
    assert (before/'frames'/f'{frame:04}.png').read_bytes()==(after/'frames'/f'{frame:04}.png').read_bytes(),frame
report={'emulator':'MesenCE 2.2.1','frames':960,'dump_pairs_identical':counts,'apu_writes_identical':True,'sound_commands_identical':True,'audio':audio,'upward_cases':details,'unchanged_frame_checks':unchanged,'controller_only_after_loading_approved_v10_state':True}
Path(a.report).write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
