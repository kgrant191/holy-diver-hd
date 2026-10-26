# Level 3 caves and independent fish hover — 0.13.0 review

This candidate is on `feature/level3-caves`, based on the unapproved 0.12.2 review at `fb1fb4d35b73711cbf6a8f82682322eb21941234`. Main remains approved 0.10.2; approved continuation 0.11.2 is unchanged. No push, PR, merge, tag or release is included in this handoff.

## Scope

| Native room | Mode | Recorded coverage |
| --- | --- | --- |
| 9B96 | 10 | Second fish/lava corridor, green floating creature, frozen pools, stairs and exit |
| 9C86 | 04 | Vertical climb with blade rings, complete recorded ascent and exit |
| 9CFE | 10 | Carved stone caps, lava/ice corridor, thawing, stairs and exit |
| 9DEE | 14 | Initial bat descent and starting viewport before the final pause |

Reuse the exact approved cave panorama, brown terrain, carved step material, lava/ice, bats, blade rings, fireballs, Randy and HUD. The green floating skeletal creature is the only new painting. Its native identities are 06D1–06DC / FF371908; the unmirrored source faces right. The complete 64×64 registration keeps its absent upper-left three cells and lower-right cell transparent, without clipping. The movie provides live coverage of its mirrored form; the other direction is registered from native geometry but is not claimed as fresh live coverage.

Built-in image generation produced `art/generated/level3_green_creature_generated.png`. Its exact prompt and reference are in `level3_caves_prompts.json`; native reference, source patterns, registered pose and reproducible atlas are under `art/level3_caves/`. All other materials are reused. New 0774–077F contours retain their native filled masks. 0796/0797 in the later corridor are solid supports and remain visible; the measured dark-palette wall layer in 9C86 is decorative. All four PPU nametables are inventoried, including the second vertical page.

`build_level3_caves.py` adds 390 tile rules plus guarded backgrounds. Modes, complete room pointers, native palettes and actual rendered-tile guards protect menus and blank transitions. Shared Stage 2 fallbacks remain last. The pack has 101 root files and 45 atlases. Only hires.txt and installed README change among the previous 100 files; all 98 previous art/audio files, including every existing fish-atlas pixel, are byte-identical. One new atlas contains the creature and reused terrain registrations.

## Why the fish still shook

0.12.2 covered only room 9AA6 with exactly one active large fish. The new recording shows room 9B96 and multiple fish, including two hovering in opposite horizontal phases. Its guards therefore left the reported shake unchanged.

The native left-facing fish settles at player screen X+87/+88; the mirrored fish at player X−88/−87. Register each complete existing pose with +1/−1 HD-pixel offsets at those two positions. This averages the two native horizontal positions without changing emulated state or using another fish's direction. Native vertical bob, fin identities, OAM disappearance on hit, attacks, collision and sound remain native. Registration is limited to gameplay mode 10 and the original fish identity/palette. Fish near the viewport boundary retain their original registration: the corrected source-left range is 7–225 native pixels.

Stock MesenCE 2.2.1's mirrored `originPositionCheckX` uses `x - (7 - OffsetX)`, although the sprite OffsetX is already screen-relative. Consequently, a mirrored origin-only condition does not identify the entire sprite cell. Pair each of its eight reported origins with that pixel's `positionCheckX`; unmirrored origins need no workaround. The final builder emits 671 conditions and 26,930 tile rules. The twenty shifted atlas cells are exactly the existing 0.12.2 cells. The fish artwork is neither redrawn nor sharpened.

An isolated fish-only replay proves changes stay inside the large fish while the rest of the image remains exact. `fish_registration.json` proves those isolated probe conditions/rules are identical and identically ordered in the final pack, after removing the separately marked cave blocks. The final combined pack is also captured and checked, including actual source-pixel matches.

## Live verification

Use stock MesenCE 2.2.1, the synchronized screenshot observer, and the supported translated ROM. The new 7,592-frame movie SHA-256 is `facbd98578ae0261fc5707b83cf11ffea8d00966b1af08b9dd555fd6c678f6db`; input/state checksums are in `evidence/level3_caves/input.json`. The native core and ROM are the same pinned files documented in LEVEL3_OPENING.md. Input, state, ROM and emulator bytes remain outside Git.

| Paired route | Movie frames | Captured native samples/type | Equal APU writes | Equal full PCM bytes |
| --- | ---: | ---: | ---: | ---: |
| Full new movie, stride 2 | 7,592 | 3,796 | 18,883 | 24,260,576 |
| New movie, first 2,200 frames at stride 1 | 7,592 | 2,200 | 18,883 | 24,260,576 |
| Earlier hover movie, stride 1 | 1,200 | 1,200 | 2,103 | 3,839,808 |
| New cap edge derivative, frames 5,470–6,000 | 6,000 | 531 | 15,845 | 19,174,552 |

All four pairs preserve RAM, PPU memory, OAM, PPU-view metadata, APU events and full PCM exactly. Repeated full-movie audio is listed per replay, not as unique route coverage. The full route retains 409 stable menu images and 73 black transitions exactly. It provides 47 complete pixel-exact green-creature matches. Earlier levels retain exact assets and recovered mapping blocks; they were not replayed afresh.

Six hover checks match 516 individual fish samples: 203 in the new recording, including two opposite-phase fish in the same 71-frame window, and 313 in the prior recording. Each check changes two alternating horizontal positions into one constant position, with every checked source pixel and native vertical position preserved. Both fish poses and both horizontal directions are observed. The preview uses actual final captures, fixed crops and explicitly labeled quarter-speed repetition; it does not track the fish or interpolate frames.

`verify_level3_cave_scenery.py` reconstructs the panorama and terrain from the actual PPU pages, palettes and registered source cells. All 58 main-route checks and 5 edge-route checks match 100% of exposed tested pixels. Native sprites/HUD are excluded explicitly. Fast vertical camera movement spans several native pixels per frame; reconstruction searches only the scroll interval bounded by adjacent captures, rather than assuming one pixel per frame. Frozen lava and its later thaw are observed in the original route.

The controller-only edge derivative backtracks through the open left entrance into the preceding room, pauses at X221/Y96 for frames 5531–5560, and then slowly traverses the new cap. This is an open connection, not an invented left wall. Stable reentry is frame 5619 at X17/Y96. The final supported anchor is X73/Y96 at frame 5731; frame 5732 is X74/Y97. Both builds agree. The visible cap is not extended to the player's overhanging sprite.

Run one emulator process at a time, using `run_mesen_movie.py` with the standard core/config/audio environment. Its proportional wall-clock watchdog affects only timeout handling, not emulation speed or controller input. Generate the edge movie with `make_level3_cave_edge.py`. Then run:

```sh
python scripts/verify_level3_caves.py --before "$BASELINE" --after "$FINAL" --out evidence/level3_caves/full.json
python scripts/verify_level3_cave_scenery.py --capture "$FINAL" --out evidence/level3_caves/scenery.json
python build.py
python scripts/verify_release.py
```

Dense fish windows use stride one; the earlier hover pair adds `--fish-only`. First empty post-state captures are recorded explicitly. Intermediate art probes and initial incomplete vertical-page inventory are not acceptance builds. `validation.json`, per-route reports, `edge_geometry.json`, source comparisons and flat-ZIP CRC/hash checks pin the final candidate.

## Handoff and remaining scope

The review ZIP extracts directly to the installable pack. The 28.67-second silent video shows the simultaneous fish repair, new creature, vertical climb, stone platforms, frozen/thawing pools and starting bat descent. `comparison.png` contains actual final Mesen pictures.

The source ZIP wraps an incremental Git bundle containing `feature/level3-opening`, `feature/level3-lava` and `feature/level3-caves`, with exact local fetch/push instructions. The user pushes the artwork with their local Git credentials. Later portions of the descent, subsequent rooms and the boss remain unfinished/unverified. This build awaits user review.
