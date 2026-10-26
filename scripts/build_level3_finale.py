"""Finish the recorded Poison Moss Land climb, boss and Overdrive transition."""
from pathlib import Path
import hashlib,json,re
import numpy as np
from PIL import Image,ImageDraw,ImageFont

r=Path(__file__).resolve().parents[1];pack=r/'build/Holy_Diver_(Tr)';art=r/'art/level3_finale'
text=(pack/'hires.txt').read_text();images=[l[5:]for l in text.splitlines()if l.startswith('<img>')];assert len(images)==46
atlas=Image.new('RGBA',(512,512));cache={};rules=[];conds=[];backgrounds=[];records=[];aliases=[];alias_records=[];imagecache={}
patterns={int(k,16):bytes.fromhex(v)for k,v in json.loads((art/'native_patterns.json').read_text()).items()}
shared=json.loads((art/'shared_patterns.json').read_text());observed=json.loads((art/'observed_backgrounds.json').read_text())
layouts=json.loads((art/'sprite_layouts.json').read_text());empty=Image.new('RGBA',(16,16))
def register(im,size):
 im=im.convert('RGBA').resize(size,Image.Resampling.LANCZOS);alpha=im.getchannel('A').point(lambda v:255 if v>=128 else 0)
 im=im.convert('RGB').quantize(colors=64).convert('RGBA');im.putalpha(alpha);return im
def obj(path):
 im=Image.open(path).convert('RGBA');box=im.getchannel('A').point(lambda v:255 if v>=128 else 0).getbbox();assert box;return im.crop(box)
def cell(f):
 idx,x,y=int(f[0]),int(f[3]),int(f[4])
 if idx not in imagecache:imagecache[idx]=Image.open(pack/images[idx]).convert('RGBA')
 return imagecache[idx].crop((x,y,x+16,y+16))
def tile(t,pal,im,kind,scope,brightness='1'):
 assert im.size==(16,16);key=hashlib.sha256(im.tobytes()).hexdigest()
 if key not in cache:
  n=len(cache);xy=(n%32*16,n//32*16);assert xy[1]+16<=512;cache[key]=xy;atlas.paste(im,xy)
 x,y=cache[key];rule=('['+scope+']'if scope else '')+f'<tile>46,{t:04X},{pal},{x},{y},{brightness},N';rules.append(rule)
 records.append(dict(tile=f'{t:04X}',palette=pal,xy=[x,y],brightness=brightness,kind=kind,scope=scope,rule=rule))
def room_scope(room):
 ptr=int(room,16);name='l3f'+room
 for suffix,addr,val in [('Mode',0x72,4),('Lo',0x78,ptr&255),('Hi',0x79,ptr>>8)]:conds.append(f'<condition>{name}{suffix},memoryCheckConstant,{addr:04X},==,{val:02X}')
 return f'{name}Mode&{name}Lo&{name}Hi'
climb=room_scope('9F1A');boss=room_scope('9F92')
def hull(t):
 b=patterns[t];a=np.array([[255 if ((b[y]|b[y+8])>>(7-x))&1 else 0 for x in range(8)]for y in range(8)],dtype=np.uint8)
 for y in range(8):
  xs=np.flatnonzero(a[y])
  if len(xs):a[y,xs[0]:xs[-1]+1]=255
 for x in range(8):
  ys=np.flatnonzero(a[:,x])
  if len(ys):a[ys[0]:ys[-1]+1,x]=255
 return Image.fromarray(a).resize((16,16),Image.Resampling.NEAREST)
# Reuse exact approved green source cells and native contours.
moss=json.loads((r/'art/poison_moss/registration.json').read_text())['mappings'];terrain={};terrain_records={}
for prefix in ['l3c9C86','l3c9CFE','l3c9DEE','l3c9B96','l3lavaRoom','l3_shaft']:
 for m in moss:
  if m['scope'].startswith(prefix):
   t=int(m['tile'],16)
   if t not in terrain:terrain[t]=cell(m['rule'].split('<tile>')[1].split(','));terrain_records[t]=m['rule']
for pal,ts in observed['9F1A'].items():
 for key in ts:
  t=int(key,16)
  if t==0x700 or(pal=='0F0F0A1A'and t in[0x738,0x739,0x73a,0x73b,0x78c,0x78d,0x796,0x797]):im=empty;kind='nonsolid climb backdrop'
  elif t in terrain:im=terrain[t];kind='approved moss terrain'
  else:continue # stale earlier-room cells in non-visible nametable pages
  tile(t,pal,im,kind,climb)
 for t in ts:
  if int(t,16)not in terrain and t!='0700':continue
  name=f'l3fClimbView_{pal}_{t}';conds.append(f'<condition>{name},tileAtPosition,128,16,{t},{pal}')
  backgrounds.append(f'[{climb}&{name}]<background>Poison_Moss_Ruins_Background.png,1,0,0,11,0,0')
# The head is one coherent image fitted within its complete native OAM footprint.
raw=obj(r/'art/generated/boss3_head.png');cover=Image.new('L',(64,96));d=ImageDraw.Draw(cover)
for y,row in enumerate(layouts['boss_rows']):
 for x,t in enumerate(row):
  if t:d.rectangle((x*16,y*16,x*16+15,y*16+15),fill=255)
fit=None
for h in range(94,79,-1):
 for w in range(62,47,-1):
  im=Image.new('RGBA',(64,96));im.paste(register(raw,(w,h)),((64-w)//2,1));arr=np.array(im)
  if not((arr[:,:,3]>0)&(np.array(cover)==0)).any():
   if fit is None or w*h>fit[0]:fit=(w*h,w,h,im)
assert fit is not None,'Boss head must fit the native missing cells without clipping'
_,bw,bh,head=fit;head.save(art/'boss_head.png')
for y,row in enumerate(layouts['boss_rows']):
 for x,t in enumerate(row):
  if t:tile(t,'FF162535',head.crop((x*16,y*16,x*16+16,y*16+16)),'boss head',boss)
# Native curved shots have staggered 8x8 origins, so fit each whole source into
# its measured union of cells before splitting; never shift individual cells.
raw=Image.open(r/'art/generated/boss3_shots.png').convert('RGBA');aa=np.array(raw.getchannel('A'));xs=np.flatnonzero(np.any(aa>=128,axis=0));groups=np.split(xs,np.flatnonzero(np.diff(xs)>raw.width*.03)+1);assert len(groups)==3
shot_fits=[]
for i,(g,positions)in enumerate(zip(groups,layouts['shot_poses'])):
 part=raw.crop((int(g[0]),0,int(g[-1])+1,raw.height));part=part.crop(part.getchannel('A').point(lambda v:255 if v>=128 else 0).getbbox());W=16 if i==1 else 32;mask=Image.new('L',(W,48));dr=ImageDraw.Draw(mask)
 for x,y in positions.values():dr.rectangle((x*2,y*2,x*2+15,y*2+15),fill=255)
 best=None
 for w in range(W-2,7,-1):
  candidate=register(part,(w,46))
  for x in range(W-w+1):
   im=Image.new('RGBA',(W,48));im.paste(candidate,(x,1))
   if not((np.array(im.getchannel('A'))>0)&(np.array(mask)==0)).any():best=(w,x,im);break
  if best:break
 assert best is not None;w,x,im=best;im.save(art/f'shot_{i}.png');shot_fits.append(dict(size=[W,48],fit_width=w,x=x,native_cells=positions))
 for t,(xx,yy)in positions.items():tile(int(t,16),'FF162535',im.crop((xx*2,yy*2,xx*2+16,yy*2+16)),'curved boss shot '+str(i),boss)
roundshot=Image.open(r/'art/level3_detail/round_shot.png').convert('RGBA')
assert '0694'in shared['088A']
for pal in ['FF162535','FF301116']:tile(0x88a,pal,roundshot,'approved round shot',boss)
orb=Image.new('RGBA',(32,32));orb.paste(register(obj(r/'art/generated/boss3_overdrive.png'),(30,30)),(1,1));orb.save(art/'overdrive.png')
for j,t in enumerate(range(0x88b,0x88f)):tile(t,'FF301116',orb.crop((j%2*16,j//2*16,j%2*16+16,j//2*16+16)),'Overdrive orb',boss)
# The ceiling/floor growths are background-tile boss bodies. Native removal,
# per-cell occlusion and changing palettes still determine their disappearance.
growth=register(obj(r/'art/generated/boss3_growth.png'),(128,48));growth.save(art/'growth_floor.png');top=growth.transpose(Image.Transpose.FLIP_TOP_BOTTOM);top.save(art/'growth_ceiling.png')
podrows=[[0x92c,0x92d,0x92e,0x92f,0x930,0x931,0x932,0x933],[0x934,0x935,0x936,0x937,0x93c,0x93d,0x93e,0x93f],[0x938,0x939,0x93a,0x93b,0x940,0x941,0x942,0x943]]
toprows=[[0x90e,0x90f,0x910,0x911,0x91a,0x91b,0x91c,0x91d],[0x912,0x913,0x914,0x915,0x91e,0x91f,0x920,0x921],[0x916,0x917,0x918,0x919,0x922,0x923,0x924,0x925]]
organic={}
for im,rows in [(growth,podrows),(top,toprows)]:
 for y,row in enumerate(rows):
  for x,t in enumerate(row):organic[t]=im.crop((x*16,y*16,x*16+16,y*16+16))
roots=register(obj(r/'art/generated/boss3_growth.png').crop((300,400,900,700)),(32,32))
for j,t in enumerate(range(0x908,0x90e)):
 im=roots.crop((j%2*16,(j//2)%2*16,j%2*16+16,(j//2)%2*16+16));im.putalpha(hull(t));organic[t]=im
exact=json.loads((art/'terrain_aliases.json').read_text());boss_terrain={};boss_geometry={}
for key,values in exact.items():
 t=int(key,16);source=next((int(v,16)for v in values if int(v,16)in terrain),None)
 if source is not None:boss_terrain[t]=terrain[source];boss_geometry[key]=dict(source_tile=f'{source:04X}',source_rule=terrain_records[source])
for pal,ts in observed['9F92'].items():
 # Normal/full-room native flashes preserve the colored terrain components;
 # only the universal color changes. Fades keep the approved HD silhouettes.
 if pal[2:]in ['091929','0A1A29','081737','071727','0F0A1A']:brightness='1'
 elif pal[2:]in ['0F0919','0F0A19','0F0727']:brightness='.65'
 elif pal[2:]in ['0F0F09','0F0F17']:brightness='.30'
 elif pal[2:]=='0F0F07':brightness='.12'
 elif pal=='0F0F0F0F':brightness='0'
 else:continue
 for key in ts:
  t=int(key,16)
  if not 0x900<=t<0xa00:continue
  if t==0x900:im=empty;kind='empty arena'
  elif t in organic:im=organic[t];kind='living boss growth'
  elif t in boss_terrain:im=boss_terrain[t];kind='approved moss terrain / exact native alias'
  else:continue
  tile(t,pal,im,kind,boss,brightness)
 # Native color flashes stay visible in the open arena. Do not replace the
 # universal red/gold/blue pulse with an unchanged green background.
 if pal.startswith('0F')and brightness!='0':
  for t in ts:
   if int(t,16)not in boss_terrain and int(t,16)not in organic and t!='0900':continue
   name=f'l3fBossView_{pal}_{t}';conds.append(f'<condition>{name},tileAtPosition,128,16,{t},{pal}')
   # Boss heads use the NES behind-background sprite bit: panorama must sit
   # behind those sprites, while the native growth tiles still occlude them.
   backgrounds.append(f'[{boss}&{name}]<background>Poison_Moss_Ruins_Background.png,{brightness},0,0,1,0,0')
# Shared Randy/HUD/weapon copies: native bytes, pose conditions and ordering
# remain exact. Also cover the recorded next-stage arrival, without scenery.
defs={l.split('>')[1].split(',')[0]:l for l in text.splitlines()if l.startswith('<condition>')};aliasdefs={}
def remap(sc,offset,pal=None):
 terms=[]
 for term in sc.split('&')if sc else []:
  neg='!'if term.startswith('!')else '';name=term.lstrip('!');f=defs.get(name,'').split('>')[-1].split(',')
  if len(f)>1 and f[1]=='spriteNearby'and int(f[4],16)<0x100:
   f[4]=f'{int(f[4],16)+offset:04X}';new=f'l3fcopy_{offset:04X}_{pal or "native"}_{name}';f[0]=new
   if pal:f[5]=pal
   aliasdefs[new]='<condition>'+','.join(f);name=new
  terms.append(neg+name)
 return '&'.join(terms)
for line in text.splitlines():
 m=re.fullmatch(r'(?:\[([^]]+)\])?<tile>(.*)',line)
 if not m:continue
 sc,f=m[1]or'',m[2].split(',');t=int(f[1],16)
 if int(f[0])not in[18,19,20,21,22,23,26,27,31]or t>=0x74 or any(k in sc for k in['pause','cardPal','lives']):continue
 for offset in[0x800,0xa00]:
  if f'{t:04X}'not in shared.get(f'{t+offset:04X}',[]):continue
  nf=f.copy();nf[1]=f'{t+offset:04X}';ns=remap(sc,offset);rule=('['+ns+']'if ns else '')+'<tile>'+','.join(nf);aliases.append(rule);alias_records.append(dict(source_rule=line,rule=rule,source_tile=f'{t:04X}',tile=nf[1]))
  if offset!=0x800:continue
  fade={'FF300036':[('FF200F26','.65'),('FF100F16','.30'),('FF000F06','.12')],'FF221136':[('FF120126','.65'),('FF020F16','.30'),('FF0F0F06','.12')],'FF301116':[('FF200106','.65'),('FF100F0F','.30'),('FF000F0F','.12')]}.get(f[2],[])
  for pal,bright in fade:
   q=nf.copy();q[2]=pal;q[5]=bright;ns=remap(sc,offset,pal);aliases.append('['+boss+('&'+ns if ns else '')+']<tile>'+','.join(q))
conds+=list(aliasdefs.values())
# Overdrive announcement and Stage 4 reuse the approved intermission framing.
for name,addr,val in [('l3fGotO',0x21cc,0x30),('l3fGotV',0x21cd,0x37),('l3fGotD',0x21d0,0x23),('l3fGotI',0x21d2,0x28),('l3fGotE',0x21d4,0x24)]:conds.append(f'<condition>{name},ppuMemoryCheckConstant,{addr:04X},==,{val:02X}')
conds.append('<condition>l3fGotRendered,tileAtPosition,96,112,1F30,0F213029')
got='cardPal1&cardPal2&cardPal3&cardRendering&l3fGotRendered&l3fGotO&l3fGotV&l3fGotD&l3fGotI&l3fGotE'
card=Image.open(pack/'Intermission_HD.png').convert('RGBA');d=ImageDraw.Draw(card)
for label,y,size,color in [('SPELL ACQUIRED',164,16,'#cbaa73'),('OVERDRIVE',205,28,'#ffe1ab')]:d.text((256,y),label,font=ImageFont.truetype(str(r/'art/fonts/DejaVuSerif-Bold.ttf'),size),fill=color,anchor='mt',stroke_width=1,stroke_fill='#050e20')
card.save(pack/'Overdrive_Acquired.png');backgrounds.append(f'[{got}]<background>Overdrive_Acquired.png,1,0,0,12,0,0')
for t in[0,*range(0x10,0x40)]:tile(0x1f00+t,'0F213029',empty,'clear native Overdrive text',got)
for i,val in enumerate([0x13,0x1c,0x29],1):conds.append(f'<condition>l3fStage4Pal{i},ppuMemoryCheckConstant,{0x3f00+i:04X},==,{val:02X}')
conds.append('<condition>l3fStage4Rendered,tileAtPosition,96,80,1F34,0F131C29')
stage='l3fStage4Pal1&l3fStage4Pal2&l3fStage4Pal3&cardRendering&stageCardS&stageCardT&stageCardA&stageCardG&stageCardE&stageRandy&stageNumber4&l3fStage4Rendered'
backgrounds += [f'[{stage}]<background>Intermission_HD.png,1,0,0,10,0,0',f'[{stage}]<background>Stage_Title_4.png,1,0,0,30,0,0']
for v in range(10):backgrounds.append(f'[{stage}&stageLives{v}]<background>Stage_Lives_{v}.png,1,0,0,31,0,0')
for t in[0,*range(0x10,0x40)]:tile(0x1f00+t,'0F131C29',empty,'clear native Stage 4 text',stage)
def block(part,items):return '# BEGIN LEVEL3_FINALE '+part+'\n'+'\n'.join(items)+'\n# END LEVEL3_FINALE '+part+'\n'
end=text.index('\n',text.rfind('<img>'))+1;text=text[:end]+block('IMAGES',['<img>Level3_Finale_Tiles_2x.png'])+text[end:]
lines=text.splitlines(keepends=True);first=next(i for i,l in enumerate(lines)if'<tile>'in l or'<background>'in l);lines[first:first]=[block('CONDITIONS',conds),block('MAPPINGS',rules+backgrounds)]
(pack/'hires.txt').write_text(''.join(lines)+block('ALIASES',aliases));atlas.save(pack/'Level3_Finale_Tiles_2x.png');atlas.save(art/'Level3_Finale_Tiles_2x.png')
(art/'registration.json').write_text(json.dumps(dict(tile_rules=len(rules)+len(aliases),conditions=len(conds),background_rules=len(backgrounds),atlas_cells=len(cache),mappings=records,actor_aliases=alias_records,terrain_aliases=boss_geometry,boss_fit=dict(size=[64,96],fit=[bw,bh],x=(64-bw)//2,y=1,clipped_pixels=0),shot_fits=shot_fits,pod_rows=podrows,ceiling_rows=toprows,previous_runtime_art_modified=False,native_gameplay_modified=False),indent=2)+'\n')
print('Level 3 finale:',len(rules)+len(aliases),'rules; green climb, boss, Overdrive and Stage 4 handoff.')
