# Level 3 review corrections — 0.11.1

Addresses the user's four review requests: create the spinning enemy, replace the first golden creature's projectiles, make the small winged eye an insect, and improve the wood. This supersedes the unapproved 0.11.0 candidate on the same feature branch. Approved main remains 0.10.2.

## Changes

- The spinning enemy is a crimson living thorn-ring with three pale scythe blades and an open center. Its native three poses occupy `0695–06AF`, nine cells per pose. One coherent generated body is registered at 48×48 and rotated through the native three-phase cadence; native OAM controls position/mirroring. Both observed ordinary palettes are mapped.
- `06B6/06B7` and `06B8/06B9` are two independent projectile frames, not emergence/body tiles. The 0.11.0 interpretation was wrong. Both now use the approved first-boss fireball source fitted into the native 32×16 HD footprints. The golden creature's body is unchanged.
- The tiny `06E7–06EE` flyer now has a compact ivory eye/thorax, antennae, tucked insect legs and rounded veined rose membranes. It has two wing positions with a common registered body position. The bat-like interpretation is superseded. Both ordinary observed palettes are mapped; native black transitions remain black.
- Broad knotted oak bark with muted moss replaces the tiny repeating strip. Separate transparent foreground surfaces follow the complete forest and tree-room native wood masks. Large features stay fixed to the world while the camera scrolls. Shading stays inside the native outline; platforms, branches and the walk-through opening keep their existing geometry.

## Sources and registration

New built-in image-generation outputs and exact prompts are under `art/generated/level3_{spinner,insect,bark_review}_generated.png` and `level3_review_prompts.json`. The original NES spinning enemy and the user's tiny flying-enemy screenshot supplied anatomy references. Generated originals remain unmodified. `scripts/build_level3_review.py` performs deterministic registration/compositing and adds overrides ahead of the previous mappings.

`art/level3_review/wood_geometry.json` records observed native cells from the existing movie. `measure_level3_wood.py` includes partially visible edge cells, including the top row of the vertical tree room. Omitting partially visible cells in the first draft exposed a narrow gap at the top of the climb; the delivered geometry includes that row. The forest surface covers 1,024×240 native pixels; the tree surface covers 256×480. The forest's two 512-pixel scroll pages select the matching source offset. Existing room/palette/view guards suppress the surfaces during transitions and menus.

All 93 previous runtime files other than `hires.txt` and installed README remain byte-identical to 0.11.0. Three new runtime PNGs bring the installation to 98 files. Removing the three marked review blocks restores the exact 0.11.0 mapping hash; removing its four marked blocks also restores approved 0.10.2. The existing entrance sound patch stays exact.

## Verification

Use the stock MesenCE 2.2.1 movie runner and synchronized screenshot observer documented in `LEVEL3_OPENING.md`. Replay the unchanged original movie into a fresh directory with capture stride 4, then run:

```sh
python scripts/verify_level3_review.py --before "$CAPTURE_0110" \
  --after "$CAPTURE_0111" --out evidence/level3_review/validation.json
```

The verifier checks the full 6,883-frame input, paired RAM/PPU/OAM/view snapshots, every captured APU write, continuous PCM, exact old assets, native black transitions and pause images. It also checks that changed pixels stay within the requested wood/actor regions, locates every complete new pose in actual screenshots, compares continuous bark pixels to their registered surfaces, and requires each visible wood mask to agree with the native nametable geometry. See the JSON report for measured counts and examples.

To reproduce the baked native wood-cell census from the accepted 0.11.0 capture:

```sh
python scripts/measure_level3_wood.py --capture "$CAPTURE_0110"
```

Earlier levels retain their exact assets and mapping bytes; they are not replayed afresh for this review. The supplied route does not reach the boss. Later Level 3 scenery and unrelated remaining native effects are outside this correction batch. No push, merge or release/tag is implied by this review build.

Measured result: 1,721 paired samples per native memory/view type, 15,528 identical APU writes and 21,995,512 identical PCM bytes. All seven complete sprite poses are found in live images. All 231 checked images containing visible wood agree with native geometry; 3,901,856 unoccluded bark pixels across 57 sampled images match the registered surfaces exactly. The other 1,251 images remain identical, including 52 native blackouts and 101 final-pause images. The 15.6-second preview is a silent edit of actual 15-fps captures, at original playback speed.
