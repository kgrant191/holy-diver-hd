"""v15.1: replace only the missing rear forearm/hand in five shared poses.

The generated arm cutout is composited inside measured native OAM coverage.
All other atlas pixels, hires rules, IPS bytes, timing and game state stay intact.
"""
from pathlib import Path
import json
import numpy as np
from PIL import Image, ImageDraw

root = Path(__file__).resolve().parents[1]
art = root / 'art'
out = root / 'build/Holy_Diver_(Tr)'
meta = json.loads((art / 'arm_repair.json').read_text())
poses = json.loads((art / 'poses.json').read_text())
patch = Image.open(art / 'randy_arm_patch.png').convert('RGBA')
report = {}
for atlas_name, prefix, preview_name in [
    ('Randy_Entrance_2x.png', 'randy_pose_', 'randy_registered_preview.png'),
    ('Randy_Equipped_2x.png', 'randy_equipped_pose_', 'randy_equipped_preview.png'),
]:
    atlas = Image.open(root / 'rollback/approved_v15' / atlas_name).convert('RGBA')
    original = np.array(atlas)
    allowed = np.zeros(original.shape[:2], dtype=bool)
    report[atlas_name] = {}
    for pose_id, (x, y) in meta['pose_positions'].items():
        i = int(pose_id)
        ox, oy = i % 4 * 64, i // 4 * 64
        coverage = Image.new('L', (64, 64))
        draw = ImageDraw.Draw(coverage)
        for tx, ty, _ in poses[i]['tiles']:
            draw.rectangle((tx*2, ty*2, tx*2+15, ty*2+15), fill=255)
        arm = Image.new('RGBA', (64, 64))
        arm.alpha_composite(patch, (x, y))
        mask = np.array(arm.getchannel('A')) > 0
        assert not np.any(mask & (np.array(coverage) == 0)), (atlas_name, i)
        allowed[oy:oy+64, ox:ox+64] |= mask
        atlas.alpha_composite(arm, (ox, oy))
        atlas.crop((ox, oy, ox+64, oy+64)).save(art / f'{prefix}{i:02}.png')
        report[atlas_name][pose_id] = int(mask.sum())
    changed = np.any(np.array(atlas) != original, axis=2)
    assert not np.any(changed & ~allowed)
    atlas.save(out / atlas_name)
    atlas.save(art / atlas_name)
    preview = Image.new('RGB', (768, 660), '#192230')
    draw = ImageDraw.Draw(preview)
    for i in range(10):
        ox, oy = i % 4 * 64, i // 4 * 64
        sprite = atlas.crop((ox, oy, ox+64, oy+64)).resize((192, 192), Image.Resampling.NEAREST)
        preview.paste(sprite, (i % 4 * 192, i // 4 * 220), sprite)
        draw.text((i % 4 * 192 + 4, i // 4 * 220 + 196), f'Pose {i}', fill='white')
    preview.save(art / preview_name)
(art / 'arm_repair_registration.json').write_text(json.dumps(report, indent=2)+'\n')
print('v15.1 arm repair: 5 poses x 2 palettes; all changes within native sprite coverage.')
