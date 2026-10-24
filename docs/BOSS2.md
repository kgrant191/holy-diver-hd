# Level 2 wall boss and Breaker — 0.10.0 candidate

The user approved the delivered 0.9.0 artwork and requested the Level 2 boss next on 2026-10-24. `feature/2-boss` starts after the approval record on `feature/screen2-6`; the installed 0.9.0 bytes and expected manifest remain unchanged. Main is still 0.6.1 pending the source-push/PR workflow.

## Native registration and artwork

The supplied state enters room 08 with room-data bytes 7D/8F (pointer 8F7D). Its initial 512-pattern PPU bank matches physical CHR 0400–05FF. The first actor patterns are exact copies of earlier banks. `art/boss2/native_inventory.json` records the matches and observed palettes; only verified copies receive aliases.

The boss is background-tile artwork spanning two nametables. A small left-facing skull joins a larger violet organ behind it, with a broad network of branching roots. Its complete layout covers 192×256 HD pixels, starting at world X208/native Y32. The first narrow generated source used the initially visible left half; it is retained only as an edit reference. The final source follows the full decoded native layout. It is registered at 160×224 within the complete canvas, offset (12,16); 199 opaque root-edge pixels outside the native tile coverage are clipped. The connected face and organ are inspected in actual play, including a fully visible boss with no viewport clipping. The exact registered source is `art/boss2/wall_registered.png`.

The ordinary palette `0F121626` selects coral-pink flesh, ivory ridges and a violet organ. The native hit palette `0F270027` selects a gold/charcoal version with the same silhouette; other observed pulse/fade palettes retain their native changes. `0F0F0F0F` hides the defeated boss. The native pickup flash changes the universal color to 31 and briefly shows its black silhouette; the pack retains that behavior against a pale-blue variant of the existing cave background. Timing is entirely native.

The chamber reuses `Stage2_Crimson_Cave_Background.png` and the accepted brown rock source. Its new terrain identities use measured native contours with the existing texture. The orange repeating wall motif is nonsolid and reveals the cave. The boss's four-cell projectile uses the unchanged first-boss fireball source. No new cave panorama, terrain painting, Randy pose or fireball source is introduced.

Breaker has a new opaque crimson/brass spell tome with a fracture rune, fitted to the native four-cell 32×32 HD footprint. Its announcement uses the existing intermission design. Exact native word probes distinguish it from Blizzard, and a rendered B-tile guard prevents the card appearing during the preceding black transition. The existing Stage 3 card, arrival and pause-menu Breaker label remain intact.

`scripts/build_boss2.py` adds 366 actor aliases with remapped `spriteNearby` anchors. Broad aliases follow existing specific rules, including the existing bank-04 lives-card mappings. New boss/room-specific rules precede older defaults. The final shared Stage 2 fallback block stays last.

New painted sources and exact built-in image-generation prompts are under `art/generated/boss2_*`. Native references, registered wall variants, spell book, fireball copy, geometry and metadata are under `art/boss2/`. Sources are committed; ROM, emulator, savestate bytes and raw capture dumps are excluded.

## Build and preservation

The pack adds three installed assets: `Boss2_Tiles_2x.png`, `Boss2_Cave_Flash.png` and `Breaker_Acquired.png`. All 88 previous runtime asset files remain byte-identical. Only hires.txt and README.txt change among the 90 old files. The install contains 93 root files, 40 atlases, 9,645 tile rules, 372 background rules and 2,030 conditions.

Static validation strips all BOSS2 sections to recover the exact approved 0.9.0 hires.txt, checks every previous runtime hash, atlas bounds and first-match conditional ordering. The exact entrance audio patch is unchanged. The manifest retains the historical `approved-pack-sha256.json` filename but describes the current review candidate; approval is tracked separately in STATUS.md.

## Live checks

Use MesenCE 2.2.1 and translated ROM SHA-1 `fe2fcd0ad334d792db16535d09f3ab9fb2bea3ac`. The unchanged 4,690-byte state `Holy_Diver_HD_1(20261024-231216).mss` has SHA-256 `3dc10e1f35dda26171678ca6548fc3f974635b6e9face870525398c1a658f7e6`.

Three routes compare 0.9.0 and 0.10.0: `victory` (2,800 frames), `poses` (900) and `arena` (720). They cover entry, both player directions/costumes, jumps and directional casts, boss/projectile phases, hit flashes, complete defeat, Breaker collection, the announcement, Stage 3 arrival and menu selection. Two previous-screen routes add 1,320 frames for a total of 5,740 per build. Inputs are controller-only with no RAM writes.

```sh
python build.py
python scripts/verify_release.py
python scripts/run_screen2_5_qa.py --mesen /path/to/Mesen --rom '/path/to/Holy_Diver_(Tr).nes' --pack work/boss2/baseline_090 --out work/boss2/before --state '/path/to/Holy_Diver_HD_1(20261024-231216).mss' --route scripts/boss2_routes.json --stride 2
python scripts/run_screen2_5_qa.py --mesen /path/to/Mesen --rom '/path/to/Holy_Diver_(Tr).nes' --pack 'build/Holy_Diver_(Tr)' --out work/boss2/after --state '/path/to/Holy_Diver_HD_1(20261024-231216).mss' --route scripts/boss2_routes.json --stride 2
python scripts/run_screen2_5_qa.py --mesen /path/to/Mesen --rom '/path/to/Holy_Diver_(Tr).nes' --pack 'build/Holy_Diver_(Tr)' --out work/boss2/regression_after --state '/path/to/Holy_Diver_HD_1(20261024-223733).mss' --route scripts/boss2_regression_routes.json --stride 2
python scripts/verify_boss2_qa.py --before work/boss2/before --after work/boss2/after --out evidence/boss2/validation.json
python scripts/export_boss2_preview.py --before work/boss2/before --after work/boss2/after --out evidence/boss2
```

The baseline pack is the exact delivered 0.9.0 installation. Regression baselines are its retained `walk_right` and `poses` captures under `work/screen2_6/after`; recreate those with the prior state and old pack if needed. Only one Mesen process may run at once. Before/after installation hashes are checked for every route.

The verifier checks paired RAM/PPU/OAM/PPU-view, APU writes and full common PCM (allowing at most one shutdown buffer), blackouts, and unchanged scenes outside the boss/Breaker presentation. It compares the entire visible boss against its registered source, including ordinary, hit and victory silhouette phases; a full-width unoccluded match is required. Actual PPU positions between adjacent two-frame captures align moving-camera samples. Complete fireball and tome matches are required. The defeated boss region must reveal exact cave pixels, and the Breaker card must match its source while native sprites/HUD remain over it. All previous 2-6 regression screenshots must be identical.

Final results: all 2,870 samples per native-state type and 18,337,804 PCM bytes match, with zero shutdown tail differences. The whole visible boss matches 64 ordinary samples, one gold hit sample and one victory silhouette sample; one sample contains the entire unclipped boss. The victory picture is captured before the end-frame palette reset, so the verifier also requires 21,859 exact pale cave pixels around that silhouette. Complete fireball/tome source matches total 74/18. The defeated boss exposes 15,494 exact cave pixels. All 660 earlier 2-6 pictures, 736 outside-room captures and 20 black captures remain exact; ten announcement samples match the Breaker card. Exact evidence is in `evidence/boss2/validation.json`.

The first candidate revealed the Breaker card one frame before a native blackout ended. The final build adds the rendered-letter guard; all candidate and regression runs are repeated against the final pinned manifest. Earlier preview runs are not final evidence. The comparison and silent normal-speed video contain unretouched actual Mesen captures.

This task verifies the boss victory and transition through the existing Stage 3 card; it does not overhaul Stage 3 scenery/enemies or test every later Breaker interaction. Previous limits on far 2-5/2-6 exits and the handled-health-jug pickup remain. The stage-card coverage is now 1–3; cards 4–6 remain mapped but untested.

## Handoff

The source ZIP contains an incremental Git bundle with `feature/screen2-4`, `feature/screen2-5`, `feature/screen2-6` and `feature/2-boss` against main 0.6.1. Its README supplies exact Downloads-based fetch/push commands. Source push, PR and Actions artifact verification follow the user's push. No merge, tag or release is performed as part of this candidate.
