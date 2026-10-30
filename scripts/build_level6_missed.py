"""Finish the red corridor and two purple rooms without changing native gameplay."""
from pathlib import Path
import hashlib, json
import numpy as np
from PIL import Image
from verify_level6_opening_rules import native_hull

R=Path(__file__).resolve().parents[1];P=R/'build/Holy_Diver_(Tr)';A=R/'art/level6_missed'
text=(P/'hires.txt').read_text();prior=json.loads((R/'evidence/0.30.1-pack-sha256.json').read_text())
assert hashlib.sha256(text.encode()).hexdigest()==prior['hires.txt']
lines=text.splitlines();images=[l[5:]for l in lines if l.startswith('<img>')];index=len(images);assert index==71
patterns={int(k,16):bytes.fromhex(v)for k,v in json.loads((A/'native_patterns.json').read_text()).items()}
inv=json.loads((A/'inventory.json').read_text());opening=json.loads((R/'art/level6_opening/registration.json').read_text())
variety=json.loads((R/'art/level6_variety/registration.json').read_text())
defs={l[11:].split(',')[0]:l[11:].split(',')[1:]for l in lines if l.startswith('<condition>')}
conditions=[];rules=[];records=[];clones=[];backgrounds=[];scopes={};cache={};dependencies={};atlas=Image.new('RGBA',(512,256))
for room,mode in [('9CA7',0x0c),('9D5B',0x08),('9DD3',0x18)]:
    terms=[]
    for suffix,addr,value in [('Mode',0x72,mode),('Lo',0x78,int(room,16)&255),('Hi',0x79,int(room,16)>>8)]:
        name='citadelMissed'+room+suffix;conditions.append(f'<condition>{name},memoryCheckConstant,{addr:04X},==,{value:02X}');terms.append(name)
    scopes[room]='&'.join(terms)
def hull(t):return Image.fromarray(native_hull(patterns[t]).astype(np.uint8)*255)
def emit(t,pal,im,room,kind):
    digest=hashlib.sha256(im.tobytes()).hexdigest()
    if digest not in cache:
        slot=len(cache);xy=(slot%32*16,slot//32*16);assert xy[1]<256;cache[digest]=xy;atlas.paste(im,xy)
    x,y=cache[digest];rule=f'[{scopes[room]}]<tile>{index},{t:04X},{pal},{x},{y},1,N';rules.append(rule)
    records.append(dict(tile=f'{t:04X}',palette=pal,xy=[x,y],room=room,scope=scopes[room],kind=kind,rule=rule))
def dependency(term):
    neg='!'if term.startswith('!')else'';name=term.lstrip('!')
    if name in ['hmirror','vmirror','bgpriority']:return term
    if name not in dependencies:
        new='citadelMissedReuse'+str(len(dependencies));dependencies[name]=new
        assert defs[name][0]!='tileNearby','No new neighbor probes'
        conditions.append('<condition>'+new+','+','.join(defs[name]))
    return neg+dependencies[name]
def clone(source,t,pal,room,kind,terms=()):
    f=source.split('<tile>')[1].split(',');assert patterns[int(f[1],16)]==patterns[t]
    f[1]=f'{t:04X}';f[2]=pal;scope='&'.join([scopes[room]]+[dependency(n)for n in terms]);rule=f'[{scope}]<tile>'+','.join(f)
    rules.append(rule);clones.append(dict(source_rule=source,rule=rule,room=room,kind=kind,source_terms=list(terms)))

# Register whole material groups, including the measured repeating ceiling lip.
purple=Image.open(R/'art/generated/level6_violet_stone.png').convert('RGB').resize((64,64),Image.Resampling.LANCZOS).quantize(colors=96).convert('RGBA');purple.save(A/'violet_material.png')
red=Image.open(R/'art/level6_variety/red_material.png').convert('RGBA')
groups={'brick':opening['groups']['brick'],
        'ceiling_body':[[0x1778,0x1779],[0x177a,0x177b]],
        'ceiling_lip':[[0x1775,0x1776],[None,0x1777]],
        'ceiling_corner':[[0x177c,0x177d],[0x177e,0x177f]],
        'hanging_edge':[[0x1789,0x178a],[0x178b,0x178c]],
        'wall_left':[[0x1744,0x1745],[0x1748,0x1749]],
        'wall_middle':[[0x1746,0x1747],[0x174a,0x174b]],
        'wall_right':[[0x174c,0x174d],[0x174e,0x174f]]}
cells={}
for name,layout in groups.items():
    im=purple.crop((0,0,len(layout[0])*16,len(layout)*16));mask=Image.new('L',im.size)
    for y,row in enumerate(layout):
        for x,t in enumerate(row):
            if t is not None:mask.paste(hull(t),(x*16,y*16))
    im.putalpha(mask);im.save(A/f'violet_{name}.png')
    for y,row in enumerate(layout):
        for x,t in enumerate(row):
            if t is not None:cells[t]=im.crop((x*16,y*16,x*16+16,y*16+16))
redbrick=red.crop((0,0,32,32));mask=Image.new('L',(32,32))
for y,row in enumerate(groups['brick']):
    for x,t in enumerate(row):mask.paste(hull(t),(x*16,y*16))
redbrick.putalpha(mask);redbrick.save(A/'red_brick.png')
empty=Image.new('RGBA',(16,16));solid={};wall={}
for room in scopes:
    # Red corridor and its incoming transition; keep accepted ivory ornaments.
    for phase in ['0F','30','31']:
        for suffix in ['061636']+(['072830']if room=='9CA7'else[]):
            for y,row in enumerate(groups['brick']):
                for x,t in enumerate(row):
                    for shift in [0,0x200]:emit(t+shift,phase+suffix,redbrick.crop((x*16,y*16,x*16+16,y*16+16)),room,'red brick')
    if room=='9CA7':continue
    solid[room]=sorted({int(t,16)for pal in ['0F051433','0F072830']for t in inv['visible_backgrounds'][room].get(pal,{})}-{0x1700})
    wall[room]=sorted({int(t,16)for pal in ['0F011121','0F172737']for t in inv['visible_backgrounds'][room].get(pal,{})})
    for phase in ['0F','30','31']:
        for suffix in ['051433','072830']:
            for shift in [0,0x200]:emit(0x1700+shift,phase+suffix,empty,room,'empty space')
            for t in solid[room]:
                im=cells.get(t)
                if im is None:
                    x,y=t%4*16,t//4%4*16;im=purple.crop((x,y,x+16,y+16));im.putalpha(hull(t))
                for shift in [0,0x200]:emit(t+shift,phase+suffix,im,room,'violet structure')
        for suffix in ['011121','172737']:
            for t in wall[room]:
                for shift in [0,0x200]:emit(t+shift,phase+suffix,empty,room,'distant blue wall')

# Exact finished eyes, including the palette missing from the earlier corridor.
for room in scopes:
    for j in range(6):
        pal='FF060C30'if j<4 else'FF301116';src=0x02d8+j;dst=0x16f8+j
        source=next(l for l in lines if l.startswith(f'<tile>34,{src:04X},{pal},'))
        clone(source,dst,pal,room,'returning eye and tear')
    # The dragon flash retains the accepted green source, including every cell.
    dragon_sources={e['tile']:e['source_rule']for e in opening['clones']if e['palette']=='FF190927'and 0x169c<=int(e['tile'],16)<=0x16b7}
    for tile,source in sorted(dragon_sources.items()):
        dst=int(tile,16)
        clone(source,dst,'FF300036',room,'dragon pickup flash')
    for j in range(13):
        src=0x10db+j;dst=0x16d8+j
        source=next(l for l in lines if l.startswith(f'<tile>57,{src:04X},FF0B2B30,'))
        clone(source,dst,'FF160636',room,'returning serpent')

# Copy the complete ordered earlier room layer, preserving animation conditions.
donor=opening['scopes']['9CA7']
donors=[l for l in lines if l.startswith('['+donor)and'<tile>'in l]
for room in ['9D5B','9DD3']:
    # Incoming red terrain follows the accepted red corridor until palette change.
    redscope=variety['scopes']['9CA7']
    for source in lines:
        if source.startswith('['+redscope+']<tile>'):
            f=source.split('<tile>')[1].split(',')
            if f[2][2:]=='061636':clone(source,int(f[1],16),f[2],room,'incoming red terrain')
    for source in donors:
        f=source.split('<tile>')[1].split(',');terms=source.split(']')[0][1:].split('&')[3:]
        clone(source,int(f[1],16),f[2],room,'complete earlier room rule',terms)

styles={'9CA7':('Crimson_Gallery','level6_crimson_gallery'),'9D5B':('Violet_Chapel','level6_violet_chapel'),'9DD3':('Amethyst_Arcade','level6_amethyst_arcade')}
for style,source in styles.values():
    im=Image.open(R/f'art/generated/{source}.png').convert('RGBA').resize((512,480),Image.Resampling.LANCZOS);im.save(P/f'Final_Citadel_{style}.png')
    flash=im.copy();flash.putalpha(176);flash.save(P/f'Final_Citadel_{style}_Flash.png')
guard_palettes=['051433','061636','060616','161606','122131','011121','071727','072830','071737','172737','081030','1B2B3B']
for room in scopes:
    for phase in ['0F','30','31']:
        for suffix in guard_palettes:
            pal=phase+suffix
            for base in [0x1700,0x1900]:
                for t in range(base,base+256):
                    name=f'citadelMissedView{room}_{t:04X}_{pal}';conditions.append(f'<condition>{name},tileAtPosition,128,16,{t:04X},{pal}')
                    style='Crimson_Gallery'if room=='9D5B'and suffix=='061636'else styles[room][0]
                    image=f'Final_Citadel_{style}'+('_Flash'if phase!='0F'else'')+'.png'
                    backgrounds.append(f'[{scopes[room]}&{name}]<background>{image},1,0,0,1,0,0')
def block(part,items):return '# BEGIN LEVEL6_MISSED '+part+'\n'+'\n'.join(items)+'\n# END LEVEL6_MISSED '+part+'\n'
# All 71 older image declarations precede this anchor. Every copied dependency
# is declared in our block, so the new first-match overrides can go here safely.
anchor='# END LEVEL6_FINALE_REPAIR IMAGES\n';at=text.index(anchor)+len(anchor)
text=text[:at]+block('IMAGES',['<img>Final_Citadel_Missed_2x.png'])+block('CONDITIONS',conditions)+block('MAPPINGS',rules+backgrounds)+text[at:]
(P/'hires.txt').write_text(text);atlas.save(P/'Final_Citadel_Missed_2x.png');atlas.save(A/'Final_Citadel_Missed_2x.png')
(A/'registration.json').write_text(json.dumps(dict(atlas_index=index,atlas_cells=len(cache),scopes=scopes,conditions=conditions,mappings=records,clones=clones,backgrounds=backgrounds,styles=styles,guard_palettes=guard_palettes,solid_tiles=solid,wall_tiles=wall,groups=groups,dependencies=dependencies),indent=2)+'\n')
print('Level 6 missed:',len(rules),'tiles;',len(backgrounds),'backgrounds;',len(cache),'atlas cells')
