# Screen 2-5 — crimson cave (0.8.0 candidate)

The user's end-of-screen 2-4 state reaches this room by jumping up and left through the upper stair exit. The preceding 0.7.1 commit repairs both stair flights; this feature is stacked on that unapproved review branch. Approved main remains 0.6.1. Neither branch is merged or released.

## Artwork

The red areas now form a deep carnelian cavern with large hanging formations, coral-lit ridges, dark burgundy openings and distant silhouettes. Foreground red mineral columns retain their native outline and use broad facets with side shading. Gold platforms, stairs and ceiling, bats, floating eyes with blue tears, lava/ice and shared player/HUD/items reuse prior art. The entire 512-pattern bank is byte-identical to screen 2-4; `shared_chr.json` records the proof.

An initial repeated flowstone texture was too fine in actual playback. The final design represents that nonsolid wall layer in the full panorama, giving the red material larger forms and deeper recesses. The generated texture sheet's left rock panel supplies the foreground column texture; its right panel is retained as source provenance but is unused by the final builder. The panorama has its own source and exact generation prompt. No earlier source art is edited.

Scope is RAM `$0072=10`, `$0078=9D`, `$0079=8D`. Three wall-palette guards and 58 rendered-tile alternatives prevent the new backdrop leaking into the outgoing room or native black frames. There are 359 aliases and 32 new rules. Removing SCREEN2_5 sections recovers the exact 0.7.1 mapping file. All 84 inherited runtime asset files remain byte-identical; only hires.txt/installed README change, plus the new atlas and panorama (88 root files total).

| Native identities | Treatment |
| --- | --- |
| Gold terrain/ceiling and `0375–0380` stairs | Existing gold artwork and measured contours |
| `028E–02B6` | Existing ghoul/bat/fireball registrations |
| `02D8–02DD` | Existing floating eye and both blue tear shapes |
| `0371–0374`, `036D`, `0370`, `03A3–03A7`, `034F` | New crimson mineral column material in native outlines |
| `035F–0368`, palette `0F061627` | Panorama represents the nonsolid red hanging wall |
| `036E–036F`, `039B–03A0`, palette `0F061626` | Reveal deep crimson cave space |

The source images are `art/generated/screen2_5_crimson_generated.png` and `screen2_5_background_generated.png`, created with the built-in image-generation tool. The exact prompts are adjacent JSON files. `scripts/build_screen2_5.py` performs deterministic crop, registration, source scaling and panorama seam blending. The user's original screenshot remains `art/screen2_5/user_red_reference.png`.

## Replay

Use MesenCE 2.2.1, the translated ROM SHA-1 `fe2fcd0ad334d792db16535d09f3ab9fb2bea3ac`, and the unchanged 9,383-byte `Holy_Diver_HD_1(20261024-155045).mss` (SHA-256 `8a67bbf57e6d756e36f4f6f42934d27b40c6266d95f6fc24118244c89e53ee40`). Run one emulator at a time:

```sh
python build.py
python scripts/verify_release.py
python scripts/run_screen2_5_qa.py --mesen /path/to/Mesen --rom '/path/to/Holy_Diver_(Tr).nes' --pack /path/to/0.7.1-pack --out work/screen2_5/before --state '/path/to/Holy_Diver_HD_1(20261024-155045).mss' --route scripts/screen2_5_routes.json --stride 2
python scripts/run_screen2_5_qa.py --mesen /path/to/Mesen --rom '/path/to/Holy_Diver_(Tr).nes' --pack 'build/Holy_Diver_(Tr)' --out work/screen2_5/after --state '/path/to/Holy_Diver_HD_1(20261024-155045).mss' --route scripts/screen2_5_routes.json --stride 2
python scripts/verify_screen2_5_qa.py --before work/screen2_5/before --after work/screen2_5/after --routes scripts/screen2_5_routes.json --out evidence/screen2_5/verification.json
```

The runner uses ordinary controller input only and records native RAM/PPU/OAM, APU writes, continuous PCM and actual screenshots. It also retains the PPU scroll/page metadata, because logical camera RAM can be stale across room transitions. The verifier requires paired native state/audio, exact menus/outside-room images and blackouts, and complete source-pixel matches for reused sprites and the new panorama. Source-RGB checks use actual colored rendering, not palette RAM alone during grayscale death frames.

Five paired routes pass 6,200 frames per build, with 3,100 exact RAM/PPU/OAM/PPU-view samples per type, identical APU writes and identical full PCM (no shutdown tail). The verifier preserves 76 black captures, 848 outside-room captures, all 300 stair-walk pictures and 56 pause-menu pictures. It finds 211 complete panorama source matches, 190 folded-bat matches, 11 eye matches and 11 tear-DC matches in actual captures. Other bat/tear forms and mirrors retain the earlier approved source bytes and registrations; this replay does not establish a new complete-sprite match for each form.

The controller-only traversal jumps up the stairs into 2-5 and reaches camera scroll 281 (player world X 409), covering the first bat and several eye platforms before death/respawn and return. Combat includes both player directions and upward/downward casts. Blizzard's native black flashes and blue player palette remain intact; no lava is visible on this route, so this is not a new lava flow/freeze test. The far exit of screen 2-5 is not yet verified. The stair end state supplements, but does not establish, uninterrupted traversal of the previously untested middle of screen 2-4.

The separate 0.7.0→0.7.1 stair-repair pair passes another 1,800 frames per build and 900 exact native samples per type. These checks cover both stair flights, the landing and upper transition, with all changes restricted to native stair cells. The final 0.8.0 stair-walk replay is pixel-identical to 0.7.1. `evidence/screen2_5/comparison.png` and the 24.33-second silent review video use unretouched actual captures; their first row/clip compares 0.7.0 stairs to 0.8.0, and the crimson-room material compares 0.7.1 to 0.8.0.

## Handoff

The install ZIP contains 88 root files, with hires.txt directly available after extraction and no nested ZIP. The source ZIP contains both feature/screen2-4 and feature/screen2-5 refs, based on approved main `5fdae8a88920ad6612d9f01ee913d85af6837209`. Exact Downloads-based fetch/push commands are included. User push, PRs, Actions artifact checks and visual approval remain pending; no tag/release is created.
