# Screen 2-4 stair repair — 0.7.1 candidate

The user supplied `Holy_Diver_HD_1(20261024-155045).mss` at the upper flight and reported the remaining original stairs. SHA-256: `8a67bbf57e6d756e36f4f6f42934d27b40c6266d95f6fc24118244c89e53ee40` (9,383 bytes). The state remains unchanged and outside Git.

Twelve native identities `0375–0380` form the two diagonal steps and horizontal landing. The builder registers each complete 16×16 native shape, fills interior shading holes, and clips the accepted gold texture to its original upper/lower outline before slicing the HD cells. Original collision and step positions remain unchanged. The twelve rules have removable `SCREEN2_4_STAIRS` markers; removing them recovers exact 0.7.0 mappings. Previously used atlas cells stay exact. Only hires.txt, the ceiling atlas and installed README change; the other 83 pack files remain identical.

Use `scripts/screen2_4_stairs_routes.json` with `run_screen2_2_qa.py`, the supplied end state, and capture stride 2. Run once with the retained 0.7.0 pack and once with 0.7.1, writing `work/screen2_4_stairs/before` and `after`. Verify with:

```sh
python scripts/verify_screen2_4_stairs.py --before work/screen2_4_stairs/before --after work/screen2_4_stairs/after --out evidence/screen2_4_stairs/verification.json
```

Two paired routes pass 1,800 frames/build, 900 RAM/PPU/OAM samples per type, identical APU events and full equal-length PCM. All 465 changed images are confined to native stair cells. All twelve identities are observed, and 332 next-room images remain exact. The mask uses the PPU nametable selector because game camera RAM resets before the displayed page on return; adjacent recorded PPU selectors cover the page boundary, while pixel differences remain limited to the twelve native tiles.

Actual captures cover both flights, their landing, the upper exit, entry into room `10/9D8D`, and return after native death/respawn. This supplements the entry/lava coverage from 0.7.0 but does not establish an uninterrupted full traversal of screen 2-4. Screen 2-5 remains unchanged in this commit and is separate new work. Both candidates remain unapproved; main remains approved 0.6.1.
