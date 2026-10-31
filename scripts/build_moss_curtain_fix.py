"""Finish missing native scenery identities in the recorded moss lava curtain."""
from pathlib import Path
import hashlib,json,re
import numpy as np
from PIL import Image

ROOT=Path(__file__).resolve().parents[1]
PACK=ROOT/'build/Holy_Diver_(Tr)'
ART=ROOT/'art/moss_curtain_fix'
SCOPE='l3c9DEEMode&l3c9DEELo&l3c9DEEHi'
NEW='Moss_Curtain_Fix_2x.png'

def build(pack=PACK):
    prior=json.loads((ROOT/'evidence/1.0.0-pack-sha256.json').read_text())
    text=(pack/'hires.txt').read_text()
    assert hashlib.sha256(text.encode()).hexdigest()==prior['hires.txt']
    lines=text.splitlines();images=[l[5:]for l in lines if l.startswith('<img>')]
    index=len(images);assert index==73
    records=[];rules=[]
    def add(source,t,pal,phase='',kind=''):
        f=source.split('<tile>')[1].split(',');old=f.copy();f[1]=f'{t:04X}';f[2]=pal
        rule='['+SCOPE+('&'+phase if phase else '')+']<tile>'+','.join(f)
        rules.append(rule);records.append(dict(kind=kind,source_rule=source,rule=rule,identity=f[1],palette=pal,phase=phase))
    # Exact CHR identities, rearranged in the Level 3 bank. Copy every existing
    # descending phase condition and both native hot colors, plus the ice form.
    aliases={0x74f:0x38e,0x750:0x38d,0x751:0x38c,0x771:0x38b,0x772:0x38a,0x773:0x389}
    for t,old in aliases.items():
        for line in lines:
            m=re.fullmatch(r'\[(s25Room&s25DataLo&s25DataHi(?:&s22FallPhase\d+)?)\]<tile>(.*)',line)
            if not m:continue
            f=m[2].split(',')
            if int(f[1],16)!=old or f[2]not in ['0F161606','0F060616','0F122131']:continue
            phase=m[1].split('&')[3:]
            add(line,t,f[2],'&'.join(phase),'approved animated lava/ice curtain')
    assert len(rules)==198
    floor_aliases={0x73e:0x345,0x73f:0x344,0x740:0x343,0x741:0x342,0x742:0x341,0x743:0x334}
    for t,old in floor_aliases.items():
        source=next(l for l in lines if l.startswith('[s21Room&s21DataLo&s21DataHi]<tile>')and l.split('<tile>')[1].split(',')[1:3]==[f'{old:04X}','0F122131'])
        add(source,t,'0F122131',kind='approved frozen lava pool')
    for t in [0x74b,0x74c,0x74d,0x74e]:
        source=next(l for l in lines if l.startswith('[l3c9B96Mode&l3c9B96Lo&l3c9B96Hi]<tile>45,')and l.split('<tile>')[1].split(',')[1:3]==[f'{t:04X}','0F0A1A29'])
        add(source,t,'0F091929',kind='approved moss ceiling detail')
    for t in [0x78f,0x790,0x791]:
        source=next(l for l in lines if l.startswith('[l3_forestRoom&l3_forestLo&l3_forestHi]<tile>45,')and l.split('<tile>')[1].split(',')[1]==f'{t:04X}')
        add(source,t,'0F0A1A29',kind='approved moss native contour')
    # Complete the missing upper-left cell with the same native hull algorithm
    # and whole moss unit used by its three previously finished neighbors.
    pattern=bytes.fromhex(json.loads((ART/'native_patterns.json').read_text())['078E'])
    mask=np.array([[bool((pattern[y]|pattern[y+8])&(1<<(7-x)))for x in range(8)]for y in range(8)])
    for y in range(8):
        xs=np.flatnonzero(mask[y])
        if len(xs):mask[y,xs[0]:xs[-1]+1]=True
    for x in range(8):
        ys=np.flatnonzero(mask[:,x])
        if len(ys):mask[ys[0]:ys[-1]+1,x]=True
    cell=Image.open(ROOT/'art/poison_moss/brick.png').convert('RGBA').crop((0,16,16,32))
    cell.putalpha(Image.fromarray((mask*255).astype('uint8')).resize((16,16),Image.Resampling.NEAREST))
    cell.save(pack/NEW)
    rule=f'[{SCOPE}]<tile>{index},078E,0F0A1A29,0,0,1,N'
    rules.append(rule);records.append(dict(kind='missing moss native contour',identity='078E',palette='0F0A1A29',rule=rule,pattern_sha256=hashlib.sha256(pattern).hexdigest()))
    assert len(rules)==212
    declaration='# BEGIN MOSS_CURTAIN_FIX IMAGES\n<img>'+NEW+'\n# END MOSS_CURTAIN_FIX IMAGES\n'
    at=text.index('\n',text.rfind('<img>'))+1;text=text[:at]+declaration+text[at:]
    block='# BEGIN MOSS_CURTAIN_FIX MAPPINGS\n'+'\n'.join(rules)+'\n# END MOSS_CURTAIN_FIX MAPPINGS\n'
    marker='# BEGIN SCREEN2_SHARED\n';assert text.count(marker)==1
    text=text.replace(marker,block+marker)
    (pack/'hires.txt').write_text(text)
    ART.mkdir(exist_ok=True)
    (ART/'registration.json').write_text(json.dumps(dict(room='9DEE',mode='14',atlas_index=index,new_image=NEW,tile_rules=212,prior_hires_sha256=prior['hires.txt'],native_aliases={f'{t:04X}':f'{o:04X}'for t,o in (aliases|floor_aliases).items()},mappings=records),indent=2)+'\n')
    print('Moss curtain repair: 212 room-scoped rules; existing animation and moss sources.')

if __name__=='__main__':build()
