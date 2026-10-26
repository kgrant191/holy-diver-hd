# Poison Moss Land — 0.14.0 review

The user asked for Level 3 to look greener and distinct from the reused caves and rocks. This candidate is on `feature/poison-moss-land`, based on unapproved 0.13.0 at `06a53b9326b0f39f36eec3e95180381647257672`. Main remains approved 0.10.2 and the approved continuation remains 0.11.2. This handoff does not push, open a PR, merge, tag or release.

## Artwork and scope

New painted panoramas show a moss forest and an overgrown Gothic conservatory, with ivy, ferns, emerald columns and green mist. The foreground uses newly painted dark emerald masonry, bright moss ledges, sage carved treads and solid green ceiling/support blocks. The new direction supersedes the historical instructions to reuse brown cave terrain in Level 3. Earlier levels retain their original artwork.

| Room | Recorded area |
| --- | --- |
| 988A | Forest approach |
| 997A | Oak-tree climb |
| 99F2 | Stone shaft |
| 9AA6 | First fish/lava corridor |
| 9B96 | Second corridor and green creature |
| 9C86 | Vertical blade-ring climb |
| 9CFE | Carved-cap/lava corridor |
| 9DEE | Beginning of the bat descent only |

Three image-generation sources and exact prompts are in `art/generated/poison_moss_*`. `scripts/build_poison_moss.py` mechanically resizes/crops these sources, retaining the original terrain alpha bytes. Its 535 room/palette-specific terrain overrides preserve the original condition order. It changes 910 existing Level 3 backdrop references and leaves the continuous oak overlays and branch wood intact. Each panorama uses a 1024-HD-pixel period made from a 512-pixel source crop and its mirror, then repeats that complete period. Stock Mesen derives horizontal background scroll from the PPU address, wrapping at 512 native pixels. Matching that period keeps both the midpoint and camera wrap seamless. Static validation checks every repeated period and both adjoining edges.

Every existing gameplay guard, native contour, solid support and lava/ice source remains. The green artwork does not extend platforms to Randy's overhanging boots. Actors, both fish poses and the independent per-fish stabilization from 0.13.0 remain exact. The new 512×256 atlas is image index 45; total atlas count is 46. `art/poison_moss/registration.json` records every prior/new rule, alpha hash and background substitution.

The install has 104 root files. Among the previous 101 files, only hires.txt and README.txt change; all 99 previous art/audio files are byte-identical. The three additions are Poison_Moss_Tiles_2x.png, Poison_Moss_Forest_Background.png and Poison_Moss_Ruins_Background.png. Static validation removes the marked overrides and reverses the recorded backdrop substitutions to recover exact 0.13.0 hires.txt. No ROM, IPS, state or audio edits are introduced.

## Verification method

Use stock MesenCE 2.2.1, the synchronized HD screenshot observer and the supported translated ROM, pinned as in LEVEL3_OPENING.md. Replay the unchanged 6,883-frame opening movie at stride four and the unchanged 7,592-frame next-room movie at stride two. The opening baseline was freshly captured from the exact 0.13.0 pack; the later-room baseline is the retained final 0.13.0 replay. Run one emulator process at a time.

Also replay the existing 6,000-frame controller-only edge derivative, capturing frames 5,470–6,000 at stride one. This backtracks through the open entrance, pauses, crosses the full carved cap slowly, and walks off its right edge. Native support ends at sprite origin X73/Y96 on frame 5731; frame 5732 is X74/Y97. The native object Y values are 112 and 113, respectively; the sprite origin is 16 pixels above that anchor. The left connection remains open and is not treated as a wall.

`verify_poison_moss.py` compares RAM, PPU memory, OAM, actual PPU-view metadata, every APU write and full PCM. It requires exact menus, blackouts and outside-scope pictures. Complete opaque fish/creature source pixels found in the previous capture must remain exact at the same coordinates in the new picture, including both fish directions and poses. This checks preservation of the earlier fix; it does not claim a new correction to native fin, vertical or hit-blink motion.

`verify_poison_moss_scenery.py` reconstructs the last four rooms from all four native PPU nametables, captured palettes, actual scrolling, new terrain sources and the new ruin panorama. It excludes the HUD and conservative native actor bounds, and searches only the scroll interval bounded by adjacent captures. Opening forest, wood overlays and shaft are inspected in actual captures separately; they are not claimed as part of this full source reconstruction.

```sh
python build.py
python scripts/verify_release.py
python scripts/verify_poison_moss.py --before "$BASELINE" --after "$FINAL" --out "$REPORT"
python scripts/verify_poison_moss_scenery.py --capture "$FINAL" --out "$SCENERY_REPORT"
```

The silent side-by-side video uses actual paired Mesen captures at normal speed, repeating each sample for its capture stride without interpolation or tracking. The source ZIP wraps an incremental Git bundle of the four Level 3 feature branches, with exact local fetch/push commands. No input movies, embedded states, ROM or emulator binaries enter the repository or source handoff. Later portions of the descent and the boss remain unfinished and unverified.

## Final build and live results

The accepted test candidate is identified by `evidence/0.14.0-pack-sha256.json`. Each paired verifier requires that complete manifest in the replay's private installed pack, as well as the exact frozen 0.13.0 baseline manifest. The initial panorama probe is excluded: it repeated over a longer period than the emulator's PPU camera wrap. The final source now repeats at the actual 512-native-pixel boundary, with strict source matching retained.

All 58 final later-room scenery checks match 100% of exposed tested pixels. The threshold was not weakened. Opening captures independently show the forest, wood overlays and shaft; the foreground's 535 alpha masks remain byte-identical to their prior registrations. The final ZIP passes CRC, all 104 hashes, flat root layout and no-nested-ZIP checks.

| Final paired route | Frames replayed | Captured native samples/type | Equal full PCM bytes |
| --- | ---: | ---: | ---: |
| Opening movie, stride 4 | 6,883 | 1,721 | 21,995,512 |
| Next-room movie, stride 2 | 7,592 | 3,796 | 24,260,576 |
| Edge derivative, stride 1 in final segment | 6,000 | 531 | 19,174,552 |

All 6,048 paired samples per native-memory type match. Full APU/PCM comparisons pass on each complete replay. There are 204 unchanged complete opaque actor-source matches, including both fish poses/directions and the recorded green creature direction. All 63 scenery/edge reconstructions match 100%. The edge derivative repeats part of the next-room movie; these counts are per replay, not unique gameplay coverage.
