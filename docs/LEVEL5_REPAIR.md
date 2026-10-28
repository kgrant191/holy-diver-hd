# Demonic Palace ceiling and climb repair — 0.21.1 review

The user requested a subdued green slime ceiling distinct from the rocky floor, and supplied a movie showing scenery disappearing during the stair climb and a serpent reverting to native artwork. This patch continues the unapproved 0.21.0 review branch. Main remains approved 0.20.5.

## Changes

- The cavern ceiling families 1101–1104 and 111D–1120, including exact 1300-bank copies, use a muted green slime source. A whole 32×32 material is registered to each native two-by-two group. All 48 original alpha masks, conditions and priority ordering are retained. The rocky floor and its standing edges are untouched.
- The 8816 stair-hall backdrop previously recognized only its entrance guard, 11AC/0F001030 at (128,16). The new movie proves seven more guards during ascent. Both physical CHR banks use the existing interior panorama and original rendering parameters.
- The serpent head 10DB–10E3 and body 10E4–10E7 use FF110130 in this room. Thirteen scoped aliases reuse the exact finished green/ivory serpent source. Native independent segments, OAM flips, movement and timing are retained.
- Restored scenery exposed black stair patches. The old tread registration had included transparent padding, then made that padding opaque with the native geometry mask. Fill only those padding pixels using the same source's opaque stone face. All 50 existing stair masks and their already-opaque tread RGB remain exact.
- The movie ends at room 888E/mode10. Its visible entrance uses the same completed stonework and interior panorama. The rest of that room and later Level 5 remain untested.

The new source is `art/generated/palace_slime.png`; its exact built-in image-generation prompt is retained beside it. Deterministic registration, visible native inventories and mapping provenance live in `art/level5_repair/`. No RAM, collision, timing, input or audio is edited.

## Preservation and checks

All 120 previous image/audio/patch files remain byte-exact. The only changed installation files are hires.txt and README.txt, plus one new atlas, Demonic_Palace_Repair_2x.png. Removing the three PALACE_REPAIR blocks recovers exact 0.21.0 mappings. The validator reconstructs and hashes the full 122-file baseline, then runs its complete validation chain, including every older validator. No new neighbor probe is introduced.

Actual paired replays cover the supplied climb and the complete preceding opening movie. Native state, audio, full-image scope checks, continuous visible scenery, whole serpent source matches, and unchanged ceiling/stair masks are recorded in `evidence/level5_repair/`. Native room-transition blackouts remain native blackouts.

## Reproduce

```sh
python3 build.py
python3 scripts/verify_release.py
python3 scripts/verify_palace_repair_replay.py --before BEFORE_CLIMB --after AFTER_CLIMB --out climb.json
python3 scripts/verify_palace_repair_replay.py --before BEFORE_OPENING --after AFTER_OPENING --out opening.json --opening
```

Use the existing run_mesen_movie.py native runner with capture stride 2. Both before/after versions must match their frozen complete manifests. Input files, ROM and emulator are local testing inputs, excluded from Git and deliverables.

## Verified result

- New 1,215-frame movie: all 607 synchronized RAM/PPU/OAM/view samples, APU writes and full PCM match 0.21.0. The panorama is visible in all 605 nonblack samples, with at least 140,784 exact source pixels each. Both native blackout samples remain exact. Complete head and segment sources match the actual moving serpent.
- Previous 9,921-frame opening movie: all 4,960 native samples and full audio match. Every changed cavern pixel lies in the ceiling families, preserving the entire floor and other foreground. Unrelated rooms and menus remain exact; the first stair-hall entry includes the intended padding repair. Native blackouts remain exact.
- Clean build, complete historical/new validation, source alpha/RGB preservation, archive CRC and all 123 file hashes pass. The preview contains 30.2 seconds of actual final Mesen captures with native audio.
