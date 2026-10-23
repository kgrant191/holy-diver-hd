"""Register a continuous standing leg and keep its two native tiles joined."""
from pathlib import Path
import json
import numpy as np
from PIL import Image,ImageDraw

root=Path(__file__).resolve().parents[1]
art=root/'art/randy_foot';pack=root/'build/Holy_Diver_(Tr)'
meta=json.loads((art/'registration.json').read_text())
x0,y0,x1,y1=meta['target_rectangle']
assert meta['target_pose']==0 and (x0,y0,x1,y1)==(16,32,32,64)
coverage=Image.new('L',(64,64));d=ImageDraw.Draw(coverage)
for x,y,t in json.loads((root/'art/poses.json').read_text())[0]['tiles']:
    d.rectangle((x*2,y*2,x*2+15,y*2+15),fill=255)
for name,filename in meta['patches'].items():
    atlas=Image.open(pack/name).convert('RGBA');before=np.array(atlas)
    patch=Image.open(art/filename).convert('RGBA')
    assert patch.size==(x1-x0,y1-y0)
    assert not np.any((np.array(patch)[:,:,3]>0)&(np.array(coverage)[y0:y1,x0:x1]==0))
    # Fit the complete forward leg as one piece. Independent knee and boot
    # placement caused the rejected 0.3.3 repair's visible discontinuity.
    atlas.paste(patch,(x0,y0))
    alpha=np.array(atlas)[32:58,16:32,3]>0
    right=np.array([np.where(row)[0].max() for row in alpha])
    assert np.max(np.abs(np.diff(right)))<=2,'Abrupt knee/shin contour break'
    diff=np.any(before!=np.array(atlas),axis=2)
    allowed=np.zeros(diff.shape,bool);allowed[y0:y1,x0:x1]=True
    assert diff.any() and not np.any(diff&~allowed)
    atlas.save(pack/name)
text=(pack/'hires.txt').read_text()
defs=[]
for name,identity,palette,atlas,old_scope in [
    ('standingLegNormal','04','FF300036',18,'randySig8'),
    ('standingLegTwin','04','FF221136',19,'randyEquippedSig8')]:
    # Tile 04 is directly above the knee. Unlike the distant hand, it remains
    # visible with the leg during the observed left-edge room transition.
    defs.append(f'<condition>{name},spriteNearby,0,-8,{identity},{palette}')
    old=f'[{old_scope}]<tile>{atlas},07,{palette},16,32,1,N'
    new=f'[{name}]<tile>{atlas},07,{palette},16,32,1,N'
    assert text.count(old)==1,old
    text=text.replace(old,new)
lines=text.splitlines(keepends=True)
first=next(i for i,line in enumerate(lines) if '<tile>' in line or '<background>' in line)
lines[first:first]=['# BEGIN STANDING_LEG CONDITIONS\n'+'\n'.join(defs)+'\n# END STANDING_LEG CONDITIONS\n']
(pack/'hires.txt').write_text(''.join(lines))
print('Standing leg: continuous knee/shin/boot in both costumes; direct vertical pose probes.')
