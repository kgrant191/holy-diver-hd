# Level 6 ceiling and 1-up — 0.25.1 review

The red strip revealed by jumping immediately was accidental: ceiling identities 17B4–17B7 still used inherited red rock. The repair registers their whole 2×2 group from the existing cool stone material, retaining every native silhouette. The Level 6 164E/164F 1-up now reuses the complete approved ivory/blue figurines, including the ivory form during the native green dragon palette.

Work continues locally on `feature/level6-opening` from 0.25.0 commit `7ab20003fb555d6f8a9ea3a46fa4c50881bd093d`. Approved main remains 0.24.0. This candidate has not been pushed, merged or released. Later Level 6 rooms and the boss remain unfinished.

## Scope and preservation

The removable LEVEL6_REPAIR layer contains 72 room/palette ceiling mappings, nine room constants and six exact 1-up aliases. It adds one 32×32 atlas; no newly generated art or panorama is needed. All 132 prior art/audio/patch files remain byte-identical, including both citadel backgrounds and the cape. Removing the new sections recovers exact 0.25.0 hires.txt. The existing normal/resume/30/31 guard conventions remain intact; no new neighbor lookups or native state/audio changes are introduced.

The upper ceiling source is `art/level6_opening/rock_material.png`, crop (0,16)–(32,48), registered to 17B4/17B5 above 17B6/17B7. The sprite aliases prove native-byte identity to 024E/024F and preserve the accepted atlas 29 pixels, masks and brightness.

## Actual paired replay results

The supplied 20261029-173117 movie runs for 1,147 consecutive frames in stock MesenCE 2.2.1. RAM, PPU, OAM, scroll/view, APU writes and complete PCM audio match 0.25.0 exactly. Only 313 images change: 63 ceiling frames and 250 1-up frames. All 834 others stay identical. Every changed ceiling pixel equals the existing stone source and stays within the newly exposed native tile bounds; all 250 item frames match the complete accepted figurine. The native life counter increases from 2 to 3 at frame 858.

The original 6,427-frame Level 6 movie also passes the same native/audio checks. It contains three 1-up palettes that the initial review missed: FF300036, FF190927 and FF221136. The repair changes only those item footprints in 1,266 images; all 5,161 others remain exact, preserving the scenery, platforms, cape and spell effects. Fourteen overlap frames are checked using the unchanged HUD cells, actual OAM priority and Mesen's exact alpha-blending arithmetic. This verifies the figurine beneath the HUD's soft edges without treating those blended pixels as a HUD change. Native life gains at frames 2313 and 6029 remain unchanged.

The stock-core neighbor observer was active in the new-movie pair and original-movie candidate replay, with no invalid-read abort. Normal upper-ceiling and all three item palettes have actual replay coverage. Resume/Thunder/dragon-flash upper-ceiling aliases have source/rule verification; the recordings do not cast those spells at the upper ceiling.

## Build and delivery

An isolated clean `python build.py` and `python scripts/verify_release.py` pass, including every historical validator and all 135 expected installation hashes. The flat ZIP independently passes CRC and extracted-byte checks. Builder steps now publish complete PNG and Path outputs atomically: intermediate builds exposed short PNG files and partial reads on this host. This I/O wrapper preserves every expected image and mapping byte; it does not alter artwork generation or gameplay.

The short review video is the complete new recording at native NTSC frame cadence with original game audio, omitting only the empty initial screenshot. No ROM, emulator, save state, movie input or raw capture dump is shipped in source.

## Reproduction

Replay each movie against frozen 0.25.0 and final 0.25.1 with `run_mesen_movie.py --stride 1`, fresh output directories and the existing synchronized capture/audio observers. Run only one emulator at a time; freeze its installed pack. Then run:

```sh
python scripts/verify_level6_repair_replay.py --before /captures/new-before --after /captures/new-after --out /captures/new-check.json
python scripts/verify_level6_repair_replay.py --before /captures/original-before --after /captures/original-after --out /captures/regression.json --regression
python build.py
python scripts/verify_release.py
```

The original 0.25.0 capture predates only its versioned README; the regression permits that documented note difference while requiring every runtime byte to match. The new-movie pair uses exact complete manifests.

[Actual before/after comparison](../evidence/level6_repair/comparison.png). See `evidence/level6_repair/replay.json`, `regression.json`, `provenance.json`, `build.json`, `build-validation.txt` and both capture manifests. Frozen expected installation files are in `evidence/0.25.1-pack-sha256.json`.
