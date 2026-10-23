# Blizzard transition repair — 0.3.2 candidate

The user confirmed the fireball repair and reported stray-looking imagery on the left during the Blizzard transition, plus Randy briefly reverting to the original sprite before the announcement. This repair remains on `feature/1-boss`; main stays approved 0.2.1.

## Findings and changes

A no-HD replay of the same controller route confirms that the original transition repeats the bell room, including its bell and gold ornaments, while scrolling upward. The HD nave panorama was only one screen high. Once scrolling passed its lower edge, the replacement backdrop became black while the native foreground continued scrolling. The missing wall made the foreground decorations appear detached and pop back into scenery at the wrap.

`Blizzard_Ascent_Background.png` repeats the approved 1536×480 nave panorama three times vertically. The bell-room background rule selects this 1536×1440 image, covering both native nametables plus the viewport. The boss hall keeps its existing background. No approved masonry pixels are redrawn, and no original bell, ornament, platform or scroll is removed. This also fills the exposed backdrop during entry into the bell room.

Randy's last fade occurs before the CHR-bank switch: it still uses bank 00 and room pointer `$0078/$0079 = B2/85`. The initial white palette was mapped, but the following `FF202020`, `FF101010` and `FF000000` palettes had mappings only in announcement bank 1E. Those final 24 frames therefore used the original NES silhouette. The repair adds the three bank-00 palettes, gated by the bell-room identity and the existing pose signatures. They retain the approved silhouette at RGB intensity 255, 173 and 102. Native full-screen white flashes and the final invisible interval remain unchanged.

All 563 prior boss-atlas cells are exact. The appended 113 cells provide the darker silhouette; the other new mappings share existing cells. The added 435 tile rules and 243 conditions retain the existing pose-specific ordering. Removing those lines and restoring the single background filename recovers the entire 0.3.1 mapping file exactly. The confirmed sprite-limit/fireball correction and Blizzard menu lettering are unchanged.

## Live verification

MesenCE 2.2.1 replays use the supplied boss states and controller input only. `boss1_transition_routes.json` contains:

| Route | Frames | Coverage |
| --- | ---: | --- |
| menu_blizzard | 2,300 | Normal costume, left-facing pickup, ascent, fade, announcement, Stage 2, both menu selections and resume |
| reverse_blizzard | 2,550 | Approach from the other side, select Twin Fire, right-facing pickup, full transition, menu and resume |
| crouch | 650 | Already-corrected boss fireball regression |

The 0.3.1 normal and fire baselines reuse the pinned captures from its review. The opposite-side baseline and all three candidate routes are new runs. Each run records installed pack hashes before and after playback. The first screenshot after state load is empty and explicitly excluded from image claims.

`verify_boss1_transition.py` compares all 5,500 paired RAM, PPU and OAM samples per type, APU writes and common PCM. It permits at most one 3,200-byte shutdown audio buffer difference. The report records actual lengths and any difference. Image checks require background changes to replace only previously black pixels within the active bell-room scope; every existing foreground pixel stays exact. All three eight-frame fade steps must equal the preceding HD white silhouette at the correct brightness and native position, in each direction. Every other screenshot, including the full fireball route, announcement, Stage 2 card, menu and full-screen flashes, must remain identical.

All checks passed. The two transition routes change 552 images in total; 4945 other valid screenshots remain exact, including all 649 fireball captures. menu_blizzard: 252 backdrop images, 24 fade images, 0 bytes of shutdown-tail difference. reverse_blizzard: 252 backdrop images, 24 fade images, 0 bytes of shutdown-tail difference. The fireball route differs by one 3,192-byte shutdown buffer; every common PCM byte matches.

See `evidence/boss1_transition/verification.json` and `comparison.png`. The comparison uses actual captures: frame 1000 for the wall, frame 1315 for the left-facing gray fade and frame 1587 for the right-facing darker fade. The labeled silhouette crops are enlarged with nearest-neighbor scaling. Earlier-stage coverage remains the historical 0.3.1 regression; it is not claimed as a new replay for this scoped repair.

## Reproduce

Build 0.3.1 in a separate checkout and keep its extracted pack. Build this candidate and run the same routes sequentially against each pack, using the local ROM, emulator and three boss states described in `test_states/README.md`:

```sh
python scripts/run_boss1_qa.py --mesen /path/to/Mesen --rom '/path/to/Holy_Diver_(Tr).nes' --pack /path/to/pack --state1 '/path/to/Holy_Diver_HD_1(5).mss' --state2 '/path/to/Holy_Diver_HD_2(3).mss' --state3 '/path/to/Holy_Diver_HD_3(2).mss' --route scripts/boss1_transition_routes.json --out work/boss1_transition/before-or-after
python scripts/verify_boss1_transition.py --before work/boss1_transition/before --after work/boss1_transition/after --old-pack /path/to/0.3.1-pack --out evidence/boss1_transition/verification.json
python scripts/export_boss1_transition.py --before work/boss1_transition/before --after work/boss1_transition/after --out evidence/boss1_transition/comparison.png
```

For native reference, the runner supports `--native`; keep those outputs separate. That diagnostic provides the original room-repeat reference, not an additional paired candidate test.

## Package

The candidate contains 79 root pack files with no nested ZIP. Against 0.3.1, only `Boss_Tiles_2x.png`, `hires.txt` and `README.txt` change, and one repeated backdrop is added. The other 75 files stay byte-identical. The prior candidate manifest is `0.3.1-pack-sha256.json`; the historical `approved-pack-sha256.json` name describes the tested candidate on this branch, not user approval.

The ZIP-wrapped incremental Git bundle includes all unmerged boss commits since main 0.2.1. The user pushes it with local credentials. The review PR and actual Actions artifact inspection follow that push. Do not merge, tag or publish a release before approval.
