# 0.1.1 review corrections

The user's 0.1.0 review identified a blurry standing purple ghoul and Randy reverting to original sprites while crouching and firing either normal fire or Twin Fire. This candidate repairs those two issues on `feature/screen-1-3`; main remains approved 0.0.2 and PR #2 remains unmerged.

## Native identities and registration

The crouching wind-up uses $21–$26 over $33–$35; the bottom row starts five native pixels to the right of the upper row. Its footprint is 29×24 native pixels. The release uses $01/$02/$2B over $2C–$2E and $2F–$32 below, a 32×24 footprint. Both were measured from controller-driven OAM, in both directions. Palette identities are FF300036 (normal) and FF221136 (Twin Fire). Nine wind-up and ten release rules per palette select complete poses using neighboring sprites. The defeated-player fallback retains priority through `!randyDefeated`.

Four generated sprites are registered into unused cells 10/11 of the two existing Randy atlases. Binary alpha and the measured OAM mask retain native sprite coverage; a small amount of trailing fabric outside the footprint is clipped. Every pixel in the ten existing poses remains unchanged. No room restriction is added.

The ghoul's two 16×24 standing poses share head tiles $94/$95 with one 16×16 rolling pose. Twelve new standing cells are appended in unused space in Nave_Tiles_2x.png and selected by nearby $96/$98 or $9A/$9C body cells. All 87 old atlas cells, including the four rolling frames, remain identical. Nearest-neighbor registration of the simplified standing art avoids the previous smoothing at 32×48 HD pixels.

The pack remains 73 files. Relative to 0.1.0, exactly five files change: Randy_Entrance_2x.png, Randy_Equipped_2x.png, Nave_Tiles_2x.png, hires.txt and README.txt. No ROM, collision, game timing, inventory or audio code changes. The existing IPS is identical.

## Reproduction

Use Python 3.12 and the local Mesen/ROM/states documented in test_states/README.md. Keep one emulator process running at a time. Save an extracted 0.1.0 pack as `work/review_fixes/baseline_pack` before building the candidate.

```sh
python build.py
python scripts/verify_release.py
python scripts/run_crouch_qa.py --mesen "$MESEN_PATH" --rom "$ROM_PATH" \
  --pack work/review_fixes/baseline_pack --out work/review_fixes/before \
  --state test_states/Holy_Diver_HD_v10_Entrance.mss
python scripts/run_crouch_qa.py --mesen "$MESEN_PATH" --rom "$ROM_PATH" \
  --pack 'build/Holy_Diver_(Tr)' --out work/review_fixes/after \
  --state test_states/Holy_Diver_HD_v10_Entrance.mss
```

Run `run_screen1_3_qa.py` once for each pack with the same three states. Use `--out work/review_fixes/ghoul_before` and `--out work/review_fixes/ghoul_after`. The optional `--case state3` repeats one case without changing its route.

```sh
python scripts/verify_review_fixes.py --root work/review_fixes \
  --out evidence/review_fixes/verification.json
python scripts/export_review_fixes.py --root work/review_fixes \
  --out evidence/review_fixes
```

The five cases total 2,640 emulated frames per build, with 1,560 paired RAM/PPU/OAM samples. Both phases, directions and palettes are observed in live play. Only requested sprite regions change in screenshots. Sixty-four rolling screenshots are exactly unchanged. APU writes and common PCM bytes match; the state1 recording has one additional 3,196-byte shutdown buffer. One truncated baseline audio capture was discarded and the same state3 route rerun, with full equal-length PCM afterward.

Fresh/reset title and earlier crypt combat regression use `run_screen1_3_regression.py` for both packs and `verify_screen1_3_regression.py` for comparison; see `evidence/review_fixes/regression.json`. These routes retain the existing screenshots and native behavior.

Live screenshots are under `evidence/review_fixes/`; raw frames, dumps and audio stay ignored under work/. Stage 2–6 cards and the unclassified player tile $3C are not newly verified.

## Transfer and approval

The downloadable incremental bundle is based on f2c51e46fc78a18378a3301550332695e16dea3a, the already-pushed 0.1.0 candidate. The user fetches the bundle and pushes its feature ref. Then verify GitHub's feature head, update PR #2 to the 0.1.1 scope and inspect the actual Actions archive: 73 root files, exact SHA-256 manifest, no nested ZIP. Do not merge main or publish a release without explicit approval.
