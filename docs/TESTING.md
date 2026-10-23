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
