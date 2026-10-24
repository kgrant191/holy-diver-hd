# Stage 2 screen 4 — second horizontal cave (0.7.0 candidate)

Review branch: `feature/screen2-4`, based on approved main `5fdae8a88920ad6612d9f01ee913d85af6837209` (0.6.1). The user supplied `Holy_Diver_HD_1(10).mss` and requested the next screen, reusing previous work. This candidate has not been approved or merged.

## Reuse and registration

The entire 8,192-byte native pattern bank (512 tiles) matches the earlier exterior bank. `art/screen2_4/shared_chr.json` records the captured bank hash and both input hashes. Existing winged demons, downward arrows, faceless pink/crimson pulsing rocks, terrain, breakable blocks, pickups, player and HUD are reused. The cave panorama and animated lava/static Blizzard ice are also unchanged approved sources.

There are 304 scoped aliases into prior mappings. Forty-four new tile rules register the additional ceiling shapes and clear nonsolid wall patterns. The only added PNG is a 128×64 atlas containing nine unique cells: four accepted gold-texture cells, four native-contour ceiling edges and one transparent cell. No new painted source is introduced.

| Native identities | Treatment |
| --- | --- |
| Existing exterior sprites and `032E–034A` | Reuse approved enemy, item and terrain mappings |
| `035B–035E`, `0389–038E`, `03A1–03A2` | Reuse pool, sixteen-phase downward falls and static ice |
| `0350–035A`, `0369–036C`, `0381–0388`, `038F–0396` | Existing gold texture registered to ceiling cells |
| `0397–039A` | Existing gold texture clipped to native lower contours |
| `0300`, `036E–036F`, `039B–03A0`, palette `0F061828` | Transparent nonsolid wall motif, revealing the cave |

Rules are limited to RAM `$0072=10`, `$0078=AD`, `$0079=8C`. The panorama also requires the rendered gold/wall tile and the incoming wall palette. The palette guard prevents it appearing over the previous vertical cave while the game changes its room pointer before replacing the picture. Rendered-tile guards preserve native blackouts. Removing the three `SCREEN2_4` sections recovers the exact approved 0.6.1 mapping file.

Native collision, movement, inventory, lives, timing and audio remain controlled by the unchanged game. All 83 existing runtime asset files retain their hashes; only `hires.txt` and installed `README.txt` change, and the one atlas is added. The pack contains 86 root files.

## Reproduce the checks

Use MesenCE 2.2.1 and the unchanged translated ROM (SHA-1 `fe2fcd0ad334d792db16535d09f3ab9fb2bea3ac`). Keep the approved 0.6.1 pack separately. Run one emulator process at a time:

```sh
python build.py
python scripts/verify_release.py
python scripts/run_screen2_2_qa.py --mesen /path/to/Mesen --rom '/path/to/Holy_Diver_(Tr).nes' --pack /path/to/0.6.1-pack --out work/screen2_4/before --state '/path/to/Holy_Diver_HD_1(10).mss' --route scripts/screen2_4_routes.json --stride 2
python scripts/run_screen2_2_qa.py --mesen /path/to/Mesen --rom '/path/to/Holy_Diver_(Tr).nes' --pack 'build/Holy_Diver_(Tr)' --out work/screen2_4/after --state '/path/to/Holy_Diver_HD_1(10).mss' --route scripts/screen2_4_routes.json --stride 2
python scripts/verify_screen2_4_qa.py --before work/screen2_4/before --after work/screen2_4/after --routes scripts/screen2_4_routes.json --state-sha256 ce8fd0ed2f9316c7edd64eef51a532e38325185c394a224371fcd7a944d7f47a --out evidence/screen2_4/verification.json
```

Replay `scripts/screen2_4_approach_routes.json` separately from the previous `Holy_Diver_HD_1(9).mss`, with baseline/candidate outputs `approach_before` and `approach_after`. Pass those outputs, the approach route file and that state's SHA-256 to the same verifier. Then run:

```sh
python scripts/verify_screen2_4_motion.py --after work/screen2_4/after --out evidence/screen2_4/motion.json
python scripts/export_screen2_4_preview.py --before work/screen2_4/before --after work/screen2_4/after --out evidence/screen2_4
```
 The route descends the previous vertical room and enters the requested cave.

The replay controller reads native state to time jumps and Blizzard, but never writes game memory. Every second frame captures RAM, PPU memory, OAM and an actual screenshot; all APU writes and continuous PCM are retained locally. The verifier compares native state/audio exactly, checks the pause menu and outside-room pictures, preserves blackouts, and matches complete reused sprites and cave pixels against their source art. The displayed horizontal camera trails endFrame RAM by two frames, so source-image matching uses that measured alignment. Grayscale/death frames are inspected separately from full-color source matching.

Final paired checks pass **12,760 frames per build**, with **6,380 identical samples per RAM/PPU/OAM type**, exact APU events and common PCM. There are 257 exact native black captures, 1,427 unchanged outside-room captures, and 4,511 full-color samples with cave coverage; 451 sampled images match the panorama's exact source pixels. Complete sprite matches cover all four demon wing/arrow poses in both directions, the downward arrow and all three unmirrored pulsing-rock poses. The maximum audio shutdown-tail difference is 0 bytes (at most one 3,200-byte capture buffer).

The route passes the breakable-block ledges and reaches the first two falls and lava pool, with actual camera travel reaching 537 pixels. Initial/transition RAM scroll 512 can be stale and is not treated as proof of travel. Both-direction movement, up/down casts, pause/resume, freeze/thaw and death/respawn are included. The separate approach descends the previous vertical room and enters this cave while preserving outgoing images. **The far exit has not been reached; complete room traversal is not claimed.**

The actual fall pixels move downward by two HD pixels in all 647 stable-palette, stationary-camera comparisons; none move upward or remain stationary. All 456 frozen comparisons remain stationary. The motion report records 31 distinct hot crops across the native pulsing palettes. The first visual review found two remaining nonsolid wall-tip identities (036E/036F); those are cleared in the final build, and all candidate replays were repeated after the correction.

The comparison image and 29.8-second silent video contain actual, unretouched paired Mesen screenshots. Every-second-frame captures play at 30 fps. `preview_sources.json` identifies each source frame/clip; native audio preservation is tested separately. `summary.json`, `verification.json`, `approach.json` and `motion.json` retain the measured results.

## Delivery

`evidence/0.6.1-pack-sha256.json` pins the approved baseline. `evidence/0.7.0-pack-sha256.json` and the historical filename `approved-pack-sha256.json` pin this review candidate; the latter filename does not grant approval. The install ZIP has `hires.txt` and assets at its root, with no nested ZIP. The incremental source bundle is based on main 5fdae8a. User push, PR and Actions artifact verification remain pending. No release/tag is requested.
