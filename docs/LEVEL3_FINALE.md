# Poison Moss Land finale — 0.15.0 review

The user approved the complete 0.14.0 pack and supplied a new movie showing two more screens, ending with the boss. Approval was recorded without changing any of the 104 installed files, in commit d18f058. This new work is on `feature/level3-finale`; 0.14.0 remains the approved continuation and main remains 0.10.2. The review does not push, open a PR, merge, tag or release.

## Recorded scope and appearance

| Room / segment | Coverage |
| --- | --- |
| 9DEE | Previous descent and pause preserved exactly before the new room |
| 9F1A, mode 04 | Final vertical climb, approved emerald terrain and ruin panorama |
| 9F92, mode 04 | Boss combat, ceiling/floor emergence, curved shots, defeat and Overdrive pickup |
| Overdrive announcement | New spell title in the existing Gothic frame |
| Stage 4 title | Existing Golden Temple artwork, native palette 0F131C29, three lives |
| A865 arrival | Recorded first 38 frames: shared Randy/HUD aliases only; scenery remains unfinished |

Four generated sources and exact prompts are retained as art/generated/boss3_*. Native references, identities and registrations are in art/level3_finale/. The coral-pink boss head is fitted as one coherent 62×94 image inside its 64×96 / twenty-cell native union without clipping. Each curved shot is likewise fitted as a whole before cutting its staggered native cells. The floor growth is one 128×48 image; the ceiling uses its vertical flip. Overdrive is the native four-tile orb, not a book. The round shot reuses the approved Level 3 source.

The new builder runs after the approved green retheme. Terrain uses exact prior moss cells and native-byte-identical boss-bank aliases. The living growths follow native background-tile removal; head emergence/occlusion follows native OAM. Because the head carries the behind-background priority bit, the ruin panorama uses priority 1, behind the head, while the living growth tiles stay in front. The backdrop guard includes organic ceiling identities. Native universal-color flashes and the original 0/4-pixel defeat camera shake remain intact. No native state, movement, collision, combat, inventory, audio or IPS changes are made.

Shared 0800/0A00 Randy/HUD/weapon copies require identical native CHR bytes and retain pose guards. Broad aliases remain after existing specific rules. The finale adds 2,505 tile rules, 1,201 conditions and 288 background rules. Its 119 unique 16×16 cells occupy a new 512×512 atlas, index 46. The only two new installed files are Level3_Finale_Tiles_2x.png and Overdrive_Acquired.png. Total: 106 files / 47 atlases. All 102 previous art/audio files remain byte-identical. Removing the four marked finale blocks recovers exact approved 0.14.0 hires.txt; only that mapping file and installed README change among existing files.

## Verification and reproduction

Use the stock MesenCE 2.2.1 native core and synchronized screenshot observer described in LEVEL3_OPENING.md. One emulator process at a time; each replay receives a private pack whose complete manifest is recorded and verified. The ROM, movies, embedded state, emulator binaries and raw captures are excluded from Git.

| Paired route | Total replay frames | Captured samples/type | Exact full PCM bytes |
| --- | ---: | ---: | ---: |
| Supplied movie, stride 2 | 4,812 | 2,406 | 15,379,208 |
| Consecutive defeat/pickup, captures 3,400–4,384 | 4,812 | 985 | 15,379,208 |
| Controller-only edge, captures 1,230–1,740 | 1,740 | 511 | 5,564,972 |

All 3,902 paired RAM, PPU, OAM and view samples per type match exactly. Every APU write and all PCM bytes match on each complete replay. The repeated capture windows are overlapping evidence, not separate gameplay coverage. The supplied-movie check preserves 95 prior-room/pause pictures and 73 native blackouts, and confines the 19 wholly-in-Stage-4 images to shared sprite changes. It finds 167 complete opaque source matches: both boss orientations, all three curved-shot poses in both vertical orientations, the reused round shot and Overdrive. The announcement and Stage 4 card match 183,808 and 188,416 unoccluded source pixels exactly, using Mesen's integer alpha blend.

The consecutive capture verifies all four native flash colors at their original times: RGB 108/6/0, 181/49/32, 234/158/34 and 192/223/255. Eleven normal-costume pickup-fade samples match 15,366 visible HD Randy source pixels with maximum RGB rounding error one. Native OAM/screenshot timing is resolved with whole-sprite offsets bounded by adjacent native OAM positions, never independent cell shifts.

There are 40 PPU/source scenery reconstructions across the movie and edge route. The HUD, observed native actor bounds and native cells changing between adjacent captures are excluded. Minimum agreement is 99.879%; 39 checks are exact within one RGB rounding level, and the remaining sample spans incremental growth removal between captured PPU phases. No matching threshold was relaxed. Source atlases and geometry are checked independently by validate_pack.py. The five inventory tables reproduce exactly through inventory_level3_finale.py against the supplied ROM and baseline capture.

The edge derivative first walks left off the upper ledge onto the lower shelf, holds left against its native stop at X23/Y157, pauses, then traverses slowly right. Frame 1405 is the last support sample at X41/Y157; frame 1406 is X42/Y158, the first fall. Native coordinates are object anchors, not the boot silhouette. The visible platform is not extended to Randy's overhang.

```sh
python build.py
python scripts/verify_release.py
python scripts/verify_level3_finale.py --before "$BASELINE" --after "$FINAL" --out "$REPORT"
python scripts/verify_level3_finale.py --before "$FLASH_BASELINE" --after "$FLASH_FINAL" --out "$FLASH_REPORT" --flashes
python scripts/verify_level3_finale.py --before "$EDGE_BASELINE" --after "$EDGE_FINAL" --out "$EDGE_REPORT" --edge
python scripts/verify_level3_finale_scenery.py --capture "$FINAL" --out "$SCENERY_REPORT"
python scripts/verify_level3_finale_fades.py --capture "$FINAL" --out "$FADE_REPORT"
```

The install ZIP passes all 106 SHA-256 checks, CRC, flat-root layout and no-nested-ZIP validation. The 32.4-second silent preview is actual side-by-side Mesen playback at normal speed, repeating each stride-two sample twice without interpolation. The source ZIP wraps an incremental Git bundle of all five Level 3 branches and exact local fetch/push commands.

Coverage is limited to the recorded route and edge derivative, not every possible boss strategy or the full game. Twin Fire fade aliases are present but not separately live-exercised here. Stage cards 1–4 are now live-verified; 5–6 remain unverified. The earlier fish artwork and stabilization remain untouched. Stage 4 scenery is the next unfinished area.
