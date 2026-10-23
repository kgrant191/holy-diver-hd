# Changelog

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
