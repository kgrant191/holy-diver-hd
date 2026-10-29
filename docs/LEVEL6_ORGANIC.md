# Level 6 crimson organic hall — 0.29.0

The user accepted 0.28.0 and supplied `Holy_Diver_HD(20261029-215619).mmo`, SHA-256 `30efe77656e6b464c92d1dd7f9dda448f1eb69ccc96bac1710a2ad7fa7e2d067`. Its 4,761 controller frames cover the accepted A2FB shaft exit, the complete recorded A3AF/mode10 organic hall, pause transitions, Overdrive and Blizzard. It ends paused in A3AF; later rooms and the boss are outside this update. Main remains approved 0.24.0. No push, PR, merge, tag or release was performed.

The original hall uses coral-red organic structure (`0F162638`), dark brown wall relief (`0F070010`), animated red lava (`0F060616`/`0F161606`) and Blizzard ice (`0F122131`). The new background is a dark burgundy ribbed cathedral. Lighter red chitin plates define solid foreground, retaining every native hull. This keeps the room visibly different from the green reliquary and shaft.

Body, ceiling, platform top and the tall wall-mounted face are registered as complete native groups before slicing. Repeated native identities share identical cells. Both 32×32 HD green orb poses retain their original four-cell OAM arrangement and native animation cadence. The new foreground atlas is index 67; three install PNGs are added.

Sprite bank 1A reuses all 450 ordered player/HUD/effect aliases from the accepted sources. Pose-specific rules retain their conditions and remapped sprite-neighbor identities. The six 1-up aliases, twelve Thunder cells and wall projectile also reuse completed art. The six lava cells exactly match the accepted Stage 2 patterns; their 54 palette/animation aliases retain native cadence. No new tileNearby conditions, gameplay, palette-RAM or audio edits are introduced.

Only A3AF/mode10 is targeted. All 146 previous art/audio/patch assets stay byte-identical. Removing the three LEVEL6_ORGANIC blocks recovers exact accepted 0.28.0 hires.txt. The historical validator chain runs through the exact baseline projection. Normal, resume and 30/31 backdrop guard families cover bank1B; all-black palettes remain inactive.

Sources and exact built-in image-generation prompts are in `art/generated/level6_organic_*.png` and `level6_organic_prompts.json`; whole registrations and the movie inventory are in `art/level6_organic/`. Build using `python build.py`, then `python scripts/verify_release.py`.

The full new movie is paired against frozen 0.28.0 at stride one. The previous 7,648-frame movie is the exact-image regression. A controller-only branch preserves the new movie's first 548 inputs and save state, stops near the left platform edge, then walks right slowly. Native RAM/PPU/OAM/view/APU and full PCM are compared for each route. The recording contains no Thunder or dragon cast in this room; those flash families have static rule coverage only.

## Completed validation

- The earlier 7,648-frame replay preserves all native state and complete audio. All 7,647 nonempty rendered frames are identical to accepted 0.28.0.
- All 4,761 new-movie native RAM/PPU/OAM/view samples, APU writes and complete PCM audio match accepted 0.28.0 exactly. All 955 recognized menu images and 115 black images remain exact. The 3,548 changed scenery frames retain at least 115,044 exact panorama pixels each, with no background dropout.
- All six whole new sources (body, ceiling, platform top, wall face and both orbs) match actual rendered pixels. Separate source checks match both accepted lava phases, Blizzard ice and the wall projectile.
- The 731-frame controller-only edge route preserves all native state and audio. Randy stops at world (794,80), immediately inside the left support limit. The original right walk-off begins at frame 636 at (839,80), with first descent at frame 640 at (842,81). The complete 64×288 HD pillar matches its source in all 75 inspected frames. Its native bounds remain x800–831, top y96; sprite overhang is unchanged.
- An isolated clean build passes the historical validator chain and all 151 installation hashes. The flat ZIP passes CRC and full manifest verification. The actual 4,760-frame preview includes original audio and passes a complete decode.

Compact machine-readable results, actual room captures and the build log are in `evidence/level6_organic/`.
