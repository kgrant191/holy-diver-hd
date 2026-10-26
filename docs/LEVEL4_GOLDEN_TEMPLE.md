# Golden Temple — 0.16.0 review

The supplied Level 4 recording opens outdoors in room A865, then enters the temple in AA09 and continues through the recorded portion of AA81. This candidate gives that approach an open twilight sky and distant golden temple, then switches to enclosed navy masonry and gold arches. Native collision tiles retain bright, readable gold stone. Columns, the doorway, stairs, rolling boulders, flying gargoyles and horned guardians now follow the same direction.

The Start/pause menu now reads OVERDRIVE. The two V cells replace the incorrect Y glyphs; the O uses a whole-cell origin condition so MP digits remain intact. All three complete glyphs are checked against the atlas in actual pause images. The actual Overdrive cast is the orbiting four-cell orb **0A8A–0A8D**, now cobalt/ivory with gold trim. Select enables the selected magic, and the controlled B press spends the native 16 MP. This differs from the acquisition orb 088B–088E completed in 0.15.0. The narrow CB–CF crescent belongs to the flying gargoyle attack and has a separate ivory/gold wave treatment.

## Implementation

`scripts/build_level4.py` adds one 512×512 atlas and two 768×480 panoramas. The new marked block precedes existing mappings, because Mesen uses the first matching replacement. Scenery is restricted to measured RAM mode/room pairs: 1C/A865, 08/AA09 and 08/AA81. Rendered-tile guards prevent scenery from appearing over menus, cards and blank transitions. The indoor guard includes palette 0F071723, used at frame 6500.

Gold terrain follows native cell positions and stepped silhouettes. Full masonry faces are opaque; mortar is a recess rather than a transparent crack. Column shafts remain continuous. Whole gargoyle and guardian silhouettes fit their native OAM unions with zero clipped pixels. Gargoyle wing animation shares its head/body pixels. Native flips, priority, timing, destruction and collisions remain in control.

Finished bats and existing projectile materials are reused where CHR bytes prove identity. The Overdrive cast has ten byte-identical bank copies, recorded in `art/level4/overdrive_aliases.json`. Those aliases reuse one orb source; later banks have static identity verification, not fresh live level coverage.

All 104 previous art/audio files, including the 56-byte entrance IPS, remain exact. Only hires.txt and the installed README change among the 106 approved files; three new images bring the candidate to 109 files. Removing the marked Golden Temple blocks recovers exact approved 0.15.0 hires.txt. The validator retains all prior historical checks.

## Live verification

Use the stock MesenCE 2.2.1 native core and the synchronized screenshot observer in `run_mesen_movie.py`. Replay the original movie against exact approved 0.15.0 and this final 0.16.0 pack. The supplied movie has 8,668 frames; full paired captures use stride four. Controlled Overdrive and platform routes change only Input.txt and retain the movie's exact embedded starting state. No RAM writes, ROM edits or fabricated screenshots are used.

```
python scripts/make_level4_routes.py USER_MOVIE.mmo work/routes
python scripts/verify_level4.py --before BASELINE_CAPTURE --after CANDIDATE_CAPTURE --out evidence/level4/movie.json
python scripts/verify_level4_scenery.py --capture CANDIDATE_CAPTURE --out evidence/level4/scenery.json
python build.py
python scripts/verify_release.py
```

The movie check compares every captured RAM, PPU, OAM and PPU-view byte, all APU writes and full PCM. Actual rendered menu changes are confined to the Overdrive letters. One endFrame sample advances to pause RAM before submitting its final gameplay image; the verifier explicitly requires the preceding sample to belong to the temple. Native sprites can briefly overlap the first pause image; glyph checks exclude only measured native OAM occlusion and require complete unoccluded O/V matches elsewhere. Native blackouts and cards remain exact. Full painted sprite matches cover all three boulder poses, both gargoyle poses/directions, guardians in both directions and Overdrive's native mirrors. The three paired runs cover 10,639 emulated frames per build and 4,139 captured native samples per type with exact full audio. The platform test stops at world anchor X499/Y160, traverses the top, remains grounded through X553, then begins falling at X554/Y161. See the precise counts in `evidence/level4/{movie,overdrive,edge,scenery,validation}.json`.

The preview is a silent 24-second side-by-side comparison made from actual unretouched Mesen pictures. Labels sit outside the game image. Its source frame ranges and playback rate are in `preview.json`.

## Scope and handoff

This is a review candidate on `feature/golden-temple`, based on approved main `2f38abeb06cd1093fc33416da20c5124fca2f4d7`. It covers the outdoor approach, first indoor room and the second indoor section reached by the supplied recording, including death/card return. Later temple areas and its boss are not covered. Earlier stages are preserved by hashes and recovered mappings; they were not all replayed for this scenery change. Stage cards 1–4 retain established live coverage; 5–6 remain unverified.

The downloadable install ZIP is flat: one extraction exposes hires.txt and all 109 files. The separate source handoff wraps an incremental Git bundle and exact non-force fetch/push instructions. No ROM, movie, emulator, raw captures or credentials are included. No source push, PR, merge, release or tag is implied; main stays at approved 0.15.0 pending review.

Source art and brief summaries: `art/generated/level4_provenance.json`. Native references, layouts, pattern proofs and registered sprites: `art/level4/`. Artwork was created with the built-in image generation tool and registered reproducibly by the builder.
