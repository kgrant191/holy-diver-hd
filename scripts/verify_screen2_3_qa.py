"""Verify paired vertical-cave replays and actual rendered sprites/background."""
from pathlib import Path
from collections import Counter
import argparse, hashlib, json
import numpy as np
from PIL import Image

p=argparse.ArgumentParser()
for n in ['before','after','out']:p.add_argument('--'+n,required=True)
a=p.parse_args();root=Path(__file__).resolve().parents[1]
old=json.loads((root/'evidence/0.5.1-pack-sha256.json').read_text())
new=json.loads((root/'evidence/approved-pack-sha256.json').read_text())
routes=json.loads((root/'scripts/screen2_3_routes.json').read_text())
bg=np.array(Image.open(root/'build/Holy_Diver_(Tr)/Stage2_Cave_Background.png').convert('RGB'))[:,:512]
report=dict(baseline='0.5.1',candidate=(root/'VERSION').read_text().strip(),controller_only=True,capture_stride=2,cases={})
observed=set();palettes=Counter();matches=Counter();examples={};max_scroll=0
sources=[('eye',root/'art/screen2_3/eye_registered.png',0xd8,1),
         ('shot_dc',root/'art/screen2_3/eye_shot_02DC.png',0xdc,2),
         ('shot_dd',root/'art/screen2_3/eye_shot_02DD.png',0xdd,2)]
for i,pose in enumerate(json.loads((root/'art/screen1_3/ghoul_poses.json').read_text())):
    path=root/(f'art/review_fixes/ghoul_standing_{i}.png' if i<2 else f'art/screen1_3/ghoul_pose_{i}.png')
    sources.append((f'ghoul_{i}',path,pose['tiles'][0][2]-6,0))
templates=[]
for name,path,t,pal in sources:
    im=np.array(Image.open(path).convert('RGBA'))
    for flip in [False,True]:
        src=im[:,::-1] if flip else im;mask=src[:,:,3]>0
        colors,counts=np.unique(src[:,:,:3][mask],axis=0,return_counts=True)
        color=colors[counts.argmin()];sy,sx=np.argwhere(mask&np.all(src[:,:,:3]==color,axis=2))[0]
        templates.append((name+('/mirrored'if flip else'/native'),src,mask,color,int(sx),int(sy),t,pal,flip))

def inspect_sprites(rgb,oams,case,n):
    for key,src,mask,color,sx,sy,t,pal,flip in templates:
        if not any(o[i]<239 and o[i+1]==t and o[i+2]&3==pal and bool(o[i+2]&64)==flip
                   for o in oams for i in range(0,256,4)):continue
        h,w=src.shape[:2]
        for y,x in np.argwhere(np.all(rgb==color,axis=2)):
            X,Y=int(x-sx),int(y-sy)
            if X<0 or Y<0 or X+w>512 or Y+h>480:continue
            if np.array_equal(rgb[Y:Y+h,X:X+w][mask],src[:,:,:3][mask]):
                matches[key]+=1;examples.setdefault(key,dict(case=case,frame=n,box=[X,Y,X+w,Y+h]));break

for case,route in routes.items():
    b,c=Path(a.before)/case,Path(a.after)/case;frames=route['frames']
    assert (b/'completed.txt').read_text()==(c/'completed.txt').read_text()==str(frames)
    assert (b/'input.json').read_bytes()==(c/'input.json').read_bytes()
    inputs=json.loads((c/'input.json').read_text())
    assert inputs['state_sha256']=='a84d2f19c107be53b9d76e78f8095ae9cf7861badbf8052555e0879dd5749df3'
    assert inputs['controller_route']==route.get('input_code','emu.setInput({'+route.get('input','')+'},0)')
    for folder,expected in [(b,old),(c,new)]:
        for f in ['installed_pack_sha256.json','installed_pack_after_sha256.json']:
            assert json.loads((folder/f).read_text())==expected,(case,f)
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
    rooms=Counter();black=outside=menu=exact=changed=backdrop=0;min_backdrop=512*480
    for n in range(2,frames+1,2):
        stem=f'{n:04}';ram=(c/'dumps'/f'{stem}.ram').read_bytes()
        ppu=(c/'dumps'/f'{stem}.ppu').read_bytes();oam=(c/'dumps'/f'{stem}.oam').read_bytes()
        rooms[f'{ram[0x72]:02X}/'+ram[0x78:0x7a].hex().upper()]+=1
        before=np.array(Image.open(b/'frames'/f'{stem}.png').convert('RGB'))
        after=np.array(Image.open(c/'frames'/f'{stem}.png').convert('RGB'))
        equal=np.array_equal(before,after);exact+=equal;changed+=not equal
        if before.max()==0:assert after.max()==0,(case,n,'black frame');black+=1
        if case=='menu' and 40<n<175:assert equal,(case,n,'pause menu');menu+=1
        # CPU room pointers change before the outgoing picture is replaced.
        # The rendered next-room palette marks completed arrival instead.
        neighbor_ppu=[(c/'dumps'/f'{j:04}.ppu').read_bytes() for j in range(max(2,n-2),min(frames,n+2)+1,2)]
        if all(v[0x3f08:0x3f0c]==bytes.fromhex('0f061828')for v in neighbor_ppu):
            assert equal,(case,n,'next-room arrival');outside+=1
        if ram[0x72]==4 and ram[0x78:0x7a]==bytes.fromhex('f98b'):
            scroll=int.from_bytes(ram[0x60:0x62],'little')
            if scroll<=512:max_scroll=max(max_scroll,scroll)
            palettes[ppu[0x3f04:0x3f08].hex().upper()]+=1
            for i in range(0,256,4):
                y,t,attr,x=oam[i:i+4]
                if y<239 and 0xd8<=t<=0xdd:observed.add((t,bool(attr&64)))
        # Compare source RGB only while the original purple wall is rendered
        # in color. Death briefly applies a hardware grayscale/emphasis filter
        # without changing palette RAM, then disables scenery but keeps sprites.
        # A palette-RAM-only test would incorrectly label those as missing art.
        colored_wall_pixels=int(np.all(before==[92,0,126],axis=2).sum())
        if ppu[0x3f08:0x3f0c]==bytes.fromhex('0f041625') and colored_wall_pixels>1000:
            pixels=int(np.all(after==bg,axis=2).sum())
            assert pixels>10000,(case,n,'missing cave panorama',pixels)
            min_backdrop=min(min_backdrop,pixels);backdrop+=1
        if n%20==0:
            nearby=[(c/'dumps'/f'{j:04}.oam').read_bytes()for j in range(max(2,n-2),min(frames,n+2)+1,2)]
            inspect_sprites(after,nearby,case,n)
    r.update(exact_black_samples=black,exact_next_room_samples=outside,exact_menu_samples=menu,
             exact_screenshots=exact,changed_screenshots=changed,rooms=dict(rooms),
             verified_backdrop_samples=backdrop,minimum_exact_backdrop_pixels=min_backdrop if backdrop else 0)
    report['cases'][case]=r

assert all(any(t==v for t,flip in observed)for v in range(0xd8,0xde)),observed
assert matches['eye/native']>20,matches
assert all(matches[f'{shot}/{flip}']>0 for shot in ['shot_dc','shot_dd']for flip in ['native','mirrored']),matches
assert any(k.startswith('ghoul_')and k.endswith('/native')for k in matches)
assert any(k.startswith('ghoul_')and k.endswith('/mirrored')for k in matches)
assert {'0F161606','0F060616','0F122131'}<=set(palettes),palettes
assert max_scroll==512 and report['cases']['descent']['exact_next_room_samples']>100
patterns=json.loads((root/'art/screen2_2/shared_chr.json').read_text())['ghoul_exact_copies']
ppu=(Path(a.after)/'combat_respawn/dumps/1000.ppu').read_bytes()
for entry in patterns:
    offset=(int(entry['target'],16)&255)*16
    assert hashlib.sha256(ppu[offset:offset+16]).hexdigest()==entry['native_pattern_sha256']
assert sorted(k for k in old if old[k]!=new[k])==['README.txt','hires.txt']
assert sorted(set(new)-set(old))==['Stage2_Vertical_Cave_Tiles_2x.png']
report.update(total_frames_per_build=sum(v['frames']for v in routes.values()),
              native_samples_per_type=sum(v['ram_identical_samples']for v in report['cases'].values()),
              exact_black_samples=sum(v['exact_black_samples']for v in report['cases'].values()),
              exact_next_room_samples=sum(v['exact_next_room_samples']for v in report['cases'].values()),
              verified_backdrop_samples=sum(v['verified_backdrop_samples']for v in report['cases'].values()),
              maximum_verified_vertical_scroll=max_scroll,room_exit_reached=True,
              coverage_limit='Full vertical room and next-room arrival; next-room scenery remains future work.',
              shared_native_chr_hashes_verified=len(patterns),unchanged_prior_pack_files=82,pack_files=85,
              observed_enemy_tiles_and_flips=[f'{t+0x200:04X}/'+('mirrored'if flip else'native')for t,flip in sorted(observed)],
              lava_palette_samples=dict(palettes),pixel_exact_complete_sprite_samples=dict(matches),sprite_examples=examples)
out=Path(a.out);out.parent.mkdir(parents=True,exist_ok=True);out.write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({k:v for k,v in report.items()if k not in ['cases','sprite_examples','observed_enemy_tiles_and_flips']},indent=2))
