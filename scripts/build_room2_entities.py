"""Register screen-2 enemy animation and heart/magic pickups to native OAM tiles."""
from pathlib import Path
from PIL import Image,ImageDraw
import numpy as np,json
root=Path(__file__).resolve().parents[1];art=root/'art/room2';out=root/'build/Holy_Diver_(Tr)';src=Image.open(root/'art/generated/crypt_enemies_generated.png').convert('RGBA')
# Measured non-overlapping source rectangles; generator gave wider flying sprites.
rects=[(0,0,535,550),(535,0,1040,550),(1040,0,1380,550),(1380,0,1774,550),(0,550,444,887),(444,550,888,887),(888,550,1331,887),(1331,550,1774,887)]
raw=[]
for rect in rects:
 im=src.crop(rect);bb=im.getchannel('A').point(lambda x:255 if x>=120 else 0).getbbox();raw.append(im.crop(bb))
def reg(im,size):
 im=im.resize(size,Image.Resampling.LANCZOS);a=im.getchannel('A').point(lambda p:255 if p>=120 else 0)
 im=im.convert('RGB').quantize(colors=40,method=Image.Quantize.MEDIANCUT).convert('RGBA');im.putalpha(a);return im
poses=json.loads((art/'enemy_poses.json').read_text());rules=[];atlas=Image.new('RGBA',(256,256));slot=0;stats={};seen=set()
scope='cryptPalette&cryptStonePalette&cryptSpritePalette'
def tile(t,pal,im,cond=scope):
 global slot
 key=(t,pal,cond)
 if key in seen:return
 seen.add(key);x=slot%16*16;y=slot//16*16;slot+=1;atlas.alpha_composite(im,(x,y));rules.append(f'[{cond}]<tile>25,{t:02X},{pal},{x},{y},1,N')
for i,p in enumerate(poses[:4]):
 w=max(x+8 for x,y,t in p['tiles'])*2;h=max(y+8 for x,y,t in p['tiles'])*2
 sprite=Image.new('RGBA',(w,h))
 if i<2:sprite=reg(raw[i],(w,h))
 else:
  # Preserve head/body width as the walking stance closes, avoiding size pulsing.
  rw=32 if i==2 else round(raw[i].width/raw[2].width*32)
  sprite.alpha_composite(reg(raw[i],(rw,h)),((w-rw)//2,0))
 cover=Image.new('L',(w,h));dr=ImageDraw.Draw(cover)
 for x,y,t in p['tiles']:dr.rectangle((x*2,y*2,x*2+15,y*2+15),fill=255)
 a=np.asarray(sprite).copy();clipped=int(((a[:,:,3]>0)&(np.asarray(cover)==0)).sum());a[:,:,3]=np.minimum(a[:,:,3],np.asarray(cover));sprite=Image.fromarray(a);stats[p['name']]={'clipped_pixels':clipped,'size':[w,h]}
 if i==1:
  # Native animation changes only four cloak tiles. Keep the head/staff/feet
  # absolutely fixed so overlapping enemies never require remote pose probes.
  stable=Image.open(art/'flying_0_hd.png').convert('RGBA')
  for x,y,t in p['tiles']:
   if t in [0xbb,0xbc,0xbd,0xbe]:stable.paste(sprite.crop((x*2,y*2,x*2+16,y*2+16)),(x*2,y*2))
  sprite=stable
 sprite.save(art/(p['name']+'_hd.png'))
 for x,y,t in p['tiles']:tile(t,p['palette'],sprite.crop((x*2,y*2,x*2+16,y*2+16)))
for phase in [1,0]:
 sprite=Image.new('RGBA',(32,32));sprite.alpha_composite(reg(raw[4+phase],(32 if phase==0 else 27,21)),(0 if phase==0 else 2,0));sprite.save(art/f'small_creature_{phase}_hd.png')
 for x,y,t in poses[4]['tiles']:tile(t,poses[4]['palette'],sprite.crop((x*2,y*2,x*2+16,y*2+16)),scope+('&cryptBatPhase' if phase else ''))
# The two drops share palette slot 2 with HUD/projectiles, but unique tile IDs.
for i,p in enumerate(poses[5:]):
 sprite=Image.new('RGBA',(16,16));sprite.alpha_composite(reg(raw[6+i],(14,14)),(1,1));sprite.save(art/(p['name']+'_hd.png'));tile(p['tiles'][0][2],p['palette'],sprite)
# Native defeat/impact rings use eight sparse 8x8 sprites around an empty
# center. Preserve their positions and let the game animate the effect.
puff=Image.open(root/'art/generated/crypt_impact_generated.png').convert('RGBA')
puff=puff.crop(puff.getchannel('A').point(lambda p:255 if p>=120 else 0).getbbox())
puff=reg(puff,(64,64));puff.save(art/'impact_hd.png')
for t,x,y in [(0x6c,1,0),(0x6d,2,0),(0x6e,0,1),(0x6f,3,1),(0x70,0,2),(0x71,3,2),(0x72,1,3),(0x73,2,3)]:
 tile(t,'FF301116',puff.crop((x*16,y*16,x*16+16,y*16+16)))
atlas.save(art/'Crypt_Entities_2x.png');atlas.save(out/'Crypt_Entities_2x.png')
p=out/'hires.txt';s=p.read_text();last=s.rfind('<img>');end=s.index('\n',last);s=s[:end]+'\n<img>Crypt_Entities_2x.png'+s[end:]
pos=s.index('<condition>');s=s[:pos]+'<condition>cryptBatPhase,frameRange,16,8\n'+s[pos:]
pos=s.index('#Chr_00_0.png');s=s[:pos]+'\n'.join(rules)+'\n'+s[pos:];p.write_text(s)
(art/'entity_registration.json').write_text(json.dumps({'source_rectangles':rects,'poses':stats,'tile_rules':len(rules)},indent=2)+'\n');print(stats,len(rules))
