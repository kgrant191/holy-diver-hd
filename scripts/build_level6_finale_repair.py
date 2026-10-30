"""Register the requested face, blue slime, visible portal and ending repairs."""
from pathlib import Path
import json, hashlib, colorsys, re
import numpy as np
from PIL import Image, ImageOps
from scipy.ndimage import label

R=Path(__file__).resolve().parents[1]; P=R/'build/Holy_Diver_(Tr)'; A=R/'art/level6_finale_repair'; G=R/'art/generated'
text=(P/'hires.txt').read_text(); prior=json.loads((R/'evidence/0.30.0-pack-sha256.json').read_text())
assert hashlib.sha256(text.encode()).hexdigest()==prior['hires.txt']
old=json.loads((R/'art/level6_finale/registration.json').read_text()); organic=json.loads((R/'art/level6_enemy_revision/registration.json').read_text())
# These older A3AF rules occur before the finale image declarations. Mark only
# their face entries inactive so the later repair can win without moving image
# indices or changing the eight approved green-blob mappings. Strip restores them.
superseded=[e['rule']for e in organic['mappings']if e['kind']=='wall face color']
assert len(superseded)==171
for rule in superseded:
    assert text.count(rule+'\n')==1
    text=text.replace(rule+'\n','# LEVEL6_FINALE_REPAIR SUPERSEDED '+rule+'\n',1)
inv=json.loads((R/'art/level6_finale/inventory.json').read_text()); index=70
images=[l[5:]for l in text.splitlines()if l.startswith('<img>')]; assert len(images)==index
atlas=Image.new('RGBA',(1024,512)); rules=[]; conditions=[]; mappings=[]; probes=[]; cache={}
empty=Image.new('RGBA',(16,16)); scopes=old['scopes']

def registered(raw,size):
    raw=raw.convert('RGBA'); box=raw.getchannel('A').point(lambda x:255 if x>=160 else 0).getbbox()
    im=raw.crop(box).resize(size,Image.Resampling.LANCZOS); alpha=im.getchannel('A').point(lambda x:255 if x>=160 else 0)
    im=im.convert('RGB').quantize(colors=192,dither=Image.Dither.NONE).convert('RGBA');im.putalpha(alpha);return im

def emit(tile,palette,im,scope,kind,brightness=1):
    key=im.tobytes()
    if key not in cache:
        n=len(cache);xy=(n%64*16,n//64*16);assert xy[1]<512;cache[key]=xy;atlas.paste(im,xy)
    x,y=cache[key];rule=f'[{scope}]<tile>{index},{tile:04X},{palette},{x},{y},{brightness},N';rules.append(rule)
    mappings.append(dict(tile=f'{tile:04X}',palette=palette,xy=[x,y],scope=scope,kind=kind,rule=rule))

def anchor(dx,dy,tile,prefix):
    terms=[]
    for suffix,typ,op,v in [('L','positionCheckX','>=',max(0,-dx)),('R','positionCheckX','<',min(256,256-dx)),('T','positionCheckY','>=',max(0,-dy)),('B','positionCheckY','<',min(240,240-dy))]:
        name=prefix+suffix;conditions.append(f'<condition>{name},{typ},{op},{v}');terms.append(name)
    name=prefix+'Anchor';conditions.append(f'<condition>{name},tileNearby,{dx},{dy},{tile:04X},0F162638,Y');terms.append(name)
    probes.append(dict(dx=dx,dy=dy,tile=f'{tile:04X}',terms=terms));return '&'.join(terms)

# Register the user's entire clean reference. No wall material underlay and no
# inherited wall alpha. Repeated left-column identities get row-specific anchors.
face=registered(Image.open(A/'wall_face_reference.png'),(48,128));face.save(A/'wall_face.png')
layout=organic['face_layout']; pals=sorted({e['palette']for e in organic['mappings']if e['kind']=='wall face color'})
for y,row in enumerate(layout):
    for x,t in enumerate(row):
        terms=anchor(8,0,row[x+1],f'finaleRepairFace{y}')if x==0 and sum(rr.count(t)for rr in layout)>1 else ''
        for scope in [organic['scope'],scopes['A49F']]:
            for pal in pals:emit(t,pal,face.crop((x*16,y*16,x*16+16,y*16+16)),scope+('&'+terms if terms else ''),'clean wall face')

# Same two mucus poses, now in the native blue enemy palette.
raw=Image.open(G/'level6_blue_blob.png').convert('RGBA')
for i in range(2):
    im=registered(raw.crop((i*raw.width//2,0,(i+1)*raw.width//2,raw.height)),(32,32));im.save(A/f'blue_blob{i}.png')
    for j in range(4):emit(0x1a9c+i*4+j,'FF110130',im.crop((j%2*16,j//2*16,j%2*16+16,j//2*16+16)),scopes['A49F'],'blue mucus blob')

# The four-by-six blank native cells above the final ledge are the doorway.
# Two different physical anchors prevent ordinary shaft recesses matching it.
portal=registered(Image.open(G/'level6_boss_portal.png'),(64,96));portal.save(A/'portal.png')
for y in range(6):
    for x in range(4):
        xx,yy=112+x*8,32+y*8
        terms=anchor(112-xx,16-yy,0x1bd3,f'finaleRepairPortal{x}_{y}Top')+'&'+anchor(96-xx,32-yy,0x1b2d,f'finaleRepairPortal{x}_{y}Side')
        for pal in ['0F162638','30162638','31162638']:
            emit(0x1b00,pal,portal.crop((x*16,y*16,x*16+16,y*16+16)),scopes['A49F']+'&'+terms,'boss entrance')
# Native activation shutters are three flat panels. Keep the registered portal
# visible during their existing activation sequence, without changing OAM/timing.
for e in inv['sprites']['A49F']:
    if 0x1aa9<=int(e['tile'],16)<=0x1aac:emit(int(e['tile'],16),e['palette'],empty,scopes['A49F'],'entrance activation')

# Whole connected dragon paintings; never compress individual image scanlines.
raw=Image.open(G/'level6_ending_dragon_repair.png').convert('RGBA'); shared={}; dragon_report=[]
for i,layout in enumerate(old['ending_layouts']):
    # Generation has unequal-height poses separated by a transparent band.
    part=raw.crop((0,0,raw.width,760))if i==0 else raw.crop((0,760,raw.width,raw.height))
    size=(128,64 if i==0 else 48)
    if i==0:im=registered(part,size)
    else:
        im=Image.new('RGBA',size);im.paste(registered(part,(128,40)),(0,8))
    arr=np.array(im);mask=np.zeros((size[1],size[0]),bool)
    for t,x,y in layout:mask[y*2:y*2+16,x*2:x*2+16]=True
    trimmed=int(((arr[:,:,3]>0)&~mask).sum());arr[~mask]=0;im=Image.fromarray(arr)
    for t,x,y in layout:
        if t in shared:im.paste(shared[t],(x*2,y*2))
        else:shared[t]=im.crop((x*2,y*2,x*2+16,y*2+16))
    im.save(A/f'ending_dragon{i}.png');components,n=label(np.array(im)[:,:,3]>0,np.ones((3,3)));counts=np.bincount(components.ravel())[1:]
    dragon_report.append(dict(trimmed_edge_pixels=trimmed,largest_connected_fraction=float(counts.max()/counts.sum())))
seen=set()
palettes=sorted({e['palette']for e in old['mappings']if e['kind']=='ending dragon'})
for i,layout in enumerate(old['ending_layouts']):
    im=Image.open(A/f'ending_dragon{i}.png').convert('RGBA')
    for t,x,y in layout:
        if t in seen:continue
        seen.add(t);base=im.crop((x*2,y*2,x*2+16,y*2+16))
        for pal in palettes:
            cell=base;bri=.35 if pal=='FF090F17'else 1
            if pal not in ['FF190927','FF090F17']:
                hue=int(pal[2:4],16)&15;rgb=colorsys.hsv_to_rgb(((hue-1)*30+225)%360/360,.8,1)
                cell=ImageOps.colorize(ImageOps.grayscale(base),tuple(int(10*v)for v in rgb),tuple(int(100+155*v)for v in rgb)).convert('RGBA');cell.putalpha(base.getchannel('A'))
            emit(0x1e00+t,pal,cell,scopes['B01C'],'connected ending dragon',bri)

# The original HD font atlases have opaque black cell backgrounds. Only clear
# their black ink in ending scope; all colored glyph pixels remain byte-exact.
loaded={};font_sources=[]
for line in text.splitlines():
    if not line.startswith('<tile>'):continue
    f=line[6:].split(',');tile=int(f[1],16);aid=int(f[0])
    if not(0x1f00<=tile<=0x1fff and 10<=aid<=17 and not f[2].startswith('FF')):continue
    if aid not in loaded:loaded[aid]=Image.open(P/images[aid]).convert('RGBA')
    x,y=int(f[3]),int(f[4]);cell=loaded[aid].crop((x,y,x+16,y+16));a=np.array(cell);black=(a[:,:,:3]==0).all(2);a[black,3]=0
    emit(tile,f[2],Image.fromarray(a),scopes['B01C'],'ending transparent text',float(f[5]));font_sources.append(line)

def block(part,entries):return '# BEGIN LEVEL6_FINALE_REPAIR '+part+'\n'+'\n'.join(entries)+'\n# END LEVEL6_FINALE_REPAIR '+part+'\n'
at=text.index('# END LEVEL6_FINALE IMAGES\n')+len('# END LEVEL6_FINALE IMAGES\n');text=text[:at]+block('IMAGES',['<img>Final_Citadel_Finale_Repair_2x.png'])+text[at:]
at=text.index('# END LEVEL6_FINALE CONDITIONS\n')+len('# END LEVEL6_FINALE CONDITIONS\n');text=text[:at]+block('CONDITIONS',conditions)+block('MAPPINGS',rules)+text[at:]
(P/'hires.txt').write_text(text);atlas.save(P/'Final_Citadel_Finale_Repair_2x.png');atlas.save(A/'Final_Citadel_Finale_Repair_2x.png')
(A/'registration.json').write_text(json.dumps(dict(atlas_index=index,mappings=mappings,conditions=conditions,probes=probes,dragon=dragon_report,font_sources=font_sources,face_layout=organic['face_layout'],ending_layouts=old['ending_layouts']),indent=2)+'\n')
print('Finale repairs:',len(rules),'rules;',len(cache),'cells;',dragon_report)
