"""Register Golden Temple scenery and shared Overdrive graphics at native scale."""
from pathlib import Path
import hashlib, json, re
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageEnhance

root=Path(__file__).resolve().parents[1]
pack=root/'build/Holy_Diver_(Tr)'; art=root/'art/level4'; gen=root/'art/generated'
text=(pack/'hires.txt').read_text(); images=[l[5:] for l in text.splitlines() if l.startswith('<img>')]
assert len(images)==47, 'Golden Temple must follow approved 0.15.0'
atlas=Image.new('RGBA',(512,512)); cache={}; rules=[]; conditions=[]; backgrounds=[]; records=[]
patterns={int(k,16):bytes.fromhex(v) for k,v in json.loads((art/'native_patterns.json').read_text()).items()}
observed=json.loads((art/'observed_backgrounds.json').read_text())
empty=Image.new('RGBA',(16,16))

def reg(im,size,colors=96):
    im=im.convert('RGBA').resize(size,Image.Resampling.LANCZOS)
    alpha=im.getchannel('A').point(lambda v:255 if v>=128 else 0)
    im=im.convert('RGB').quantize(colors=colors).convert('RGBA'); im.putalpha(alpha)
    return im

def tile(t,pal,im,kind,scope='',brightness='1'):
    assert im.size==(16,16)
    key=hashlib.sha256(im.tobytes()).hexdigest()
    if key not in cache:
        n=len(cache); xy=(n%32*16,n//32*16); assert xy[1]<512
        cache[key]=xy; atlas.paste(im,xy)
    x,y=cache[key]; rule=('['+scope+']' if scope else '')+f'<tile>47,{t:04X},{pal},{x},{y},{brightness},N'
    rules.append(rule); records.append(dict(tile=f'{t:04X}',palette=pal,xy=[x,y],kind=kind,scope=scope,rule=rule))

def hull(t):
    b=patterns[t]; a=np.array([[255 if ((b[y]|b[y+8])>>(7-x))&1 else 0 for x in range(8)]for y in range(8)],dtype=np.uint8)
    for y in range(8):
        xs=np.flatnonzero(a[y])
        if len(xs): a[y,xs[0]:xs[-1]+1]=255
    for x in range(8):
        ys=np.flatnonzero(a[:,x])
        if len(ys): a[ys[0]:ys[-1]+1,x]=255
    return Image.fromarray(a).resize((16,16),Image.Resampling.NEAREST)

scopes={}
for room,mode in [('A865',0x1c),('AA09',8),('AA81',8)]:
    prefix='temple'+room
    for suffix,addr,val in [('Mode',0x72,mode),('Lo',0x78,int(room,16)&255),('Hi',0x79,int(room,16)>>8)]:
        conditions.append(f'<condition>{prefix}{suffix},memoryCheckConstant,{addr:04X},==,{val:02X}')
    scopes[room]='&'.join(prefix+s for s in ['Mode','Lo','Hi'])

# Backdrops stay behind native foreground geometry and actor priority.
for source,name,bright in [('temple_exterior.png','Golden_Temple_Exterior.png',.64),('temple_interior.png','Golden_Temple_Interior.png',.72)]:
    im=reg(Image.open(gen/source),(768,480),128)
    im=ImageEnhance.Brightness(im).enhance(bright); im.save(pack/name)

raw=Image.open(gen/'temple_masonry.png').convert('RGBA')
brick=reg(raw.crop((188,0,350,310)),(32,32))
brick2=reg(raw.crop((352,0,505,310)),(32,32))
wall=reg(raw,(64,64))
interior=Image.open(gen/'temple_interior.png').convert('RGBA')
pillar=Image.open(gen/'temple_column.png').convert('RGBA')
shaft=reg(pillar.crop((440,300,582,500)),(32,64))
cap=reg(pillar.crop((334,12,691,173)),(64,16))
neck=reg(pillar.crop((440,173,582,240)),(32,16))
column={}
for i,t in enumerate(range(0xb03,0xb07)): column[t]=cap.crop((i*16,0,i*16+16,16))
for t,x in [(0xb07,0),(0xb08,16)]: column[t]=neck.crop((x,0,x+16,16))
for t,x in [(0xb09,0),(0xb0a,16),(0xb0b,16),(0xb14,0),(0xb15,16),(0xb16,0),(0xb17,16),(0xb1a,0),(0xb1b,16),(0xb1e,0),(0xb1f,16),*[(0xb34+i,(i%2)*16)for i in range(6)]]:
    column[t]=shaft.crop((x,16,x+16,32))
for t in column:
    column[t].putalpha(Image.new('L',(16,16),255) if 0xb07<=t<=0xb1f else hull(t))

# Two complete masonry blocks retain the native staggered floor layout.
terrain={}
for i,t in enumerate(range(0xb3a,0xb42)):
    src=brick if i%4<2 else brick2; x=(i%2)*16; y=i//4*16
    terrain[t]=src.crop((x,y,x+16,y+16))
for i,t in enumerate(range(0xb42,0xb4a)):
    x=(i%2)*16; y=i//4*16; terrain[t]=(brick2 if i%4<2 else brick).crop((x,y,x+16,y+16))
for i,t in enumerate(range(0xb4e,0xb54)):
    x=(i%2)*16; y=((i//2)%2)*16; terrain[t]=brick.crop((x,y,x+16,y+16))
for t in [*range(0xb78,0xb7c),*range(0xb80,0xb89)]:
    x=(t%2)*16;y=((t//2)%2)*16;terrain[t]=brick.crop((x,y,x+16,y+16))
for t in terrain:
    # Mortar inside a full solid block is an opaque recess, not open scenery.
    if 0xb80<=t<=0xb87: terrain[t].putalpha(hull(t))
    else: terrain[t].putalpha(Image.new('L',(16,16),255))
for rows in [[[0xb83,0xb82],[0xb81,0xb80]],[[0xb87,0xb86],[0xb85,0xb84]]]:
    # Join the whole stair contour before cutting its native cells. Filling
    # individual cells leaves cracks at internal boundaries of a solid step.
    a=np.block([[np.array(hull(t))for t in row]for row in rows])
    for xx in range(32):
        ys=np.flatnonzero(a[:,xx])
        if len(ys):a[ys[0]:ys[-1]+1,xx]=255
    for yy,row in enumerate(rows):
        for xx,t in enumerate(row):terrain[t].putalpha(Image.fromarray(a[yy*16:yy*16+16,xx*16:xx*16+16]))

# The entrance opening remains dark as soon as its left jamb appears.
for i in range(1,5):
    for left in [0xb57,0xb58]:
        name=f'templeDoor{i}_{left:04X}'; bound=f'templeDoorBound{i}'
        conditions.append(f'<condition>{name},tileNearby,{-8*i},0,{left:04X},0F071737')
        if left==0xb57: conditions.append(f'<condition>{bound},positionCheckX,>=,{i*8}')
        tile(0xb00,'0F071737',Image.new('RGBA',(16,16),'#060a16'),'dark entrance',scopes['A865']+'&'+name+'&'+bound)

geometry={}
for room,scope in scopes.items():
    for pal,ts in observed[room].items():
        if not pal.startswith('0F'): continue
        for key in ts:
            t=int(key,16)
            if not 0xb00<=t<0xc00: continue
            if t in terrain:
                im=terrain[t];kind='native collision masonry'
            elif room=='A865' and t in column and pal in ['0F071737','0F071703','0F072830']:
                im=column[t];kind='outdoor gold column'
            elif room=='A865' and (0xb54<=t<=0xb68 or 0xbdf<=t<=0xbe2):
                im=wall.crop(((t%4)*16,((t//4)%4)*16,(t%4+1)*16,((t//4)%4+1)*16));kind='temple entrance facade'
                portal_rows=[[0xbdf,0xbe0,0xbe1,0xbe2],[0xb5b,0xb5c,0xb63,0xb64],[0xb5d,0xb5e,0xb65,0xb66],[0xb5f,0xb60,0xb67,0xb68]]
                portal=reg(interior.crop((228,120,526,740)),(64,64))
                for yy,row in enumerate(portal_rows):
                    if t in row:
                        xx=row.index(t);im=portal.crop((xx*16,yy*16,xx*16+16,yy*16+16));break
            elif t<0xb78 or t in [0xb7c,0xb7d,0xb7e,0xb7f,0xb8c,0xb8d,0xb96,0xb97,0xb9a,0xb9b]:
                im=empty;kind='nonsolid scenery reveal'
            else: continue
            tile(t,pal,im,kind,scope)
            if t in terrain: geometry[key]=np.array(im.getchannel('A')).tolist()
        # A live rendered tile guard excludes menus, blank transitions and cards.
        if pal not in ['0F031323','0F071737','0F072830','0F073703','0F1B2B3B','0F041424','0F001020','0F172737','0F071723','0F071703']:continue
        for key in ts:
            if not key.startswith('0B'):continue
            name=f'templeView{room}_{key}_{pal}'
            conditions.append(f'<condition>{name},tileAtPosition,128,16,{key},{pal}')
            file='Golden_Temple_Exterior.png' if room=='A865' else 'Golden_Temple_Interior.png'
            backgrounds.append(f'[{scope}&{name}]<background>{file},1,0,0,1,0,0')

# Correct V, while keeping Y in PLAYER and the numeric zero in MP costs.
menu='pauseScreen&pauseMagicRow&pausedPalette'
font=ImageFont.truetype(str(root/'art/fonts/DejaVuSerif-Bold.ttf'),14)
for char,t in [('V',0x96c),('O',0x949)]:
    im=Image.new('RGBA',(16,16));ImageDraw.Draw(im).text((8,8),char,font=font,anchor='mm',fill='#f4deb0')
    scope=menu
    if char=='O':
        conditions += ['<condition>overdriveMenuX,originPositionCheckX,==,120','<condition>overdriveMenuY,originPositionCheckY,==,120']
        scope+='&overdriveMenuX&overdriveMenuY'
    tile(t,'0F072830',im,'Overdrive menu '+char,scope)

# The gargoyle's crescent uses three native growing-wave heights. Native OAM
# continues to control placement, horizontal mirroring and cadence.
source=Image.open(gen/'temple_wave.png').convert('RGBA')
source=source.crop(source.getchannel('A').point(lambda v:255 if v>=160 else 0).getbbox())
wave=reg(source,(16,64),48);wave.save(art/'gargoyle_wave.png')
pieces={0xacb:wave.crop((0,0,16,16)),0xacc:wave.crop((0,16,16,32)),0xacd:wave.crop((0,32,16,48)),0xace:wave.crop((0,48,16,64)),0xacf:reg(wave.crop((0,16,16,48)),(16,16),48)}
aliases=json.loads((art/'wave_aliases.json').read_text())
for t,im in pieces.items():
    for key in aliases[f'{t:04X}']:
        for pal in ['FF300036','FF221136']:tile(int(key,16),pal,im,'gargoyle wave')

def obj(name):
    im=Image.open(gen/name).convert('RGBA')
    return im.crop(im.getchannel('A').point(lambda v:255 if v>=160 else 0).getbbox())

poses=[]
def sprite(name,im,layout,palette):
    im.save(art/(name+'.png'))
    for key,x,y in layout:
        tile(int(key,16),palette,im.crop((x*2,y*2,x*2+16,y*2+16)),name)
    poses.append(dict(name=name,size=list(im.size),layout=layout,palette=palette))

# Whole native actors retain their OAM footprint; no independently shifted limbs.
layouts=json.loads((art/'native_sprite_layouts.json').read_text())
fits={}
def fit(name,raw,layout,size):
    mask=Image.new('L',size);dr=ImageDraw.Draw(mask)
    for key,x,y in layout:dr.rectangle((x*2,y*2,x*2+15,y*2+15),fill=255)
    allowed=np.array(mask)>0; best=None
    for h in range(size[1]-2,size[1]-15,-1):
        for w in range(size[0]-2,size[0]-19,-1):
            scaled=reg(raw,(w,h))
            for y in range(1,min(5,size[1]-h+1)):
                for x in range(1,min(5,size[0]-w+1)):
                    im=Image.new('RGBA',size);im.paste(scaled,(x,y))
                    if not ((np.array(im.getchannel('A'))>0)&~allowed).any():
                        if best is None or w*h>best[0]:best=(w*h,w,h,x,y,im)
        if best and best[0]>=((size[0]-2)*(h-1)):break
    assert best is not None, name+' cannot fit native union without clipping'
    _,w,h,x,y,im=best;fits[name]=dict(size=size,fit=[w,h],offset=[x,y],clipped_pixels=0)
    return im,(w,h,x,y)

base=Image.new('RGBA',(48,48));base.paste(reg(obj('temple_boulder.png'),(44,44)),(2,2))
for i,start in enumerate([0xa9a,0xaa3,0xaac]):
    im=base.rotate(i*120,Image.Resampling.BICUBIC)
    im.putalpha(im.getchannel('A').point(lambda v:255 if v>=128 else 0))
    sprite('boulder_'+str(i),im,[(f'{start+y*3+x:04X}',x*8,y*8)for y in range(3)for x in range(3)],'FF172737')
for t in [0xa97,0xa98,0xa99]:
    im=reg(obj('temple_boulder.png'),(16,16));im.putalpha(hull(t));tile(t,'FF172737',im,'boulder fragments')

dragon0=next(p for p in layouts['dragon'] if len(p['layout'])==15 and any(t=='0AB5'for t,x,y in p['layout']))
dragon1=next(p for p in layouts['dragon'] if len(p['layout'])==15 and any(t=='0AC4'for t,x,y in p['layout']))
raw=Image.open(gen/'temple_gargoyle.png').convert('RGBA')
box=raw.getchannel('A').point(lambda v:255 if v>=160 else 0).getbbox();raw=raw.crop(box)
gargoyle,placement=fit('gargoyle',raw,dragon0['layout'],[80,64])
w,h,x,y=placement
alt_raw=Image.open(gen/'temple_gargoyle_alt.png').convert('RGBA').crop(box)
alt=Image.new('RGBA',(80,64));alt.paste(reg(alt_raw,(w,h)),(x,y))
# Native shared cells and every head/body pixel stay exact across wingbeats.
a=np.array(alt);b=np.array(gargoyle);stable=np.ones((64,80),dtype=bool)
for key,xx,yy in dragon1['layout']:
    if int(key,16)>=0xac4 and xx>=24:stable[yy*2:yy*2+16,xx*2:xx*2+16]=False
a[stable]=b[stable];alt=Image.fromarray(a)
sprite('gargoyle_0',gargoyle,dragon0['layout'],'FF26173A')
# Shared native identities were already registered by the first pose.
sprite('gargoyle_1',alt,[(t,x,y)for t,x,y in dragon1['layout']if int(t,16)>=0xac4],'FF26173A')
guardian0=layouts['knight'][0]
guardian,_=fit('guardian',obj('temple_guardian.png'),guardian0['layout'],[64,64])
sprite('guardian',guardian,guardian0['layout'],'FF003008')

wheel=Image.new('RGBA',(32,32));wheel.paste(reg(obj('overdrive_orb.png'),(30,30)),(1,1))
sprite('overdrive_orb',wheel,[(f'{0xa8a+y*2+x:04X}',x*8,y*8)for y in range(2)for x in range(2)],'FF301116')
# Native-identical banks reuse the same Overdrive orb after this level.
for key,aliases in json.loads((art/'overdrive_aliases.json').read_text()).items():
    i=int(key,16)-0xa8a;xx=i%2*16;yy=i//2*16
    for alias in aliases:
        if alias!=key:tile(int(alias,16),'FF301116',wheel.crop((xx,yy,xx+16,yy+16)),'Overdrive orb alias')
sprite('moving_platform',brick,[(f'{0xaf8+y*2+x:04X}',x*8,y*8)for y in range(2)for x in range(2)],'FF172737')
# Small returning crescent projectile reuses the approved curved-shot source.
shot=reg(Image.open(root/'art/level3_finale/shot_0.png'),(16,16));tile(0xafc,'FF301116',shot,'shared curved shot material')

source_lines=text.splitlines(); shared=[]
for pair in json.loads((art/'actor_aliases.json').read_text()):
    src,dst=pair['source'],pair['tile']
    line=next(l for l in source_lines if l.startswith('<tile>')and l.split('<tile>')[1].split(',')[1]==src)
    f=line.split('<tile>')[1].split(',');xx,yy=map(int,f[3:5]);im=Image.open(pack/images[int(f[0])]).convert('RGBA').crop((xx,yy,xx+16,yy+16))
    tile(int(dst,16),f[2],im,'approved actor reuse');shared.append(dict(source_rule=line,tile=dst))

def block(part,lines):return '# BEGIN GOLDEN_TEMPLE '+part+'\n'+'\n'.join(lines)+'\n# END GOLDEN_TEMPLE '+part+'\n'
end=text.index('\n',text.rfind('<img>'))+1
text=text[:end]+block('IMAGES',['<img>Golden_Temple_Tiles_2x.png'])+text[end:]
lines=text.splitlines(keepends=True);first=next(i for i,l in enumerate(lines)if '<tile>' in l or '<background>' in l)
lines[first:first]=[block('CONDITIONS',conditions),block('MAPPINGS',rules+backgrounds)]
(pack/'hires.txt').write_text(''.join(lines));atlas.save(pack/'Golden_Temple_Tiles_2x.png');atlas.save(art/'Golden_Temple_Tiles_2x.png')
(art/'registration.json').write_text(json.dumps(dict(mappings=records,geometry=geometry,tile_rules=len(rules),conditions=len(conditions),background_rules=len(backgrounds),atlas_cells=len(cache),scopes=scopes,poses=poses,actor_fits=fits,shared_actors=shared),indent=2)+'\n')
print('Golden Temple:',len(rules),'tile rules;',len(backgrounds),'rendered backdrop guards;',len(cache),'atlas cells')
