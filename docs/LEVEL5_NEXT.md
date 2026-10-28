# Demonic Palace next rooms — 0.22.0 review

The user accepted the 0.21.1 artwork and supplied a new movie showing further background dropouts and the next two rooms. This update continues `feature/demonic-palace`. Main remains approved 0.20.5; no publication or merge is authorized.

## Changes

The 888E/mode10 dragon stair hall previously had only entrance background guards. The new camera positions move different native tiles through that guard, disabling the panorama. Complete normal-palette guard families now cover both 1100/1300 CHR bank copies throughout this hall and the two following rooms, 897E/mode10 and 8A6E/mode08. Exact room and rendered-palette conditions preserve native all-black transitions and pickup flashes. The same completed panorama and its placement are reused.

Both new rooms use the completed stair stone, native structural outlines and approved animated lava/frozen lava. Only the nonsolid distant wall palette is cleared to reveal the panorama. Native collision, lava hazards, freeze/thaw timing and camera behavior are unchanged.

The new sprite bank is 1200. Complete pose-conditioned player/HUD/effect aliases carry their exact native neighbor identities and retain conditional priority; broad fallbacks remain last. The walking dragon reuses the complete Level 2 poses, the floating horned guardian and curved shot reuse their finished sources, and pickups, small drops, transformation stars and Thunder reuse existing artwork. Native bytes prove each bank alias. These are registration changes, not new enemy designs.

The rising armored sentry (12B1–12C2, FF0C1C30) is the one new painted character. Its complete 64×112 source is registered in horizontal bands before slicing. Native BE/BF lower-body repetitions are byte-identical, all opaque source pixels stay within the native sprite-cell union, and OAM controls emergence, height, movement and mirroring. The built-in image-generation prompt is saved beside `art/generated/palace_sentry.png`; the registration and native inventory are in `art/level5_next/`.

## Preservation and validation

All 121 prior art/audio/patch files remain byte-exact. The only changed installation files are hires.txt and README.txt, plus the new Demonic_Palace_Next_2x.png atlas. Removing the four PALACE_NEXT blocks recovers exact 0.21.1 mappings. The validation chain reconstructs and hashes that complete baseline and runs every historical validator. No new neighbor probe, RAM write, controller change or audio replacement is introduced.

The supplied 10,206-frame movie is replayed before and after in the same MesenCE 2.2.1 native core, with unmodified starting state and inputs. The paired checks compare RAM, PPU, OAM, scroll state, APU writes and full PCM; inspect panorama presence and native blackouts; and locate complete new/returning sources in actual gameplay. Detailed results are in `evidence/level5_next/movie_validation.json`. The preview uses actual captures and native audio from this run.

The new movie includes both lava rooms, Blizzard, Overdrive, death and restart. It ends in 8A6E and does not show later Level 5 rooms or the boss. It also contains Thunder casts in the preceding dragon stair hall; the 0.22.0 review missed their flash-palette scenery fallback. That defect and consecutive-frame verification are documented in LEVEL5_FLASH.md.

## Reproduce

```sh
python3 build.py
python3 scripts/verify_release.py
python3 scripts/verify_palace_next_replay.py --before BEFORE --after AFTER --out movie_validation.json
python3 scripts/export_palace_next_preview.py --capture AFTER --out preview.mp4
```

Use the existing native `run_mesen_movie.py` runner with stride 2. Before/after installations must match the frozen complete manifests. ROM, movies, save states and emulator binaries are local test inputs and excluded from the handoff. The source handoff contains all unpushed Demonic Palace commits after the approved main prerequisite.

## Verified result

- All 5,103 synchronized native samples per RAM/PPU/OAM/view type, APU writes and full PCM match.
- All 174 native blackouts and 762 stable menu/lives-card images remain exact. Native sprite-only death/restart screens retain their black fields; the measured grayscale/blue-emphasis flashes match the native renderer formula.
- The panorama is verified throughout normal recorded gameplay in all three rooms; exact per-room counts and minimum source-pixel matches are recorded in movie_validation.json. Native disabled-background death frames are excluded from panorama claims.
- Complete walking-dragon poses match at frames 1988/1996, the sentry at 2552 and the floating guardian at 5500.
- A clean build and all historical/new validators pass. All 124 ZIP members match their complete manifest and the actual replay installation; CRCs and flat install layout pass. The 45.67-second preview decodes cleanly.
