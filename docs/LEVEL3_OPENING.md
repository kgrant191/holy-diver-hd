# Level 3 opening — 0.11.0 review candidate

The supplied standard Mesen movie is sufficient to build several connected rooms. This candidate covers the forest approach (`10/988A`), tree climb (`04/997A`) and masonry shaft (`04/99F2`). These are the native room mode and data-pointer signatures, not guessed screenshot numbers. The subsequent corridor keeps its original scenery; shared approved actors now follow their proven native graphics copies there too. The boss is not reached.

## Artwork and registration

New built-in image-generation sources are the midnight forest panorama, broad vertical bark texture, three golden ember-creature forms and two crimson flyer forms. Exact prompts are in `art/generated/level3_prompts.json`; generated originals and measured native references are retained. Source images are registered deterministically at pack scale 2. The small ember source supplies two half-height emergence frames; these are separate native 16×8 sprites, not one 16×16 pose. The two larger forms share exact head/body pixels where their native identities repeat. Native OAM supplies mirroring, placement and animation timing.

Approved material is reused for brown ground/ledges, branches, lava and Blizzard ice, nave masonry, Randy's poses and both costumes, HUD, weapons, floating eyes/blue tears and hanging bats. Bat pose aliases follow the native sequence rather than the first matching CHR byte pattern: open and folded lower cells share native bytes but have different approved paint. CHR comparisons are recorded in `art/level3_opening/native_aliases.json`. Player pose-anchor conditions are remapped along with tile identities. New aliases follow all existing specific rules; shared Stage 2 fallbacks remain last.

Scenery replacements are limited to the three room signatures and observed palettes. Native terrain silhouettes are retained as masks; solid ground bodies are opaque. Only the measured nonsolid forest and wall identities reveal background art. The first draft mistakenly cleared some brown body cells and repeated the narrow approved tree awkwardly; neither draft is the delivered pack. The final tree uses new wide-trunk bark with the approved branches.

All 91 previous runtime files except mappings and installed README are byte-identical to approved 0.10.2. Removing the four marked Level 3 sections restores the exact prior `hires.txt` SHA-256. Two new runtime PNGs bring the installation to 95 files. No ROM edit or audio replacement is added, and the existing 56-byte entrance audio patch stays exact.

## Input and native playback

- Original movie: `Holy_Diver_HD.mmo`, 6,883 input frames, about 1m55s.
- SHA-256: `c6c3f99a7204f5052c1758ef44ffb4387d2ebc5a8534127a0ddde60ccfde74cd` (authoritative full value is also in `test_states/README.md` and validation JSON).
- Embedded starting state: SHA-256 `956c402469389e969b3443c8c5c5019458e5f1d65e8830f63f815b928a23f5f0`.
- Translated ROM SHA-1: `fe2fcd0ad334d792db16535d09f3ab9fb2bea3ac`.
- Stock MesenCE 2.2.1 native core: SHA-256 `f45cd3fd53d48176f66a1d2ff9713394e4428fae98bee53df69bed5a442e7e79`.
- Exact configuration header source: MesenCE tag `2.2.1`, commit `20ba206cef5ba207c21203176d02cb9f43dda9fb`.

`scripts/run_mesen_movie.py` plays the movie through Mesen's native movie API and adds read-only Lua observers. It never writes emulated RAM or substitutes inputs during the original replay. Each run has its own copied pack and verifies that its installation hashes stay unchanged. Keep exactly one emulator process running at a time.

The NES endFrame callback occurs before video submission. HD rendering is asynchronous, so an immediate screenshot can otherwise contain the preceding or pending image. An early paired run exposed this at the shaft exit despite identical RAM/PPU/OAM. `scripts/sync_movie_capture.cpp` waits for the pending native decoder before calling the original Lua screenshot function. It changes no pixels, input, state or audio. Acceptance evidence comes from paired replays with this observer enabled; the unsynchronized trial is not acceptance evidence.

Compile the configuration and observer against the exact source tag and the user's stock core, then invoke the runner with local paths:

```sh
c++ -shared -fPIC -std=c++17 -O2 -I"$MESEN_SOURCE/Core" -I"$MESEN_SOURCE" \
  scripts/mesen_movie_config.cpp "$MESEN_CORE" -o movie_config.so
c++ -shared -fPIC -std=c++17 -O2 -I"$MESEN_SOURCE/Core" -I"$MESEN_SOURCE" \
  scripts/record_audio.cpp scripts/sync_movie_capture.cpp -o movie_capture.so -ldl

LD_PRELOAD="$PWD/movie_capture.so:/usr/lib/x86_64-linux-gnu/libstdc++.so.6" \
HOLY_DIVER_MESEN_CORE="$MESEN_CORE" HOLY_DIVER_AUDIO_CAPTURE="$CAPTURE_OUT/full.wav" \
timeout 240s python scripts/run_mesen_movie.py \
  --core "$MESEN_CORE" --config "$PWD/movie_config.so" --database "$MESEN_DATABASE" \
  --rom "$ROM_PATH" --movie "$MOVIE_PATH" --pack "$PACK_PATH" --out "$CAPTURE_OUT" --stride 4

python scripts/verify_level3_movie.py --before "$BASELINE_CAPTURE" \
  --after "$CANDIDATE_CAPTURE" --detail-before "$BASELINE_DETAIL" \
  --detail-after "$CANDIDATE_DETAIL" --out evidence/level3_opening/validation.json
```

For the detail pair, replay the same complete movie with `--stride 1 --capture-start 3148 --capture-end 3172`. The native bat alternates open and folded wings on consecutive frames; a four-frame sampling interval misses the open-wing pictures. This 25-frame paired window verifies both complete poses without changing input.

Run baseline and candidate sequentially in fresh output directories. The helper's private C++ ABI bindings are pinned to this exact Linux 2.2.1 core; they are not a general emulator-version compatibility promise. The installable HD pack itself does not include or require this observer.

## Coverage and limits

The paired full movie checks native RAM, PPU, OAM and scroll metadata every fourth frame, every recorded APU write and continuous PCM. Actual image checks cover full new enemy sprites, native mirrors, returning enemies, native black transitions, the final pause menu and unchanged later-room scenery outside the shared sprite footprints. Exact counts and examples are in `evidence/level3_opening/validation.json`.

`make_level3_edge_movies.py` derives additional left-boundary and slow ledge walk-off input routes from the original movie. It keeps the embedded state and game settings byte-identical; only controller rows change. Their native trajectories and paired results are recorded separately.

The recorded route traverses all three target rooms and enters the following corridor. This is not the whole level, a boss test, or exhaustive validation of every possible encounter/palette. Earlier levels are protected by exact prior mapping recovery and unchanged assets; they are not replayed afresh for this feature. Approval, source push, PR/Actions and merge remain separate steps. No release/tag is requested.

Remaining native artwork in the opening: the red spinning creature (068A–06AF family) and unmapped effects. This batch replaces the three rooms of scenery, selected new creatures and proven shared actors; it does not complete every Level 3 sprite. The existing recording covers this remaining work and the following corridor.

Measured acceptance: 6,883 original input frames, 1,721 paired RAM/PPU/OAM/view samples per type, 15,528 identical APU writes and 21,995,512 identical PCM bytes. The 25-frame bat window adds eight complete open-wing matches. Both controller-derived edge routes pass: left stop at X23/Y176, and no-jump walk-off from X448/Y112 to X480/Y128. See `edge_checks.png`, `comparison.png` and the two JSON reports.
