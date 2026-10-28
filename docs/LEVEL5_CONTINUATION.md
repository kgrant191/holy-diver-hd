# Demonic Palace late rooms — 0.23.0 review

The user supplied `Holy_Diver_HD(20261028-125935).mmo` for the next Level 5 screens. This candidate starts from approved main `c1a192c31b7594e4430c721bfa6367ce410d9557` on `feature/palace-continuation`. Main remains approved 0.22.2. No push, PR, merge, tag or release is part of this delivery.

## Recorded scope and artwork

| Room / mode | Recorded area | Update |
| --- | --- | --- |
| 8AE6 / 10 | Long lava corridor | Existing palace interior, stone platforms, animated lava and Blizzard ice; complete skeleton/bone aliases |
| 8BD6 / 04 | Narrow platform shaft | Same interior and stone; a complete registered moving lift |
| 8C4E / 10 | Green hall | Same interior and native structural contours; returning rising sentry and alternate skeleton palette |
| 8D3E / 04 | Beginning of skull-lined shaft | Same interior and stone within native block outlines; returning skeleton |

The native wall palettes are decorative. Only their observed identities are made transparent to reveal the approved panorama. Structural palettes retain the native row/column hull, including standing edges, steps and undersides. The moving lift repeats a two-by-two native tile unit; the whole 32x32 HD unit is assembled before slicing and OAM repeats it into the unchanged 64x32 span. This uses the accepted stair material, with no new generated artwork.

The floating skeleton's 12E5–12F6 cells are byte-identical to approved 10E8–10F9. All three recorded palettes reuse its complete head/leg phases in four recorded combinations and bone projectile. The green hall's 12B1–12C2 sentry uses the exact existing source. Randy, HUD, horned guardians, Overdrive and 1-ups retain their established mappings; their art is not redrawn.

Complete rendered guard families cover both 1100/1300 background banks. Every new foreground/background rule has 30/31 flash counterparts following the accepted 0.22.1 approach: unchanged source RGB, flash panorama alpha 176, and preserved native palette/animation conditions. Native all-black and menu palettes remain excluded. The supplied route shows Blizzard and Overdrive, but no Thunder cast or dragon pickup in these new rooms; flash support is structurally verified rather than claimed as live cast coverage.

## Preservation and reproducibility

Only hires.txt, installed README.txt and one new 256x256 atlas differ from the approved installation. All 124 existing art/audio/patch files remain exact. Stripping the three PALACE_CONTINUATION blocks recovers byte-exact 0.22.2 hires.txt. The validator reconstructs and hashes the complete baseline before running every historical validator. No new neighbor probes, ROM/RAM writes, controller changes or audio edits occur in the pack.

The original movie contains 14,595 input frames and an embedded starting state. Replay uses the same translated ROM, unmodified input/state, MesenCE 2.2.1 native core and synchronized screenshot observer as the approved work. Only the frozen complete 0.22.2 installation and final candidate are used for paired evidence. An early diagnostic run without the complete pack is excluded: missing the unchanged entrance IPS makes that run unsuitable for gameplay comparisons.

`inventory_palace_continuation.py` extracts the actual visible identities and native patterns. `build_palace_continuation.py` constructs the removable layer. `verify_palace_continuation_rules.py` checks geometry, source aliases, complete guards, flash cloning and exact baseline recovery. `verify_palace_continuation_replay.py` compares all sampled RAM/PPU/OAM/view files, APU writes and full PCM, checks actual panorama pixels and complete enemy/lift sources, and preserves prior-room/menu/blackout pictures.

```sh
python3 build.py
python3 scripts/verify_release.py
python3 scripts/verify_palace_continuation_replay.py --before BEFORE --after AFTER --out movie_validation.json
python3 scripts/make_palace_continuation_edge.py --movie ORIGINAL.mmo --out EDGE.mmo
python3 scripts/export_palace_continuation_preview.py --capture AFTER --out preview.mp4
```

The supplemental edge movie preserves the original state and first 1,840 controller rows, pauses at the small platform's far-left standing point, then uses intermittent Right input with no jump or attack. Source inputs, ROM/emulator, captures, save states and build archives remain outside Git. The incremental Git bundle starts at approved main; the installation ZIP is flat and requires only one extraction.

The full new route ends in 8D3E. It does not establish completion of that shaft, later chambers or the Level 5 boss.

## Verified result

- Clean build, the complete historical validator chain and all 127 installation hashes pass. The actual ZIP has a flat layout, valid CRCs and matching bytes for every member.
- The full 14,595-frame paired movie passes 7,297 RAM/PPU/OAM/view samples per type, exact APU writes and exact full PCM. All 97 native blackouts and 554 stable preceding-room/menu/lives pictures remain exact. Native sprite-only death frames retain their black field.
- The panorama is present throughout normal recorded gameplay: 3,741 lava-corridor samples, 746 platform-shaft samples, 1,715 green-hall samples and 306 skull-shaft samples. Minimum exact source-pixel counts exceed 120,000 in every room. Native filters and transition submissions are accounted for separately.
- Complete skeleton source poses, bone, guardian, moving lift and rising sentry match actual gameplay pixels. A separate check matches all four recorded skeleton head/leg combinations, including a mirrored pose, against the unchanged approved atlas.
- The final controller-only edge route is 2,000 frames, with consecutive captures from 1,800 through 2,000. All 201 paired native samples, full APU writes and full PCM match. Randy stops at world (607,80), crosses the full platform, enters native falling state at (648,80), then descends at frame 1909. All 46 checked complete platform images match the exact source; the art stays within the native world span [608,640). An earlier slower route was interrupted by enemy contact and is excluded from the clean walk-off claim.
- The 49.92-second preview contains actual final replay footage with the original game audio and decodes without errors. It covers every new chamber, including freeze/thaw, skeleton combat, the moving lift and sentry emergence.

Compact evidence is in `evidence/level5_continuation/`: `movie_validation.json`, `skeleton_combinations.json`, `edge_validation.json`, `artifacts.json` and `build_validation.txt`. The baseline restoration and interrupted setup trials are outside Git and are not cited as paired evidence.
