# Demonic Palace opening — 0.21.0 review

This focused branch starts at approved main 0.20.5. It updates the opening shown in the user's 9,921-frame movie, and restores the missing H in THUNDER on the Start/pause screen. It is a review candidate; main remains approved 0.20.5.

## Recorded scope

| Room | Covered content |
| --- | --- |
| 850A / 18 | Gothic lava cavern, native rock platforms, floating skeletons/bones, rolling jade boulders, lava and Blizzard freeze/thaw |
| 8672 / 04 | Vertical crimson-column chamber, death/restart, climb |
| 86EA / 08 | Following column hall and distant frieze |
| 8762 / 04 | Segmented serpent, two Thunder casts, dragon pickup/transformation/flight |
| 8816 / 04 | First stair-hall entry only, followed by the pause menu |

The later staircase route, remaining Level 5 rooms and boss are outside this movie. Stage cards 5–6 still have no new live title-card coverage. Do not describe this as the completed level.

## Artwork and mapping

Eight generated whole raster sources are retained in `art/generated/palace_*.png`, with exact generation prompts in `palace_prompts.json`. `prepare_level5.py` registers whole skeleton poses before slicing, preserving shared skull/body/arm cells. Rolling rock poses use the same registered source rotated as native animation advances. The worm head and individual body segments remain independent OAM actors. `build_level5.py` registers Thunder cores along the original staggered four-cell lightning shapes; native mirrored directions and timing remain authoritative.

The cavern uses dark Gothic arches behind gray-olive stone. The interior uses distant crimson vaults and complete carved red spiral columns with a single cap. Physical contours retain their standing edges; internal rock texture gaps are filled as solid stone. The first stair hall reuses existing cut-stone material. Only observed nonsolid wall/frieze families are cleared. Room/mode/palette guards restrict all scenery, and rendered-position guards suppress panoramas during native flashes and blackouts. Each new roof neighbor probe has a preceding screen bound.

Sprite bank 1000–1074 is byte-identical to the approved 0A00–0A74 player/HUD bank. Conditional aliases preserve complete pose signatures and take priority over broad aliases. Background 1300 is an exact copy of 1100 and receives the same room-scoped mappings. Approved lava/ice, Randy, HUD, pickups and dragon sources are reused. The missing H was a menu mapping to an empty atlas cell; the repair is restricted to 0946/0F072830 in the magic row.

## Preservation and validation

All 117 earlier image/audio/patch files remain byte-exact. The only installed changes are hires.txt, the versioned README, and three new Palace PNGs. Stripping the four named Palace sections recovers the exact approved 0.20.5 hires.txt. Validation constructs and hashes all 119 approved files, then runs the complete original validator on that recovered projection. Historical checks are retained. New checks cover room scopes, CHR equality, whole skeleton unions/shared cells, Thunder H, ordered neighbor bounds and all new references.

Live evidence is in `evidence/level5/`. Tests use actual MesenCE 2.2.1, the supported ROM and native controller input. No emulated RAM, collision, timing or audio is edited. The source handoff excludes ROM, emulator, movie/savestate bytes, raw frame dumps and build archives.

## Reproduce

```sh
python3 build.py
python3 scripts/verify_release.py
python3 scripts/verify_level5_replay.py --before BEFORE --after AFTER --out REPORT.json
python3 scripts/make_level5_edge_routes.py --movie USER_MOVIE.mmo --out LOCAL_ROUTES
python3 scripts/export_level5_preview.py --capture AFTER --out Demonic_Palace_v0.21.0_preview.mp4
```

Use `--edge` for controller edge comparisons and `--regression` for the prior-stage movie. See the existing run_mesen_movie.py interface and docs for native runtime setup; diagnostic binaries are local test tools, never pack dependencies.

## Verified result

- Complete supplied movie: 9,921 frames; 4,960 synchronized samples each of RAM, PPU, OAM and scrolling/view state are byte-exact against approved 0.20.5. Complete APU writes and PCM audio also match. All 209 sampled native blackout frames remain exact.
- Actual captures contain complete source matches for all three skeleton poses in both horizontal directions, the bone, three boulder poses, serpent head and body, and all three Thunder shapes (21 orientation/pose variants total).
- 524 stable rendered menu captures confine the change to the H; changed pixels occupy HD rectangle (257,275)–(270,285), within its original cell. Every other menu pixel stays exact.
- Controller-only edge routes: 660-frame left-stop/span route and 950-frame slow-right-walkoff route. Paired native state and full audio match. The initial stop remains x=23, the first obstruction x=121. The elevated platform holds y=128 before the native drop to y=160; the lower edge then falls toward lava. Actual edge screenshots are retained.
- Prior-stage regression: all 2,855 nonempty images are exact through 2,856 frames, including 195 blackouts. Native state, APU and full PCM match.
- Clean build plus all historical/new validators pass. The final flat ZIP has 122 files; every member matches the frozen candidate manifest and passes CRC verification.

The preview is a 52-second selection of actual final captures with native audio, plus a brief hold on the final menu. Its clip manifest is retained. Main is still approved 0.20.5; this 0.21.0 candidate awaits visual review.
