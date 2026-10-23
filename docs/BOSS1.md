# First boss and Blizzard chamber — initial 0.3.0 candidate

The current candidate is 0.3.1; see [the fireball/menu review repair](BOSS1_REVIEW.md). The 0.3.0 results below remain the original feature evidence.

`feature/1-boss` starts from approved main 0.2.1 at `2427afd4739f273bf527810edcfae93e6592e344`. This is a review candidate. The approved main branch stays unchanged until the user approves adoption.

The three user states cover entry, a paused crouching-fire encounter, and the beginning of the boss defeat. Input hashes are in `test_states/README.md`. No ROM, state bytes, emulator or raw capture directories are committed.

## Native registration

The boss occupies a sparse 40×64-native-pixel standing footprint and a 40×48 compact footprint. Its head and torso are shared. Native mouth tiles E3–E6 produce both firing poses; E7–EC provide the alternating step legs; ED–F0 compact the legs for crouch/jump. Hardware mirroring controls direction. Unique leg-neighbor signatures select the correct lower body before the standing fallback. The four fireball tiles are arranged F1/F2 above F3/F4.

The normal boss palette is `FF1C0B36`; hits alternate with `FF102030`. The second palette retains the same registered silhouette and uses pale blue/white shading. The death state removes all 36 standing tiles one by one, ending at replay frame 300, while the native universal-color changes drive the red backdrop pulses. The builder does not add animation clocks, gameplay hooks or ROM edits.

The organ hall is identified by native room data `$0078/$0079 = 3A/85`, plus the three measured background palette checks. The Blizzard room uses `B2/85` and the same background palette checks. Existing stone cells, sconces, navy masonry and gold pendant artwork are reused. New pipe cap/repeat/foot segments retain the original lengths and positions. The bell uses its measured 48×80-native tile layout. The collectible occupies the original 16×16-native four-sprite footprint.

The native spell announcement changes graphics banks. The first 96 native tile patterns are identical in banks 00, 02 and 1E; their hashes are retained in `art/boss1/shared_chr_copies.json`. The builder aliases the existing Randy, weapon and HUD mappings with corresponding neighboring-sprite conditions for the two observed additional banks. All existing player atlases stay exact. Monochrome ascent/fade palettes reuse the approved silhouette. Exact text and palette probes select the Blizzard announcement; the native Stage 2 title/lives card remains unchanged.

## Art provenance

The built-in image-generation tool produced the boss sheet, pipe, bell, tome and fireball. The native reconstructed pose reference establishes proportions and sparse tile coverage; it is not a live screenshot. The approved ghoul and navy masonry are style references. Prompts are in `art/generated/boss1_prompts.json`; complete source images remain beside them. Registration and palette variants are deterministic in `scripts/build_boss1.py`.

The generated sheet supplies six design poses. Registration locks the upper body, uses the measured native lower-body/mouth regions, and crops to the available OAM cells. Actual emulator screenshots, rather than the concept sheet, are the review evidence.

## Reproduce the checks

Build with `python build.py`, then run `python scripts/verify_release.py`. Retain an extracted approved 0.2.1 pack for the paired baseline. Configure portable MesenCE 2.2.1 as described in `TESTING.md`; run only one emulator process at a time.

```sh
python scripts/run_boss1_qa.py --mesen /path/to/Mesen --rom '/path/to/Holy_Diver_(Tr).nes' --pack /path/to/0.2.1-pack --state1 '/path/to/Holy_Diver_HD_1(5).mss' --state2 '/path/to/Holy_Diver_HD_2(3).mss' --state3 '/path/to/Holy_Diver_HD_3(2).mss' --route scripts/boss1_routes.json --out work/boss1/before
python scripts/run_boss1_qa.py --mesen /path/to/Mesen --rom '/path/to/Holy_Diver_(Tr).nes' --pack 'build/Holy_Diver_(Tr)' --state1 '/path/to/Holy_Diver_HD_1(5).mss' --state2 '/path/to/Holy_Diver_HD_2(3).mss' --state3 '/path/to/Holy_Diver_HD_3(2).mss' --route scripts/boss1_routes.json --out work/boss1/after
python scripts/verify_boss1_qa.py --before work/boss1/before --after work/boss1/after --out evidence/boss1/verification.json
python scripts/export_boss1_preview.py --before work/boss1/before --after work/boss1/after --out evidence/boss1/comparison.png
```

The routes use controller input only. They capture screenshots and RAM/PPU/OAM every frame, APU writes, native PCM, installed pack hashes and state/ROM checksums. State 2 resumes with Start. End-frame memory can describe the following render; the screenshots establish the visual result. Every-frame capture is necessary to see both alternating hit palettes.

The reward platform is approached from each side. The left and right routes leave the tome uncollected, settle on the corresponding side and walk off. The center route collects it and verifies the automatic ascent, announcement and Stage 2 arrival. The floor route walks to both chamber walls. These checks respect the native collision footprint rather than extending the shelf to Randy's sprite overhang.

For regressions, run `run_screen1_3_regression.py` against each pack for the fresh/reset title and earlier crypt. Use `run_boss1_qa.py` with `boss1_regression_routes.json`, passing the earlier third-section state as state 1 and tree-court state as state 2; state 3 is unused in those routes. Keep the four cases in the same before/after directories and run `verify_boss1_regression.py`. It requires identical images, RAM/PPU/OAM and audio for title, crypt, nave and tree court.

## Verified result

The final paired replays cover 11,030 frames per build and 9,500 samples per memory type. Native memory and APU events match exactly. All common PCM bytes match; one boss route and the tree regression differ by one shutdown buffer. Earlier-room regression preserves 1,470 screenshots exactly, and the Stage 2 card preserves another 184. Full results are in `evidence/boss1/verification.json` and `regression.json`. Native scanline sprite limits remain unchanged, including occasional projectile flicker in crowded frames.

## Package and review

The candidate has 78 root pack files. Only `hires.txt` and `README.txt` change among the 75 approved files. New assets are `Boss_Tiles_2x.png`, `Boss_Hall_Flash.png` and `Blizzard_Acquired.png`; 73 existing runtime files remain byte-identical. Removing the marked BOSS1 sections recovers the approved mapping file exactly. The validator retains all earlier integrity and rule-order checks.

`evidence/0.2.1-pack-sha256.json` preserves approved main. The historical `approved-pack-sha256.json` name describes the candidate on this branch and is not user approval. The build archive must expose all 78 files after one extraction, with no nested ZIP. After the user pushes the incremental bundle, create the review PR and download the actual Actions artifact to verify the same names and hashes. Do not merge, tag or publish a release before approval.

The Stage 2 card and arrival are observed. Stage 2 scenery/enemies and cards 3–6 remain outside this feature's visual coverage.
