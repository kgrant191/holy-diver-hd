from pathlib import Path
from PIL import Image,ImageDraw
import numpy as np,json
root=Path(__file__).resolve().parents[1];art=root/'art';out=root/'build/Holy_Diver_(Tr)';P=json.loads((art/'poses.json').read_text());src=Image.open(root/'art/generated/randy_generated.png').convert('RGBA')
atlas=Image.new('RGBA',(256,192));preview=Image.new('RGB',(4*192,3*220),'#192230');d=ImageDraw.Draw(preview);conditions=[];rules=[];seen={}
for i,p in enumerate(P):
 col=i%4;row=i//4;cell=src.crop((round(col*src.width/4),round(row*src.height/3),round((col+1)*src.width/4),round((row+1)*src.height/3)))
 # Alpha bounding boxes register the redrawn pose to the original visible extent.
 mask=cell.getchannel('A').point(lambda x:255 if x>=80 else 0);bb=mask.getbbox();cell=cell.crop(bb)
 old=Image.open(art/f'pose_{i}.png');obox=old.getchannel('A').getbbox();sprite=Image.new('RGBA',(64,64));cell=cell.resize(((obox[2]-obox[0])*2,(obox[3]-obox[1])*2),Image.Resampling.LANCZOS)
 # Binary alpha avoids translucent edges and colored fringes in the NES renderer.
 a=cell.getchannel('A').point(lambda x:255 if x>=135 else 0);rgb=cell.convert('RGB').quantize(colors=40,method=Image.Quantize.MEDIANCUT).convert('RGBA');rgb.putalpha(a);sprite.alpha_composite(rgb,(obox[0]*2,obox[1]*2))
 coverage=Image.new('L',(64,64));cd=ImageDraw.Draw(coverage)
 for x,y,t in p['tiles']:cd.rectangle((x*2,y*2,x*2+15,y*2+15),fill=255)
 arr=np.array(sprite);extra=((arr[:,:,3]>0)&(np.array(coverage)==0)).sum();arr[:,:,3]=np.minimum(arr[:,:,3],np.array(coverage));sprite=Image.fromarray(arr);print(i,'clipped pixels',extra)
 sprite.save(art/f'randy_pose_{i:02}.png');atlas.alpha_composite(sprite,(col*64,row*64));big=sprite.resize((192,192),Image.Resampling.NEAREST);preview.paste(big,(col*192,row*220),big);d.text((col*192+4,row*220+196),f'Pose {i}')
 # Minimal measured sprite-neighborhood signatures disambiguate shared tiles.
 for j,(x,y,t) in enumerate(p['tiles']):
  ours={(xx-x,yy-y,tt) for xx,yy,tt in p['tiles']}
  competitors=[]
  for qn,q in enumerate(P):
   for qx,qy,qt in q['tiles']:
    if qt==t and not(qn==i and qx==x and qy==y):competitors.append({(xx-qx,yy-qy,tt) for xx,yy,tt in q['tiles']})
  selected=[]
  while competitors:
   choices=[m for m in ours if m!=(0,0,t)]
   best=max(choices,key=lambda m:sum(m not in c for c in competitors))
   if all(best in c for c in competitors):break
   selected.append(best);competitors=[c for c in competitors if best in c]
  names=[]
  for dx,dy,tt in selected:
   key=(dx,dy,tt)
   if key not in seen:
    name=f'randySig{len(seen)}';seen[key]=name;conditions.append(f'<condition>{name},spriteNearby,{dx},{dy},{tt:02X},FF300036')
   names.append(seen[key])
  prefix='['+'&'.join(['gameplay','entranceLowerA','entranceLowerB','entrancePillar','litPalette']+names)+']'
  rules.append(prefix+f'<tile>18,{t:02X},FF300036,{col*64+x*2},{row*64+y*2},1,N')
atlas.save(out/'Randy_Entrance_2x.png');atlas.save(art/'Randy_Entrance_2x.png');preview.save(art/'randy_registered_preview.png')
base=(out/'hires.txt').read_text();pos=base.index('#Chr_00_0.png');base=base[:pos]+'<img>Randy_Entrance_2x.png\n'+'\n'.join(conditions)+'\n'+'\n'.join(rules)+'\n\n'+base[pos:];(out/'hires.txt').write_text(base)
print(len(conditions),'sprite conditions;',len(rules),'sprite rules')
