# Screen 1-4 wall and 1-up revision — 0.2.1 candidate

User feedback on 0.2.0: the 1-up should be a front-facing doll or statue, and the left walls looked strange in the supplied screenshots. The screenshots showed half-arches, banded column joins, small repeating brickwork and a disconnected gold fragment near the lower wall.

## Result and scope

The 1-up is now a front-facing Randy figurine on a bronze base, with blue and ivory costume variants. Both retain the native 8×16 footprint, sprite identities $4E/$4F, palette checks and hardware behavior. The source art was generated for this collectible rather than reusing a walking player pose.

The decorative wall is now one continuous facade with three complete pointed arches and joined stone columns. It occupies HD X0–224/Y0–896 behind the native shelf, ending at the floor. The first bay is registered to end at Y224, beneath the shelf's top. Its 32-pixel setback leaves the native shelf edge visible. Only the 46 nonsolid masonry atlas cells are cleared. The four actual shelf cells, tree, branches, roots and ground retain their exact 0.2.0 pixels and native tile bindings.

Only three installed files differ from 0.2.0: Tree_Court_Background.png, Tree_Court_Tiles_2x.png and README.txt. All mappings, condition ordering, other atlases and the IPS remain byte-identical. The package still contains 75 root files with no nested ZIP. `0.2.0-pack-sha256.json` retains the previous candidate; `approved-pack-sha256.json` describes this review candidate, not user approval. Main remains approved 0.1.1.

## Source art

The built-in image-generation tool created three source images on 2026-10-23:

- `art/generated/screen1_4_facade_generated.png`: approved chamber art used as the material/style reference; one complete isolated facade.
- `art/generated/screen1_4_one_up_blue_generated.png`: the approved Twin Fire Randy crop used as character reference, with an explicitly front-facing collectible pose.
- `art/generated/screen1_4_one_up_ivory_generated.png`: generated color edit of the blue figurine, retaining its pose and shape.

Exact prompts are retained in `art/generated/screen1_4_review_prompts.json`. `scripts/build_screen1_4.py` thresholds source alpha at 110, crops the visible source bounds, scales and quantizes to the measured registration sizes. The wall's source crop is split at Y550 into the upper bay and remaining two bays, registered to 224×224 and 224×672. The complete registered wall is also retained in `art/screen1_4/facade_registered.png`. Figure variants register to 16×32 and occupy the same four atlas cells as before.

## Verification and reproduction

Use an extracted 0.2.0 pack as the baseline. Run the same five routes described in SCREEN1_4.md for each pack, with outputs under `work/screen1_4_review/before` and `after`. They cover both 1-up collections, natural normal-costume conversion, all ghoul poses/directions, full descent, the shelf edge and the previous-room transition. No RAM writes or cheats are used.

```sh
python build.py
python scripts/verify_release.py
python scripts/verify_screen1_4_review_assets.py --before-pack /path/to/0.2.0-pack --out evidence/screen1_4_review/package.json
python scripts/verify_screen1_4_qa.py --before work/screen1_4_review/before --after work/screen1_4_review/after --baseline 0.2.0 --out evidence/screen1_4_review/verification.json
python scripts/export_screen1_4_preview.py --before work/screen1_4_review/before --after work/screen1_4_review/after --before-label 0.2.0 --after-label '0.2.1 candidate' --out evidence/screen1_4_review
```

Run the existing title/crypt and nave regression commands from SCREEN1_4.md against these two packs, then `verify_screen1_4_regression.py`. Reports and actual Mesen captures are retained in `evidence/screen1_4_review/`. The figure detail image is a 4× nearest-neighbor enlargement of actual gameplay crops, not a mockup.

The asset verifier proves every pixel outside the wall's rectangle and the 46 cleared wall/four figurine atlas cells is unchanged. It separately checks native shelf pixels, all other installed hashes, and the exported archive. The live verifier requires exact paired RAM/PPU/OAM and APU events, identical overlapping PCM with at most one shutdown buffer of length difference, both extra-life increments and unchanged previous-room screenshots.

## 0.2.1 wall/figurine revision results

Five paired routes: 4,780 frames per build, 2,390 identical samples per memory type, exact APU events and equal-length byte-identical PCM. Both front-facing pickup colors were observed and collected through controller input; lives increased 3→4. All six ghoul poses appeared in both directions. The left transition retains 185 byte-identical previous-room screenshots.

Earlier title/reset, crypt combat and nave: 2,880 frames, 990 identical samples per memory type, 468 byte-identical screenshots, exact APU events and equal-length identical PCM. Total accepted paired coverage: 7,660 frames per build and 3,380 samples per memory type. Every playback is driven by controller input, without RAM writes.

The first baseline left-transition audio capture ended early while its memory/frame capture completed. It was retained locally as an excluded capture and that one unchanged route was repeated. The replacement capture passes the original exact audio checks; no tolerance was relaxed. All other accepted cases are from the original paired runs.

The rebuilt pack matches all 75 expected hashes. Pixel checks confirm changes are limited to the decorative wall rectangle, 46 cleared wall cells and four figurine cells. All other pixels, native shelf cells, mapping bytes and the IPS are unchanged. Actual gameplay comparisons and reports are in evidence/screen1_4_review/. Main remains approved 0.1.1.

## Handoff

The ZIP-wrapped incremental bundle includes the initial screen-1-4 commit and this correction, based on main `74bee5892050e417420002d7ddc6b86a4c045b8b`. The earlier 0.2.0 bundle is not required. After the user pushes `feature/screen1-4`, open the review PR and verify the actual Actions artifact contains all 75 files at its root with matching hashes and no nested ZIP. No merge, release or tag is authorized by this revision.
