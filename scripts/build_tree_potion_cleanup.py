"""Join existing chapel branches to their trunk and brighten the health jug."""
from pathlib import Path
import hashlib,json
import numpy as np
from PIL import Image

r=Path(__file__).resolve().parents[1];p=r/'build/Holy_Diver_(Tr)';a=r/'art/tree_potion_cleanup';a.mkdir(exist_ok=True)
text=(p/'hires.txt').read_text();prior=json.loads((r/'evidence/0.20.2-pack-sha256.json').read_text())
assert hashlib.sha256(text.encode()).hexdigest()==prior['hires.txt'] and text.count('<img>')==56
atlas=Image.new('RGBA',(256,256));cells={};conditions=[];rules=[];records=[]
scope='cleanupTreeMode&cleanupTreeLo&cleanupTreeHi'
conditions+=['<condition>cleanupTreeMode,memoryCheckConstant,0072,==,04','<condition>cleanupTreeLo,memoryCheckConstant,0078,==,C2','<condition>cleanupTreeHi,memoryCheckConstant,0079,==,84']

def register(im,size):
    im=im.convert('RGBA').resize(size,Image.Resampling.LANCZOS)
    alpha=im.getchannel('A').point(lambda v:255 if v>=110 else 0)
    im=im.convert('RGB').quantize(colors=64).convert('RGBA');im.putalpha(alpha);return im

def tile(key,pal,im,terms,kind,extra=None):
    digest=hashlib.sha256(im.tobytes()).hexdigest()
    if digest not in cells:
        n=len(cells);xy=(n%16*16,n//16*16);assert xy[1]+16<=atlas.height
        cells[digest]=xy;atlas.paste(im,xy)
    x,y=cells[digest];line=('['+terms+']'if terms else '')+f'<tile>56,{key},{pal},{x},{y},1,N'
    rules.append(line);records.append(dict(rule=line,kind=kind,tile=key,palette=pal,xy=[x,y],**(extra or {})))

reg=json.loads((r/'art/screen1_4/registration.json').read_text())
original=Image.open(p/'Tree_Court_Tiles_2x.png').convert('RGBA')
trunk=[m for m in reg['mappings']if m['kind']=='tree repeat']
tree=Image.open(r/'art/layers/20_tree_and_branches.png').convert('RGBA')
body=Image.new('RGBA',(64,64))
for i,m in enumerate(trunk):
    x,y=m['atlas'];body.paste(original.crop((x,y,x+16,y+16)),(i%4*16,i//4*16))

# Restore the branch shoulders from the SAME original complete tree. Only
# the two adjacent trunk columns receive these context-specific registrations.
# Existing branch strips/standing edges and the rest of the tree remain exact.
for side,source_y,anchor in [('left',368,'014E'),('right',464,'015B')]:
    patch=np.array(register(tree.crop((286,source_y,354,source_y+48)),(64,48)))
    horizontal=np.clip((32-np.arange(64))/16,0,1) if side=='left' else np.clip((np.arange(64)-31)/16,0,1)
    vertical=np.minimum(np.clip(np.arange(48)/8,0,1),np.clip((47-np.arange(48))/8,0,1))
    weight=vertical[:,None]*horizontal[None,:]
    registered={}
    for i,m in enumerate(trunk):
        col=i%4
        if (side=='left'and col>=2)or(side=='right'and col<2):continue
        x,y=m['atlas'];base=np.array(original.crop((x,y,x+16,y+16)))
        for relative_row in [-1,0,1]:
            py=(relative_row+1)*16;px=col*16
            src=patch[py:py+16,px:px+16];w=weight[py:py+16,px:px+16];out=base.copy()
            both=(src[:,:,3]>0)&(base[:,:,3]>0)
            mix=w[:,:,None]*src[:,:,:3]+(1-w[:,:,None])*base[:,:,:3]
            out[:,:,:3][both]=np.rint(mix[both]).astype('uint8')
            added=(src[:,:,3]>0)&(base[:,:,3]==0)&(w>=.5)
            out[added]=src[added]
            if np.array_equal(out,base):continue
            im=Image.fromarray(out);name=f'cleanupJoin{side}{m["identity"]}_{relative_row+1}'
            dx=-(col+1)*8 if side=='left' else (4-col)*8;dy=-relative_row*8
            terms=[scope]
            for suffix,typ,op,value in [('X','positionCheckX','>='if dx<0 else '<',-dx if dx<0 else 256-dx),('Y','positionCheckY','>='if dy<0 else '<',-dy if dy<0 else 240-dy)]:
                bound=name+suffix;conditions.append(f'<condition>{bound},{typ},{op},{value}');terms.append(bound)
            conditions.append(f'<condition>{name},tileNearby,{dx},{dy},{anchor},0F071737');terms.append(name)
            tile(m['identity'],'0F071737',im,'&'.join(terms),'branch shoulder',dict(side=side,relative_row=relative_row,column=col,source_xy=m['atlas'],probe=[dx,dy,anchor]))
            registered[m['identity'],relative_row]=im
    # A complete source reference for the observed branch row (41/42/49/4A).
    whole=body.crop((0,0,64,48))
    for i,m in enumerate(trunk[:12]):
        im=registered.get((m['identity'],i//4-1))
        if im:whole.paste(im,(i%4*16,i//4*16))
    whole.save(a/f'{side}_shoulder.png')
    joined=Image.new('RGBA',(128,48));joined.paste(whole,(64 if side=='left' else 0,0))
    branch=Image.new('RGBA',(64,16))
    for j,m in enumerate(m for m in reg['mappings']if m['kind']==side+' branch'):
        x,y=m['atlas'];branch.paste(original.crop((x,y,x+16,y+16)),(j*16,0))
    joined.paste(branch,(0 if side=='left' else 64,16));joined.save(a/f'{side}_whole_join.png')

# Same original four-cell footprint and native alias groups. Bright ivory
# rims distinguish red liquid from the red cave without adding a floating halo.
raw=Image.open(r/'art/generated/cleanup_health_jug_generated.png').convert('RGBA')
bbox=raw.getchannel('A').point(lambda v:255 if v>=128 else 0).getbbox()
jug=register(raw.crop(bbox),(30,30));full=Image.new('RGBA',(32,32));full.paste(jug,(1,1));full.save(a/'health_jug.png')
identity=json.loads((r/'art/screen2_5_review/native_jug.json').read_text())
for first in identity['identical_groups']:
    for j in range(4):
        x,y=j%2*16,j//2*16;tile(f'{int(first,16)+j:04X}','FF301116',full.crop((x,y,x+16,y+16)),'','readable health jug')

def block(name,lines):return '# BEGIN TREE_POTION_CLEANUP '+name+'\n'+'\n'.join(lines)+'\n# END TREE_POTION_CLEANUP '+name+'\n'
end=text.index('\n',text.rfind('<img>'))+1;text=text[:end]+block('IMAGES',['<img>Tree_Potion_Cleanup_2x.png'])+text[end:]
lines=text.splitlines(keepends=True);first=next(i for i,l in enumerate(lines)if '<tile>'in l or '<background>'in l)
lines[first:first]=[block('CONDITIONS',conditions),block('MAPPINGS',rules)]
(p/'hires.txt').write_text(''.join(lines));atlas.save(p/'Tree_Potion_Cleanup_2x.png')
(a/'registration.json').write_text(json.dumps(dict(tile_rules=len(rules),conditions=len(conditions),atlas_cells=len(cells),mappings=records,tree_scope='84C2/mode04',branch_strips_unchanged=True,prior_assets_modified=False,native_gameplay_modified=False),indent=2)+'\n')
print('Tree/potion cleanup:',len(rules),'rules;',len(conditions),'conditions;',len(cells),'cells')
