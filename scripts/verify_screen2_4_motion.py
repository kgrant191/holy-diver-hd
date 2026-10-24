"""Measure downward lava motion and stationary Blizzard ice in actual captures."""
from pathlib import Path
from collections import Counter
import argparse
import hashlib
import json
import numpy as np
from PIL import Image

p=argparse.ArgumentParser()
p.add_argument('--after',required=True)
p.add_argument('--out',required=True)
a=p.parse_args()
root=Path(__file__).resolve().parents[1]
pack=root/'build/Holy_Diver_(Tr)'
atlas=np.array(Image.open(pack/'Stage2_Cave_Tiles_2x.png').convert('RGB'))
colors={pal:set() for pal in ['0F161606','0F060616','0F122131']}

def rgb_codes(im):
    im=im.astype(np.uint32)
    return (im[...,0]<<16)|(im[...,1]<<8)|im[...,2]

for line in (pack/'hires.txt').read_text().splitlines():
    if not line.startswith('[s24Room&s24DataLo&s24DataHi') or '<tile>33,' not in line:
        continue
    f=line.split('<tile>')[1].split(',')
    t,pal=int(f[1],16),f[2]
    if 0x389<=t<=0x38e and pal in colors:
        x,y=int(f[3]),int(f[4])
        colors[pal].update(rgb_codes(atlas[y:y+16,x:x+16]).ravel())

flow,ice=Counter(),Counter()
phases=set()
examples={}
for case in ['hot_falls','traversal']:
    folder=Path(a.after)/case
    previous=None
    for f in sorted((folder/'frames').glob('*.png')):
        n=int(f.stem)
        if n<1200:
            continue
        ram=(folder/'dumps'/f'{n:04}.ram').read_bytes()
        aligned=(folder/'dumps'/f'{n-2:04}.ram').read_bytes()
        scroll=int.from_bytes(aligned[0x60:0x62],'little')
        # Upper body of the first fall: the player and shots remain below it.
        # Select by actual source colors, including native palette flashes.
        X=2*(548-scroll)
        if ram[0x72]!=0x10 or ram[0x78:0x7a]!=bytes.fromhex('ad8c') or ram[0x440]==0 or not 0<=X<=488:
            previous=None
            continue
        crop=np.array(Image.open(f).convert('RGB'))[160:224,X:X+24]
        present=set(rgb_codes(crop).ravel())
        pal=next((pal for pal,values in colors.items() if present<=values),None)
        if previous and previous[:3]==(n-2,scroll,pal):
            prev=previous[3]
            if pal in ['0F161606','0F060616']:
                flow['pairs']+=1
                flow['downward_2px']+=int(np.array_equal(crop[2:],prev[:-2]))
                flow['upward_2px']+=int(np.array_equal(crop[:-2],prev[2:]))
                flow['stationary']+=int(np.array_equal(crop,prev))
                phases.add(hashlib.sha256(crop.tobytes()).hexdigest())
                examples.setdefault('hot',dict(case=case,frame=n,box=[X,160,X+24,224]))
            elif pal=='0F122131':
                ice['pairs']+=1
                ice['stationary']+=int(np.array_equal(crop,prev))
                examples.setdefault('ice',dict(case=case,frame=n,box=[X,160,X+24,224]))
        previous=(n,scroll,pal,crop)
assert flow['pairs']>30 and flow['downward_2px']==flow['pairs'],flow
assert flow['upward_2px']==flow['stationary']==0,flow
assert ice['pairs']>30 and ice['stationary']==ice['pairs'],ice
assert len(phases)>=16,len(phases)
report=dict(hot_fall=dict(flow),frozen_fall=dict(ice),distinct_hot_crops=len(phases),
            capture_stride=2,hd_pixels_down_per_capture=2,examples=examples)
out=Path(a.out)
out.parent.mkdir(parents=True,exist_ok=True)
out.write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
