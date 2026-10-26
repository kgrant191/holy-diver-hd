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

## Stage 2 vertical cave (approved 0.6.1)

Reuse the approved cave panorama as a stationary distant layer while the native gold platforms scroll down the shaft. Clear only the six nonsolid purple wall-pattern identities. Preserve all terrain edges, lava/ice, ghoul poses and shared player/HUD artwork.

The new enemy is a floating eye, with a compact ivory eyeball, teal iris/pupil and short crimson spiked rim. Register the complete body at 32×32 HD across its native four tiles. The 0.6.1 review replaces the fire-like shots with smooth blue teardrops, preserving their measured native bounds (DC: X1–6/Y0–7, DD: X0–6/Y1–7). Original OAM preserves position, trajectory, flips and cadence. Source and prompt: `art/generated/screen2_3_eye_generated.png` and `screen2_3_prompts.json`; the tear source/prompt are `screen2_3_tear_generated.png` and `screen2_3_tear_prompt.json`. Registration: `scripts/build_screen2_3.py`.

## Stage 2 second horizontal cave (0.7.0 candidate)

Reuse the approved cave panorama, gold terrain, brown winged demons and downward arrows, faceless pulsing pink/red rocks, and lava/ice. The complete native pattern bank matches the exterior. New ceiling cells use the accepted gold texture and native lower-edge masks. Clear the nonsolid red/ochre wall motif to expose the cave. Preserve native flips, sprite footprints and terrain boundaries. See `SCREEN2_4.md`; this screen introduces no new painted source.

## Stage 2 crimson cave (0.8.0 candidate)

Keep this room distinctly red: broad carnelian stalactites, coral-lit mineral edges, dark burgundy recesses and distant plum silhouettes. The initial small repeating flowstone registration looked too tight in live play; represent that nonsolid wall layer with the full panorama instead. Keep brighter crimson foreground columns within their native outlines, using broad source facets and side shading for depth. Gold terrain/stairs, bats and eyes/blue tears reuse approved assets. The earlier caves and their backgrounds remain exact. Sources and built-in image-generation prompts are under `art/generated/screen2_5_*`; runtime registration is in `scripts/build_screen2_5.py`.

## Cave visual review (0.8.1 candidate; supersedes the foreground direction above)

The user rejected the rock-textured stairs, repeated red columns and heavy brown ceiling hiding the stronger red backdrop. Use pale-edged cut-stone steps with cool dark faces, retaining native contours. Remove the red columns and ceiling fill; keep gold platforms and only slim dark crimson overhead boundaries. Do not add coral in their place: the selected direction is the open existing panorama. The newly identified handled health jug uses opaque ruby enamel and brass edging/handle so the vessel reads against red scenery. It is separate from the accepted two-tile HP/Magic bottles, which stay exact. Built-in source images and exact prompts are under `art/generated/screen2_5_*`; registrations and user references are under `art/screen2_5_review/`. See `SCREEN2_5_REVIEW.md` for the live-check limits.

## Readable ceiling (0.8.2 candidate; supersedes the roof direction above)

The user accepted the 0.8.1 stairs but found the transparent roof and thin outline insufficient: the player can bump their head, and bats need a visible surface to hang from. Keep the stairs exact and restore the complete foreground ceiling silhouette. Use dense charcoal/plum stone with subdued red reflections and a readable lower edge, separate from the brighter crimson panorama. Preserve gold ground platforms and removal of the rejected red foreground columns. Readability of physical obstacles takes priority over exposing more background. Source and exact built-in image-generation prompt: `art/generated/screen2_5_roof_generated.png` and `screen2_5_roof_prompt.json`; registration: `scripts/build_screen2_5_roof.py`.

## Original brown ceiling (0.8.3; supersedes the charcoal/plum roof)

The user rejected the 0.8.2 treatment: "no lets go back to what we had originally with the brown". Restore the exact original 0.8.0 brown ceiling pixels, native shapes and registrations. Keep the accepted 0.8.1 cut-stone stairs, red background and removed red columns. Reuse the existing atlas sources recorded in `art/screen2_5_roof/previous_geometry.json`; do not generate or recolor a replacement.

## Screen 2-6 and shared artwork (0.9.0 candidate)

Finished art is shared whenever native tile identity and palette match. Keep room overrides before shared fallbacks and retain pose anchors, lava phases and native flip behavior. Different tile slots or palettes need proven registration aliases, not another redraw. Do not make decorative transparency global: a later room may use a different wall composition.

Use the accepted crimson panorama with the restored original brown solid terrain and existing bats. The only new painted subject is the orange/gold bipedal winged dragon: long open snout, small ember-red wings, clawed hands and two walking leg poses. Native artwork faces left; OAM mirrors the full creature right. Share its 18 upper-body cells exactly between poses so the head and torso do not wobble. Fit the whole silhouette inside the measured native tile footprint without clipping. The horizontal shot reuses the approved boss fireball source. Sources, native reference, prompt and registration are under `art/screen2_6/` and `art/generated/screen2_6_*`.

## Level 2 wall boss (approved in 0.10.1)

The boss is a small left-facing demonic skull joined to a much larger violet organ behind it, enclosed by branching coral-pink roots and ivory ridges. Preserve that native asymmetry: the face must not dominate the organ. Its full measured footprint spans two nametables, 192×256 HD pixels. The first narrow source represented only the visible left half and is provenance; use `boss2_wall_full_generated.png` for the full creature. Retain a coherent face/organ connection and fit the roots within the measured tile coverage. Native palette changes control hit phases and disappearance.

Reuse the accepted brown rock texture and crimson panorama. The new room has different native contour cells, so register that same texture inside their shapes. The boss fireballs reuse the first boss's finished source. Breaker is a crimson leather/brass tome with a bright fracture rune, and its announcement uses the existing intermission design. All prompts and image-generation inputs are under `art/generated/boss2_*`; registered assets and native references are under `art/boss2/`.

The 0.10.1 repair retains the same boss through the two darker gold defeat palettes. After disappearance it must stay gone, including the Breaker pickup flash; the earlier black boss silhouette was rejected. Keep the native pale cave flash and timing. This is a mapping/palette repair using existing art.

## Level 3 opening (0.11.0 review candidate)

Use a midnight-blue and muted forest-teal wooded backdrop with distant Gothic ruins. Keep bright brown terrain and branch collision edges readable. Broad trees use vertical warm-brown bark, with the approved branches tied to native positions. The stone shaft reuses approved navy nave masonry and solid columns behind warm brown ledges. New golden ember creatures preserve their compact curled anatomy and shared head between poses; tiny crimson flyers retain their slim body and two native wing positions. Source prompts and registrations are under `art/generated/level3_*` and `art/level3_opening/`. See `LEVEL3_OPENING.md` for native scopes and verification.

## Level 3 review (0.11.1)

The small winged eye is an insect: antennae, tucked legs and rounded veined rose membranes, not bat wings. The spinner is a crimson thorn-ring with three pale curved blades and an open center. First-creature shots use the existing fireball art in their measured half-height footprints. Giant trees use broad continuous knotted oak and subdued moss, shaded within their original outline; avoid tiny repeated vertical strips. See LEVEL3_REVIEW.md.


## Level 3 detail review — 0.11.2

The requested round projectile is native 0694/FF301116 and reuses the exact approved 12×12 fireball inside its 16×16 HD cell. The boot is the magenta collectible (068A–068D/FF301525), with a pale folded cuff and left-pointing toe; do not alter Randy’s worn boots. Branches must be one continuous two-row oak body with a mossy upper edge, never duplicate thin strips with empty centers. Keep their nine original alpha masks exactly; do not extend walkable-looking paint beyond the original contour. Built-in image-generation sources and exact prompts are retained under art/generated/level3_*_generated.png and level3_detail_prompts.json.
