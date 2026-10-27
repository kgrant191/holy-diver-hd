"""Check native aliases, whole-band registration and every reachable probe."""
from pathlib import Path
import json
import numpy as np
from PIL import Image

def verify(root):
    pack = root / 'build/Holy_Diver_(Tr)'
    lines = (pack / 'hires.txt').read_text().splitlines()
    defs = {l[11:].split(',')[0]: l[11:].split(',')[1:] for l in lines if l.startswith('<condition>')}
    reg = json.loads((root / 'art/level4_finale/registration.json').read_text())
    patterns = json.loads((root / 'art/level4_finale/native_patterns.json').read_text())
    aliases = json.loads((root / 'art/level4_finale/native_aliases.json').read_text())
    for source, targets in aliases.items():
        for target in targets:
            assert patterns[source] == patterns[target], (source, target)
    for t in range(256):
        assert patterns[f'{0xb00+t:04X}'] == patterns[f'{0xd00+t:04X}']
    for t in range(0x75):
        assert patterns[f'{0xa00+t:04X}'] == patterns[f'{0xe00+t:04X}']

    # Normalize identities to offsets: identical ordered address calculations
    # need only one exhaustive grid, independently of the tile being matched.
    chains = set()
    for m in reg['mappings'] + reg['clones']:
        line = m['rule']
        if not line.startswith('['):
            continue
        chain = []
        for term in line[1:line.index(']')].split('&'):
            d = defs[term.lstrip('!')]
            if d[0] in ['positionCheckX', 'positionCheckY', 'tileNearby']:
                chain.append((term.startswith('!'), *d[:3]))
        if any(c[1] == 'tileNearby' for c in chain):
            chains.add(tuple(chain))
    y, x = np.indices((240, 256)); reads = blocked = 0
    for chain in chains:
        live = np.ones((240, 256), bool)
        for neg, kind, p, q in chain:
            if kind == 'tileNearby':
                dx, dy = int(p), int(q)
                safe = (x+dx >= 0) & (x+dx < 256) & (y+dy >= 0) & (y+dy < 240)
                assert np.all(safe[live]), (chain, dx, dy)
                reads += int(live.sum())
            else:
                values = x if kind == 'positionCheckX' else y
                v = int(q)
                ok = {'>=': values >= v, '<': values < v, '==': values == v}[p]
                if neg:
                    ok = ~ok
                blocked += int((live & ~ok).sum()); live &= ok
    assert chains and reads

    layouts = json.loads((root / 'art/level4_finale/boss_band_layouts.json').read_text())[:8]
    boss_views = [d for name, d in defs.items() if name.startswith('finaleBossView_')]
    edge_keys = {key for layout in layouts for key, x, y in layout['layout'] if x == 0}
    assert len(boss_views) == len(edge_keys)*5*2
    for kind, x, y, key, pal in boss_views:
        assert kind == 'tileAtPosition' and x == '96' and int(y) in [32, 96, 128, 160, 224]
        assert key in edge_keys and key != '0F00' and pal in ['0F071727', '0F001030']
    atlas = Image.open(pack / 'Golden_Temple_Finale_2x.png').convert('RGBA')
    assert len(reg['boss_pose_rules']) == 8*2*28
    for phase in range(8):
        native = {(x, y): key for key, x, y in layouts[phase]['layout']}
        assert len(native) == 28
        for pal in ['0F071727', '0F001030']:
            assembled = Image.new('RGBA', (112, 64))
            entries = [m for m in reg['boss_pose_rules'] if m['phase'] == phase and m['palette'] == pal]
            assert len(entries) == 28
            for m in entries:
                x, y = m['x'], m['y']
                assert m['tile'] == native[x, y]
                assert m['signature'] == [[key, xx-x, yy-y] for key, xx, yy in layouts[phase]['layout'] if (xx, yy) != (x, y)]
                f = m['rule'].split('<tile>')[1].split(','); ax, ay = map(int, f[3:5])
                assembled.paste(atlas.crop((ax, ay, ax+16, ay+16)), (x*16, y*16))
            source = Image.open(root / f'art/level4_finale/tower_band_{phase}_{pal}.png').convert('RGBA')
            assert assembled.tobytes() == source.tobytes(), (phase, pal)
    return dict(native_aliases_exact=True, whole_registered_bands=16,
                ordered_probe_geometries=len(chains), coordinate_cases=len(chains)*61440,
                safe_reads=reads, blocked_branches=blocked, unsafe_reads=0)

if __name__ == '__main__':
    root = Path(__file__).resolve().parents[1]
    report = verify(root)
    out = root / 'evidence/level4_finale/neighbor_rules.json'
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps(report, indent=2))
