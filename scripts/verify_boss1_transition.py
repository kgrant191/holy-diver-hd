"""Verify the bounded 0.3.2 ascent/fade repair against 0.3.1 live captures."""
from pathlib import Path
import argparse
import hashlib
import json
import re
import numpy as np
from PIL import Image

p=argparse.ArgumentParser()
for name in ['before','after','old-pack','out']:p.add_argument('--'+name,required=True)
a=p.parse_args()
root=Path(__file__).resolve().parents[1]
old_pack=Path(a.old_pack);pack=root/'build/Holy_Diver_(Tr)'
old=json.loads((root/'evidence/0.3.1-pack-sha256.json').read_text())
new=json.loads((root/'evidence/approved-pack-sha256.json').read_text())
routes=json.loads((root/'scripts/boss1_transition_routes.json').read_text())
hashes=lambda folder:{f.name:hashlib.sha256(f.read_bytes()).hexdigest() for f in folder.iterdir() if f.is_file()}
assert hashes(old_pack)==old and hashes(pack)==new
assert len(new)==79 and new.keys()-old.keys()=={'Blizzard_Ascent_Background.png'}
changed=sorted(k for k in old if old[k]!=new[k])
assert changed==['Boss_Tiles_2x.png','README.txt','hires.txt']

# Only appended atlas cells may change; every old cell stays byte-identical.
b=np.array(Image.open(old_pack/'Boss_Tiles_2x.png').convert('RGBA'))
c=np.array(Image.open(pack/'Boss_Tiles_2x.png').convert('RGBA'))
cells_b=b.reshape(32,16,32,16,4).transpose(0,2,1,3,4).reshape(1024,16,16,4)
cells_c=c.reshape(32,16,32,16,4).transpose(0,2,1,3,4).reshape(1024,16,16,4)
assert np.array_equal(cells_b[:563],cells_c[:563])
assert not cells_b[563:676].any() and not cells_c[676:].any()
wall=np.array(Image.open(pack/'Nave_Background.png').convert('RGB'))
assert np.array_equal(np.tile(wall,(3,1,1)),np.array(Image.open(pack/'Blizzard_Ascent_Background.png')))

# Remove only the new bank-00 fades and restore the single backdrop reference.
text=(pack/'hires.txt').read_text()
prior=re.sub(r'^<condition>bossCopy0_FF(?:202020|101010|000000)_[^\n]+\n','',text,flags=re.M)
prior,n=re.subn(r'^\[blizzardDataLo&blizzardDataHi[^\n]*\]<tile>30,00[0-9A-F]{2},FF(?:202020|101010|000000),[^\n]+\n','',prior,flags=re.M)
assert n==435
prior=prior.replace('<background>Blizzard_Ascent_Background.png,','<background>Nave_Background.png,')
assert prior==(old_pack/'hires.txt').read_text()
assert '<options>disableSpriteLimit' in text and '<addition>' not in text

report={'baseline':'0.3.1','candidate':'0.3.2','emulator':'MesenCE 2.2.1','ram_writes':False,
        'pack_files':79,'changed_existing_files':changed,'added_files':['Blizzard_Ascent_Background.png'],
        'unchanged_existing_files':75,'prior_atlas_cells_preserved':563,'new_atlas_cells':113,
        'added_tile_rules':435,'added_conditions':243,'prior_rules_preserved_except_bell_backdrop':True,
        'backdrop_is_exact_threefold_repeat':True,'cases':{}}

for case,route in routes.items():
    before,after=Path(a.before)/case,Path(a.after)/case
    frames=route['frames']
    assert (before/'completed.txt').read_text()==(after/'completed.txt').read_text()==str(frames)
    assert (before/'input.json').read_bytes()==(after/'input.json').read_bytes()
    for folder,expected in [(before,old),(after,new)]:
        for filename in ['installed_pack_sha256.json','installed_pack_after_sha256.json']:
            assert json.loads((folder/filename).read_text())==expected
    r={'frames':frames,**json.loads((after/'input.json').read_text())}
    for ext in ['ram','ppu','oam']:
        files=sorted((before/'dumps').glob('*.'+ext));assert len(files)==frames
        for f in files:assert f.read_bytes()==(after/'dumps'/f.name).read_bytes(),(case,f.name)
        r[ext+'_identical_samples']=len(files)
    apu=(before/'apu.tsv').read_bytes();assert apu==(after/'apu.tsv').read_bytes()
    r['apu_sha256']=hashlib.sha256(apu).hexdigest()
    bp,cp=(before/'full.wav').read_bytes()[44:],(after/'full.wav').read_bytes()[44:]
    common=min(len(bp),len(cp));assert common and bp[:common]==cp[:common]
    assert abs(len(bp)-len(cp))<=3200
    r.update(identical_pcm_bytes=common,before_pcm_bytes=len(bp),after_pcm_bytes=len(cp),
             shutdown_tail_difference_bytes=abs(len(bp)-len(cp)))
    changed_frames=[];background_frames=[];fade_frames={k:[] for k in ['202020','101010','000000']}
    white_mask=None;white_origin=None;pickup_palette=None;facing=set();empty=[]
    for f in range(1,frames+1):
        filename=f'{f:04}.png'
        if not (before/'frames'/filename).stat().st_size or not (after/'frames'/filename).stat().st_size:
            assert f==1 and (before/'frames'/filename).read_bytes()==(after/'frames'/filename).read_bytes()
            empty.append(f);continue
        bi=np.array(Image.open(before/'frames'/filename).convert('RGB'))
        ci=np.array(Image.open(after/'frames'/filename).convert('RGB'))
        diff=np.any(bi!=ci,axis=2)
        prev=f'{f-1:04}'
        q=(after/'dumps'/(prev+'.ppu')).read_bytes()
        ram=(after/'dumps'/(prev+'.ram')).read_bytes()
        o=(after/'dumps'/(prev+'.oam')).read_bytes()
        bell=ram[0x78:0x7a]==bytes.fromhex('b285')
        pal=q[0x3f1d:0x3f20].hex()
        sprite_rect=np.zeros(diff.shape,bool)
        player=[tuple(o[i:i+4]) for i in range(0,256,4) if o[i]<239 and o[i+1]<0x60 and o[i+2]&3==3]
        for y,t,attr,x in player:sprite_rect[(y+1)*2:min(480,(y+9)*2),x*2:min(512,(x+8)*2)]=True
        if bell and player:
            facing.update(attr&0x40 for y,t,attr,x in player)
            if pal in ['300036','221136']:pickup_palette=pal
        if bell and pal=='303030' and np.max(ci[0])==0 and player:
            white_mask=np.any(ci!=0,axis=2)
            assert not np.any(white_mask&~sprite_rect)
            white_origin=(min(v[3] for v in player),min(v[0] for v in player))
        if bell and pal in fade_frames:
            assert white_mask is not None and player
            origin=(min(v[3] for v in player),min(v[0] for v in player))
            mask=np.roll(white_mask,((origin[1]-white_origin[1])*2,(origin[0]-white_origin[0])*2),axis=(0,1))
            expected=np.zeros_like(ci);expected[mask]={'202020':255,'101010':173,'000000':102}[pal]
            assert np.array_equal(ci,expected),(case,f,'HD fade silhouette differs')
            assert not np.any(diff&~sprite_rect)
            assert diff.any();fade_frames[pal].append(f)
        elif diff.any():
            assert bell and (q[0x3f05],q[0x3f09],q[0x3f0d])==(6,0,9),(case,f,'outside bell background')
            assert not np.any(bi[diff]),(case,f,'existing foreground changed')
            background_frames.append(f)
        if diff.any():changed_frames.append(f)
    if case=='crouch':assert not changed_frames
    else:
        assert len(background_frames)>200 and all(len(v)==8 for v in fade_frames.values())
        assert pickup_palette==('300036' if case=='menu_blizzard' else '221136')
        assert (64 if case=='menu_blizzard' else 0) in facing
    r.update(changed_screenshots=len(changed_frames),unchanged_screenshots=frames-len(changed_frames)-len(empty),
             empty_load_captures=empty,backdrop_only_screenshots=len(background_frames),
             backdrop_changed_range=[min(background_frames),max(background_frames)] if background_frames else [],
             fade_frames=fade_frames,pickup_palette=pickup_palette,observed_player_flip_bits=sorted(facing),
             changes_confined_to='previously empty bell backdrop and Randy fade silhouette')
    report['cases'][case]=r
report['total_frames_per_build']=sum(r['frames'] for r in routes.values())
report['native_memory_and_audio_preserved']=True
out=Path(a.out);out.parent.mkdir(parents=True,exist_ok=True);out.write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({k:v for k,v in report.items() if k!='cases'},indent=2))
