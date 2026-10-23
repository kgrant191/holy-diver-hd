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

## Fourth section tree court (approved 0.2.1)

Reuse the approved entrance tree, branches, roots, gold ground and distant ruins. Register these to native tiles so every platform follows the original layout. The left masonry uses a continuous aged-gold facade with complete Gothic arches and dark navy inset stone. Nonsolid decorative tiles are cleared; the shelf remains bound to its native tiles. Preserve the moon’s castle occlusion. The 1-up is an 8×16-native front-facing Randy doll/statue on a small bronze base, with blue and ivory variants. Enemies reuse the approved sharp standing and rolling sprites. See SCREEN1_4.md and SCREEN1_4_REVIEW.md for source provenance.

## First boss and Blizzard chamber (0.3.3 candidate)

The boss preserves the native oversized head, curled ivory horns, teal/green palette, clawed hands and bent legs. Register its head/torso once; vary only the measured lower-body and mouth regions. Maintain the compact airborne/crouched footprint and the native 36-piece bottom-up disappearance. White hit frames and red defeat backdrop pulses follow the actual palette events.

Use brass organ pipes over the approved navy masonry, keeping native pipe lengths, stone collision tiles and gold pendants. The Blizzard chamber has an aged bronze/green bell and a cobalt tome with a cyan frost rune. Reuse the approved Gothic intermission frame for the spell announcement. Source briefs and registration are in `art/generated/boss1_prompts.json`, `art/boss1/` and `scripts/build_boss1.py`.

The 0.3.1 repair keeps the fireball artwork exact and removes the NES scanline sprite limit through Mesen’s pack option. Blizzard’s alternate R/D menu tiles use the same ivory serif font, size and positioning as the other letters. See `BOSS1_REVIEW.md`.

The 0.3.2 ascent backdrop repeats the approved nave panorama vertically to cover both nametables and the viewport. Preserve the original bell and ornaments during the repeating-room scroll. The pre-announcement white/gray steps retain the approved Randy silhouette, with native brightness values 255/173/102. See `BOSS1_TRANSITION.md`.

The standing boot repair changes only pose 0 at local HD coordinates X18–31/Y44–63, preserving the original knee and rear boot. Keep the toe and complete sole inside the native X<32 lower-body footprint; do not extend native geometry or clip a larger generated foot. Both costume patches use their existing boot colors. See `RANDY_FOOT.md`.
