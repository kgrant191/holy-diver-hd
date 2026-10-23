"""Check 0.3.1's bounded fireball/menu repair against the 0.3.0 candidate."""
from pathlib import Path
import argparse
import hashlib
import json
import re
import numpy as np
from PIL import Image

p=argparse.ArgumentParser()
for name in ['before','after','old-pack','out']:
    p.add_argument('--'+name,required=True)
a=p.parse_args()
root=Path(__file__).resolve().parents[1]
old_pack=Path(a.old_pack)
pack=root/'build/Holy_Diver_(Tr)'
old=json.loads((root/'evidence/0.3.0-pack-sha256.json').read_text())
new=json.loads((root/'evidence/approved-pack-sha256.json').read_text())
routes=json.loads((root/'scripts/boss1_review_routes.json').read_text())
hashes=lambda folder:{f.name:hashlib.sha256(f.read_bytes()).hexdigest() for f in folder.iterdir() if f.is_file()}
assert hashes(old_pack)==old and hashes(pack)==new
assert old.keys()==new.keys() and len(new)==78
changed=sorted(k for k in old if old[k]!=new[k])
assert changed==['Boss_Tiles_2x.png','README.txt','hires.txt']

# Only two formerly empty menu-glyph cells may change in the existing atlas.
b=np.array(Image.open(old_pack/'Boss_Tiles_2x.png').convert('RGBA'))
c=np.array(Image.open(pack/'Boss_Tiles_2x.png').convert('RGBA'))
allowed=np.zeros(b.shape[:2],bool)
allowed[272:288,272:304]=True
assert not b[allowed].any()
assert np.array_equal(b[~allowed],c[~allowed])
assert np.any(b[allowed]!=c[allowed])

# Removing just the two menu rules and rendering option recovers 0.3.0 exactly.
text=(pack/'hires.txt').read_text()
prior=re.sub(r'^# BEGIN BOSS1 OPTIONS\n.*?^# END BOSS1 OPTIONS\n','',text,flags=re.M|re.S)
prior=re.sub(r'^\[[^\n]+\]<tile>30,096[45],0F072830,[^\n]+\n','',prior,flags=re.M)
assert prior==(old_pack/'hires.txt').read_text()
assert '<options>disableSpriteLimit' in text and '<addition>' not in text

fire=np.array(Image.open(root/'art/boss1/boss_fireball_registered.png').convert('RGBA'))
fire_mask=fire[:,:,3]>0
report={'baseline':'0.3.0','candidate':'0.3.1','emulator':'MesenCE 2.2.1',
        'ram_writes':False,'sprite_limit_removed':True,
        'pack_files':len(new),'changed_pack_files':changed,'unchanged_pack_files':len(new)-len(changed),
        'changed_atlas_pixels':int(np.any(b!=c,axis=2).sum()),'previous_rules_preserved':True,
        'cases':{}}
def projectiles(oam):
    return [tuple(oam[i:i+4]) for i in range(0,256,4)
            if oam[i]<239 and 0xf1<=oam[i+1]<=0xf4 and oam[i+2]&3==0]

for case,route in routes.items():
    before,after=Path(a.before)/case,Path(a.after)/case
    frames=route['frames']
    assert (before/'completed.txt').read_text()==(after/'completed.txt').read_text()==str(frames)
    assert (before/'input.json').read_bytes()==(after/'input.json').read_bytes()
    for folder,expected in [(before,old),(after,new)]:
        assert json.loads((folder/'installed_pack_sha256.json').read_text())==expected
    # The retained 0.3.0 combat captures predate the runner's after-run hash
    # export. Require it for every new run; check it in old runs when present.
    assert json.loads((after/'installed_pack_after_sha256.json').read_text())==new
    if (before/'installed_pack_after_sha256.json').exists():
        assert json.loads((before/'installed_pack_after_sha256.json').read_text())==old
    r={'frames':frames,**json.loads((after/'input.json').read_text())}
    for ext in ['ram','ppu','oam']:
        files=sorted((before/'dumps').glob('*.'+ext))
        assert len(files)==frames
        for f in files:
            assert f.read_bytes()==(after/'dumps'/f.name).read_bytes(),(case,f.name)
        r[ext+'_identical_samples']=len(files)
    apu=(before/'apu.tsv').read_bytes()
    assert apu==(after/'apu.tsv').read_bytes(),case+' APU differs'
    r['apu_sha256']=hashlib.sha256(apu).hexdigest()
    bp,cp=(before/'full.wav').read_bytes()[44:],(after/'full.wav').read_bytes()[44:]
    common=min(len(bp),len(cp))
    assert common and bp[:common]==cp[:common],case+' PCM differs'
    assert abs(len(bp)-len(cp))<=3200,case+' audio truncated'
    r.update(identical_pcm_bytes=common,before_pcm_bytes=len(bp),after_pcm_bytes=len(cp),
             shutdown_tail_difference_bytes=abs(len(bp)-len(cp)))
    changed_frames=[];complete_fire=[];menu_frames=[];equipped_cursor_rows=set();empty_frames=[]
    for f in range(1,frames+1):
        filename=f'{f:04}.png'
        if not (before/'frames'/filename).stat().st_size or not (after/'frames'/filename).stat().st_size:
            assert f==1 and (before/'frames'/filename).read_bytes()==(after/'frames'/filename).read_bytes()
            empty_frames.append(f)
            continue
        before_im=np.array(Image.open(before/'frames'/filename).convert('RGB'))
        after_im=np.array(Image.open(after/'frames'/filename).convert('RGB'))
        diff=np.any(before_im!=after_im,axis=2)
        q=(after/'dumps'/f'{f:04}.ppu').read_bytes()
        if case=='menu_blizzard':
            allowed=np.zeros(diff.shape,bool)
            allowed[176:192,336:368]=True
            if (q[0x20e3],q[0x212f],q[0x3f11])==(0x86,0x82,0x0f):
                assert q[0x216f:0x2177]==bytes.fromhex('6b 59 83 62 62 5a 64 65')
                menu_frames.append(f)
                o=(after/'dumps'/f'{f:04}.oam').read_bytes()
                equipped_cursor_rows.update(o[i] for i in range(0,256,4) if o[i]<239 and o[i+1]==0x48)
        else:
            # endFrame OAM describes the following render. The preceding dump
            # provides the actual projectile rectangles in this screenshot.
            o=(after/'dumps'/f'{max(1,f-1):04}.oam').read_bytes()
            shots=projectiles(o)
            allowed=np.zeros(diff.shape,bool)
            # Removing the limit also restores other native sprites on crowded
            # scanlines. Every changed pixel must still lie in native OAM.
            for i in range(0,256,4):
                y,t,attr,x=o[i:i+4]
                if y<239:
                    allowed[(y+1)*2:min(480,(y+9)*2),x*2:min(512,(x+8)*2)]=True
            for y,t,attr,x in shots:
                if t!=0xf1 or attr!=0 or x>240 or y>222:
                    continue
                crop=after_im[(y+1)*2:(y+17)*2,x*2:(x+16)*2]
                if crop.shape==fire[:,:,:3].shape and np.array_equal(crop[fire_mask],fire[:,:,:3][fire_mask]):
                    complete_fire.append(f)
        assert not np.any(diff&~allowed),(case,f,'pixels changed outside repair')
        if diff.any():changed_frames.append(f)
    r.update(changed_screenshots=len(changed_frames),unchanged_screenshots=frames-len(changed_frames)-len(empty_frames),
             empty_load_captures=empty_frames,
             changes_confined_to='Blizzard R/D cells' if case=='menu_blizzard' else 'native sprite rectangles')
    assert changed_frames
    if case=='menu_blizzard':
        assert len(menu_frames)>200 and {71,87}<=equipped_cursor_rows
        r.update(menu_frames=len(menu_frames),equipped_cursor_rows=sorted(equipped_cursor_rows),
                 selection_and_resume_observed=True)
    else:
        assert len(complete_fire)>20
        r.update(complete_fireball_screenshots=len(set(complete_fire)),
                 complete_fireball_examples=sorted(set(complete_fire))[:20])
        # Frames 20–23 still overlap the boss's native foreground sprites.
        if case=='crouch':assert set(range(24,34))<=set(complete_fire)
    report['cases'][case]=r
report['total_frames_per_build']=sum(r['frames'] for r in routes.values())
report['all_changes_within_requested_visuals']=True
out=Path(a.out);out.parent.mkdir(parents=True,exist_ok=True)
out.write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({k:v for k,v in report.items() if k!='cases'},indent=2))
