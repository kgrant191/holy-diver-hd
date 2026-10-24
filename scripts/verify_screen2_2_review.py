"""Bound the cave review to removed red decoration and downward hot falls."""
from pathlib import Path
import argparse,hashlib,json,re
from collections import Counter
import numpy as np
from PIL import Image
p=argparse.ArgumentParser()
for n in ['before','after','baseline-pack','approach-before','approach-after','out']:
    p.add_argument('--'+n,required=True)
a=p.parse_args();root=Path(__file__).resolve().parents[1]
oldpack=Path(a.baseline_pack);newpack=root/'build/Holy_Diver_(Tr)'
old=json.loads((root/'evidence/0.5.0-pack-sha256.json').read_text())
new=json.loads((root/'evidence/approved-pack-sha256.json').read_text())
assert set(old)==set(new)
assert sorted(k for k in old if old[k]!=new[k])==['README.txt','Stage2_Cave_Tiles_2x.png','hires.txt']
def mappings(pack):
    text=(pack/'hires.txt').read_text();atlas=np.array(Image.open(pack/'Stage2_Cave_Tiles_2x.png').convert('RGBA'))
    result={}
    for line in text.splitlines():
        if not line.startswith('[s22Room&s22DataLo&s22DataHi')or'<tile>33,'not in line:continue
        cond,data=line.split(']<tile>');f=data.split(',');x,y=int(f[3]),int(f[4])
        result[(int(f[1],16),f[2],cond[1:])]=atlas[y:y+16,x:x+16]
    return result
before_tiles,after_tiles=mappings(oldpack),mappings(newpack)
hud_atlas=np.array(Image.open(oldpack/'Screen_UI_2x.png').convert('RGBA'))
hud_alpha={}
for line in (oldpack/'hires.txt').read_text().splitlines():
    if line.startswith('[bossCopyHudPalette]<tile>21,02'):
        f=line.split('<tile>')[1].split(',');t=int(f[1],16)&255;x,y=int(f[3]),int(f[4])
        alpha=hud_atlas[y:y+16,x:x+16,3];hud_alpha[t]=(alpha>0)&(alpha<255)
scope='s22Room&s22DataLo&s22DataHi';hot={'0F161606','0F060616'}
is_red=lambda t,p:0x35f<=t<=0x368 and p=='0F061627'
is_fall=lambda t,p:0x389<=t<=0x38e and p in hot
unchanged=0;allowed=np.zeros(1<<24,dtype=bool)
def rgb_codes(a):
    a=a.astype(np.uint32);return(a[...,0]<<16)|(a[...,1]<<8)|a[...,2]
for key,pixels in before_tiles.items():
    t,pal,cond=key
    if is_red(t,pal):assert not after_tiles[key][:,:,3].any(),key
    elif not is_fall(t,pal):assert np.array_equal(pixels,after_tiles[key]),key;unchanged+=1
    if is_red(t,pal)or is_fall(t,pal):
        allowed[rgb_codes(pixels[:,:,:3])[pixels[:,:,3]>0]]=True
# Strict static proof: each hot body phase is a 2px downward translation of
# the preceding phase, including both 16px tile rows and the 32px loop seam.
fall_phases={}
for pal in sorted(hot):
    for phase in range(16):
        cond=scope+(f'&s22FallPhase{phase}'if phase else'')
        body=np.concatenate([np.concatenate([after_tiles[(t,pal,cond)]for t in row],axis=1)
                             for row in [[0x38b,0x38c],[0x38d,0x38e]]],axis=0)
        fall_phases[pal,phase]=body
        assert np.array_equal(body,np.roll(fall_phases[pal,0],phase*2,axis=0))
        for t,x in [(0x389,0),(0x38a,16)]:
            assert np.array_equal(after_tiles[t,pal,cond],body[16:32,x:x+16])
    assert np.array_equal(np.roll(body,2,axis=0),fall_phases[pal,0])
render_colors={pal:set(rgb_codes(fall_phases[pal,0][:,:,:3]).ravel())for pal in hot}
render_colors['0F122131']=set(np.concatenate([rgb_codes(after_tiles[t,'0F122131',scope][:,:,:3]).ravel()for t in range(0x389,0x38f)]))
def rendered_palette(crop):
    colors=set(rgb_codes(crop).ravel())
    return next((pal for pal,values in render_colors.items()if colors<=values),None)

routes=json.loads((root/'scripts/screen2_2_routes.json').read_text())
routes.update(json.loads((root/'scripts/screen2_2_approach_routes.json').read_text()))
report=dict(baseline='0.5.0',candidate='0.5.1',cases={})
flow=Counter();ice=Counter();observed=set();previous=None
for case,route in routes.items():
    b,c=(Path(a.approach_before)/case,Path(a.approach_after)/case)if case=='approach'else(Path(a.before)/case,Path(a.after)/case)
    frames=route['frames'];assert(b/'completed.txt').read_text()==(c/'completed.txt').read_text()==str(frames)
    assert(b/'input.json').read_bytes()==(c/'input.json').read_bytes()
    for folder,expected in [(b,old),(c,new)]:
        for name in ['installed_pack_sha256.json','installed_pack_after_sha256.json']:
            assert json.loads((folder/name).read_text())==expected
    for ext in ['ram','ppu','oam']:
        for f in (b/'dumps').glob('*.'+ext):assert f.read_bytes()==(c/'dumps'/f.name).read_bytes(),(case,f.name)
    assert(b/'apu.tsv').read_bytes()==(c/'apu.tsv').read_bytes()
    bp,cp=(b/'full.wav').read_bytes()[44:],(c/'full.wav').read_bytes()[44:]
    common=min(len(bp),len(cp));assert common and bp[:common]==cp[:common]
    assert abs(len(bp)-len(cp))<=3200
    changed=exact=black=0;previous=None
    for n in range(2,frames+1,2):
        stem=f'{n:04}';old_image=np.array(Image.open(b/'frames'/f'{stem}.png').convert('RGB'))
        new_image=np.array(Image.open(c/'frames'/f'{stem}.png').convert('RGB'))
        diff=np.any(old_image!=new_image,axis=2)
        allowed_pixels=allowed[rgb_codes(old_image)]
        # Existing antialiased HUD edges blend with the background beneath
        # them. Permit only their measured partial-alpha pixels, not glyph
        # interiors or a broad UI rectangle. HUD artwork/rules remain exact.
        for j in range(max(2,n-2),min(frames,n+2)+1,2):
            oo=(c/'dumps'/f'{j:04}.oam').read_bytes()
            for y,t,attr,x in zip(oo[::4],oo[1::4],oo[2::4],oo[3::4]):
                if y>=40 or t not in hud_alpha or attr&3!=2 or x>248:continue
                alpha=hud_alpha[t]
                if attr&64:alpha=alpha[:,::-1]
                if attr&128:alpha=alpha[::-1]
                Y,X=2*(y+1),2*x;allowed_pixels[Y:Y+16,X:X+16]|=alpha
        # Asset-specific old RGB values bound every changed pixel. Separate
        # tile comparisons above keep pools, gold, ice and sprites exact.
        assert not np.any(diff & ~allowed_pixels),(case,n,'unrelated pixels changed')
        changed+=bool(diff.any());exact+=not diff.any()
        if old_image.max()==0:assert new_image.max()==0;black+=1
        ram=(c/'dumps'/f'{stem}.ram').read_bytes();ppu=(c/'dumps'/f'{stem}.ppu').read_bytes()
        scroll=int.from_bytes(ram[96:98],'little');pal=ppu[0x3f04:0x3f08].hex().upper()
        # A fixed, unobstructed portion of the first fall, after the camera
        # stops. Restrict to living gameplay and the source-defined palettes.
        if case=='crossing' and ram[0x72]==0x10 and ram[0x440]>0 and 1500<=n<=2500 and scroll in [548,569]:
            X=2*(608-scroll);crop=new_image[160:288,X:X+32]
            old_crop=old_image[160:288,X:X+32]
            # endFrame PPU palettes lead the displayed image during native
            # black flashes/pulse changes. Classify the actual rendered fall
            # using its exact source colors; blackouts are checked separately.
            rendered=rendered_palette(crop)
            if previous and previous[0]==scroll and previous[1]==rendered:
                prev=previous[2]
                if rendered in hot:
                    down=np.array_equal(crop[2:],prev[:-2]);up=np.array_equal(crop[:-2],prev[2:])
                    flow['pairs']+=1;flow['downward_2px']+=down;flow['upward_2px']+=up
                    flow['identical']+=np.array_equal(crop,prev)
                    observed.add(hashlib.sha256(crop.tobytes()).hexdigest())
                elif rendered=='0F122131':
                    ice['pairs']+=1;ice['stationary']+=np.array_equal(crop,prev)
                    assert np.array_equal(crop,old_crop),(case,n,'ice artwork changed')
            previous=(scroll,rendered,crop)
        else:previous=None
    report['cases'][case]=dict(frames=frames,paired_memory_samples_per_type=frames//2,changed_screenshots=changed,
                              exact_screenshots=exact,exact_black_samples=black,identical_pcm_bytes=common,
                              shutdown_tail_bytes=abs(len(bp)-len(cp)))
assert flow['downward_2px']>30 and flow['downward_2px']==flow['pairs'] and flow['upward_2px']==0,flow
assert ice['stationary']>30 and ice['stationary']==ice['pairs'],ice
assert len(observed)>=16,len(observed)
report.update(total_frames_per_build=sum(r['frames']for r in routes.values()),unchanged_pack_files=81,
              unchanged_cave_tile_variants=unchanged,removed_red_tile_variants=10,
              hot_fall_animation=dict(phases=16,frames_per_phase=2,downward_hd_pixels_per_phase=2),
              actual_hot_flow_samples=dict(flow),actual_frozen_samples=dict(ice),distinct_hot_crops=len(observed),
              change_bounds='Removed red decoration and hot falls only; other tile pixels and 81 pack files exact.')
out=Path(a.out);out.parent.mkdir(parents=True,exist_ok=True);out.write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({k:v for k,v in report.items()if k!='cases'},indent=2))
