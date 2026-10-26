# Build and live testing

## Build (no ROM required)

Use Python 3.12 and requirements.txt. Run `python build.py`, then `python scripts/verify_release.py`. The latter compares every built file against evidence/approved-pack-sha256.json. The original evidence/v15.1-pack-sha256.json remains as the historical import reference: version 0.0.1 changes only README.txt, and all 70 runtime files match exactly. The DejaVu font/license are bundled in art/fonts/.

CI runs these commands and uploads the extracted pack files as a downloadable artifact. Older builders remain for provenance; build.py is the current entry point.

## Live inputs and setup

Use local MesenCE 2.2.1 and the supported translated ROM (SHA-1 fe2fcd0ad334d792db16535d09f3ab9fb2bea3ac). Restore savestates using test_states/README.md. All these inputs are excluded from Git.

Linux replay helpers require a C++ compiler for record_audio.cpp; video export requires ffmpeg. The runners preload /usr/lib/x86_64-linux-gnu/libstdc++.so.6 when starting Mesen. Adapt that runtime path for another host if needed.

Mesen settings: NES HD packs enabled; Port1 Type NesController; AutoConfigureInput false; Lua AllowIoOsAccess true; ScriptTimeout 10. Install the pack in the ROM-matching HdPacks directory before playback.

```sh
python scripts/run_arm_qa.py --mesen /path/to/Mesen --rom '/path/to/Holy_Diver_(Tr).nes' --out work/arms
python scripts/run_v15_qa.py --mesen /path/to/Mesen --rom '/path/to/Holy_Diver_(Tr).nes' --out work/v15
```

run_v15_qa.py accepts --case title|normal|twin|enemy|menu and --capture-every-frame.

Run sequentially; never reinstall the pack during playback. The first loaded-state screenshot can be empty. endFrame OAM may describe the next pose, so evaluate joins from captured images.

Paired tests use identical states, controller routes, emulator settings and capture intervals. Compare RAM/PPU/OAM and sound events for behavior preservation; inspect images/video for visual quality. Do not modify RAM to stage pickups/death.

## Recorded coverage

- Fresh start/reset and native two-press title sequence.
- Screen-2 combat and both death phases; normal/Twin Fire death; collected bracelet pause/resume.
- Repaired rear arm in both directions/palettes, ground and airborne; unchanged run/upward samples.
- Stage 1 card and life counts 3/2. Other card mappings are implemented but not all live-tested.

Detailed results are in TEST_RESULTS.md and evidence/. Full raw runs/videos remain in prior handoff archives. A clone builds immediately; live testing needs separately supplied emulator, ROM and states.

## Title and entrance repair replay (0.0.2)

Build the baseline 0.0.1 revision in a separate checkout and retain its extracted pack. Then build the candidate. The runner installs the supplied pack before replay and requires exclusive use of Mesen. It uses fresh boot and controller input; no savestate or RAM edits are required.

Use an isolated portable emulator folder outside automatically synchronized directories. The runner records installed file hashes for every case and checks them again after playback. This prevents a background sync process from silently replacing a baseline with a newer candidate.

```sh
python scripts/run_title_ledge_qa.py --mesen /path/to/Mesen --rom '/path/to/Holy_Diver_(Tr).nes' --pack /path/to/0.0.1-pack --out work/title_screen_1_1/before
python scripts/run_title_ledge_qa.py --mesen /path/to/Mesen --rom '/path/to/Holy_Diver_(Tr).nes' --pack 'build/Holy_Diver_(Tr)' --out work/title_screen_1_1/after
python scripts/verify_title_ledge_qa.py --before work/title_screen_1_1/before --after work/title_screen_1_1/after --out evidence/title_screen_1_1/verification.json
python scripts/export_title_ledge_preview.py --before work/title_screen_1_1/before --after work/title_screen_1_1/after --out evidence/title_screen_1_1/comparison.png
```

Inspect title captures 0240/0420 and reset captures 1140/1320. The stationary ledge tests above are historical behavior checks only: a grounded sprite can overhang the collision boundary. They did not establish the correct visible platform span and must not replace the full traversal below.

## Full ledge boundary replay (revised 0.0.2)

The user supplied Holy_Diver_HD_1(2).mss (upper) and Holy_Diver_HD_2(1).mss (lower); hashes are in test_states/README.md. Retain the previous candidate's pack and run each version sequentially in the isolated emulator folder:

```sh
python scripts/run_ledge_boundary_qa.py --mesen /path/to/Mesen --rom '/path/to/Holy_Diver_(Tr).nes' --pack /path/to/previous-pack --upper-state '/path/to/Holy_Diver_HD_1(2).mss' --lower-state '/path/to/Holy_Diver_HD_2(1).mss' --out work/ledge_boundaries/before
python scripts/run_ledge_boundary_qa.py --mesen /path/to/Mesen --rom '/path/to/Holy_Diver_(Tr).nes' --pack 'build/Holy_Diver_(Tr)' --upper-state '/path/to/Holy_Diver_HD_1(2).mss' --lower-state '/path/to/Holy_Diver_HD_2(1).mss' --out work/ledge_boundaries/after
python scripts/verify_ledge_boundary_qa.py --before work/ledge_boundaries/before --after work/ledge_boundaries/after --out evidence/ledge_boundaries/verification.json
python scripts/export_ledge_boundary_preview.py --before work/ledge_boundaries/before --after work/ledge_boundaries/after --out evidence/ledge_boundaries
```

Each case runs 460 frames: left 10–129, neutral through 159, then right two frames per eight through 439. Verify the settled left stop at 132–159 and the full slow traverse. Upper first fall: frame 353; lower: 417. Inspect both sides of those transitions, not just the stationary pose. Artwork spans HD X0–128/Y192 and X0–160/Y544; do not add 32 pixels for the full boot/OAM width.

Artifact check: download the current Actions artifact and inspect its ZIP directory. hires.txt must be at the archive root, all files listed in the current expected manifest must be present, and no .zip entry may exist. One extraction into the ROM-matching pack folder must be sufficient.

## Third chapel section (0.1.0 candidate)

Retain an extracted 0.0.2 pack, then build the candidate. Pass all three user states from test_states/README.md. Each run records installed hashes, 720 frames per state, RAM/PPU/OAM every two frames, APU writes and Mesen PCM. Only controller input drives the game.

```sh
python scripts/run_screen1_3_qa.py --mesen /path/to/Mesen --rom '/path/to/Holy_Diver_(Tr).nes' --pack /path/to/0.0.2-pack --state1 '/path/to/Holy_Diver_HD_1(3).mss' --state2 '/path/to/Holy_Diver_HD_2(2).mss' --state3 '/path/to/Holy_Diver_HD_3(1).mss' --out work/screen1_3/before
python scripts/run_screen1_3_qa.py --mesen /path/to/Mesen --rom '/path/to/Holy_Diver_(Tr).nes' --pack 'build/Holy_Diver_(Tr)' --state1 '/path/to/Holy_Diver_HD_1(3).mss' --state2 '/path/to/Holy_Diver_HD_2(2).mss' --state3 '/path/to/Holy_Diver_HD_3(1).mss' --out work/screen1_3/after
python scripts/verify_screen1_3_qa.py --before work/screen1_3/before --after work/screen1_3/after --out evidence/screen1_3/verification.json
python scripts/export_screen1_3_preview.py --before work/screen1_3/before --after work/screen1_3/after --out evidence/screen1_3
```

Inspect the window/body repeats during scrolling, native block edges, the gold ornament's transparent surroundings, both palettes/directions of Randy, all six ghoul poses in both directions, both blue skull poses, initial impact, shared expanding rings and lives transition. See docs/SCREEN1_3.md for identities and source-art briefs.

Run the existing fresh/reset title and earlier crypt combat routes against each pack. The earlier crypt test requires the retained room2/Holy_Diver_HD_1(1).mss input.

```sh
python scripts/run_screen1_3_regression.py --mesen /path/to/Mesen --rom '/path/to/Holy_Diver_(Tr).nes' --pack /path/to/0.0.2-pack --out work/screen1_3/regression-before
python scripts/run_screen1_3_regression.py --mesen /path/to/Mesen --rom '/path/to/Holy_Diver_(Tr).nes' --pack 'build/Holy_Diver_(Tr)' --out work/screen1_3/regression-after
python scripts/verify_screen1_3_regression.py --before work/screen1_3/regression-before --after work/screen1_3/regression-after --out evidence/screen1_3/regression.json
```

The regression verifier requires identical screenshots as well as memory/audio. The final Actions artifact must contain exactly the 73 expected pack files at its root and no nested ZIP. `approved-pack-sha256.json` retains its historical name; it now describes approved 0.1.1. The reviewed pre-approval pack is retained as `0.1.1-reviewed-pack-sha256.json`; only its README changes during approval bookkeeping. User approval is recorded in STATUS.md.

## 0.1.1 review fixes

See `docs/REVIEW_FIXES.md` for the crouch-attack replay and comparison commands. `run_crouch_qa.py` uses controller input only and captures every frame in both normal/Twin Fire modes. `verify_review_fixes.py` requires both attack phases and both directions, paired native memory/audio equality, and unchanged rolling screenshots. `run_screen1_3_qa.py --case state3` supports a targeted replay when capture output needs repeating.

## Screen 1-4 tree court (0.2.0 candidate)

See [SCREEN1_4.md](SCREEN1_4.md) for the supplied-state routes, actual pickup/edge results, native memory/audio comparisons, background coverage and regression commands. The candidate has 75 root pack files. `0.1.1-pack-sha256.json` preserves approved main; `approved-pack-sha256.json` describes the tested candidate on this review branch and is not an approval record.

## Screen 1-4 wall/figurine revision (approved 0.2.1)

See [SCREEN1_4_REVIEW.md](SCREEN1_4_REVIEW.md). Pair the same five routes against 0.2.0 and pass `--baseline 0.2.0` to the verifier; the original default retains the initial screen-addition checks. Run `verify_screen1_4_review_assets.py` for the strict pixel/file change boundary. The current candidate has 75 root files and three changed files relative to 0.2.0. Earlier reports and manifests remain historical evidence.

0.2.1 was approved in chat on 2026-10-23. Its original live runs are pinned to `0.2.1-reviewed-pack-sha256.json`. Approval changes only README.txt; all 74 runtime hashes remain identical. No additional emulator run is needed for that text-only change. Rebuild and verify the approved manifest and archive, then check the actual Actions artifact from PR #3.

## First boss and Blizzard transition (0.3.0 candidate)

See [BOSS1.md](BOSS1.md) and `scripts/boss1_routes.json`. Eight controller-only routes cover 7,670 frames per build at one-frame capture intervals. They cover every boss pose in both directions, both hit palettes, all 36 disappearance counts, both reward-platform edges, floor boundaries, pickup/ascent/announcement and Stage 2 arrival. The approved Stage 2 card remains exact. `verify_boss1_qa.py` requires identical native RAM/PPU/OAM and APU events, with byte-identical common PCM and at most one shutdown buffer of audio-tail difference.

`boss1_regression_routes.json` adds nave/tree-court replays to the existing title/crypt checks. `verify_boss1_regression.py` requires identical screenshots and native memory/audio across all four earlier cases. The candidate's expected manifest contains 78 root pack files. Main remains approved 0.2.1; the actual Actions artifact must be checked after the user pushes the bundle and the review PR is opened.

## Boss fireball and Blizzard menu review repair (0.3.1 candidate)

See [BOSS1_REVIEW.md](BOSS1_REVIEW.md). `boss1_review_routes.json` adds the post-pickup pause menu, both spell selections and resume to three combat routes. `verify_boss1_review.py` checks all native memory/audio, limits combat differences to native sprite rectangles, limits menu differences to the two letter cells, and confirms the prior mapping text and artwork are preserved.

The supported sprite-limit option affects rendering throughout the pack. Repeat the title/crypt/nave/tree routes and use `verify_boss1_review_regression.py`; only nave sprite pixels on overflowing scanlines may differ. Earlier exact-image verification scripts remain for the original feature's historical evidence. Current repair coverage totals 7,460 frames per build. The 78-file Actions artifact still requires verification after the user's push.

## Blizzard ascent/fade repair (0.3.2 candidate)

See [BOSS1_TRANSITION.md](BOSS1_TRANSITION.md). `boss1_transition_routes.json` covers normal/left-facing and Twin Fire/right-facing pickups through Stage 2, menu selections and resume, plus the corrected fireball regression. `verify_boss1_transition.py` requires 5,500 identical paired samples per RAM/PPU/OAM type, identical APU/common PCM, exact prior artwork/mappings outside the specified additions, unchanged foreground, and the same HD silhouette through all three final fade steps. The pack contains 79 root files. The actual Actions artifact remains pending the user’s push and review PR.

## Standing boot repair (rejected 0.3.3 candidate)

See [RANDY_FOOT.md](RANDY_FOOT.md). `randy_foot_routes.json` tests normal/Twin Fire standing in both directions, crouching and crouched casts, running, jumps and casts, then replays both Blizzard transitions and the corrected fireball. The historical verifier passed its pixel bounds and native memory/audio checks but missed the broken knee/shin outline. The user rejected the result.

## Connected standing leg (0.3.4 candidate)

See [RANDY_LEG.md](RANDY_LEG.md). `randy_leg_routes.json` adds two clear-background routes to the preceding five cases, totaling 6,940 frames per build. `verify_randy_leg.py` detects the rejected knee contour, requires a connected and gradual replacement outline, checks the complete leg in both directions/costumes, and verifies the idle knee mapping when the outer hand is offscreen. All image changes must stay inside the idle forward leg; every other pose and all native memory/APU/common PCM must remain exact. Inspect the unretouched live close-ups; numerical checks do not replace visual review. The 79-file artifact still requires actual Actions verification after the user's push.

## HP and Magic recovery flasks (approved 0.3.5)

See [RECOVERY_ITEMS.md](RECOVERY_ITEMS.md). Six controller-only routes cover both supplied pickups, collection in normal/Twin Fire costumes, and neutral drop/expiry behavior. `verify_recovery_items.py` requires exact paired native memory/APU/common PCM, changes confined to the four native item tiles, and exact images after collection or expiry. HP collection raises 5→6; Magic raises 10→50, in both costumes. All existing art and mapping text stay exact. Base-bank items are live-tested; identical later-bank copies are mapped without claiming live coverage. Actions run 40004314865 verified all 80 expected hashes and uploaded 80 files. The user downloaded artifact 12523247888 and confirmed its flat 80-file layout, hires.txt at the root and no nested ZIP before authorizing PR #4's merge. Independent assistant extraction was unavailable because the local execution environment failed; record the user's archive-layout check separately from CI's pre-upload hash verification.

Approval changes only the installed README.txt. All 79 other pack hashes remain identical to `evidence/0.3.5-reviewed-pack-sha256.json`; `evidence/approved-pack-sha256.json` records the new README hash. Rebuild and verify that manifest in Actions. The existing live evidence remains valid for the unchanged runtime art and mappings.

## Stage 2 screen 1 (0.4.0 candidate)

See [SCREEN2_1.md](SCREEN2_1.md) for the four supplied states, six controller routes, frame-by-frame preservation checks, native Blizzard blackouts, complete outdoor traversal and earlier-boss regression. The candidate has 82 root pack files and preserves all 78 existing runtime asset files exactly. `0.3.5-pack-sha256.json` pins approved main; the current manifest describes the review candidate. Actions artifact verification follows the user's push and review.

## Stage 2 cave and enemy repairs (approved 0.4.1)

See [SCREEN2_1_REVIEW.md](SCREEN2_1_REVIEW.md). Pair the six existing Stage 2 routes with 0.4.0, then add the 420-frame cave approach from `Holy_Diver_HD_1(7).mss`. The verifier bounds changes to the two enemies and doorway, checks all animation/arrow identities, derives facing from native sprite-X deltas while the camera is stationary, preserves exact blackouts/native state/audio, and checks the next room unchanged. The cave's displayed camera trails the endFrame RAM sample by two frames; use the aligned scroll for exact interior-pixel assertions. Inspect both flyer directions and all three red poses in actual Mesen captures.

0.4.1 was approved by the user on 2026-10-23. The reviewed replay manifest is retained as `0.4.1-reviewed-pack-sha256.json`; the installed approval README is the only changed pack file. All 81 runtime files stay exact, so no additional emulator replay is required for approval bookkeeping. PR #5 and its merge into main passed Actions (runs 40018693181 and 40019141872). Both actual downloaded archives independently passed all 82 approved hashes, ZIP CRC checks, root-layout and no-nested-ZIP checks. See `evidence/screen2_1_review/pr_artifact.json` and `main_artifact.json`. Merge/adoption records change no installed pack files.

## Stage 2 screen 2 cave (0.5.0 candidate)

See [SCREEN2_2.md](SCREEN2_2.md). `screen2_2_routes.json` supplies four controller-only cases, plus the separate previous-room approach route. Capture every second frame, retaining every native APU write and continuous PCM. The verifier requires paired RAM/PPU/OAM and APU equality, identical common PCM, exact native blackouts, unchanged menus/outside-room captures, observed hot/ice palettes, every new bat/shot identity and complete registered sprite matches in actual screenshots. It also verifies the 24 shared ghoul native patterns. Full cave traversal is not claimed.

The 84-file candidate archive must pass CRC, root layout, no-nested-ZIP and every expected SHA-256. `0.4.1-pack-sha256.json` retains approved main; the current expected manifest describes the review branch. Actual Actions artifact checks follow the user's push and PR.

## Cave decoration and falling-lava review (0.5.1 candidate)

See [SCREEN2_2_REVIEW.md](SCREEN2_2_REVIEW.md). Repeat the five cave/approach routes against 0.5.1. Compare with the retained 0.5.0 replays using `verify_screen2_2_review.py`; additionally use `verify_screen2_2_qa.py` with approved 0.4.1 to retain the original full native/pose coverage. The review verifier limits image changes to red decoration/hot-fall source colors and the measured partial-alpha HUD edges that blend over them. It requires every unaffected cave tile variant and 81 other pack files to stay exact. It verifies actual downward pixel translation and stationary Blizzard ice from an unobstructed fall segment with a stationary camera. Inspect the actual motion video as well as numerical checks. No RAM edits are used.

0.5.1 visuals were approved on 2026-10-24. The reviewed manifest remains pinned in `0.5.1-reviewed-pack-sha256.json`; approval changes only installed README. All 83 runtime hashes remain exact, so the live evidence still applies. PR #6 and main Actions builds and their actual 84-file artifacts were subsequently verified; the work is included in approved main 0.6.1.

## Stage 2 vertical cave (0.6.0 candidate)

Use the unchanged `Holy_Diver_HD_1(9).mss` with `scripts/screen2_3_routes.json` and the existing `run_screen2_2_qa.py` runner. Exact commands and scope are in `docs/SCREEN2_3.md`; verifier and preview exporter are `verify_screen2_3_qa.py` and `export_screen2_3_preview.py`.

Four paired routes pass 5,560 frames/build and 2,780 exact samples per native-memory type, preserving APU/common PCM, 106 native black frames, 270 completed next-room captures and the pause menu. All 1,957 actual full-color wall samples reveal the stationary approved panorama. The full vertical scroll reaches 512, crosses frozen lava and exits into the next room. Eye body, both shot shapes/flips and all six ghoul poses/both directions have exact complete-sprite matches in actual captures. Native death grayscale/emphasis and subsequent scenery disable are inspected separately from source-RGB matching; unchanged palette RAM does not imply full-color rendering. All 82 previous non-mapping/non-readme files remain hash-identical.

## Blue-tear repair (approved 0.6.1)

Replay `screen2_3_review_routes.json` with the same cave runner and user state. Compare against the retained 0.6.0 combat/respawn capture using `verify_screen2_3_review.py`; commands and limits are in `docs/SCREEN2_3_REVIEW.md`. The 2,400-frame paired run preserves 1,200 native samples/type and equal full PCM/APU. Differences in 637 captures are confined to the eye shots; 563 captures remain identical. Source-atlas checks constrain changes to exactly two cells; 83 other installed files are hash-identical. Both tear shapes and mirrors are verified from actual sprite pixels.

Approval bookkeeping for 0.6.1 changes only installed README.txt. All 84 runtime files retain the reviewed hashes, so no additional emulator run is required for the documentation-only approval update. The reviewed manifest is retained separately; the build/expected-hash check verifies the approved installation.

PRs #6/#7 were merged after the user explicitly authorized them. The final 0.6.1 PR run 40053346170 and main run 40053648543 passed. Both actual downloaded artifacts contain 85 root files, with every approved hash matching, valid ZIP CRCs and no nested ZIP. Adoption documentation changes no runtime files. See `evidence/screen2_3_review/{pr_artifact,main_artifact,approval}.json`.

## Stage 2 second horizontal cave (0.7.0 candidate)

Use MesenCE 2.2.1, `screen2_4_routes.json` and the existing cave runner with the user's unchanged `Holy_Diver_HD_1(10).mss`. Run the separate approach route from the preceding screen 3 state. `verify_screen2_4_qa.py` compares approved 0.6.1 and candidate captures for native RAM/PPU/OAM, APU/common PCM, blackouts, menu/outside-room preservation, complete sprites and source panorama pixels. `verify_screen2_4_motion.py` measures actual two-HD-pixel downward fall translation and stationary Blizzard ice from consecutive captures with a stationary camera. Commands, exact input hashes, results and coverage limits are in [SCREEN2_4.md](SCREEN2_4.md).

The whole native pattern bank matches the approved exterior. Static validation removes the SCREEN2_4 blocks to recover the exact 0.6.1 mapping, and checks all 83 prior runtime file hashes. The initial live preview exposed two unmapped wall-tip identities beneath platforms; the final build clears 036E/036F with the surrounding nonsolid wall. Final candidate replays are repeated after that mapping correction. Build/CRC/hash checks require 86 root files and no nested ZIP. Actions remains pending the user's source-bundle push.

## Screen 2-4 stairs (0.7.1 candidate)

The supplied end state exercises all twelve stair identities and the upper exit. `screen2_4_stairs_routes.json` and `verify_screen2_4_stairs.py` verify 1,800 paired frames/build, 900 exact native samples/type, equal full PCM/APU, changes confined to stair cells and 332 unchanged next-room pictures. See [SCREEN2_4_STAIRS.md](SCREEN2_4_STAIRS.md).

## Screen 2-5 crimson cave (0.8.0 candidate)

Use the same end state with `run_screen2_5_qa.py`, `screen2_5_routes.json` and `verify_screen2_5_qa.py`. Five routes pass 6,200 paired frames/build and 3,100 exact RAM/PPU/OAM/PPU-view samples per type, identical APU and full PCM, 76 exact black captures, 848 outside-room captures and 56 menu captures. All 300 final stair-walk pictures match 0.7.1. The panorama matches its source pixels in 211 sampled pictures; complete reused sprite matches cover the folded bat, eye and tear-DC. Other registered forms remain byte-preserved, without claiming fresh complete-sprite coverage.

The runner adds actual PPU page/fine-scroll metadata at every capture: logical camera RAM remains stale at the room entrance and resets early during return. Source comparisons use the integer PPU positions traversed between adjacent two-frame samples. The live route reaches camera scroll 281 and the first bat/eye platforms, with both player directions, combat casts, Blizzard flashes, pause, death and return. It does not reach the far exit or establish a new lava freeze test. See [SCREEN2_5.md](SCREEN2_5.md) for exact commands and coverage. The install ZIP passes CRC/root-layout and all 88 expected SHA-256 checks; Actions awaits the user's source-bundle push.

## Cave visual review (0.8.1 candidate)

Run `screen2_5_review_routes.json` through `run_screen2_5_qa.py`, then `verify_screen2_5_review.py`. Five paired routes pass 6,800 frames/build and 3,400 exact RAM/PPU/OAM/PPU-view samples/type, identical full PCM/APU, 80 black captures, 259 outside-room pictures, 56 menu pictures, 25,569 gold floor-body cell checks and 352 complete stair-source matches. The stair alpha contours equal 0.8.0; 2-4 changes are confined to those cells. The extended route reaches camera scroll 482 and the hot lava fall before death/return. The far exit remains unverified.

The handled health jug is not reached. `health_jug_static.json` records native CHR identity, geometry and binary-alpha/opaque-body checks, without claiming a live pickup or collection. A save at that jug is needed to close the live coverage gap. Exact commands, sources, scope and remaining limits are in [SCREEN2_5_REVIEW.md](SCREEN2_5_REVIEW.md). The ZIP passes all 89 expected hashes, CRC and root-layout checks.

## Readable cave ceiling (0.8.2 candidate)

Use `screen2_5_roof_routes.json` with `run_screen2_5_qa.py`, comparing the final 0.8.1 and 0.8.2 packs through `verify_screen2_5_roof.py`. The 6,800 paired frames/build preserve 3,400 RAM/PPU/OAM/PPU-view samples per type, every APU write and all full PCM bytes (zero shutdown-tail difference). All 300 stair captures remain exact. The verifier restricts image changes to the 46 roof identities, preserving gold floor cells through their cap-above conditions; it handles partial left-edge tiles and measured PPU scroll phases. Runtime matches cover 12 roof identities and 143 complete folded bats against ceiling geometry. Static validation preserves all 46 old alpha contours and every one of the 87 prior runtime assets.

Inspect the actual bat attachment and low-overhang captures, not only the source atlas. All 1,652 changed pictures stay inside ceiling cells; 1,748 pictures remain exact, including 80 black, 1,479 outside-room and 56 menu pictures. Source checks include 67,420 roof-cell matches and 26,391 unchanged gold floor-body cells. The native jump is interrupted under the restored overhang with identical Y progression. The silent video labels that segment half speed. Exact commands, results and remaining coverage limits are in [SCREEN2_5_ROOF.md](SCREEN2_5_ROOF.md). The ZIP passes all 90 hashes, CRC and flat-layout checks. Actions awaits source push.

## Original brown ceiling restoration (0.8.3 candidate)

Use the unchanged `screen2_5_roof_routes.json` with the same runner and save. `verify_screen2_5_brown_roof.py` compares fresh 0.8.3 captures against the retained final 0.8.1 baseline, requiring exact native state/audio, unchanged stairs/platforms, ceiling-only image changes and exact original brown source pixels. The 6,800 paired frames pass all checks; all 300 stair captures remain identical. See [SCREEN2_5_BROWN_ROOF.md](SCREEN2_5_BROWN_ROOF.md) for full counts and bounded coverage. Static validation checks all 46 original atlas-cell references and all 87 previous runtime hashes. The ZIP has 89 root files and no rejected ceiling atlas. Actual preview images compare 0.8.2 with 0.8.3; the head-bump video is labeled half speed.

## Screen 2-6 and shared artwork (0.9.0 candidate)

Use `screen2_6_routes.json` and `run_screen2_5_qa.py` with the unchanged new save; pair 0.8.3/0.9.0 for 6,580 frames. Add the two previous-room routes in `screen2_6_regression_routes.json` for 3,000 frames. `verify_screen2_6_qa.py` checks 9,580 paired frames, exact native memory/audio, panorama alignment, both dragon poses/directions, both fireball directions and folded/open bats. The short-lived mirrored shot is checked at every observed two-frame sample. Previous-room pictures remain exact except 59 frames of a previously unmapped 1-up now using the existing figurine; its source pixels, native OAM bounds and exact surrounding scenery are required. All 300 stair pictures remain identical.

Static validation requires the shared fallback block to follow every specific rule, preserves every atlas reference and only allows the measured brown palette alias, recovers the exact 0.8.3 hires.txt after removing new blocks, and checks all 87 prior runtime asset hashes. The install contains 90 root files. Coverage reaches 2-6 camera scroll 249; the far exit and new lava/ice traversal are unverified. See [SCREEN2_6.md](SCREEN2_6.md) for commands, provenance and exact scope.

## Level 2 boss and Breaker (0.10.0 candidate)

Use the supplied boss state and `boss2_routes.json` with `run_screen2_5_qa.py`; add the previous-screen routes in `boss2_regression_routes.json`. Five paired routes cover 5,740 frames/build. `verify_boss2_qa.py` requires paired native state/audio, whole visible boss source matches in normal/hit/victory phases, a fully visible unoccluded boss, complete fireball/tome matches, exact native blackouts, Breaker announcement source pixels, unchanged Stage 3 card/arrival/menu and exact prior 2-6 captures. The final rendered-letter guard fixes an initial one-frame early announcement; candidate/regression replays use the final pinned manifest. See [BOSS2.md](BOSS2.md) for commands, source provenance and bounded coverage. The pack contains 93 root files and preserves all 88 prior runtime assets. Stage cards 1–3 are now observed; cards 4–6 remain untested.

## Level 2 boss defeat/pickup repair (approved 0.10.1)

See [BOSS2_REVIEW.md](BOSS2_REVIEW.md). The new gold-defeat save is captured every frame through both reported reappearances, with the original three boss routes as regression. Final checks cover 6,020 frames/build, 3,810 native samples/type, identical APU/common PCM (one 3,196-byte shutdown tail), 38 changes confined to boss tiles and 3,771 exact images. Each changed boss tile's non-sprite pixels must match the complete HD fade source or exposed pale cave pixels. The one empty initial image is recorded. An isolated retained arena capture discrepancy is documented; a complete unchanged-pack repeat passes all 360 images. Only hires.txt, unused boss-atlas cells and README change; 90 other runtime files stay exact. The old black silhouette expectation is historical and no longer applies to this repair.

## Randy during Breaker pickup (approved 0.10.2)

See [BREAKER_RANDY.md](BREAKER_RANDY.md). Capture the supplied defeat state every frame; pair the earlier victory and combat/pose routes as regression. Verify native RAM/PPU/OAM/view and APU/PCM, changed pixels confined to Randy, and visible HD sprite pixels through every final fade phase. The native orbiting effects can occlude part of the source; report the tested pixel count. Preserve every earlier installed image exactly.

## Level 3 movie workflow (0.11.0 review candidate)

See [LEVEL3_OPENING.md](LEVEL3_OPENING.md) for standard `.mmo` replay with its embedded starting state, exact native-core/header versions, synchronized screenshot observer, full paired memory/audio checks, and input-only edge routes. This replaces the need for separate user states for the captured route. Never claim a whole-level or boss test from this opening/corridor recording.

## Level 3 review corrections (0.11.1)

Run the unchanged movie through the synchronized native-core harness, then `verify_level3_review.py` against the retained 0.11.0 capture. Require every new sprite pose, exact native state/audio, unchanged old assets, changes confined to requested artwork and agreement between the wood masks and native cells. Check the top of the climb and forest doorway during motion. Commands and coverage: `LEVEL3_REVIEW.md`.


## Level 3 round shot, branches and collectible boot (0.11.2)

Use the unchanged embedded-state movie and synchronized native-core runner. Compare against the retained final 0.11.1 movie with verify_level3_details.py. Require exact native RAM/PPU/OAM/view, APU and complete PCM; changed pixels must stay within the actual shot, collectible and branch masks. Require complete boot/shot source matches and actual unoccluded branch source pixels. Static validation preserves every branch alpha mask and all previous runtime assets. Controller-only derivatives start on the lowest branch, move to its left support edge, pause, then walk slowly right across the full supported span and off the right collision edge. The trunk is a backdrop here, so do not assume it blocks movement. See LEVEL3_DETAILS.md for measurements.

## Level 3 lava corridor, menu boot, fish and Breaker — 0.12.0

Replay the supplied 3,705-frame movie with stride 2; derive Breaker direction/palette, Blizzard and slow-edge tests with make_level3_lava_routes.py. Replay the earlier 6,883-frame opening movie with stride 4 as regression. Use verify_level3_lava.py on each pair to preserve RAM/PPU/OAM/view/APU/full PCM, confine menu changes to the boot, retain blank menu transitions and blackouts, and compare actual sprites and scenery with the registered sources. Charge pixels occluded by Randy are excluded using native OAM bounds; complete fish templates account for the native hit blink, which omits the fish on alternating frames. Source checks align PPU scroll within one capture interval. Only complete native runs count. Detailed results and commands are in LEVEL3_LAVA.md.

## Fish motion consistency — 0.12.1

Use the same full corridor movie at stride one against retained 0.12.0 and 0.12.1. `verify_fish_motion.py` requires consecutive native samples, complete paired audio, unchanged mappings, image differences confined to the small alternate pose, exact static head/body pixels, and runtime source matches in both directions. Preserve native large-fish hit blinking. See FISH_MOTION.md.

## Large-fish hover stability — 0.12.2

Use the new 1,200-frame user movie at stride one and the previous 3,705-frame corridor movie at stride one. Pair the 821-frame Blizzard derivative at stride one. `verify_big_fish_motion.py` compares all sampled native state and full APU/PCM, restricts differences to the large fish and eligible movement state, checks preserved source pixels and proves zero horizontal oscillation in three measured hover windows. The original-art probe disables only the ten large-fish mappings. See BIG_FISH_MOTION.md.
