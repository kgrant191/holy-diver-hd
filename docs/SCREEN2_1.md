# Stage 2 screen 1 — 0.4.0 historical review candidate

Superseded by the cave and enemy repairs in [0.4.1](SCREEN2_1_REVIEW.md). The original implementation and results below are retained as history.

Branch: `feature/screen-2-1`. Base: approved main `19176d026eb5670523ad8358d82447c63732d506` (0.3.5). The four supplied states are documented by filename and checksum in `test_states/README.md`; their bytes and the ROM are excluded from Git.

## Artwork and mapping

The entire outdoor room uses a dark volcanic panorama, native gold platform caps, molten pools, cobalt Blizzard ice, new flying imps and tumbling lava creatures, breakable gold blocks, and a textured exit cliff. The panorama is subordinate to actual rendered sky and disappears on native black frames. The cliff retains the original stepped silhouette and stalactite masks; neighboring rock signatures keep the doorway dark without painting the open sky black.

All 78 previous runtime asset files remain byte-identical. Only `hires.txt` and installation text change among the 80-file 0.3.5 pack; two PNGs are added. Removing the marked `SCREEN2_1` sections reproduces the exact approved mapping bytes. The audio patch remains unchanged. Randy, HUD, weapons, pause menu, large HP/Magic flasks and defeat rings reuse approved assets. Six aliases add the small heart, small Magic crystal and both 1-up colors in this CHR bank. No new item designs are introduced.

Scope: room `$0072=18`, room-data pointer `$0078/$0079=A1/89`. Native CHR banks are 02 (sprites) and 03 (background). Terrain and enemy art is registered to native tile/OAM positions; no collision, input, timing, inventory, ROM or RAM changes are made.

| Native identity/palette | Treatment |
| --- | --- |
| Background 0301–032D | Clear native sky/cloud/forest cells for the panorama, with their original palettes |
| Background 032E–0333 | Approved gold floor texture, cap and repeating body |
| Background 0345/0344, 0343/0342, 0341/0334 | Pool surface and body |
| `0F161606`, `0F060616` | Native pulsing lava shades |
| `0F122131` | Native solid Blizzard ice |
| Background 0347–034A | Breakable gold blocks, disappearing with native tiles |
| Background 0335–0340, 034B–034D | Exit cliff and native cutout edges |
| Sprites 027A–028D | Flying imp and falling projectile, native mirroring |
| Sprites 02DE–02F8 | Three native tumbling lava-creature poses |
| Sprite 0274 | Blizzard snow crystal |
| Sprites 0247/0248, 024E/024F | Exact approved small-drop and figurine artwork |

The native Blizzard effect alternates black and visible frames at both freeze and thaw. Using only the game's PPUMASK shadow `$FE` made the custom background appear during black frames because the watched memory and rendered frame were out of phase. `s21SkyRendered` instead requires the actual sky tile at native (128,16). The paired cast/thaw replay checks all 92 native black frames exactly. Lava/ice selection follows the native palette; there is no independent guessed timer.

Source PNGs and production briefs: `art/generated/screen2_1_*`. Built-in image generation produced the source art. `scripts/build_screen2_1.py` performs deterministic registration, with measured layouts/masks in `art/screen2_1/`. The approved gold-ground artwork is reused. Imp source art is mirrored to match the native unflipped right-facing identity; shared body cells remain stable as the native head/tail change.

## Replay and verification

Use MesenCE 2.2.1, the supported translated ROM and the four exact user states. Only one emulator may run at a time. Retain the extracted 0.3.5 pack, then build 0.4.0. Run the following once for each pack, changing `--pack` and `--out`:

```sh
python scripts/run_screen2_1_qa.py --mesen /path/to/Mesen --rom /path/to/Holy_Diver_\(Tr\).nes \
  --pack /path/to/pack --out work/screen2_1/before \
  --state1 '/path/to/Holy_Diver_HD_1(6).mss' \
  --state2 '/path/to/Holy_Diver_HD_2(5).mss' \
  --state3 '/path/to/Holy_Diver_HD_3(4).mss' \
  --state4 '/path/to/Holy_Diver_HD_4(1).mss' \
  --route scripts/screen2_1_routes.json
python scripts/verify_screen2_1_qa.py --before work/screen2_1/before --after work/screen2_1/after --out evidence/screen2_1/verification.json
python scripts/export_screen2_1_preview.py --before work/screen2_1/before --after work/screen2_1/after --out evidence/screen2_1
```

Six controller-only routes cover 6,040 frames per build: entry combat and upward attacks, neutral freeze/thaw, walking left/right across frozen pools, red-creature combat, a long crossing with two Blizzard casts and normal-fire block destruction, and pause/spell-selection/resume. The crossing reaches scroll 1280, showing the final cliff, then includes death and respawn. It does not establish the next room's artwork. The runner captures each frame's screenshot, RAM, PPU memory, OAM, APU writes and PCM; the first loaded screenshot can be empty and is excluded from image claims.

The verifier requires exact native memory and APU events, identical common PCM with at most one shutdown buffer difference, both imp directions, every enemy animation tile, all three native lava-creature poses, the pool palettes, exact black frames and unchanged pause/outside-room screenshots. The original lava creature uses rotated poses without horizontal OAM mirroring in these routes; mirrored coverage is not claimed for that enemy. Images in `evidence/screen2_1/` are actual emulator output with labels only; they are not synthetic tile-stack mockups. Review the complete silhouette and joins visually as well as the numerical report.

The separate regression routes replay the first-boss fireball, the Blizzard reward/ascent/announcement into Stage 2, and an earlier recovery item. Previous-room images must remain exact; only the new exterior may differ after arrival. The final Actions artifact must contain all 82 pack files directly at its root, including `hires.txt`, with no nested ZIP. User push and artifact verification remain pending review. No release tag or public Release is created.

For that regression, use the same runner with `--route scripts/screen2_1_regression_routes.json --stride 2`. Set states 1–4 to the prior inputs `Holy_Diver_HD_2(3).mss`, `Holy_Diver_HD_3(2).mss`, `Holy_Diver_HD_2(4).mss`, and `Holy_Diver_HD_3(3).mss` respectively. Store the paired outputs as `work/screen2_1/regression-before` and `work/screen2_1/regression-after`, then run:

```sh
python scripts/verify_screen2_1_regression.py --before work/screen2_1/regression-before --after work/screen2_1/regression-after --out evidence/screen2_1/regression.json
```

## Limits

The exterior report passes 6,040 paired samples per native-memory type and identical APU events. Common PCM matches exactly; the red-combat and menu recordings differ by one shutdown buffer (3,192/3,196 bytes). All 350 native black frames remain black, including the 92-frame freeze/thaw test. The delivered silent Blizzard clip is the unretouched candidate `cast_thaw` frames 3–920 at 60 fps; stills retain full 512×480 emulator frames.

Earlier-scene regression adds 2,470 frames per build, 1,235 exact native-memory samples per type and 1,169 unchanged previous-scene screenshots. One initial capture at reward frame 1248 had a black field instead of the baseline's white fade. A complete repeat with unchanged candidate bytes matches the baseline, including that frame, and passes every assertion. An earlier candidate replay also matched the white frame. The cause is unconfirmed; the initial discrepancy is recorded in `reward_capture_repeat.json`, without excluding that frame or changing artwork to obtain a passing result.

- This is the outdoor Stage 2 room only. The cave interior and later screens are not claimed as completed or tested.
- Small-heart drop is exercised by the red-enemy route. Other reused pickup aliases are verified against the approved source identities, without claiming every item naturally dropped in this room.
- One native pose can be partly offscreen; per-sprite mirroring and clipping are preserved.
- Artwork remains a review candidate until the user approves it.
