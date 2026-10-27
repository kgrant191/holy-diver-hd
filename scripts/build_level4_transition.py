"""Complete temple stairs, Thunder acquisition, tower fade and dragon flash."""
from pathlib import Path
import hashlib, json, re
import numpy as np
from PIL import Image, ImageOps, ImageDraw, ImageFont

r = Path(__file__).resolve().parents[1]
p = r/'build/Holy_Diver_(Tr)'
a = r/'art/level4_transition'
a.mkdir(exist_ok=True)
text = (p/'hires.txt').read_text()
prior = json.loads((r/'evidence/0.20.1-pack-sha256.json').read_text())
assert hashlib.sha256(text.encode()).hexdigest() == prior['hires.txt']
images = [l[5:] for l in text.splitlines() if l.startswith('<img>')]
assert len(images) == 55
defs = {l[11:].split(',')[0]:l[11:].split(',') for l in text.splitlines() if l.startswith('<condition>')}
conditions, rules, backgrounds, records = [], [], [], []
atlas = Image.new('RGBA', (512,256))
cells, image_cache, condition_cache = {}, {}, {}

def source(fields):
    idx,x,y = int(fields[0]),int(fields[3]),int(fields[4])
    if idx not in image_cache: image_cache[idx] = Image.open(p/images[idx]).convert('RGBA')
    return image_cache[idx].crop((x,y,x+16,y+16))

def tile(key,pal,im,scope,kind,source_rule=None):
    digest = hashlib.sha256(im.tobytes()).hexdigest()
    if digest not in cells:
        i=len(cells); xy=(i%32*16,i//32*16)
        assert xy[1]+16 <= atlas.height
        cells[digest]=xy; atlas.paste(im,xy)
    x,y=cells[digest]
    line=f'[{scope}]<tile>55,{key},{pal},{x},{y},1,N'
    rules.append(line)
    records.append(dict(rule=line,kind=kind,source_rule=source_rule))
    return line

def condition(term, palettes=None):
    """Copy dependencies before use, preserving original ordered bounds."""
    palettes = palettes or {}
    neg='!' if term.startswith('!') else ''; name=term.lstrip('!')
    if name in {'hmirror','vmirror','bgpriority'}: return term
    key=(name,tuple(sorted(palettes.items())))
    if key not in condition_cache:
        f=defs[name].copy(); new='transitionC'+str(len(condition_cache))
        condition_cache[key]=new; f[0]=new
        if f[1] in {'spriteNearby','tileNearby','tileAtPosition'} and f[-1] in palettes: f[-1]=palettes[f[-1]]
        conditions.append('<condition>'+','.join(f))
    return neg+condition_cache[key]

def scope(room,mode):
    names=[]
    for label,addr,value in [('Mode',0x72,mode),('Lo',0x78,int(room,16)&255),('Hi',0x79,int(room,16)>>8)]:
        name='transition'+room+label
        conditions.append(f'<condition>{name},memoryCheckConstant,{addr:04X},==,{value:02X}')
        names.append(name)
    return '&'.join(names)

boss=scope('AFA9',4); flight=scope('AFE5',4)

# The earlier assembly assumed the wrong ascending layout. Recorded live
# nametables prove 82,83 / 84,85. Preserve its complete upper half and RGB.
ascending=Image.new('RGBA',(32,32))
for j,key in enumerate(['0B82','0B83','0B84','0B85']):
    line=next(l for l in text.splitlines() if re.search(r'<tile>48,'+key+r',0F172737,',l))
    ascending.paste(source(line.split('<tile>')[1].split(',')),(j%2*16,j//2*16))
old=np.array(ascending); step=old.copy()
for x in range(32):
    bottom=31-(12*x+15)//31
    step[16:,x,3]=0; step[16:bottom+1,x,3]=255
assert np.array_equal(old[:16],step[:16]) and np.array_equal(old[:,:,:3],step[:,:,:3])
ascending=Image.fromarray(step); ascending.save(a/'ascending_step.png')
seen=set()
for line in text.splitlines():
    m=re.fullmatch(r'\[([^]]+)\]<tile>48,(0[BD]8[2345]),([^,]+),(\d+),(\d+),1,N',line)
    if not m or line in seen: continue
    seen.add(line)
    # Only physical masonry source rules. Window/wall clear rules are separate.
    terms='&'.join(condition(t) for t in m[1].split('&'))
    j=int(m[2][-2:],16)-0x82
    tile(m[2],m[3],ascending.crop((j%2*16,j//2*16,j%2*16+16,j//2*16+16)),terms,'ascending stair underside',line)

# Register a complete new tome inside the original four-cell pickup footprint.
raw=Image.open(r/'art/generated/temple_thunder_generated.png').convert('RGBA')
raw=raw.crop(raw.getchannel('A').getbbox())
book=Image.new('RGBA',(32,32)); fitted=ImageOps.contain(raw,(30,30),Image.Resampling.LANCZOS)
book.paste(fitted,((32-fitted.width)//2,(32-fitted.height)//2))
pixels=np.array(book); pixels[:,:,3]=np.where(pixels[:,:,3]>=96,255,0)
book=Image.fromarray(pixels); book.save(a/'thunder_tome.png')
for j,key in enumerate(['0E8F','0E90','0E91','0E92']):
    tile(key,'FF301116',book.crop((j%2*16,j//2*16,j%2*16+16,j//2*16+16)),boss,'Thunder tome')

# The first impact phase precedes the already shared expanding gold rings.
# Native CHR bytes for 0E60–63 equal 0060–63 (retained provenance table).
for key in range(0x60,0x64):
    line=next(l for l in text.splitlines() if re.search(r'<tile>28,'+f'{key:04X}'+r',FF301116,',l))
    fields=line.split('<tile>')[1].split(',');fields[1]=f'{key+0xE00:04X}'
    new=f'[{boss}]<tile>'+','.join(fields)
    rules.append(new);records.append(dict(rule=new,source_rule=line,kind='boss initial impact'))

# Native palettes change during pickup flashes and three fade steps. Clone
# complete ordered pose signatures, including every neighbor palette.
normal_bg=['0F071727','0F071737','0F031323','0F001030']
normal_sp=['FF26173A','FF172737','FF301116','FF221136','FF300036']
phases=[
    ('flash',dict(zip(normal_bg,['31071727','31071737','31031323','31001030'])),1),
    ('fade1',dict(zip(normal_bg+normal_sp,['0F0F0717','0F0F0727','0F0F0313','0F0F0020','FF16072A','FF071727','FF200106','FF120126','FF200F26'])),.65),
    ('fade2',dict(zip(normal_bg+normal_sp,['0F0F0F07','0F0F0F17','0F0F0F03','0F0F0F10','FF060F1A','FF0F0717','FF100F0F','FF020F16','FF100F16'])),.30),
    ('fade3',dict(zip(normal_bg+normal_sp,['0F0F0F0F','0F0F0F07','0F0F0F0F','0F0F0F00','FF0F0F0A','FF0F0F07','FF000F0F','FF0F0F06','FF000F06'])),.12),
]
for label,palettes,brightness in phases:
    guard='transition'+label+'LastColor'
    value={'flash':0x30,'fade1':0x20,'fade2':0x10,'fade3':0x00}[label]
    conditions.append(f'<condition>{guard},ppuMemoryCheckConstant,3F0F,==,{value:02X}')
    for line in text.splitlines():
        m=re.fullmatch(r'(?:\[([^]]+)\])?<tile>(.*)',line)
        if not m: continue
        head=m[1] or ''; f=m[2].split(','); key=int(f[1],16)
        if f[2] not in palettes or not (0xE00<=key<=0xEB7 or 0xF00<=key<=0xFFF): continue
        # Only actual tower rules or shared actors. Exclude other room scopes.
        room_checks=[defs[t.lstrip('!')] for t in head.split('&') if t and t.lstrip('!') in defs and defs[t.lstrip('!')][1]=='memoryCheckConstant' and int(defs[t.lstrip('!')][2],16) in [0x72,0x78,0x79]]
        if key>=0xF00 and 'finaleAFA9Mode' not in head: continue
        if key<0xF00 and room_checks and 'finaleAFA9Mode' not in head: continue
        terms=[boss,guard]+[condition(t,palettes) for t in head.split('&') if t]
        result=f.copy();result[2]=palettes[f[2]];result[5]=str(float(f[5])*brightness)
        new='['+'&'.join(terms)+']<tile>'+','.join(result)
        rules.append(new);records.append(dict(rule=new,source_rule=line,kind='boss '+label))
    # Retain the subdued hall through normal fade steps. The universal flash
    # and fully black native frame deliberately have no panorama override.
    if label!='flash':
        for line in text.splitlines():
            if not line.startswith('[finaleAFA9Mode&') or '<background>' not in line: continue
            head,body=line[1:].split(']<background>');args=body.split(',')
            terms=[guard]+[condition(t,palettes) for t in head.split('&')]
            args[1]=str(float(args[1])*brightness)
            backgrounds.append('['+'&'.join(terms)+']<background>'+','.join(args))

# Flight ends with a native white silhouette. Preserve its cadence, using
# exactly the finished dragon's alpha and registered whole-pose cell layout.
for line in text.splitlines():
    m=re.fullmatch(r'(?:\[([^]]+)\])?<tile>(.*)',line)
    if not m: continue
    f=m[2].split(',')
    if not 0xE93<=int(f[1],16)<=0xEAE or f[2]!='FF190927': continue
    assert not m[1], 'Dragon aliases are shared native identities'
    arr=np.array(source(f));arr[:,:,:3]=255
    tile(f[1],'FF303030',Image.fromarray(arr),flight,'dragon native white flash',line)

# Exact native THUNDER word and rendered identity exclude blank transitions.
terms=[condition(t) for t in ['cardPal1','cardPal2','cardPal3','cardRendering']]
for j,value in enumerate([0x35,0x27,0x36,0x2d,0x23,0x24,0x33]):
    name='transitionThunderWord'+str(j)
    conditions.append(f'<condition>{name},ppuMemoryCheckConstant,{0x21CD+j:04X},==,{value:02X}');terms.append(name)
conditions.append('<condition>transitionThunderRendered,tileAtPosition,104,112,1F35,0F213029')
terms.append('transitionThunderRendered');card_scope='&'.join(terms)
card=Image.open(p/'Intermission_HD.png').convert('RGBA');draw=ImageDraw.Draw(card)
for label,y,size,color in [('SPELL ACQUIRED',164,16,'#cbaa73'),('THUNDER',205,30,'#ffe1ab')]:
    draw.text((256,y),label,font=ImageFont.truetype(str(r/'art/fonts/DejaVuSerif-Bold.ttf'),size),fill=color,anchor='mt',stroke_width=1,stroke_fill='#050e20')
card.save(p/'Thunder_Acquired.png')
backgrounds.append(f'[{card_scope}]<background>Thunder_Acquired.png,1,0,0,12,0,0')
for t in [0,*range(0x10,0x40)]: tile(f'{0x1f00+t:04X}','0F213029',Image.new('RGBA',(16,16)),card_scope,'clear native Thunder announcement')

def block(name,lines): return '# BEGIN TEMPLE_TRANSITION '+name+'\n'+'\n'.join(lines)+'\n# END TEMPLE_TRANSITION '+name+'\n'
end=text.index('\n',text.rfind('<img>'))+1
text=text[:end]+block('IMAGES',['<img>Golden_Temple_Transition_2x.png'])+text[end:]
lines=text.splitlines(keepends=True)
first=next(i for i,l in enumerate(lines) if '<tile>' in l or '<background>' in l)
lines[first:first]=[block('CONDITIONS',conditions),block('MAPPINGS',rules+backgrounds)]
(p/'hires.txt').write_text(''.join(lines));atlas.save(p/'Golden_Temple_Transition_2x.png')
(a/'registration.json').write_text(json.dumps(dict(tile_rules=len(rules),conditions=len(conditions),background_rules=len(backgrounds),mappings=records,backgrounds=backgrounds,palette_phases=phases,atlas_cells=len(cells),native_gameplay_modified=False,prior_assets_modified=False),indent=2)+'\n')
print('Temple transition:',len(rules),'rules;',len(conditions),'conditions;',len(cells),'cells')
