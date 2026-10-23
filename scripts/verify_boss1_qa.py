"""Verify paired native behavior, boss pose coverage and the Blizzard transition."""
from pathlib import Path
import argparse
import hashlib
import json

p=argparse.ArgumentParser()
for name in ['before','after','out']:p.add_argument('--'+name,required=True)
a=p.parse_args()
root=Path(__file__).resolve().parents[1]
routes=json.loads((root/'scripts/boss1_routes.json').read_text())
poses=json.loads((root/'art/boss1/native_poses.json').read_text())
old=json.loads((root/'evidence/0.2.1-pack-sha256.json').read_text())
expected=json.loads((root/'evidence/approved-pack-sha256.json').read_text())
report={'emulator':'MesenCE 2.2.1','baseline':'0.2.1','candidate':'0.3.0','ram_writes':False,'cases':{}}
examples={};palette_examples={};projectiles=set()
for case,route in routes.items():
    b,c=Path(a.before)/case,Path(a.after)/case
    frames=route['frames']
    assert (b/'completed.txt').read_text()==(c/'completed.txt').read_text()==str(frames)
    assert (b/'input.json').read_bytes()==(c/'input.json').read_bytes()
    assert json.loads((b/'installed_pack_sha256.json').read_text())==old
    assert json.loads((c/'installed_pack_sha256.json').read_text())==expected
    r={'emulated_frames':frames,**json.loads((c/'input.json').read_text())}
    for ext in ['ram','ppu','oam']:
        files=sorted((b/'dumps').glob('*.'+ext))
        assert len(files)==frames,(case,ext,len(files))
        for f in files:assert f.read_bytes()==(c/'dumps'/f.name).read_bytes(),(case,ext,f.name)
        r[ext+'_identical_samples']=frames
    apu=(b/'apu.tsv').read_bytes()
    assert apu==(c/'apu.tsv').read_bytes(),case+' APU mismatch'
    r['apu_sha256']=hashlib.sha256(apu).hexdigest()
    bp,cp=(b/'full.wav').read_bytes()[44:],(c/'full.wav').read_bytes()[44:]
    common=min(len(bp),len(cp))
    assert common and bp[:common]==cp[:common],case+' PCM mismatch'
    assert abs(len(bp)-len(cp))<=3200,case+' audio truncated'
    r.update(identical_pcm_bytes=common,before_pcm_bytes=len(bp),after_pcm_bytes=len(cp),shutdown_tail_difference_bytes=abs(len(bp)-len(cp)))
    images=sorted((c/'frames').glob('*.png'));assert len(images)==frames
    r['changed_screenshots']=sum(f.read_bytes()!=(b/'frames'/f.name).read_bytes()for f in images)
    assert r['changed_screenshots']>0
    boss_counts=[];pickup_frames=[];card_frames=[];stage2_frames=[];observed=set()
    for f in range(1,frames+1):
        o=(c/'dumps'/f'{f:04}.oam').read_bytes();q=(c/'dumps'/f'{f:04}.ppu').read_bytes()
        sprites=[tuple(o[i:i+4])for i in range(0,256,4)]
        active=[s for s in sprites if s[0]<239]
        palette='FF'+q[0x3f15:0x3f18].hex().upper()
        boss=[s for s in active if 0xbf<=s[1]<=0xf0 and s[2]&3==1]
        if boss:
            boss_counts.append((f,len(boss)))
            palette_examples.setdefault(palette,dict(case=case,memory_frame=f))
        for y,t,attr,x in active:
            if t in [0xf1,0xf2,0xf3,0xf4] and attr&3==0:projectiles.add(t)
        for pose in poses:
            for y,t,attr,x in boss:
                ax,ay,at=pose['tiles'][0]
                if t!=at:continue
                flip=bool(attr&0x40)
                dx=lambda px:pose['size'][0]-8-px if flip else px
                ox,oy=x-dx(ax),y-ay
                if all((oy+py,pt,attr,ox+dx(px))in sprites for px,py,pt in pose['tiles']):
                    key=pose['name']+'_'+('left' if flip else 'right')
                    observed.add(key);examples.setdefault(key,dict(case=case,memory_frame=f))
        if any(t==0x78 and attr&3==2 for y,t,attr,x in active):pickup_frames.append(f)
        if (q[0x216d],q[0x21cc],q[0x21cf],q[0x21d3])==(0x26,0x21,0x3b,0x23):card_frames.append(f)
        if (q[0x214c],q[0x214d],q[0x2152])==(0x34,0x35,0x13):stage2_frames.append(f)
    r['boss_poses']=sorted(observed)
    if route['state']==3:
        assert boss_counts[0]==(1,36) and boss_counts[-1]==(300,1),boss_counts[-3:]
        assert set(n for _,n in boss_counts)==set(range(1,37))
        r['death_disappearance']={'initial_tiles':36,'final_tile_frame':300,'all_native_tile_counts_observed':True}
    if case=='pickup':
        assert pickup_frames and card_frames and stage2_frames
        assert max(pickup_frames)<min(card_frames)<min(stage2_frames)
        r.update(last_pickup_sprite_frame=max(pickup_frames),spell_message_first_frame=min(card_frames),stage2_card_first_frame=min(stage2_frames))
        # The stage-name/lives card is already approved artwork and stays exact.
        stable=[f for f in stage2_frames if f>min(stage2_frames)+4 and f<max(stage2_frames)-4]
        assert stable and all((b/'frames'/f'{f:04}.png').read_bytes()==(c/'frames'/f'{f:04}.png').read_bytes()for f in stable)
        r['unchanged_stage2_card_screenshots']=len(stable)
    if case in ['chamber_floor','platform_edge','platform_left']:
        assert pickup_frames and not card_frames and not stage2_frames
        r['pickup_left_uncollected']=True
    report['cases'][case]=r
required={pose['name']+'_'+direction for pose in poses for direction in ['left','right']}
assert required<=examples.keys(),sorted(required-examples.keys())
assert {'FF1C0B36','FF102030'}<=palette_examples.keys()
assert projectiles=={0xf1,0xf2,0xf3,0xf4}
assert sorted(expected.keys()-old.keys())==['Blizzard_Acquired.png','Boss_Hall_Flash.png','Boss_Tiles_2x.png']
assert sorted(k for k in old if old[k]!=expected[k])==['README.txt','hires.txt']
report.update(boss_pose_examples=examples,boss_palette_examples=palette_examples,projectile_tiles=[f'{t:02X}'for t in sorted(projectiles)],
              total_frames_per_build=sum(r['frames']for r in routes.values()),capture_interval_frames=1,
              unchanged_approved_runtime_files=73,pack_files=len(expected))
out=Path(a.out);out.parent.mkdir(parents=True,exist_ok=True);out.write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({k:v for k,v in report.items()if k!='cases'},indent=2))
