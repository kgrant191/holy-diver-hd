# Screen 2-6 and shared Stage 2 artwork — 0.9.0

The user moved on to screen 2-6 and asked why repeating enemies and scenery did not already have the finished graphics. This adds shared fallback mappings for known Stage 2 identities, in addition to the new room. Existing room-specific art remains first in Mesen's matching order. The continuation uses 0.8.3's original brown ceiling and accepted cut-stone stairs; it does not imply approval to merge the stacked branches.

## Reuse and new work

`scripts/build_shared_stage2.py` runs last and appends 485 rules referencing existing atlas cells. It removes only each source rule's room/pointer prefix; pose anchors and downward-lava animation conditions remain. Exact native tile identity and palette must match. A measured 0F071737 → 0F081737 terrain alias handles the new room's slightly different brown palette. New or relocated identities still need a verified mapping; this is not fuzzy image recognition. Background transparency stays room-specific.

Shared sources cover the original brown terrain, accepted cut-stone stairs, lava/ice, ghouls, folded/open bats and their shots, winged demons and downward arrows, faceless pulsing rock enemies, eyes with blue tears, player effects and collectibles. Existing mappings win wherever a room already has them. `art/shared_stage2/registration.json` retains every source rule and its derived fallback for review.

Screen 2-6 uses room value 10 and room-data bytes 8D/8E (pointer 8E8D). Its entire 512-pattern PPU bank matches physical CHR 0200–03FF exactly, as recorded in `art/screen2_6/shared_chr.json`. The solid 0346/034E cells are additional registrations using existing brown body cells. The six red nonsolid wall patterns and ten hanging decorations reveal the existing crimson cave panorama. The brown physical ceiling remains visible.

The only new painted subject is the orange/gold bipedal winged dragon. The native creature has two walking poses, a long open snout, wings and clawed arms. Its 31 body identities 02B7–02D5 use the native 96×80 HD canvas; the generated art fits inside it at 92×70, offset (4,10), with zero clipped opaque pixels. Eighteen upper-body cells are exactly shared across poses while the leg identities change. OAM retains the original left/right mirroring. The two-cell 02D6/02D7 projectile reuses `art/boss1/boss_fireball_registered.png` at its native 32×16 HD footprint.

Source and provenance:

- `art/generated/screen2_6_dragon_generated.png`: built-in image-generation result.
- `art/generated/screen2_6_dragon_prompt.json`: exact prompt, tool and native reference.
- `art/screen2_6/native_enemy_reference.png`, `native_enemy_poses.json`: measured native anatomy and OAM layout.
- `art/screen2_6/dragon_pose_0.png`, `dragon_pose_1.png`, `dragon_fireball.png`: deterministic registered art.
- `scripts/build_screen2_6.py`: atlas, mapping and scenery registration.

The install adds only `Stage2_Dragon_2x.png`. All 87 prior runtime asset files remain byte-identical; only hires.txt and README.txt change among the 89 earlier files. The new pack has 90 root files, 39 atlases, 7,536 tile rules, 307 background rules and 1,773 conditions. Static validation strips both new blocks to recover the exact 0.8.3 hires.txt and checks every prior runtime hash.

## Live verification

Use MesenCE 2.2.1 with translated ROM SHA-1 `fe2fcd0ad334d792db16535d09f3ab9fb2bea3ac`. The unchanged 9,650-byte user save `Holy_Diver_HD_1(20261024-223733).mss` has SHA-256 `60945ccab9020ab3fdde2247161a5f119c5ac32d4ec5af3e6385f0aa187df0b2`. No ROM, emulator or savestate bytes are committed.

Five paired routes compare final 0.8.3 and 0.9.0 over 6,580 frames per build: walk/combat, poses, Blizzard cast, menu and attempted traversal. Two prior-room regressions add 3,000 frames from the stair/2-5 approach save, for 9,580 frames and 4,790 samples per native memory type. Inputs use the controller only; no RAM writes. Actual PPU page/fine-scroll metadata aligns the panorama because logical camera RAM is stale at the entrance.

```sh
python build.py
python scripts/verify_release.py
python scripts/run_screen2_5_qa.py --mesen /path/to/Mesen --rom '/path/to/Holy_Diver_(Tr).nes' --pack 'work/screen2_6/baseline_083' --out work/screen2_6/before --state '/path/to/Holy_Diver_HD_1(20261024-223733).mss' --route scripts/screen2_6_routes.json --stride 2
python scripts/run_screen2_5_qa.py --mesen /path/to/Mesen --rom '/path/to/Holy_Diver_(Tr).nes' --pack 'build/Holy_Diver_(Tr)' --out work/screen2_6/after --state '/path/to/Holy_Diver_HD_1(20261024-223733).mss' --route scripts/screen2_6_routes.json --stride 2
python scripts/run_screen2_5_qa.py --mesen /path/to/Mesen --rom '/path/to/Holy_Diver_(Tr).nes' --pack 'build/Holy_Diver_(Tr)' --out work/screen2_6/regression_after --state '/path/to/Holy_Diver_HD_1(20261024-155045).mss' --route scripts/screen2_6_regression_routes.json --stride 2
python scripts/verify_screen2_6_qa.py --before work/screen2_6/before --after work/screen2_6/after --routes scripts/screen2_6_routes.json --out evidence/screen2_6/validation.json
python scripts/export_screen2_6_preview.py --before work/screen2_6/before --after work/screen2_6/after --out evidence/screen2_6
```

The baseline pack is a separately rebuilt 0.8.3 tree pinned to `evidence/0.8.3-pack-sha256.json`. Regression baseline captures are the final 0.8.3 `stair_walk` and `extended_traversal` under `work/screen2_5_brown_roof/after`; recreate them with the regression routes and old pack if absent. Only one Mesen process may run at a time. Every route verifies the installation manifest before and after playback.

The final report preserves 30,605,608 common PCM bytes exactly; one run has a 3,192-byte shutdown-buffer tail difference. It passes all 9,580 paired frames, 4,790 samples per native type, 310 exact panorama pictures, 64 native black captures and 66 menu captures. Complete source matches include 246 bats, 61 dragon poses and 43 fireballs across the required directions.

The verifier requires exact paired RAM/PPU/OAM/PPU-view, APU writes and common full PCM (with at most one audio shutdown buffer), native blackouts, menu preservation and source-pixel panorama alignment. Complete sprites must match both dragon strides and both shot directions, plus folded/open bats. The short-lived mirrored projectile needs every observed two-frame sample: the ten-frame sample at frame 360 overlaps another effect by one pixel; frames 364/366 show the complete source without relaxing the pixel comparison.

Prior-room regression identified a previously unmapped 1-up over the 2-5 lava fall. The shared rules now apply the exact approved front-facing figurine. This is intended automatic reuse: 59 pictures change only inside its native two-cell footprint. The verifier requires the actual approved source pixels and exact surrounding scenery; it also checks the OAM identity/palette. The other 1,441 previous-room pictures, including all 300 stair pictures, remain exact. Native behavior and audio stay identical.

Coverage reaches camera scroll 249 in 2-6 and includes bats, both dragon strides/directions, fireball directions, combat, jumps, menu spell selection, Blizzard flashes and death/return. The final traversal attempt does not reach the far exit. Several controller strategies were explored; only the final declared routes count toward paired results. No hot/frozen lava crossing in 2-6 or full-room completion is claimed. Known lava/ice rules are reused and retain their existing tests. Earlier limits on the 2-5 exit and actual handled-health-jug collection remain.

The comparison and silent normal-speed video use unretouched actual Mesen screenshots. The install ZIP passes flat-layout, CRC and all 90 hashes; the video decodes without errors. Exact results are in `evidence/screen2_6/validation.json`, with archive checks in `local_artifact.json`.

## Source handoff

The ZIP-wrapped incremental bundle includes `feature/screen2-4`, `feature/screen2-5` and `feature/screen2-6`, based on approved main 0.6.1. The older refs stay at their earlier commits; the current combined work is on screen2-6. README_SOURCE.txt contains exact Downloads-based fetch/push commands. Main, merges and releases remain untouched. Source push, PR and Actions artifact checks follow the user's push.
