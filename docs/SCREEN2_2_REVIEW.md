# Cave scenery and falling-lava fixes — approved 0.5.1

The user requested removal of the reddish hanging rocks to expose the cave backdrop, and downward motion on the lava falls. This updates the existing `feature/screen2-2` branch from 0.5.0. Main remains approved 0.4.1.

## Result and change boundary

The ten red decoration identities `035F–0368` now use transparent cells. Their native geometry/data is untouched. The indigo/plum cave panorama, gold ceiling/platforms, bats, ghouls, Randy, HUD and other effects keep their existing source art. The previous red-rock generator output remains source-history provenance but is no longer read by the builder.

Hot falls `0389–038E` animate downward using sixteen translations of the approved lava material, two HD pixels every two emulated frames. The 32-pixel body is registered as a whole before slicing, preserving continuity across the alternating `038B/C` and `038D/E` rows. The top pair joins the same cycle. Descending `frameRange` conditions precede phase zero because Mesen uses the first matching rule. Both native hot palettes keep their existing brightness pulse.

The ice palette `0F122131` selects the exact six static 0.5.0 fall tiles. Pool mappings remain unchanged. Blizzard freeze, thaw, collision and damage remain controlled by the original game; no ROM/RAM/input timing changes are made.

The pack retains 84 root files. Only `hires.txt`, `Stage2_Cave_Tiles_2x.png` and installed `README.txt` change from 0.5.0. All 81 other files match exactly, including the cave panorama and previous artwork/audio patch. The cave now contains 86 shared aliases and 237 tile rules, with 92 distinct atlas cells. The full pack has 34 atlases, 5,542 tile rules, 106 background rules and 1,464 conditions.

## Verification

Use the unchanged supplied states and routes in [SCREEN2_2.md](SCREEN2_2.md). Replay the four cases from `screen2_2_routes.json` with `Holy_Diver_HD_1(8).mss`, plus `screen2_2_approach_routes.json` with `Holy_Diver_HD_1(7).mss`. Capture every second frame. The exact tested install bytes are pinned in each replay; `evidence/0.5.0-pack-sha256.json` retains the baseline.

```sh
python build.py
python scripts/verify_release.py
python scripts/verify_screen2_2_review.py --before work/screen2_2_review/before --after work/screen2_2_review/after --baseline-pack work/screen2_2_review/baseline-pack --approach-before work/screen2_2/approach-after --approach-after work/screen2_2_review/approach-after --out evidence/screen2_2_review/verification.json
python scripts/verify_screen2_2_qa.py --before work/screen2_2/before --after work/screen2_2_review/after --approach-before work/screen2_2/approach-before --approach-after work/screen2_2_review/approach-after --out evidence/screen2_2_review/full_regression.json
python scripts/export_screen2_2_review.py --before work/screen2_2_review/before --after work/screen2_2_review/after --out evidence/screen2_2_review
```

The five controller-only cases cover 5,680 frames per build and 2,840 paired RAM/PPU/OAM samples per type. Native APU writes and common PCM must match. The full regression also retains exact menus/outside-room images, native blackouts, every new bat/shot identity, all six shared ghoul poses in both directions and both bat silhouettes.

The review verifier separately requires transparency for all ten removed red identities; exact pixels for unaffected tile variants, including ice; and an exact two-pixel downward translation for every hot animation phase and loop seam. Actual gameplay comparisons bound changes to old red/hot-lava source pixels. Existing antialiased HUD edges blend over the changed backdrop, so only their measured partial-alpha pixels are permitted as additional differences. Fully opaque glyph pixels stay protected.

Motion checks use an unobstructed section of the fall with a stationary camera, comparing consecutive captures while the rendered palette remains stable. Exact source colors classify the displayed palette because the endFrame PPU state can lead the screenshot during pulses and black flashes. The image rows must translate down; upward matches are rejected. Frozen captures must remain identical to each other and the 0.5.0 ice artwork. The final checks pass 173 downward two-pixel transitions with no upward or stationary hot pairs, and all 222 frozen pairs remain stationary. Per-case results and measured counts are in `evidence/screen2_2_review/verification.json`.

An isolated crossing screenshot showed different player/bat poses despite identical native state. The complete candidate crossing was repeated with unchanged bytes; the discrepancy persisted. A fresh capture of the unchanged 0.5.0 baseline then passed the same strict comparison across all five cases. See `capture_repeat.json`. No exception is added to the final verification.

The comparison image and silent side-by-side video contain unretouched Mesen captures. Two-frame samples play at 30 fps for original gameplay speed. Coverage reaches the first fall and opposite ledge, including freeze/thaw and death/respawn; the full cave exit remains unverified. Approved by the user in chat on 2026-10-24. The reviewed hash manifest is preserved as `0.5.1-reviewed-pack-sha256.json`; approval updates only installed README. All 83 runtime files remain identical. The subsequent push, PR and adoption are recorded below; no public release was requested.

The user explicitly authorized merging both pending PRs on 2026-10-24 ("merge it"). PR #6 merged screen2-2 at `e3d957fc75e80ba9a6d9c6dd5afe61be6c557470`, followed by PR #7 for approved 0.6.1. PR/main runs 40052944384/40053555272 passed, and both actual downloaded 84-file artifacts match the approved hashes with valid CRCs and no nested ZIP. See `pr_artifact.json` and `main_artifact.json` in `evidence/screen2_2_review/`.
