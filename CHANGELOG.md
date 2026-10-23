# Changelog

## 0.3.5 — approved 2026-10-23

- Added the large HP and Magic recovery pickups: a ruby-red rounded flask and a cobalt faceted vial with antique brass trim, fitted to the native 8×16 sprite footprint.
- Added 64 shared mappings for sixteen byte-identical copies of each of the four native tiles. Existing small heart/crystal drops, Randy's confirmed leg repair and all previous artwork/mapping priority stay exact.
- Retained native pickup effects, sprite positions, gameplay and audio. Added one atlas for 80 root pack files.
- The user approved the complete first-boss/Blizzard feature and all retained repairs, verified the Actions artifact's 80-file layout with no nested ZIP, and authorized merging PR #4. Actions run 40004314865 passed all 80 expected file hashes before upload.
- Approval bookkeeping updates documentation and only README.txt within the installed pack. All 79 other pack files retain the reviewed hashes; `evidence/0.3.5-reviewed-pack-sha256.json` preserves the original candidate. No release tag or GitHub Release is created.

## 0.3.4 — confirmed leg repair, 2026-10-23

The user confirmed the standing-leg correction ("thats fixed"). Full boss-feature approval followed in 0.3.5.

- Corrected the knee/shin discontinuity introduced by 0.3.3. Register the complete forward standing leg as one piece within its native two-tile footprint in normal/Twin Fire colors and both directions.
- Anchor the idle knee rule to the torso tile directly above it, preserving the same leg at the left-room edge when the distant hand tile leaves the screen. Existing rule priority and every other pose are preserved.
- Added a contour regression check and live comparisons against a clear backdrop, plus paired native memory/audio and unchanged-pose checks. The pack has 79 root files; main remains approved 0.2.1.

## 0.3.3 — rejected review candidate, 2026-10-23

The user rejected this repair because fitting the boot separately broke the knee-to-shin outline. The tests below checked bounds and preservation but missed the visual discontinuity. Superseded by 0.3.4.

- Repaired the cropped toe on Randy’s forward standing boot in normal and Twin Fire colors. The compact complete boot fits entirely within the original two native tiles and mirrors correctly.
- Changed only idle pose 0 below the knee; all crouching, casting, running, airborne, rear-boot and upper-body artwork remains exact. Shared graphics-bank aliases use the same corrected cells, and monochrome idle silhouettes are regenerated consistently.
- Preserved the entire mapping file, existing fireball/backdrop corrections, native gameplay, audio and platform boundaries. The pack still contains 79 root files.
- Main remains approved 0.2.1; the bundle contains all unmerged boss work and review repairs.

## 0.3.2 — superseded review candidate, 2026-10-23

- Extended the Blizzard-room backdrop through the complete native vertical scroll. It repeats the approved masonry exactly, filling the black gaps behind the original bell and ornaments.
- Added the three missing bank-00 fade palettes so Randy retains the approved HD silhouette immediately before the spell announcement, in both directions and after either costume.
- Preserved all prior atlas cells, foreground artwork, native room repeats, white flashes, gameplay and audio. The confirmed fireball repair remains intact.
- Added one backdrop for 79 root pack files. Main remains approved 0.2.1; the bundle includes all unmerged boss work.

## 0.3.1 — superseded review candidate, 2026-10-23

- Fixed the Blizzard pause menu's alternate R and D tile identities with the existing HD font, including both spell selections and pause/resume.
- Enabled Mesen's supported `disableSpriteLimit` HD-pack option. The boss fireball no longer loses alternate halves when boss/player sprites crowd its scanlines. This rendering option applies throughout the loaded pack; native sprites and hit flashes keep their original positions and timing.
- Preserved every existing artwork pixel; only two formerly empty atlas cells gain menu glyphs. Previous mappings and the audio patch stay exact.
- Kept 78 root pack files. Main remains approved 0.2.1; the bundle includes the entire unmerged boss feature plus this repair.

## 0.3.0 — superseded review candidate, 2026-10-23

- Added the first horned boss with standing, stepping, compact jump/crouch and both firing poses, round fireballs, white hit flashes and the native gradual death sequence.
- Added the brass organ hall and Blizzard bell chamber, reusing approved masonry, stone and ornaments at native tile positions.
- Added the Blizzard tome and announcement; retained the native pickup, ascent, flashes and Stage 2 transition. Reused approved Randy/HUD art for identical graphics-bank copies in the announcement and Stage 2 arrival.
- Preserved every earlier PNG/IPS and the complete previous mapping text. Added three runtime PNGs for 78 root pack files.
- Added frame-by-frame controller replays and paired memory/audio verification. Main remains approved 0.2.1 pending review and the agreed manual bundle push.

## 0.2.1 — approved 2026-10-23

- Replaced the sideways miniature Randy pickup with a front-facing figurine on a bronze base in normal and Twin Fire colors.
- Replaced fragmented wall decoration with one continuous Gothic facade: complete arches, joined columns and coherent masonry down to the floor.
- Preserved all native platform pixels, tree/ground art, enemy art, mappings, gameplay and audio. Only two runtime PNGs and README.txt change; the pack still has 75 root files.
- Added bounded pixel checks and repeated the live pickup/descent/edge/transition and earlier-room regressions.
- Approved by the user in chat. Approval bookkeeping changes only README.txt; all 74 runtime files match the reviewed candidate. The artwork was pushed to feature/screen1-4; adoption and Actions artifact verification are tracked in PR #3.

## 0.2.0 — superseded screen 1-4 review candidate, 2026-10-23

- Added the full tree court and descent from the supplied save: Gothic masonry, the approved entrance tree adapted to native repeating tiles, alternating branches, roots and lower ground.
- Added both miniature Randy 1-up palettes; verified collection raises lives from 3 to 4 in normal and Twin Fire modes.
- Reused all six approved purple-ghoul poses, including sharp standing variants, with room-specific mapping conditions.
- Preserved every existing PNG/IPS and all earlier mapping text. Two runtime PNGs bring the pack to 75 root files; hires.txt and README.txt are the only changed existing files.
- Added controller-only pickup, full descent, slow ledge traversal and left-transition replays, plus title/crypt/nave regression checks. Native memory and audio remain unchanged.
- Awaiting user review and local bundle push. Main remains approved 0.1.1; no tag, release or merge.

## 0.1.1 — approved 2026-10-23

- Redrew both standing ghoul poses with crisp pixel clusters and pose-specific mappings. All four rolling frames retain their exact 0.1.0 pixels.
- Added complete crouching spell wind-up/release sprites in both normal and Twin Fire palettes, for both native directions. Shared mappings fix the fallback across matching gameplay identities.
- Used spare cells in the existing atlases, retaining all ten earlier Randy poses. Pack remains 73 root files with no nested archive.
- Added controller-driven live checks and paired gameplay/audio comparisons. Approved by the user in chat for adoption as the main baseline through PR #2.
- Verified the pushed candidate Actions artifact: 73 root files, exact reviewed hashes, no nested ZIP. Approval bookkeeping changes only the pack README; all 72 other pack files remain identical to the reviewed candidate.

## 0.1.0 — superseded review candidate, 2026-10-23

- Added the third chapel section from three supplied savestates: masonry backdrop, emerald/ruby windows, reinforced blocks and gold serpent wall ornament.
- Added all six observed purple-ghoul poses, including its rolling attack; added both small blue flying-skull poses and registered the initial impact flash from approved gold ring artwork.
- Reused approved Randy, weapon, HUD, stone, flying-enemy and expanding defeat artwork. All 69 pre-existing PNG/IPS files remain byte-identical; only hires.txt and the install README change, with two runtime PNGs added.
- Added reproducible paired 720-frame routes for all three states and compact live evidence. Gameplay and audio preservation are checked independently from image review.
- Development artifact only. Awaiting user review; no release tag or GitHub Release.

## 0.0.2 — approved 2026-10-22

- Reconstructed the title-prompt background, removing the former patch seam and rectangular plaque. The original gold PRESS START letters appear after the first Start press.
- Rebuilt the two entrance shelf caps continuously from the left edge to their native fall boundaries: upper HD X0–128 at Y192, lower X0–160 at Y544. Full traversals from the supplied save states replace the earlier, incorrect rightward extensions.
- Actions artifacts now contain the installable pack files directly; one extraction exposes hires.txt instead of another ZIP.
- Preserved all sprite atlases, tile rules, collision, input timing and audio patch bytes.

## 0.0.1 — 2026-10-22

- Initial repository development version, based on approved historical v15.1 artwork.
- Added agent guidance, project status, art/testing documentation, repeatable build validation and GitHub Actions.
- All 70 runtime pack files match v15.1 exactly. Pack README.txt identifies development version 0.0.1 and the source repository.
- Adopted semantic versioning for ongoing development; reserve 1.0.0 for the completed, tested game pack.

## Historical builds

The labels below predate semantic versioning and identify retained artwork and test evidence.

## v15.1 — approved 2026-10-22

- Completed the rear forearm and clenched fist in five Randy poses in both normal and Twin Fire atlases.
- Preserved other atlas pixels, tile mappings, title behavior and audio patch.
- Verified both directions, standing/airborne casts, screen-2 combat and death in Mesen.

## v15

- Matching compact/expanded gold defeat effects for enemies and Randy.
- Navy/gold stage and lives cards using native game values.
- Approved HD health/magic glyphs restored after death.

## v14.1

- Collected Start/pause-menu item uses the approved bracelet artwork.

## v14

- Red winged-skull drop corrected to a gold/ruby bracelet.
- Shared Randy defeat fallback mappings added.

## v13

- Screen-2 crypt environment and observed entities/pickups.
- Measured Randy/HUD/weapon mappings shared across matching native room identities.

## v12 and earlier entrance work

- Clean splash; first Start reveals PRESS START; second Start starts play.
- Entrance environment, Randy poses, normal/Twin Fire weapons and upward attack.
- Approved entrance audio priority/thunder-mask IPS.
