## Palace surfaces and Overdrive pickup — 0.32.0

Run `verify_palace_surfaces_rules.py` and the complete historical validator chain on the recovered 0.31.0 baseline. Pair the supplied Level 5 climb, next rooms, late rooms and finale movies, plus the Level 3 finale movie; compare all captured native RAM/PPU/OAM/view and full APU/PCM. The opening movie is an exact-image regression through the unchanged early rooms. Check the controller-only continuation edge route from frame 1800 through the full walk-off at stride one. Require the complete book source in actual captures and unchanged active Overdrive artwork. See PALACE_SURFACES.md and evidence/palace_surfaces/.

## Final recorded Level 6 rooms — 0.31.0

Run the full 8998-frame movie against frozen 0.30.1 and 0.31.0 with synchronized screenshots and the stock-core neighbor bounds observer. `verify_level6_missed_replay.py` requires all native RAM/PPU/OAM/view samples, APU and full PCM to match; actual images must change only in the three requested rooms and retain the selected normal/flash backdrop. Menus, deaths, blackouts and stable 9F3B stay exact. Run the paired controller-only ledge route and `verify_level6_missed_edge.py` for the right wall stop, slow left walk-off and complete source/mask verification. Clean isolated build and `verify_release.py` must reproduce all 173 file hashes and the full historical validator chain. See LEVEL6_MISSED.md.

## Level 6 finale repair verification

Run `python3 scripts/verify_level6_finale_repair_rules.py` and the full historical chain through `python3 scripts/validate_pack.py "build/Holy_Diver_(Tr)"`. The two full replays are checked by `verify_level6_finale_repair_replay.py`, using the final 0.30.0 composite PNGs for the finale and the approved enemy-revision capture for the earlier face room. Use `--earlier` for the latter. Actual image changes must stay inside the requested native cell unions; boss images, blackouts and full state/audio remain exact. See `docs/LEVEL6_FINALE_REPAIR.md`.

# Build and live testing

## Level 6 finale 0.30.0

Pair the full 19,215-frame final-screen/boss/ending movie against approved 0.29.1 at stride one. Require exact RAM/PPU/OAM/view/APU/full PCM, menus/blackouts, connected whole boss forms during native scrolling and lateral motion, and the visible complete ending pose. Verify both ending pose mappings statically and preserve the second pose's native behind-background priority during text. Check all bounded relative body anchors with the native observer. Pair the prior 4,761-frame movie as an exact-image regression; run an isolated build, all historical validators, 165-file manifest, preview decode and fresh main-only source-bundle import. See LEVEL6_FINALE.md.

## Level 6 enemy revision 0.29.1

See [enemy revision](LEVEL6_ENEMY_REVISION.md) for the scoped two-pose blob, bone-gray face and independent original-orb restoration.

## Level 6 crimson organic hall — 0.29.0

Completed validation: the full 4,761-frame new-room replay, 731-frame platform route and 7,648-frame earlier-room regression preserve native state and complete audio. All 7,647 earlier rendered images remain exact. New terrain, face and orb sources, accepted lava/ice/projectile sources, backdrop continuity, isolated clean build and all 151 install hashes pass. See `evidence/level6_organic/`.

Pair the 4,761-frame movie against frozen 0.28.0 at stride one, checking every native state sample, APU/full PCM, room backdrop continuity, menus/blackouts and whole registered terrain/face/orb sources. Pair the previous 7,648-frame movie as an exact-image regression. Use the controller-only edge branch for a left-edge stop and slow right walk-off. Run the isolated clean build, historical validators, 151-file manifest, archive CRCs and source-bundle import. Coverage and results are in LEVEL6_ORGANIC.md and evidence/level6_organic/.

## Level 6 green hall and descent — 0.28.0

Completed: all three paired routes pass native state and full audio checks; the earlier route also passes exact-image regression. All 15 inspected whole sources and both scrolling panoramas pass. The isolated clean build, historical validators, 148-file manifest, archive CRCs and full preview decode pass. Evidence is in `evidence/level6_late/`.

Pair all 7,648 frames of the new movie against accepted 0.27.0, comparing native RAM/PPU/OAM/view/APU/full PCM, menu/blackout images, room-specific panoramas and complete actor/terrain sources. Pair the earlier 3,393-frame movie as an exact-image regression. The 700-frame controller branch tests the entry floor left stop and slow right walk-off. Run an isolated clean build, full historical validators, archive CRCs, manifest checks and source-bundle import verification.

## Level 6 room variety — 0.27.0

Completed validation: full new-room and opening replays plus the corridor edge route match native execution and full audio. Both sentinel hit colors match whole HD sources in both directions. The isolated build passes all historical validators; all 143 install file hashes match. See `evidence/level6_variety/` for results.

Pair the complete 3,393-frame movie with exact 0.26.0, checking both damage palettes, the full climb, A0DF combat, pause and death/card transition. Pair the original 6,427-frame opening movie and the 367 captured edge-route frames. Native RAM/PPU/OAM/view/APU and full PCM must match. Inspect actual whole-source matches, both mirrored hit sources, source masks and room-specific panorama coverage. The new recording contains no Thunder/dragon flash cast; normal/resume/30/31 rules are statically complete. Run the full historical validator chain and isolated clean build.

## Level 6 skull corridor — 0.26.0

Replay all 2528 frames of 20261029-181929 at stride one against 0.25.1 and the candidate. `verify_level6_next_replay.py` requires identical native RAM/PPU/OAM/view, APU/full PCM, exact menus/blackouts and source matches for whole terrain, four sentinel poses, flying skull and both crawler poses. The first full capture predates only the install-note correction from "ghouls" to "flying skulls"; its retained note must match exactly and every runtime byte stays frozen. Edge and original-movie regression use the final complete manifest.

`make_level6_next_edge.py` preserves the original state and first 1400 controller frames, then walks left, stops and slowly walks right off the full 144-native-pixel corridor platform. Pair its 1400–1766 window at stride one with the stock-core neighbor observer. `verify_level6_next_edge.py` compares native state/full audio and the complete 288×160 HD platform. Replay the original 6427-frame Level 6 movie with `--regression`; every screenshot must stay identical. New-room spell flashes have static rule/source coverage only. Keep the complete historical validator chain and 136-file manifest. See LEVEL6_NEXT.md.

## Level 6 ceiling and 1-up — 0.25.1

Pair the complete 1147-frame 20261029-173117 recording at stride 1 against 0.25.0. `verify_level6_repair_replay.py` requires exact RAM/PPU/OAM/view, APU and full PCM; all changed pixels must be inside the newly exposed native ceiling or 1-up footprint, with exact existing stone pixels and complete figurine source matches. Verify the life count changes at native frame 858. Replay the original 6427-frame Level 6 movie against the repair with `--regression` and allow only the requested 1-up changes, with all other rendered pixels exact. Keep the stock-core neighbor observer active. The static validator preserves all 132 earlier assets and projects exact 0.25.0 through the historical chain. See LEVEL6_REPAIR.md.

## Level 6 opening — 0.25.0

Replay the complete 6427-frame 20261029-152041 movie at stride 1 against approved 0.24.0 and the candidate. Compare RAM/PPU/OAM/view, APU writes and full PCM using verify_level6_opening_replay.py. Check the new panoramas in every rendered gameplay frame, including dragon acquisition and Thunder, exact menus outside the cape, native blackouts and complete registered stone/skull/cape source matches. The full-movie capture predates only the versioned README; require every delivered runtime byte to match.

make_level6_edge.py changes only controller input in the original movie: stop at the opening platform’s left edge, walk right slowly and fall naturally. Pair it at stride 1 with check_hd_neighbor_bounds.cpp active. Verify the full platform span and first descent against native state. No RAM edits. validate_pack.py must recover exact 0.24.0 and pass every historical validator; verify_release.py must match all 134 delivered hashes. See LEVEL6_OPENING.md and evidence/level6_opening/.

Palace baseline projections copy unchanged assets into their temporary packs.
Do not hard-link them: GitHub runners may mount the checkout and `/tmp` on
different filesystems. Every projected file still requires its historical
SHA-256 match before invoking the unchanged earlier validators. This portability
fix changes no installed pack bytes.

## Palace 1-up repair — 0.22.2

Pair the full 20261027-235225 movie at stride two against frozen 0.22.1/0.22.2.
Use make_palace_one_up_route.py to reach the upper-hall green 1-up using only
controller input and the original state; capture frames 740–1464 consecutively.
verify_palace_one_up_replay.py requires exact native memory/scroll, APU/full PCM,
all changes confined to the native figurine footprint, complete approved source
pixels and exact surrounding images. Inspect both actual room captures and the
palette transitions. The screenshots alone prove native identity/color, while
the replay supplies runtime coverage. The lava route collects the blue figurine
and increments lives 6→7; the green route does not collect its item. The static
validator preserves all 124 previous assets and the complete historical chain.

## Golden Temple all stairs / victory transition (0.20.2)

Use `verify_level4_transition.py` for paired native/audio and pixel-scope checks and `verify_transition_sources.py` for actual complete-source matches. The installed manifest is frozen per capture. Three earlier stair recordings retain their pre-impact manifest with an exact four-rule scope-equivalence proof; the final movie10 uses the delivered manifest. See LEVEL4_TRANSITION.md and evidence/level4_transition/. Never substitute a synthetic atlas montage for the actual movie.

## Boss entrance and stair underside — 0.20.1

Pair the full7591-frame finale recording and the earlier298-frame controller-only stair edge route at stride1 against frozen0.20.0. Use verify_level4_finish.py for exact native state/full audio, differences confined to the requested stair/door cells, complete source matches and unchanged boss images/blackouts. Static checks recover exact0.20.0 mappings and preserve all113 earlier assets, test the untouched standing edge and exhaust upward doorway-probe bounds. See LEVEL4_FINISH.md.

## Stray ornament repair — 0.19.1

Replay both retained dragon routes at stride1 against frozen0.19.0. Require exact native RAM/PPU/OAM/view, APU writes and full PCM with verify_level4_residue.py. All image differences must stay inside the observed0DF8/0F073703 footprint and equal the unchanged exterior panorama. Keep the existing invalid-neighbor diagnostic enabled. The clean build must recover exact0.19.0 hires.txt after removing TEMPLE_RESIDUE, with every other asset byte-exact.

## Dragon, items and decorative columns — 0.19.0

Pair both unchanged user states through the987-frame flight and610-frame A-button routes at stride1. Replay movie8/movie7 at stride2 and movie6 at stride4 against frozen0.18.0. Require exact RAM/PPU/OAM/view, APU and full PCM, plus pixel differences confined to requested item/form/column cells and native pickup-flash foreground. Verify every observed dragon pose in both orientations, transformation/star/fire, staff in gameplay/menu, and both small drops. Keep the stock-core neighbor diagnostic active and exhaust copied flash-condition bounds. See LEVEL4_DRAGON.md.

## Staff hall and outdoor arena — 0.18.0

Replay unchanged Holy_Diver_HD(8).mmo against 0.17.0 and final0.18.0 at stride2, then replay Holy_Diver_HD(7).mmo at stride2 as regression. Require exact paired RAM/PPU/OAM/view, APU writes and full PCM with verify_level4_staff.py. Check the panorama throughout every stable full-color gameplay sample; require actual complete staff/menu, both ornaments, all four sentinel layouts, observed hit palettes and both native orientations. Menus may change only inside the staff's32x32 icon. Every earlier movie screenshot remains exact. Exhaust new neighbor bounds through verify_staff_neighbor_rules.py and run the existing invalid-read diagnostic during both candidate replays. See LEVEL4_STAFF.md for commands and limits.

## Golden Temple courtyard continuation — 0.17.0

Replay Holy_Diver_HD(7).mmo against approved 0.16.3 and the candidate with the neighbor-bounds diagnostic active. Require exact RAM, PPU, OAM, PPU-view metadata, APU writes and full PCM. Check untouched rooms and menus, complete wings/orb/stone source matches, interior/exterior/re-entry scenery and previous movie regression. See docs/LEVEL4_COURTYARD.md.

## Golden Temple stairs — 0.16.3

Use the unchanged 20261026-181741 save with make_level4_stair_routes.py. Pair its walk, jump and slow-edge routes at stride one, plus the full original movie at stride four, through verify_level4_stairs.py. Require exact native state/full PCM/APU, stair-only pixel changes and complete step-source matches. Inspect the supplied landing, upper contact, descent, room wrap, left stop and right walk-off. Retain the invalid-neighbor observer. See LEVEL4_STAIRS.md for coverage and excluded investigation attempts.

## Golden Temple entry and drops — 0.16.2

Run the exhaustive column-neighbor bounds/truth-table check through validate_pack.py. Replay the unchanged full movie with check_hd_neighbor_bounds.cpp observing the stock core, then pair it against retained 0.16.1 with verify_level4_repairs.py. Require exact native state/full audio, all non-pickup pixels unchanged, and complete heart/crystal source matches. The earlier uninstrumented success did not establish neighbor-read safety. See LEVEL4_REPAIRS.md for the reproduced invalid read, tooling limits and exact coverage.

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

## Next Level 3 caves and multi-fish hover — 0.13.0

Replay the supplied 7,592-frame movie with the synchronized MesenCE 2.2.1 harness, pairing 0.12.2 and 0.13.0 at stride two. Capture the first 2,200 frames at stride one for individual-fish source fits and simultaneous opposite-phase hover. Replay the prior 1,200-frame hover movie at stride one. Use make_level3_cave_edge.py for controller-only backtracking through the open left entrance, a pause, and slow traversal/walk-off of the complete new carved-cap platform. The runner's proportional wall-clock watchdog does not alter emulation timing or input.

Use verify_level3_caves.py for paired memory, APU, full PCM, unchanged menus/blackouts and source sprites; use verify_level3_cave_scenery.py for native-PPU reconstruction in both horizontal and vertical scrolling. Inventory all four nametables and retain solid 0796/0797 supports in the later corridor. Docs/LEVEL3_CAVES.md records exact coverage and limits.

## Poison Moss Land green scenery — 0.14.0

Pair the unchanged 6,883-frame opening movie at stride four against 0.13.0, the 7,592-frame next-room movie at stride two, and the 6,000-frame controller-only cap-edge derivative capturing frames 5,470–6,000 at stride one. Use verify_poison_moss.py for exact RAM/PPU/OAM/view/APU/full PCM, unchanged menus/blackouts/outside-room images and unchanged actor source pixels. verify_poison_moss_scenery.py reconstructs the last four recorded rooms from all four PPU nametables, actual scroll and new source artwork. Inspect actual opening/shaft captures separately. Static validation recovers exact 0.13.0 mappings, preserves all 99 earlier art/audio files and checks each new cell against its original alpha mask. See POISON_MOSS.md for final counts and coverage limits.

## Level 3 finale — 0.15.0

Replay the full 4,812-frame movie at stride two against exact approved 0.14.0. Capture frames 3,400–4,384 consecutively in a separate complete paired replay to inspect alternating defeat flashes. Use make_level3_finale_edge.py for the controller-only far-left stop, pause, slow full-span traverse and right walk-off. Pair native RAM/PPU/OAM/view, APU writes and full PCM with verify_level3_finale.py. Require exact prior-room/pause/blackout images, both boss orientations, all three curved shots, Overdrive and both cards; Stage 4 changes stay inside shared sprite bounds. Use verify_level3_finale_scenery.py for native PPU reconstruction including both measured defeat-shake offsets (0/4), and verify_level3_finale_fades.py for HD Randy source pixels in all three observed normal-costume fades. See LEVEL3_FINALE.md for commands, measured results and coverage limits.


## Golden Temple — 0.16.0 review

Use the supplied 8,668-frame movie against approved 0.15.0 and final 0.16.0. Pair all native state and full audio through verify_level4.py; generate controller-only Overdrive and platform routes with make_level4_routes.py. The actual spell is 0A8A–0A8D; CB–CF is an enemy attack. Verify source panoramas/stone through verify_level4_scenery.py. Scope, commands and bounded coverage: LEVEL4_GOLDEN_TEMPLE.md.


## Golden Temple foreground revision — 0.16.1

Pair the full 8,668-frame recording and 1,485-frame input-only edge route against the final 0.16.0 captures. verify_level4_masonry.py requires exact native state/audio, changes confined to foreground cells, source block/column matches and unchanged panorama pixels. Keep the background/outdoor-column assets and previous mappings exact. Native 0B4E–0B51 destruction is documented from three live events. See LEVEL4_MASONRY.md.

## Demonic Palace 0.21.0

Use the supplied 20261027-212503 movie for the complete recorded opening, both Thunder casts, dragon flight and the 8816 stair-hall entry. Capture stride 2 for full native comparisons, and stride 1 for the derived controller edge routes. Keep the original embedded state. The 20261027-183338 movie is a prior-stage regression. verify_level5_replay.py compares RAM/PPU/OAM/view, APU writes and complete PCM, checks native blackouts and the one-cell H repair, and finds whole registered actor/effect sources in actual captures. Source matches and visual contact sheets complement each other. validate_pack.py retains every historical validator through a byte-exact 0.20.5 projection.

## Demonic Palace repair 0.21.1

Pair the 20261027-221951 climb movie and the prior 20261027-212503 opening movie against 0.21.0, stride 2. Use verify_palace_repair_replay.py with --opening only for the earlier movie. Require byte-exact native/audio data, complete serpent source matches and panorama pixels in every nonblack climb capture. Native transition blackouts must remain exact. The opening comparison confines cavern differences to ceiling cells; all other room/menu images remain exact except the intended 8816 stair padding repair. Static checks preserve all 48 roof masks/conditions and 50 old stair masks/opaque RGB.

## Palace finale — 0.24.0

Pair the full 15,585-frame 20261028-142617 movie with 0.23.0 at stride two. Use `verify_palace_finale_replay.py` for all sampled native data, APU/full PCM, native blackouts/menus, complete source matches and rendered flash panorama checks. The original palette write and visible frame can differ by one submission; inspect actual pictures and retain grayscale/emphasis.

Use `run_mesen_movie.py --stride 1 --capture-windows evidence/level5_finale/capture_windows.json` for complete selected intervals, `verify_palace_finale_consecutive.py` for the repeat and every boss-backdrop frame, then `export_palace_finale_preview.py` for the 60.0988 fps actual preview. No RAM changes or alternate emulator core are used. `verify_palace_finale_rules.py` preserves the full historical validator chain and byte-exact 0.23.0 projection. See LEVEL5_FINALE.md for results and coverage limits.

The pre-card full comparison uses `--candidate-manifest evidence/level5_finale/pre_card_pack_sha256.json`. After the single-frame Stage 6 card correction, run the full movie capturing 15120–15585 consecutively and use `verify_palace_finale_card.py`. Its only allowed image change is frame15374, equal to the previous complete HD Stage6 card. Export the final preview with `--ending` pointing at this last replay; earlier gameplay mappings are byte-identical.
