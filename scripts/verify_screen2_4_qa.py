"""Check paired controller replays, preserved assets, cave coverage and sprites."""
from pathlib import Path
from collections import Counter
import argparse
import hashlib
import json
import numpy as np
from PIL import Image

p = argparse.ArgumentParser()
for key in ['before','after','out','routes']:
    p.add_argument('--'+key, required=True)
p.add_argument('--state-sha256', required=True)
a = p.parse_args()
root = Path(__file__).resolve().parents[1]
old = json.loads((root/'evidence/0.6.1-pack-sha256.json').read_text())
new = json.loads((root/'evidence/0.7.0-pack-sha256.json').read_text())
routes = json.loads(Path(a.routes).read_text())
bg = np.array(Image.open(root/'build/Holy_Diver_(Tr)/Stage2_Cave_Background.png').convert('RGB'))
report = dict(baseline='0.6.1', candidate='0.7.0', emulator='MesenCE 2.2.1',
              controller_only=True, ram_writes=False, capture_stride=2, cases={})
matches, examples = Counter(), {}
atlas = Image.open(root/'art/screen2_1/Stage2_Exterior_Tiles_2x.png').convert('RGBA')
mapping = json.loads((root/'art/screen2_1/registration.json').read_text())['mappings']
cells = {(int(e['identity'],16),e['palette']):tuple(e['atlas']) for e in mapping}
poses = json.loads((root/'art/screen2_1/native_poses.json').read_text())
sources = []
for i,pose in enumerate(poses):
    palette = 'FF160636' if pose['kind']=='lava' else 'FF370726'
    image = Image.new('RGBA',tuple(v*2 for v in pose['size']))
    for x,y,t in pose['tiles']:
        ax,ay = cells[(t+0x200,palette)]
        image.paste(atlas.crop((ax,ay,ax+16,ay+16)),(x*2,y*2))
    sources.append((f"{pose['kind']}_{i}",image,pose['tiles'][0][2],0 if pose['kind']=='lava' else 1))
sources.append(('arrow',Image.open(root/'art/screen2_1/arrow_registered.png').convert('RGBA'),0x8c,1))
templates = []
for name,image,t,pal in sources:
    original = np.array(image)
    for flip in [False,True]:
        src = original[:,::-1] if flip else original
        mask = src[:,:,3]>0
        colors,counts = np.unique(src[:,:,:3][mask],axis=0,return_counts=True)
        color = colors[counts.argmin()]
        sy,sx = np.argwhere(mask & np.all(src[:,:,:3]==color,axis=2))[0]
        templates.append((name+('/mirrored' if flip else '/native'),src,mask,color,int(sx),int(sy),t,pal,flip))

def inspect_sprites(rgb,oams,case,n):
    for key,src,mask,color,sx,sy,t,pal,flip in templates:
        if not any(o[i]<239 and o[i+1]==t and o[i+2]&3==pal and bool(o[i+2]&64)==flip
                   for o in oams for i in range(0,256,4)):
            continue
        h,w = src.shape[:2]
        for y,x in np.argwhere(np.all(rgb==color,axis=2)):
            X,Y = int(x-sx),int(y-sy)
            if X<0 or Y<0 or X+w>512 or Y+h>480:
                continue
            if np.array_equal(rgb[Y:Y+h,X:X+w][mask],src[:,:,:3][mask]):
                matches[key]+=1
                examples.setdefault(key,dict(case=case,frame=n,box=[X,Y,X+w,Y+h]))
                break

for case,route in routes.items():
    b,c = Path(a.before)/case,Path(a.after)/case
    frames = route['frames']
    assert (b/'completed.txt').read_text()==(c/'completed.txt').read_text()==str(frames)
    assert (b/'input.json').read_bytes()==(c/'input.json').read_bytes()
    inputs = json.loads((c/'input.json').read_text())
    assert inputs['state_sha256']==a.state_sha256
    assert inputs['rom_sha1']=='fe2fcd0ad334d792db16535d09f3ab9fb2bea3ac'
    assert inputs['controller_route']==route.get('input_code','emu.setInput({'+route.get('input','')+'},0)')
    for folder,expected in [(b,old),(c,new)]:
        for name in ['installed_pack_sha256.json','installed_pack_after_sha256.json']:
            assert json.loads((folder/name).read_text())==expected,(case,name)
    r = dict(emulated_frames=frames,**inputs)
    for ext in ['ram','ppu','oam']:
        files = sorted((b/'dumps').glob('*.'+ext))
        assert len(files)==frames//2
        for f in files:
            assert f.read_bytes()==(c/'dumps'/f.name).read_bytes(),(case,f.name)
        r[ext+'_identical_samples']=len(files)
    apu = (b/'apu.tsv').read_bytes()
    assert apu==(c/'apu.tsv').read_bytes(),(case,'APU')
    r['apu_sha256']=hashlib.sha256(apu).hexdigest()
    bp,cp = (b/'full.wav').read_bytes()[44:],(c/'full.wav').read_bytes()[44:]
    common,tail = min(len(bp),len(cp)),abs(len(bp)-len(cp))
    assert common and bp[:common]==cp[:common],(case,'PCM')
    assert tail<=3200,(case,'audio shutdown tail',tail)
    r.update(identical_pcm_bytes=common,shutdown_tail_bytes=tail)
    rooms,states,palettes = Counter(),Counter(),Counter()
    black=outside=menu=changed=exact=backdrop=panorama=0
    scrolls=[]
    for n in range(2,frames+1,2):
        stem=f'{n:04}'
        ram=(c/'dumps'/f'{stem}.ram').read_bytes()
        ppu=(c/'dumps'/f'{stem}.ppu').read_bytes()
        before=np.array(Image.open(b/'frames'/f'{stem}.png').convert('RGB'))
        after=np.array(Image.open(c/'frames'/f'{stem}.png').convert('RGB'))
        equal=np.array_equal(before,after)
        exact+=equal;changed+=not equal
        room=f'{ram[0x72]:02X}/'+ram[0x78:0x7a].hex().upper()
        rooms[room]+=1;states[f'{ram[0x300]:02X}']+=1
        target=room=='10/AD8C'
        if before.max()==0:
            assert after.max()==0,(case,n,'native black screen')
            black+=1
        if case=='menu' and 40<n<175:
            assert equal,(case,n,'pause menu')
            menu+=1
        neighbors=[j for j in [n-2,n,n+2] if 2<=j<=frames]
        if not target and all((c/'dumps'/f'{j:04}.ram').read_bytes()[0x78:0x7a]!=bytes.fromhex('ad8c')
                              for j in neighbors):
            assert equal,(case,n,'outside requested room')
            outside+=1
        if target:
            palettes[ppu[0x3f04:0x3f08].hex().upper()]+=1
            scroll=int.from_bytes(ram[0x60:0x62],'little')
            if n>300:
                scrolls.append(scroll)
        # Palette RAM alone does not prove colored rendering during death.
        # Check actual native wall pixels before asserting panorama source RGB.
        wall=np.all(before==[108,6,0],axis=2)
        if target and ppu[0x3f08:0x3f0c]==bytes.fromhex('0f061828') and wall.sum()>1000:
            assert np.mean(np.all(after[wall]==0,axis=1))<0.01,(case,n,'missing backdrop')
            backdrop+=1
            if n%20==0:
                # Screenshots trail endFrame camera RAM by two frames.
                aligned=(c/'dumps'/f'{max(2,n-2):04}.ram').read_bytes()
                offset=2*int.from_bytes(aligned[0x60:0x62],'little') % 1024
                offsets={offset}
                count=max(int(np.all(after==bg[:,x:x+512],axis=2).sum()) for x in offsets)
                assert count>10000,(case,n,'panorama source mismatch',count,scroll)
                panorama+=1
        if target and n%40==0:
            oams=[(c/'dumps'/f'{j:04}.oam').read_bytes() for j in neighbors]
            inspect_sprites(after,oams,case,n)
    r.update(exact_black_samples=black,exact_outside_room_samples=outside,exact_menu_samples=menu,
             exact_screenshots=int(exact),changed_screenshots=int(changed),rooms=dict(rooms),
             player_states=dict(states),lava_palette_samples=dict(palettes),
             covered_cave_samples=backdrop,exact_panorama_samples=panorama,
             ram_scroll_range_including_transition_values=[min(scrolls),max(scrolls)] if scrolls else None)
    report['cases'][case]=r

assert sorted(k for k in old if old[k]!=new[k])==['README.txt','hires.txt']
assert sorted(set(new)-set(old))==['Stage2_Second_Cave_Tiles_2x.png']
report.update(total_frames_per_build=sum(v['frames'] for v in routes.values()),
              native_samples_per_type=sum(v['ram_identical_samples'] for v in report['cases'].values()),
              exact_black_samples=sum(v['exact_black_samples'] for v in report['cases'].values()),
              exact_outside_room_samples=sum(v['exact_outside_room_samples'] for v in report['cases'].values()),
              covered_cave_samples=sum(v['covered_cave_samples'] for v in report['cases'].values()),
              exact_panorama_samples=sum(v['exact_panorama_samples'] for v in report['cases'].values()),
              pixel_exact_complete_sprite_samples=dict(matches),sprite_examples=examples,
              unchanged_prior_runtime_files=83,pack_files=86)
out=Path(a.out);out.parent.mkdir(parents=True,exist_ok=True)
out.write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({k:v for k,v in report.items() if k not in ['cases','sprite_examples']},indent=2))
