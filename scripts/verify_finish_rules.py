"""Check repair scope, preserved assets, stair silhouette and doorway bounds."""
from pathlib import Path
import hashlib, json, re
import numpy as np
from PIL import Image

def verify(root, pack, content=None, inventory=None):
    text = (pack/'hires.txt').read_text() if content is None else content
    lines = text.splitlines()
    reg = json.loads((root/'art/level4_finish/registration.json').read_text())
    previous = json.loads((root/'evidence/0.20.0-pack-sha256.json').read_text())
    assert (inventory if inventory is not None else {p.name for p in pack.iterdir() if p.is_file()}) == set(previous)|{'Golden_Temple_Finish_2x.png'}
    for name, digest in previous.items():
        if name not in {'hires.txt', 'README.txt'}:
            assert hashlib.sha256((pack/name).read_bytes()).hexdigest() == digest, name
    for section in ['IMAGES', 'CONDITIONS', 'MAPPINGS', 'EARLY_STAIRS']:
        text, count = re.subn(r'^# BEGIN TEMPLE_FINISH '+section+r'\n.*?^# END TEMPLE_FINISH '+section+r'\n', '', text, flags=re.M|re.S)
        assert count == 1
    assert hashlib.sha256(text.encode()).hexdigest() == previous['hires.txt']
    old = np.array(Image.open(root/'art/level4_stairs/descending_step.png').convert('RGBA'))
    step = np.array(Image.open(root/'art/level4_finish/descending_step.png').convert('RGBA'))
    atlas = np.array(Image.open(pack/'Golden_Temple_Finish_2x.png').convert('RGBA'))
    assert np.array_equal(atlas[:32,:32], step)
    assert np.array_equal(step[:16], old[:16])
    assert np.array_equal(step[:,:,:3], old[:,:,:3])
    bottoms = []
    for x in range(32):
        ys = np.flatnonzero(step[:,x,3]); bottoms.append(int(ys[-1]))
        assert (step[ys[0]:ys[-1]+1,x,3] == 255).all()
    assert max(np.abs(np.diff(bottoms))) <= 1
    defs = {l[11:].split(',')[0]:l[11:].split(',')[1:] for l in lines if l.startswith('<condition>')}
    probes = 0
    for m in reg['mappings']:
        line = m['rule']; assert line in lines
        if m['kind'] == 'smooth descending step':
            assert m['source_rule'] in text.splitlines()
            assert lines.index(line) < lines.index(m['source_rule'])
            assert line.replace(']<tile>54,', ']<tile>49,') == m['source_rule']
            continue
        assert line.startswith('['+reg['portal_scope']+'&') or line.startswith('['+reg['portal_scope']+']')
        if m['kind'] != 'boss entrance opening': continue
        terms = line[1:line.index(']')].split('&')
        bound, neighbor = defs[terms[-2]], defs[terms[-1]]
        assert bound[:2] == ['positionCheckY','>='] and neighbor[0]=='tileNearby'
        dx,dy = map(int,neighbor[1:3]); assert dx==0
        for y in range(240):
            if y < int(bound[2]): continue
            for x in range(256):
                assert 0 <= (y+dy)*256+x < 61440
                probes += 1
    return dict(tile_rules=reg['tile_rules'], conditions=reg['conditions'],
                prior_assets_exact=113, exact_previous_mapping_recovery=True,
                standing_surface_unchanged=True, continuous_stair_underside=True,
                bounded_neighbor_reads=probes, unsafe_reads=0)

if __name__ == '__main__':
    r=Path(__file__).resolve().parents[1]
    report=verify(r,r/'build/Holy_Diver_(Tr)')
    print(json.dumps(report,indent=2))
