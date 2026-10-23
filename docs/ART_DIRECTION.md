# Art direction

Preserve the approved dark Gothic style: deep navy scenery, warm gold/fire lighting, textured stone and restrained highlights. The approved PNGs are the visual reference.

Randy has long dark hair, white/ivory normal costume, blue Twin Fire costume, dark wrist guards/pants and brown boots. Keep face, proportions and lower-body poses coherent. Rear forearms and hands must remain readable rather than ending at the cape.

Pack scale is 2: each native 8x8 tile maps to 16x16. Usual Randy pose cells are 64x64; the upward pose is 32x80 per palette. Native OAM coverage and per-sprite mirroring determine usable footprints. Check joins in both directions in live Mesen.

Use retained generated images as references for raster edits. Keep prompts/metadata and register art into measured layouts. Preserve approved poses outside the requested change.

The bracelet is a gold band with a ruby detail; drop and pause-menu artwork must match. Defeat effects use the approved two gold/ivory phases at native positions and cadence.

Acceptance screenshots/video must come from actual emulator playback. Label enlargements and distinguish concept art from runtime evidence.

## Third chapel section (approved in 0.1.1)

Use a solid navy masonry nave wall so the native emerald/ruby windows read as inset glass. Preserve the native top/side edges of reinforced blocks and existing stone tiles. The large gold serpent pendant is background decoration in the recorded states; do not assign it collision or enemy behavior. Purple ghouls retain the native crouched proportions and compact rolling footprint. Native unflipped ghoul and blue-skull graphics face left; hardware mirroring controls direction. The blue flying skull keeps its pale/cyan face, cobalt shadow and red fin/wing.

New source art and generation briefs are in art/generated/screen1_3_*.png and docs/SCREEN1_3.md. Registration is deterministic in scripts/build_screen1_3.py. The standing ghoul refinements and missing crouch attacks are documented in docs/REVIEW_FIXES.md. Other earlier approved poses remain unchanged.

## Fourth section tree court (0.2.1 candidate)

Reuse the approved entrance tree, branches, roots, gold ground and distant ruins. Register these to native tiles so every platform follows the original layout. The left masonry uses a continuous aged-gold facade with complete Gothic arches and dark navy inset stone. Nonsolid decorative tiles are cleared; the shelf remains bound to its native tiles. Preserve the moon’s castle occlusion. The 1-up is an 8×16-native front-facing Randy doll/statue on a small bronze base, with blue and ivory variants. Enemies reuse the approved sharp standing and rolling sprites. See SCREEN1_4.md and SCREEN1_4_REVIEW.md for source provenance.
