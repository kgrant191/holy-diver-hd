"""Exact baseline recovery, geometry/alpha and ordered neighbor safety."""
from pathlib import Path
import hashlib,json,re
import numpy as np
from PIL import Image

ADDED={'Golden_Temple_Transition_2x.png','Thunder_Acquired.png'}
def strip(text):
    for section in ['IMAGES','CONDITIONS','MAPPINGS']:
        text,n=re.subn(r'^# BEGIN TEMPLE_TRANSITION '+section+r'\n.*?^# END TEMPLE_TRANSITION '+section+r'\n','',text,flags=re.M|re.S)
        assert n==1
    return text

def verify(root,pack):
    text=(pack/'hires.txt').read_text();reg=json.loads((root/'art/level4_transition/registration.json').read_text())
    prior=json.loads((root/'evidence/0.20.1-pack-sha256.json').read_text())
    assert {p.name for p in pack.iterdir()if p.is_file()}==set(prior)|ADDED
    for name,digest in prior.items():
        if name not in {'hires.txt','README.txt'}:assert hashlib.sha256((pack/name).read_bytes()).hexdigest()==digest,name
    old=strip(text);assert hashlib.sha256(old.encode()).hexdigest()==prior['hires.txt']
    old_lines=set(old.splitlines());lines=text.splitlines();positions={l:i for i,l in reversed(list(enumerate(lines)))};defs={l[11:].split(',')[0]:l[11:].split(',')[1:] for l in lines if l.startswith('<condition>')}
    images=[l[5:]for l in lines if l.startswith('<img>')];cache={}
    def cell(line):
        f=line.split('<tile>')[1].split(',');idx,x,y=int(f[0]),int(f[3]),int(f[4])
        if idx not in cache:cache[idx]=Image.open(pack/images[idx]).convert('RGBA')
        return np.array(cache[idx].crop((x,y,x+16,y+16)))
    step=np.array(Image.open(root/'art/level4_transition/ascending_step.png'))
    bottoms=[]
    for x in range(32):
        ys=np.flatnonzero(step[:,x,3]);bottoms.append(int(ys[-1]));assert (step[ys[0]:ys[-1]+1,x,3]==255).all()
    assert max(np.abs(np.diff(bottoms)))<=1 and bottoms[0]==31 and bottoms[-1]==19
    neighbors=0;stair_scopes=set()
    for m in reg['mappings']:
        line=m['rule'];assert line in positions
        if m['source_rule']:assert m['source_rule']in old_lines
        terms=line[1:line.index(']')].split('&');bounds=[0,255,0,239]
        for term in terms:
            d=defs.get(term.lstrip('!'))
            if not d:continue
            if d[0] in {'positionCheckX','positionCheckY'} and not term.startswith('!'):
                i=0 if d[0]=='positionCheckX' else 2;v=int(d[2])
                if d[1]=='>=':bounds[i]=max(bounds[i],v)
                elif d[1]=='>':bounds[i]=max(bounds[i],v+1)
                elif d[1]=='<':bounds[i+1]=min(bounds[i+1],v-1)
                elif d[1]=='<=':bounds[i+1]=min(bounds[i+1],v)
            if d[0]=='tileNearby':
                dx,dy=map(int,d[1:3]);assert 0<=bounds[0]+dx and bounds[1]+dx<256 and 0<=bounds[2]+dy and bounds[3]+dy<240,(line,d,bounds)
                neighbors+=1
        if m['kind']=='ascending stair underside':
            before,after=cell(m['source_rule']),cell(line)
            assert np.array_equal(before[:,:,:3],after[:,:,:3])
            key=int(line.split('<tile>')[1].split(',')[1],16)&255
            if key in [0x82,0x83]:assert np.array_equal(before,after)
            stair_scopes.add(m['source_rule'].split(']')[0])
            assert positions[line]<positions[m['source_rule']]
        if m['kind']=='dragon native white flash':
            before,after=cell(m['source_rule']),cell(line)
            assert np.array_equal(before[:,:,3],after[:,:,3]) and (after[:,:,:3]==255).all()
    assert len(stair_scopes)==9
    patterns=json.loads((root/'art/level4_transition/impact_native_patterns.json').read_text())
    impacts=[m for m in reg['mappings']if m['kind']=='boss initial impact']
    assert len(impacts)==4
    for key in range(0x60,0x64):assert patterns[f'{key:04X}']==patterns[f'{key+0xE00:04X}']
    return dict(tile_rules=reg['tile_rules'],conditions=reg['conditions'],background_rules=reg['background_rules'],prior_assets_exact=len(prior)-2,exact_previous_mapping_recovery=True,stair_rooms=len(stair_scopes),standing_surface_exact=True,dragon_alpha_exact=True,bounded_neighbor_conditions=neighbors,unsafe_reads=0)

if __name__=='__main__':
    root=Path(__file__).resolve().parents[1];print(json.dumps(verify(root,root/'build/Holy_Diver_(Tr)'),indent=2))
