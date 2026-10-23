# Third chapel section — 0.1.0 review candidate

Branch: `feature/screen-1-3`. Approval is pending in chat; approved main is 0.0.2. The three supplied states and their SHA-256 values are listed in test_states/README.md. State binaries and the supported ROM are excluded from Git.

## Native observations and registration

All three states use the same chapel palette and CHR bank. Normal and Twin Fire Randy, weapons, HUD, regular stone, the large gold flying enemy and expanding death rings already use shared replacements. Native collision, OAM placement, mirroring, animation timing and audio are unchanged.

| Addition | Native identity / palette | Measured footprint |
| --- | --- | --- |
| Reinforced blocks | BG C9–CC / 0F001030 | 16×16 native; 32×32 HD |
| Window cap and repeating body | BG B9–BE / 0F262B17 | 16×8 cap; 16×16 repeat |
| Gold serpent wall ornament | BG 8B–9D / 0F172737 | Sparse 32×56 native, 19 cells |
| Purple ghoul | Sprite 94–AB / FF140436 | Two 16×24 standing poses, four 16×16 rolling poses |
| Blue flying skull | Sprite 8C–93 / FF301116 | Two 16×16 poses |
| Initial impact flash | Sprite 60–63 / FF301116 | 16×16; registered from approved compact gold ring |
| Shared rock palette | BG 01–10, A8–AB / 0F262B17 | Reuses approved Crypt_Terrain cells |
| Empty background | BG 00 / gold and window palettes | Transparent, removes old black atlas blocks |

Background identities above are relative to pattern base $1000 (rule identity adds $0100). Scope requires the existing crypt checks plus PPU $3F0D/$3F0E/$3F0F = $26/$2B/$17. The new 1536×480 panorama repeats after 512 native horizontal pixels. It uses background layer 11, above the existing layer-10 panorama and behind native terrain/sprites. Scrolling was inspected in the three controller routes.

`scripts/build_screen1_3.py` adds 87 tile rules, three conditions, one background and atlas 28. Registered art and metadata live in `art/screen1_3/`. Shared ghoul head tiles 94/95 are identical across both standing poses and the upright compact pose. Source graphics face left before native hardware flipping. Window and ornament art is clipped/sliced into native cells; block tops retain the full native collision span.

All 69 pre-existing PNG/IPS files are byte-identical to 0.0.2. Only hires.txt and README.txt change, and two runtime PNGs are added. The validator removes the three marked addition sections and requires the original hires.txt bytes and ordering exactly. This also preserves the approved title/ledge fixes and exact audio IPS.

## Generation briefs and source assets

Five assets were produced with the built-in image-generation tool, with transparent backgrounds for the object/enemy sheets. These briefs record their design constraints; registration code defines the final pixel dimensions and alignment.

| Source in art/generated/ | Brief and references |
| --- | --- |
| screen1_3_background_generated.png | Solid navy Gothic nave masonry, carved arches and warm gold torch accents, consistent with the approved crypt. No floor, platforms, characters or glass windows; native geometry and window tiles supply those elements. Opaque wide image. |
| screen1_3_environment_generated.png | Three separated transparent columns: silver/blue reinforced ribbed stone block; narrow pointed emerald/ruby Gothic glass window; gold coiled-serpent medallion with upper stalk and lower pendant. Native reference and approved crypt style guide identity and palette. |
| screen1_3_ghoul_generated.png | Two matching crouched purple-haired, pale-faced ghoul poses, facing right in the generated source, with different arms/legs and a consistent head. Dark Gothic game sprite style, transparent. Registration mirrors them to native left-facing orientation. |
| screen1_3_ghoul_roll_generated.png | Four compact curled ghoul poses: upright face left, quarter turn lower left, upside down with face upper right, quarter turn upper left. Purple hair wraps the pale face into a rolling silhouette. Same identity and transparent background. |
| screen1_3_blue_skulls_generated.png | Two square animation cells of the native small flying skull/head, both facing left. Ice-white/cyan face, cobalt shadow, hollow dark eye socket, pointed jaw and brick-red fin/wing swept behind the crown. Raised then folded wing, same head scale; no body, bracelet, scenery, glow outside silhouette or text. Native live crop supplied as reference. Readable at 32×32 HD. |

The brief first impact flash reuses `art/death_ring_0_registered.png`; it is not a new painted effect. New tile registration uses binary alpha, restrained color quantization and measured OAM footprints.

## Live review

Three 720-frame routes cover scrolling, both Randy palettes/directions, jumping/casting, all six ghoul poses in both hardware directions, both flying-skull poses, impact/death effects and the existing lives card. The pairwise report records 1,080 identical samples per memory type and identical APU writes and full captured PCM for each route. Runtime screenshots are authoritative; endFrame OAM may describe the next pose.

- `evidence/screen1_3/comparison.png`: approved 0.0.2 versus candidate, starting views from all three states.
- `evidence/screen1_3/motion.png`: actual combat, impact, death and lives-card captures.
- `evidence/screen1_3/ghoul_live_poses.png`: actual screenshot crops enlarged 3× with nearest-neighbor scaling; some poses naturally overlap Randy.
- `evidence/screen1_3/verification.json`: paired memory/audio results and installed-pack change scope.
- `evidence/screen1_3/observed_enemy_poses.json`: first sampled appearances by native mirror state.
- `evidence/screen1_3/regression.json`: fresh/reset title and earlier-crypt equality checks.

The title/reset regression includes one additional 3,196-byte final PCM buffer in the candidate capture at emulator shutdown; all 5,749,992 overlapping bytes, all APU writes and all 90 screenshots are identical. Earlier crypt combat has identical full PCM and 180 screenshots.

Coverage is limited to these recorded routes, not a whole-stage completion. Stage cards 2–6 and later rooms remain outside live coverage. No release/tag is created by this branch.
