# Level 3 lava corridor — 0.12.0 review candidate

This build updates the supplied corridor recording, its large/small fish, the collected boot on the Start/pause menu, and Breaker casts. It branches from approved 0.11.2 at `9eb0678f0ba3ee9aed9d19481c6eacb5f89fdd58`. Main remains merged 0.10.2. The new candidate is not approved, published or merged.

## Art and native registration

| Subject | Native identities / palette | Implementation |
| --- | --- | --- |
| Collected menu boot | 0971–0974 / 0F172737 | Exact approved 32×32 collectible art, registered in the separate background-cell arrangement |
| Large fish | 06DD–06E6 / FF301627 | Two 48×48 poses; six shared cells stay identical and the absent upper-left cell stays transparent |
| Small fish | 06EF–06F2 / FF301627 | Two 32×16 poses from the same painted fish; native unflipped art faces right, large fish faces left |
| Breaker charge | 0675–067D | Coherent 48×48 cobalt/cyan orb |
| Horizontal release and bolts | 067E–0683 | 32×32 release, 32×16 travelling bolt, native three-shot spacing |
| Upward release and bolts | 0684–0689 | Rotated 32×32 release and 16×32 travelling bolt |
| Lava / Blizzard ice | 073E–0743 | Exact approved 0345, 0344, 0343, 0342, 0341, 0334 cells in both hot palettes and frozen palette |

Breaker maps both FF221136 and FF300036 and twelve complete byte-identical banks (0675 through 1C75 in 0200 steps). The current bank is live-tested; alias identity is a static ROM-byte proof, not a claim of later-level playthroughs. Native mirroring, motion, MP use, projectile count, stair destruction and audio remain untouched. No additional Breaker cast phase remains original in the supplied movie or the left/right/upward controller probes.

The corridor is mode 10 / room 9AA6. Three palette guards protect hot and frozen states from menus and shaft transitions. It reuses the exact Stage 2 cave panorama, approved brown body material and native floor caps. Both stair orientations register the approved carved-step source inside native contours; the ceiling follows native lower boundaries. Nonsolid hanging decorations reveal the backdrop. Empty cells left by Breaker-destroyed stairs also reveal the cave.

Only fish and spell source art are newly painted. Built-in image generation produced `art/generated/level3_fish_generated.png` and `level3_breaker_generated.png`; exact prompts and native reference paths are retained in `level3_lava_prompts.json`. Reproducible registration, native patterns, alias proofs and poses are in `art/level3_lava/`.

The builder adds 735 tile rules, 42 conditions and 90 guarded background rules ahead of earlier replacements; Mesen uses the first match. The shared Stage 2 fallback remains last. One new atlas brings the pack to 100 files and 44 atlases. The intentionally changed prior files are hires.txt and README.txt; all 97 other approved 0.11.2 runtime files remain byte-identical. Removing the three marked new blocks recovers exact approved 0.11.2 mappings. Static validation retains all previous checks.

## Paired native tests

Use the synchronized stock MesenCE 2.2.1 harness documented in LEVEL3_OPENING.md. Native core SHA-256 is `f45cd3fd53d48176f66a1d2ff9713394e4428fae98bee53df69bed5a442e7e79`; ROM SHA-1 is `fe2fcd0ad334d792db16535d09f3ab9fb2bea3ac`. The user movie SHA-256 is `b13e4d21d182ea84f5e9614d839db71c765f26d4874b4a6cbea5b91e8332699d`; embedded starting state is `2306869106294ce3111a22fc02f298dcd3f60593e0adec6839afbc1a90426671`. Neither input bytes, ROM nor emulator is committed.

Create input-only derivatives with:

```sh
python scripts/make_level3_lava_routes.py "$USER_MOVIE" "$ROUTES"
```

The Breaker route appends left, upward and right casts and toggles magic during the final charge. Capture every frame from frame 3700. Blizzard branches at frame 200 and casts the already-selected spell; capture every second frame. The edge route branches at 200, moves left for 12 frames, waits 20, then repeats Right×3 / neutral×1 45 times and waits 60. Capture every frame. All derivatives preserve the embedded state and settings. `art/level3_lava/routes.json` pins the exact tested movies and input hashes. ZIP container timestamps may change a regenerated movie digest; uncompressed input/state hashes establish the same test.

Run one emulator process at a time. Example (with the preload/audio environment from LEVEL3_OPENING.md):

```sh
python scripts/run_mesen_movie.py --core "$CORE" --config "$CONFIG" \
  --database "$DB" --rom "$ROM" --movie "$MOVIE" \
  --pack 'build/Holy_Diver_(Tr)' --out "$CAPTURE" --stride 2
python scripts/verify_level3_lava.py --before "$BASELINE_CAPTURE" \
  --after "$CAPTURE" --out evidence/level3_lava/replay.json
```

| Route | Movie frames | Paired RAM/PPU/OAM/view samples per type | Equal APU writes | Equal full PCM bytes |
| --- | ---: | ---: | ---: | ---: |
| replay | 3,705 | 1,852 | 8,144 | 11,842,628 |
| breaker | 4,111 | 412 | 9,210 | 13,139,692 |
| blizzard | 821 | 410 | 1,537 | 2,629,004 |
| opening_regression | 6,883 | 1,721 | 15,528 | 21,995,512 |
| edge | 472 | 472 | 617 | 1,514,040 |

The full new movie traverses camera 0–752 across the corridor. Its 221 visible menu-boot pictures match the approved boot pixels; every pixel outside that menu cell box stays exact, including blank menu transitions. Complete fish matches cover both large poses, both small poses and native/mirrored forms across the full and Blizzard routes. Breaker release and bolt sources match in both horizontal directions and upward. Randy naturally occludes part of the charge; the verifier checks all exposed source pixels outside non-charge OAM cells, rather than claiming a complete unobstructed orb. Both spell palettes are observed.

Scene comparisons reconstruct the approved panorama and foreground cells from native PPU state, aligning within the capture interval and excluding native sprites. The full movie has 80 checks (minimum 99.9113%); the earlier-movie regression has 85 checks (minimum 99.9884%). A few alternate-frame sprite/wing edge pixels remain outside the conservative OAM masks; these are reported, not represented as exact full-background matches. The ten dense Breaker and thirteen Blizzard scene checks match 100%. `ice_motion.json` proves 120 stationary 1,200-pixel ice samples at fixed camera position. The hot palettes use the exact previous lava cells and native cycling. Thawing is not claimed.

The earlier 6,883-frame movie is replayed with stride 4: 619 unaffected-room images remain exact, 52 black transitions stay exact, and the newly mapped corridor/menu changes stay within the authorized scope. Earlier levels retain exact artwork/rules but were not replayed anew.

The native edge route stops at X10/Y96 for frames 213–232, traverses the supported span, and falls from X75/Y96 at frame 318 to X76/Y97 at 319. The native visible cap ends before the player anchor's last supported position; artwork is not extended to the boot silhouette. Trying farther left enters the previous shaft, so there is no invented left wall. Intermediate controller drafts and emulator-initialization stalls are excluded from acceptance. Completed paired edge evidence is in edge.json and edge_geometry.json. Both edge runs have an empty initial screenshot; frame 1 is excluded only from image comparisons, while its native state remains paired. At the extreme left, the inherited partially clipped Randy pose is unchanged from the baseline; this work does not claim a new player-art repair.

## Deliverables and limits

`comparison.png` uses actual before/after captures with integer enlargement only. The 18.8-second silent preview uses actual frames at normal speed, with the two close spell casts explicitly labeled half speed. It shows menu, fish/lava, traversed corridor, stairs, horizontal/upward Breaker and frozen pools. `artifact.json` records final flat-ZIP layout, CRC and SHA-256 verification.

The source ZIP wraps an incremental Git bundle carrying both feature/level3-opening and feature/level3-lava on top of main. The user pushes the artwork with local credentials. No push, PR, merge, tag or release is implied by this handoff. Later Level 3 rooms and the boss, unobserved fish identities and later-bank gameplay remain outside this coverage.
