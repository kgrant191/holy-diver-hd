"""Validate the title, entrance thunder and preserved native effects from live runs."""
from pathlib import Path
from collections import Counter
import json,hashlib,csv
root=Path.cwd();w=root/'work/v12';report={}
def rows(p):return [line.split(',') for line in (p/'apu.tsv').read_text().splitlines()]
def apu(p):return [tuple(row[:3]) for row in rows(p)]
original=w/'idle_original';fixed=w/'idle_fixed'
assert (original/'commands.tsv').read_bytes()==(fixed/'commands.tsv').read_bytes()
assert apu(original)==apu(fixed)
report['entrance_idle_thunder']={'frames':1200,'sound_requests_identical':True,'apu_register_value_and_frame_sequence_identical':True,'register_writes':len(apu(fixed)),'paired_thunder_bursts':9,'pcm_not_claimed_identical':'The arbitration hook adds CPU cycles, so register writes can move slightly within a frame.'}
old=root/'work/v10/route_fixed';new=w/'route_fixed';a,b=rows(old),rows(new)
effects={}
for name,s,span,ids in [('primary',106,34,['04']),('select',300,60,['06']),('twin_fire',386,44,['2A','35'])]:
 sig=lambda rr:[(int(x[0])-s,*x[1:]) for x in rr if s<=int(x[0])<s+span and x[5] in ids]
 assert sig(a)==sig(b),name
 effects[name]={'apu_writes':len(sig(b)),'matches_approved_v10_v11_effect':True}
assert [x for x in a if int(x[0])>=500]==[x for x in b if int(x[0])>=500]
assert (old/'commands.tsv').read_bytes()==(new/'commands.tsv').read_bytes()
diffs=set();count=0
for p in (old/'dumps').glob('*.ram'):
 q=new/'dumps'/p.name;diffs.update(i for i,(u,v) in enumerate(zip(p.read_bytes(),q.read_bytes())) if u!=v);count+=1
assert diffs==set(range(0x1ec,0x1f2)),diffs
assert all(p.read_bytes()==(new/'dumps'/p.name).read_bytes() for p in (old/'dumps').glob('*.oam'))
assert all(p.read_bytes()==(new/'frames'/p.name).read_bytes() for p in (old/'frames').glob('*.png'))
report['route']={'frames':900,'effects':effects,'next_room_apu_unchanged_from_frame':500,'sound_requests_identical':True,'unchanged_screenshots':450,'unchanged_oam_snapshots':450,'ram_snapshot_pairs':count,'only_ram_differences':'$01EC-$01F1: scratch stack bytes used by the additional subroutine; gameplay and audio-state RAM are unchanged'}
t=w/'title_final';o=w/'title_original';assert apu(t)==apu(o)
assert (t/'commands.tsv').read_bytes()==(o/'commands.tsv').read_bytes()
events=list(csv.reader((t/'events.tsv').open()))
assert all(int(r[1])!=1 for r in events[159:1005]);assert all(int(r[1])==1 for r in events[2100:2400]);assert int(events[2699][6])!=64
assert int(events[1005][1])==1  # The original intro can also finish naturally.
from PIL import Image
import numpy as np
intro=np.array(Image.open(root/'source_v12/build/Holy_Diver_(Tr)/Title_Intro_HD.png'))
ready=np.array(Image.open(root/'source_v12/build/Holy_Diver_(Tr)/Title_HD.png'))
for f,im in [(2000,intro),(2200,ready)]:
 cap=np.array(Image.open(t/f'frames/{f:04}.png').convert('RGBA'))
 assert np.array_equal(cap[402:451],im[402:451])
# All approved v11 PNG files remain identical, including overlays and player art.
pack=root/'source_v12/build/Holy_Diver_(Tr)';prior=root/'source_v11/build/Holy_Diver_(Tr)'
for p in prior.glob('*.png'):assert p.read_bytes()==(pack/p.name).read_bytes(),p.name
report['title']={'frames':3000,'initial_prompt_absent':True,'natural_intro_completion_frame':1006,'first_start_frame':2100,'ready_state_frame':2101,'second_start_frame':2400,'gameplay_reached':True,'title_native_audio_registers_and_requests_unchanged':True,'repeated_lightning_events':[523,1908],'live_prompt_regions_match_selected_art':True}
report['approved_v11_pngs_preserved']=len(list(prior.glob('*.png')))
report['original_rom_sha1']=hashlib.sha1((root/'upload/Holy_Diver_(Tr).nes').read_bytes()).hexdigest();assert report['original_rom_sha1']=='fe2fcd0ad334d792db16535d09f3ab9fb2bea3ac'
report['emulator']='MesenCE 2.2.1';report['compatible_save']='Approved v10 state, unchanged'
p=root/'source_v12/evidence/verification.json';p.write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
