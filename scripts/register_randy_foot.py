"""Reproduce the connected standing-leg patches from the retained generated edit."""
from pathlib import Path
import json
import numpy as np
from PIL import Image,ImageDraw

root=Path(__file__).resolve().parents[1];art=root/'art/randy_foot'
meta=json.loads((art/'registration.json').read_text())
source=Image.open(root/meta['generated_source']).convert('RGBA')
mask=Image.new('L',source.size);ImageDraw.Draw(mask).polygon([tuple(p) for p in meta['source_polygon']],fill=255)
pixels=np.array(source);pixels[:,:,3]=np.minimum(pixels[:,:,3],np.array(mask))
x0,y0,x1,y1=meta['target_rectangle']
registered=Image.fromarray(pixels).crop(tuple(meta['source_crop'])).resize((x1-x0,y1-y0),Image.Resampling.LANCZOS)
alpha=registered.getchannel('A').point(lambda v:255 if v>=128 else 0)
for name,filename in meta['patches'].items():
    # The arm and crouch fixes do not touch this historical forward-leg rectangle.
    old=np.array(Image.open(root/'rollback/approved_v15'/name).convert('RGBA').crop(tuple(meta['palette_rectangle'])))
    colors=np.unique(old[old[:,:,3]>0,:3],axis=0)
    palette=Image.new('P',(1,1));values=colors.flatten().tolist();palette.putpalette(values+[0]*(768-len(values)))
    patch=registered.convert('RGB').quantize(palette=palette,dither=Image.Dither.NONE).convert('RGBA')
    patch.putalpha(alpha);patch.save(art/filename)
print('Reproduced both connected standing-leg patches from retained source and approved colors.')
