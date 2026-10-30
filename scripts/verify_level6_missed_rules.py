"""Check complete native hulls, exact reuse, palette coverage and reversibility."""
from pathlib import Path
import hashlib,json,re,tempfile,shutil,subprocess,sys
import numpy as np
from PIL import Image
from verify_level6_opening_rules import native_hull

NEW={'Final_Citadel_Missed_2x.png'}|{f'Final_Citadel_{s}{f}.png'for s in ['Crimson_Gallery','Violet_Chapel','Amethyst_Arcade']for f in ['','_Flash']}
def strip(text):
    for part in ['IMAGES','CONDITIONS','MAPPINGS']:
        text,n=re.subn(r'^# BEGIN LEVEL6_MISSED '+part+r'\n.*?^# END LEVEL6_MISSED '+part+r'\n','',text,flags=re.M|re.S);assert n==1
    return text
def verify(root,pack):
    prior=json.loads((root/'evidence/0.30.1-pack-sha256.json').read_text());text=(pack/'hires.txt').read_text();old=strip(text)
    assert hashlib.sha256(old.encode()).hexdigest()==prior['hires.txt']
    assert {p.name for p in pack.iterdir()if p.is_file()}==set(prior)|NEW
    for name,digest in prior.items():
        if name not in ['hires.txt','README.txt']:assert hashlib.sha256((pack/name).read_bytes()).hexdigest()==digest,name
    art=root/'art/level6_missed';reg=json.loads((art/'registration.json').read_text());patterns={int(k,16):bytes.fromhex(v)for k,v in json.loads((art/'native_patterns.json').read_text()).items()}
    atlas=Image.open(pack/'Final_Citadel_Missed_2x.png').convert('RGBA');assert atlas.size==(512,256)
    assert (pack/'Final_Citadel_Missed_2x.png').read_bytes()==(art/'Final_Citadel_Missed_2x.png').read_bytes()
    images=[l[5:]for l in text.splitlines()if l.startswith('<img>')];assert reg['atlas_index']==71 and images[71]=='Final_Citadel_Missed_2x.png'
    lines=set(text.splitlines());oldlines=set(old.splitlines());positions={l:i for i,l in enumerate(text.splitlines())}
    defs={l[11:].split(',')[0]:l[11:].split(',')[1:]for l in reg['conditions']};olddefs={l[11:].split(',')[0]:l[11:].split(',')[1:]for l in oldlines if l.startswith('<condition>')}
    assert all(d[0]!='tileNearby'for d in defs.values())
    assert all(l in lines for l in reg['conditions']+reg['backgrounds'])
    for room,mode in [('9CA7','0C'),('9D5B','08'),('9DD3','18')]:
        assert [defs[n]for n in reg['scopes'][room].split('&')]==[['memoryCheckConstant','0072','==',mode],['memoryCheckConstant','0078','==',room[2:]],['memoryCheckConstant','0079','==',room[:2]]]
    count=0;kinds={}
    for e in reg['mappings']:
        assert e['rule']in lines and e['scope']==reg['scopes'][e['room']]
        x,y=e['xy'];cell=np.array(atlas.crop((x,y,x+16,y+16)));t=int(e['tile'],16);kinds[e['kind']]=kinds.get(e['kind'],0)+1
        if e['kind']in ['empty space','distant blue wall']:assert not cell[:,:,3].any()
        else:assert np.array_equal(cell[:,:,3]>0,native_hull(patterns[t]));count+=1
        if t>=0x1900:assert patterns[t]==patterns[t-0x200]
    for e in reg['clones']:
        assert e['source_rule']in oldlines and e['rule']in lines
        a=e['source_rule'].split('<tile>')[1].split(',');b=e['rule'].split('<tile>')[1].split(',')
        assert a[0]==b[0]and a[3:]==b[3:] and patterns[int(a[1],16)]==patterns[int(b[1],16)]
        assert e['rule'].startswith('['+reg['scopes'][e['room']])
        terms=e['rule'].split(']')[0][1:].split('&')[3:]
        assert len(terms)==len(e['source_terms'])
        for new,src in zip(terms,e['source_terms']):
            assert new.startswith('!')==src.startswith('!')
            assert defs[new.lstrip('!')]==olddefs[src.lstrip('!')]
        if e['room']in ['9D5B','9DD3']and e['kind']=='complete earlier room rule':
            # Our first-match overrides precede both inherited and old room rules.
            f=e['rule'].split('<tile>')[1].split(',')
            candidates=[m for m in reg['mappings']if m['room']==e['room']and m['tile']==f[1]and m['palette']==f[2]]
            if candidates:assert all(positions[m['rule']]<positions[e['rule']]for m in candidates)
    for style,_ in reg['styles'].values():
        normal=np.array(Image.open(pack/f'Final_Citadel_{style}.png').convert('RGBA'));flash=np.array(Image.open(pack/f'Final_Citadel_{style}_Flash.png').convert('RGBA'))
        assert normal.shape==(480,512,4)and np.all(normal[:,:,3]==255)
        assert np.array_equal(normal[:,:,:3],flash[:,:,:3])and np.all(flash[:,:,3]==176)
    assert not {'213029','041424','001020'}&set(reg['guard_palettes'])
    standby=json.loads((root/'art/level6_enemy_revision/standby.json').read_text())
    for name,digest in standby['original_files'].items():assert hashlib.sha256((root/name).read_bytes()).hexdigest()==digest
    return dict(prior_assets_exact=len(prior)-2,exact_0301_rules_recovery=True,native_hull_mappings=count,mappings=kinds,clone_rules=len(reg['clones']),background_rules=len(reg['backgrounds']),new_neighbor_probes=0,green_enemy_standby_exact=True,new_files=sorted(NEW))
def legacy_projection(root,pack):
    prior=json.loads((root/'evidence/0.30.1-pack-sha256.json').read_text())
    with tempfile.TemporaryDirectory(prefix='citadel-0301-')as directory:
        target=Path(directory)
        for name,digest in prior.items():
            if name=='hires.txt':(target/name).write_text(strip((pack/name).read_text()))
            elif name=='README.txt':shutil.copyfile(root/'evidence/level6_missed/baseline_README.txt',target/name)
            else:shutil.copyfile(pack/name,target/name)
            assert hashlib.sha256((target/name).read_bytes()).hexdigest()==digest,name
        subprocess.run([sys.executable,str(root/'scripts/validate_pack.py'),str(target)],check=True)
if __name__=='__main__':
    root=Path(__file__).resolve().parents[1];print(json.dumps(verify(root,root/'build/Holy_Diver_(Tr)'),indent=2))
