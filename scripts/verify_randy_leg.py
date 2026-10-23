"""Bound the connected standing-leg repair to its artwork and actual native footprint."""
from pathlib import Path
import argparse
import hashlib
import json
import numpy as np
from PIL import Image

p=argparse.ArgumentParser()
for name in ['before','after','old-pack','out']:p.add_argument('--'+name,required=True)
a=p.parse_args();root=Path(__file__).resolve().parents[1]
old_pack=Path(a.old_pack);pack=root/'build/Holy_Diver_(Tr)'
old=json.loads((root/'evidence/0.3.3-pack-sha256.json').read_text())
new=json.loads((root/'evidence/approved-pack-sha256.json').read_text())
routes=json.loads((root/'scripts/randy_leg_routes.json').read_text())
hashes=lambda folder:{f.name:hashlib.sha256(f.read_bytes()).hexdigest() for f in folder.iterdir() if f.is_file()}
assert hashes(old_pack)==old and hashes(pack)==new
assert old.keys()==new.keys() and len(new)==79
changed=sorted(k for k in old if old[k]!=new[k])
assert changed==['Boss_Tiles_2x.png','README.txt','Randy_Entrance_2x.png','Randy_Equipped_2x.png','hires.txt']
# Existing conditions remain exact, though their order within the definitions
# section can change when the builder first encounters the new pose probe.
old_text=(old_pack/'hires.txt').read_text();new_text=(pack/'hires.txt').read_text()
old_defs={line.split('>',1)[1].split(',')[0]:line for line in old_text.splitlines() if line.startswith('<condition>')}
new_defs={line.split('>',1)[1].split(',')[0]:line for line in new_text.splitlines() if line.startswith('<condition>')}
assert all(new_defs.get(k)==v for k,v in old_defs.items())
added=set(new_defs)-set(old_defs);assert len(added)==14
assert all('standingLeg' in name for name in added)
prior=new_text.replace('standingLegNormal','randySig8').replace('standingLegTwin','randyEquippedSig8')
strip=lambda text:'\n'.join(line for line in text.splitlines() if not line.startswith('<condition>') and 'STANDING_LEG CONDITIONS' not in line)
assert strip(prior)==strip(old_text),'Tile priority or unrelated mapping changed'
assert sum(x!=y for x,y in zip([v for v in old_text.splitlines() if '<tile>' in v],[v for v in new_text.splitlines() if '<tile>' in v]))==14
atlases={};asset_changes={}
for mode,name in enumerate(['Randy_Entrance_2x.png','Randy_Equipped_2x.png']):
    b=np.array(Image.open(old_pack/name).convert('RGBA'));c=np.array(Image.open(pack/name).convert('RGBA'))
    allowed=np.zeros(b.shape[:2],bool);allowed[32:64,16:32]=True
    diff=np.any(b!=c,axis=2);assert diff.any() and not np.any(diff&~allowed)
    patch=np.array(Image.open(root/f'art/randy_foot/boot_{mode}.png').convert('RGBA'))
    assert np.array_equal(c[32:64,16:32],patch)
    # The rejected repair jumps sideways by six pixels below the knee. The
    # continuous piece must have a gradual outer contour and a connected join.
    edges=lambda im:np.array([np.where(row)[0].max() for row in im[32:58,16:32,3]>0])
    assert np.max(np.abs(np.diff(edges(b))))>2,'Baseline must reproduce the broken knee'
    assert np.max(np.abs(np.diff(edges(c))))<=2,'Abrupt knee/shin contour break'
    mask=c[31:64,16:32,3]>0
    assert all(np.any(mask[y]&mask[y+1]) for y in range(len(mask)-1))
    assert np.any(patch[27:31,14:,3]),'Complete toe missing' 
    atlases['300036' if mode==0 else '221136']=c
    asset_changes[name]=int(diff.sum())
b=np.array(Image.open(old_pack/'Boss_Tiles_2x.png').convert('RGBA'))
c=np.array(Image.open(pack/'Boss_Tiles_2x.png').convert('RGBA'))
assert np.array_equal(b[:,:,:3],c[:,:,:3]),'Monochrome RGB changed'
allowed=np.zeros(b.shape[:2],bool)
for x,y,sx,sy in [(368,112,16,32),(400,112,16,48),(128,176,16,32),(160,176,16,48),
                  (400,224,16,32),(432,224,16,48),(192,288,16,32),(224,288,16,48)]:
    assert np.array_equal(c[y:y+16,x:x+16,3],atlases['300036'][sy:sy+16,sx:sx+16,3])
    allowed[y:y+16,x:x+16]=True
diff=np.any(b!=c,axis=2);assert diff.any() and not np.any(diff&~allowed)
asset_changes['Boss_Tiles_2x.png']=int(diff.sum())

report={'baseline':'0.3.3','candidate':'0.3.4','emulator':'MesenCE 2.2.1','ram_writes':False,
        'pack_files':79,'changed_files':changed,'unchanged_files':74,'new_conditions':14,'updated_standing_tile_scopes':14,'other_mappings_identical':True,'knee_contour_regression_checked':True,
        'changed_atlas_pixels':asset_changes,'changed_pose':0,'changed_pose_rectangle':[16,32,32,64],
        'other_pose_pixels_identical':True,'cases':{}}
for case,route in routes.items():
    before,after=Path(a.before)/case,Path(a.after)/case;frames=route['frames']
    assert (before/'completed.txt').read_text()==(after/'completed.txt').read_text()==str(frames)
    assert (before/'input.json').read_bytes()==(after/'input.json').read_bytes()
    for folder,expected in [(before,old),(after,new)]:
        for name in ['installed_pack_sha256.json','installed_pack_after_sha256.json']:
            assert json.loads((folder/name).read_text())==expected
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
    changed_frames=[];empty=[];directions=set();full_leg_frames=[];crouch_frames=[];other_pose_frames=[]
    for f in range(1,frames+1):
        name=f'{f:04}.png'
        if not (before/'frames'/name).stat().st_size or not (after/'frames'/name).stat().st_size:
            assert f==1 and (before/'frames'/name).read_bytes()==(after/'frames'/name).read_bytes()
            empty.append(f);continue
        bi=np.array(Image.open(before/'frames'/name).convert('RGB'));ci=np.array(Image.open(after/'frames'/name).convert('RGB'))
        diff=np.any(bi!=ci,axis=2);prev=f'{f-1:04}'
        q=(after/'dumps'/(prev+'.ppu')).read_bytes();o=(after/'dumps'/(prev+'.oam')).read_bytes()
        player=[tuple(o[i:i+4]) for i in range(0,256,4) if o[i]<239 and o[i+1]<0x60 and o[i+2]&3==3]
        ids=sorted(v[1] for v in player)
        # At the left-room exit the outer hand tile 05 is offscreen for one
        # frame. The other eight tiles still identify the same standing pose.
        idle=ids in [list(range(1,10)),[1,2,3,4,6,7,8,9]]
        allowed=np.zeros(diff.shape,bool)
        if idle:
            for y,t,attr,x in player:
                if t not in [7,9]:continue
                assert not attr&0x80
                x0=x*2;y0=(y+1)*2
                allowed[y0:min(480,(y+9)*2),x0:min(512,x0+16)]=True
            if diff.any():
                directions.update(attr&0x40 for y,t,attr,x in player)
                pal=q[0x3f1d:0x3f20].hex()
                if pal in atlases:
                    valid=True
                    for y,t,attr,x in player:
                        if t not in [7,9]:continue
                        source=atlases[pal][32 if t==7 else 48:48 if t==7 else 64,16:32]
                        if attr&0x40:source=source[:,::-1]
                        mask=source[:,:,3]>0
                        crop=ci[(y+1)*2:(y+9)*2,x*2:(x+8)*2]
                        if crop.shape!=source[:,:,:3].shape or not np.array_equal(crop[mask],source[:,:,:3][mask]):valid=False
                    if valid:full_leg_frames.append(f)
        elif player:
            other_pose_frames.append(f)
            if any(t in [0x2f,0x30,0x31,0x32,0x33,0x34,0x35] for y,t,attr,x in player):crouch_frames.append(f)
        assert not np.any(diff&~allowed),(case,f,'change outside standing forward leg')
        if diff.any():changed_frames.append(f)
    if case in ['normal','twin']:
        assert directions=={0,64} and len(full_leg_frames)>100
        assert len(crouch_frames)>30 and len(other_pose_frames)>100
    if case.startswith('clear_'):assert directions=={0,64} and len(full_leg_frames)>50
    if case in ['menu_blizzard','reverse_blizzard']:assert 616 in full_leg_frames,'Offscreen hand must not break leg mapping'
    r.update(changed_screenshots=len(changed_frames),unchanged_screenshots=frames-len(changed_frames)-len(empty),
             empty_load_captures=empty,changed_frame_range=[min(changed_frames),max(changed_frames)] if changed_frames else [],
             observed_repaired_flip_bits=sorted(directions),pixel_exact_leg_frames=len(full_leg_frames),
             pixel_exact_leg_examples=full_leg_frames[:10],unchanged_crouch_frames=len(crouch_frames),
             unchanged_other_pose_frames=len(other_pose_frames),changes_confined_to='standing forward leg')
    report['cases'][case]=r
report['total_frames_per_build']=sum(v['frames'] for v in routes.values())
report['native_memory_and_audio_preserved']=True
out=Path(a.out);out.parent.mkdir(parents=True,exist_ok=True);out.write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({k:v for k,v in report.items() if k!='cases'},indent=2))
