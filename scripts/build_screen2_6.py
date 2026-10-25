"""Screen 2-6: reuse scenery and register only the new walking dragon."""
from pathlib import Path
import hashlib,json
import numpy as np
from PIL import Image,ImageDraw

root=Path(__file__).resolve().parents[1];pack=root/'build/Holy_Diver_(Tr)';art=root/'art/screen2_6'
text=(pack/'hires.txt').read_text();assert text.count('<img>')==38
images=[line[5:]for line in text.splitlines()if line.startswith('<img>')]
scope='s26Room&s26DataLo&s26DataHi'
conditions=['<condition>s26Room,memoryCheckConstant,0072,==,10',
 '<condition>s26DataLo,memoryCheckConstant,0078,==,8D',
 '<condition>s26DataHi,memoryCheckConstant,0079,==,8E',
 '<condition>s26Wall0,ppuMemoryCheckConstant,3F09,==,06',
 '<condition>s26Wall1,ppuMemoryCheckConstant,3F0A,==,16',
 '<condition>s26Wall2,ppuMemoryCheckConstant,3F0B,==,26']
rules=[];metadata=[];atlas=Image.new('RGBA',(256,128));cache={}
def tile(t,palette,im,kind,condition=scope):
 key=hashlib.sha256(im.tobytes()).hexdigest()
 if key not in cache:
  n=len(cache);xy=(n%16*16,n//16*16);assert xy[1]+16<=atlas.height;cache[key]=xy;atlas.paste(im,xy)
 x,y=cache[key];prefix='['+condition+']'if condition else ''
 rules.append(f'{prefix}<tile>38,{t:04X},{palette},{x},{y},1,N')
 metadata.append(dict(identity=f'{t:04X}',palette=palette,atlas=[x,y],kind=kind,scope=condition))

poses=json.loads((art/'native_enemy_poses.json').read_text())
source=Image.open(root/'art/generated/screen2_6_dragon_generated.png').convert('RGBA')
cells={};registered=[];clipped=[]
for i,pose in enumerate(poses):
 im=source.crop((i*source.width//2,0,(i+1)*source.width//2,source.height))
 im=im.crop(im.getchannel('A').point(lambda a:255 if a>=128 else 0).getbbox()).resize((92,70),Image.Resampling.LANCZOS)
 alpha=im.getchannel('A').point(lambda a:255 if a>=128 else 0)
 im=im.convert('RGB').quantize(colors=64).convert('RGBA');im.putalpha(alpha)
 full=Image.new('RGBA',(96,80));full.paste(im,(4,10))
 cover=Image.new('L',(96,80));draw=ImageDraw.Draw(cover)
 for part in pose['parts']:
  x,y=[v*2 for v in part['xy']];draw.rectangle((x,y,x+15,y+15),fill=255)
 outside=int(((np.array(full)[:,:,3]>0)&(np.array(cover)==0)).sum());clipped.append(outside);assert outside==0,(i,outside)
 # The native upper-body identities are shared between the two walking
 # poses. Reuse those exact cells so only the native leg cells animate.
 for part in pose['parts']:
  t=int(part['identity'],16);x,y=[v*2 for v in part['xy']]
  if t in cells:full.paste(cells[t],(x,y))
  else:cells[t]=full.crop((x,y,x+16,y+16))
 full.save(art/f'dragon_pose_{i}.png');registered.append(full)
for t,im in sorted(cells.items()):tile(t,'FF162730',im,'walking dragon',None)
# Its two-cell shot reuses the approved boss fireball source, fitted into the
# native horizontal projectile footprint. OAM retains direction and timing.
projectile=Image.open(root/'art/boss1/boss_fireball_registered.png').convert('RGBA').resize((32,16),Image.Resampling.LANCZOS)
alpha=projectile.getchannel('A').point(lambda a:255 if a>=128 else 0);projectile=projectile.convert('RGB').quantize(colors=48).convert('RGBA');projectile.putalpha(alpha)
projectile.save(art/'dragon_fireball.png')
for i,t in enumerate([0x2d6,0x2d7]):tile(t,'FF162730',projectile.crop((i*16,0,i*16+16,16)),'reused fireball',None)

# New native registrations reuse existing brown body cells, not new paint.
brown=json.loads((root/'art/screen2_5_roof/previous_geometry.json').read_text())
for target,original in [(0x346,'0330'),(0x34e,'0332')]:
 src=brown[original];x,y=src['xy'];idx=images.index(src['image'])
 rules.append(f'[{scope}]<tile>{idx},{target:04X},0F081737,{x},{y},1,N')
# The red repeating wall and nonsolid gold hanging decoration reveal the
# accepted crimson panorama. Solid overhead brown shapes remain visible.
empty=Image.new('RGBA',(16,16))
for t in range(0x39b,0x3a1):tile(t,'0F061626',empty,'shared crimson background reveal')
for t in range(0x35f,0x369):tile(t,'0F071727',empty,'nonsolid hanging decoration removed')
for palette in ['0F061626','0F071727','0F081737']:tile(0x300,palette,empty,'cave space')
guards=[(int(t,16),'0F081737')for t in brown]
guards += [(t,'0F081737')for t in [0x32e,0x32f,0x346,0x34e,*range(0x375,0x381)]]
guards += [(t,'0F061626')for t in range(0x39b,0x3a1)]+[(t,'0F071727')for t in range(0x35f,0x369)]
backgrounds=[]
for i,(t,pal)in enumerate(guards):
 name=f's26Rendered{i}';conditions.append(f'<condition>{name},tileAtPosition,128,16,{t:04X},{pal}')
 backgrounds.append(f'[{scope}&s26Wall0&s26Wall1&s26Wall2&{name}]<background>Stage2_Crimson_Cave_Background.png,1,1,1,11,0,0')
def section(kind,lines):return '# BEGIN SCREEN2_6 '+kind+'\n'+'\n'.join(lines)+'\n# END SCREEN2_6 '+kind+'\n'
end=text.index('\n',text.rfind('<img>'))+1;text=text[:end]+section('IMAGES',['<img>Stage2_Dragon_2x.png'])+text[end:]
lines=text.splitlines(keepends=True);first=next(i for i,line in enumerate(lines)if '<tile>'in line or '<background>'in line)
lines[first:first]=[section('CONDITIONS',conditions),section('MAPPINGS',rules+backgrounds)]
(pack/'hires.txt').write_text(''.join(lines));atlas.save(pack/'Stage2_Dragon_2x.png');atlas.save(art/'Stage2_Dragon_2x.png')
(art/'registration.json').write_text(json.dumps(dict(scope=scope,tile_rules=len(rules),conditions=len(conditions),background_rules=len(backgrounds),atlas_cells=len(cache),new_painted_assets=['walking dragon'],reused_projectile='art/boss1/boss_fireball_registered.png',reused_background='Stage2_Crimson_Cave_Background.png',new_brown_registrations={'0346':'0330','034E':'0332'},dragon_clipped_pixels=clipped,shared_dragon_cells=len(set(int(p['identity'],16)for p in poses[0]['parts'])&set(int(p['identity'],16)for p in poses[1]['parts'])),mappings=metadata,previous_runtime_assets_modified=False,native_gameplay_modified=False),indent=2)+'\n')
print('Screen 2-6:',len(rules),'rules; existing scenery and new walking dragon.')
