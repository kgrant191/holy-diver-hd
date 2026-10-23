"""Register the first boss, organ hall and Blizzard sequence to measured native data."""
from pathlib import Path
import hashlib
import json
import re
from PIL import Image, ImageDraw, ImageFont, ImageOps
import numpy as np

root = Path(__file__).resolve().parents[1]
art = root/'art/boss1'
pack = root/'build/Holy_Diver_(Tr)'
generated = root/'art/generated'
text = (pack/'hires.txt').read_text()
assert text.count('<img>') == 30
atlas = Image.new('RGBA', (512,512))
conditions, rules, backgrounds, cells = [], [], [], []
cell_cache = {}

def reg(im, size, nearest=False):
    im = im.convert('RGBA').resize(size, Image.Resampling.NEAREST if nearest else Image.Resampling.LANCZOS)
    alpha = im.getchannel('A').point(lambda a: 255 if a >= 120 else 0)
    im = im.convert('RGB').quantize(colors=48).convert('RGBA')
    im.putalpha(alpha)
    return im

def source(name):
    im = Image.open(generated/name).convert('RGBA')
    im.putalpha(im.getchannel('A').point(lambda a: 255 if a >= 120 else 0))
    return im.crop(im.getbbox())

def tile(identity, pal, im, scope, kind):
    assert im.size == (16,16)
    digest = hashlib.sha256(im.tobytes()).hexdigest()
    if digest not in cell_cache:
        n = len(cell_cache); x,y=n%32*16,n//32*16
        assert y+16 <= atlas.height
        atlas.paste(im,(x,y)); cell_cache[digest]=(x,y)
    x,y=cell_cache[digest]
    rules.append(f'[{scope}]<tile>30,{identity:04X},{pal},{x},{y},1,N')
    cells.append(dict(identity=f'{identity:04X}',palette=pal,atlas=[x,y],scope=scope,kind=kind))

def probe(name, address, value, memory=False):
    conditions.append(f'<condition>{name},{"memoryCheckConstant" if memory else "ppuMemoryCheckConstant"},{address:04X},==,{value:02X}')
    return name

hall_data='&'.join([probe('bossHallDataLo',0x78,0x3a,True),probe('bossHallDataHi',0x79,0x85,True)])
bell_data='&'.join([probe('blizzardDataLo',0x78,0xb2,True),probe('blizzardDataHi',0x79,0x85,True)])
room_pal='&'.join([probe('bossHallPal1',0x3f05,6),probe('bossHallPal2',0x3f09,0),probe('bossHallPal3',0x3f0d,9)])
hall=hall_data+'&'+room_pal
bell=bell_data+'&'+room_pal
red=probe('bossDefeatRed',0x3f00,0x16)

# Standing art supplies all shared head/torso cells. Only measured leg and
# mouth regions vary, so the native animation cannot resize the boss's head.
raw=Image.open(generated/'boss1_sprite_sheet_generated.png').convert('RGBA')
raw.putalpha(raw.getchannel('A').point(lambda a:255 if a>=120 else 0))
rects=[(0,0,512,530),(512,0,1024,530),(1024,0,1536,530),
       (0,530,512,1024),(512,530,1024,1024),(1024,530,1536,1024)]
sprites=[]
for i,rect in enumerate(rects):
    im=raw.crop(rect);im=im.crop(im.getbbox())
    sprites.append(reg(im,(80,96 if i in [3,5] else 128),nearest=True))
poses=json.loads((art/'native_poses.json').read_text())
base=sprites[0]
registered=[base.copy(),base.copy(),base.copy(),base.crop((0,0,80,96))]
registered[1].paste(ImageOps.mirror(sprites[2].crop((0,80,80,128))),(0,80))
registered[2].paste(sprites[2].crop((0,80,80,128)),(0,80))
registered[3].paste(reg(sprites[3].crop((0,72,80,96)),(80,16),nearest=True),(0,80))
mouth=sprites[4].crop((32,32,64,64))
pose_stats=[]
for i,(pose,im) in enumerate(zip(poses[:4],registered)):
    cover=Image.new('L',im.size);d=ImageDraw.Draw(cover)
    for x,y,t in pose['tiles']:d.rectangle((x*2,y*2,x*2+15,y*2+15),fill=255)
    a=np.array(im);clipped=int(((a[:,:,3]>0)&(np.array(cover)==0)).sum())
    a[:,:,3]=np.minimum(a[:,:,3],np.array(cover));registered[i]=Image.fromarray(a)
    registered[i].save(art/(pose['name']+'_registered.png'))
    pose_stats.append(dict(name=pose['name'],size=im.size,clipped_pixels=clipped))

def hit_flash(im):
    # Native palette 1C/0B/36 -> 10/20/30: retain the HD silhouette and shading.
    a=np.array(im); l=np.asarray(im.convert('L')).astype(float)/255
    a[:,:,:3]=np.stack([115+140*l,139+116*l,163+92*l],axis=2).astype('uint8')
    return Image.fromarray(a)

for pal in ['FF1C0B36','FF102030']:
    images=[im if pal=='FF1C0B36' else hit_flash(im) for im in registered]
    # Specific leg layouts precede the standing fallback. Sparse death frames
    # naturally lose these probes and keep their matching standing cells.
    for i,anchor_id,other_id in [(1,0xe7,0xe8),(2,0xea,0xeb),(3,0xed,0xef)]:
        pose=poses[i]
        for n,(x,y,t) in enumerate(pose['tiles']):
            if y<40:continue
            ax,ay,at=next(v for v in pose['tiles'] if v[2]==(other_id if t==anchor_id else anchor_id))
            name=f'bossLeg{i}_{n}_{pal[2:]}'
            conditions.append(f'<condition>{name},spriteNearby,{ax-x},{ay-y},{at:02X},{pal}')
            tile(t,pal,images[i].crop((x*2,y*2,x*2+16,y*2+16)),hall_data+'&'+name,'boss '+pose['name'])
    for x,y,t in poses[0]['tiles']:
        tile(t,pal,images[0].crop((x*2,y*2,x*2+16,y*2+16)),hall_data,'boss standing/death')
    im=mouth if pal=='FF1C0B36' else hit_flash(mouth)
    for n,t in enumerate([0xe3,0xe4,0xe5,0xe6]):
        x,y=n%2*16,n//2*16
        tile(t,pal,im.crop((x,y,x+16,y+16)),hall_data,'boss firing mouth')

# Four native sprites form one round boss projectile. Its artwork stays exact;
# the supported HD-pack option below prevents the native scanline limit from
# dropping alternate halves when the boss and Randy occupy the same scanlines.
fire=reg(source('boss1_fireball_generated.png'),(32,32),nearest=True)
fire.save(art/'boss_fireball_registered.png')
for x,y,t in [(0,0,0xf1),(16,0,0xf2),(0,16,0xf3),(16,16,0xf4)]:
    tile(t,'FF162830',fire.crop((x,y,x+16,y+16)),hall_data,'boss fireball')

empty=Image.new('RGBA',(16,16))
terrain=Image.open(pack/'Crypt_Terrain_2x.png').convert('RGBA')
terrain_map=json.loads((root/'art/room2/terrain_mapping.json').read_text())
pipe=source('boss1_pipe_generated.png')
pw,ph=pipe.size
cap=reg(pipe.crop((0,0,pw,round(ph*.23))),(32,64))
body=reg(pipe.crop((0,round(ph*.4),pw,round(ph*.45))),(32,16))
foot=reg(pipe.crop((0,round(ph*.91),pw,ph)),(32,32))
# The repeat has identical top/bottom pixels and is reused for both native rows.
pa=np.array(body); edge=((pa[0].astype(int)+pa[-1].astype(int))//2).astype('uint8');pa[0]=edge;pa[-1]=edge;body=Image.fromarray(pa)
# The pickup scroll wraps the native nametable vertically. The approved nave
# panorama is only one screen high, so repeating its exact pixels across both
# nametables plus a viewport keeps the backdrop present throughout the ascent.
wall=Image.open(pack/'Nave_Background.png').convert('RGB')
ascent_wall=Image.new('RGB',(wall.width,wall.height*3))
for row in range(3):ascent_wall.paste(wall,(0,row*wall.height))
ascent_wall.save(pack/'Blizzard_Ascent_Background.png')
for scope in [hall,bell]:
    for prefix in ['0F','16','31']:
        for pal in ['172737','061627','001030','093918']:
            tile(0x100,prefix+pal,empty,scope,'clear native backdrop')
        for t in range(0x87,0x8b):tile(0x100+t,prefix+'061627',empty,scope,'continuous masonry backdrop')
        for key,(x,y) in terrain_map.items():
            t,pal=key.split(':');t=int(t,16)
            if 0x70<=t<=0x77 or 0xa4<=t<=0xa7:
                tile(t+0x100,prefix+'001030',terrain.crop((x,y,x+16,y+16)),scope,'approved stone/sconce')
        for n,t in enumerate(range(0x78,0x80)):
            x,y=n%2*16,n//2*16;tile(t+0x100,prefix+'061627',cap.crop((x,y,x+16,y+16)),scope,'organ pipe cap')
        for t,x in [(0x80,0),(0x81,16),(0x82,16)]:tile(t+0x100,prefix+'061627',body.crop((x,0,x+16,16)),scope,'organ pipe repeat')
        for n,t in enumerate(range(0x83,0x87)):
            x,y=n%2*16,n//2*16;tile(t+0x100,prefix+'061627',foot.crop((x,y,x+16,y+16)),scope,'organ pipe foot')
    backdrop='Blizzard_Ascent_Background.png' if scope==bell else 'Nave_Background.png'
    backgrounds.append(f'[{scope}]<background>{backdrop},1,1,1,11,0,0')

# The golden pendant has the same native layout as the approved nave ornament.
ornament=Image.open(root/'art/screen1_3/serpent_ornament.png').convert('RGBA')
for x,y,t in json.loads((root/'art/screen1_3/registration.json').read_text())['ornament_native_tiles']:
    for prefix in ['0F','16']:
        tile(t+0x100,prefix+'172737',ornament.crop((x*16,y*16,x*16+16,y*16+16)),hall,'approved serpent pendant')

# The native boss defeat pulses the background color red. A separate backdrop
# follows that exact palette event instead of suppressing the visible flash.
flash=Image.open(pack/'Nave_Background.png').convert('RGBA')
fa=np.array(flash);fa[:,:,0]=np.clip(fa[:,:,0].astype(float)*.7+85,0,255);fa[:,:,1:3]=(fa[:,:,1:3].astype(float)*.55).astype('uint8')
Image.fromarray(fa).save(pack/'Boss_Hall_Flash.png')
backgrounds.append(f'[{hall}&{red}]<background>Boss_Hall_Flash.png,1,1,1,12,0,0')

bell_im=reg(source('boss1_bell_generated.png'),(96,160))
bell_im.save(art/'bell_registered.png')
for x,y,t in json.loads((art/'bell_layout.json').read_text()):
    for prefix in ['0F','31']:
        tile(t+0x100,prefix+'093918',bell_im.crop((x*2,y*2,x*2+16,y*2+16)),bell,'Blizzard bell')
book=reg(source('boss1_blizzard_generated.png'),(32,32),nearest=True)
book.save(art/'blizzard_registered.png')
for n,t in enumerate(range(0x78,0x7c)):
    x,y=n%2*16,n//2*16
    tile(t,'FF301116',book.crop((x,y,x+16,y+16)),bell_data,'Blizzard pickup')

# The announcement uses a separate CHR bank. Exact native text probes prevent
# a room or another acquired spell from selecting this presentation.
spell_sig='&'.join([probe('gotBlizzardG',0x216d,0x26),probe('gotBlizzardB',0x21cc,0x21),probe('gotBlizzardZ',0x21cf,0x3b),probe('gotBlizzardD',0x21d3,0x23)])
spell_card='cardPal1&cardPal2&cardPal3&cardRendering&'+spell_sig
card=Image.open(pack/'Intermission_HD.png').convert('RGBA')
d=ImageDraw.Draw(card);font=root/'art/fonts/DejaVuSerif-Bold.ttf'
for label,y,size,color in [('SPELL ACQUIRED',164,16,'#cbaa73'),('BLIZZARD',205,30,'#d3f2ff')]:
    d.text((256,y),label,font=ImageFont.truetype(str(font),size),fill=color,anchor='mt',stroke_width=1,stroke_fill='#050e20')
card.save(pack/'Blizzard_Acquired.png')
backgrounds.append(f'[{spell_card}]<background>Blizzard_Acquired.png,1,0,0,12,0,0')
for t in [0,*range(0x10,0x40)]:tile(0x1f00+t,'0F213029',empty,spell_card,'clear native spell announcement')

# Clone existing pose signatures and atlas references for byte-identical ROM
# copies observed during the spell announcement and Stage 2 arrival. No art in
# the approved atlases changes, and old-bank rule ordering remains untouched.
defs={line.split('>')[1].split(',')[0]:line for line in text.splitlines() if line.startswith('<condition>')}
copies=json.loads((art/'shared_chr_copies.json').read_text())
aliases=[];alias_defs={}
def remap_scope(scope,bank,palette=None):
    terms=[]
    for term in scope.split('&') if scope else []:
        neg='!' if term.startswith('!') else '';name=term.lstrip('!');line=defs.get(name,'');p=line.split('>')[-1].split(',')
        if len(p)>1 and p[1]=='spriteNearby' and int(p[4],16)<0x100:
            new=f'bossCopy{bank}_{palette or "native"}_{name}';p[0]=new;p[4]=f'{bank*256+int(p[4],16):04X}'
            if palette:p[5]=palette
            alias_defs[new]='<condition>'+','.join(p);name=new
        terms.append(neg+name)
    return '&'.join(terms)

source_rules=[]
for line in text.splitlines():
    m=re.fullmatch(r'(?:\[([^]]+)\])?<tile>(.*)',line)
    if not m:continue
    scope,v=m.groups();p=v.split(',');idx,t=int(p[0]),int(p[1],16)
    if idx in [18,19,20,21,22,23] and t<0x60:source_rules.append((scope or '',p))
copy_palettes={
    'FF300036':probe('bossCopyIvoryPalette',0x3f1d,0x30),
    'FF221136':probe('bossCopyBluePalette',0x3f1d,0x22),
    'FF301116':probe('bossCopyHudPalette',0x3f19,0x30),
}
for bank in [2,30]:
    for scope,p0 in source_rules:
        p=p0.copy();t=int(p[1],16)
        if f'{t:02X}' not in copies[str(bank)]:continue
        p[1]=f'{bank*256+t:04X}';scope=remap_scope(scope,bank)
        scope=scope or copy_palettes[p[2]]
        aliases.append('['+scope+']<tile>'+','.join(p))

# Native monochrome ascent/fade palettes keep their exact opacity cadence,
# using the already approved Randy shape instead of reverting to NES pixels.
normal_atlas=Image.open(pack/'Randy_Entrance_2x.png').convert('RGBA')
for pal,intensity,bank in [('FF303030',255,0),('FF303030',255,30),('FF202020',255,30),('FF101010',173,30),('FF000000',98,30)]:
    for scope,p in source_rules:
        if p[0]!='18' or p[2]!='FF300036':continue
        t=int(p[1],16);x,y=int(p[3]),int(p[4]);im=normal_atlas.crop((x,y,x+16,y+16))
        color=Image.new('RGBA',(16,16),(intensity,intensity,intensity,255));color.putalpha(im.getchannel('A'))
        scope=remap_scope(scope,bank,pal)
        scope='&'.join(filter(None,[bell_data if bank==0 else spell_sig,scope]))
        tile(bank*256+t,pal,color,scope,'Randy native monochrome transition')

# The Blizzard menu uses alternate R and D identities, unlike TWIN FIRE's R.
# Match the existing code-rendered menu font without altering the approved UI
# atlas or any of its earlier mappings. Append these cells after all old cells.
menu_scope='pauseScreen&pauseMagicRow&pausedPalette'
for identity,char in [(0x964,'R'),(0x965,'D')]:
    glyph=Image.new('RGBA',(16,16))
    ImageDraw.Draw(glyph).text((8,8),char,font=ImageFont.truetype(str(font),14),
                              anchor='mm',fill='#f4deb0')
    tile(identity,'0F072830',glyph,menu_scope,'Blizzard pause-menu '+char)

# The pre-announcement fade still uses CHR bank 00 and the bell-room identity.
# Its 20/10/00 palettes precede the announcement's CHR-bank switch. Retain the
# exact HD silhouette through those native fade steps, in either direction.
# Append after existing cells so all previously registered artwork stays exact.
for pal,intensity in [('FF202020',255),('FF101010',173),('FF000000',102)]:
    for scope,p in source_rules:
        if p[0]!='18' or p[2]!='FF300036':continue
        t=int(p[1],16);x,y=int(p[3]),int(p[4])
        im=normal_atlas.crop((x,y,x+16,y+16))
        color=Image.new('RGBA',(16,16),(intensity,intensity,intensity,255))
        color.putalpha(im.getchannel('A'))
        scope='&'.join(filter(None,[bell_data,remap_scope(scope,0,pal)]))
        tile(t,pal,color,scope,'Randy pre-announcement fade')

conditions.extend(alias_defs.values())
atlas.save(art/'Boss_Tiles_2x.png');atlas.save(pack/'Boss_Tiles_2x.png')
def section(kind,lines):return '# BEGIN BOSS1 '+kind+'\n'+'\n'.join(lines)+'\n# END BOSS1 '+kind+'\n'
end=text.index('\n',text.rfind('<img>'))+1
text=text[:end]+section('IMAGES',['<img>Boss_Tiles_2x.png'])+text[end:]
lines=text.splitlines(keepends=True);first=next(i for i,l in enumerate(lines)if '<tile>' in l or '<background>' in l)
lines[first:first]=[section('CONDITIONS',conditions),section('MAPPINGS',rules+backgrounds),section('ALIASES',aliases),section('OPTIONS',['<options>disableSpriteLimit'])]
(pack/'hires.txt').write_text(''.join(lines))
report=dict(tile_rules=len(rules)+len(aliases),conditions=len(conditions),background_rules=len(backgrounds),atlas_cells=len(cell_cache),
            shared_bank_aliases=len(aliases),poses=pose_stats,mappings=cells,collision_modified=False,existing_rules_modified=False,
            boss_scope=hall,bell_scope=bell,spell_card_scope=spell_card,
            global_sprite_limit_changed=True,menu_glyphs={'0964':'R','0965':'D'},
            ascent_backdrop='Blizzard_Ascent_Background.png',ascent_backdrop_repeat_rows=3,
            pre_announcement_fade={'FF202020':255,'FF101010':173,'FF000000':102})
(art/'registration.json').write_text(json.dumps(report,indent=2)+'\n')
print('Boss 1:',len(rules)+len(aliases),'rules;',len(cell_cache),'atlas cells;',len(aliases),'shared bank aliases')
