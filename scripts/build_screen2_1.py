"""Stage 2 exterior: native tile geometry, palette-driven ice, shared pickups."""
from pathlib import Path
import hashlib
import json
import re
from PIL import Image, ImageDraw
import numpy as np

root = Path(__file__).resolve().parents[1]
art = root / 'art/screen2_1'
gen = root / 'art/generated'
pack = root / 'build/Holy_Diver_(Tr)'
text = (pack / 'hires.txt').read_text()
assert text.count('<img>') == 32
scope = 's21Room&s21DataLo&s21DataHi'
background_scope = scope + '&s21SkyPalette&s21SkyRendered'
conditions = [
    '<condition>s21Room,memoryCheckConstant,0072,==,18',
    '<condition>s21DataLo,memoryCheckConstant,0078,==,A1',
    '<condition>s21DataHi,memoryCheckConstant,0079,==,89',
    '<condition>s21SkyPalette,ppuMemoryCheckConstant,3F09,==,15',
    '<condition>s21SkyRendered,tileAtPosition,128,16,0301,0F150426',
]
atlas = Image.new('RGBA', (512, 256))
rules, mappings, cached = [], [], {}

def register(im, size):
    im = im.convert('RGBA').resize(size, Image.Resampling.LANCZOS)
    alpha = im.getchannel('A').point(lambda a: 255 if a >= 120 else 0)
    im = im.convert('RGB').quantize(colors=48).convert('RGBA')
    im.putalpha(alpha)
    return im

def obj(im):
    im = im.convert('RGBA')
    im.putalpha(im.getchannel('A').point(lambda a: 255 if a >= 120 else 0))
    return im.crop(im.getbbox())

def tile(identity, palette, im, kind, condition=scope):
    assert im.size == (16, 16)
    digest = hashlib.sha256(im.tobytes()).hexdigest()
    if digest not in cached:
        n = len(cached); x, y = n % 32 * 16, n // 32 * 16
        assert y + 16 <= atlas.height
        atlas.paste(im, (x, y)); cached[digest] = (x, y)
    x, y = cached[digest]
    rules.append(f'[{condition}]<tile>32,{identity:04X},{palette},{x},{y},1,N')
    mappings.append(dict(identity=f'{identity:04X}', palette=palette,
                         atlas=[x, y], kind=kind, scope=condition))

def grid(rows, pal, im, kind):
    for y, row in enumerate(rows):
        for x, t in enumerate(row):
            tile(0x300+t, pal, im.crop((x*16, y*16, x*16+16, y*16+16)), kind)

# The original distant clouds/forest are non-solid. Only those identities are
# cleared; foreground ledges and lava remain native nametable-bound tiles.
empty = Image.new('RGBA', (16, 16))
for pal in ['0F071737', '0F060616', '0F161606', '0F122131', '0F150426', '0F162726']:
    tile(0x300, pal, empty, 'empty background')
for t in range(1, 0x16):
    tile(0x300+t, '0F150426', empty, 'distant sky/clouds')
for t in range(0x16, 0x2e):
    tile(0x300+t, '0F162726', empty, 'distant scorched forest')

bg = Image.open(gen/'screen2_1_background_generated.png').convert('RGB').resize((1024,480), Image.Resampling.LANCZOS)
# Match seam colors over a narrow margin, then repeat with native full-speed
# scrolling. The extra viewport prevents a black edge at the last room tile.
a = np.array(bg).astype(float)
edge = (a[:,0] + a[:,-1])/2
for x in range(24):
    weight = (1-x/24)**2
    a[:,x] = a[:,x]*(1-weight)+edge*weight
    a[:,-1-x] = a[:,-1-x]*(1-weight)+edge*weight
bg = Image.fromarray(a.astype('uint8'))
panorama = Image.new('RGB', (8704,480))
for x in range(0,8704,1024): panorama.paste(bg,(x,0))
panorama.save(pack/'Stage2_Exterior_Background.png')

# Reuse the approved gold ground texture. Native 2E/2F are the cap; the
# 30..33 quartet repeats below it, exactly following each original platform.
floor = Image.open(root/'art/layers/50_floor.png').convert('RGBA').crop((256,864,320,928))
cap = register(floor.crop((0,0,64,16)), (32,16))
body = register(floor.crop((0,16,64,48)), (32,32))
grid([[0x2e,0x2f]], '0F071737', cap, 'approved gold platform cap')
grid([[0x30,0x31],[0x32,0x33]], '0F071737', body, 'approved gold rock body')

# The far-right cliff reuses approved rock texture. Native masks preserve the
# stepped silhouette and stalactites; the doorway remains a dark opening.
cliff=register(floor.crop((0,16,64,48)),(64,32))
grid([[0x35,0x36,0x37,0x38],[0x39,0x3a,0x3b,0x3c]],'0F071737',cliff,'exit cliff rock')
for key,data in json.loads((art/'native_cliff_edges.json').read_text()).items():
    t=int(key,16);bits=bytes.fromhex(data);mask=Image.new('L',(8,8))
    mask.putdata([255 if ((bits[y]|bits[y+8])>>(7-x))&1 else 0 for y in range(8) for x in range(8)])
    cell=cliff.crop(((t%4)*16,0,(t%4+1)*16,16))
    cell.putalpha(mask.resize((16,16),Image.Resampling.NEAREST))
    if t in [0x4b,0x4c,0x4d]:
        # These are the cave ceiling, so cutouts expose its black interior.
        ceiling=Image.new('RGBA',(16,16),'#000000')
        ceiling.alpha_composite(cell)
        cell=ceiling
    tile(0x300+t,'0F071737',cell,'native cliff edge/stalactite')
for i in range(4):
    for row,left in [(0,0x338),(1,0x33c)]:
        ln=f's21DoorL{i}_{row}';xn=f's21DoorX{i}_{row}'
        conditions.extend([f'<condition>{ln},tileNearby,{-8*(i+1)},0,{left:04X},0F071737',
                           f'<condition>{xn},positionCheckX,>=,{8*(i+1)}'])
        tile(0x300,'0F071737',Image.new('RGBA',(16,16),'#000000'),'dark cave opening',scope+'&'+ln+'&'+xn)
# The left jamb remains visible when the doorway first enters from the right.
# Requiring the offscreen right jamb delayed the dark fill until full reveal.
# X bounds prevent tileNearby from wrapping the probe across the screen edge.
# Specific doorway tiles must precede the generic transparent zero tile.
rules.sort(key=lambda line: 0 if 's21Door' in line else 1)

# The exact native palette selects liquid/solid artwork. No emulated frame
# timer, RAM write, collision patch or guessed thaw duration is introduced.
pools = Image.open(gen/'screen2_1_pools_generated.png').convert('RGBA')
pool_report = {}
for i, (name, pals) in enumerate([
    ('lava',['0F161606','0F060616']), ('ice',['0F122131'])
]):
    raw = pools.crop((i*pools.width//2,0,(i+1)*pools.width//2,pools.height))
    surface = register(raw.crop((0,0,raw.width,raw.height//3)), (32,16))
    repeat = register(raw.crop((0,raw.height//3,raw.width,raw.height*2//3)), (32,32))
    for phase,pal in enumerate(pals):
        # Native lava swaps its two red shades. Preserve the pulse using the
        # same geometry and a modest brightness variation of the source art.
        surf,fill=surface.copy(),repeat.copy()
        if phase:
            for im in (surf,fill):
                data=np.array(im);data[:,:,:3]=(data[:,:,:3].astype(float)*.83).astype('uint8');im.paste(Image.fromarray(data))
        grid([[0x45,0x44]], pal, surf, name+' surface')
        grid([[0x43,0x42],[0x41,0x34]], pal, fill, name+' body')
    preview=Image.new('RGBA',(32,48));preview.paste(surface,(0,0));preview.paste(repeat,(0,16));preview.save(art/(name+'_registered.png'))
    pool_report[name] = pals

block=register(Image.open(gen/'screen2_1_block_generated.png'),(32,32))
grid([[0x47,0x48],[0x49,0x4a]],'0F071737',block,'breakable gold block')
block.save(art/'gold_block_registered.png')
snow=register(obj(Image.open(gen/'screen2_1_snow_generated.png')),(14,14))
flake=Image.new('RGBA',(16,16));flake.paste(snow,(1,1))
tile(0x274,'FF301116',flake,'Blizzard snow crystal')
flake.save(art/'snow_crystal_registered.png')

poses=json.loads((art/'native_poses.json').read_text())
creature=Image.open(gen/'screen2_1_pulsing_rock_generated.png').convert('RGBA')
for i,pose in enumerate(poses[:3]):
    raw=obj(creature.crop((i*creature.width//3,0,(i+1)*creature.width//3,creature.height)))
    im=register(raw,(48,48));im.save(art/f'lava_creature_{i}.png')
    for x,y,t in pose['tiles']:
        tile(0x200+t,'FF160636',im.crop((x*2,y*2,x*2+16,y*2+16)),'lava creature pose '+str(i))

# Unflipped sprites travel LEFT (measured world-X delta -1/-2 per frame).
# Fit the complete demon to the common OAM footprint; preserve its body in all
# phases and change only the native wing cells plus the held-arrow cells.
demon=Image.open(gen/'screen2_1_demon_generated.png').convert('RGBA')
# obj() crops, so retain the same absolute alpha bounds for the alternate pose.
source_box=demon.getchannel('A').point(lambda a:255 if a>=120 else 0).getbbox()
base=Image.new('RGBA',(64,48))
base.paste(register(demon.crop(source_box),(46,39)),(2,9))
wing=Image.open(gen/'screen2_1_demon_wing_generated.png').convert('RGBA')
assert wing.size==demon.size
alternate=Image.new('RGBA',(64,48))
alternate.paste(register(wing.crop(source_box),(46,39)),(2,9))
mask=Image.new('L',(64,48));d=ImageDraw.Draw(mask)
for x,y,t in poses[-1]['tiles']:
    if y<24:d.rectangle((x*2,y*2,x*2+15,y*2+15),fill=255)
a=np.array(base);clipped=int(((a[:,:,3]>0)&(np.array(mask)==0)).sum())
assert clipped==0, f'demon exceeds native footprint: {clipped}'
a[:,:,3]=np.minimum(a[:,:,3],np.array(mask));base=Image.fromarray(a)
base.save(art/'imp_base_registered.png')
cell={}
for pose in poses[3:]:
    for x,y,t in pose['tiles']:
        if y<24:
            # Only wing pixels vary. Face, arms, torso, legs and tail use base.
            src=alternate if t in [0x84,0x85,0x86,0x87] else base
            cell[t]=src.crop((x*2,y*2,x*2+16,y*2+16))
        else:cell[t]=Image.new('RGBA',(16,16))
arrow=register(obj(Image.open(gen/'screen2_1_arrow_generated.png')),(8,30))
projectile=Image.new('RGBA',(16,32));projectile.paste(arrow,(4,1))
# The original two-cell held arrow is replaced by the same arrow as its drop.
cell[0x81].alpha_composite(projectile.crop((0,0,16,16)))
cell[0x83]=projectile.crop((0,16,16,32))
for t,im in sorted(cell.items()):tile(0x200+t,'FF370726',im,'winged demon facing left')
projectile.save(art/'arrow_registered.png')
for i,t in enumerate([0x8c,0x8d]):tile(0x200+t,'FF370726',projectile.crop((0,i*16,16,i*16+16)),'downward arrow')

# Shared art aliases: byte-identical native heart, magic, figurine, HUD and
# defeat tiles. Choose the approved replacement once, not an obsolete fallback.
aliases=[]
for line in text.splitlines():
    m=re.fullmatch(r'(?:\[([^]]+)\])?<tile>(.*)',line)
    if not m:continue
    old_scope,values=m.groups();p=values.split(',');idx,t=int(p[0]),int(p[1],16)
    take = (idx==25 and t in [0x47,0x48]) or (idx==29 and t in [0x4e,0x4f])
    if take:
        p[1]=f'{0x200+t:04X}';aliases.append(f'[{scope}]<tile>'+','.join(p))
assert len(aliases)==6, len(aliases)
atlas.save(art/'Stage2_Exterior_Tiles_2x.png');atlas.save(pack/'Stage2_Exterior_Tiles_2x.png')
def section(kind,lines):return '# BEGIN SCREEN2_1 '+kind+'\n'+'\n'.join(lines)+'\n# END SCREEN2_1 '+kind+'\n'
end=text.index('\n',text.rfind('<img>'))+1
text=text[:end]+section('IMAGES',['<img>Stage2_Exterior_Tiles_2x.png'])+text[end:]
lines=text.splitlines(keepends=True)
first=next(i for i,line in enumerate(lines) if '<tile>' in line or '<background>' in line)
lines[first:first]=[section('CONDITIONS',conditions),section('MAPPINGS',rules+aliases+[f'[{background_scope}]<background>Stage2_Exterior_Background.png,1,1,1,11,0,0'])]
(pack/'hires.txt').write_text(''.join(lines))
(art/'registration.json').write_text(json.dumps(dict(scope=scope,background_scope=background_scope,
    palette_states=pool_report,tile_rules=len(rules),shared_aliases=len(aliases),atlas_cells=len(cached),
    mappings=mappings,imp_clipped_pixels=clipped,collision_modified=False,existing_art_modified=False,
    background_size=panorama.size),indent=2)+'\n')
print('Stage 2 exterior:',len(rules),'new mappings,',len(aliases),'shared aliases')
