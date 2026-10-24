"""Compare cave replays, native behavior, prior art, and actual sprite pixels."""
from pathlib import Path
import argparse, hashlib, json
from collections import Counter
import numpy as np
from PIL import Image

p=argparse.ArgumentParser()
for n in ['before','after','approach-before','approach-after','out']:
    p.add_argument('--'+n,required=True)
a=p.parse_args();root=Path(__file__).resolve().parents[1]
old=json.loads((root/'evidence/0.4.1-pack-sha256.json').read_text())
new=json.loads((root/'evidence/approved-pack-sha256.json').read_text())
routes=json.loads((root/'scripts/screen2_2_routes.json').read_text())
routes.update(json.loads((root/'scripts/screen2_2_approach_routes.json').read_text()))
report=dict(baseline='0.4.1',candidate=(root/'VERSION').read_text().strip(),controller_only=True,capture_stride=2,cases={})
observed=set();palettes=Counter();matches=Counter();examples={};max_scroll=0
poses=[]
for i,pose in enumerate(json.loads((root/'art/screen1_3/ghoul_poses.json').read_text())):
    path=root/(f'art/review_fixes/ghoul_standing_{i}.png' if i<2 else f'art/screen1_3/ghoul_pose_{i}.png')
    poses.append((f'ghoul_{i}',np.array(Image.open(path).convert('RGBA')),[(x,y,t-6) for x,y,t in pose['tiles']],1))
poses += [('bat_folded',np.array(Image.open(root/'art/screen2_2/bat_folded.png')),[(x*8,y*8,0xb0+y*2+x)for y in range(3)for x in range(2)],0),
          ('bat_open',np.array(Image.open(root/'art/screen2_2/bat_open.png')),[(x*8,y*8,t)for x,y,t in [(0,0,0xa6),(1,0,0xa7),(2,0,0xa8),(3,0,0xa9),(0,1,0xaa),(1,1,0xab),(2,1,0xac),(3,1,0xad),(1,2,0xae),(2,2,0xaf)]],0)]

def actual_sprite_matches(rgb, oams, case, frame):
    """Locate a complete registered opaque silhouette near native OAM anchors.

    endFrame OAM can describe the next frame. Adjacent two-frame samples and
    a one-native-pixel offset cover that timing; screenshots remain the proof.
    """
    for name,source,layout,pal in poses:
        h,w=source.shape[:2];dx,dy,t=layout[0]
        found=set()
        if name.startswith('bat_'):
            # The fast diving pose can move farther than one pixel between
            # rendered screenshots and endFrame OAM. Locate its exact source
            # colors in the actual image rather than enlarging a timing guess.
            mask=source[:,:,3]>0
            colors,counts=np.unique(source[:,:,:3][mask],axis=0,return_counts=True)
            color=colors[counts.argmin()]
            sy,sx=np.argwhere(mask & np.all(source[:,:,:3]==color,axis=2))[0]
            for y,x in np.argwhere(np.all(rgb==color,axis=2)):
                X,Y=int(x-sx),int(y-sy)
                if X<0 or Y<0 or X+w>512 or Y+h>480:continue
                if np.array_equal(rgb[Y:Y+h,X:X+w][mask],source[:,:,:3][mask]):
                    key=name+'/native';found.add(key)
                    examples.setdefault(key,dict(case=case,frame=frame,box=[X,Y,X+w,Y+h]))
                    break
            matches.update(found)
            continue
        for oam in oams:
            for i in range(0,256,4):
                y,ot,attr,x=oam[i:i+4]
                if y>=239 or ot!=t or attr&3!=pal or attr&128:continue
                flip=bool(attr&64);key=name+('/mirrored' if flip else '/native')
                if key in found:continue
                sprite=source[:,::-1] if flip else source
                xx=2*x-(w-16-2*dx if flip else 2*dx);yy=2*(y+1-dy)
                mask=sprite[:,:,3]>0
                for sy in [0,-2,2]:
                    for sx in [0,-2,2]:
                        X,Y=xx+sx,yy+sy
                        if X<0 or Y<0 or X+w>512 or Y+h>480:continue
                        if np.array_equal(rgb[Y:Y+h,X:X+w][mask],sprite[:,:,:3][mask]):
                            found.add(key);examples.setdefault(key,dict(case=case,frame=frame,box=[X,Y,X+w,Y+h]))
        matches.update(found)

for case,route in routes.items():
    b,c=(Path(a.approach_before)/case,Path(a.approach_after)/case) if case=='approach' else (Path(a.before)/case,Path(a.after)/case)
    frames=route['frames'];assert (b/'completed.txt').read_text()==(c/'completed.txt').read_text()==str(frames)
    assert (b/'input.json').read_bytes()==(c/'input.json').read_bytes()
    inputs=json.loads((c/'input.json').read_text())
    assert inputs['controller_route']==route.get('input_code','emu.setInput({'+route.get('input','')+'},0)')
    for folder,expected in [(b,old),(c,new)]:
        for file in ['installed_pack_sha256.json','installed_pack_after_sha256.json']:
            assert json.loads((folder/file).read_text())==expected,(case,file)
    r=dict(emulated_frames=frames,**inputs)
    for ext in ['ram','ppu','oam']:
        fs=sorted((b/'dumps').glob('*.'+ext));assert len(fs)==frames//2
        for f in fs:assert f.read_bytes()==(c/'dumps'/f.name).read_bytes(),(case,f.name)
        r[ext+'_identical_samples']=len(fs)
    apu=(b/'apu.tsv').read_bytes();assert apu==(c/'apu.tsv').read_bytes(),(case,'APU')
    r['apu_sha256']=hashlib.sha256(apu).hexdigest()
    bp,cp=(b/'full.wav').read_bytes()[44:],(c/'full.wav').read_bytes()[44:]
    common=min(len(bp),len(cp));tail=abs(len(bp)-len(cp))
    assert common and bp[:common]==cp[:common],(case,'PCM');assert tail<=3200,(case,'tail',tail)
    r.update(identical_pcm_bytes=common,shutdown_tail_bytes=tail)
    rooms=Counter();black=outside=menu=exact=changed=0
    for n in range(2,frames+1,2):
        stem=f'{n:04}'
        ram=(c/'dumps'/f'{stem}.ram').read_bytes();ppu=(c/'dumps'/f'{stem}.ppu').read_bytes();oam=(c/'dumps'/f'{stem}.oam').read_bytes()
        room=ram[0x72];rooms[f'{room:02X}']+=1
        before=np.array(Image.open(b/'frames'/f'{stem}.png').convert('RGB'))
        after=np.array(Image.open(c/'frames'/f'{stem}.png').convert('RGB'))
        equal=np.array_equal(before,after);exact+=equal;changed+=not equal
        if before.max()==0:assert after.max()==0,(case,n,'black frame');black+=1
        neighbors=[(c/'dumps'/f'{j:04}.ram').read_bytes()[0x72] for j in range(max(2,n-4),min(frames,n+4)+1,2)]
        if all(v!=0x10 for v in neighbors):assert equal,(case,n,'outside cave');outside+=1
        if case=='menu' and 40<n<175:assert equal,(case,n,'pause menu');menu+=1
        if room==0x10:
            scroll=int.from_bytes(ram[96:98],'little')
            # The initial load retains the previous room's 1280 scroll until
            # this camera starts moving. Do not count that stale value.
            if scroll<1200:max_scroll=max(max_scroll,scroll)
            palettes[ppu[0x3f04:0x3f08].hex().upper()]+=1
            for i in range(0,256,4):
                y,t,attr,x=oam[i:i+4]
                if y<239 and ((0x8e<=t<=0xa5 and attr&3==1)or(0xa6<=t<=0xb5 and attr&3==0)or(t==0xb6 and attr&3==2)):
                    observed.add((t,bool(attr&64)))
            nearby=[(c/'dumps'/f'{j:04}.oam').read_bytes() for j in range(max(2,n-2),min(frames,n+2)+1,2)]
            actual_sprite_matches(after,nearby,case,n)
    r.update(exact_black_samples=black,exact_outside_cave_samples=outside,exact_menu_samples=menu,
             exact_screenshots=exact,changed_screenshots=changed,rooms=dict(rooms))
    report['cases'][case]=r

# All new body/shot identities must actually appear. Shared ghoul coverage is
# reported individually instead of inventing a native pose/direction pairing.
assert all(any(t==v for t,flip in observed)for v in range(0xa6,0xb7)),observed
assert all(matches[k]>10 for k in ['bat_folded/native','bat_open/native']),matches
assert any(k.startswith('ghoul_')and k.endswith('/native')for k in matches)
assert any(k.startswith('ghoul_')and k.endswith('/mirrored')for k in matches)
assert {'0F161606','0F060616','0F122131'}<=set(palettes),palettes
patterns=json.loads((root/'art/screen2_2/shared_chr.json').read_text())['ghoul_exact_copies']
ppu=(Path(a.after)/'entry_combat/dumps/0020.ppu').read_bytes()
for entry in patterns:
    offset=(int(entry['target'],16)&255)*16
    assert hashlib.sha256(ppu[offset:offset+16]).hexdigest()==entry['native_pattern_sha256']
assert sorted(k for k in old if old[k]!=new[k])==['README.txt','hires.txt']
assert sorted(set(new)-set(old))==['Stage2_Cave_Background.png','Stage2_Cave_Tiles_2x.png']
report.update(total_frames_per_build=sum(v['frames']for v in routes.values()),
              native_samples_per_type=sum(v['ram_identical_samples']for v in report['cases'].values()),
              exact_black_samples=sum(v['exact_black_samples']for v in report['cases'].values()),
              exact_outside_cave_samples=sum(v['exact_outside_cave_samples']for v in report['cases'].values()),
              maximum_verified_scroll=max_scroll,room_exit_reached=False,
              coverage_limit='Supplied entry through the first lava fall and opposite ledge, death/respawn, menus, freeze/thaw; full cave exit not reached.',
              shared_native_chr_hashes_verified=len(patterns),unchanged_prior_pack_files=80,pack_files=84,
              observed_enemy_tiles_and_flips=[f'{t+0x200:04X}/'+('mirrored'if flip else'native')for t,flip in sorted(observed)],
              lava_palette_samples=dict(palettes),pixel_exact_complete_sprite_samples=dict(matches),sprite_examples=examples)
out=Path(a.out);out.parent.mkdir(parents=True,exist_ok=True);out.write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({k:v for k,v in report.items()if k not in ['cases','sprite_examples','observed_enemy_tiles_and_flips']},indent=2))
