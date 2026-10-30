"""Register whole final-boss forms and ending dragon before native slicing."""
from pathlib import Path
import json
import numpy as np
from PIL import Image
R=Path(__file__).resolve().parents[1];A=R/'art/level6_finale';G=R/'art/generated'
def registered(raw,size):
 raw=raw.convert('RGBA');box=raw.getchannel('A').point(lambda x:255 if x>=160 else 0).getbbox();raw=raw.crop(box).resize(size,Image.Resampling.LANCZOS);alpha=raw.getchannel('A').point(lambda x:255 if x>=160 else 0)
 raw=raw.convert('RGB').quantize(colors=192,dither=Image.Dither.NONE).convert('RGBA');raw.putalpha(alpha);return raw
def prepare():
 variants=json.loads((A/'boss_background_variants.json').read_text());patterns=json.loads((A/'native_patterns.json').read_text());old={v for k,v in patterns.items()if 0x1b00<=int(k,16)<0x1c00};report={};cells={};fills={}
 for name,filename in [('boss1','level6_final_boss.png'),('boss2','level6_final_boss_detached.png')]:
  spec=variants[name];x0,y0,x1,y1=spec['box'];whole=registered(Image.open(G/filename),(x1-x0,y1-y0));table={};blank=[]
  for pos in spec['positions']:
   x,y=pos['x']-x0,pos['y']-y0;cell=whole.crop((x,y,x+16,y+16))
   for t in pos['tiles']:
    if t=='1D00':continue
    if name=='boss1'and patterns[t]in old:continue
    table.setdefault(t,dict(x=x,y=y,image=cell))
   # Fill only permanently empty interior cells, never a destroyed boss part.
   if set(pos['tiles'])=={'1D00'}and cell.getchannel('A').getbbox():blank.append(dict(x=pos['x'],y=pos['y'],image=cell))
  whole.save(A/(name+'_painting.png'));cells[name]=table;fills[name]=blank;report[name]=dict(size=whole.size,box=spec['box'],unique_cells=len(table),static_interior_fill_cells=len(blank),native_dynamic_blank_cells_preserved=True)
 raw=Image.open(G/'level6_final_components.png').convert('RGBA');parts={}
 for i,name in enumerate(['joint0','joint1','joint2','joint3','connector','burst']):
  x,y=i%3*raw.width//3,i//3*raw.height//2;im=registered(raw.crop((x,y,x+raw.width//3,y+raw.height//2)),(48,32)if name=='connector'else(32,32));im.save(A/(name+'.png'));parts[name]=im
 parts['shot']=registered(parts['joint0'],(16,16));parts['shot'].save(A/'shot.png')
 # The three rotating attack silhouettes occupy 2, 4 and 3 native cells.
 for name,size,missing in [('arc0',(32,16),False),('arc1',(32,32),False),('arc2',(32,32),True)]:
  im=registered(parts['burst'],size)
  if missing:
   # Fit the entire lower half into the one native lower-left cell.
   bottom=im.crop((0,16,32,32)).resize((16,16),Image.Resampling.LANCZOS);im.paste((0,0,0,0),(0,16,32,32));im.paste(bottom,(0,16));im.putalpha(im.getchannel('A').point(lambda x:255 if x>=160 else 0))
  im.save(A/(name+'.png'));parts[name]=im
 # Two front-view ending poses. The curled lower-body cells are shared by NES.
 raw=Image.open(G/'level6_ending_dragon.png').convert('RGBA');dragon=[];layouts=[
  [(0xcd,0,0),(0xce,8,0),(0xcf,48,0),(0xd0,56,0)]+[(0xd1+i,8+i*8,8)for i in range(6)]+[(0xd7+i,16+i*8,16)for i in range(4)]+[(0xdb+i,16+i*8,24)for i in range(3)],
  [(0xde+i,8+i*8,0)for i in range(6)]+[(0xe4+i,i*8,8)for i in range(8)]+[(0xdb+i,16+i*8,16)for i in range(3)]]
 shared={}
 for i,layout in enumerate(layouts):
  size=(128,64 if i==0 else 48);im=registered(raw.crop((0,i*raw.height//2,raw.width,(i+1)*raw.height//2)),size);a=np.array(im);mask=np.zeros((size[1],size[0]),bool)
  for t,x,y in layout:mask[y*2:y*2+16,x*2:x*2+16]=True
  # Fit each side separately where the lifted wings leave a central gap.
  for y in range(size[1]):
   allowed=np.flatnonzero(mask[y]);active=np.flatnonzero(a[y,:,3])
   if not len(active):continue
   runs=np.split(allowed,np.where(np.diff(allowed)>1)[0]+1)
   if len(runs)==1:
    lo,hi=max(int(active[0]),int(allowed[0])),min(int(active[-1]),int(allowed[-1]))
    if active[0]<lo or active[-1]>hi:
     row=Image.fromarray(a[y:y+1,active[0]:active[-1]+1]).resize((hi-lo+1,1),Image.Resampling.LANCZOS);a[y]=0;a[y,lo:hi+1]=np.array(row)[0]
   else:
    original=a[y].copy();a[y]=0
    for k,run in enumerate(runs):
     lo,hi=(0,64)if k==0 else(64,128);xs=np.flatnonzero(original[lo:hi,3])+lo
     if len(xs):a[y,run[0]:run[-1]+1]=np.array(Image.fromarray(original[None,xs[0]:xs[-1]+1]).resize((len(run),1),Image.Resampling.LANCZOS))[0]
  im=Image.fromarray(a);im.putalpha(im.getchannel('A').point(lambda x:255 if x>=160 else 0))
  for t,x,y in layout:
   if t in shared:im.paste(shared[t],(x*2,y*2))
   else:shared[t]=im.crop((x*2,y*2,x*2+16,y*2+16))
  assert not ((np.array(im)[:,:,3]>0)&~mask).any();im.save(A/f'ending_dragon{i}.png');dragon.append((im,layout))
 report['ending_dragon']=dict(poses=2,shared_tail_cells=3,clipped_pixels=0,native_cell_unions_exact=True)
 (A/'source_registration.json').write_text(json.dumps(report,indent=2)+'\n');return cells,fills,parts,dragon
if __name__=='__main__':prepare()
