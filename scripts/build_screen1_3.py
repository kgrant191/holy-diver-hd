"""Add the third chapel section using measured native tile and OAM layouts."""
from pathlib import Path
import json
import numpy as np
from PIL import Image, ImageOps, ImageDraw

root = Path(__file__).resolve().parents[1]
art = root/'art/screen1_3'
pack = root/'build/Holy_Diver_(Tr)'
art.mkdir(exist_ok=True)
generated = root/'art/generated'
scope = 'cryptPalette&cryptStonePalette&cryptSpritePalette&navePal1&navePal2&navePal3'

def crop_object(image, rectangle):
    im = image.crop(rectangle)
    bbox = im.getchannel('A').point(lambda a: 255 if a >= 120 else 0).getbbox()
    assert bbox
    return im.crop(bbox)

def register(image, size):
    im = image.resize(size, Image.Resampling.LANCZOS)
    alpha = im.getchannel('A').point(lambda a: 255 if a >= 120 else 0)
    im = im.convert('RGB').quantize(colors=56, method=Image.Quantize.MEDIANCUT).convert('RGBA')
    im.putalpha(alpha)
    return im

# Opaque masonry attaches the tile-bound windows to a wall, while native
# terrain retains all collision edges. Repeat after 512 native scroll pixels.
wall = Image.open(generated/'screen1_3_background_generated.png').convert('RGB').resize((1024, 480), Image.Resampling.LANCZOS)
pixels = np.array(wall).astype(float)
edge = (pixels[:, 0]+pixels[:, -1])/2
for x in range(24):
    weight = (1-x/24)**2
    pixels[:, x] = pixels[:, x]*(1-weight)+edge*weight
    pixels[:, -1-x] = pixels[:, -1-x]*(1-weight)+edge*weight
wall = Image.fromarray(pixels.astype('uint8'))
panorama = Image.new('RGBA', (1536, 480))
panorama.paste(wall, (0, 0))
panorama.paste(wall.crop((0, 0, 512, 480)), (1024, 0))
panorama.save(art/'Nave_Background.png')
panorama.save(pack/'Nave_Background.png')

source = Image.open(generated/'screen1_3_environment_generated.png').convert('RGBA')
objects = [crop_object(source, (i*source.width//3, 0, (i+1)*source.width//3, source.height)) for i in range(3)]
block = Image.new('RGBA', (32, 32), '#182137')
block.alpha_composite(register(objects[0], (32, 32)))
block.save(art/'reinforced_block.png')
window = objects[1]
# Native window: one pointed 8-pixel top, then a repeating 16-pixel body.
cap = register(window.crop((0, 0, window.width, round(window.height*.24))), (32, 16))
body = register(window.crop((0, round(window.height*.37), window.width, round(window.height*.62))), (32, 32))
cap.save(art/'window_cap.png')
body.save(art/'window_repeat.png')
ornament = register(objects[2], (64, 112))
ornament_layout = [(1,0,0x8b),(2,0,0x95),(0,1,0x8c),(1,1,0x8d),(2,1,0x96),
                   (0,2,0x8e),(1,2,0x8f),(2,2,0x97),(3,2,0x98),
                   (0,3,0x90),(1,3,0x91),(2,3,0x99),(3,3,0x9a),
                   (1,4,0x92),(2,4,0x9b),(1,5,0x93),(2,5,0x9c),(1,6,0x94),(2,6,0x9d)]
cover = Image.new('L', ornament.size)
draw = ImageDraw.Draw(cover)
for x,y,t in ornament_layout:
    draw.rectangle((x*16,y*16,x*16+15,y*16+15), fill=255)
arr = np.array(ornament)
clipped = int(((arr[:,:,3]>0)&(np.array(cover)==0)).sum())
arr[:,:,3] = np.minimum(arr[:,:,3], np.array(cover))
ornament = Image.fromarray(arr)
ornament.save(art/'serpent_ornament.png')

atlas = Image.new('RGBA', (256,128))
rules, mappings = [], []
seen = {}
def tile(identity, palette, image, kind):
    key = (identity,palette)
    if key in seen:
        assert np.array_equal(np.array(seen[key]),np.array(image)), key
        return
    seen[key] = image
    slot = len(mappings)
    x,y = slot%16*16, slot//16*16
    assert y+16 <= atlas.height
    atlas.paste(image,(x,y))
    rules.append(f'[{scope}]<tile>28,{identity:04X},{palette},{x},{y},1,N')
    mappings.append({'identity':f'{identity:04X}','palette':palette,'atlas':[x,y],'kind':kind})

# Native empty cells around the gold pendant and windows otherwise retain
# opaque black from the broad imported atlas, obscuring the new wall.
for palette in ['0F172737','0F262B17']:
    tile(0x100,palette,Image.new('RGBA',(16,16)),'empty background')

for i,t in enumerate([0xc9,0xca,0xcb,0xcc]):
    x,y = i%2*16,i//2*16
    tile(0x100+t,'0F001030',block.crop((x,y,x+16,y+16)),'reinforced block')
for i,t in enumerate([0xb9,0xba]):
    tile(0x100+t,'0F262B17',cap.crop((i*16,0,i*16+16,16)),'window cap')
for i,t in enumerate([0xbb,0xbc,0xbd,0xbe]):
    x,y = i%2*16,i//2*16
    tile(0x100+t,'0F262B17',body.crop((x,y,x+16,y+16)),'window repeat')
for x,y,t in ornament_layout:
    tile(0x100+t,'0F172737',ornament.crop((x*16,y*16,x*16+16,y*16+16)),'serpent ornament')

# The same terrain identities also occur with this section's green/red palette.
# Reuse the approved rock cells; do not repaint existing room-2 assets.
terrain = Image.open(pack/'Crypt_Terrain_2x.png').convert('RGBA')
for key,(x,y) in json.loads((root/'art/room2/terrain_mapping.json').read_text()).items():
    identity,palette = key.split(':')
    if palette == '0F071728':
        tile(0x100+int(identity,16),'0F262B17',terrain.crop((x,y,x+16,y+16)),'shared rock')

ground_source = Image.open(generated/'screen1_3_ghoul_generated.png').convert('RGBA')
ground = [ImageOps.mirror(register(crop_object(ground_source, (i*ground_source.width//2,0,(i+1)*ground_source.width//2,ground_source.height)),(32,48))) for i in range(2)]
# Native unflipped graphics face left; hardware flips both cells and positions.
# Tiles 94/95 are shared by both standing poses and the upright compact pose.
ground[1].paste(ground[0].crop((0,0,32,16)),(0,0))
roll_source = Image.open(generated/'screen1_3_ghoul_roll_generated.png').convert('RGBA')
roll = [register(crop_object(roll_source, (i*roll_source.width//4,0,(i+1)*roll_source.width//4,roll_source.height)),(32,32)) for i in range(4)]
roll[0].paste(ground[0].crop((0,0,32,16)),(0,0))
images = [ground[0],ground[1],roll[3],roll[0],roll[1],roll[2]]
poses = json.loads((art/'ghoul_poses.json').read_text())
for i,(pose,image) in enumerate(zip(poses,images)):
    assert image.size == tuple(v*2 for v in pose['size'])
    image.save(art/f'ghoul_pose_{i}.png')
    for x,y,t in pose['tiles']:
        tile(t,'FF140436',image.crop((x*2,y*2,x*2+16,y*2+16)),f'ghoul pose {i}')

# Small flying skulls only enter after movement. Register both wing poses
# together so the head keeps the same scale and lower baseline.
skull_source = Image.open(generated/'screen1_3_blue_skulls_generated.png').convert('RGBA')
skulls = [crop_object(skull_source, (i*skull_source.width//2,0,(i+1)*skull_source.width//2,skull_source.height)) for i in range(2)]
extent = max(max(im.size) for im in skulls)
for i,source in enumerate(skulls):
    sprite = register(source, tuple(max(1,round(v*32/extent)) for v in source.size))
    image = Image.new('RGBA',(32,32))
    image.paste(sprite,(0,32-sprite.height))
    image.save(art/f'blue_skull_pose_{i}.png')
    for n in range(4):
        x,y=n%2*16,n//2*16
        tile(0x8c+i*4+n,'FF301116',image.crop((x,y,x+16,y+16)),f'blue skull pose {i}')

# The brief first impact frame has a smaller footprint than the already
# approved expanding rings. Reuse that approved art at its measured 16x16 size.
impact = register(Image.open(root/'art/death_ring_0_registered.png').convert('RGBA'),(32,32))
impact.save(art/'impact_registered.png')
for n in range(4):
    x,y=n%2*16,n//2*16
    tile(0x60+n,'FF301116',impact.crop((x,y,x+16,y+16)),'initial impact')
atlas.save(art/'Nave_Tiles_2x.png')
atlas.save(pack/'Nave_Tiles_2x.png')

path = pack/'hires.txt'
s = path.read_text()
assert s.count('<img>') == 28
def section(name, lines):
    return '# BEGIN SCREEN1_3 '+name+'\n'+'\n'.join(lines)+'\n# END SCREEN1_3 '+name+'\n'
last = s.rfind('<img>')
end = s.index('\n',last)+1
s = s[:end]+section('IMAGES',['<img>Nave_Tiles_2x.png'])+s[end:]
pos = s.index('<condition>')
conditions = ['<condition>navePal1,ppuMemoryCheckConstant,3F0D,==,26',
              '<condition>navePal2,ppuMemoryCheckConstant,3F0E,==,2B',
              '<condition>navePal3,ppuMemoryCheckConstant,3F0F,==,17']
s = s[:pos]+section('CONDITIONS',conditions)+s[pos:]
pos = s.index('#Chr_00_0.png')
new_lines = rules+[f'[{scope}]<background>Nave_Background.png,1,1,0,11,0,0']
s = s[:pos]+section('MAPPINGS',new_lines)+s[pos:]
path.write_text(s)
metadata = {'scope':scope,'tile_rules':len(rules),'background_rules':1,'conditions':3,
            'ornament_native_tiles':ornament_layout,'ornament_clipped_pixels':clipped,
            'ghoul_native_unflipped_direction':'left','mappings':mappings,
            'collision_modified':False,'existing_rules_modified':False}
(art/'registration.json').write_text(json.dumps(metadata,indent=2)+'\n')
print(f'Screen 1-3: {len(rules)} tile rules; 6 ghoul poses; native geometry retained.')
