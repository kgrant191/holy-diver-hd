# Screen 1-4 tree court — initial 0.2.0 candidate

Historical implementation/evidence for the initial candidate; superseded by [0.2.1 wall and figurine revisions](SCREEN1_4_REVIEW.md).

Branch: `feature/screen1-4`. Base: approved 0.1.1, main commit `74bee5892050e417420002d7ddc6b86a4c045b8b`. This candidate is awaiting user review. It does not approve a merge or publish a release.

## Measured scene and registration

The supplied state starts on a 128-native-pixel shelf. A miniature Randy 1-up sits on the tree crown; purple ghouls walk and roll on the branches. Controller-driven descent reveals alternating branches, roots and a full-width rocky floor. The gold orb is background scenery, replaced by the approved moon behind the distant castle.

The environment uses native background tile identities rather than a fixed collision panorama. This preserves native platform spans and handles the nametable transition during vertical scrolling. The tree crown occupies native X176–208 at world Y96. Left branches use X144–176; right branches X208–240. The shelf uses X0–128 at Y112. The bottom ground appears at native screen Y192 when the camera reaches its final scroll position. A grounded player's sprite may overhang a platform; the artwork is not extended to the full boot/OAM silhouette.

| Element | Native identities | Source |
| --- | --- | --- |
| Crown | Background $3D/$3E/$45/$46 | Approved entrance tree crown |
| Trunk | $3F–$44/$47–$4C/$4F–$52 | Approved bark, 32×32 native repeat |
| Left/right branches | $22/$23/$4D/$4E; $5B–$5E | Approved branch ridges, each 32×8 native |
| Roots | $61–$6F | Approved root art clipped to native cells |
| Ground | $18–$1B and $01–$10 | Approved entrance ground |
| Cornices, columns, wall and arch fragments | Native masonry identities in registration.json | New generated masonry sheet |
| 1-up | Sprites $4E/$4F, 8×16 native | Approved Randy walk pose 1 at half size |
| Purple ghoul | Sprites $94–$AB, six poses | Existing Nave_Tiles_2x.png, including sharp standing cells |

`scripts/build_screen1_4.py` adds 150 atlas cells and 48 shared enemy rules: 198 tile rules total, four conditions and one background. Existing blue-skull and first-impact rules are included for matching identities, but blue skulls were not observed in this section's recorded routes. All six purple-ghoul poses were observed in both native directions.

The scope requires the measured `$0072 == $04` RAM signature plus PPU palette bytes `$3F05 == $07`, `$3F0B == $3B`, `$3F0F == $37` and the existing sprite check `$3F11 == $37`. The RAM signature remains $04 through pickup, normal-costume conversion and full descent; it changes to $08 before the left exit streams previous-room tiles. It is a read-only observed signature, not a RAM patch or a claim about the game's internal variable name. Palette checks alone leave a brief transition window. The signature closes it.

Sharp standing-specific rules precede the broader rolling mappings. The old atlas is not repainted. Every existing PNG and IPS is byte-identical to approved 0.1.1. Removing the marked `SCREEN1_4` sections recovers the old hires.txt byte for byte.

## Artwork provenance

New source: `art/generated/screen1_4_masonry_generated.png`, generated with the built-in image-generation tool on 2026-10-23. References: approved `art/generated/chamber_generated.png` for materials/style, and an actual native capture from frame 20 of the supplied state for architectural context. The prompt requested a 1024×1024 sheet; the returned image is resized to that registration grid before extracting the four regions. Generated art is used only for environment textures, never to fabricate runtime evidence.

Generation prompt:

> Use case: stylized-concept. Asset type: modular environment texture sheet for a 2D side-scrolling Gothic game at 2x NES resolution. Input 1 is ONLY approved material/style reference: dark navy shadows, warm aged gold stone, sharp detailed pixel-art clusters. Input 2 shows native left-hand temple architecture being replaced. Generate a NEW 1024x1024 texture sheet, opaque dark navy backing, four equal 512x512 quadrants, no labels, no borders/gaps. Top-left quadrant: a horizontal golden carved cornice/platform, its perfectly straight walkable top exactly at the quadrant top edge; large carved gold repeating dentils and stone slab body filling quadrant. Top-right quadrant: one slender vertical gold sandstone column shaft, frontal orthographic, symmetrical fluting and repeating carved bands, fills whole quadrant width and height, seamless vertical repeat. Bottom-left quadrant: dark navy/teal stone brickwork inset wall, soft mossy green aging and occasional warm gold cracks, seamless repeating material, fills whole quadrant. Bottom-right quadrant: one frontal narrow pointed Gothic recessed arch on dark navy masonry, warm golden carved stone frame, dark teal center, apex near quadrant top and arch legs running straight to bottom. These assets will be mechanically sliced and resized to exact native tile positions. Crisp 2D readable pixels, no blur, no bloom, no perspective, no scene composition, no characters, no trees, no text. Use the approved reference's material detail and restrained highlights.

Reused source layers: `00_distant_ruins.png`, `05_moon_behind_castles.png`, `20_tree_and_branches.png`, and `50_floor.png` under `art/layers/`. The moon and its castle occlusion are moved together. Randy and enemy pixels come from approved runtime atlases. Registered output, miniature sprites and exact mappings are under `art/screen1_4/`.

## Live verification

Five paired native-controller routes run for 4,780 frames per build. RAM, PPU and OAM are sampled every two frames; APU writes and PCM are captured continuously. No cheats or RAM writes are used.

- `pickup`: hold jump from the upper shelf and collect the blue miniature. Lives at RAM $048F increase 3→4; the pickup disappears after sampled OAM frame 126.
- `normal_pickup`: use repeated crouching spells to consume magic naturally, then collect the ivory miniature. Lives increase 3→4 again.
- `descent`: traverse alternating branch platforms and reach the lower ground, including deeper floor identities streamed near the bottom. Randy later changes to the normal costume as magic runs out.
- `ledge`: move near the left doorway, hold, then walk slowly across the shelf and fall from its right edge. OAM first records downward movement at sampled frame 592; inspect actual screenshots 588/596. The left end is a doorway, not a hard wall.
- `left_transition`: walk fully left into the previous room. From frame 104, the first full previous-room capture, the candidate screenshots must match the approved build exactly. endFrame memory changes before the corresponding rendered screenshot.

The verifier also requires every observed background tile/palette pair in the active room's two nametables to have an HD mapping, and all six ghoul poses in both directions to occur. Full-frame visual review covers the top, middle, bottom, both pickup colors, standing/rolling enemies and shelf edge. Compact evidence is in `evidence/screen1_4/`; screenshots are actual Mesen output, with labels added outside the captures.

Fresh/reset title, earlier crypt combat and the earlier nave state add 2,880 regression frames. Their screenshots are required to remain byte-identical. Audio comparison uses exact APU events and unmodified overlapping PCM; at most one 3,200-byte shutdown buffer may differ in length. See the JSON reports for actual lengths. Total paired coverage is 7,660 frames per build and 3,380 samples per memory type.

## Reproduce

Build approved main separately and retain its extracted pack. Supply the ROM/emulator and state locally using the checksums in `test_states/README.md`.

```sh
python build.py
python scripts/verify_release.py
python scripts/run_screen1_4_qa.py --mesen /path/to/Mesen --rom '/path/to/Holy_Diver_(Tr).nes' --pack /path/to/0.1.1-pack --state '/path/to/Holy_Diver_HD_1(4).mss' --route scripts/screen1_4_routes.json --out work/screen1_4/before
python scripts/run_screen1_4_qa.py --mesen /path/to/Mesen --rom '/path/to/Holy_Diver_(Tr).nes' --pack 'build/Holy_Diver_(Tr)' --state '/path/to/Holy_Diver_HD_1(4).mss' --route scripts/screen1_4_routes.json --out work/screen1_4/after
python scripts/verify_screen1_4_qa.py --before work/screen1_4/before --after work/screen1_4/after --out evidence/screen1_4/verification.json
python scripts/export_screen1_4_preview.py --before work/screen1_4/before --after work/screen1_4/after --out evidence/screen1_4
```

Use the earlier title/crypt regression runner documented in TESTING.md for both packs. Run `run_screen1_3_qa.py --case state1` for both packs, supplying all three state path arguments as required by its interface. Then:

```sh
python scripts/verify_screen1_4_regression.py --before work/screen1_4/regression_before --after work/screen1_4/regression_after --nave-before work/screen1_4/nave_before --nave-after work/screen1_4/nave_after --out evidence/screen1_4/regression.json
```

The stored nave baseline replay used the reviewed 0.1.1 pack, whose only difference from approved 0.1.1 is README.txt. All runtime bytes match. The candidate report records actual installed hashes for every new replay.

## Handoff

The new minor version follows the repository's screen-addition policy. The candidate has **75 root files** (73 previous files plus two new PNGs), no nested ZIP. The user pushes the ZIP-wrapped incremental bundle using local credentials. After that push, open the review PR and download the actual Actions artifact to compare every entry and SHA-256 against `evidence/approved-pack-sha256.json`. Do not claim the Actions artifact is verified before downloading it. Keep main at 0.1.1 until approval.

Stage cards 2–6 remain mapped but not live-tested; this work does not change that coverage. The repeated pickup routes verify the extra life itself, not every possible subsequent stage/life card.
