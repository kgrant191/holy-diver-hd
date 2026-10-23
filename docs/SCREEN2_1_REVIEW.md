# Stage 2 cave and enemies — approved 0.4.1

The user reported three issues with 0.4.0: clouds showed through the cave until the far wall entered the viewport; the brown flyers faced backward and lacked wings/downward arrows; the red enemy had a face absent from the original. The supplied cave-approach state and original-enemy screenshot are the review references.

## Repairs

The original dark-opening rule required both rock jambs in the rendered frame. It could not match while the right jamb was offscreen. The revised rule uses the left jamb plus `positionCheckX >= probe distance`. The position guard is necessary because `tileNearby` otherwise wraps negative X to the opposite screen edge, painting a dark patch in the outdoor sky. Blank doorway cells still match their native palette and room signature; native ceiling masks, cliff geometry and collision remain unchanged.

Measured consecutive sprite-X positions with a stationary camera show unflipped flyer sprites moving left and mirrored sprites moving right. The new source faces left. Register the entire brown winged demon inside the shared native OAM footprint with zero clipped opaque pixels. Keep the head/body/legs/tail stable, vary only native wing cells, and use one arrow source for both the held two-cell arrow and the falling two-cell projectile. The original release cadence and falling trajectory remain native.

The red enemy now has a pink stone scaffold around swelling crimson lobes. Three source poses follow its native animation identities without eyes, mouths or skull details. Its movement, timing, damage and hitbox are unchanged.

Built-in `image_gen` produced four transparent project assets in `art/generated/`: `screen2_1_demon_generated.png`, `screen2_1_demon_wing_generated.png`, `screen2_1_arrow_generated.png`, and `screen2_1_pulsing_rock_generated.png`. Exact briefs and generation method are in `screen2_1_review_prompts.json`. Registration is reproducible in `scripts/build_screen2_1.py`. Earlier source art remains retained as provenance.

## Verification and reproduction

Use the existing six routes in `scripts/screen2_1_routes.json` with their four supplied states, as described in `SCREEN2_1.md`. Compare the retained 0.4.0 `work/screen2_1/after` captures with the new candidate. Then run `scripts/screen2_1_review_cave_routes.json` once against each pack, using `Holy_Diver_HD_1(7).mss` for state1 (the runner requires state2–4 arguments as well; pass the same path). This 420-frame route walks right from frame 20 through the first partial reveal, full entrance, fade and next-room arrival.

```sh
python build.py
python scripts/verify_release.py
python scripts/verify_screen2_1_review.py \
  --before work/screen2_1/after --after work/screen2_1_review/final \
  --cave-before work/screen2_1_review/before \
  --cave-after work/screen2_1_review/cave-repeat \
  --out evidence/screen2_1_review/verification.json
python scripts/export_screen2_1_review.py \
  --before work/screen2_1/after --after work/screen2_1_review/final \
  --cave-before work/screen2_1_review/before \
  --cave-after work/screen2_1_review/cave-repeat \
  --out evidence/screen2_1_review
```

The verifier compares native RAM, PPU, OAM, APU writes and PCM; requires all enemy/arrow animation tiles and measured travel in both directions with a stationary camera; confines image changes to those enemy footprints and the world-space doorway; checks the early cave interior is black; and requires exact blackouts and previous/next-room images. Adjacent OAM samples account for the documented endFrame screenshot/pose timing difference. Still comparisons use unretouched frames, labels and explicitly marked nearest-neighbor crops. The video concatenates actual cave, demon and red-enemy gameplay at 60 fps without audio.

Only `hires.txt`, `Stage2_Exterior_Tiles_2x.png` and installed `README.txt` change from 0.4.0. All 79 other pack files remain exact, including the panorama, Randy, HUD, items, earlier art and audio patch. Removing the marked Stage 2 sections preserves the previous mapping bytes exactly. `evidence/0.4.0-pack-sha256.json` retains the prior review manifest; `0.4.1-reviewed-pack-sha256.json` pins the reviewed replay bytes; `approved-pack-sha256.json` records the approved installation text. The install ZIP has 82 files directly at its root.

The next room is traversed only to confirm its existing appearance remains unchanged; new next-room artwork is outside this repair. The user approved 0.4.1 on 2026-10-23. Main remains at 0.3.5 pending the source push, PR and Actions artifact verification. No release tag or GitHub Release is created.

An initial next-room screenshot at frame 403 exactly duplicated frame 402 despite identical RAM/PPU/OAM. A complete 420-frame repeat with the same installed pack bytes matched the baseline at 403 and throughout next-room frames 220–420. The cause is unconfirmed; both the initial discrepancy and repeat are retained in `evidence/screen2_1_review/capture_repeat.json`. The final verifier uses the complete repeat, with no exception or assertion removed.

Final paired verification passes across **6,460 frames per build**: all RAM/PPU/OAM and APU events match; common PCM is identical. There are 357 exact black frames, 579 unchanged outside-room captures, and 129 verified early cave-interior samples. Stationary-camera motion samples show 499 left-facing native steps and 209 right-facing mirrored steps, with no opposite-direction samples. All new enemy/arrow identities are observed. Audio shutdown-tail differences, where present, are at most one 3,200-byte buffer and are recorded per case. A complete unchanged-pack cave repeat resolves the one documented duplicated screenshot; final checks contain no exceptions.

Approval changes only installed README.txt; all 81 runtime file hashes remain identical to the reviewed commit. Existing replay evidence remains valid. The approval record is `evidence/screen2_1_review/approval.json`.
