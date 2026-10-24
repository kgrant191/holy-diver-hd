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

## First boss and Blizzard chamber (approved 0.3.5)

The boss preserves the native oversized head, curled ivory horns, teal/green palette, clawed hands and bent legs. Register its head/torso once; vary only the measured lower-body and mouth regions. Maintain the compact airborne/crouched footprint and the native 36-piece bottom-up disappearance. White hit frames and red defeat backdrop pulses follow the actual palette events.

Use brass organ pipes over the approved navy masonry, keeping native pipe lengths, stone collision tiles and gold pendants. The Blizzard chamber has an aged bronze/green bell and a cobalt tome with a cyan frost rune. Reuse the approved Gothic intermission frame for the spell announcement. Source briefs and registration are in `art/generated/boss1_prompts.json`, `art/boss1/` and `scripts/build_boss1.py`.

The 0.3.1 repair keeps the fireball artwork exact and removes the NES scanline sprite limit through Mesen’s pack option. Blizzard’s alternate R/D menu tiles use the same ivory serif font, size and positioning as the other letters. See `BOSS1_REVIEW.md`.

The 0.3.2 ascent backdrop repeats the approved nave panorama vertically to cover both nametables and the viewport. Preserve the original bell and ornaments during the repeating-room scroll. The pre-announcement white/gray steps retain the approved Randy silhouette, with native brightness values 255/173/102. See `BOSS1_TRANSITION.md`.

The standing leg correction changes only pose 0 at local HD coordinates X16–31/Y32–63. Register thigh, knee, shin and boot together; the isolated 0.3.3 boot fit visibly broke the knee join. Keep the continuous leg and complete toe inside the native X<32 footprint. Preserve the rear boot, upper body, all other poses and each costume's existing colors. Judge the joint in live captures against a clear backdrop in both directions, including where the knee and shin span separate native tiles. See `RANDY_LEG.md`.

Large recovery pickups use a rounded ruby-red HP flask and faceted cobalt/cyan Magic vial with restrained antique brass collars/bases. Keep the complete bottles in the native two-tile 16×32 HD canvas, including its eight transparent top rows. The small heart and crystal retain their existing artwork. Shared matching CHR copies reuse the same flask art. See `RECOVERY_ITEMS.md`.

## Stage 2 exterior (approved 0.4.1)

Use deep plum/navy skies, firelit burgundy clouds, distant scorched forests and Gothic ruins. The gold native platforms keep their exact tile-defined edges; lava is red-orange molten rock and Blizzard ice is cobalt/cyan with a level frost crust. Distinguish breakable blocks with an antique-gold frame and cracked center. The exit cliff reuses approved gold-rock texture and native silhouette masks; its doorway stays dark.

The reviewed direction (0.4.1) replaces the initial hooded skull with a brown winged demon: two recognizable chestnut/ochre bat wings, pale demonic face, tucked legs and curled tail. Native unflipped sprites travel LEFT; hardware mirroring travels right. Hold and drop a slender downward arrow with gold fletching and an ivory arrowhead. Keep the body stable across the native wingbeat identities.

The red enemy is FACELESS: pale pink stone scaffold with rounded crimson lobes pulsing through its cracks, in three native poses. No eyes, mouth, skull or facial ridges. The supplied original-game close-up is the anatomy reference. The cave opening must stay dark as soon as any of it enters the viewport; neighbor probes must not wrap across the left screen edge.

## Stage 2 cave (approved 0.5.1)

Reuse approved gold platforms, purple ghouls, lava/ice, pickups, player and HUD. Distinguish artwork reuse from native identity registration: the cave's ghoul graphics move six slots earlier in its CHR bank, and pose-anchor conditions must move with them. Keep the repaired sharp standing heads ahead of broad rolling rules.

The entirely underground backdrop uses indigo/plum depth and faint lava glow. The user requested removal of the reddish hanging layer in the 0.5.1 review: clear those decorative identities to expose the existing cave panorama. Keep the gold ceiling and platforms. Hot vertical falls use sixteen downward translation phases with continuous tile joins; the native ice palette selects the unchanged static frozen tiles. Preserve approved pool artwork. The earlier generated red-rock source remains provenance, not a build input.

The original narrow pale/teal ceiling enemy becomes a folded-wing Gothic bat and the same creature with wings open. Keep its central lower body within the native two-cell bottom row, and both wing tips in the upper four-cell rows. Use actual playback to inspect the wing/body joins, fireball timing and silhouettes. Sources/prompts are under `art/generated/screen2_2_*`; native reference and registration are under `art/screen2_2/`.

## Stage 2 vertical cave (0.6.1 review candidate)

Reuse the approved cave panorama as a stationary distant layer while the native gold platforms scroll down the shaft. Clear only the six nonsolid purple wall-pattern identities. Preserve all terrain edges, lava/ice, ghoul poses and shared player/HUD artwork.

The new enemy is a floating eye, with a compact ivory eyeball, teal iris/pupil and short crimson spiked rim. Register the complete body at 32×32 HD across its native four tiles. The 0.6.1 review replaces the fire-like shots with smooth blue teardrops, preserving their measured native bounds (DC: X1–6/Y0–7, DD: X0–6/Y1–7). Original OAM preserves position, trajectory, flips and cadence. Source and prompt: `art/generated/screen2_3_eye_generated.png` and `screen2_3_prompts.json`; the tear source/prompt are `screen2_3_tear_generated.png` and `screen2_3_tear_prompt.json`. Registration: `scripts/build_screen2_3.py`.
