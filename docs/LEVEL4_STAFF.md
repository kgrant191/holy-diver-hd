# Golden Temple staff hall and outdoor arena — 0.18.0 review

The supplied recording continues through the previously untraversed staff hall, then enters an outdoor arena. This update repairs the disappearing interior background and incomplete upper ornaments, gives the staff pickup and Start-menu icon the same finished artwork, and applies the exterior treatment to the following encounter. Work is on `feature/golden-temple-staff` from frozen 0.17.0 commit `55382eb`. Main remains approved 0.15.0; the last explicit Level 4 approval is 0.16.3. No publication, PR, merge or release has occurred.

| Room / mode | Treatment | Recorded coverage |
| --- | --- | --- |
| AC61 / 04 | Enclosed Golden Temple interior | Climb, upper ornaments, staff pickup and pause menu |
| ACD9 / 18 | Outdoor Golden Temple arena | Entry, combat, pause, player death and lives card |

The recording does not defeat the sentinel or reach a subsequent room. Victory, rewards and later areas remain untested.

## Backgrounds and upper artwork

The old AC61 background condition matched only its entrance view. The new layer covers the recorded rendered identities and palettes through the climb. Rendered guards preserve menus, loading transitions and native background disable on death. Scenery images are reused byte-for-byte; no replacement panorama is painted.

The upper ornaments reuse both complete courtyard statue layouts in the hall's `0F172737` palette, including their context-dependent shared foot. The room's `0F071727` wall details are decorative, including B80/B81 in that palette. Physical stair mappings remain exact.

The arena uses physical background bank `0D`, although all 256 patterns are identical to `0B`. A byte-search inventory alone reports the first matching bank and cannot distinguish this. Arena tile rules and their neighbor signatures are remapped to `0D`; native equality is retained as a build-time proof. Complete final outdoor stone, columns, ornaments and scenery rules are reused. Doorway bounds precede the new neighbor probes; changing the order preserves the predicate while preventing an out-of-screen lookup. Previous installed rules remain exactly recoverable.

## Staff and actors

The staff is native `0A95/0A96`, palette `FF26173A`, in a 16×32 HD footprint. The 32×32 menu composition centers that identical image and maps 096A/0969 above 0968/0956 at exact native origins (40/48,104/112). Position guards keep the common 0956 pattern from changing elsewhere.

The arena's `0C00–0C74` actor/HUD bank is byte-identical to `0A00–0A74`. Aliases include the existing sprite-neighbor pose signatures and follow every earlier specific mapping, preserving normal/Twin Fire Randy, poses and HUD priorities. Native Randy-shaped enemy phases reuse those approved silhouettes with the observed palette treatments.

The crimson armored sentinel uses four observed OAM layouts, each registered as a complete 96×96 image before slicing. The registration preserves all native shared cells, fits every opaque pixel inside the native cell union, and keeps head/torso pixels stable during stepping. The attack uses the native chest-cannon layout and retains its genuinely absent upper-right cell. Native OAM controls mirroring, motion, hits and visibility; no RAM is edited. Normal, white and blue hit palettes are mapped. The round cannon shot reuses byte-proven finished 0A94 art through 0CF8; the small 0CF7 ember reuses the existing fire bead.

Exact generation prompts and original sources are retained in `art/generated/level4_staff*_prompt*.json` and `temple_*.png`. The first attack draft is retained for provenance but is not a runtime source. `prepare_level4_sentinel.py` registers the final corrected art. `inventory_level4_staff.py` reproduces the inventories, CHR proofs and canonical OAM layouts from the unchanged input and supported ROM.

## Verification

Both final replays use the stock MesenCE 2.2.1 native core, synchronized HD screenshot observer and invalid-neighbor diagnostic. Only one emulator runs at a time; each run uses a private immutable pack copy. The diagnostic and emulator are not shipped.

```sh
python build.py
python scripts/verify_staff_neighbor_rules.py
python scripts/verify_level4_staff.py --before BASELINE_MOVIE8 --after FINAL_MOVIE8 --out evidence/level4_staff/movie.json
python scripts/verify_level4_staff.py --before BASELINE_MOVIE7 --after FINAL_MOVIE7 --regression --out evidence/level4_staff/regression.json
python scripts/verify_release.py
```

The new 3,632-frame recording and earlier 4,386-frame recording are sampled every two frames. The verifier requires exact paired RAM, PPU, OAM, view metadata, every APU write and complete PCM. Earlier screenshots must all remain exact. The new-room checks require exact panorama pixels in every stable full-color gameplay sample, both complete upper ornaments, all four sentinel layouts, observed palettes/orientations and the staff in both places. Pause-image changes are confined to its 32×32 menu slot.

Native menu blackouts and the player's death sequence are preserved. On death, the game deliberately disables the background while retaining player/HUD sprites. The verifier proves this from the old picture outside the native HUD cells and full observed death-actor extent and requires the same black region in the candidate. HUD masks use the documented two-sample interval around submitted frames; the rapidly alternating death fragments use their full measured extent; this is not treated as the reported gameplay background dropout.

All twelve new ordered neighbor chains pass 737,280 screen-coordinate cases with zero unsafe reads. The existing bounds, stair and earlier-art checks remain active. Removing the four `TEMPLE_STAFF` blocks recovers exact 0.17.0 `hires.txt`; all 110 earlier art/audio/patch assets retain their hashes. The install adds atlas51, changes only `hires.txt` and README among prior files, and contains 113 flat root files.

Final machine-readable counts and checks are in `evidence/level4_staff/{movie,regression,summary,archive}.json`. Comparison PNGs and the preview use unretouched actual emulator frames with labels outside the game image. The silent preview runs at normal speed and holds its final arena still for two seconds.

Final paired verification covers 8,018 frames per build and 4,009 samples per native-memory type, with 25,627,656 full PCM bytes identical. All 2,193 earlier screenshots remain exact. Background checks pass 1,221 indoor and 297 outdoor stable gameplay samples; every checked picture contains at least 110,202 exact panorama pixels. Complete source matches cover 79 staffs, 122 ornaments and 34 sentinel poses, with 113 menu staff matches.

## Source handoff

The ZIP-wrapped incremental Git bundle includes `feature/golden-temple`, `feature/golden-temple-courtyard` and `feature/golden-temple-staff`, with approved main `2f38abeb06cd1093fc33416da20c5124fca2f4d7` as its prerequisite. Its README provides exact verification, fetch and push commands. ROM, movie/state inputs, emulator binaries, raw captures and build archives are excluded from Git. No repository publication is performed by this handoff.
