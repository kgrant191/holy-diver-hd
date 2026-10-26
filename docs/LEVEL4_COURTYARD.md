# Golden Temple hall and courtyard — 0.17.0 review

The user accepted 0.16.3 and supplied the next recording. This continuation carries the approved treatment through the next hall and outdoor courtyard, updates the wings and fire chain, and restores the indoor background at the recorded re-entry. Work is on `feature/golden-temple-courtyard`; main remains approved 0.15.0. No publication, PR, merge or release has been performed.

## Recorded scope

| Room / RAM mode | Treatment | Recording coverage |
| --- | --- | --- |
| AA81 / 08 | Existing approved interior | Starting tail, unchanged |
| AAF9 / 08 | Enclosed Golden Temple hall | Complete traversal, stairs and wings |
| AB71 / 10 | Outdoor Golden Temple courtyard | Complete traversal, fire chain and entrance |
| AC61 / 04 | Enclosed Golden Temple hall | Initial arrival only, then the user pauses |

Later AC61 traversal and the rest of Level 4 remain untested. Do not describe this as a completed level.

## Registration

`build_level4_courtyard.py` runs after the unchanged 0.16.3 stair repair. It clones the final approved room mappings in their original priority order, including the restored stairs and the ordered short-circuit pillar bounds. Removing its three marked blocks recovers byte-exact 0.16.3 `hires.txt`. All 109 earlier art/audio/patch assets remain byte-identical; the candidate adds atlas50 and changes only the mapping file and installed README among earlier files. The install contains 112 root files.

Backgrounds, worn sandstone, cracked breakables, stair shapes, interior supports and exterior fluted columns reuse approved artwork. AAF9's decorative window palette `0F071723` reuses some staircase-shaped CHR cells; it is cleared only in this room's wall context. The recorded physical stone uses `0F172737`. The following indoor room's decorative palette is `0F071727`. Twelve rendered-tile guards select the appropriate panorama without replacing pause screens or blank transitions.

The courtyard's original purple clouds and decorative screens reveal the accepted exterior panorama. Alternate capitals reuse the approved complete four-cell capital. Existing gargoyle art supplies two gold-stone architectural poses. Their unique four-by-four native layouts share one foot cell; bounded left/right neighbor probes select the opposite pose without cutting it apart at a screen edge. The recessed entrance stays dark. No new generated scenery is introduced.

The wings are native `0A92/0A93`, rendered as one joined 32×16 HD source before slicing. Eight byte-identical CHR copies reuse that art with the observed `FF301116` palette. The new enemy is eight independently moving `0AE1/FF162830` fire beads. Each is registered in its own 16×16 native cell; the game retains all chain motion, formation changes, attacks and defeat behavior. No static ring replaces the native animation. The recording does not show a wings pause-menu icon; none is invented.

The two new painted sources and exact image-generation prompts are in `art/generated/level4_courtyard_prompts.json`. Registered sprites, native inventories, palette counts, alias proofs and mapping provenance are in `art/level4_courtyard/`. `inventory_level4_courtyard.py` reproduces all seven inventory/proof files from the unchanged original ROM and paired baseline captures. Build and static validation need neither ROM nor emulator.

## Verification

Use the stock MesenCE 2.2.1 native core, supported translated ROM and the existing synchronized observer. Run only one emulator at a time. The input movies and embedded states are unchanged; no RAM writes or fabricated gameplay are used. The neighbor-bounds diagnostic is enabled during accepted candidate replays and is never shipped with the pack.

```
python build.py
python scripts/verify_courtyard_neighbor_rules.py
python scripts/verify_level4_courtyard.py --before BEFORE --after AFTER --out evidence/level4_courtyard/movie.json
python scripts/verify_level4_courtyard.py --before EARLIER_BEFORE --after EARLIER_AFTER --regression --out evidence/level4_courtyard/regression.json
python scripts/verify_release.py
```

`movie.json` requires exact RAM, PPU, OAM, PPU-view metadata, every APU write and full PCM across the supplied 4,386-frame recording. All visual changes stay within the requested rooms, allowing only the documented two-capture metadata interval at room transitions. Actual complete source matches cover the wings, fire bead, both statue poses and solid masonry. Nine actual scenes compare exact panorama pixels, including the return indoors. Pause samples and native black frames remain intact.

The earlier 8,668-frame Level 4 recording is replayed against the frozen 0.16.3 result. Its regression requires every screenshot as well as native state and full audio to remain exact. Static validation also preserves every previous recovery/geometry/bounds check. The two new statue probes pass all 122,880 screen-coordinate cases; inherited pillar rules remain exact copies of the already exhaustively checked rules.

`evidence/level4_courtyard/` contains the accepted reports, input/runtime provenance and actual comparison frames. The 29.47-second preview is a silent, normal-speed cut of paired emulator captures; labels are outside the game image. The final re-entry still is held for two seconds. No game pixels are retouched.

The accepted paired runs cover 13,054 frames per build and 4,361 native samples per type, with 41,716,360 full PCM bytes identical. All 2,168 earlier screenshots remain exact. New-room checks find 12 complete wings, 466 fire beads, 68 statue poses and 4,344 solid-stone source matches. All 212 pause samples remain unchanged.

## Handoff

The source ZIP contains an incremental Git bundle for both `feature/golden-temple` (including the 0.16.3 approval record) and `feature/golden-temple-courtyard`, based on main `2f38abeb06cd1093fc33416da20c5124fca2f4d7`. ROM, save states, movie inputs, emulator binaries, raw captures and the install ZIP are excluded. Artwork prompts, registered sources, builders and verification evidence are included. The user can publish with their own Git credentials after review.
