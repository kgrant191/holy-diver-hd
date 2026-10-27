"""Scope/recovery, native alias, preserved geometry and neighbor safety checks."""
from pathlib import Path
import hashlib,json,re
import numpy as np
from PIL import Image
ADDED={'Tree_Potion_Cleanup_2x.png'}
def strip(text):
    for section in ['IMAGES','CONDITIONS','MAPPINGS']:
        text,n=re.subn(r'^# BEGIN TREE_POTION_CLEANUP '+section+r'\n.*?^# END TREE_POTION_CLEANUP '+section+r'\n','',text,flags=re.M|re.S);assert n==1
    return text
def verify(root,pack,content=None):
    text=content if content is not None else (pack/'hires.txt').read_text();prior=json.loads((root/'evidence/0.20.2-pack-sha256.json').read_text())
    assert {p.name for p in pack.iterdir()if p.is_file()}==set(prior)|ADDED
    for name,digest in prior.items():
        if name not in {'hires.txt','README.txt'}:assert hashlib.sha256((pack/name).read_bytes()).hexdigest()==digest,name
    old=strip(text);assert hashlib.sha256(old.encode()).hexdigest()==prior['hires.txt']
    reg=json.loads((root/'art/tree_potion_cleanup/registration.json').read_text());lines=text.splitlines();positions={l:i for i,l in reversed(list(enumerate(lines)))}
    defs={l[11:].split(',')[0]:l[11:].split(',')[1:]for l in lines if l.startswith('<condition>')}
    branches={'0122','0123','014D','014E','015B','015C','015D','015E'}
    trunk={f'{n:04X}'for n in [0x13f,0x140,0x147,0x148,0x141,0x142,0x149,0x14a,0x143,0x144,0x14b,0x14c,0x14f,0x150,0x151,0x152]}
    tested=0;neighbors=0
    for m in reg['mappings']:
        assert m['rule']in positions and m['tile']not in branches
        if m['kind']=='readable health jug':continue
        assert m['tile']in trunk and m['palette']=='0F071737'
        terms=m['rule'][1:m['rule'].index(']')].split('&');assert terms[:3]==['cleanupTreeMode','cleanupTreeLo','cleanupTreeHi']
        lo,hi,top,bottom=0,255,0,239
        for term in terms[3:]:
            d=defs[term]
            if d[0]=='positionCheckX':
                if d[1]=='>=':lo=max(lo,int(d[2]))
                else:assert d[1]=='<';hi=min(hi,int(d[2])-1)
            elif d[0]=='positionCheckY':
                if d[1]=='>=':top=max(top,int(d[2]))
                else:assert d[1]=='<';bottom=min(bottom,int(d[2])-1)
            else:
                assert d[0]=='tileNearby';dx,dy=map(int,d[1:3]);assert 0<=lo+dx<=hi+dx<256 and 0<=top+dy<=bottom+dy<240
                tested+=(hi-lo+1)*(bottom-top+1);neighbors+=1
        previous=[l for l in old.splitlines()if f'<tile>29,{m["tile"]},0F071737,'in l]
        assert previous and positions[m['rule']]<positions[previous[0]]
    jug=np.array(Image.open(root/'art/tree_potion_cleanup/health_jug.png').convert('RGBA'));assert jug.shape==(32,32,4) and set(np.unique(jug[:,:,3]))=={0,255}
    assert not jug[0,:,3].any()and not jug[-1,:,3].any()and not jug[:,0,3].any()and not jug[:,-1,3].any()
    identities=json.loads((root/'art/screen2_5_review/native_jug.json').read_text());expected={f'{int(first,16)+j:04X}'for first in identities['identical_groups']for j in range(4)}
    assert {m['tile']for m in reg['mappings']if m['kind']=='readable health jug'}==expected
    for side in ['left','right']:
        joined=np.array(Image.open(root/f'art/tree_potion_cleanup/{side}_whole_join.png').convert('RGBA'))
        assert ((joined[16:32,63,3]>0)&(joined[16:32,64,3]>0)).sum()>=4
    old_jug=np.array(Image.open(root/'art/screen2_5_review/health_jug.png').convert('RGBA'))
    bright=lambda im:int(((im[:,:,:3].min(2)>180)&(im[:,:,3]>0)).sum())
    assert bright(jug)>bright(old_jug)
    return dict(tile_rules=reg['tile_rules'],conditions=reg['conditions'],prior_assets_exact=len(prior)-2,exact_previous_mapping_recovery=True,branch_strips_and_standing_edges_exact=True,neighbor_rules=neighbors,bounded_probe_positions=tested,unsafe_reads=0,jug_alias_groups=len(identities['identical_groups']),jug_footprint=[32,32])
if __name__=='__main__':
    root=Path(__file__).resolve().parents[1];print(json.dumps(verify(root,root/'build/Holy_Diver_(Tr)'),indent=2))
