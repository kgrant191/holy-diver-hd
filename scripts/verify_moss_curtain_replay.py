"""Pair native execution/audio and bound every changed pixel to repaired cells."""
from pathlib import Path
import argparse,json,hashlib,wave
from collections import Counter
import numpy as np
from PIL import Image

p=argparse.ArgumentParser()
for k in ['before','after','out']:p.add_argument('--'+k,required=True)
a=p.parse_args();root=Path(__file__).resolve().parents[1];before,after=Path(a.before),Path(a.after)
info=[json.loads((d/'result.json').read_text())for d in [before,after]]
for d,v in zip([before,after],info):
    if 'movie_frames'not in v:
        # The original runner writes this field after its final directory
        # audit. Host copy sidecars interrupted that audit in the full-stride
        # captures; require a complete consecutive sample sequence instead.
        seq=sorted(int(f.stem)for f in(d/'ram').glob('*.bin'))
        assert v['stride']==1 and seq==list(range(1,len(seq)+1))
        v['movie_frames']=len(seq)
for k in ['movie_sha256','rom_sha1','movie_frames','core_sha256','stride']:assert info[0][k]==info[1][k],k
assert all(v['movie_completed']for v in info)
prior=json.loads((root/'evidence/1.0.0-pack-sha256.json').read_text())
expected=[prior,json.loads((root/'evidence/1.0.1-pack-sha256.json').read_text())]
sidecars=[]
for i,d in enumerate([before,after]):
    manifest=json.loads((d/'installed_pack.json').read_text());pack=d/'mesen_home/HdPacks/Holy_Diver_(Tr)'
    # Older captures preceded the documentation-only version update. Accept
    # either approved README, and require every graphics/audio asset exactly.
    names=set(expected[i]);public={n:v for n,v in manifest.items()if not n.startswith('.')}
    assert set(public)==names
    for n in names:
        if n!='README.txt':assert public[n]==expected[i][n],(d,n)
        assert hashlib.sha256((pack/n).read_bytes()).hexdigest()==public[n],(d,n)
    extras=[f.name for f in pack.iterdir()if f.name.startswith('.')]
    assert all(n.startswith('.hires.txt.')for n in extras),extras
    sidecars.append(extras)
apu=(before/'apu.tsv').read_bytes();assert apu==(after/'apu.tsv').read_bytes()
with wave.open(str(before/'full.wav'))as f:params=f.getparams();pcm=f.readframes(f.getnframes())
with wave.open(str(after/'full.wav'))as f:assert f.getparams()==params and f.readframes(f.getnframes())==pcm
frames=sorted(int(f.stem)for f in(after/'ram').glob('*.bin'));native={}
for n in frames:
    d={}
    for kind in ['ram','ppu','oam','view']:
        name=f'{n:06}'+('.json'if kind=='view'else'.bin');b=(before/kind/name).read_bytes();assert b==(after/kind/name).read_bytes(),(n,kind)
        d[kind]=json.loads(b)if kind=='view'else b
    d['room']=int.from_bytes(d['ram'][0x78:0x7a],'little');native[n]=d
def mask(d):
    out=np.zeros((480,512),np.uint8)
    if d['room']!=0x9dee or d['ram'][0x72]!=0x14:return out
    pp=d['ppu'];v=d['view'];t=v['vram'];sx=(t&31)*8+v['xscroll']+(256 if t&0x400 else 0);sy=((t>>5)&31)*8+((t>>12)&7)+(240 if t&0x800 else 0)
    for yy in range(sy//8,(sy+239)//8+1):
        for xx in range(sx//8,(sx+255)//8+1):
            tx,ty=xx%32,yy%30;nt=0x2000+(xx//32%2)*0x400+(yy//30%2)*0x800;tile=0x700+pp[nt+ty*32+tx];at=pp[nt+960+ty//4*8+tx//4];pi=at>>((ty%4)//2*4+(tx%4)//2*2)&3
            pal=(bytes([pp[0x3f00]])+pp[0x3f01+pi*4:0x3f04+pi*4]).hex().upper()
            target=(tile in [0x74f,0x750,0x751,0x771,0x772,0x773]and pal in ['0F060616','0F161606','0F122131'])or(tile in range(0x73e,0x744)and pal=='0F122131')or(tile in range(0x74b,0x74f)and pal=='0F091929')or(tile in range(0x78e,0x792)and pal=='0F0A1A29')
            if target:
                x,y=(xx*8-sx)*2,(yy*8-sy)*2;out[max(0,y):min(480,y+16),max(0,x):min(512,x+16)]=1
    return out
stats=Counter();palettes=Counter();changed=[]
for idx,n in enumerate(frames):
    paths=[d/'frames'/f'{n:06}.png'for d in [before,after]]
    if not paths[0].stat().st_size:
        assert not paths[1].stat().st_size;stats['empty_initial_capture']+=1;continue
    old,new=[np.array(Image.open(d/'frames'/f'{n:06}.png').convert('RGB'))for d in [before,after]];diff=np.any(old!=new,2)
    if diff.any():
        near=[native[frames[j]]for j in range(max(0,idx-1),min(len(frames),idx+2))];allowed=np.logical_or.reduce([mask(d)for d in near])
        # Camera movement between sampled endFrame and submitted video is at
        # most one sample interval. Keep the measured two-pixel native margin.
        radius=2*info[1]['stride'];integral=np.pad(np.pad(allowed.astype('uint8'),radius),((1,0),(1,0))).astype('int32').cumsum(0).cumsum(1);w=radius*2+1
        allowed=integral[w:,w:]-integral[:-w,w:]-integral[w:,:-w]+integral[:-w,:-w]>0
        assert not(diff&~allowed).any(),(n,int((diff&~allowed).sum()))
        stats['changed_images_within_repaired_native_cells']+=1;changed.append(n)
    else:stats['identical_images']+=1
    if not old.any():assert not new.any();stats['blackouts_exact']+=1
    palettes[native[n]['ppu'][0x3f04:0x3f08].hex().upper()]+=1
report=dict(movie=info[1],native_samples_per_type=len(frames),native_ram_ppu_oam_view_exact=True,full_apu_and_pcm_exact=True,apu_sha256=hashlib.sha256(apu).hexdigest(),pcm_sha256=hashlib.sha256(pcm).hexdigest(),statistics=dict(stats),observed_lava_palette_rows=dict(palettes),changed_frames=changed,replay_host_copy_sidecars=sidecars,all_declared_runtime_files_unchanged_during_replay=True)
Path(a.out).write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:v for k,v in report.items()if k not in ['changed_frames','replay_host_copy_sidecars']},indent=2))
