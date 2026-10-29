# Level 6 opening — 0.25.0 review

Screens 1 and 2 now have their own cold blue-violet citadel scenery: distant ruined spires in the opening shaft and an enclosed Gothic hall beyond it. Dark stone, carved cornices and ivory skull blocks keep native solid/breakable shapes readable. A purple cape with ivory lining and gold trim replaces the original lower-right Start-menu icon.

This is a local review candidate on `feature/level6-opening`, based on approved main `f716c2a7071bf6344e2e52b10b6df8b61d3e929b` (0.24.0). No push, PR, merge, tag or release was performed. Later Level 6 rooms and the boss remain unfinished.

## Implementation

- Gameplay scopes: 9A8B/mode04 and 9BB7/mode10. The brief 9CA7/mode0C interval preserves the outgoing shaft scene; it does not establish another completed room.
- New scenery is a removable `LEVEL6_OPENING` layer inserted before inherited mappings. Removing it recovers the exact approved 0.24.0 hires.txt hash. All 127 previous art/audio/patch files remain byte-identical.
- Brick, skull and cornice units are registered as whole native layouts before slicing. Shared cornice identities remain pixel-identical. Every structural alpha mask retains its native filled silhouette, including the rough top ridge of the opening platform.
- Native-byte identity proves reuse of accepted dragon forms/pickup/fire, the pulsing enemy, rising sentry, floating eye/tears, wing drops and Thunder. Lava and Blizzard ice retain the approved atlas cells and animation conditions. Native background 1769–1774 is lava/ice, not removable decoration.
- Complete 1700-bank rendered guards cover normal, resume, Thunder and dragon-flash palettes. Flash images retain normal RGB at alpha 176. The new layer adds no tileNearby lookups.
- Cape layout is 0955/0954 above 0952/0951, palette 0F172737, native origin (72,104). Pause and origin guards restrict the replacement to its 32×32 HD icon. The finished boot and staff remain unchanged.

## Actual emulator verification

MesenCE 2.2.1 replayed the unchanged 6,427-frame user movie at stride one against frozen 0.24.0 and the candidate. Every RAM, PPU, OAM and scroll/view sample matches, as do all APU writes and complete PCM audio. These are actual emulator screenshots, not composited gameplay mockups.

The image checks verify 5,498 panorama frames, including 47 native spell/pickup flash frames; all 216 native black frames stay black. All 659 rendered menu frames differ only inside the cape. The remaining 53 nonpanorama transition frames remain exact. Seven room/pause boundaries show the outgoing rendered image while endFrame RAM already names the next room; each is verified against the immediately previous room's complete panorama.

Complete live source matches include the cape, skull, brick, cornice, three dragon poses, sentry, floating eye and all three Thunder components. The new scenery stays visible through scrolling, Blizzard, repeated Thunder, dragon acquisition/flight and pause/resume. The full movie was captured before only the versioned README was written; every final runtime byte matches that installed capture. The edge replay uses all 134 final file hashes.

A separate 180-frame controller-only route uses the original embedded state. Randy stops at the opening platform's left edge (world X128, Y176), walks right without jumping, begins falling at frame 113 (X167, Y176), first descends at frame 117 (X170, Y177), and lands on the lower platform at frame 147. Native execution and full audio match. The complete 64×80 HD platform source matches in 139 consecutive images; its solid span stays X128–160, with the original one-pixel rough ridge. The stock-core neighbor observer reports no invalid read in either edge run or the complete baseline replay. No native state edits were used.

`python build.py` passes from a clean output directory, including every historical validator. `python scripts/verify_release.py` matches all 134 install hashes. The flat installation ZIP passes CRC and independent extracted-byte checks. Source changes contain no ROM, emulator binary, movie, save state, or raw replay dumps.

## Reproduction and evidence

Use the existing `scripts/run_mesen_movie.py`, synchronized screenshot observer, audio recorder and supported translated ROM. Run one emulator process at a time, use fresh output directories, and keep the installed pack frozen. Replay the full movie with `--stride 1`, then run:

```sh
python scripts/verify_level6_opening_replay.py --before /captures/before --after /captures/after --out /captures/replay.json
python scripts/make_level6_edge.py --movie '/inputs/Holy_Diver_HD(20261029-152041).mmo' --out /inputs/level6-edge.mmo
# Replay that generated input against both packs at stride 1.
python scripts/verify_level6_edge.py --before /captures/edge-before --after /captures/edge-after --out /captures/edge.json
python build.py
python scripts/verify_release.py
```

[Actual before/after views](../evidence/level6_opening/comparison.png) · [Actual platform traversal](../evidence/level6_opening/platform-edge.png)

See `evidence/level6_opening/replay.json`, `edge.json`, `provenance.json`, `build.json`, `build-validation.txt`, the frozen capture manifest and `evidence/0.25.0-pack-sha256.json`. The review video is the full actual movie, encoded at native NTSC frame cadence with original game audio; its initial empty screenshot is omitted.
