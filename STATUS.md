# Current status

Updated: 2026-10-22 (America/New_York).

## Current review candidate

0.0.2 on branch `fix/title-screen-1-1`, awaiting user review. It repairs the title prompt background in both Start states and extends the two entrance rock ledges to cover the measured grounded range. main remains at approved 0.0.1 until the PR is accepted. No GitHub Release is being published.

Candidate verification: 6,440 frames per build and 1,610 paired RAM/PPU/OAM samples match 0.0.1 exactly. APU writes and common captured PCM also match. Live captures cover fresh/reset title states and stable upper/lower shelf positions facing both directions. Only three background PNGs and the pack README change; 67 package files remain byte-identical. See evidence/title_screen_1_1/verification.json, package_changes.json and comparison.png.

## Approved baseline

Development version **0.0.1**, using the approved historical v15.1 artwork, accepted after the Randy arm repair (the user said "much better"). Initial GitHub import preserves all 70 runtime pack files exactly; README.txt only updates the development version and source location. Version 1.0.0 is reserved for the completed, tested game pack.

Completed: entrance/title sequence, entrance environment, known shared Randy poses and normal/Twin Fire palettes, screen-2 crypt environment/enemies, bracelet drop and matching pause icon, shared defeat-effect phases, stage/lives cards, post-death HUD, and rear forearm/hand repair.

## Latest verification

- Both Randy costumes, left/right, standing and airborne idle/horizontal casts. Sampled run/upward frames unchanged.
- Screen-2 combat and Randy death retain RAM/PPU/OAM, APU writes and recorded audio. Frozen death pose includes the repaired arm.
- 2,040 emulated frames and 1,558 paired state captures: evidence/arm_repair/verification.json and TEST_RESULTS.md.
- Earlier v15 tests covered fresh start/reset, normal/Twin Fire death, enemy combat and collected-bracelet pause/resume. Historical results remain in evidence/v15/.

## Next work

Move to the next screen when its savestate or route is available. Inspect native tiles, palettes, entities and geometry first. Apply shared player/weapon/effect art where identities match, then build newly observed environment/enemies.

## Known limits

- This is a partial HD overhaul, not a finished all-stage pack.
- All six stage names and life counts 0–9 are mapped; live card coverage is Stage 1 and counts 3/2.
- Native player tiles $33, $34, $35 and $3C were previously observed as unmapped leg fragments. Investigate if a live route uses them; do not guess from tile numbers.
- The earlier report of Randy fully reverting to original art during death was not independently reproduced. Shared defeat fallbacks exist, and current recorded death poses remain HD.
- Old scripts remain for provenance. build.py is the supported build entry point.
- Full historical capture runs/videos and original savestates remain in the prior source/handoff archives. The repository keeps compact evidence and exact rollback inputs.
