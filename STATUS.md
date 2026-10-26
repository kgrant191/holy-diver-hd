# Current status

## Golden Temple continuation — 0.17.0 review

Work is on feature/golden-temple-courtyard from approved 0.16.3. The next hall AAF9 uses the enclosed interior; AB71 uses the exterior; the recorded AC61 re-entry returns indoors. The wings pickup and eight-orb fire chain have new art. All earlier assets remain exact. Main is still approved 0.15.0. No push, PR, merge or release is requested. Paired checks pass 13,054 frames per build, 4,361 native samples per type, exact full PCM/APU and all 2,168 earlier screenshots. Both candidate replays complete with the crash detector enabled. All 112 install hashes and flat ZIP checks pass. See docs/LEVEL4_COURTYARD.md and evidence/level4_courtyard/.

## Approved Golden Temple continuation — 0.16.3

The user accepted 0.16.3 on 2026-10-26 ("ok good") and requested the next rooms, wings item and new outdoor enemy. All 111 reviewed installation bytes remain frozen. Main stays 0.15.0; publication/merge is not requested. See evidence/level4_stairs/approval.json.

## Current Golden Temple stair repair — 0.16.3

The user's new save identifies a missing descending stair flight in AA09. Native 0B7C–0B7F were wrongly cleared as scenery. Scoped overrides now restore them with existing gold stone and a joined native silhouette. All 108 prior assets and the 0.16.2 crash/pickup fixes stay exact. Controller-only walk/jump routes and the full recording are paired against 0.16.2; see docs/LEVEL4_STAIRS.md and evidence/level4_stairs/ for accepted results. The 111-file candidate awaits review on feature/golden-temple; main remains approved 0.15.0.

## Current Golden Temple repair — 0.16.2

The user found old small drops outdoors and a crash entering the temple. A diagnostic replay catches a one-past-screen read in the pillar checks at frame4046. Position guards now prevent it while preserving column rendering. Small health/magic drops reuse the existing heart/crystal cells through proven shared-bank mappings. All 108 prior assets stay exact. The full 8,668-frame movie completes with the invalid-read observer active; all 2,168 native samples per type and full audio match. Only small-pickup pixels change; all 92 complete source matches pass. See docs/LEVEL4_REPAIRS.md and evidence/level4_repairs/. Candidate remains on feature/golden-temple; main is approved 0.15.0.

## Current Golden Temple review — 0.16.1

The user accepted the backgrounds and outdoor columns, requested distinct breakable blocks, and rejected the flat square masonry and indoor block-stack supports. New worn horizontal sandstone, darker cracked breakable faces, and carved indoor columns address that feedback. All 107 prior art/audio files remain exact. Paired checks pass 3,653 native samples per type across 10,153 frames per build, with exact full PCM/APU and foreground-only changes. All 110 install hashes and flat-layout/CRC checks pass. The 110-file candidate awaits review on feature/golden-temple; main remains approved 0.15.0. See docs/LEVEL4_MASONRY.md and evidence/level4_masonry/.

## Golden Temple review — 0.16.0

The outdoor approach and both indoor sections reached by the supplied recording now have distinct Golden Temple scenery. OVERDRIVE is spelled correctly in the Start menu and casts new cobalt/ivory orbiting orbs. New temple actors retain native footprints, animation and behavior; proven returning actors reuse approved art. All 104 previous art/audio files remain exact. The 109-file install is a review candidate, based on approved main 0.15.0. No push, PR, merge, tag or release has occurred. Paired tests pass 4,139 native samples per type across 10,639 frames per build, with exact full PCM/APU. The archive passes all 109 hashes and flat-layout/CRC checks. See docs/LEVEL4_GOLDEN_TEMPLE.md and evidence/level4/.

Later unrecorded temple areas and its boss remain unfinished. Review this candidate before adoption. Historical entries below retain their original delivery/approval status.

## Approved baseline — 0.15.0, main

The user approved the completed Level 3 pack and authorized all five PRs and merges on 2026-10-26. PRs #13 → #14 → #15 → #16 → #17 are merged into main in dependency order, with each successor retargeted to main. Every merge tree matches its reviewed branch head. All five PR builds and all five main merge builds passed; all ten downloaded artifacts match their complete expected manifests, archive digests, CRCs and flat install layouts. The final pack retains all 106 reviewed installation bytes, including historical README wording. See evidence/stage3_adoption/ and evidence/level3_finale/approval.json.

Main now includes the Level 3 opening/detail fixes, lava/Breaker work, independent multi-fish stabilization, green Poison Moss Land scenery, final climb, boss and Overdrive sequence. Live review evidence includes 3,902 paired native samples/type with exact full audio, 167 actor-source matches, 40 scenery reconstructions, all four defeat-flash colors and all three observed normal-costume pickup fades. The approved cumulative baseline is 0.15.0; historical review entries below describe their original delivery state.

Next: Level 4 / Golden Temple, from a focused branch based on main. Its title card and recorded initial arrival are covered; later scenery and encounters remain unfinished. No release tag or GitHub Release was requested or created.

Updated: 2026-10-26 (America/New_York).

## Approved continuation — 0.14.0, feature/poison-moss-land

The user requested a greener Poison Moss Land instead of reused caves and rocks. New painted forest and overgrown Gothic ruin panoramas, with green mossy masonry, cover all eight completed/recorded Level 3 rooms. Existing wood, all terrain alpha contours, actors, independent fish hover stabilization, lava/ice, collision and sound are preserved. Later portions of the descent and the boss remain unfinished.

This candidate adds three runtime images and changes only hires.txt and installed README among the previous 101 files. All 99 previous art/audio files remain exact. The user approved the delivered 104-file pack on 2026-10-26. All reviewed installation bytes, including the historical review label in README.txt, remain frozen. This is the new continuation baseline; main remains approved 0.10.2 pending publication/adoption. Final paired checks pass 6,048 captured native samples per type across three replays with identical full audio. All 204 actor-source matches and 63 scenery/edge reconstructions pass exactly. See docs/POISON_MOSS.md and evidence/poison_moss/ for completed checks and coverage.

## Previous review — 0.13.0, feature/level3-caves

The 7,592-frame movie reproduces fish shaking in room 9B96, including two fish oscillating in opposite phases. The previous correction was confined to room 9AA6 and a single active fish. The new registration matches each rendered fish at its own player-relative horizontal equilibrium. Complete source poses shift ±1 HD pixel, independently of object count; fins, vertical motion, native OAM blinking, collisions and audio remain. Partly clipped boundary sprites fall back to the original registration.

The next recorded areas are the second fish/lava corridor (9B96), vertical blade-ring climb (9C86), stone-cap/lava corridor (9CFE), and beginning of the bat descent (9DEE). Reuse the approved cave, brown terrain, carved stone, lava/ice and returning actors; the green floating skeletal creature is the only new painting. Keep solid support bodies visible. Later portions of the descent and the boss are untested and unfinished.

This candidate changes hires.txt and installed README, adds one atlas, and preserves all 98 previous art/audio files exactly. The 101-file pack is review-only; no source push, PR, merge, tag or release is implied. The approved continuation remains 0.11.2 and main remains 0.10.2. Final paired checks pass 7,727 captured native samples per type across four replays with identical full audio. Six hover checks prove 516 stable fish source samples; all 63 scenery/edge source checks match exactly. See docs/LEVEL3_CAVES.md and evidence/level3_caves/.

## Previous review — 0.12.2, feature/level3-lava

The new 1,200-frame movie reproduces the actual report: the large fish shifts horizontally by one native pixel every frame while hovering, without being hit. The original sprite and HD fish share this native OAM oscillation. The previous small-fish fix did not address this reported motion.

A graphics-only correction offsets the complete existing large-fish art by ±1 HD pixel in the observed horizontal hover/cruise state. This cancels the two-HD-pixel alternation at hover equilibrium while retaining the native vertical bob and fin animation. It is scoped to mode 10 / room 9AA6, exactly one active type-26 fish, fractional horizontal speed CC with high byte 00/80, and no damage timer. Both native mirror directions are handled. Other states and ambiguous multiple-fish cases retain the original registration. No emulated state or IPS is modified.

Only hires.txt, unused cells in Stage3_Lava_Tiles_2x.png and installed README change; all 97 other installation files and every existing atlas cell stay exact. The source fish images are unchanged. See docs/BIG_FISH_MOTION.md and evidence/big_fish_motion/. All three paired routes pass 5726 frames per build with identical native state/APU/PCM; all 313 measured hover pictures have zero horizontal shake and unchanged vertical motion. This review is not approved or published. Approved continuation baseline remains 0.11.2; main remains 0.10.2.

## Previous review — 0.12.1, feature/level3-lava

The user clarified that the fish looked blurry/glitchy during movement, not in still artwork. No sharpening or new design is applied. Independent per-frame adaptive color reduction made all 227 visible pixels in the small fish's two poses change; only the fin should move. Reuse the first pose's palette and exact pixels wherever its scaled source is static. Both large-fish poses and the first small-fish pose remain exact. Existing atlas slots are preserved, so hires.txt and all other runtime mappings stay byte-identical to 0.12.0.

Consecutive-frame investigation also identifies the large fish's blink after impact in native OAM: eight cells alternate with none. That native hit blink is preserved. The report does not establish that every perceived motion artifact on the user's display has been reproduced. See docs/FISH_MOTION.md and evidence/fish_motion/. The full 3,705-frame stride-one pair passes: 562 images change only inside the small alternate pose, 3142 valid images remain exact, and native memory/APU/full PCM match. This candidate remains unapproved and unpublished; approved continuation baseline is 0.11.2 and main stays 0.10.2.

## Previous review — 0.12.0, feature/level3-lava

Implements the next supplied recording: the Start/pause-menu boot now uses the approved collectible, the complete recorded lava corridor reuses approved cave/brown terrain/carved steps, large and small fish receive two painted poses each, and hot/frozen lava uses exact existing atlas cells. Breaker now has all 21 native charge/release/flight identities, including upward release/bolts, both directions and both observed spell palettes. Source-identical copies in twelve banks share the replacements; only the recorded bank has fresh live coverage.

The new branch starts from approved 0.11.2 at `9eb0678f0ba3ee9aed9d19481c6eacb5f89fdd58`. This candidate is not approved, pushed or merged. It adds one atlas and changes only hires.txt and installed README among the previous 99 files; 97 prior runtime assets stay exact. The expected manifest describes 0.12.0, while `0.11.2-pack-sha256.json` retains the approved continuation baseline. Main remains merged 0.10.2. See `docs/LEVEL3_LAVA.md` and `evidence/level3_lava/` for paired native-state/audio, sprite, source-art and edge checks. Later Level 3 rooms and the boss are outside this recording.

## Approved continuation baseline — 0.11.2, feature/level3-opening

The user approved the delivered 0.11.2 by saying "approved" on 2026-10-25 (America/New_York). `evidence/level3_detail/approval.json` pins the reviewed artwork commit and install ZIP. All 99 reviewed installation files, including the historical review label in the installed README, stay exact. This is the baseline for further Level 3 work; source publication, PR/Actions and merge remain pending.

Addresses the newly identified round shot (0694), the collectible boot (068A–068D), and split-looking branch surfaces (0768–0770). The shot reuses the approved small fireball; the boot and branches use new painted sources. The branches retain every original alpha contour. All 96 prior runtime assets other than mappings/README are exact; one new atlas brings the pack to 99 files. Approved main remains 0.10.2; the branch is not pushed or merged. See docs/LEVEL3_DETAILS.md and evidence/level3_detail/.

The previous review changed 06B6–06B9, which were incorrectly identified as the reported projectile. The screenshot and native OAM identify 0694 as the actual round shot; this version adds that mapping. The old B6–B9 artwork remains unchanged pending separate confirmation of its role.

## Previous review — 0.11.1, feature/level3-opening

Addresses all four requested corrections: spinning blade-ring enemy, flame shots for the first golden creature, an insect-like winged eye, and continuous knotted oak surfaces. All 93 prior assets other than mappings/installed README remain exact; three new PNGs bring the pack to 98 files. Approved main is still 0.10.2; this branch is not approved, pushed or merged. Full movie and pixel/geometry checks are documented in docs/LEVEL3_REVIEW.md and evidence/level3_review/.

## Superseded review — 0.11.0, feature/level3-opening

Builds the first three Level 3 rooms from the user's Mesen movie: forest approach, tree climb and masonry shaft. Adds the night forest panorama, wide-tree bark, three ember-creature forms and two crimson flyer forms. Reuses approved Randy/HUD/weapon poses, eyes and blue tears, ceiling bats, lava/ice, brown terrain, branches and nave masonry. The following corridor retains its original scenery while verified shared actor aliases also work there.

Approved main remains 0.10.2. This candidate is not approved, pushed or merged. All 91 prior files other than hires.txt and installed README are byte-identical, and removing the marked Level 3 blocks restores the exact approved mapping bytes. The current expected manifest describes the candidate; evidence/0.10.2-pack-sha256.json retains approved main.

The full recorded route supplies three-room traversal, both Randy costumes, combat, Blizzard, menus, and transition into the next corridor. A native-core movie harness now supports embedded-state .mmo inputs, continuous audio capture and a synchronized screenshot observer. See docs/LEVEL3_OPENING.md and evidence/level3_opening/ for measured results and remaining coverage limits. Later Level 3 scenery and its boss remain unfinished; the supplied recording is enough to start the next corridor batch without another recording.

## Approved baseline — 0.10.2, main

Repairs the reported original-Randy flash after collecting Breaker. The three final native fade palettes were absent from the boss bank’s player aliases. The repair keeps the existing normal/Twin Fire artwork and every pose condition, using three brightness steps inside the boss room. No images are created or modified. Only hires.txt and installed README change; all 91 other files match approved 0.10.1.

The supplied defeat state and earlier boss state reproduce the defect in both costumes. Paired controller replays cover both pickup routes, an alternate pickup timing and combat/pose regression. The automatic pickup animation holds Randy facing right; mirrored combat poses are checked unchanged, and the aliases retain native mirror behavior. See `docs/BREAKER_RANDY.md` for exact coverage and `evidence/breaker_randy/validation.json` for results. The user approved the delivered pack and authorized its merge on 2026-10-24 ("approved. merge it"). PR #12 is merged into main. Approval bookkeeping preserves all 93 reviewed installation files, including the historical review label in the frozen installed README. See `evidence/breaker_randy/approval.json`, `pr_artifact.json` and `main_artifact.json` for the exact approval, merge and downloaded artifact checks. PR and main builds passed; both actual downloaded artifacts match all 93 expected hashes, archive digests, CRCs and flat layouts.

## Previous approved baseline — 0.10.1

The user approved the delivered 0.10.1 on 2026-10-24 ("approved"). `evidence/boss2_review/approval.json` records the reviewed artwork commit and exact installation hashes. Approval bookkeeping changes only source documentation; all 93 installation files and the delivered install ZIP remain unchanged. The historical review label in the frozen installed README is retained to preserve those exact bytes. The user authorized “merge them all”; all four feature branches are merged through PRs [#8](https://github.com/kgrant191/holy-diver-hd/pull/8), [#9](https://github.com/kgrant191/holy-diver-hd/pull/9), [#10](https://github.com/kgrant191/holy-diver-hd/pull/10) and [#11](https://github.com/kgrant191/holy-diver-hd/pull/11). That merge established approved 0.10.1, now superseded by the 0.10.2 repair above. See `evidence/stage2_adoption/merges.json` for the exact merge commits and main builds.

Fixes both reported boss reappearances. The new save defeats the boss on the gold hit palette; its two darker fade palettes were missing, briefly exposing the original NES art. They now use dimmer versions of the existing HD boss. The native Breaker flash previously selected a deliberate black boss silhouette; the repair uses the existing transparent cell so the defeated boss stays gone while the cave flash remains. No new painting is introduced.

Four final paired routes pass 6,020 frames per build and 3,810 identical RAM/PPU/OAM/PPU-view samples per type. APU writes and 19,232,332 common PCM bytes match; the new-save run has one 3,196-byte shutdown-buffer tail difference. The new save is captured every frame, with one identical empty initial capture. All 38 changed pictures stay within the boss tile coverage: eight samples for each gold fade and 22 samples clearing the pickup echo across both victory routes. Every non-sprite pixel in that coverage matches the HD fade source or pale cave pixels. The other 3,771 valid pictures remain exact, including 810 combat/pose/arena pictures and the existing announcement, Stage 3 transition and pause menu.

One retained 0.10.0 arena picture differed around Randy/projectiles despite identical native state/audio. A complete paired 720-frame repeat with unchanged pack manifests has all 360 images exact and matches the first candidate replay. The cause of the old capture discrepancy is unconfirmed and recorded in `evidence/boss2_review/arena_capture_repeat.json`; no image exception is accepted by the final verifier.

Only hires.txt, the boss atlas's previously unused cells and installed README change from 0.10.0; all 90 other runtime files remain byte-identical. The 93-file ZIP passes CRC, flat-layout and all hashes. Actual comparison/video show both repairs. See `docs/BOSS2_REVIEW.md` and `evidence/boss2_review/validation.json`. Earlier coverage limits remain. All four initial PR builds pass. Downloaded artifacts contain 86/89/90/93 root files for 0.7.1/0.8.3/0.9.0/0.10.1; every expected SHA-256, archive digest and ZIP CRC matches, with no nested ZIP. Records are in the corresponding `pr_artifact.json` files. PRs #8 → #9 → #10 → #11 merged in order, retargeting each successor to main. Each merge tree exactly matches its reviewed feature head. All four main Actions builds pass, and their actual downloaded artifacts independently match all expected hashes, archive digests, CRCs and flat layouts; see the corresponding `main_artifact.json` records. No release or tag was created. This adoption record changes no build input or installation byte.

## Superseded review candidate — 0.10.0, feature/2-boss

Adds the Level 2 wall-root demon in its complete native tile layout, its hit/defeat palette phases, Breaker tome and announcement. Reuses the crimson cave panorama, original brown terrain texture, Randy poses, HUD and fireball source. The boss's new graphics bank has 366 verified actor aliases with remapped pose anchors. All 88 earlier runtime asset files stay byte-identical; three additions bring the pack to 93 root files.

Five paired controller routes pass 5,740 frames per build, with 2,870 identical RAM/PPU/OAM/PPU-view samples per type, identical APU writes and all 18,337,804 PCM bytes (zero shutdown-tail difference). Source checks find 64 ordinary whole-visible boss matches, one gold hit phase and one black victory silhouette; one match shows the entire unclipped boss. The flash additionally matches 21,859 pale cave pixels because its end-frame palette has already reset. Complete fireball/tome matches total 74/18. The defeated boss reveals 15,494 exact cave pixels, and ten announcement samples match the Breaker card. All 660 prior 2-6 captures remain exact, along with 736 outside-room pictures and 20 native black captures.

Coverage includes the boss defeat, Breaker collection/announcement, existing Stage 3 card/arrival, and Breaker pause-menu selection. The initial one-frame early announcement is repaired with a rendered-letter guard; all final candidate/regression runs use the delivered hashes. Stage cards 1–3 are verified; cards 4–6 and later Breaker interactions remain untested. Previous far 2-5/2-6 exit and handled-health-jug pickup limits remain. See `docs/BOSS2.md` and `evidence/boss2/validation.json`.

The 93-file install ZIP passes CRC, flat-layout and every hash. Comparison and video use actual Mesen captures. The source bundle includes all four feature refs through `feature/2-boss`; screen2-6 also records the user's 0.9.0 approval. Main remains 0.6.1. User push, PRs and Actions artifact checks remain pending; the boss artwork is a review candidate.

## Approved continuation baseline — 0.9.0, feature/screen2-6

The user approved the delivered 0.9.0 on 2026-10-24 and requested the level 2 boss next. Approval is recorded in `evidence/screen2_6/approval.json`; runtime files and hashes remain exact. The user previously moved on to screen 2-6 and requested automatic reuse of finished enemies and scenery. The build adds 485 shared Stage 2 fallback mappings after all room-specific rules. Exact native identities and palettes reuse existing artwork, retaining pose anchors and lava animation conditions. The new room reuses the red cave panorama, original brown terrain and bats; only the two-pose walking dragon is newly painted. Its horizontal shot uses the existing fireball source. All 87 prior runtime assets remain byte-identical; one new atlas brings the pack to 90 root files.

Seven paired routes pass 9,580 frames per build, with 4,790 identical samples per RAM/PPU/OAM/PPU-view type, identical APU writes and 30,605,608 identical common PCM bytes. One run has a 3,192-byte shutdown-buffer tail difference. Live source matches cover both dragon strides and both directions, both fireball directions, folded/open bats and 310 panorama pictures. Native blackouts and menus remain exact. Prior-room regression preserves 1,441 pictures including all 300 stair captures. Its only 59 changed pictures show a previously unmapped 1-up now using the existing approved figurine; all differences stay inside that native item footprint, with source pixels and surrounding scenery verified.

Coverage reaches camera scroll 249 in 2-6, with combat, jumps, spell selection, Blizzard flashes and death/return. The far exit and a new hot/frozen lava crossing remain unverified. Earlier 2-5 exit and handled-health-jug pickup limits remain. See `docs/SCREEN2_6.md` and `evidence/screen2_6/validation.json`. The 90-file install ZIP passes CRC, flat-layout and every hash; the actual comparison/video are verified.

The source bundle includes feature/screen2-4, feature/screen2-5 and feature/screen2-6, with the current combined work on screen2-6. Older refs and approved main 0.6.1 remain unchanged. Moving to the next screen is continuation, not merge authorization. User push, PRs and Actions artifact checks remain pending.

## Prior continuation baseline — 0.8.3, feature/screen2-5

The user rejected the charcoal/plum roof and requested the original brown ceiling. This restores 46 exact original atlas-cell references from 0.8.0. The accepted 0.8.1 stairs, red panorama, removed red columns, gold platforms and health jug remain intact. All 87 runtime assets from 0.8.1 stay byte-identical. The rejected roof atlas is excluded; the install returns to 89 root files.

Five paired routes pass 6,800 frames per build, with 3,400 identical RAM/PPU/OAM/PPU-view samples per type, identical APU writes and all 21,724,228 PCM bytes (zero shutdown-tail difference). All 300 stair captures remain exact, along with 1,479 outside-room pictures, 80 black captures and 56 menu captures. Every one of the 1,652 changed images stays within ceiling cells; 1,748 images remain identical. Source checks find 67,420 exact original ceiling-cell matches across 12 observed identities, 143 complete folded bats with visible ceiling contact, and 26,391 unchanged gold floor-body cells. The native head-bump Y progression remains exact. All before/after installation hashes match the final 89-file pack.

The local ZIP passes CRC, flat-layout and all 89 hashes; the actual comparison/video show the restored brown roof. Coverage reaches the hot lava fall at camera scroll 482, then death/return. The far exit, uninterrupted middle of 2-4 and live handled-health-jug pickup remain unverified. See `docs/SCREEN2_5_BROWN_ROOF.md` and `evidence/screen2_5_brown_roof/`. The source bundle contains both feature refs; current accepted stairs and ceiling are on feature/screen2-5, while feature/screen2-4 retains 0.7.1. Approved main remains 0.6.1; source push, PRs and Actions remain pending. No merge or release is authorized.

## Rejected ceiling candidate — 0.8.2, feature/screen2-5

The user accepted the 0.8.1 stairs but found the faint roof outline unclear. This revision restores the complete solid ceiling silhouette in charcoal/plum stone with a lighter lower edge, making head-bump boundaries and bat attachment points visible against the red cave. All 87 previous runtime assets remain exact, including the accepted stairs; red foreground columns remain removed. One new atlas brings the pack to 90 root files.

Five paired routes pass 6,800 frames/build and 3,400 exact native samples/type, with identical full PCM and APU. All 300 stair captures, 1,479 outside-room pictures, 80 black captures and 56 menu captures remain exact. The 1,652 changed captures stay inside ceiling cells. Source checks pass 67,420 ceiling matches over 12 observed identities, 143 complete hanging-bat/ceiling contacts and 26,391 unchanged gold floor-body cells. All 46 ceiling identities preserve their earlier alpha contours. See `docs/SCREEN2_5_ROOF.md` and `evidence/screen2_5_roof/`.

Coverage reaches the hot lava fall at camera scroll 482, including the low-overhang jump, then death/return. The far exit, uninterrupted middle of 2-4 and live handled-health-jug pickup remain unverified. The install ZIP passes all 90 hashes, CRC and root-layout checks; the comparison video decodes successfully. The source bundle includes both feature refs. The accepted stair appearance is on feature/screen2-5; feature/screen2-4 retains its earlier 0.7.1 source. Approved main remains 0.6.1; user push, PRs and Actions checks remain pending. No merge or release is authorized.

## Superseded review candidate — 0.8.1, feature/screen2-5

Responds to the user's rejected rock stairs, heavy brown ceiling and foreground red columns. Uses pale-edged cut-stone treads in both rooms, removes the ceiling fill/columns in 2-5 and retains the accepted panorama, gold platforms and slim overhead boundaries. The health screenshot reveals a previously unmapped four-tile handled jug; new opaque red/brass art covers its five exact native CHR groups. All 86 previous runtime assets remain byte-identical; one atlas brings the install to 89 root files.

Five paired controller routes pass 6,800 frames/build with 3,400 exact native samples/type and identical full PCM/APU. They preserve 80 black captures, 259 outside-room captures and 56 menu captures; 25,569 gold platform-body cell checks and 352 complete stair matches pass. Coverage extends to camera scroll 482 and the lava fall, then death/return. The far exit remains unverified. The jug mapping, native bounds and opacity are checked statically; the actual pickup is not reached, so a save with that jug visible is needed for its live check. See `docs/SCREEN2_5_REVIEW.md` and `evidence/screen2_5_review/`.

The final stair appearance is on feature/screen2-5; feature/screen2-4 retains the earlier 0.7.1 candidate. Both refs remain in the source bundle and unmerged. The user subsequently accepted the 0.8.1 stair appearance; the ceiling direction was superseded by 0.8.2. Approved main remains 0.6.1. Local ZIP hashes/CRC/layout pass; user push, PRs and Actions checks remain pending.

## Superseded review candidate — 0.8.0, feature/screen2-5

Adds the crimson cave reached by jumping up the repaired stairs. A new large-scale red cavern panorama replaces the tiny repeating wall motif, and a new atlas registers shaded crimson mineral columns within their native outlines. Reuses 359 existing rules for gold terrain/stairs, lava/ice, ghouls, bats and eyes with blue tears; player/HUD/items remain shared. All 84 previous runtime assets stay byte-identical. Two new installed PNGs bring the pack to 88 root files.

The branch is stacked on the unapproved 0.7.1 stair repair at `937c7c7`; both review branches are retained in the source bundle. Approved main remains 0.6.1. No merge/release is authorized. Results and precise coverage are in `docs/SCREEN2_5.md` and `evidence/screen2_5/`.

Five paired controller routes pass 6,200 frames/build with 3,100 exact native-memory samples per type and identical full PCM/APU. They preserve 76 black captures, 848 outside-room pictures (including the 300-picture stair walk) and 56 menu pictures. The new panorama has 211 source-pixel matches; folded bats, eyes and blue tears also match their reused source artwork. Live coverage reaches camera scroll 281, the first bat and several eye platforms, combat in both player directions, Blizzard flashes, pause and death/return. The far 2-5 exit remains unverified. Local install ZIP CRC/layout and all 88 file hashes pass; source push, PRs and Actions checks remain pending.

## Stair review candidate — 0.7.1, feature/screen2-4

Repairs twelve original stair identities at the end of screen 2-4 with the existing gold texture and exact native contours. Two controller-only routes pass 1,800 frames/build with 900 exact samples per native-memory type and identical full PCM/APU. All changes remain inside the native stair cells; 332 next-room pictures remain exact. The supplied end state extends coverage to both stair flights and the upward exit into screen 2-5, without claiming traversal of the previously untested middle stretch. Only hires.txt, the ceiling atlas's previously unused cells and installed README change from 0.7.0. No approval/merge/release is requested yet. See `docs/SCREEN2_4_STAIRS.md`.

## Earlier review candidate — 0.7.0, feature/screen2-4

The next horizontal cave reuses the approved panorama, gold terrain, winged demons with downward arrows, faceless pulsing rock enemies, lava/ice, player, pickups and HUD. All 512 native patterns match the earlier exterior bank. The only new installed image is a 128×64 ceiling-registration atlas using the existing gold texture; 304 aliases reuse previous mappings and 44 new rules fit additional ceiling edges and clear nonsolid wall patterns. All 83 prior runtime assets remain byte-identical. The install ZIP contains 86 root files.

Paired controller checks pass 12,760 frames/build and 6,380 exact native-memory samples per type, preserving APU/common PCM, 257 black captures and 1,427 outside-room pictures. All 647 measured hot-fall pairs move downward; all 456 ice pairs stay stationary. Live coverage includes the previous-room approach, combat/poses, menus, death/respawn, breakable-block ledges and the first two falls/pool, reaching camera scroll 537. The far exit remains unverified.

This is a review candidate based on approved main `5fdae8a88920ad6612d9f01ee913d85af6837209`; approval, source-bundle push, PR and Actions checks are pending. No merge or release/tag is authorized for this candidate. The historical `approved-pack-sha256.json` filename pins the candidate bytes on this branch and does not grant approval. See `docs/SCREEN2_4.md` and `evidence/screen2_4/` for exact tests and coverage. Full room exit coverage is not claimed.

## Current approved version on main — 0.6.1

**0.6.1** changes the floating-eye projectiles into blue teardrops, as requested. Pointed tops, rounded liquid bodies and cobalt/cyan highlights replace the fire-like art. Only the two projectile cells and installed README change; the other 83 pack files, mapping file, eye bodies, scenery and unrelated fireballs remain byte-identical.

Focused paired checks pass **2,400 frames per build** with 1,200 equal RAM/PPU/OAM samples per type and exact APU/equal-length PCM. All 637 changed captures are confined to eye-projectile bounds; 563 others remain exact. Both tear identities and their mirrored forms have complete pixel-exact live matches. See `docs/SCREEN2_3_REVIEW.md` and `evidence/screen2_3_review/`. The earlier full-room/exit tests remain below; the repair replay covers combat, scrolling and death/respawn. The install ZIP still contains 85 root files. The user approved v0.6.1 in chat on 2026-10-24 ("approved"). Reviewed artwork commit: `29bf3b688010fd46863103c2974c8ae88f3c1c62`. The user pushed feature/screen2-2 at `2a6022930c45a40f79b313d1838ded4285af1492` and feature/screen2-3 at `29bf3b688010fd46863103c2974c8ae88f3c1c62`. Approval bookkeeping was published at `167f9f6fcddcade222e1074180907d5f41e9f545`; only installed README changes and all 84 runtime files retain the reviewed hashes. `0.6.1-reviewed-pack-sha256.json` preserves the accepted review, and `0.6.1-pack-sha256.json`/`approved-pack-sha256.json` pin the approved installation.

The user explicitly authorized both merges on 2026-10-24 ("merge it"), resolving the earlier automatic-approval block. [PR #6](https://github.com/kgrant191/holy-diver-hd/pull/6) merged screen2-2 at `e3d957fc75e80ba9a6d9c6dd5afe61be6c557470`; [PR #7](https://github.com/kgrant191/holy-diver-hd/pull/7) was then retargeted to main and merged screen2-3 at `40d67dbf516eaea5b2a20e3ad9a8093a7d7b347a`. Main now contains the approved 0.6.1 artwork. No release/tag was created.

PR runs 40052944384 (0.5.1) and 40053346170 (final 0.6.1 head) passed. Main runs 40053555272 and 40053648543 also passed. The actual downloaded PR and main artifacts have 84/85 root files respectively, match every approved SHA-256 hash, pass ZIP CRC checks and contain no nested ZIP. Compact records are in each screen's `pr_artifact.json` and `main_artifact.json`, plus `evidence/screen2_3_review/approval.json`. Adoption records change no installed pack files; all 85 approved installation hashes remain exact.

## Superseded 0.6.0 candidate — feature/screen2-3

**0.6.0** adds the vertical cave from the user's next save, based on locally approved 0.5.1. Reuses the accepted cave panorama, gold terrain, ghouls, lava/ice, pickups, player and HUD through 98 aliases. The new artwork is a compact ivory/teal floating eye with a crimson spiked rim; both shot identities use the accepted fireball source within measured native bounds. Six nonsolid wall-pattern tiles reveal the stationary distant cave layer while platforms scroll vertically.

Final paired tests pass **5,560 frames per build**, with 2,780 identical RAM/PPU/OAM samples per type, exact APU events and common PCM, 106 exact black frames, 270 unchanged next-room captures and 1,957 exact full-color cave-backdrop samples. Complete rendered sprite checks cover the eye, both projectile shapes/flips and all six ghoul poses in both directions. The controller-only route traverses all 512 pixels of vertical camera travel, crosses frozen lava and enters room 10 at pointer AD/8C. Pause, upward/crouching casts, hot/frozen palettes and death/respawn are included. See `docs/SCREEN2_3.md` and `evidence/screen2_3/verification.json`.

The pack contains 85 root files. Only hires.txt and installed README change among approved 0.5.1 files; all other 82 remain exact, and one atlas is added. Removing SCREEN2_3 sections recovers the exact 0.5.1 mapping file. `0.6.0-pack-sha256.json` preserves this superseded review candidate; `approved-pack-sha256.json` now pins approved 0.6.1. Native death grayscale is visually inspected; source-RGB panorama checks apply to actual full-color wall rendering. The next room is unchanged future work, and this run does not establish complete traversal of the preceding horizontal cave.

The original source handoff was based on main 14434d6. This screen addition and the blue-tear repair were subsequently accepted together in 0.6.1 and merged through PR #7, following PR #6 for the previous cave. No release/tag was created.

## Previous approved version — 0.5.1 (merged through PR #6)

**0.5.1** revises the cave after the user requested removal of the reddish rock layer and waterfall motion in the lava falls. The ten decorative red tile identities now expose the unchanged cave backdrop. Hot fall tiles use a continuous sixteen-phase downward loop, advancing two HD pixels every two emulated frames. Each body row and the loop seam align; the native hot palettes still pulse and select the static ice artwork during Blizzard. All six ice fall tiles and every other cave tile variant retain their source pixels.

Only `hires.txt`, `Stage2_Cave_Tiles_2x.png` and installed `README.txt` change from 0.5.0; all 81 other pack files remain exact. The pack still contains 84 root files. `evidence/0.5.0-pack-sha256.json` pins the prior candidate; `0.5.1-pack-sha256.json` pins this approved build. See `docs/SCREEN2_2_REVIEW.md` and `evidence/screen2_2_review/` for paired native-state/audio, unchanged-art bounds and measured downward-motion/frozen-state checks.

Final paired checks pass 5,680 frames per build and 2,840 native-memory samples per type, preserving APU/common PCM, 258 black captures and 262 outside-cave captures. The rendered fall advances downward in all 173 stable-palette pairs; all 222 frozen pairs stay stationary. A fresh capture of the unchanged 0.5.0 crossing resolved one older screenshot discrepancy; the final verifier has no exceptions.

Coverage remains the supplied entry through the first fall and opposite ledge, both-direction combat, menus, Blizzard freeze/thaw, death/respawn and the previous-room approach. Full cave exit coverage remains unverified. Main was 0.4.1 at the initial review. The user approved the visuals in chat on 2026-10-24 ("looks good. ok next screen is here in this save state"). Reviewed commit: `8d67d65eae7f32a8df5eb3283e0e34b1a3967460`. At approval time, GitHub had no feature/screen2-2 ref. The user subsequently pushed `2a6022930c45a40f79b313d1838ded4285af1492` and explicitly authorized the merge. PR #6 merged at `e3d957fc75e80ba9a6d9c6dd5afe61be6c557470`; PR/main Actions and their downloaded 84-file artifacts were verified. This work is now included in approved main 0.6.1. Only installed README changes during approval bookkeeping; all 83 runtime files retain the reviewed hashes. Continue new work from approved main 0.6.1. No release was requested.

## Superseded 0.5.0 review candidate — feature/screen2-2

**0.5.0**, based on approved main `14434d6ff9604db085a968eda12b317d43474c47`. The supplied `Holy_Diver_HD_1(8).mss` starts inside the Stage 2 cave. Reuse is explicit: 86 aliases point to approved terrain, pools, items, snow and purple ghoul art. The ghoul's 24 native tiles are byte-identical copies shifted six slots within the new bank, so both tile rules and standing-pose anchors are translated. Randy and HUD were already shared. New work covers the cave backdrop/formations, ceiling bats and vertical fall registration.

The candidate contains 84 root files. All 80 prior files other than hires.txt and README.txt remain exact; only those two change and two PNGs are added. `evidence/0.4.1-pack-sha256.json` pins approved main. The historical `approved-pack-sha256.json` filename describes this branch's candidate and does not grant approval. See `docs/SCREEN2_2.md`, the actual Mesen comparison and `evidence/screen2_2/verification.json`.

Coverage is deliberately bounded: entry through the first lava fall and opposite ledge, combat/pose/direction checks, Blizzard freeze/thaw, pause menu, death/respawn and the previous-room approach. The full cave exit has not been reached in these controller-only replays. Do not describe the whole room or later rooms as completely tested. Paired verification passes 5,680 emulated frames per build, with 2,840 equal RAM/PPU/OAM samples per type, identical APU/common PCM, 258 exact black captures and 262 unchanged outside-cave captures. Actual images contain 1,866 complete folded-bat and 74 open-bat matches, plus all six ghoul poses in both directions. The local ZIP and incremental source bundle are for review; user push, PR, Actions artifact verification and approval are pending. No merge or release is authorized for 0.5.0.

## Previous approved main baseline — 0.4.1

**0.4.1**, approved by the user in chat on 2026-10-23 ("approved"). Reviewed artwork commit: `c4ff13db886046d97f9f57572aef98517c3d1076` on `feature/screen-2-1`, based on approved main `19176d026eb5670523ad8358d82447c63732d506` (0.3.5). The user requested repairs to the initial Stage 2 exterior candidate: keep the cave opening dark from first reveal, correct the backward-facing brown flyers into winged demons with downward arrows, and remove faces from the pink/red pulsating rock enemies.

The cave uses its visible left jamb with a screen-boundary guard, so its right wall need not be onscreen. The flyer source faces left to match measured unflipped movement; native mirroring faces right. Both wing phases preserve the body, and held/falling arrows share one source. Three pink-shell/crimson-lobe poses replace the rejected face-like rocks. Native terrain, movement, timing, inventory and audio remain unchanged. See `docs/SCREEN2_1_REVIEW.md`.

The build contains 82 root files. Only `hires.txt`, `Stage2_Exterior_Tiles_2x.png` and `README.txt` change from 0.4.0; all 79 others remain exact. The 103 non-enemy tile images in the Stage 2 atlas are unchanged, and the new demon fits its native OAM footprint with zero opaque-pixel clipping. All 78 runtime assets from approved 0.3.5 remain exact. The prior review manifest is retained as `evidence/0.4.0-pack-sha256.json`. `0.4.1-reviewed-pack-sha256.json` pins the exact tested and accepted bytes. Approval bookkeeping changes only installed README.txt; all 81 runtime files stay byte-identical.

The seven controller routes cover the original six exterior/Blizzard cases plus the supplied cave approach through next-room arrival. Final verification is recorded in `evidence/screen2_1_review/verification.json`; the visuals are now accepted by the user. The next room's existing art is preserved, not redesigned. The user pushed `17d9021af5c43f5ec0e31af12ae4860250dd32e9`, then explicitly authorized the merge ("ok merge it then, you've been doing the merges"). [PR #5](https://github.com/kgrant191/holy-diver-hd/pull/5) merged at `b50f95862e4fc49e5f86d71d82f81f48ff87bd35`. PR Actions run 40018693181 and main run 40019141872 passed. Both actual downloaded artifacts were independently checked: 82 files at the archive root, all approved SHA-256 hashes matching, ZIP CRC checks passing and no nested ZIP. See `evidence/screen2_1_review/pr_artifact.json`, `main_artifact.json` and `approval.json`. Use 0.4.1 as the approved baseline for subsequent work; no tag or public release was created.

Final paired verification passes across **6,460 frames per build**: all RAM/PPU/OAM and APU events match; common PCM is identical. There are 357 exact black frames, 579 unchanged outside-room captures, and 129 verified early cave-interior samples. Stationary-camera motion samples show 499 left-facing native steps and 209 right-facing mirrored steps, with no opposite-direction samples. All new enemy/arrow identities are observed. Audio shutdown-tail differences, where present, are at most one 3,200-byte buffer and are recorded per case. A complete unchanged-pack cave repeat resolves the one documented duplicated screenshot; final checks contain no exceptions.

## Superseded 0.4.0 candidate

**0.4.0** on `feature/screen-2-1`, based on approved main `19176d026eb5670523ad8358d82447c63732d506` (PR #4, 0.3.5). The user requested Stage 2 screen 1 and supplied four states covering its start, hot lava, frozen lava and later platforms. No merge or public release is authorized for this candidate.

The exterior uses new volcanic scenery and enemies, plus approved gold-ground texture and existing Randy/HUD/item/effect artwork. The native lava palette selects hot/ice textures, including the original thaw flashes. A rendered-sky tile condition suppresses the custom panorama on actual black frames; the CPU shadow of PPUMASK alone was one frame out of phase during this effect. Breakable blocks and the exit cliff remain tied to their native tiles. Small heart/magic drops and 1-up figurines reuse approved art in this CHR bank; large flasks and defeat rings already had shared mappings.

The build has 82 root files. Only `hires.txt` and `README.txt` change among the 80 approved files; all 78 previous runtime files stay byte-identical. `evidence/0.3.5-pack-sha256.json` preserves the approved baseline. The historical `approved-pack-sha256.json` filename describes this branch's review candidate and does not grant approval. Full results and limitations are in `docs/SCREEN2_1.md` and `evidence/screen2_1/verification.json`.

The six exterior replays pass across 6,040 frames per build, with exact RAM/PPU/OAM and APU events, identical common PCM, and 350 exact native black frames. The neutral cast/thaw case accounts for 92 of those black frames. Both imp directions and all three unmirrored lava-creature poses are observed. The crossing reaches native scroll 1280 and the exit cliff, then death/respawn; next-room entry is not claimed. Two audio captures differ only by one shutdown buffer (3,192 and 3,196 bytes).

Earlier boss/reward/recovery regression adds 2,470 frames per build, 1,235 exact native-memory samples per type and 1,169 exact previous-scene screenshots. Total coverage is 8,510 frames per build and 7,275 paired samples per memory type. A single inconsistent reward-fade capture in the initial run did not recur in a complete repeat with unchanged candidate bytes; the discrepancy and its unconfirmed cause are retained in `evidence/screen2_1/reward_capture_repeat.json`. Final reports pass without exceptions. The local install ZIP has all 82 verified root files; the user push, PR and actual Actions artifact check remain pending.

## Previous approved version — 0.3.5

**0.3.5**, approved by the user on 2026-10-23 for adoption through [PR #4](https://github.com/kgrant191/holy-diver-hd/pull/4). Reviewed artwork commit: `9a290ec8a9160fbbd387cf7ab1ec954da9b11199` on `feature/1-boss`, based on previous approved main `2427afd4739f273bf527810edcfae93e6592e344` (0.2.1). The user approved the final visuals, then confirmed the Actions artifact packaging and explicitly authorized the merge ("verified, merge it"). No release tag or GitHub Release is authorized.

The user confirmed the 0.3.4 leg repair ("thats fixed") and supplied two more states showing original HP/Magic flasks. The approved 0.3.5 build adds red HP and blue Magic bottle artwork for native tiles 49–4C, distinct from the already-covered small heart/crystal drops. Shared mappings cover all sixteen byte-identical CHR copies; live coverage is the supplied chapel/tree states. The confirmed Randy artwork and every other previous asset remain exact. See `docs/RECOVERY_ITEMS.md`.

The user confirmed the 0.3.2 transition fix, then reported a missing standing toe while crouching was correct. They rejected the 0.3.3 repair because the isolated boot fit cut the knee/shin outline. The 0.3.4 correction registers the full forward standing leg as one continuous piece in both costumes. It also keeps the idle knee rule active at the left-screen edge by probing the torso directly above it. Other poses and rule priority stay exact. See `docs/RANDY_LEG.md`.

The user confirmed the 0.3.1 fireball fix. The 0.3.2 transition repair extends the bell-room backdrop through the complete native vertical wrap and adds the missing bank-00 white/gray fade palettes for Randy. The repeated bell and ornaments occur in the original sequence; the HD backdrop previously ended beneath them. See `docs/BOSS1_TRANSITION.md`. The final boss feature and repairs are approved in 0.3.5.

The 0.3.1 review repair fixes the Blizzard menu's R/D font fallback and enables Mesen's supported sprite-limit removal to keep the boss fireball complete. It applies to rendering throughout this pack; it does not edit the ROM or controller route. Existing artwork stays exact, with two menu glyphs added in formerly empty boss-atlas cells. See `docs/BOSS1_REVIEW.md`.

Approved art covers the six native boss poses in both directions, hit-palette flashes, the native 36-tile progressive disappearance, the organ hall, Blizzard bell chamber, spell pickup, ascent and announcement. The Stage 2 title/lives card is now verified in live play. Known Randy/HUD copies in the announcement and Stage 2 graphics banks reuse the approved art. Stage 2 scenery/enemies remain future work.

The pack contains 80 root files. The requested standing-foot repair also changes the two Randy atlases. Along with hires.txt and README.txt, these are the only changed files among the 75 main-baseline files; 71 existing runtime files stay exact. Five PNGs are added. The old expected manifest is retained as `evidence/0.2.1-pack-sha256.json`. `evidence/approved-pack-sha256.json` now records the approved build. `evidence/0.3.5-reviewed-pack-sha256.json` preserves the exact reviewed candidate. Approval bookkeeping changes only the installed README.txt; all 79 other pack-file hashes remain identical. See `docs/BOSS1.md` and `evidence/boss1/verification.json` for reproduction and coverage.

Initial 0.3.0 live checks passed: 11,030 frames per build, 9,500 paired RAM/PPU/OAM samples per type, identical APU events and common PCM. Earlier-room regression has 1,470 identical screenshots; the unchanged Stage 2 card adds 184. Two runs have one shutdown-buffer audio-tail difference, documented in the reports. All six boss poses are observed in both directions.

The 0.3.1 repair checks pass: 7,460 frames per build, 5,930 paired native-memory samples per type and identical APU/common PCM. Title, crypt and tree images remain exact; 39 nave images restore only native sprites dropped on overflowing scanlines. The rest of the 1,470 earlier-room captures are identical. See `evidence/boss1_review/verification.json` and `regression.json`.

The 0.3.2 repair checks pass: 5,500 frames per build and paired samples per native-memory type, identical APU events and common PCM. Both pickup directions/costumes keep the HD silhouette through all 24 final fade frames. Background differences replace only previously black bell-room pixels. The full 649-image fireball replay remains exact. See `evidence/boss1_transition/verification.json`.

The rejected 0.3.3 repair passed 6,460 frames of bounds, source-pixel and native memory/audio checks, but those checks missed the visibly broken knee/shin join. Its report under `evidence/randy_foot/` remains historical evidence of preservation, not visual acceptance. The new correction adds whole-leg contour checks and live views against a clear backdrop.

The 0.3.4 checks pass across 6,940 frames per build and paired samples per native-memory type, with identical APU events and common PCM. The normal/Twin Fire entrance routes each have 248 pixel-exact complete-leg captures and 75 unchanged crouching/crouch-cast captures. Each clear-background route adds 177 complete-leg captures in both directions. Changes are confined to the standing forward leg in 2,736 images; 4,197 other valid screenshots remain identical. Both frame-616 offscreen-hand cases retain the complete registered leg. The clear-background close-ups were visually inspected in both directions and costumes. See `evidence/randy_leg/verification.json` and `comparison.png`.

The 0.3.5 pickup checks pass across 1,320 frames per build and paired samples per native-memory type. HP restores 5→6 and Magic restores 10→50 in both normal/Twin Fire costumes; neutral cases preserve each item's native expiry. All 405 changed screenshots are confined to the flask tiles, 909 valid images remain identical, and 397 captures match the complete bottle artwork exactly. APU events and common PCM match; the HP neutral case has one 3,192-byte shutdown-tail difference. All 77 previous files other than mapping/readme remain byte-identical. See `evidence/recovery_items/verification.json` and the live comparison.

The user pushed the reviewed artwork, and PR #4 was opened. Actions run [40004314865](https://github.com/kgrant191/holy-diver-hd/actions/runs/40004314865) passed: all 80 pack hashes matched, and all 80 files were uploaded directly from the extracted pack directory. The user downloaded artifact [12523247888](https://github.com/kgrant191/holy-diver-hd/actions/runs/40004314865/artifacts/12523247888) and confirmed that one extraction exposes 80 files including hires.txt, with no nested ZIP. The assistant retrieved the artifact through the integration but could not independently extract it because the execution environment was unavailable. Archive-layout confirmation is attributed to the user; CI verified file hashes before upload. See `evidence/boss1/approval.json`.

0.3.5 is retained as the previous approved baseline. Preserve the ZIP-wrapped incremental Git bundle workflow for artwork-heavy updates; small text-only approval changes may use the integration. No additional emulator replay is required for the install-text update.

## Previous approved version

**0.2.1**, approved by the user in chat on 2026-10-23 ("approved"). Reviewed commit: `ad0e91c4921648c3d67bb426feb41be519a60eb9` on `feature/screen1-4`. Preserve its screen-1-4 tree court, front-facing blue/ivory 1-up figurines, continuous Gothic wall and shared HD enemies as the accepted visual baseline.

The user pushed the reviewed artwork commit to `feature/screen1-4`. [PR #3](https://github.com/kgrant191/holy-diver-hd/pull/3) was merged into main at `2427afd4739f273bf527810edcfae93e6592e344` after approval and artifact verification. The downloaded main Actions artifact (run 39967379016, artifact 12507780985) contains all 75 expected root files with matching hashes and no nested ZIP. No release tag or GitHub Release was created.

Approval bookkeeping changes only README.txt in the installed pack. All 74 runtime files remain byte-identical to the approved review. `0.2.1-reviewed-pack-sha256.json` preserves the reviewed bytes; `0.2.1-pack-sha256.json` preserves the approved installation bytes. Historical reports and captures remain unchanged. See evidence/screen1_4_review/approval.json for the bookkeeping check.

Live verification of the approved art: 7,660 frames per build, 3,380 paired samples per memory type, exact APU events and equal-length identical PCM. Both pickup palettes award lives 3→4. Earlier title/crypt/nave regression has 468 identical screenshots; the previous-room transition adds 185 unchanged captures. The pack has 75 root files and no nested ZIP. The actual Actions artifact check is recorded in PR #3.

## Previous approved version

**0.1.1**, approved by the user in chat on 2026-10-23 ("approved. pushed") for adoption through PR #2. It adds the third chapel section, sharpens the standing purple ghoul while retaining the rolling frames, and supplies both crouching attack phases in normal/Twin Fire colors and both directions. No release tag or GitHub Release is published.

The pushed candidate is `2251a0419f6cf6e6b832dcac84ebf8ac49662357`. Actions run 39893523922 passed; its actual downloaded artifact contains 73 root files with all reviewed hashes matching and no nested ZIP. Approval bookkeeping changes only README.txt in the installed pack. All 72 other files remain identical. `evidence/0.1.1-reviewed-pack-sha256.json` preserves the reviewed bytes and `evidence/0.1.1-pack-sha256.json` retains its approved installation bytes.

## Previous approved version

**0.0.2**, approved by the user in chat on 2026-10-22 and adopted as the main baseline through PR #1 (`fix/title-screen-1-1`). It repairs the title prompt background, aligns both entrance rock shelves across their full native spans, and removes the nested ZIP from Actions artifacts. This is an approved development build; no release tag or GitHub Release is published.

The previous candidate's rightward shelf extensions were incorrect. Full traversals from the user's two save states establish upper HD X0–128 at Y192 and lower X0–160 at Y544. Continuous caps now cover the far-left standing position and stop before Randy falls. Do not use the earlier stationary-boot footprint as the platform boundary.

Current ledge verification: 920 frames per build, with 920 paired RAM/PPU/OAM samples and identical APU writes/common PCM. Both replays walk fully left, hold, and step slowly right through the fall. See evidence/ledge_boundaries/verification.json and comparison.png. The title PNGs and rules retain the exact bytes tested in the original fresh/reset title replay. Against previous approved 0.0.1, only three background PNGs and the pack README change; 67 files remain byte-identical.

## Previous approved baseline

Development version **0.0.1**, using the approved historical v15.1 artwork, accepted after the Randy arm repair (the user said "much better"). Initial GitHub import preserves all 70 runtime pack files exactly; README.txt only updates the development version and source location. Version 1.0.0 is reserved for the completed, tested game pack.

Completed: entrance/title sequence, entrance environment, known shared Randy poses and normal/Twin Fire palettes, screen-2 crypt environment/enemies, bracelet drop and matching pause icon, shared defeat-effect phases, stage/lives cards, post-death HUD, and rear forearm/hand repair.

## Historical arm verification

- Both Randy costumes, left/right, standing and airborne idle/horizontal casts. Sampled run/upward frames unchanged.
- Screen-2 combat and Randy death retain RAM/PPU/OAM, APU writes and recorded audio. Frozen death pose includes the repaired arm.
- 2,040 emulated frames and 1,558 paired state captures: evidence/arm_repair/verification.json and TEST_RESULTS.md.
- Earlier v15 tests covered fresh start/reset, normal/Twin Fire death, enemy combat and collected-bracelet pause/resume. Historical results remain in evidence/v15/.

## Approved screen-1-3 work

`feature/screen-1-3` builds approved **0.1.1**. The 0.1.0 screen addition was refined in response to the standing-ghoul and crouching-attack feedback. This is an approved development build, not a public release.

Three supplied states cover the third chapel section. Native inspection and movement revealed emerald/ruby windows, reinforced blocks, a large gold background ornament, a purple ghoul with two standing and four rolling poses, and small blue flying skulls with two poses. The approved addition supplies a solid nave wall behind those details. Randy, weapons, HUD, stone blocks, the large gold flying enemy and the expanding death rings reuse existing art.

The initial screen implementation adds 87 scoped tile rules, three palette checks, one background rule and two runtime PNGs. The 0.1.1 repairs add 50 pose rules and 66 signatures. Two Randy atlases and the nave atlas gain sprites only in previously unused cells: all earlier Randy poses and all four rolling ghoul frames are pixel-identical. The pack still has 73 files. Removing the marked screen-1-3 and review-fix sections recovers the approved mapping file exactly. The current approved build manifest is `approved-pack-sha256.json`. `0.0.2-pack-sha256.json` retains the approved baseline, and `0.1.0-pack-sha256.json` retains the prior review candidate.

Initial 0.1.0 candidate: 2,160 frames across the new states, 1,080 paired samples per memory type and identical full PCM. Regression: 1,800 fresh/reset title frames plus 360 earlier-crypt combat frames, all 270 screenshots identical; title audio has one shutdown buffer of length difference with identical common PCM.

The 0.1.1 live checks cover both crouching attack phases, both directions and both costumes, plus all three chapel routes: 2,640 frames per build and 1,560 paired RAM/PPU/OAM samples. Changes are confined to the requested sprites; 64 rolling-attack screenshots remain exactly identical. See `evidence/review_fixes/verification.json` and the live comparison images. Fresh/reset title and earlier crypt regression add 2,160 frames, 630 paired samples per memory type and 270 identical screenshots, with equal-length identical audio. Total reviewed coverage is 4,800 frames per build. Existing 0.1.0 evidence remains under `evidence/screen1_3/`.

The user has authorized adoption through PR #2. Use 0.1.1 as the baseline for the next requested change. Preserve the agreed bundle/push workflow for artwork-heavy updates. See `docs/REVIEW_FIXES.md` for reproduction commands and limits.

## Known limits

- This is a partial HD overhaul, not a finished all-stage pack.
- All six stage names and life counts 0–9 are mapped; live card coverage is Stages 1–3 and counts 4/3/2. Stages 4–6 remain untested.
- Native player tiles $33–$35 are now measured and covered as crouching wind-up legs. Tile $3C remains unclassified; investigate only when a live route uses it.
- The earlier report of Randy fully reverting to original art during death was not independently reproduced. Shared defeat fallbacks exist, and current recorded death poses remain HD.
- Old scripts remain for provenance. build.py is the supported build entry point.
- Full historical capture runs/videos and original savestates remain in the prior source/handoff archives. The repository keeps compact evidence and exact rollback inputs.

Historical 0.11.0 limitation: the spinning creature was left native. The 0.11.1 review now adds its 0695–06AF frames and corrects the projectiles, flyer and bark. Other native effects and later-room scenery remain future work; the existing recording covers the next corridor.
