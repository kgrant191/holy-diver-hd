"""Compare paired controller replays and inventory the observed native sprites."""
from pathlib import Path
import argparse
import hashlib
import json

p=argparse.ArgumentParser()
for name in ['before','after','out']:
    p.add_argument('--'+name,required=True)
a=p.parse_args()
root=Path(__file__).resolve().parents[1]
routes=json.loads((root/'scripts/screen1_4_routes.json').read_text())
poses=json.loads((root/'art/screen1_3/ghoul_poses.json').read_text())
mapped={(int(m['identity'],16)-256,m['palette']) for m in json.loads((root/'art/screen1_4/registration.json').read_text())['mappings'] if int(m['identity'],16)>=256}
report={'emulator':'MesenCE 2.2.1','ram_writes':False,'cases':{}}
all_ghouls={}
for case,route in routes.items():
    b,c=Path(a.before)/case,Path(a.after)/case
    frames=route['frames']
    assert (b/'completed.txt').read_text()==(c/'completed.txt').read_text()==str(frames)
    assert (b/'input.json').read_bytes()==(c/'input.json').read_bytes()
    r={'emulated_frames':frames,**json.loads((c/'input.json').read_text())}
    before=json.loads((b/'installed_pack_sha256.json').read_text())
    after=json.loads((c/'installed_pack_sha256.json').read_text())
    assert sorted(after.keys()-before.keys())==['Tree_Court_Background.png','Tree_Court_Tiles_2x.png']
    assert sorted(k for k in before if before[k]!=after[k])==['README.txt','hires.txt']
    assert len(before)==73 and len(after)==75
    r.update(unchanged_approved_files=71,added_files=2,changed_files=['README.txt','hires.txt'])
    for ext in ['ram','ppu','oam']:
        files=sorted((b/'dumps').glob('*.'+ext))
        assert len(files)==frames//2
        assert all(f.read_bytes()==(c/'dumps'/f.name).read_bytes() for f in files),(case,ext)
        r[ext+'_identical_samples']=len(files)
    apu=(b/'apu.tsv').read_bytes()
    assert apu==(c/'apu.tsv').read_bytes(),case+' APU mismatch'
    r['apu_sha256']=hashlib.sha256(apu).hexdigest()
    bp,cp=(b/'full.wav').read_bytes()[44:],(c/'full.wav').read_bytes()[44:]
    common=min(len(bp),len(cp))
    assert common and bp[:common]==cp[:common],case+' PCM mismatch'
    assert abs(len(bp)-len(cp))<=3200,case+' truncated audio'
    r.update(identical_pcm_bytes=common,before_pcm_bytes=len(bp),after_pcm_bytes=len(cp))
    observed=set();palettes=set();pickups=[];backgrounds=set()
    for path in sorted((c/'dumps').glob('*.oam')):
        data=path.read_bytes();frame=int(path.stem)
        sprites=[tuple(data[n:n+4]) for n in range(0,256,4)]
        ppu=(c/'dumps'/f'{frame:04}.ppu').read_bytes()
        ram=(c/'dumps'/f'{frame:04}.ram').read_bytes()
        active=ram[0x72]==4 and (ppu[0x3f05],ppu[0x3f0b],ppu[0x3f0f],ppu[0x3f11])==(7,0x3b,0x37,0x37)
        if active:
            for base in [0x2000,0x2800]:
                for yy in range(30):
                    for xx in range(32):
                        t=ppu[base+yy*32+xx]
                        attr=ppu[base+960+yy//4*8+xx//4]
                        pal=(attr>>((yy%4//2)*4+(xx%4//2)*2))&3
                        key=(t,ppu[0x3f00+pal*4:0x3f04+pal*4].hex().upper())
                        assert key in mapped,(case,frame,key)
                        backgrounds.add(key)
        palette='FF'+ppu[0x3f1d:0x3f20].hex().upper()
        if active and any(y<239 and t==0x4e and attr&3==3 for y,t,attr,x in sprites):
            pickups.append(frame);palettes.add(palette)
        for i,pose in enumerate(poses):
            for y,t,attr,x in sprites:
                ax,ay,at=pose['tiles'][0]
                if y>=239 or t!=at or attr&3!=1:continue
                flip=bool(attr&0x40)
                dx=lambda value:pose['size'][0]-8-value if flip else value
                ox,oy=x-dx(ax),y-ay
                if all((oy+py,pt,attr,ox+dx(px)) in sprites for px,py,pt in pose['tiles']):
                    key=f'pose_{i}_'+('right' if flip else 'left')
                    observed.add(key);all_ghouls.setdefault(key,dict(case=case,frame=frame))
    r['ghoul_poses']=sorted(observed)
    r['one_up_palettes']=sorted(palettes)
    r['mapped_background_tile_palette_pairs']=len(backgrounds)
    if case in ['pickup','normal_pickup']:
        start=(c/'dumps/0020.ram').read_bytes()[0x48f]
        end=(c/'dumps'/('0200.ram' if case=='pickup' else '1600.ram')).read_bytes()[0x48f]
        assert (start,end)==(3,4)
        assert pickups and max(pickups)<(160 if case=='pickup' else 1520)
        r.update(lives_before=start,lives_after=end,last_one_up_oam_frame=max(pickups))
        if case=='normal_pickup':assert 'FF300036' in palettes
    if case=='left_transition':
        # endFrame memory can describe the next render. The first fully
        # previous-room screenshot on the four-frame capture cadence is 104.
        images=[f for f in (c/'frames').glob('*.png') if int(f.stem)>=104]
        assert images and all(f.read_bytes()==(b/'frames'/f.name).read_bytes() for f in images)
        r['identical_previous_room_screenshots']=len(images)
    report['cases'][case]=r
assert len(all_ghouls)==12,all_ghouls
report['ghoul_pose_examples']=all_ghouls
report['total_frames_per_build']=sum(r['frames'] for r in routes.values())
report['paired_samples_per_memory_type']=report['total_frames_per_build']//2
out=Path(a.out);out.parent.mkdir(parents=True,exist_ok=True)
out.write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
