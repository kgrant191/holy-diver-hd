"""Vertical cave: shared gold/cave scenery and the native floating eye."""
from pathlib import Path
import hashlib,json
from PIL import Image

root=Path(__file__).resolve().parents[1]
pack=root/'build/Holy_Diver_(Tr)';art=root/'art/screen2_3';art.mkdir(exist_ok=True)
text=(pack/'hires.txt').read_text();assert text.count('<img>')==34
scope='s23Room&s23DataLo&s23DataHi'
conditions=['<condition>s23Room,memoryCheckConstant,0072,==,04',
            '<condition>s23DataLo,memoryCheckConstant,0078,==,F9',
            '<condition>s23DataHi,memoryCheckConstant,0079,==,8B']
aliases=[];rules=[];metadata=[];cache={};atlas=Image.new('RGBA',(128,64))

def tile(t,pal,im,kind):
    assert im.size==(16,16)
    digest=hashlib.sha256(im.tobytes()).hexdigest()
    if digest not in cache:
        n=len(cache);xy=(n%8*16,n//8*16);assert xy[1]+16<=atlas.height
        atlas.paste(im,xy);cache[digest]=xy
    x,y=cache[digest];rules.append(f'[{scope}]<tile>34,{t:04X},{pal},{x},{y},1,N')
    metadata.append(dict(identity=f'{t:04X}',palette=pal,atlas=[x,y],kind=kind))

def register(im,size):
    im=im.convert('RGBA').resize(size,Image.Resampling.LANCZOS)
    alpha=im.getchannel('A').point(lambda v:255 if v>=120 else 0)
    im=im.convert('RGB').quantize(colors=48).convert('RGBA');im.putalpha(alpha)
    return im

# Explicitly reuse the accepted cells; the room scope and pointer distinguish
# this vertical chamber from the earlier tree room, which also uses ID 04.
prior=json.loads((root/'art/screen2_2/registration.json').read_text())['scope']
for line in text.splitlines():
    if not line.startswith('['+prior) or '<tile>' not in line:continue
    f=line.split('<tile>')[1].split(',');t=int(f[1],16)
    if (0x32e<=t<=0x34d or 0x35b<=t<=0x35e or 0x28e<=t<=0x2a5 or
        t in [0x300,0x3a1,0x3a2,0x247,0x248,0x24e,0x24f,0x274]):
        aliases.append(line.replace(prior,scope,1))

# The repeated purple wall motif is nonsolid scenery. Clear those identities
# and reuse the approved deep cave panorama as a distant stationary layer.
for t in range(0x39b,0x3a1):
    tile(t,'0F041625',Image.new('RGBA',(16,16)),'cave backdrop reveal')

source=Image.open(root/'art/generated/screen2_3_eye_generated.png').convert('RGBA')
source.putalpha(source.getchannel('A').point(lambda v:255 if v>=120 else 0))
eye=register(source.crop(source.getbbox()),(32,32));eye.save(art/'eye_registered.png')
for i,t in enumerate(range(0x2d8,0x2dc)):
    x=i%2*16;y=i//2*16;tile(t,'FF060C30',eye.crop((x,y,x+16,y+16)),'floating eye')

# The eye sheds blue tears. Preserve both native projectile bounds and OAM
# timing/flips; only these two atlas cells change in the 0.6.1 review repair.
shot_source=Image.open(root/'art/generated/screen2_3_tear_generated.png').convert('RGBA')
shot_source.putalpha(shot_source.getchannel('A').point(lambda v:255 if v>=120 else 0))
shot_source=shot_source.crop(shot_source.getbbox())
for t,size,offset in [(0x2dc,(12,16),(2,0)),(0x2dd,(14,14),(0,2))]:
    im=Image.new('RGBA',(16,16));im.paste(register(shot_source,size),offset)
    im.save(art/f'eye_shot_{t:04X}.png');tile(t,'FF301116',im,'blue teardrop')

backgrounds=[]
guards=[(t,'0F071737')for t in [*range(0x32e,0x334),*range(0x35b,0x35f),0x3a1,0x3a2]]
guards +=[(t,'0F041625')for t in range(0x39b,0x3a1)]
for i,(t,pal)in enumerate(guards):
    name=f's23Rendered{i}';conditions.append(f'<condition>{name},tileAtPosition,128,16,{t:04X},{pal}')
    backgrounds.append(f'[{scope}&{name}]<background>Stage2_Cave_Background.png,1,0,0,11,0,0')

atlas.save(art/'Stage2_Vertical_Cave_Tiles_2x.png');atlas.save(pack/'Stage2_Vertical_Cave_Tiles_2x.png')
def section(kind,lines):return '# BEGIN SCREEN2_3 '+kind+'\n'+'\n'.join(lines)+'\n# END SCREEN2_3 '+kind+'\n'
end=text.index('\n',text.rfind('<img>'))+1
text=text[:end]+section('IMAGES',['<img>Stage2_Vertical_Cave_Tiles_2x.png'])+text[end:]
lines=text.splitlines(keepends=True);first=next(i for i,line in enumerate(lines)if'<tile>'in line or'<background>'in line)
lines[first:first]=[section('CONDITIONS',conditions),section('MAPPINGS',aliases+rules+backgrounds)]
(pack/'hires.txt').write_text(''.join(lines))
(art/'registration.json').write_text(json.dumps(dict(scope=scope,shared_aliases=len(aliases),new_tile_rules=len(rules),atlas_cells=len(cache),background_rules=len(backgrounds),
    existing_background_reused='Stage2_Cave_Background.png',background_scroll=[0,0],eye_size=[32,32],mappings=metadata,
    native_collision_modified=False,previous_artwork_modified=False),indent=2)+'\n')
print('Stage 2 vertical cave:',len(aliases),'shared aliases,',len(rules),'new tile mappings')
