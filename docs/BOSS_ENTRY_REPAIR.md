# Level 2 wall-boss entrance — 0.20.4

The user approved the complete 0.20.3 pack, then supplied a 1,665-frame movie showing the Level 2 wall boss reverting to original artwork during entry. Approval is recorded in `evidence/tree_potion_cleanup/approval.json`; the 119 installed baseline files are frozen. This repair is on `feature/boss-entry-repair`. Main remains approved 0.15.0. No push, PR, merge, tag or release was performed.

## Cause and repair

The recording starts in room 8E8D, enters boss room 8F7D/mode 08, opens the menu, fights and defeats the boss, and ends before collecting Breaker. Existing mappings cover the ordinary, hit and defeat palettes. Three additional entrance palettes had no corresponding HD boss mapping and therefore showed the original NES image for 30 frames.

| Native entrance palette | Approved artwork reused | Observed repaired frames |
| --- | --- | --- |
| 0F271027 | Gold hit, 0F270027 | 22 |
| 0F271006 | Gold hit, 0F270027 | 4 |
| 0F020627 | Normal, 0F121626 | 4 |

`build_boss_entry_repair.py` adds 387 aliases: all 129 boss cells for each missing palette. The exact existing room guard limits them to 8F7D/mode 08. The two warm flashes use the accepted gold presentation; the colored phase uses the accepted normal presentation. No new art, conditions, neighbor probes, timing hooks or RAM edits are introduced. Every alias points directly to the existing atlas 39 coordinates.

Removing the single marked block recovers byte-exact 0.20.3 mappings. All 117 previous art/audio/patch assets stay exact. Only `hires.txt` and installed `README.txt` differ in the 119-file install pack. The earlier branch/potion cleanup and all other stages retain their approved pixels.

## Verification

The stock MesenCE 2.2.1 core replayed the unchanged supplied movie with both the approved and repaired packs, capturing every frame. All 1,665 RAM, PPU, OAM and view samples per type match. APU writes and all 5,325,360 PCM bytes match exactly. The first screenshot is empty in both runs; 1,634 rendered images are identical, including eight native black frames. All differences occur in the 30 entrance frames between 91 and 220, exclusively within the boss's native cells.

Every changed picture matches the complete visible approved boss source after accounting for camera scrolling and native sprite occlusion. Transparent source regions expose exact existing cave pixels or native black, with no leftover original boss fragments. All three missing palettes are live verified. Combat, the menu, defeat and the uncollected Breaker scene remain pixel-identical. The movie does not cover Breaker collection or the next level.

`python build.py` retains every older validator; `verify_boss_entry_rules.py` additionally verifies all aliases, scope and exact baseline recovery. `verify_boss_entry_replay.py` performs the paired native/audio, changed-region and whole-source checks. The expected candidate manifest is `evidence/0.20.4-pack-sha256.json`; the historical `approved-pack-sha256.json` filename describes this tested candidate, not user approval. The install ZIP has a flat layout and its payload hashes and CRC are checked.

The preview uses real before/after replay captures, first at normal speed and then with the entrance replayed at half speed. No synthetic gameplay frames are used. The source handoff includes the five cumulative Level 4 refs, the approved tree/potion cleanup ref and this repair ref, against main 2f38abeb. ROM, savestates, movie bytes, emulator binaries and raw frame dumps are excluded.
