"""Level 2 wall boss, existing cave texture, shared actors and Breaker reward."""
from pathlib import Path
import hashlib,json,re
import numpy as np
from PIL import Image,ImageDraw,ImageFont
root=Path(__file__).resolve().parents[1];art=root/'art/boss2';pack=root/'build/Holy_Diver_(Tr)'
text=(pack/'hires.txt').read_text();assert text.count('<img>')==39
atlas=Image.new('RGBA',(1024,1024));cache={};rules=[];conds=[];backgrounds=[];records=[]
scope='b2Room&b2Lo&b2Hi'
conds += ['<condition>b2Room,memoryCheckConstant,0072,==,08','<condition>b2Lo,memoryCheckConstant,0078,==,7D','<condition>b2Hi,memoryCheckConstant,0079,==,8F']
def reg(im,size):
 im=im.convert('RGBA').resize(size,Image.Resampling.LANCZOS);alpha=im.getchannel('A').point(lambda a:255 if a>=128 else 0);im=im.convert('RGB').quantize(colors=64).convert('RGBA');im.putalpha(alpha);return im
def obj(path):
 im=Image.open(path).convert('RGBA');im.putalpha(im.getchannel('A').point(lambda a:255 if a>=128 else 0));return im.crop(im.getbbox())
def tile(t,pal,im,kind,sc=scope):
 key=hashlib.sha256(im.tobytes()).hexdigest()
 if key not in cache:
  n=len(cache);xy=(n%64*16,n//64*16);assert xy[1]+16<=1024;cache[key]=xy;atlas.paste(im,xy)
 x,y=cache[key];rules.append(('['+sc+']'if sc else '')+f'<tile>39,{t:04X},{pal},{x},{y},1,N');records.append(dict(identity=f'{t:04X}',palette=pal,xy=[x,y],kind=kind))
def tint(im,factor=1,color=None):
 a=np.array(im).copy()
 if color is not None:
  l=np.asarray(im.convert('L'))/255;a[:,:,:3]=np.stack([np.clip(l*c,0,255)for c in color],axis=2).astype('uint8')
 else:a[:,:,:3]=(a[:,:,:3].astype(float)*factor).clip(0,255).astype('uint8')
 return Image.fromarray(a)
empty=Image.new('RGBA',(16,16));layout=json.loads((art/'wall_layout.json').read_text());cover=Image.new('L',(192,256));d=ImageDraw.Draw(cover)
for x,y in layout.values():d.rectangle((x,y,x+15,y+15),fill=255)
wall=Image.new('RGBA',(192,256));wall.paste(reg(obj(root/'art/generated/boss2_wall_full_generated.png'),(160,224)),(12,16));wa=np.array(wall);clipped=int(((wa[:,:,3]>0)&(np.array(cover)==0)).sum());wa[:,:,3]=np.minimum(wa[:,:,3],np.array(cover));wall=Image.fromarray(wa);wall.save(art/'wall_registered.png')
variants={'0F121626':wall,'0F270027':tint(wall,color=[255,210,125]),'0F221636':tint(wall,1.12),'0F220036':tint(wall,color=[245,232,255]),'0F020616':tint(wall,.55),'0F0F0F06':tint(wall,.20),'0F071607':tint(wall,color=[140,72,30]),'0F041424':tint(wall,.35),'310F0F0F':tint(wall,0)}
for pal,im in variants.items():
 im.save(art/('wall_'+pal+'.png'))
 for t,(x,y)in layout.items():tile(int(t,16),pal,im.crop((x,y,x+16,y+16)),'wall boss / native palette phase')
for t in layout:tile(int(t,16),'0F0F0F0F',empty,'defeated boss hidden')
# Same brown rock source, newly registered to this bank's measured contours.
gold=reg(Image.open(root/'art/layers/50_floor.png').convert('RGBA').crop((256,880,320,912)),(32,32))
patterns=json.loads((art/'terrain_patterns.json').read_text());terrain={}
for key,b in patterns.items():
 t=int(key,16)
 if 0x543<=t<=0x54a:continue
 cell=gold.crop(((t&1)*16,((t>>1)&1)*16,(t&1)*16+16,((t>>1)&1)*16+16))
 mask=np.array([[bool(((b[y]|b[y+8])>>(7-x))&1)for x in range(8)]for y in range(8)])
 if 0x539<=t<=0x540:mask[:]=True
 else:
  for y in range(8):
   xs=np.flatnonzero(mask[y]);
   if len(xs):mask[y,xs[0]:xs[-1]+1]=True
  for x in range(8):
   ys=np.flatnonzero(mask[:,x]);
   if len(ys):mask[ys[0]:ys[-1]+1,x]=True
 cell.putalpha(Image.fromarray((mask*255).astype('uint8')).resize((16,16),Image.Resampling.NEAREST));terrain[key]=mask.astype(int).tolist()
 for pal,f in [('0F071737',1),('31071737',1),('0F0F0727',.65),('0F0F0F17',.38),('0F0F0F07',.18),('0F0F0F0F',0)]:tile(t,pal,tint(cell,f),'reused brown terrain / native contour')
# Non-solid orange wall motif is replaced by the existing crimson cave.
for t in [0x500,*range(0x543,0x54b)]:
 for pal in ['0F170F0F','0F070F0F','0F0F0F0F','0F021222','31170F0F','0F121626','0F270027','310F0F0F']:
  tile(t,pal,empty,'clear nonsolid wall / room space')
conds+=['<condition>b2Full,ppuMemoryCheckConstant,3F03,==,37','<condition>b2Flash,ppuMemoryCheckConstant,3F00,==,31']
for i,t in enumerate([*range(0x539,0x559)]):
 pal='0F170F0F'if 0x543<=t<=0x54a else '0F071737';name=f'b2Visible{i}';conds.append(f'<condition>{name},tileAtPosition,128,16,{t:04X},{pal}');backgrounds.append(f'[{scope}&b2Full&{name}]<background>Stage2_Crimson_Cave_Background.png,1,1,1,11,0,0')
 # Flash changes the universal palette component but preserves geometry.
 name+='F';conds.append(f'<condition>{name},tileAtPosition,128,16,{t:04X},31{pal[2:]}');backgrounds.append(f'[{scope}&b2Full&b2Flash&{name}]<background>Boss2_Cave_Flash.png,1,1,1,11,0,0')
bg=Image.open(pack/'Stage2_Crimson_Cave_Background.png').convert('RGB');a=np.array(bg);l=np.asarray(bg.convert('L'))/255;fa=np.stack([130+90*l,175+65*l,210+45*l],axis=2).astype('uint8');Image.fromarray(fa).save(pack/'Boss2_Cave_Flash.png')
# Native 16x16 boss projectiles use the approved fireball artwork.
fire=Image.open(root/'art/boss1/boss_fireball_registered.png').convert('RGBA');fire.save(art/'fireball_registered.png')
for i,t in enumerate(range(0x479,0x47d)):
 for pal,f in [('FF300616',1),('FF200F06',.6),('FF100F0F',.3),('FF000F0F',.12)]:tile(t,pal,tint(fire.crop((i%2*16,i//2*16,i%2*16+16,i//2*16+16)),f),'reused boss fireball')
book=reg(obj(root/'art/generated/boss2_breaker_generated.png'),(32,32));book.save(art/'breaker_registered.png')
for i,t in enumerate(range(0x475,0x479)):tile(t,'FF301116',book.crop((i%2*16,i//2*16,i%2*16+16,i//2*16+16)),'Breaker tome')
# Alias exact native actor copies, including every pose anchor, without edits.
inv=json.loads((art/'native_inventory.json').read_text());defs={l.split('>')[1].split(',')[0]:l for l in text.splitlines()if l.startswith('<condition>')};aliasdefs={};aliases=[]
def remap(sc,pal=None):
 out=[]
 for term in sc.split('&')if sc else []:
  neg='!'if term.startswith('!')else '';name=term.lstrip('!');parts=defs.get(name,'').split('>')[-1].split(',')
  if len(parts)>1 and parts[1]=='spriteNearby' and int(parts[4],16)<0x100:
   parts[4]=f'{int(parts[4],16)+0x400:04X}';new=f'b2copy_{pal or "native"}_{name}';parts[0]=new
   if pal:parts[5]=pal
   aliasdefs[new]='<condition>'+','.join(parts);name=new
  out.append(neg+name)
 return '&'.join(out)
for line in text.splitlines():
 m=re.fullmatch(r'(?:\[([^]]+)\])?<tile>(.*)',line)
 if not m:continue
 sc,p=m[1]or'',m[2].split(',');t=int(p[1],16);idx=int(p[0])
 if idx not in [18,19,20,21,22,23,26,27,31] or t>=0x74 or any(k in sc for k in ['pause','cardPal','lives']):continue
 if f'{t:04X}'not in inv['exact_shared_patterns'].get(f'{t+0x400:04X}',[]):continue
 q=p.copy();q[1]=f'{t+0x400:04X}';ns=remap(sc);aliases.append(('['+ns+']'if ns else '')+'<tile>'+','.join(q))
 # HUD/effect fade aliases keep their HD shape during native palette ramps.
 if p[2]=='FF301116':
  source=Image.open(pack/[l[5:]for l in text.splitlines()if l.startswith('<img>')][idx]).convert('RGBA').crop((int(p[3]),int(p[4]),int(p[3])+16,int(p[4])+16))
  for pal,f in [('FF200106',.65),('FF100F0F',.3),('FF000F0F',.12)]:tile(t+0x400,pal,tint(source,f),'shared HUD/effect fade',scope+('&'+remap(sc,pal)if sc else ''))
conds+=list(aliasdefs.values())
# Breaker announcement: exact native word probes, separate from Blizzard.
for name,addr,val in [('b2GotB',0x21cc,0x21),('b2GotR',0x21cd,0x33),('b2GotA',0x21cf,0x20),('b2GotK',0x21d0,0x2a),('b2GotEnd',0x21d2,0x33)]:conds.append(f'<condition>{name},ppuMemoryCheckConstant,{addr:04X},==,{val:02X}')
conds.append('<condition>b2GotRendered,tileAtPosition,96,112,1F21,0F213029')
cardsc='b2GotRendered&cardPal1&cardPal2&cardPal3&cardRendering&b2GotB&b2GotR&b2GotA&b2GotK&b2GotEnd';card=Image.open(pack/'Intermission_HD.png').convert('RGBA');d=ImageDraw.Draw(card);font=root/'art/fonts/DejaVuSerif-Bold.ttf'
for label,y,size,color in [('SPELL ACQUIRED',164,16,'#cbaa73'),('BREAKER',205,30,'#ffe1ab')]:d.text((256,y),label,font=ImageFont.truetype(str(font),size),fill=color,anchor='mt',stroke_width=1,stroke_fill='#050e20')
card.save(pack/'Breaker_Acquired.png');backgrounds.append(f'[{cardsc}]<background>Breaker_Acquired.png,1,0,0,12,0,0')
for t in [0,*range(0x10,0x40)]:tile(0x1f00+t,'0F213029',empty,'clear native Breaker announcement',cardsc)
def block(name,lines):return '# BEGIN BOSS2 '+name+'\n'+'\n'.join(lines)+'\n# END BOSS2 '+name+'\n'
end=text.index('\n',text.rfind('<img>'))+1;text=text[:end]+block('IMAGES',['<img>Boss2_Tiles_2x.png'])+text[end:];lines=text.splitlines(keepends=True);first=next(i for i,l in enumerate(lines)if '<tile>'in l or '<background>'in l);lines[first:first]=[block('CONDITIONS',conds),block('MAPPINGS',rules+backgrounds)];(pack/'hires.txt').write_text(''.join(lines)+block('ALIASES',aliases));atlas.save(pack/'Boss2_Tiles_2x.png');atlas.save(art/'Boss2_Tiles_2x.png')
(art/'registration.json').write_text(json.dumps(dict(tile_rules=len(rules)+len(aliases),conditions=len(conds),background_rules=len(backgrounds),alias_rules=len(aliases),atlas_cells=len(cache),wall_size=[192,256],source_fit=[160,224,12,16],clipped_root_pixels=clipped,terrain_masks=terrain,mappings=records,previous_runtime_assets_modified=False,native_gameplay_modified=False),indent=2)+'\n');print('Boss 2:',len(rules)+len(aliases),'rules;',len(cache),'cells; existing actors/scenery and new boss/Breaker.')
