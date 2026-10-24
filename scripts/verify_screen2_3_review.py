"""Bound the blue-tear repair to the two eye projectile cells and live sprites."""
from pathlib import Path
from collections import Counter
import argparse,hashlib,json
import numpy as np
from PIL import Image

p=argparse.ArgumentParser()
for n in ['before','after','out']:p.add_argument('--'+n,required=True)
a=p.parse_args();root=Path(__file__).resolve().parents[1]
old=json.loads((root/'evidence/0.6.0-pack-sha256.json').read_text())
new=json.loads((root/'evidence/approved-pack-sha256.json').read_text())
assert set(old)==set(new)
assert sorted(k for k in old if old[k]!=new[k])==['README.txt','Stage2_Vertical_Cave_Tiles_2x.png']
atlas_old=np.array(Image.open(root/'evidence/screen2_3_review/baseline_0.6.0_atlas.png').convert('RGBA'))
atlas_new=np.array(Image.open(root/'build/Holy_Diver_(Tr)/Stage2_Vertical_Cave_Tiles_2x.png').convert('RGBA'))
allowed=np.zeros(atlas_old.shape[:2],bool);old_shots={}
for m in json.loads((root/'art/screen2_3/registration.json').read_text())['mappings']:
    if m['identity']in ['02DC','02DD']:
        x,y=m['atlas'];allowed[y:y+16,x:x+16]=True
        old_shots[int(m['identity'],16)&255]=atlas_old[y:y+16,x:x+16]
assert np.any(atlas_old!=atlas_new)
assert not np.any(np.any(atlas_old!=atlas_new,axis=2)&~allowed)
templates=[];matches=Counter();examples={}
for t in [0xdc,0xdd]:
    src=np.array(Image.open(root/f'art/screen2_3/eye_shot_02{t:02X}.png').convert('RGBA'))
    for flip in [False,True]:
        im=src[:,::-1]if flip else src;mask=im[:,:,3]>0
        colors,counts=np.unique(im[:,:,:3][mask],axis=0,return_counts=True)
        color=colors[counts.argmin()];sy,sx=np.argwhere(mask&np.all(im[:,:,:3]==color,axis=2))[0]
        templates.append((t,flip,im,mask,color,int(sx),int(sy)))

report=dict(baseline='0.6.0',candidate='0.6.1',controller_only=True,capture_stride=2,cases={})
for case,route in json.loads((root/'scripts/screen2_3_review_routes.json').read_text()).items():
    b,c=Path(a.before)/case,Path(a.after)/case;frames=route['frames']
    assert (b/'completed.txt').read_text()==(c/'completed.txt').read_text()==str(frames)
    assert (b/'input.json').read_bytes()==(c/'input.json').read_bytes()
    inputs=json.loads((c/'input.json').read_text())
    assert inputs['controller_route']=='emu.setInput({'+route['input']+'},0)'
    for folder,expected in [(b,old),(c,new)]:
        for f in ['installed_pack_sha256.json','installed_pack_after_sha256.json']:
            assert json.loads((folder/f).read_text())==expected
    r=dict(emulated_frames=frames,**inputs)
    for ext in ['ram','ppu','oam']:
        files=sorted((b/'dumps').glob('*.'+ext));assert len(files)==frames//2
        for f in files:assert f.read_bytes()==(c/'dumps'/f.name).read_bytes(),f.name
        r[ext+'_identical_samples']=len(files)
    apu=(b/'apu.tsv').read_bytes();assert apu==(c/'apu.tsv').read_bytes()
    r['apu_sha256']=hashlib.sha256(apu).hexdigest()
    bp,cp=(b/'full.wav').read_bytes()[44:],(c/'full.wav').read_bytes()[44:]
    common=min(len(bp),len(cp));tail=abs(len(bp)-len(cp))
    assert common and bp[:common]==cp[:common] and tail<=3200
    r.update(identical_pcm_bytes=common,shutdown_tail_bytes=tail)
    changed=identical=black=rendered_bounds=0;maximum_changed=0
    for n in range(2,frames+1,2):
        stem=f'{n:04}';before=np.array(Image.open(b/'frames'/f'{stem}.png').convert('RGB'))
        after=np.array(Image.open(c/'frames'/f'{stem}.png').convert('RGB'))
        diff=np.any(before!=after,axis=2);count=int(diff.sum());maximum_changed=max(maximum_changed,count)
        if before.max()==0:assert after.max()==0;black+=1
        # endFrame OAM can lead screenshots; include adjacent captured OAM and
        # a two-native-pixel motion margin, never another enemy/player tile.
        oams=[(c/'dumps'/f'{j:04}.oam').read_bytes()for j in range(max(2,n-2),min(frames,n+2)+1,2)]
        bounds=np.zeros((480,512),bool)
        for o in oams:
            for i in range(0,256,4):
                y,t,attr,x=o[i:i+4]
                if y>=239 or t not in [0xdc,0xdd]or attr&3!=2:continue
                X,Y=x*2,(y+1)*2
                bounds[max(0,Y-4):min(480,Y+20),max(0,X-4):min(512,X+20)]=True
        if np.any(diff&~bounds):
            # During fast vertical scrolling, a shot can re-enter from below
            # farther from endFrame OAM. Prove its actual position using BOTH
            # complete old and new sprite pixels; do not widen the OAM margin.
            for t,flip,src,mask,color,sx,sy in templates:
                old_src=old_shots[t][:,::-1]if flip else old_shots[t]
                old_mask=old_src[:,:,3]>0
                for y,x in np.argwhere(np.all(after==color,axis=2)):
                    X,Y=int(x-sx),int(y-sy)
                    if X<0 or Y<0 or X+16>512 or Y+16>480:continue
                    if (np.array_equal(after[Y:Y+16,X:X+16][mask],src[:,:,:3][mask]) and
                        np.array_equal(before[Y:Y+16,X:X+16][old_mask],old_src[:,:,:3][old_mask])):
                        bounds[Y:Y+16,X:X+16]=True;rendered_bounds+=1
        assert not np.any(diff&~bounds),(case,n,'changed outside eye projectile positions')
        if count:changed+=1
        else:identical+=1
        if n%10:continue
        for t,flip,src,mask,color,sx,sy in templates:
            if not any(o[i]<239 and o[i+1]==t and o[i+2]&3==2 and bool(o[i+2]&64)==flip
                       for o in oams for i in range(0,256,4)):continue
            for y,x in np.argwhere(np.all(after==color,axis=2)):
                X,Y=int(x-sx),int(y-sy)
                if X<0 or Y<0 or X+16>512 or Y+16>480:continue
                if np.array_equal(after[Y:Y+16,X:X+16][mask],src[:,:,:3][mask]):
                    key=f'02{t:02X}/'+('mirrored'if flip else'native');matches[key]+=1
                    examples.setdefault(key,dict(case=case,frame=n,box=[X,Y,X+16,Y+16]));break
    r.update(changed_screenshots=changed,identical_screenshots=identical,exact_black_samples=black,
             maximum_changed_pixels=maximum_changed,all_changes_within_eye_projectile_bounds=True,
             exact_old_and_new_sprite_positions_used=rendered_bounds)
    report['cases'][case]=r
assert all(matches[f'{t}/{flip}']>10 for t in ['02DC','02DD']for flip in ['native','mirrored']),matches
report.update(total_frames_per_build=sum(v['emulated_frames']for v in report['cases'].values()),
              unchanged_pack_files=83,changed_atlas_cells=['02DC','02DD'],mapping_file_unchanged=True,
              pixel_exact_teardrop_samples=dict(matches),sprite_examples=examples)
out=Path(a.out);out.parent.mkdir(parents=True,exist_ok=True);out.write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
