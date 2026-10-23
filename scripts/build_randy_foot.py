"""Fit the standing pose's complete forward boot inside its native tiles."""
from pathlib import Path
import json
import numpy as np
from PIL import Image,ImageDraw

root=Path(__file__).resolve().parents[1]
art=root/'art/randy_foot';pack=root/'build/Holy_Diver_(Tr)'
meta=json.loads((art/'registration.json').read_text())
x0,y0,x1,y1=meta['target_rectangle']
assert meta['target_pose']==0 and (x0,y0,x1,y1)==(18,44,32,64)
coverage=Image.new('L',(64,64));d=ImageDraw.Draw(coverage)
for x,y,t in json.loads((root/'art/poses.json').read_text())[0]['tiles']:
    d.rectangle((x*2,y*2,x*2+15,y*2+15),fill=255)
for name,filename in meta['patches'].items():
    atlas=Image.open(pack/name).convert('RGBA');before=np.array(atlas)
    patch=Image.open(art/filename).convert('RGBA')
    assert patch.size==(x1-x0,y1-y0)
    assert not np.any((np.array(patch)[:,:,3]>0)&(np.array(coverage)[y0:y1,x0:x1]==0))
    # Replace the clipped lower boot, including its old silhouette. The rear
    # boot, knee, upper body and every other pose remain exactly as approved.
    atlas.paste(patch,(x0,y0))
    diff=np.any(before!=np.array(atlas),axis=2)
    allowed=np.zeros(diff.shape,bool);allowed[y0:y1,x0:x1]=True
    assert diff.any() and not np.any(diff&~allowed)
    atlas.save(pack/name)
print('Standing boot: complete toe registered in normal/Twin Fire native footprints.')
