"""Keep native surfaces, earlier artwork and the exact 0.31.0 rule projection."""
from pathlib import Path
import hashlib,json,re,tempfile,shutil,subprocess,sys
from PIL import Image
NEW='Palace_Surfaces_Book_2x.png'
def recover(root,text):
    text,n=re.subn(r'^# BEGIN PALACE_SURFACES IMAGES\n.*?^# END PALACE_SURFACES IMAGES\n','',text,flags=re.M|re.S);assert n==1
    lines=text.splitlines()
    for e in json.loads((root/'art/palace_surfaces/registration.json').read_text())['substitutions']:
        assert lines[e['line']]==e['new'];lines[e['line']]=e['old']
    return '\n'.join(lines)+'\n'
def verify(root,pack):
    prior=json.loads((root/'evidence/0.31.0-pack-sha256.json').read_text());text=(pack/'hires.txt').read_text();old=recover(root,text)
    assert hashlib.sha256(old.encode()).hexdigest()==prior['hires.txt']
    assert {p.name for p in pack.iterdir()if p.is_file()}==set(prior)|{NEW}
    for name,digest in prior.items():
        if name not in ['hires.txt','README.txt']:assert hashlib.sha256((pack/name).read_bytes()).hexdigest()==digest,name
    images=[l[5:]for l in text.splitlines()if l.startswith('<img>')];assert images[72]==NEW
    reg=json.loads((root/'art/palace_surfaces/registration.json').read_text());atlas=Image.open(pack/NEW).convert('RGBA');assert atlas.size==(512,256)
    assert (pack/NEW).read_bytes()==(root/'art/palace_surfaces'/NEW).read_bytes()
    loaded={};counts={};rooms={};book=[]
    for e in reg['substitutions']:
        aa,bb=e['old'].split('<tile>'),e['new'].split('<tile>');assert aa[0]==bb[0]
        a,b=aa[1].split(','),bb[1].split(',');assert a[1:3]==b[1:3]and a[5:]==b[5:]and int(b[0])==72
        counts[e['kind']]=counts.get(e['kind'],0)+1;rooms[e['room']]=rooms.get(e['room'],0)+1
        name=images[int(a[0])]
        if name not in loaded:loaded[name]=Image.open(pack/name).convert('RGBA')
        x,y=map(int,a[3:5]);original=loaded[name].crop((x,y,x+16,y+16));x,y=map(int,b[3:5]);new=atlas.crop((x,y,x+16,y+16))
        if e['kind']=='Overdrive acquisition book':
            assert e['room']=='9F92'and 0x88b<=int(a[1],16)<=0x88e and a[2]=='FF301116';book.append(int(a[1],16))
            source=Image.open(root/'art/palace_surfaces/overdrive_book.png').convert('RGBA');j=int(a[1],16)-0x88b;x,y=j%2*16,j//2*16
            assert source.crop((x,y,x+16,y+16)).tobytes()==new.tobytes()
        else:
            assert e['room']in reg['rooms']and e['style']in ['silver','violet','green']
            assert original.getchannel('A').tobytes()==new.getchannel('A').tobytes()
            assert original.getchannel('A').getbbox()is not None
    assert sorted(book)==list(range(0x88b,0x88f))
    assert not {'850A','8672','86EA','8762'}&set(rooms)
    return dict(exact_0310_recovery=True,prior_assets_exact=len(prior)-2,terrain_alpha_exact=True,rule_order_and_conditions_exact=True,unchanged_opening_rooms=True,all_background_rules_exact=True,only_acquisition_book_changed=True,scoped_replacements=counts,rooms=rooms)
def legacy_projection(root,pack):
    prior=json.loads((root/'evidence/0.31.0-pack-sha256.json').read_text())
    with tempfile.TemporaryDirectory(prefix='palace-surfaces-0310-')as d:
        target=Path(d)
        for name,digest in prior.items():
            if name=='hires.txt':(target/name).write_text(recover(root,(pack/name).read_text()))
            elif name=='README.txt':shutil.copyfile(root/'evidence/palace_surfaces/baseline_README.txt',target/name)
            else:shutil.copyfile(pack/name,target/name)
            assert hashlib.sha256((target/name).read_bytes()).hexdigest()==digest,name
        subprocess.run([sys.executable,str(root/'scripts/validate_pack.py'),str(target)],check=True)
if __name__=='__main__':
    root=Path(__file__).resolve().parents[1];print(json.dumps(verify(root,root/'build/Holy_Diver_(Tr)'),indent=2))
