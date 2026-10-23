"""Register standing ghoul and crouch-cast repairs without changing old poses."""
from pathlib import Path
import json
import numpy as np
from PIL import Image, ImageDraw, ImageOps

root = Path(__file__).resolve().parents[1]
art = root / 'art/review_fixes'
art.mkdir(exist_ok=True)
pack = root / 'build/Holy_Diver_(Tr)'
conditions, rules = [], []
report = {'crouch': [], 'ghoul': [], 'rolling_pixels_changed': 0}

def register(source, rectangle, size, nearest=False):
    cell = source.crop(rectangle)
    bounds = cell.getchannel('A').point(lambda a: 255 if a >= 120 else 0).getbbox()
    assert bounds
    cell = cell.crop(bounds).resize(size, Image.Resampling.NEAREST if nearest else Image.Resampling.LANCZOS)
    alpha = cell.getchannel('A').point(lambda a: 255 if a >= 128 else 0)
    result = cell.convert('RGB').quantize(colors=24 if nearest else 40).convert('RGBA')
    result.putalpha(alpha)
    return result

# Use the two previously unused 64x64 cells in each approved Randy atlas.
# No pixels in the ten existing poses are touched.
poses = json.loads((root/'art/crouch_attack_poses.json').read_text())
source = Image.open(root/'art/generated/randy_crouch_attack_generated.png').convert('RGBA')
for mode, (palette, atlas_name, atlas_index) in enumerate([
    ('FF300036', 'Randy_Entrance_2x.png', 18),
    ('FF221136', 'Randy_Equipped_2x.png', 19),
]):
    atlas = Image.open(pack/atlas_name).convert('RGBA')
    for phase, pose in enumerate(poses):
        size = tuple(v*2 for v in pose['size'])
        rectangle = (phase*source.width//2, mode*source.height//2,
                     (phase+1)*source.width//2, (mode+1)*source.height//2)
        if phase == 0:
            sprite = Image.new('RGBA',size)
            sprite.paste(register(source,rectangle,(48,44)),(6,4))
        else:
            sprite = register(source, rectangle, size)
        coverage = Image.new('L', size)
        draw = ImageDraw.Draw(coverage)
        for x,y,t in pose['tiles']:
            draw.rectangle((x*2,y*2,x*2+15,y*2+15), fill=255)
        pixels = np.array(sprite)
        clipped = int(((pixels[:,:,3] > 0) & (np.array(coverage) == 0)).sum())
        pixels[:,:,3] = np.minimum(pixels[:,:,3], np.array(coverage))
        sprite = Image.fromarray(pixels)
        sprite.save(art/f'randy_{mode}_{phase}.png')
        ox,oy = (phase+2)*64,128
        assert not atlas.crop((ox,oy,ox+64,oy+64)).getchannel('A').getbbox()
        atlas.paste(sprite,(ox,oy))
        for index,(x,y,t) in enumerate(pose['tiles']):
            # Windup $33 is unique to crouch. Release $2F identifies the
            # crouching lower row; upper $2C separates it from ordinary ducking.
            anchors = [pose['tiles'][6]] if phase == 0 else [pose['tiles'][3],pose['tiles'][6]]
            if phase == 0 and t == 0x33:
                anchors = [pose['tiles'][0]]
            names=[]
            for n,(ax,ay,at) in enumerate(anchors):
                if (ax,ay,at)==(x,y,t):
                    continue
                name=f'crouchCast{mode}_{phase}_{index}_{n}'
                conditions.append(f'<condition>{name},spriteNearby,{ax-x},{ay-y},{at:02X},{palette}')
                names.append(name)
            assert names
            rules.append('['+'&'.join(['!randyDefeated']+names)+f']<tile>{atlas_index},{t:02X},{palette},{ox+x*2},{oy+y*2},1,N')
        report['crouch'].append({'palette':palette,'phase':pose['name'],'size':size,'clipped_pixels':clipped})
    atlas.save(pack/atlas_name)
    atlas.save(art/atlas_name)

# Retain all original atlas cells, including the head used by the rolling pose.
# New standing heads select only when the corresponding six-sprite body exists.
atlas = Image.open(pack/'Nave_Tiles_2x.png').convert('RGBA')
source = Image.open(root/'art/generated/ghoul_standing_review_generated.png').convert('RGBA')
ghoul_poses = json.loads((root/'art/screen1_3/ghoul_poses.json').read_text())
scope = json.loads((root/'art/screen1_3/registration.json').read_text())['scope']
for phase,pose in enumerate(ghoul_poses[:2]):
    sprite = ImageOps.mirror(register(source,(phase*source.width//2,0,(phase+1)*source.width//2,source.height),(32,48),nearest=True))
    sprite.save(art/f'ghoul_standing_{phase}.png')
    for index,(x,y,t) in enumerate(pose['tiles']):
        slot=87+phase*6+index
        ox,oy=slot%16*16,slot//16*16
        assert not atlas.crop((ox,oy,ox+16,oy+16)).getchannel('A').getbbox()
        atlas.paste(sprite.crop((x*2,y*2,x*2+16,y*2+16)),(ox,oy))
        ax,ay,at=pose['tiles'][4 if index==2 else 2]
        name=f'ghoulStanding{phase}_{index}'
        conditions.append(f'<condition>{name},spriteNearby,{ax-x},{ay-y},{at:02X},FF140436')
        rules.append(f'[{scope}&{name}]<tile>28,{t:04X},FF140436,{ox},{oy},1,N')
    report['ghoul'].append({'phase':phase,'size':[32,48],'resampling':'nearest','colors':24})
atlas.save(pack/'Nave_Tiles_2x.png')
atlas.save(art/'Nave_Tiles_2x.png')

path=pack/'hires.txt'
text=path.read_text()
def section(name,lines):
    return '# BEGIN REVIEW_FIXES '+name+'\n'+'\n'.join(lines)+'\n# END REVIEW_FIXES '+name+'\n'
# Earlier imported player rules are ahead of the screen section. Insert
# repairs at the first tile rule, after all original condition definitions.
block=section('MAPPINGS',rules)
defs=section('CONDITIONS',conditions)
lines=text.splitlines(keepends=True)
first=next(i for i,line in enumerate(lines) if '<tile>' in line or '<background>' in line)
lines[first:first]=[defs,block]
path.write_text(''.join(lines))
report.update(tile_rules=len(rules),conditions=len(conditions),existing_pose_pixels_changed=0)
(art/'registration.json').write_text(json.dumps(report,indent=2)+'\n')
print('Review repairs:',len(rules),'rules;',len(conditions),'signatures;',report['crouch'])
