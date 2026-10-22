"""Register the generated terrain to measured NES scene coordinates.
This is asset extraction/registration, never screenshot compositing.
"""
from pathlib import Path
import numpy as np
from PIL import Image
from scipy.ndimage import binary_closing,binary_fill_holes,binary_dilation
root=Path(__file__).resolve().parents[1]; art=root/'art'; layers=art/'layers';layers.mkdir(exist_ok=True)
src=Image.open(root/'art/generated/chamber_generated.png').convert('RGB').resize((512,960),Image.Resampling.LANCZOS)
a=np.asarray(src).astype(float)
warm=(a[:,:,0]>a[:,:,2]*.83)&(a[:,:,0]>a[:,:,1]*1.12)&(a[:,:,0]>24)
warm=binary_closing(warm,iterations=1)
bg=Image.open(root/'art/generated/backdrop_generated.png').convert('RGB').resize((512,960),Image.Resampling.LANCZOS)
# Slightly lower the busy distant architecture's value for foreground readability.
bg=Image.fromarray((np.array(bg)*.78).astype('uint8')).quantize(colors=80,method=Image.Quantize.MEDIANCUT).convert('RGBA')
bg.save(layers/'00_distant_ruins.png')
def empty():return Image.new('RGBA',(512,960))
def store(name,im):im.save(layers/name);return im
# Extract the generated lunar disk with its castle occlusion intact. Keep the
# approved background pixels outside the moon unchanged. This is a separate
# editable layer; the former foreground jewel/branches are removed entirely.
moon=Image.open(art/'generated/moon_background_generated.png').convert('RGBA').resize((512,960),Image.Resampling.LANCZOS)
ma=np.asarray(moon);mm=np.zeros((960,512),dtype=bool)
mm[64:180,320:430]=(ma[64:180,320:430,0]>40)&(ma[64:180,320:430,1]>40)
mm=binary_fill_holes(binary_closing(mm,iterations=1))
moon.putalpha(Image.fromarray((mm*255).astype('uint8')))
store('05_moon_behind_castles.png',moon)
old_orb=layers/'40_orb.png'
if old_orb.exists():old_orb.unlink()
# Terrain registration: vertical landmark pairs source->collision-aligned target.
left=empty();lp=left.load();sp=src.load()
layout=np.asarray(Image.open(art/'chamber_layout.png').convert('RGB'))
from scipy.ndimage import gaussian_filter1d
edges=[]
for yy in range(839):
 inds=np.where(warm[yy,:164])[0]
 edge=int(inds[-1]+1) if len(inds) else (100 if yy<197 else 133 if yy<525 else 154)
 edges.append(min(edge,116 if yy<197 else 138 if yy<525 else 161))
smoothed=np.empty(839)
for a0,a1 in [(0,197),(197,525),(525,839)]:smoothed[a0:a1]=gaussian_filter1d(np.array(edges[a0:a1],float),7)
for y in range(864):
 # Live stationary landing confirms the second ledge is NES Y272 = HD Y544.
 sy=min(838,int(np.interp(y,[0,192,544,864],[0,197,525,838])))
 desired=96 if y<192 else 128 if y<544 else 160
 edge=edges[sy];ratio=desired/smoothed[sy]
 tw=max(1,round(edge*ratio))
 rowim=src.crop((0,sy,edge,sy+1)).resize((tw,1),Image.Resampling.LANCZOS).convert('RGBA')
 left.paste(rowim.crop((0,0,min(desired,tw),1)),(0,y))
store('10_cliff.png',left)
# Tree body, roots and FIVE branches are independently registered. The original
# room has left branches at NES world Y 192, 288, 384 and right branches at
# Y 240, 336. All five were confirmed by stationary controller-only landings.
def cut(box,mask=True):
 x0,y0,x1,y1=box;im=src.crop(box).convert('RGBA')
 if mask:
  m=warm[y0:y1,x0:x1];m=binary_fill_holes(binary_closing(m,iterations=1));m=binary_dilation(m,iterations=1)
  im.putalpha(Image.fromarray((m*255).astype('uint8')))
 return im
trunk=empty();body=cut((282,313,354,819));body=body.resize((68,504),Image.Resampling.NEAREST);trunk.alpha_composite(body,(286,320))
roots=cut((253,800,388,841));trunk.alpha_composite(roots.resize((136,48),Image.Resampling.NEAREST),(252,816))
# source_contact_y is the branch's main load-bearing ridge in the generated
# image, not the top of the crop (which includes decorative knots/twigs).
branch_specs = [
 ('upper_left',  (225,374,292,394), 224, (68,20), 378, 384),
 ('upper_right', (345,463,412,488), 350, (66,24), 468, 480),
 ('middle_left', (225,547,292,575), 224, (68,28), 555, 576),
 ('lower_right', (345,653,412,676), 350, (66,24), 658, 672),
 ('lower_left',  (225,745,292,768), 224, (68,24), 750, 768),
]
for name,box,x,size,source_contact_y,world_contact_y in branch_specs:
 dy=round((source_contact_y-box[1])*size[1]/(box[3]-box[1]))
 dest=(x,world_contact_y-dy)
 piece=cut(box);trunk.alpha_composite(piece.resize(size,Image.Resampling.NEAREST),dest)
store('20_tree_and_branches.png',trunk)
pillars=empty();pillars.alpha_composite(cut((438,0,483,754),False).resize((32,784),Image.Resampling.NEAREST),(448,0));pillars.alpha_composite(cut((494,0,512,960),False).resize((16,960),Image.Resampling.NEAREST),(496,0));store('30_pillars.png',pillars)
floor=empty();floor.alpha_composite(src.crop((0,838,512,960)).convert('RGBA').resize((512,96),Image.Resampling.NEAREST),(0,864));store('50_floor.png',floor)
scene=bg.copy()
for im in [moon,left,trunk,pillars,floor]:scene.alpha_composite(im)
scene.save(art/'EntranceScene_registered.png')
# OpenRaster layered source, directly editable by common raster editors.
import zipfile,io,xml.etree.ElementTree as ET
stack=ET.Element('image',{'w':'512','h':'960','name':'Holy Diver • Cursed Chapel Entrance'});st=ET.SubElement(stack,'stack')
with zipfile.ZipFile(art/'Holy_Diver_Entrance.ora','w') as z:
 z.writestr('mimetype','image/openraster',compress_type=zipfile.ZIP_STORED)
 for i,p in enumerate(reversed(sorted(layers.glob('*.png')))):
  dest=f'data/layer{i}.png';z.write(p,dest);ET.SubElement(st,'layer',{'name':p.stem,'src':dest,'opacity':'1.0','visibility':'visible','composite-op':'svg:src-over','x':'0','y':'0'})
 z.writestr('stack.xml',ET.tostring(stack));buf=io.BytesIO();scene.save(buf,format='PNG');z.writestr('mergedimage.png',buf.getvalue())
print('Registered scene and six editable layers saved.')
