"""Register generated repairs into the approved title and entrance artwork.

Only the prompt footprint and two measured cliff ledges are replaced. Native
rules, sprite art, collision, input handling and the audio patch are untouched.
"""
from pathlib import Path
import io
import json
import zipfile
import xml.etree.ElementTree as ET

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

root = Path(__file__).resolve().parents[1]
art = root / 'art'
pack = root / 'build/Holy_Diver_(Tr)'
seed = root / 'rollback/approved_v14_1'

# Repair the full plaque footprint, including the former narrow patch boundary.
original = Image.open(seed / 'Title_HD.png').convert('RGBA')
clean = Image.open(art / 'generated/title_clean_0_0_2_generated.png').convert('RGBA')
clean = clean.resize(original.size, Image.Resampling.LANCZOS)
mask = Image.new('L', original.size)
ImageDraw.Draw(mask).rounded_rectangle((110, 397, 402, 451), radius=12, fill=255)
mask = mask.filter(ImageFilter.GaussianBlur(3))
# Preserve the existing copyright footer and every pixel outside the repair.
mask_array = np.array(mask)
mask_array[:390] = 0
mask_array[452:] = 0
mask = Image.fromarray(mask_array)
intro = Image.composite(clean, original, mask)

# Register the original approved gold letters only, without their plaque.
letters = original.crop((194, 416, 320, 435))
pixels = np.array(letters)
gold = ((pixels[:, :, 0].astype(float) > pixels[:, :, 2] * 1.35)
        & (pixels[:, :, 0] > 70) & (pixels[:, :, 1] > 48))
pixels[:, :, 3] = gold.astype('uint8') * 255
letters = Image.fromarray(pixels)
ready = intro.copy()
shadow = Image.new('RGBA', letters.size, '#030713')
shadow.putalpha(letters.getchannel('A').filter(ImageFilter.MaxFilter(3)))
ready.alpha_composite(shadow, (194, 417))
ready.alpha_composite(letters, (194, 416))
for name, image in [('Title_Intro_HD.png', intro), ('Title_HD.png', ready)]:
    image.save(art / name)
    image.save(pack / name)

# Full traversals of the user's upper/lower savestates establish the native
# collision spans: X0..64 and X0..80 at Y96 and Y272. A standing sprite can
# overhang the collision edge; its complete OAM footprint is not solid ground.
# Register continuous caps from the left screen edge to those exact boundaries.
source = Image.open(art / 'generated/ledge_extensions_0_0_2_generated.png').convert('RGBA')
source = source.resize((512, 960), Image.Resampling.LANCZOS)
overlay = Image.new('RGBA', (512, 960))
specs = [
    {'name': 'upper', 'source': [84, 192, 190, 244], 'target': [0, 192, 128, 236],
     'native_surface': {'left': 0, 'right_exclusive': 64, 'y': 96}},
    {'name': 'lower', 'source': [116, 544, 210, 596], 'target': [0, 544, 160, 588],
     'native_surface': {'left': 0, 'right_exclusive': 80, 'y': 272}},
]
for spec in specs:
    patch = source.crop(spec['source'])
    rgba = np.array(patch)
    color = rgba[:, :, :3].astype(float)
    warm = ((color[:, :, 0] > color[:, :, 2] * 1.15)
            & (color[:, :, 0] > color[:, :, 1] * 1.08)
            & (color[:, :, 0] > 28))
    alpha = np.zeros(warm.shape, dtype='uint8')
    for y, row in enumerate(warm):
        xs = np.flatnonzero(row)
        if xs.size:
            alpha[y, :xs[-1] + 1] = 255
    rgba[:, :, 3] = alpha
    x0, y0, x1, y1 = spec['target']
    patch = Image.fromarray(rgba).resize((x1-x0, y1-y0), Image.Resampling.LANCZOS)
    rgba = np.array(patch)
    # Keep the ridge continuous through the left edge. Fade only the underside
    # into the existing cliff; fading X would recreate the missing left cap.
    fade_y = np.minimum(1, (patch.height-1-np.arange(patch.height)) / 7)
    rgba[:, :, 3] = np.rint(rgba[:, :, 3] * fade_y[:, None]).astype('uint8')
    overlay.alpha_composite(Image.fromarray(rgba), (x0, y0))
overlay.save(art / 'layers/11_ledge_extensions.png')
scene = Image.open(seed / 'EntranceScene.png').convert('RGBA')
scene.alpha_composite(overlay)
scene.save(art / 'EntranceScene_registered.png')
scene.save(pack / 'EntranceScene.png')

# Keep the editable source aligned with the installed background.
document = ET.Element('image', {'w': '512', 'h': '960', 'name': 'Holy Diver Entrance'})
stack = ET.SubElement(document, 'stack')
with zipfile.ZipFile(art / 'Holy_Diver_Entrance.ora', 'w') as archive:
    def write(name, data):
        info = zipfile.ZipInfo(name, (2026, 10, 22, 0, 0, 0))
        archive.writestr(info, data)
    write('mimetype', b'image/openraster')
    for i, path in enumerate(reversed(sorted((art / 'layers').glob('*.png')))):
        destination = f'data/layer{i}.png'
        write(destination, path.read_bytes())
        ET.SubElement(stack, 'layer', {'name': path.stem, 'src': destination,
                      'opacity': '1.0', 'visibility': 'visible',
                      'composite-op': 'svg:src-over', 'x': '0', 'y': '0'})
    write('stack.xml', ET.tostring(document))
    buffer = io.BytesIO()
    scene.save(buffer, format='PNG')
    write('mergedimage.png', buffer.getvalue())

metadata = {'title_repair_region': [100, 390, 412, 452],
            'ready_prompt': 'original gold letters, no rectangular plaque',
            'title_state_logic': 'unchanged: first Start reveals prompt; second starts play',
            'ledge_registration': specs, 'native_collision_modified': False}
(art / 'title_ledge_registration.json').write_text(json.dumps(metadata, indent=2)+'\n')
print('Registered seamless title states and two full-width collision-aligned ledge caps.')
