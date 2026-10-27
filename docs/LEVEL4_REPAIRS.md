# Golden Temple entry and pickup repair — 0.16.2

The user reported original item drops outdoors and a Mesen crash on entering
the temple with 0.16.1. This patch changes only hires.txt and the installed
README. All 108 other assets remain byte-identical. The backgrounds, masonry,
pillars, actors, Overdrive and menu art are preserved.

## Crash diagnosis

Stock MesenCE 2.2.1's `HdPackTileNearbyCondition::InternalCheckCondition`
checks `pixelIndex > ScreenPixelCount`, but the screen array has only
`ScreenPixelCount` elements. Index61440 therefore passes despite being one
past the 256×240 allocation. A pillar query two rows below (0,224), or one row
below (0,232), reaches that invalid index.

`check_hd_neighbor_bounds.cpp` observes original stock condition calls and
aborts before this invalid access. The unchanged user recording with 0.16.1
reaches it at replay frame4046 / native frame120343 as the indoor room appears:
`!masonryAA090B780F172737below2`, tile0B78, x=0/y=224, dy=16.
See `evidence/level4_repairs/crash_diagnosis.json`.

This establishes an actual invalid read at the reported transition. It is
not the user's platform crash log. Reading outside an allocation can also
appear to work, which explains why the earlier uninstrumented replay missed
the defect.

## Pack-side fix

`build_level4_repairs.py` follows the unchanged 0.16.1 builders. It rewrites
88 column rules so screen-position checks short-circuit before every neighbor
lookup. Explicit off-screen alternatives retain the intended no-neighbor
behavior for inverted checks, preserving cap/base rendering. No emulator
update or binary patch is required. The observer never ships in the install.

`verify_temple_neighbor_rules.py` checks all 240 screen rows and every relevant
neighbor truth assignment: 63,360 cases, 121,088 valid neighbor evaluations,
zero out-of-range evaluations. All offsets have dx=0, so this covers every x.
The static validator runs this regression and reverses the patch to recover
byte-exact 0.16.1 hires.txt before retaining every earlier validation.

## Item reuse

Small health (0A47) and magic (0A48) lacked Level 4 mappings. Both patterns
have sixteen byte-identical CHR copies. Existing Stage 2 heart/crystal cells
from atlas25 are reused exactly. Twenty-eight missing unconditional aliases
are appended after earlier specific/pause rules, which keep priority.
Large flasks already have matching mappings. No new artwork is generated.

`art/level4_repairs/pickup_patterns.json` records all 32 native tile patterns.
Validation requires each mapping to retain the identical source pattern,
palette, atlas cell and brightness.

## Verification

The full unchanged 8,668-frame user recording completes with the bounds
observer active, including both recorded indoor sections. All 2,168 sampled
RAM/PPU/OAM/PPU-view states match retained 0.16.1. Complete PCM (27,698,116
bytes) and all APU writes match. Of 2,168 images, 1,780 are identical and 388
change only within small-pickup footprints. Forty black frames remain exact.
All 92 complete heart/crystal source matches pass.

endFrame OAM can be three native pixels ahead of a falling/spawning drop's
submitted picture. The checker uses adjacent captures and the measured
six-HD-pixel margin (maximum at frame3436). Source matches are checked
independently. Exact results: `evidence/level4_repairs/movie.json`.

```sh
python build.py
python scripts/verify_release.py
python scripts/verify_temple_neighbor_rules.py
python scripts/verify_level4_repairs.py --before BEFORE --after AFTER --out evidence/level4_repairs/movie.json
```

Build the diagnostic against the pinned core headers with
`g++ -std=c++17 -shared -fPIC -O2`, the source/Core/Utilities include paths and
`-ldl`. Preload it before the existing screenshot/audio observer, with
`HOLY_DIVER_MESEN_CORE` pointing to the stock core. It forwards every valid
call unchanged and aborts only before index61440. No game memory or input is
edited. The source observer depends on the pinned Linux C++ ABI; it is test
tooling, not an emulator patch or install requirement.

The 15-second silent preview contains unretouched native 2× Mesen captures:
outdoor drops followed by the approach, transition and inside the temple.
Captions are outside the game image. All 110 install files stay at the ZIP
root. Fully close Mesen before replacing/reloading the pack.

0.16.2 remains a review candidate on feature/golden-temple; main is approved
0.15.0. No push, PR, merge, tag or release is implied. Later unrecorded temple
rooms and the boss remain outside this repair's runtime coverage.
