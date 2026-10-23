# First-boss review fixes — 0.3.1 candidate

The user reported a flashing split fireball as it leaves the boss and mixed-font letters in the Blizzard pause-menu entry. This patch stays on `feature/1-boss`; approved main remains 0.2.1. The incremental bundle includes the whole unmerged boss feature and this repair.

## Corrections

The fireball is four correctly registered native tiles, F1/F2 above F3/F4. The game rotates their OAM order every frame. When the boss, Randy and the fireball share a crowded scanline, the NES eight-sprite limit drops alternating halves. Their straight cropped edges caused the reported line and flicker. The fireball artwork is unchanged.

The pack now uses Mesen's supported `<options>disableSpriteLimit` setting. It applies automatically throughout the loaded pack and restores native sprites beyond the eight-sprite rendering limit. It changes no controller inputs, ROM bytes, collision or animation timers. Boss hit flashes, normal sprite occlusion while the fireball emerges, and death timing remain native. The [official HD-pack format](https://github.com/SourMesen/Mesen/blob/master/Docs/content/hdpacks/_index.md#options-tag) documents this option. No `<addition>` rules or custom emulator build are required.

Blizzard uses alternate menu CHR identities `0964` and `0965` for R and D, unlike the R used in TWIN FIRE. Both now use the existing DejaVu Serif Bold 14-pixel ivory menu font at the same cell anchor. They occupy two formerly empty cells in `Boss_Tiles_2x.png`; all earlier pixels in that atlas and every other artwork file remain exact. Rules require the existing pause-screen, magic-row and paused-palette signatures.

## Live evidence

`boss1_review_routes.json` covers 4,100 frames per build: crouched fire, hit flashes, standing/rightward fire, defeat, Blizzard pickup/ascent, Stage 2 arrival, pause, both menu selections and resume. The three combat baselines reuse the pinned 0.3.0 captures; the menu baseline was replayed for this repair. All 4,100 paired RAM/PPU/OAM samples per type and all APU writes match. All common PCM bytes match; the right-fire and menu routes differ only by one 3,196-byte shutdown buffer.

Frame-by-frame image checks require combat differences to stay inside native sprite rectangles. The menu route changes only the two R/D cells; its other 2,003 captured images remain identical, covering the original defeat/transition sequence. Each combat route has more than 150 complete, pixel-exact fireball captures. In the first shot, frames 24–33 contain the entire registered fireball; frames 20–23 still overlap the native boss sprites.

The earlier-room suite adds 3,360 frames and 1,830 paired memory samples per type. Title/reset, crypt and tree-court images remain identical. The nave changes 39 of 500 images: every changed pixel is within a native sprite rectangle on a scanline containing more than eight sprites. These restore previously dropped flying-enemy/player pixels. All 1,431 other regression images, memory, APU writes and equal-length PCM remain identical. Inspect `evidence/boss1_review/nave_sprite_comparison.png` for this expected effect of the rendering option.

Total coverage for this repair: **7,460 frames per build and 5,930 paired samples per memory type**. These are actual MesenCE 2.2.1 screenshots and controller replays, with no game-RAM writes. Reports are `verification.json` and `regression.json` under `evidence/boss1_review/`. Initial 0.3.0 feature coverage remains separately documented in `BOSS1.md`; it is not relabeled as a new test run.

## Reproduce

Use the ROM, Mesen and three boss states described in `test_states/README.md`; configure Mesen as in `TESTING.md`. Build 0.3.0 separately for the baseline, then build this candidate. Run each pack sequentially:

```sh
python scripts/run_boss1_qa.py --mesen /path/to/Mesen --rom '/path/to/Holy_Diver_(Tr).nes' --pack /path/to/pack --state1 '/path/to/Holy_Diver_HD_1(5).mss' --state2 '/path/to/Holy_Diver_HD_2(3).mss' --state3 '/path/to/Holy_Diver_HD_3(2).mss' --route scripts/boss1_review_routes.json --out work/boss1_review/before-or-after
python scripts/verify_boss1_review.py --before work/boss1_review/before --after work/boss1_review/after --old-pack /path/to/0.3.0-pack --out evidence/boss1_review/verification.json
python scripts/export_boss1_review.py --before work/boss1_review/before --after work/boss1_review/after --out evidence/boss1_review/comparison.png
```

Run the existing `run_screen1_3_regression.py` title/crypt routes and `boss1_regression_routes.json` nave/tree routes for both packs, then use `verify_boss1_review_regression.py`. It preserves the earlier verifier's exact-image requirement for title, crypt and tree, while requiring nave differences to lie strictly within native sprite-overflow pixels.

## Package and approval

The candidate still contains 78 root files. Relative to 0.3.0, only `hires.txt`, `Boss_Tiles_2x.png` and `README.txt` change; 75 files remain byte-identical. Only 178 formerly transparent atlas pixels change. Removing the two glyph rules and one option section recovers the complete prior mapping file. Relative to approved 0.2.1, all 73 earlier runtime files remain exact.

`0.3.0-pack-sha256.json` preserves the prior candidate; `approved-pack-sha256.json` retains its historical filename but describes unapproved 0.3.1 on this branch. The pack ZIP must contain all 78 matching files at its root with no nested ZIP. The actual Actions artifact check and review PR follow the user's manual bundle push. Do not merge, tag or publish a release before approval.
