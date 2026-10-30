"""Check the four requested repairs and exact recoverability of 0.30.0."""
from pathlib import Path
import hashlib,json,re,tempfile,shutil,subprocess,sys
import numpy as np
from PIL import Image
from scipy.ndimage import label

NEW='Final_Citadel_Finale_Repair_2x.png'
def strip(text):
    for part in ['IMAGES','CONDITIONS','MAPPINGS']:
        text,n=re.subn(r'^# BEGIN LEVEL6_FINALE_REPAIR '+part+r'\n.*?^# END LEVEL6_FINALE_REPAIR '+part+r'\n','',text,flags=re.M|re.S);assert n==1
    return text.replace('# LEVEL6_FINALE_REPAIR SUPERSEDED ','')

def verify(root,pack):
    prior=json.loads((root/'evidence/0.30.0-pack-sha256.json').read_text());text=(pack/'hires.txt').read_text();baseline=strip(text)
    assert hashlib.sha256(baseline.encode()).hexdigest()==prior['hires.txt']
    old_face=json.loads((root/'art/level6_enemy_revision/registration.json').read_text())
    expected={e['rule']for e in old_face['mappings']if e['kind']=='wall face color'}
    marked={l.removeprefix('# LEVEL6_FINALE_REPAIR SUPERSEDED ')for l in text.splitlines()if l.startswith('# LEVEL6_FINALE_REPAIR SUPERSEDED ')}
    assert marked==expected and len(marked)==171
    assert {p.name for p in pack.iterdir()if p.is_file()}==set(prior)|{NEW}
    for name,digest in prior.items():
        if name not in ['hires.txt','README.txt']:assert hashlib.sha256((pack/name).read_bytes()).hexdigest()==digest,name
    art=root/'art/level6_finale_repair';reg=json.loads((art/'registration.json').read_text());atlas=Image.open(pack/NEW).convert('RGBA')
    assert (pack/NEW).read_bytes()==(art/NEW).read_bytes();assert reg['atlas_index']==70 and atlas.size==(1024,512)
    images=[l[5:]for l in text.splitlines()if l.startswith('<img>')];assert images[70]==NEW
    defs={l[11:].split(',')[0]:l[11:].split(',')[1:]for l in reg['conditions']};positions={l:i for i,l in enumerate(text.splitlines())};kinds={}
    for p in reg['probes']:
        dx,dy=p['dx'],p['dy'];expected=[['positionCheckX','>=',str(max(0,-dx))],['positionCheckX','<',str(min(256,256-dx))],['positionCheckY','>=',str(max(0,-dy))],['positionCheckY','<',str(min(240,240-dy))],['tileNearby',str(dx),str(dy),p['tile'],'0F162638','Y']]
        assert [defs[t]for t in p['terms']]==expected
    for e in reg['mappings']:
        assert e['rule']in positions and int(e['tile'],16)>=0x1a00
        for p in reg['probes']:
            if p['terms'][-1]in e['scope'].split('&'):assert '&'.join(p['terms'])in e['scope']
        kinds[e['kind']]=kinds.get(e['kind'],0)+1
    assert kinds['blue mucus blob']==8 and kinds['boss entrance']==72
    assert set(kinds)=={'clean wall face','blue mucus blob','boss entrance','entrance activation','connected ending dragon','ending transparent text'}
    face=Image.open(art/'wall_face.png').convert('RGBA')
    for y,row in enumerate(reg['face_layout']):
        for x,t in enumerate(row):
            source=face.crop((x*16,y*16,x*16+16,y*16+16)).tobytes()
            assert any(atlas.crop((*e['xy'],e['xy'][0]+16,e['xy'][1]+16)).tobytes()==source for e in reg['mappings']if int(e['tile'],16)==t and e['kind']=='clean wall face')
    shared={}
    for i,layout in enumerate(reg['ending_layouts']):
        im=Image.open(art/f'ending_dragon{i}.png').convert('RGBA');mask=np.zeros((im.height,im.width),bool)
        for t,x,y in layout:
            mask[y*2:y*2+16,x*2:x*2+16]=True;cell=im.crop((x*2,y*2,x*2+16,y*2+16)).tobytes()
            if t in shared:assert shared[t]==cell
            shared[t]=cell
            e=next(e for e in reg['mappings']if e['tile']==f'{0x1e00+t:04X}'and e['palette']=='FF190927')
            xx,yy=e['xy'];assert atlas.crop((xx,yy,xx+16,yy+16)).tobytes()==cell
        a=np.array(im)[:,:,3]>0;assert not(a&~mask).any();_,n=label(a,np.ones((3,3)));assert n==1
    assert not any(e['palette']in ['FF0F0F07','FF0F0F0F']for e in reg['mappings']if e['kind']=='connected ending dragon')
    for line in reg['font_sources']:
        f=line[6:].split(',');source=Image.open(pack/images[int(f[0])]).convert('RGBA');x,y=int(f[3]),int(f[4]);before=np.array(source.crop((x,y,x+16,y+16)))
        e=next(e for e in reg['mappings']if e['tile']==f[1]and e['palette']==f[2]and e['kind']=='ending transparent text');x,y=e['xy'];after=np.array(atlas.crop((x,y,x+16,y+16)))
        black=(before[:,:,:3]==0).all(2);assert np.array_equal(before[:,:,:3],after[:,:,:3]);assert np.array_equal(before[~black],after[~black]);assert not after[black,3].any()
    standby=json.loads((root/'art/level6_enemy_revision/standby.json').read_text())
    for path,digest in standby['original_files'].items():assert hashlib.sha256((root/path).read_bytes()).hexdigest()==digest
    return dict(prior_assets_exact=len(prior)-2,exact_0300_rules_recovery=True,mappings=kinds,bounded_probes=len(reg['probes']),connected_dragon_poses=2,shared_tail_exact=True,ending_glyph_colors_exact=True,green_orb_standby_exact=True)

def legacy_projection(root,pack):
    prior=json.loads((root/'evidence/0.30.0-pack-sha256.json').read_text())
    with tempfile.TemporaryDirectory(prefix='citadel-0300-')as directory:
        target=Path(directory)
        for name,digest in prior.items():
            if name=='hires.txt':(target/name).write_text(strip((pack/name).read_text()))
            elif name=='README.txt':(target/name).write_bytes((root/'evidence/level6_finale_repair/baseline_README.txt').read_bytes())
            else:shutil.copyfile(pack/name,target/name)
            assert hashlib.sha256((target/name).read_bytes()).hexdigest()==digest,name
        subprocess.run([sys.executable,str(root/'scripts/validate_pack.py'),str(target)],check=True)

if __name__=='__main__':
    root=Path(__file__).resolve().parents[1];print(json.dumps(verify(root,root/'build/Holy_Diver_(Tr)'),indent=2))
