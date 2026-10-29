# Level 6 room variety and enemy hit frames — 0.27.0

Review candidate on `feature/level6-opening`, continuing 0.26.0. Approved main remains 0.24.0; nothing has been pushed, merged or released.

The user reported native enemy graphics when shooting and asked for different room designs following the original color schemes. This supersedes the initial uniform cold-stone direction. All new scenery comes from new generated sources; no old red cave panorama is reused.

| Room | Original palette | Updated design |
| --- | --- | --- |
| 9A8B / 04 | Red stone | Red masonry with the separate ruined exterior |
| 9BB7 / 10 | Red stone | Red masonry with the enclosed Gothic hall |
| 9CA7 / 0C | Outgoing opening transition | Red masonry, retained exterior |
| 9F3B / 10 | Warm orange `0F162738` | Amber masonry and ossuary corridor |
| A02B / 04 | Red `0F061636` | Crimson stone and vertical fortress shaft |
| A0DF / 14 | Green `0F0B1B3B`, blue `0F011121` | Green stone, blue-accented verdant crypt |

The cape, 1-up, ivory skull blocks and carved ornaments keep their finished sources. Foreground stone is registered in complete native groups before slicing. Every native hull remains exact, including ceiling outlines and platform edges. Only the green room's measured blue decorative wall layer is cleared to its panorama. Both identical background-bank copies, normal/resume and 30/31 phases are covered. Flash backgrounds retain RGB with alpha 176.

Sentinel identities 18A9–18DD are byte-identical to 0CBE–0CF2. Both missing hit palettes (`FF102030` and `FF122232`) now reuse the complete four-pose atlas-51 art. The normal silver palette remains intact. The one-cell shot follows its owner's hit palettes; 18DE reuses the byte-identical finished spark. A0DF inherits the finished player/HUD, sentinel, skull, projectile, Thunder and crawler sources, with specific pose conditions preserved.

The new layer is removable. Reversing the two scoped panorama substitutions and removing its three blocks recovers exact 0.26.0 mapping bytes. All 134 earlier art/audio/patch files remain unchanged; seven install images are added. No new tile-neighbor probes, native state edits, gameplay changes or audio changes are introduced.

Validation records are in `evidence/level6_variety/`. The 3,393-frame user movie covers the full vertical climb and green-room combat, pause/resume, Overdrive, death and Stage 6 card transition. The earlier 6,427-frame movie checks the opening scenery, cape, 1-up, native spell flashes and transitions. The controller-only corridor edge route checks the full platform span, far-left stop and slow right walk-off. Native execution and full audio are compared at every captured frame. New-room Thunder/dragon flashes are covered by complete static rules; this movie does not cast them. Later unrecorded rooms and the final boss remain unfinished.

Six generated source PNGs and their exact prompts are under `art/generated/level6_*`; normalized materials, whole terrain registrations and mapping provenance are under `art/level6_variety/`. Build with `python build.py`; verify with `python scripts/verify_release.py`. The build invokes the complete historical validator chain through exact baseline projections.

## Recorded results

- Full new movie: 3,393 paired native samples; RAM, PPU, OAM, view state, APU writes and full PCM are exact. 3,125 images change; 267 remain identical. All 55 recognized menu images and 12 native black frames stay exact. No missing new-room panoramas.
- Native hit phases occur on 189 silver and 75 blue samples. Whole finished sentinel sources match actual combat in both horizontal directions for both colors. Blue poses 0 and 3 are fully mapped but are not seen as complete unoccluded units in this route.
- All six inspected whole terrain units and both crawler poses match live source pixels. The new source masks retain 10,170 structural-rule masks; 222 registered whole-terrain cells are checked across the three colors.
- The controller edge route preserves all 367 captured native samples and full audio. The 288×160 HD corridor platform matches in 151 frames; the left stop stays at world (527,144), native falling begins at (680,144), and first descent occurs at (684,145).
- An isolated build passes the full historical validator chain. All 143 install files match the frozen manifest. The ZIP is flat, with all CRCs and contained file hashes checked. The 3,392-frame actual-gameplay preview decodes in full and retains the game audio.

- Opening regression: 6,427 paired native samples and full audio match exactly. The 2,432 changed images contain the red generic-stone update; 3,994 images remain identical. All 659 recognized menus and 216 black frames remain exact. Whole cape, ivory/blue 1-ups, skull, brick and cornice sources match live pixels. Background pixels remain exact in all 2,417 changed normal frames and 15 changed phase-31 flash frames. The recorded hall is dominated by retained carved ornaments, so its images remain unchanged; generic stone in its scope is mapped to red for consistency.

One opening replay attempt stalled during emulator initialization before any frame was captured. The completed fresh replay above supplies all regression evidence; no result from the stalled attempt is counted.
