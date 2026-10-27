# Poison Moss background continuity — 0.20.5

The user approved the complete 0.20.4 pack, then supplied a movie showing background dropouts. Approval is recorded in `evidence/boss_entry_repair/approval.json`; all 119 installed baseline files are frozen. This repair is on `feature/background-continuity`. Main remains approved 0.15.0. No push, PR, merge, tag or release was performed.

## Cause and repair

The 2,856-frame recording explores the Poison Moss Land lava corridor, room 9DEE/mode 14. It includes horizontal movement in both directions, several Blizzard casts and menu visits, player death and restart. The existing scenery guard checks the native rendered background tile at screen position (128,16). Its ceiling family included 0744–074A but omitted 074B and 074C in palette 0F091929. As those ceiling tiles cross the probe, the panorama disappears even though gameplay continues.

`build_background_continuity.py` adds the two missing rendered-tile conditions and two background rules, with the existing exact room guard. Both reuse `Poison_Moss_Ruins_Background.png` at its original brightness, camera factors, offsets and priority. No tile replacements, new images, native-neighbor probes or emulated-state changes are introduced. The actual rendered palette guard continues to distinguish normal scenery from menus, death transitions and native spell blackouts.

Removing the single marked block recovers byte-exact 0.20.4 mappings. All 117 previous art/audio/patch assets remain exact. Only `hires.txt` and the installed `README.txt` differ in the 119-file pack. Existing scenery and actor art are retained.

## Verification

The stock MesenCE 2.2.1 core replayed the unchanged supplied movie with both packs, capturing every frame. All 2,856 RAM, PPU, OAM and view samples per type match. APU writes and all 9,130,300 PCM bytes match exactly. The first screenshot is empty in both runs. Of the remaining images, 98 restore missing scenery and 2,757 are identical. All 195 fully black native frames and all 313 menu/title-room images remain exact.

The repaired intervals are frames 259–274, 381–397, 454–469, the nonblack alternating spell frames 591–629, and 1161–1189. Every changed image has a measured 074B/074C signature beside its capture time. Restored background pixels match the unchanged panorama exactly. The 374 changed translucent HUD-edge pixels match Mesen's exact integer alpha compositing of the unchanged HUD source over that panorama. All opaque foreground pixels remain unchanged. Later combat, death and restart images are identical to the baseline.

`python build.py` retains every previous validator. `verify_background_rules.py` additionally checks exact baseline recovery, room scope, two guard identities and unchanged assets. `verify_background_replay.py` checks native state, audio, exact panorama pixels, HUD compositing and preservation of native blackouts. The expected candidate manifest is `evidence/0.20.5-pack-sha256.json`; the historical `approved-pack-sha256.json` filename describes this tested candidate, not user approval. The install ZIP has a flat layout with checked CRC and payload hashes.

The preview contains actual paired captures of forward scrolling and the return pass, with the latter labeled half speed. No synthetic gameplay frames are used. Coverage is the supplied corridor movie, not all possible routes in the game. The source handoff carries the five cumulative Level 4 refs, tree/potion cleanup, wall-boss repair and this background repair against main 2f38abeb. ROM, savestates, movie bytes, emulator binaries and raw frame dumps are excluded.
