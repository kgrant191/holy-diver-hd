# Level 6 skull corridor — 0.26.0 review

The next recorded corridor now continues the enclosed blue-violet citadel, with existing dark stone, hanging edges and ivory skull blocks. HD Randy, HUD, flying skulls and all four silver armored-sentinel poses follow the new actor bank. Two new bronze crawler poses appear at the following room's entrance.

This local review candidate continues `feature/level6-opening` from 0.25.1 commit `36446e22eff73aaee93839d0ac1dea420544ccb2`. Approved main remains 0.24.0. No push, PR, merge, tag or release is part of this delivery.

## Scope and implementation

The movie traverses 9F3B/mode10 and shows only the entrance of A02B/mode04 before pausing. The rest of that room, later Level 6 rooms and the final boss remain unreviewed. Both indistinguishable physical background copies 1700/1900 receive the complete normal/resume/30/31 guards and native foreground masks. No new background-neighbor probes are added.

The removable LEVEL6_NEXT layer adds one 256×256 atlas, 13,230 tile rules and 36,864 background guards. All 133 earlier art/audio/patch files remain byte-identical; removing its four marked sections recovers exact 0.25.1 mappings. The existing enclosed panorama and flash variant are reused directly.

New corridor stone is registered as six complete native groups before slicing, with exact existing material RGB and native filled hulls. Returning 1800-bank Randy/HUD/effect rules retain their original priority and remapped sprite-neighbor signatures. Native byte equality proves reuse of 18A9–DD silver sentinels, 18DF–E6 flying skulls and 18F9 round shots. 18EB/FF000F30 is a different native one-cell projectile pattern; it reuses the same finished fireball artwork without claiming byte identity.

The new crawler is 18E7–F2/FF072630. Its 48×32 resting and 64×32 leaping sources fit the measured native cell unions. A smooth whole-image registration preserves its tail/claw around missing corner cells; no opaque source pixels are cut from the registered body. 18EB has a separate palette-specific body mapping here. The built-in image-generation source and exact prompt are in `art/generated/level6_crawler.png` and `level6_next_prompt.json`.

## Actual replay verification

Stock MesenCE 2.2.1 replays the unchanged 2528-frame user recording at stride one. All RAM, PPU, OAM, scroll/view metadata, APU writes and full PCM audio match 0.25.1 exactly. Of 2527 nonempty screenshots, 1808 show the intended new scenery/actors and 719 are identical. All 537 menu frames and 104 native black frames stay exact. Every changed gameplay image has over 101,000 exact panorama pixels; no background dropout is found. Three pause boundaries display the outgoing scene while endFrame RAM already names the menu; each is explicitly recorded.

Complete actual source matches verify all six terrain units, skull blocks, four sentinel poses, both flying-skull poses and both crawler poses. All sentinel and flying-skull poses also match their complete mirrored sources. The supplied route contains no Thunder or dragon-flash cast in these new rooms; their aliases and flash backgrounds are statically verified. The whole movie was captured before correcting one noun in README.txt; the retained capture note documents that exact difference. Every installed runtime byte matches the delivered pack. The edge route and original-movie regression use the final complete manifest.

The controller-only 1766-frame edge route retains the embedded state and the first 1400 original input frames. Randy stops at world (527,144) for 60 frames, then crosses the platform slowly without jumping. Native solid bounds remain X528–672, top Y160. Falling starts at frame 1690, world (680,144), with the first descent at 1694, world (684,145). All 367 consecutive captured native samples and full audio match. The complete 288×160 HD platform matches its assembled source in 151 images. Native sprite overhang is preserved without extending the art into the pit.

The stock-core neighbor observer is active in all new captures; no invalid-read abort occurs. The original 6427-frame Level 6 regression also matches all native state and complete audio; all 6426 nonempty screenshots remain pixel-identical. An isolated clean build passes the complete historical validator chain, all 136 file hashes and independent flat-ZIP CRC/member checks. Build and archive results are recorded in `evidence/level6_next/build.json` and `build-validation.txt`.

## Reproduction

Use the existing `run_mesen_movie.py`, stock core, synchronized screenshot/audio observers and the supported translated ROM. Freeze each installed pack and run only one emulator at a time. Replay the new movie and original 6427-frame movie at stride one, then:

```sh
python scripts/verify_level6_next_replay.py --before /captures/new-before --after /captures/new-after --out /captures/replay.json
python scripts/verify_level6_next_replay.py --before /captures/original-before --after /captures/original-after --out /captures/regression.json --regression
python scripts/make_level6_next_edge.py --movie '/inputs/Holy_Diver_HD(20261029-181929).mmo' --out /inputs/edge.mmo
# Replay the generated route against both packs, stride 1, capture-start 1400.
python scripts/verify_level6_next_edge.py --before /captures/edge-before --after /captures/edge-after --out /captures/edge.json
python build.py
python scripts/verify_release.py
```

[Actual before/after views](../evidence/level6_next/comparison.png). The review video is the complete actual new movie at native NTSC cadence with original game audio; only the initial empty screenshot is omitted. Source excludes the ROM, emulator, save state, movie inputs and raw capture dumps.
