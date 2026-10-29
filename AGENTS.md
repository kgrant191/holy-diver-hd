# Holy Diver HD working instructions

## Current continuation — Level 6 green hall and descent 0.28.0

The user accepted 0.27.0 ("this looks great") and supplied the 20261029-204125 movie. Preserve all 143 accepted install files as the baseline; main remains 0.24.0. No push, PR, merge or release is authorized.

Cover A20B/mode10 and the recorded A2FB/mode04 descent. Use separate dark green skull-relief reliquary and open green tower backgrounds, with the accepted green stone and ivory skull blocks. Native palettes are 0B1B3B (hall solid), 0A1A29 (decorative hall wall), 0A1A39 (shaft solid), and 081030/1B2B3B (skulls). Both 1700/1900 bank copies and normal/resume/30/31 guards are required. Exclude death/card palettes 213029/041424 from room guards.

Reuse complete ordered A0DF actor/terrain rules, retaining native masks and every sprite pose condition. 18F3–18F8 equals 02D8–02DD: approved eye/tear atlas 34 applies. 17F6/17F7 over 17F8/17F9 forms a complete 32×32 HD floating ledge from the accepted green material. Add no new neighbor probes or gameplay/audio edits. Keep exact removable 0.27.0 mappings and the full historical validator chain. See docs/LEVEL6_LATE.md. Later rooms and boss remain unfinished.

## Current continuation — Level 6 room variety and hit frames 0.27.0

The user requests distinct rooms that retain the original color families. This supersedes the earlier uniform cold-stone direction: opening rooms use red stone with their separate exterior/hall backdrops; 9F3B is an amber ossuary; A02B is a crimson vertical shaft; A0DF is a green crypt with blue accents. The 20261029-190811 movie traverses the full shaft and green room. Preserve native structural hulls, carved ornaments, skull blocks, lava/ice, menus, blackouts, timing and audio.

Both sentinel damage palettes (FF102030 and FF122232) reuse all 53 byte-identical cells from finished atlas 51. The projectile follows both hit palettes; the returning spark also reuses its approved source. The green room inherits complete actor rules and normal/resume/30/31 bank guards for 1700/1900. Clear only its measured decorative blue wall palette. New room art is a removable layer plus reversible corridor/shaft panorama substitutions; all 134 previous art/audio/patch files remain exact. See docs/LEVEL6_VARIETY.md.

Work remains local on `feature/level6-opening`; approved main stays 0.24.0. Later Level 6 rooms and the final boss remain unfinished. No push, PR, merge, tag or release has occurred.

## Current continuation — Level 6 skull corridor 0.26.0

- The 20261029-181929 movie traverses 9F3B/mode10 and shows only the entrance of A02B/mode04. Reuse the enclosed citadel, skull blocks and cold stone. Both physical background banks 1700/1900 have identical bytes; cover both, including normal/resume/30/31 palettes. Preserve every native structural hull and menu/blackout.
- Bank1800 needs complete pose-conditioned Randy/HUD/effect aliases, including remapped sprite-neighbor identities. 18A9–DD reuses all four silver sentinel poses; 18DF–E6 is the returning flying skull, not a ghoul. 18F9 reuses the finished round shot. The differently patterned one-cell 18EB/FF000F30 also reuses that art, explicitly not a CHR-identity claim.
- 18E7–F2/FF072630 forms two whole bronze crawler poses at the A02B entrance. Keep their measured native cell unions, full connected registration and zero clipped corner pixels. Do not conflate its 18EB body cell with the differently paletted projectile.
- Preserve all 133 earlier art/audio/patch files and exact removable 0.25.1 mapping text. Keep the historical validator chain, full native/audio checks, unchanged earlier-movie regression and complete corridor-platform edge route. See docs/LEVEL6_NEXT.md. Work stays local on feature/level6-opening; main remains approved 0.24.0. No publication/merge approval is implied.

## Current repair — Level 6 ceiling and 1-up 0.25.1

- The immediate-jump recording reveals 17B4–17B7 at the upper ceiling. Their old red texture was accidental. Register their whole 2×2 native group from the existing cool rock material, keeping native hulls and normal/resume/30/31 guards.
- 164E/164F are byte-identical to approved 024E/024F. Reuse atlas 29 ivory/blue figurines in FF300036, FF221136 and FF190927; no new item art. The new movie shows and collects the ivory form; the original movie also verifies blue and dragon-form appearances.
- Preserve all 132 prior art/audio/patch files and exact recoverable 0.25.0 mapping text. The repair is a separate removable layer. Keep the complete historical validation chain, exact native/audio comparison, and original-movie regression. See docs/LEVEL6_REPAIR.md. Work remains local on feature/level6-opening; no merge/publication approval is implied.

## Current review — Level 6 opening 0.25.0

- Start from approved main f716c2a; work locally on `feature/level6-opening`. The user requests screens 1–2 with different scenery from previous red caves and an HD cape in Start. No merge/publication approval is implied.
- Use separate blue-violet ruined citadel and enclosed Gothic panoramas. Scope 9A8B/04 and 9BB7/10, plus 9CA7/0C only for the recorded outgoing-room transition. Preserve every native structural hull, blackouts, menus and spell cadence.
- Cape is lower-right, native origin (72,104), layout 0955/0954 over 0952/0951 in 0F172737. Keep origin/menu guards; the upper-right boot is already finished.
- Background bank 1700; actors 1600. Decorative wall 1734–173A and 1751–1768 clears to panorama. 1769–1774 is lava/ice, not decoration. Preserve its accepted animation frame conditions. Full normal/30/31 rendered-bank guards preserve scrolling and native flashes. No new tileNearby conditions.
- Register skull, brick and cornice as complete native unions before slicing. Preserve repeated cornice cells. Returning actors and spells use exact native-byte aliases to approved atlas cells.
- Preserve all 127 earlier art/audio/patch files and exact recoverable 0.24.0 hires.txt. Keep historical validators through a copied baseline projection. See docs/LEVEL6_OPENING.md for actual replay/edge coverage and evidence; later rooms and boss are outside this update.

## Approved main — Demonic Palace 0.24.0

PR [#27](https://github.com/kgrant191/holy-diver-hd/pull/27) merged on 2026-10-28, adopting the approved 0.23.0 late rooms and 0.24.0 finale. The pushed commit matched the approved handoff, and the merge tree matches the validated PR head exactly. PR and main builds pass; both downloaded artifacts match all 129 approved file hashes and flat install layout. Preserve all 129 reviewed installation files, including the frozen installed README. See docs/LEVEL5_FINALE_ADOPTION.md and evidence/level5_finale_adoption/ for build and artifact verification.

Next work is Level 6, the final level. Its recorded entrance and title-card transition are already covered; later rooms remain unfinished. The user may revisit some platform and main-walkway artwork later, but current graphics are approved. No release tag was requested or created. Historical pending/review labels below describe earlier delivery states and are superseded by this adoption.


## Approved continuation — 0.24.0; merge authorized

On 2026-10-28 the user approved 0.24.0, including the preceding 0.23.0 continuation, and authorized its merge. Preserve all 129 reviewed install files exactly, including the installed README. Approval bookkeeping changes source documentation only. GitHub does not yet have feature/palace-finale; source push is required before PR/build/artifact verification and merge. No further merge approval is needed.

Some platform and main-walkway artwork may be revisited later; the current graphics are approved and this does not block adoption. Next work is Level 6, the final level. Only its recorded entrance and title transition are currently covered. No release tag or GitHub Release was requested. See evidence/level5_finale/approval.json. Historical review/no-merge statements below are superseded by this approval.


## Current continuation — Palace finale 0.24.0 review

The 20261028-142617 movie supplies the remaining skull shaft, Level 5 boss, victory ascent and Level 6 threshold. This candidate fixes the shaft's moving-lift scope and remaining masonry, reuses accepted actor/HUD/effect artwork in the boss and Level 6 banks, and adds registered whole boss components and chamber ornaments. Normal scenery, Thunder flashes and victory fade phases retain their HD replacements. The final Stage 6 card clone uses an actual rendered S-tile guard instead of the early-clearing RAM render latch, fixing frame 15374 without altering card timing or native blackouts. All 125 prior art/audio/patch files and exact recoverable 0.23.0 rules are preserved.

Work is on `feature/palace-finale`, continuing the unmerged 0.23.0 candidate. Main remains approved 0.22.2. No push, PR, merge, tag or release is authorized by this request. Only the recorded Level 6 entrance is covered; later Level 6 content is unfinished. See docs/LEVEL5_FINALE.md and evidence/level5_finale/.

## Current continuation — late Palace rooms 0.23.0

- The user supplied the 20261028-125935 movie for the next screens. Work starts from approved main c1a192c on feature/palace-continuation. New work is a review candidate; no merge/publication approval is implied.
- Scope is 8AE6/mode10, 8BD6/mode04, 8C4E/mode10 and only the recorded entrance to 8D3E/mode04. Reuse approved interior/stone/lava/ice. Exact native palette roles separate distant walls from structural tiles. Both 1100/1300 copies need complete rendered guards, including accepted 30/31 flash behavior; retain blackouts and menus.
- 12E5–12F6 equals 10E8–10F9: reuse whole floating skeleton/bone poses in FF160730, FF110130 and FF0C1C30. 12B1–12C2 in 8C4E reuses the rising sentry. 12F7–12FA is a repeated two-by-two moving-lift block; register its whole unit before slicing, retaining OAM movement and the native 64x32 HD span.
- Preserve all 124 prior art/audio/patch files and exact removable 0.22.2 mappings. No new neighbor probes or native gameplay/audio edits. Keep the historical validator chain. See docs/LEVEL5_CONTINUATION.md and paired replay/edge evidence. The movie does not show the rest of the skull shaft or boss and contains no Thunder/dragon flash cast in the new rooms.

## Approved baseline — 0.22.2 on main

- The user approved the complete Demonic Palace continuation and authorized its merge on 2026-10-27. PR #26 is merged into main. The pushed source matched the approved handoff, and the merge tree equals the validated PR head. PR and main merge builds pass; both actual downloaded artifacts match all 126 approved file hashes, CRCs and flat installation layout. See docs/LEVEL5_ADOPTION.md and evidence/level5_adoption/.
- Preserve all 126 reviewed installation files, including the frozen installed README. Adoption bookkeeping changes source documentation only. This includes the green slime ceiling, recorded Palace rooms/enemies, ascent background continuity, Thunder/dragon flash repair, THUNDER H and complete 1-up palettes.
- Later Level 5 rooms and the boss beyond recorded 8A6E remain unfinished. The green upper-hall 1-up is visually verified; the lava-room item is also collected with native lives 6 to 7. No release tag or GitHub Release was requested or created.
- Start future requested changes on focused branches from approved main. Historical review and no-merge labels below describe prior delivery status; this approved baseline takes precedence.

## Current repair — Palace 1-up 0.22.2

- The user accepts the rest of 0.22.1 and reports native 1-ups in two screenshots. Preserve every existing art/audio/patch file and all recoverable 0.22.1 rules, including the flash repair.
- 104E/104F and 124E/124F equal the approved 024E/024F figurine. Add exact atlas 29 fallbacks for FF300036 (ivory), FF221136 (blue), and FF190927 (ivory during dragon form). No new artwork or native palette/gameplay changes.
- The green screenshot proves all 100 opaque native pixels and the FF190927 palette, but cannot distinguish identical physical CHR banks. Cover both. Use actual native replay/source matches and state/audio equality; do not claim live collection or a palette absent from a recorded route.
- See docs/LEVEL5_ONE_UP.md and evidence/level5_one_up/. Work remains local on feature/demonic-palace. No push, PR or merge authorized; main stays approved 0.20.5.

## Current repair — Palace flash palettes 0.22.1

- The user reports native scenery during Thunder and dragon pickup in the preview. Preserving a native flash does not permit reverting to native artwork. Previous normal-palette-only checks missed this defect.
- Clone existing scoped Palace background/foreground rules for universal 30/31, including native-neighbor palette signatures and both 1100/1300 copies. Preserve original order, masks, animation and bounds. No sprite changes.
- Flash panoramas retain original RGB with alpha 176 so Mesen blends the native flash color beneath them. Keep ordinary 0F frames exact and native blackouts inactive. Preserve all 122 earlier art/audio/patch assets and exact recoverable 0.22.0 rules.
- Test both provided movies' Thunder/pickup windows at stride 1 and show a 60 fps actual preview. Keep the historical validator chain. See docs/LEVEL5_FLASH.md. No push, PR or merge authorized; main remains approved 0.20.5.

## Current continuation — Demonic Palace 0.22.0

- The user accepted 0.21.1 artwork and supplied a new movie showing background loss and two more rooms. Preserve that art; main remains approved 0.20.5. Continue feature/demonic-palace without push, PR or merge.
- Cover the 888E/mode10 dragon stair hall and new 897E/mode10, 8A6E/mode08 lava rooms. Complete rendered normal-palette guard families cover both 1100/1300 banks; retain native blackouts and flashes. Reuse existing palace scenery, stair stone, lava/ice and every matching enemy source.
- Sprite bank 1200 needs complete conditional player/HUD aliases; broad fallbacks stay last. 12C4–E4 reuses the Level2 walking dragon; 12A4–AF the floating guardian; 12B0 its shot. Native bytes prove each alias. Only 12B1–C2 rising sentry is new art; register its whole native union and preserve repeated BE/BF cells.
- Preserve all 121 prior art/audio/patch files and exact recoverable 0.21.1 mappings; run every historical validator through baseline projection. No new neighbor probes or native gameplay/audio edits. See docs/LEVEL5_NEXT.md and evidence/level5_next/. The movie ends in 8A6E, before later rooms/boss.

## Current repair — Demonic Palace 0.21.1

- The user requests a subdued green slime ceiling and reports missing ascent backgrounds and native serpent sprites. Work continues on feature/demonic-palace from the unapproved 0.21.0 candidate; approved main stays 0.20.5.
- Ceiling art changes only 1101–04/111D–20 in cavern 850A, plus 1300 copies; keep exact masks/conditions. Preserve the floor. Register whole 32×32 ceiling groups, not a vertically squeezed strip.
- Room 8816 background guards must cover the climb. FF110130 serpent copies reuse the exact completed 10DB–E7 head/body source. Room 888E coverage is its entrance only.
- Old stair material included transparent padding. New overrides fill only that padding from the same source's stone face; preserve original opaque RGB and native masks. Native transition blackouts remain black.
- Preserve all 120 previous art/audio/patch files and exact recoverable 0.21.0 mappings. Keep every historical validator through the exact baseline projection. See docs/LEVEL5_REPAIR.md and evidence/level5_repair/. No publication or merge authorized.


## Current review — Demonic Palace opening 0.21.0

- Start from approved 0.20.5; work on feature/demonic-palace. Preserve 117 prior art/audio/patch assets and recover exact baseline mappings by stripping DEMONIC_PALACE blocks. Main remains approved 0.20.5.
- Scope is 850A/18, 8672/04, 86EA/08, 8762/04 and only the 8816/04 entry. Use native 1100/1300 bank copies and full pose-conditioned 1000 actor aliases. The movie casts Thunder twice and shows dragon transformation/flight, but does not traverse the stair hall or later level/boss.
- Skeleton shared cells and whole silhouettes stay connected. Keep independently moving worm segments and native bolt flips/footprints. Crimson column cap is 115C/D; shaft rows are 115E/F and 1160/61.
- H repair is only 0946/0F072830 in pauseMagicRow. All new neighbor probes require ordered screen bounds. No native RAM/gameplay/audio edits. Keep full historical validation through the byte-exact baseline projection.
- See docs/LEVEL5_DEMONIC_PALACE.md and evidence/level5/ for scope, actual replays and review status. No publication/merge is authorized by the level request.


## Approved baseline — 0.20.5 on main

- The user approved 0.20.5 and requested a bundle and merge on 2026-10-27. PRs #18–#25 are merged into main in dependency order. All eight PR builds and eight merge builds pass; all sixteen downloaded artifacts match their complete manifests, archive digests, CRCs and flat install layouts. See evidence/stage4_adoption/ and docs/LEVEL4_ADOPTION.md.
- Preserve all 119 reviewed installation files, including the frozen installed README. Approval/adoption bookkeeping changes source documentation only. Every merge tree matches its reviewed branch head.
- The approved baseline includes Golden Temple scenery, enemies, items, Overdrive, dragon, tower boss, all temple stair repairs and victory transition, plus the chapel branch/potion, wall-boss entrance and Poison Moss background repairs. Historical review/publication labels below describe their original delivery dates; this baseline takes precedence.
- Start future requested changes on focused branches from main. No release tag or GitHub Release was requested or created. Existing live-coverage limits remain: the temple movie acquires Thunder without casting it, and the potion cleanup did not include a dedicated collection replay.

## Current repair — background continuity 0.20.5

- In 9DEE/mode 14, ceiling tiles 074B/074C with 0F091929 were missing from the rendered (128,16) backdrop guard family. Add only those two conditions/rules, reusing the exact ruin panorama parameters and room guard. No tile artwork or neighbor probes change.
- Preserve all 117 previous art/audio/patch files and recoverable 0.20.4 mappings. Native blackouts, menus and death transitions must remain unchanged.
- The paired 2,856-frame movie restores 98 scenery frames. Native state/full audio, opaque foreground, 195 native black frames and 313 menu/title-room images remain exact. Translucent HUD edges use the unchanged source and Mesen integer alpha blend; their resulting RGB correctly changes over restored scenery. See docs/BACKGROUND_CONTINUITY.md.
- Work remains on feature/background-continuity. Main is approved 0.15.0 and 0.20.4 is the approved continuation. No publication or merge is authorized.

## Approved continuation — 0.20.4

The user approved the delivered 0.20.4 wall-boss entrance repair on 2026-10-27, then supplied a separate movie showing background dropouts. Preserve all 119 frozen installation files. Main remains approved 0.15.0; no push, PR, merge or release is authorized. See evidence/boss_entry_repair/approval.json.

## Current repair — wall-boss entrance 0.20.4

- The supplied movie proves three missing Level 2 entrance palettes in 8F7D/mode 08: 0F271027 and 0F271006 reuse the approved gold boss; 0F020627 reuses the approved normal boss. Cover every one of the 129 wall identities for each palette.
- Reuse atlas 39 directly, with b2Room/b2Lo/b2Hi. No new image or condition is needed. Preserve all 117 previous art/audio/patch assets and byte-exact recoverable 0.20.3 mappings.
- The 1,665-frame paired movie verifies all three phases, combat and boss defeat, ending before Breaker collection. All 30 changed frames are restricted to the entrance boss; native state and full audio match. See docs/BOSS_ENTRY_REPAIR.md.
- Work remains on feature/boss-entry-repair. Main is approved 0.15.0 and 0.20.3 is the approved continuation. No publication or merge is authorized.

## Approved continuation — 0.20.3

The user approved the delivered 0.20.3 branch/potion cleanup on 2026-10-27, then supplied a separate boss-entry movie. Preserve all 119 frozen installation files. Main remains approved 0.15.0; no push, PR, merge or release is authorized. See evidence/tree_potion_cleanup/approval.json.

## Current cleanup — 0.20.3

- Branch joins are chapel84C2/mode04, not the Level3 tree. Preserve native0122/0123/014D/014E and015B–015E branch strips and standing edges; only their adjacent trunk shoulders change. Use the original whole-tree source and bounded native-neighbor context.
- The potion is the handled four-cell health jug, not the two-cell HP flask. Reuse its five proven native groups with FF301116. Preserve its32×32 footprint; brighter ivory/gold edges keep the red health identity.
- The supplied1079-frame movie verifies both branch sides. The1800-frame cave regression does not contain the jug. Do not claim live potion/collection coverage or present the labeled artwork panel as gameplay. No RAM edits.
- Preserve all116 prior art/audio/patch assets and exact recoverable0.20.2 mappings. Main stays0.15.0;0.20.2 is the approved continuation. No push, PR, merge or release is authorized.

## Approved continuation — 0.20.2

The user approved the delivered0.20.2 pack on2026-10-27 and requested separate branch/potion cleanup. Preserve all118 frozen installation files during approval bookkeeping. Main stays approved0.15.0; no push, PR, merge or release is authorized. See evidence/level4_transition/approval.json.

## Current repair — all temple stairs and victory transition 0.20.2

- The user confirms the previously repaired stairs and now requests all remaining Golden Temple stair copies. Live nametables prove the ascending layout is 0B82,83 / 84,85, with exact 0D copies. Smooth that complete lower edge, preserving the entire upper half and RGB. The earlier hardcoded 83,82 / 81,80 assembly was not the actual ascending step. 80/81 and 86/87 also occur in decorative walls/windows and must not be globally restored.
- Movie10 reaches boss defeat, Thunder acquisition, dragon travel and the start of Level5. Thunder is 0E8F–92/FF301116; use the violet/gold lightning tome and exact rendered THUNDER announcement guard. The movie does not cast Thunder.
- AFA9 defeat uses hit palette0F001030, native31 flash and fade palettes0F0F0020/0F0F0F10/0F0F0F00. Clone complete tower signatures and neighbor palettes, retaining ordered bounds and native blackout. Explicit3F0F guards prevent faded art surviving into all-black frames. Reuse the accepted initial impact for byte-identical0E60–63.
- AFE5 flight changes the finished dragon to FF303030. Reuse its exact registered alpha with white RGB and preserve native flash cadence. No change to Level5 scenery.
- build_level4_transition.py adds a removable layer, atlas55 and the Thunder card; all114 previous art/audio/patch assets remain exact. Keep older validators and exact0.20.1 recovery. Native state/full audio and actual source matches are required. Main remains0.15.0; feature/golden-temple-boss is not published or merged.

## Current repair — boss entrance and stair underside 0.20.1

- The final AEF5 boss entrance uses the four-by-four 0DDF–E2 / 0D5B–68 crown and six blank rows beneath it. Earlier interior clones cleared the crown and opening. Restore the existing entrance crown and dark opening only in AEF5, in palettes 0F172737/0F071723. The lower two opening rows use 0F071723. Bounds must precede all upward tileNearby probes.
- Smooth only the reported descending 0B7C–7F / 0D7C–7F step family. Preserve the full upper half, standing edge and exact stone RGB. The continuous lower diagonal supersedes the historical jagged native alpha requirement for this family. Other stair shapes remain unchanged.
- build_level4_finish.py adds atlas54 and 144 removable overrides. All113 earlier art/audio/patch assets stay exact; stripping TEMPLE_FINISH recovers exact0.20.0 mappings. Keep every older validator.
- Use paired actual recordings and the existing controller-only stair edge route with verify_level4_finish.py. Native state and full audio must match; boss-room images remain exact. Source branch stays feature/golden-temple-boss, main0.15.0; no publication or merge authorized.

## Current continuation — Golden Temple finale 0.20.0

- AE41 and AEF5/mode0C are indoor halls. Clone the complete repaired AC61 scenery into physical bank0D, including stair repairs and decorative-column removal. Return the finished0C sentinels, drops and HUD. Do not redraw accepted scenery.
- AFA9/mode04 is the boss interior. The tower is background bank0F: three independently rotating7x4-cell bands, eight native layouts. Register each whole112x64 band before slicing; shared identities must not splice eyes from different phases. Preserve normal0F071727 and hit0F001030 timing. All tileNearby probes require ordered screen bounds.
- Actor/HUD bank0E00–74 equals0A00–74. New conditional aliases precede existing ordinary rules; broad aliases remain last. Native0EB4–B7 moving ledges reuse complete64x32 accepted stone.0CB6–BD rings use two complete32x32 poses with one scale.
- Reuse the existing interior panorama at half brightness in the boss room, with rendered guards that retain native transitions and death blackouts. Graphics only; never edit emulated RAM, input, collision, timing or audio.
- Branch feature/golden-temple-boss starts at frozen0.19.1. Preserve all112 earlier art/audio/patch assets and exact recoverable mappings. Main remains approved0.15.0; last explicit Level4 approval0.16.3. No push, merge or release authorized. The supplied7591-frame movie ends at game over, not boss defeat. See docs/LEVEL4_FINALE.md and paired evidence.

## Current repair — stray ornament 0.19.1

- The reported purple/ivory bars are background0DF8/0F073703 in ACD9/mode18, not a dragon sprite or ring enemy. The earlier pillar cleanup missed this ornament cell. build_level4_residue.py adds only two arena/palette-scoped empty mappings, including31073703 for native pickup flashes.
- Reuse atlas50's empty16x16 cell. Preserve all112 earlier art/audio/patch assets, every other mapping and the native flash/menu sequence. Never globally clear F8 or the ring enemies.
- Require paired actual replays with verify_level4_residue.py: native state/full audio exact, every changed pixel confined to F8 and equal to the existing panorama. Main/approval status unchanged; no publication authorized.

## Current continuation — dragon/items 0.19.0

- Both 20261026-202217/202440 states start in ACD9/mode18 before the dragon pickup. Native pickup is0CB1–B4, form0C94–AF, shot0CB0, star0C74. Three observed whole112x48 layouts share exact cells. Native mirrors, movement, blinking and timing remain authoritative; no RAM edits.
- Thin outdoor columns0B03–0B39 plus exact copied capitals are decorative. Clear only proven scoped rules and their courtyard/arena clones. B78–7B are physical masonry; B7C–87 include stairs. Do not clear those families.
- Form uses FF190927, pickup/fire FF301116. Keep native31 universal-color flash: HD foreground aliases retain bounds before neighbor probes, with no full-color panorama during the flash.
- Brighter staff remains16x32 with the identical menu source. Small heart/magic overrides are scoped to the seven recorded temple rooms; preserve earlier conditional mappings. All111 earlier installed art/audio/patch files stay byte-exact.
- Candidate branch feature/temple-dragon-items starts at frozen0.18.0. Main remains approved0.15.0; last explicit Level4 approval0.16.3. No publication or merge authorized. See docs/LEVEL4_DRAGON.md and paired evidence.

## Current continuation — staff hall and outdoor arena 0.18.0

- AC61/mode04 is indoors through the staff climb; ACD9/mode18 is outdoors. The recording ends with player death, not sentinel defeat. Do not claim victory or later-room coverage.
- AC61's former single entrance-view guard fails while scrolling. Cover recorded rendered identities/palettes, while retaining menus and native transitions. Upper statue palette is 0F172737. Decorative B80/B81 in 0F071727 are wall details; physical stair families remain untouched.
- ACD9 uses physical background bank0D, byte-identical to0B. First-byte-match CHR inventories cannot distinguish them. Clone complete final scenery rules with 0D tile/neighbor identities, preserving bounds before probes. Actor bank0C00–74 equals0A00–74; clone spriteNearby pose signatures too and append aliases after all earlier specific rules.
- Staff pickup0A95/96 is16x32 HD; menu0956/0968/0969/096A composes32x32 with the same staff centered. Exact menu origin guards prevent common glyph0956 from changing elsewhere.
- Register each whole96x96 sentinel before slicing. All native shared cells remain exact across four layouts; preserve OAM mirrors, native decoys and hit palettes. No RAM edits. See docs/LEVEL4_STAFF.md, prepare_level4_sentinel.py and paired evidence.
- Review branch feature/golden-temple-staff starts from frozen0.17.0; this does not record whole-pack0.17 approval. Main remains0.15.0; last explicit Level4 approval is0.16.3. All earlier110 assets remain byte-exact. No push/PR/merge/release authorized.

## Current continuation — Golden Temple courtyard 0.17.0

- AAF9/mode08 is indoors; AB71/mode10 is outdoors; the recorded AC61/mode04 re-entry is indoors. The rest of AC61 is not traversed. Clone final 0.16.3 rules, including ordered bounds and stair repairs, rather than the original 0.16.0 builder.
- Room palettes distinguish decoration from physical cells: AAF9 0F071723 windows reuse staircase patterns. These are decoration; 0F172737 is the recorded solid palette. AB71 clouds/fences are decoration; native 0B92–0BA1 forms the four-by-four statue.
- Wings are 0A92/0A93 in a 32x16 HD footprint; eight byte-identical banks are proven. Fire-chain beads are 0AE1/FF162830, each independently moved by native OAM. Never replace the whole moving chain with a static ring.
- New atlas50 leaves every earlier asset unchanged. Keep exact recovery of 0.16.3 and all older validators. Work remains pending review, no merge or release authorized.

## Approved continuation baseline — 0.16.3

- On 2026-10-26 the user accepted the delivered repair ("ok good") and requested the next recorded rooms. Preserve all 111 installed files as the reviewed baseline; approval bookkeeping must not alter the frozen installed README. Main remains 0.15.0; no push/merge/release is authorized. See evidence/level4_stairs/approval.json.

## Current stair repair — Golden Temple 0.16.3

- The supplied 20261026-181741 state proves 0B7C–0B7F are descending stairs, not decoration. build_level4_stairs.py overrides the erroneous clear rules with 24 room/palette mappings. Preserve their native top surface and joined sloped underside. Do not apply the historical scenery classification to these cells.
- Reuse existing stone RGB; preserve every 0.16.2 asset and its neighbor bounds/pickup fixes. The additional atlas is index49. Opposite-facing 0B80–0B87 remain exact.
- Require paired save-state movement and full-movie checks through verify_level4_stairs.py, with native state/full audio equality and stair-only image differences. See docs/LEVEL4_STAIRS.md. Candidate is unapproved on feature/golden-temple; main remains 0.15.0.

## Current repair — Golden Temple 0.16.2

- The user reports old small drops outdoors and a crash entering the temple. The diagnostic catches a stock Mesen tileNearby read at index61440 (one past the screen) on entry. Do not call the earlier successful uninstrumented replay proof of memory safety.
- build_level4_repairs.py bounds all new pillar neighbor evaluations, including inverted checks, while preserving off-screen/no-neighbor behavior. Keep the exhaustive bounds regression in validate_pack.py. Do not ship or require the diagnostic observer.
- Reuse exact atlas25 heart/crystal pixels for byte-proven pickup aliases; earlier conditional/menu rules retain priority. Every 0.16.1 image/audio/patch file stays exact. See docs/LEVEL4_REPAIRS.md and evidence/level4_repairs/.
- 0.16.2 remains a review candidate on feature/golden-temple. Main stays approved 0.15.0; no merge/release authorization is implied.

## Current revision — Golden Temple 0.16.1

- The user accepted the 0.16.0 backgrounds and outdoor fluted columns, but rejected its square slabs and indoor block-stack supports. Preserve those accepted assets exactly; this is partial art acceptance, not whole-pack approval.
- build_level4_masonry.py adds atlas48 and scoped overrides after the unchanged 0.16.0 builder. Solid blocks use the native staggered four-by-two layout. 0B4E–0B51 are confirmed destructible blocks; 0B78–0B7B are indoor structural columns with contextual caps/bases. Keep 0B4A–0B4D cleared as nonsolid scenery.
- Preserve all 107 earlier art/audio files, actors, Overdrive/menu fixes, and native gameplay/audio. Existing stair masks remain exact. Source/evidence: docs/LEVEL4_MASONRY.md, art/level4_masonry/, evidence/level4_masonry/. concept_only.png is generated design reference, never runtime evidence.
- 0.16.1 is awaiting review on feature/golden-temple. Main remains 0.15.0; no push/merge/release is implied.

## Current review — Golden Temple 0.16.0

- Work is on feature/golden-temple from approved main 2f38abeb. The user requested an outdoor first area, indoor next area, corrected Overdrive spelling and updated spell graphics. The 109-file candidate is awaiting review; do not merge or label approved.
- Scenery scopes: mode1C/A865 outdoors, mode08/AA09 and mode08/AA81 indoors. Keep rendered guards including 0F071723 at frame6500. Background priority1 stays behind actors. Preserve native collision contours and continuous shafts.
- The actual Overdrive cast is 0A8A–0A8D, an orbiting orb, with ten CHR-proven bank copies. Select enables selected magic. 088B–088E is the acquisition orb; CB–CF is the gargoyle crescent attack, not the player spell.
- Preserve all 104 previous art/audio files and exact recoverable 0.15.0 mappings. New scope/provenance/evidence: docs/LEVEL4_GOLDEN_TEMPLE.md, art/level4/, evidence/level4/. The source handoff is a ZIP-wrapped incremental bundle. Later temple areas/boss remain untested.

## Approved baseline — 0.15.0 on main

- The user approved 0.15.0 and authorized all five Level 3 merges on 2026-10-26. PRs #13–#17 are merged into main in dependency order. All PR/main builds pass, and all ten downloaded artifacts match their frozen hashes and flat install layouts. Preserve all 106 reviewed installation bytes, including the historical installed README. See evidence/level3_finale/approval.json and evidence/stage3_adoption/.
- Next area: Level 4 / Golden Temple. Start a focused branch from approved main. Stage 4 scenery remains unfinished; only its title card and the recorded initial arrival are covered. Historical sections below retain their original delivery-time labels; this baseline takes precedence.
- Final climb 9F1A / boss 9F92 use mode 04. Reuse exact approved moss terrain and native contours. The pink head uses twenty cells in a 64×96 footprint; each entire curved shot fits its staggered native cell union. Preserve native OAM flips, occlusion, emergence and defeat removal.
- Boss heads carry NES behind-background priority. The ruin panorama must use background priority 1, behind those sprites; native living growths remain in front. Normal backdrop guards must include the organic ceiling cells. Native universal-color flashes remain visible.
- Preserve all 102 previous art/audio assets and exact recoverable 0.14.0 mappings. Add shared native-byte-proven 0800/0A00 actor aliases after the existing specific mappings. Preserve the 56-byte entrance IPS and native audio.
- Overdrive is the native four-tile orb 088B–088E. Stage 4 card uses palette 0F131C29; reuse the approved card sources. Stage 4 scenery is outside this change. Cards 1–4 are now live-verified; cards 5–6 remain unverified.
- Evidence and precise limits: docs/LEVEL3_FINALE.md, evidence/level3_finale/. The five Level 3 branches are merged. Future merges require user authorization; no release tag is requested.

Read README.md, STATUS.md, docs/ART_DIRECTION.md and docs/TESTING.md before changing the project. Update STATUS.md and CHANGELOG.md when work changes the approved build or leaves a concrete follow-up.

## Approved Poison Moss Land continuation — 0.14.0

- Work is on `feature/poison-moss-land`, based on 0.13.0 at 06a53b9. The user explicitly requested a greener Level 3 distinct from the reused caves/rocks. This direction supersedes the historical Level 3 brown/cave reuse instructions below; Stage 1/2 remain unchanged.
- `build_poison_moss.py` runs after shared fallbacks and inserts its scoped overrides before existing mappings, preserving original priority. Three newly painted sources supply a moss forest, overgrown Gothic ruins and green masonry. Preserve every terrain alpha contour and all original native guards, including solid supports 0796/0797. Preserve continuous oak overlays and branch wood.
- All 99 prior art/audio files and all fish mappings remain exact. Only Level 3 scenery references change, plus installed README. Removing the marked overrides and reversing recorded background substitutions must recover exact 0.13.0 hires.txt.
- The user approved the complete delivered 0.14.0 pack on 2026-10-26. Preserve all 104 reviewed installation files exactly for approval bookkeeping; keep installed README frozen. Main remains 0.10.2. This is the continuation baseline, including previous Level 3 work and fish corrections. See evidence/poison_moss/approval.json and docs/POISON_MOSS.md.

## Previous Level 3 caves review — 0.13.0

- Work is on `feature/level3-caves`, based on review 0.12.2 at fb1fb4d. The user still saw fish shaking in the next room, where several fish appear together. 0.12.2's one-fish/one-room guard was insufficient.
- `build_big_fish_motion.py` now registers each complete fish independently at its native player-relative horizontal hover equilibrium. Match the actual tile origin; preserve the stock Mesen 2.2.1 mirrored-origin workaround pairing originPositionCheckX with positionCheckX. An origin-only mirrored guard changes isolated pixel stripes and is incorrect. Do not change native movement, hit blinking or source poses. Partly clipped boundary sprites retain original registration.
- `build_level3_caves.py` covers room pointers 9B96, 9C86, 9CFE and the recorded beginning of 9DEE, with modes 10/04/10/14. Inventory all four PPU nametables: the vertical room uses the second vertical page. Native 0796/0797 with 0F0A1A29 in 9CFE/9DEE are solid supports, not removable decoration; only the measured 9C86 dark wall palette is decorative.
- Reuse approved cave, brown rock, carved stone, lava/ice, bats and blade rings. The green floating creature is the only new painted source; its twelve-cell 64×64 footprint and missing upper-left/lower-right cells are preserved. All 98 previous art/audio files remain exact.
- This is unapproved. Main 0.10.2 and approved continuation 0.11.2 remain pinned. See docs/LEVEL3_CAVES.md and evidence/level3_caves/.

## Previous large-fish hover review — 0.12.2

- The user's new movie demonstrates native horizontal hover oscillation in the large fish without damage. 0.12.1 repaired a separate small-fish color problem; do not claim it addressed this report.
- Keep the original painted fish and native gameplay exact. `build_big_fish_motion.py` adds ±1 HD-pixel registrations only for the measured one-fish hover/cruise state in room 9AA6. Preserve both mirrors, original fin/vertical motion, attacks and hit blinking. Multiple-fish ambiguity falls back to original art.
- Do not shift individual limbs or redraw the fish. The complete 48×48 source shifts together inside its measured margin, with no clipping. Original atlas cells remain exact; the twenty new cells occupy X0–319/Y496–511.
- See docs/BIG_FISH_MOTION.md and evidence/big_fish_motion/. 0.12.2 is unapproved; main 0.10.2 and approved continuation 0.11.2 remain pinned.

## Previous small-fish motion review — 0.12.1

- The user clarified motion blur/glitching, not a request to sharpen or redesign the fish. Preserve original generated art, both large poses and the first small pose. The small alternate pose now shares the base palette and static head/body pixels. Keep reserved atlas slots so all existing mappings stay exact.
- Native large-fish hit blinking is present in OAM and must remain. Do not describe generic alternate-frame flicker as an HD mapping bug. Capture consecutive frames for motion defects; stride two cannot reveal every alternating phase.
- See docs/FISH_MOTION.md and evidence/fish_motion/. 0.12.1 is unapproved, based on review 0.12.0; 0.11.2 remains the approved continuation baseline. Main is 0.10.2.

## Previous Level 3 lava review — 0.12.0

- Work is on `feature/level3-lava`, based on approved `feature/level3-opening` at 9eb0678. The new corridor, menu boot, fish and Breaker casts are a review candidate, not approved. Preserve the frozen 0.11.2 manifest; main remains 0.10.2. See docs/LEVEL3_LAVA.md.
- Lava room scenery is limited to RAM mode 10 / room 9AA6 and exact hot/ice palette guards. Menu boots are background IDs 0971–0974; reuse the approved collectible art. Small unflipped fish point right; native OAM mirroring makes the left-moving form face left.
- Breaker uses 0675–0689 (charge, horizontal release/bolts, upward release/bolts) and twelve proven identical bank copies with both FF221136/FF300036 palettes. Preserve native OAM flips, timing, MP costs and stair destruction.
- Runtime changes from 0.11.2 are hires.txt, README.txt and one new Stage3_Lava_Tiles_2x.png atlas. All 97 other approved runtime files stay exact. Shared Stage 2 fallback remains last.

## Approved Level 3 continuation baseline

- The user approved 0.11.2 on `feature/level3-opening` on 2026-10-25 (America/New_York), saying "approved". Preserve all 99 reviewed installation files exactly. This is the continuation baseline; main remains at merged 0.10.2 pending the source push, PR and merge. See `evidence/level3_detail/approval.json`, `docs/LEVEL3_DETAILS.md` and the paired live evidence. Approval bookkeeping changes source documentation only; keep the installed README frozen.
- Preserve the complete native wood masks, including partially visible top-row cells. The reported round shot is 0694/FF301116; 068A–068D/FF301525 form the boot collectible (not Randy’s boots). The 0.11.1 attribution of 06B6–06B9 as the reported projectile was incorrect. Preserve those historical sprites pending a separate identification; do not use them to claim round-shot coverage. Branches 0768–0770 use complete two-row registration with exact native alpha contours.
- The `.mmo` input embeds the correct starting state and matches the project's ROM. Use `run_mesen_movie.py` with the stock MesenCE 2.2.1 native core, configuration shim and synchronized screenshot observer. Do not replace it with MesenAI. Input bytes remain outside Git.
- NES endFrame fires before video submission; asynchronous HD decode can otherwise produce a one-frame capture mismatch. `sync_movie_capture.cpp` waits for the pending decode and then calls the original screenshot routine without changing pixels or native state.
- New Level 3 scenery rules are limited to the three measured room pointers; actor aliases use proven native CHR copies. Preserve original conditional priority and the last shared Stage 2 fallback block.

## Approved latest repair

- The user approved 0.10.2 and authorized its merge on 2026-10-24 ("approved. merge it"). PR #12 is merged; main is the approved 0.10.2 baseline. The repair keeps HD Randy through the three final Breaker pickup fades. Preserve all 93 reviewed installation bytes. Approval and artifact records are in `evidence/breaker_randy/`. See `docs/BREAKER_RANDY.md` and `evidence/breaker_randy/validation.json`.

## Approved main and source history

- Approved continuation baseline: **0.10.2 on `main`**. The user approved the delivered boss and defeat/pickup repairs on 2026-10-24; see `evidence/boss2_review/approval.json`. Preserve all 93 reviewed installation files exactly, including the original brown ceiling, accepted stairs and shared Stage 2 artwork. PRs #8–#11 are merged into main after the user authorized all four merges.
- The current source handoff includes `feature/screen2-4`, `feature/screen2-5`, `feature/screen2-6` and `feature/2-boss`. Older refs stay at their earlier source commits; screen2-6 includes the 0.9.0 approval record. No release/tag is requested. Boss artwork is approved; PRs #8–#11 merged in dependency order (screen2-4 → screen2-5 → screen2-6 → 2-boss), retargeting each successor to main. PR/main builds and all downloaded artifacts pass. See `evidence/stage2_adoption/merges.json` and the four `main_artifact.json` records. The 0.10.1 repair covers both gold defeat-fade palettes and removes the dead boss silhouette during Breaker flashes; preserve the native room flash.
- Finished artwork must be reused for matching native identities/palettes. `build_shared_stage2.py` appends fallbacks after all specific rules; the Poison Moss postprocessor preserves that priority. Verified new-bank aliases retain pose conditions; put broad aliases after existing specific rules. Never globally clear scenery. See `docs/SCREEN2_6.md` and `docs/BOSS2.md`.

## Preserve approved behavior

- Current approved development version on main: 0.10.2. Includes all approved Stage 2 work through the boss and Breaker fixes, plus the Stage 2 cave/lava flow (PR #6) and vertical cave with blue eye tears (PR #7). The user explicitly authorized both merges on 2026-10-24 ("merge it"); both are merged. PR/main Actions builds and actual downloaded 84/85-file artifacts were verified. See STATUS.md and evidence/screen2_3_review/approval.json. Imported artwork baseline: historical v15.1. Preserve approved artwork and native gameplay except for the user's requested change.
- Preserve the title sequence: clean splash, first Start reveals PRESS START, second Start starts play. Preserve the exact Entrance_SFX_Priority.ips bytes.
- Randy's normal/Twin Fire art is shared across matching native identities. Fix shared assets/mappings where appropriate instead of adding needless room-specific copies.
- The red winged-skull drop is a bracelet. Its collected Start/pause-menu icon must use the same bracelet artwork.
- Preserve native collision, animation timing, inventory, lives and audio. Use controller input for visual tests; do not patch RAM to fabricate evidence.
- Pose-specific hires.txt rules precede broader rules: Mesen uses the first matching replacement. Preserve native per-sprite flip behavior and OAM footprints.

## Build and verification

- Python 3.12; install requirements.txt. Run `python build.py` and `python scripts/verify_release.py` against the approved pack manifest.
- For visual changes run relevant live Mesen replays and inspect actual captures in both directions and affected palettes. Atlas mockups alone are not evidence of runtime correctness.
- For limb repairs, inspect the whole joint and silhouette against a clear backdrop. Alpha connectivity and pixel-exact rendering alone missed the rejected 0.3.3 knee/shin break; register adjoining limb sections together and check their outline across tile boundaries.
- For platform artwork, test the complete span, far-left stop, and slow walk-off at the right edge. A grounded sprite can overhang collision tiles; do not extend solid artwork to the full OAM or boot silhouette.
- Perform routine emulator testing here when inputs/tools are available; do not ask the user to perform it instead.
- Only one Mesen process at a time. Do not replace its pack or overwrite the audio-capture library during a run.
- The first screenshot after loading a state can be empty. endFrame OAM can describe the next pose; screenshots are authoritative for visual claims.
- Report coverage precisely. Stage cards 1–4 are verified in live play; cards 5–6 remain mapped but untested.
- Review and document intentionally changed files before updating expected hashes; do not weaken validation merely to make it pass.

## Repository workflow

- Keep main as the approved baseline. Use focused branches for later changes unless the user directs otherwise. Preserve unrelated work.
- Use this chat for bugs, priorities and approvals. Do not introduce GitHub Issues or a TASKS.md backlog unless requested. Push changes on the requested branch and open a PR for review; merge only after user approval.
- For artwork-heavy changes, prepare a ZIP-wrapped incremental Git bundle and exact fetch/push commands. The user pushes with their local Git credentials; use the GitHub integration for PRs and Actions. Avoid transferring large encoded images through tool arguments or chat. Small text-only changes may use the integration directly.
- Actions artifacts are development test builds. Publish release tags or GitHub Releases only when explicitly requested; reserve the completed release for 1.0.0.
- Upload the extracted pack contents to Actions artifacts, never a ZIP inside the artifact ZIP. One extraction must expose hires.txt and the installable assets.
- Follow semantic versioning in docs/REPOSITORY_WORKFLOW.md. Keep VERSION, INSTALL.txt, README.md, STATUS.md, CHANGELOG.md and approved pack hashes consistent when approving a new version. Reserve 1.0.0 for the completed, tested game pack.
- Commit source art, mappings, scripts, compact evidence and notes. Exclude ROMs, emulator binaries, savestates, credentials, raw frame dumps and build archives.
- Local test-input names/checksums are in test_states/README.md; input bytes are ignored by Git.
- Existing rollback folders are build inputs and provenance. Do not delete them until their consumers have deliberately been migrated.
- CI validates/builds without a ROM. Live emulator review remains separate for visual work.
- User instructions and authorization in the active conversation take precedence over these defaults.
