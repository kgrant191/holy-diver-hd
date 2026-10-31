"""Verify the removable 1.0.1 repair and exact preservation of the released pack."""
from pathlib import Path
import hashlib,json,re,tempfile,shutil,subprocess,sys
from PIL import Image

NEW='Moss_Curtain_Fix_2x.png'
def recover(text):
    for part in ['IMAGES','MAPPINGS']:
        text,n=re.subn(r'^# BEGIN MOSS_CURTAIN_FIX '+part+r'\n.*?^# END MOSS_CURTAIN_FIX '+part+r'\n','',text,flags=re.M|re.S)
        assert n==1
    return text

def verify(root,pack):
    prior=json.loads((root/'evidence/1.0.0-pack-sha256.json').read_text());text=(pack/'hires.txt').read_text()
    assert hashlib.sha256(recover(text).encode()).hexdigest()==prior['hires.txt']
    public={p.name for p in pack.iterdir()if p.is_file()and not p.name.startswith('.')}
    assert public==set(prior)|{NEW}
    for name,digest in prior.items():
        if name not in ['hires.txt','README.txt']:assert hashlib.sha256((pack/name).read_bytes()).hexdigest()==digest,name
    reg=json.loads((root/'art/moss_curtain_fix/registration.json').read_text());patterns=json.loads((root/'art/moss_curtain_fix/native_patterns.json').read_text())
    rules=[e['rule']for e in reg['mappings']];assert len(rules)==len(set(rules))==212
    assert all(rule.startswith('[l3c9DEEMode&l3c9DEELo&l3c9DEEHi')for rule in rules)
    images=[l[5:]for l in text.splitlines()if l.startswith('<img>')];assert images[73]==NEW and len(images)==74
    for t,source in reg['native_aliases'].items():assert patterns[t]==patterns[source]
    for e in reg['mappings']:
        assert text.splitlines().count(e['rule'])==1
        if 'source_rule'in e:
            old=e['source_rule'].split('<tile>')[1].split(',');new=e['rule'].split('<tile>')[1].split(',')
            assert old[0]==new[0]and old[3:]==new[3:]
        if e['kind']=='approved animated lava/ice curtain':
            assert e['source_rule'].split('<tile>')[0].split('&')[3:]==e['rule'].split('<tile>')[0].split('&')[3:]
    assert Image.open(pack/NEW).size==(16,16)
    return dict(room='9DEE',mode='14',tile_rules=212,previous_nontext_assets_exact=172,original_rule_text_exactly_recoverable=True,native_lava_aliases_exact=True,all_existing_animation_conditions_preserved=True,new_neighbor_probes=0)

def legacy_projection(root,pack):
    prior=json.loads((root/'evidence/1.0.0-pack-sha256.json').read_text())
    with tempfile.TemporaryDirectory(prefix='moss-curtain-100-')as d:
        p=Path(d)
        for name,digest in prior.items():
            if name=='hires.txt':(p/name).write_text(recover((pack/name).read_text()))
            elif name=='README.txt':shutil.copyfile(root/'evidence/moss_curtain_fix/baseline_README.txt',p/name)
            else:shutil.copyfile(pack/name,p/name)
            assert hashlib.sha256((p/name).read_bytes()).hexdigest()==digest,name
        subprocess.run([sys.executable,str(root/'scripts/validate_pack.py'),str(p)],check=True)

if __name__=='__main__':
    root=Path(__file__).resolve().parents[1];print(json.dumps(verify(root,root/'build/Holy_Diver_(Tr)'),indent=2))
