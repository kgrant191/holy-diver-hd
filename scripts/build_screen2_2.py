"""Stage 2 cave: reuse accepted art, register only new cave/bat identities."""
from pathlib import Path
import hashlib
import json
import numpy as np
from PIL import Image, ImageDraw

root = Path(__file__).resolve().parents[1]
art, gen = root/'art/screen2_2', root/'art/generated'
pack = root/'build/Holy_Diver_(Tr)'
text = (pack/'hires.txt').read_text()
assert text.count('<img>') == 33
scope = 's22Room&s22DataLo&s22DataHi'
conditions = ['<condition>s22Room,memoryCheckConstant,0072,==,10',
              '<condition>s22DataLo,memoryCheckConstant,0078,==,09',
              '<condition>s22DataHi,memoryCheckConstant,0079,==,8B']
rules, metadata, aliases = [], [], []
atlas = Image.new('RGBA', (256, 128))
cache = {}

def register(im, size):
    im = im.convert('RGBA').resize(size, Image.Resampling.LANCZOS)
    alpha = im.getchannel('A').point(lambda v:255 if v>=120 else 0)
    im = im.convert('RGB').quantize(colors=48).convert('RGBA')
    im.putalpha(alpha)
    return im

def tile(t, pal, im, kind):
    assert im.size == (16,16)
    digest = hashlib.sha256(im.tobytes()).hexdigest()
    if digest not in cache:
        n=len(cache);xy=(n%16*16,n//16*16)
        assert xy[1]+16<=atlas.height
        atlas.paste(im,xy);cache[digest]=xy
    x,y=cache[digest]
    rules.append(f'[{scope}]<tile>33,{t:04X},{pal},{x},{y},1,N')
    metadata.append(dict(identity=f'{t:04X}',palette=pal,atlas=[x,y],kind=kind))

# The cave uses the same CHR identities and palettes as the exterior for
# platforms, pools, breakable blocks, and Blizzard snow. Point to that atlas.
exterior_scope = json.loads((root/'art/screen2_1/registration.json').read_text())['scope']
for line in text.splitlines():
    if not line.startswith('['+exterior_scope+']<tile>'):
        continue
    values=line.split('<tile>')[1].split(',')
    t=int(values[1],16)
    if 0x32e<=t<=0x34d or t in [0x274,0x247,0x248,0x24e,0x24f]:
        aliases.append(line.replace(exterior_scope,scope,1))

# In this bank the 24 ghoul tiles moved six slots earlier. The native bytes
# are exact copies; translate both tile identities and pose-anchor probes.
nave_scope=json.loads((root/'art/screen1_3/registration.json').read_text())['scope']
anchors={}
for line in text.splitlines():
    if line.startswith('<condition>ghoulStanding'):
        fields=line[len('<condition>'):].split(',')
        name=fields[0];fields[0]='s22'+name;fields[4]=f'{int(fields[4],16)+0x1fa:04X}'
        conditions.append('<condition>'+','.join(fields));anchors[name]=fields[0]
for line in text.splitlines():
    if not line.startswith('['+nave_scope) or '<tile>28,' not in line:
        continue
    before,after=line.split('<tile>');fields=after.split(',');t=int(fields[1],16)
    if not 0x94<=t<=0xab:continue
    fields[1]=f'{t+0x1fa:04X}'
    before=before.replace(nave_scope,scope,1)
    for old,new in anchors.items():before=before.replace(old,new)
    aliases.append(before+'<tile>'+','.join(fields))

for pal in ['0F071737','0F061627','0F041625','0F060616','0F161606','0F122131']:
    tile(0x300,pal,Image.new('RGBA',(16,16)),'cave space')

patterns=json.loads((art/'native_terrain.json').read_text())
def mask(t):
    b=bytes.fromhex(patterns[f'{t:04X}'])
    im=Image.new('L',(8,8))
    im.putdata([255 if ((b[y]|b[y+8])>>(7-x))&1 else 0 for y in range(8)for x in range(8)])
    return im.resize((16,16),Image.Resampling.NEAREST)

rock_source=Image.open(gen/'screen2_2_rock_generated.png')
cx,cy=rock_source.width//2,rock_source.height//2
rock=register(rock_source.crop((cx-128,cy-128,cx+128,cy+128)),(32,32))
gold=Image.open(root/'art/layers/50_floor.png').convert('RGBA').crop((256,880,320,912))
gold=register(gold,(32,32))
def outline_mask(ts, hanging):
    big=Image.new('L',(32,16*(len(ts)//2)))
    for i,t in enumerate(ts):big.paste(mask(t),(i%2*16,i//2*16))
    a=np.array(big)
    for x in range(a.shape[1]):
        ys=np.where(a[:,x]>0)[0]
        if len(ys):
            if hanging:a[:ys[-1]+1,x]=255
            else:a[ys[0]:,x]=255
    return Image.fromarray(a)
gold_edge=outline_mask(list(range(0x35b,0x35f)),True)
red_start=outline_mask(list(range(0x35f,0x363)),False)
red_end=outline_mask([0x367,0x368],True)
for t in range(0x35b,0x369):
    material=gold if t<0x35f else rock
    first=0x35b if t<0x35f else 0x35f if t<0x363 else 0x363 if t<0x367 else 0x367
    n=t-first;x=(n%2)*16;y=(n//2)*16
    cell=material.crop((x,y,x+16,y+16))
    shape=gold_edge if t<0x35f else red_start if t<0x363 else red_end if t>=0x367 else None
    if shape is not None:cell.putalpha(shape.crop((x,y,x+16,y+16)))
    tile(t,'0F071737' if t<0x35f else '0F061627',cell,
         'gold ceiling edge' if t<0x35f else 'burgundy cave formation')
for t in [0x3a1,0x3a2]:
    x=(t-0x3a1)*16
    cell=gold.crop((x,0,x+16,16));cell.putalpha(mask(t))
    tile(t,'0F071737',cell,'native platform underside')

# The vertical falls use the accepted pool artwork, turned so its mineral
# streaks run down the shaft. Native palettes still control lava versus ice.
for name,pals in [('lava',['0F161606','0F060616']),('ice',['0F122131'])]:
    im=Image.open(root/f'art/screen2_1/{name}_registered.png').convert('RGBA')
    im=im.crop((0,16,32,48)).transpose(Image.Transpose.ROTATE_90)
    for phase,pal in enumerate(pals):
        variant=im.copy()
        if phase:
            a=np.array(variant);a[:,:,:3]=(a[:,:,:3]*.83).astype('uint8');variant=Image.fromarray(a)
        for t,(x,y) in zip(range(0x389,0x38f),[(0,0),(16,0),(0,0),(16,0),(0,16),(16,16)]):
            tile(t,pal,variant.crop((x,y,x+16,y+16)),name+' fall')

source=Image.open(gen/'screen2_2_bat_generated.png').convert('RGBA')
split=round(source.width*.3)
raws=[]
for box in [(0,0,split,source.height),(split,0,source.width,source.height)]:
    im=source.crop(box);alpha=im.getchannel('A').point(lambda v:255 if v>=120 else 0)
    im.putalpha(alpha);raws.append(im.crop(im.getbbox()))
folded=Image.new('RGBA',(32,48));folded.paste(register(raws[0],(28,46)),(2,1))
spread=register(raws[1],(62,46))
# Fit both wing tips in the upper two native OAM rows; the bottom row has
# only the central two cells. Register the connected lower body separately.
arr=np.array(spread);outer=np.r_[np.arange(0,15),np.arange(47,62)]
cut=int(np.where(np.any(arr[:,outer,3]>0,axis=1))[0].max())+1
opened=Image.new('RGBA',(64,48))
opened.paste(register(spread.crop((0,0,62,cut)),(62,32)),(1,0))
opened.paste(register(spread.crop((0,cut,62,46)),(62,16)),(1,32))
cover=Image.new('L',(64,48));d=ImageDraw.Draw(cover)
d.rectangle((0,0,63,31),fill=255);d.rectangle((16,32,47,47),fill=255)
clipped=int(((np.array(opened)[:,:,3]>0)&(np.array(cover)==0)).sum())
assert clipped==0,clipped
folded.save(art/'bat_folded.png');opened.save(art/'bat_open.png')
for n,t in enumerate(range(0x2b0,0x2b6)):
    x=n%2*16;y=n//2*16
    tile(t,'FF10300C',folded.crop((x,y,x+16,y+16)),'bat folded')
layout=[(0,0,0xa6),(1,0,0xa7),(2,0,0xa8),(3,0,0xa9),
        (0,1,0xaa),(1,1,0xab),(2,1,0xac),(3,1,0xad),(1,2,0xae),(2,2,0xaf)]
for x,y,t in layout:tile(t+0x200,'FF10300C',opened.crop((x*16,y*16,x*16+16,y*16+16)),'bat open')
shot=Image.new('RGBA',(16,16))
shot.paste(register(Image.open(root/'art/boss1/boss_fireball_registered.png'),(12,12)),(2,2))
tile(0x2b6,'FF301116',shot,'shared fireball source')

bg=Image.open(gen/'screen2_2_background_generated.png').convert('RGB').resize((1024,480),Image.Resampling.LANCZOS)
a=np.array(bg).astype(float);edge=(a[:,0]+a[:,-1])/2
for x in range(24):
    w=(1-x/24)**2;a[:,x]=a[:,x]*(1-w)+edge*w;a[:,-1-x]=a[:,-1-x]*(1-w)+edge*w
bg=Image.fromarray(a.astype('uint8'))
panorama=Image.new('RGB',(8704,480))
for x in range(0,8704,1024):panorama.paste(bg,(x,0))
panorama.save(pack/'Stage2_Cave_Background.png')
# Match actual rendered terrain at this screen point, not the CPU's delayed
# PPUMASK shadow. The multiple rules are alternatives for a scrolling ceiling.
backgrounds=[]
guards=[(t,'0F071737')for t in range(0x32e,0x341)]+[(t,'0F071737')for t in range(0x35b,0x35f)]+[(t,'0F061627')for t in range(0x35f,0x369)]
guards += [(t,pal)for t in range(0x389,0x38f)for pal in ['0F161606','0F060616','0F122131']]
for i,(t,pal)in enumerate(guards):
    name=f's22Rendered{i}'
    conditions.append(f'<condition>{name},tileAtPosition,128,16,{t:04X},{pal}')
    backgrounds.append(f'[{scope}&{name}]<background>Stage2_Cave_Background.png,1,1,1,11,0,0')

atlas.save(art/'Stage2_Cave_Tiles_2x.png');atlas.save(pack/'Stage2_Cave_Tiles_2x.png')
def section(kind,lines):return '# BEGIN SCREEN2_2 '+kind+'\n'+'\n'.join(lines)+'\n# END SCREEN2_2 '+kind+'\n'
end=text.index('\n',text.rfind('<img>'))+1
text=text[:end]+section('IMAGES',['<img>Stage2_Cave_Tiles_2x.png'])+text[end:]
lines=text.splitlines(keepends=True)
first=next(i for i,line in enumerate(lines)if '<tile>'in line or '<background>'in line)
lines[first:first]=[section('CONDITIONS',conditions),section('MAPPINGS',aliases+rules+backgrounds)]
(pack/'hires.txt').write_text(''.join(lines))
(art/'registration.json').write_text(json.dumps(dict(scope=scope,shared_aliases=len(aliases),new_tile_rules=len(rules),
    atlas_cells=len(cache),mappings=metadata,bat_clipped_pixels=clipped,bat_open_source_split=cut,
    background_rules=len(backgrounds),native_collision_modified=False,previous_artwork_modified=False),indent=2)+'\n')
print('Stage 2 cave:',len(aliases),'shared aliases,',len(rules),'new tile mappings')
