"""Bound the 0.2.1 art revision to the wall and two pickup palettes."""
from pathlib import Path
import argparse
import hashlib
import json
import zipfile
import numpy as np
from PIL import Image

p=argparse.ArgumentParser()
p.add_argument('--before-pack',required=True,help='Extracted 0.2.0 candidate')
p.add_argument('--out',required=True)
a=p.parse_args()
root=Path(__file__).resolve().parents[1]
before=Path(a.before_pack)
after=root/'build/Holy_Diver_(Tr)'
hashes=lambda d:{f.name:hashlib.sha256(f.read_bytes()).hexdigest() for f in d.iterdir() if f.is_file()}
old,new=hashes(before),hashes(after)
assert old==json.loads((root/'evidence/0.2.0-pack-sha256.json').read_text())
assert old.keys()==new.keys() and len(new)==75
changed=sorted(k for k in old if old[k]!=new[k])
assert changed==['README.txt','Tree_Court_Background.png','Tree_Court_Tiles_2x.png']
old_bg=np.array(Image.open(before/'Tree_Court_Background.png').convert('RGBA'))
new_bg=np.array(Image.open(after/'Tree_Court_Background.png').convert('RGBA'))
assert np.array_equal(old_bg[:,224:],new_bg[:,224:])
assert np.array_equal(old_bg[896:],new_bg[896:])
old_atlas=np.array(Image.open(before/'Tree_Court_Tiles_2x.png').convert('RGBA'))
new_atlas=np.array(Image.open(after/'Tree_Court_Tiles_2x.png').convert('RGBA'))
allowed=np.zeros(old_atlas.shape[:2],dtype=bool)
wall_kinds={'wall infill','column','column repeat','weathered brick','arch cap','arch leg','wall edge','cornice'}
cells=json.loads((root/'art/screen1_4/registration.json').read_text())['mappings']
cleared=figurines=0
for cell in cells:
    x,y=cell['atlas'];kind=cell['kind']
    if kind in wall_kinds:
        allowed[y:y+16,x:x+16]=True
        assert not new_atlas[y:y+16,x:x+16,3].any()
        cleared+=1
    elif kind=='1-up front-facing figurine':
        allowed[y:y+16,x:x+16]=True
        assert new_atlas[y:y+16,x:x+16,3].any()
        figurines+=1
assert figurines==4
assert np.array_equal(old_atlas[~allowed],new_atlas[~allowed])
assert all(np.array_equal(old_atlas[y:y+16,x:x+16],new_atlas[y:y+16,x:x+16])
           for c in cells if c['kind']=='platform cap' for x,y in [c['atlas']])
archive=root/f'build/Holy_Diver_HD_v{(root/"VERSION").read_text().strip()}.zip'
with zipfile.ZipFile(archive) as z:
    names=z.namelist()
    assert len(names)==75 and set(names)==set(new)
    assert all('/' not in n and not n.lower().endswith('.zip') for n in names)
    assert all(hashlib.sha256(z.read(n)).hexdigest()==new[n] for n in names)
report=dict(changed_files=changed,unchanged_files=72,root_files=75,nested_zip=False,
            archive_sha256=hashlib.sha256(archive.read_bytes()).hexdigest(),
            wall_bounds_hd=[0,0,224,896],unchanged_background_outside_wall=True,
            cleared_wall_cells=cleared,figurine_cells=figurines,
            unchanged_other_atlas_pixels=True,unchanged_platform_caps=True,
            unchanged_rules=True,unchanged_ips=True)
out=Path(a.out);out.parent.mkdir(parents=True,exist_ok=True)
out.write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
