"""Register the fourth section to native tiles; reuse approved tree and sprites."""
from pathlib import Path
import json
from PIL import Image, ImageChops
import numpy as np

root = Path(__file__).resolve().parents[1]
pack = root/'build/Holy_Diver_(Tr)'
art = root/'art/screen1_4'
art.mkdir(exist_ok=True)
scope = 'treeRoomSignature&treeRoomPal1&treeRoomPal2&treeRoomPal3&cryptSpritePalette'
palettes = ['0F072830','0F071737','0F1B2B3B','0F172737']
atlas = Image.new('RGBA',(256,256))
rules, mappings = [], []
seen = set()

def register(im, size):
    im = im.convert('RGBA').resize(size,Image.Resampling.LANCZOS)
    alpha = im.getchannel('A').point(lambda a: 255 if a>=110 else 0)
    im = im.convert('RGB').quantize(colors=64).convert('RGBA')
    im.putalpha(alpha)
    return im

def tile(t, pal, im, kind, sprite=False):
    identity = t if sprite else t+0x100
    assert (identity,pal) not in seen
    seen.add((identity,pal))
    slot=len(mappings);x,y=slot%16*16,slot//16*16
    assert y+16<=atlas.height
    assert im.size==(16,16)
    atlas.paste(im,(x,y))
    rules.append(f'[{scope}]<tile>29,{identity:04X},{pal},{x},{y},1,N')
    mappings.append(dict(identity=f'{identity:04X}',palette=pal,atlas=[x,y],kind=kind))

def grid(rows,pal,im,kind):
    for y,row in enumerate(rows):
        for x,t in enumerate(row):
            if t is not None:
                tile(t,pal,im.crop((x*16,y*16,x*16+16,y*16+16)),kind)

empty=Image.new('RGBA',(16,16))
for pal in palettes:
    tile(0,pal,empty,'transparent background')
# The moon is scenery, not an enemy. Replace its native ornament with the
# approved distant moon and castle silhouette in the scrolling backdrop.
for t in range(0x28,0x3d):
    tile(t,palettes[0],empty,'moon cleared for backdrop')
backdrop=Image.open(root/'art/layers/00_distant_ruins.png').convert('RGBA')
moon=Image.open(root/'art/layers/05_moon_behind_castles.png').convert('RGBA')
backdrop.alpha_composite(moon)
# Move the castle occlusion with the moon, retaining its approved silhouette.
backdrop=ImageChops.offset(backdrop,-48,0).resize((512,1024),Image.Resampling.NEAREST)
backdrop.save(art/'Tree_Court_Background.png')
backdrop.save(pack/'Tree_Court_Background.png')

# The original tree has a 32-native-pixel repeating trunk. Keep its native
# top, branches and irregular root footprint separate so scrolling and every
# collision edge are inherited from the PPU, not guessed from a panorama.
tree=Image.open(root/'art/layers/20_tree_and_branches.png').convert('RGBA')
top=register(tree.crop((286,320,354,336)),(64,16))
body=register(tree.crop((286,400,354,464)),(64,64))
# Blend the two texture boundaries only; no native silhouette is enlarged.
arr=np.array(body);edge=((arr[0].astype(int)+arr[-1].astype(int))//2).astype('uint8')
arr[0]=edge;arr[-1]=edge;body=Image.fromarray(arr)
grid([[0x3d,0x3e,0x45,0x46]],palettes[1],top,'tree crown')
grid([[0x3f,0x40,0x47,0x48],[0x41,0x42,0x49,0x4a],
      [0x43,0x44,0x4b,0x4c],[0x4f,0x50,0x51,0x52]],palettes[1],body,'tree repeat')
left=register(tree.crop((224,384,288,400)),(64,16))
right=register(tree.crop((350,480,414,496)),(64,16))
grid([[0x22,0x23,0x4d,0x4e]],palettes[1],left,'left branch')
grid([[0x5b,0x5c,0x5d,0x5e]],palettes[1],right,'right branch')
roots=register(tree.crop((252,816,388,864)),(128,48))
grid([[None,None,None,None,0x68,None,None,None],
      [None,0x61,0x62,0x63,0x69,0x6a,0x6b,None],
      [0x64,0x65,0x66,0x67,0x6c,0x6d,0x6e,0x6f]],palettes[1],roots,'roots')
floor=Image.open(root/'art/layers/50_floor.png').convert('RGBA').crop((256,864,320,928))
grid([[0x18,0x19,0x1a,0x1b],[5,6,7,8],[9,10,11,12],[13,14,15,16]],palettes[3],floor,'ground')
grid([[1,2,3,4]],palettes[3],floor.crop((0,32,64,48)),'deep ground repeat')
# The next nametable row is streamed while descending. Retain matching
# approved stone for these identities as well, even below the last viewport.
terrain=Image.open(pack/'Crypt_Terrain_2x.png').convert('RGBA')
for key,(x,y) in json.loads((root/'art/room2/terrain_mapping.json').read_text()).items():
    t,pal=key.split(':')
    if 0x70<=int(t,16)<=0x77:
        tile(int(t,16),palettes[2],terrain.crop((x,y,x+16,y+16)),'shared lower stone')

src=Image.open(root/'art/generated/screen1_4_masonry_generated.png').convert('RGBA').resize((1024,1024),Image.Resampling.LANCZOS)
cornice=register(src.crop((0,0,512,240)),(64,64))
brick=register(src.crop((0,512,512,1024)),(32,32))
column=register(src.crop((682,0,850,512)),(32,96))
arch=register(src.crop((645,512,773,1024)),(32,96))
for pal in palettes[1:]:
    tile(0x26,pal,brick.crop((0,0,16,16)),'wall infill')
grid([[0x78,0x79],[0x7a,0x7b],[0x7c,0x7d],[0x7e,0x7f],[0x80,0x81]],palettes[1],column,'column')
tile(0x82,palettes[1],column.crop((16,80,32,96)),'column repeat')
grid([[0x87,0x88],[0x89,0x8a]],palettes[1],brick,'weathered brick')
grid([[0xb3,0xb1],[0xb0,0xc4]],palettes[2],arch,'arch cap')
for t,y in [(0xc3,32),(0xc2,48),(0xc1,64)]:
    tile(t,palettes[3],arch.crop((0,y,16,y+16)),'arch leg')
for t,xy in [(0x15,(0,0)),(0x16,(16,0)),(0x17,(16,16)),(0x24,(0,16)),(0xbf,(0,0)),(0xc0,(16,0))]:
    x,y=xy;tile(t,palettes[2],brick.crop((x,y,x+16,y+16)),'wall edge')
for t,xy in [(0x24,(0,16)),(0x25,(16,0)),(0x27,(16,16))]:
    x,y=xy;tile(t,palettes[3],brick.crop((x,y,x+16,y+16)),'wall edge')
# Ceiling and shelf molding: each native ID keeps its exact 8x8 footprint.
for t,xy in [(0xd8,(0,0)),(0xd7,(16,0)),(0xd6,(0,16)),(0xd5,(16,16)),
             (0xd4,(0,32)),(0xd3,(16,32)),(0xd2,(32,32)),
             (0xd1,(0,48)),(0xd0,(16,48)),(0xcf,(48,0)),(0xce,(48,16)),(0xcd,(48,32))]:
    x,y=xy;tile(t,palettes[3],cornice.crop((x,y,x+16,y+16)),'cornice')
ledge=register(src.crop((0,0,64,90)),(16,32))
for t,y in [(0xd9,0),(0xda,16),(0xdb,0),(0xdc,16)]:
    tile(t,palettes[3],ledge.crop((0,y,16,y+16)),'platform cap')

# The 1-up is a miniature Randy, two vertically stacked sprites, not a new
# full-sized pose. Reuse approved walk pose 1 and preserve both palette forms.
for pal,name in [('FF300036','Randy_Entrance_2x.png'),('FF221136','Randy_Equipped_2x.png')]:
    mini=register(Image.open(pack/name).convert('RGBA').crop((64,0,96,64)),(16,32))
    mini.save(art/('one_up_'+pal+'.png'))
    for i,t in enumerate([0x4e,0x4f]):
        tile(t,pal,mini.crop((0,i*16,16,i*16+16)),'1-up miniature Randy',sprite=True)

# Same enemy identities, different room palette. Reuse the approved atlas
# including sharp standing-specific cells; keep those ahead of broad rolls.
text=(pack/'hires.txt').read_text()
nave_scope=json.loads((root/'art/screen1_3/registration.json').read_text())['scope']
enemy_rules=[]
for line in text.splitlines():
    if line.startswith('['+nave_scope) and '<tile>28,' in line:
        identity=int(line.split('<tile>28,')[1].split(',')[0],16)
        if 0x60<=identity<=0xab:
            enemy_rules.append(line.replace(nave_scope,scope,1))
assert len(enemy_rules)==48
rules=enemy_rules+rules
atlas.save(art/'Tree_Court_Tiles_2x.png')
atlas.save(pack/'Tree_Court_Tiles_2x.png')

def section(name,lines):
    return '# BEGIN SCREEN1_4 '+name+'\n'+'\n'.join(lines)+'\n# END SCREEN1_4 '+name+'\n'
end=text.index('\n',text.rfind('<img>'))+1
text=text[:end]+section('IMAGES',['<img>Tree_Court_Tiles_2x.png'])+text[end:]
conditions=['<condition>treeRoomSignature,memoryCheckConstant,0072,==,04',
            '<condition>treeRoomPal1,ppuMemoryCheckConstant,3F05,==,07',
            '<condition>treeRoomPal2,ppuMemoryCheckConstant,3F0B,==,3B',
            '<condition>treeRoomPal3,ppuMemoryCheckConstant,3F0F,==,37']
# Existing spriteNearby definitions must exist before the shared enemy rules.
lines=text.splitlines(keepends=True)
first=next(i for i,line in enumerate(lines) if '<tile>' in line or '<background>' in line)
lines[first:first]=[section('CONDITIONS',conditions),section('MAPPINGS',rules+[f'[{scope}]<background>Tree_Court_Background.png,1,1,1,11,0,0'])]
(pack/'hires.txt').write_text(''.join(lines))
report=dict(scope=scope,tile_rules=len(rules),conditions=4,background_rules=1,
            shared_enemy_rules=len(enemy_rules),new_atlas_cells=len(mappings),mappings=mappings,
            collision_modified=False,existing_rules_modified=False)
(art/'registration.json').write_text(json.dumps(report,indent=2)+'\n')
print('Screen 1-4:',len(rules),'tile rules;',len(mappings),'new cells; native geometry retained.')
