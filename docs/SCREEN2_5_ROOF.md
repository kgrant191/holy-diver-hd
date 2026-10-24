# Readable cave ceiling — 0.8.2 candidate

The user accepted the 0.8.1 stairs ("stairs look good") but rejected the faint ceiling outline: head bumps and the bats' hanging surfaces were unclear. This revision preserves those stairs and restores a separate foreground ceiling. Stair acceptance is recorded in `evidence/screen2_5_roof/stair_acceptance.json`; the overall build remains under review on feature/screen2-5, with main still approved 0.6.1. Neither feature branch is merged or released.

## Artwork and scope

The roof uses opaque dark charcoal/plum stone with subdued red reflections and a highlighted lower edge, visibly separate from the brighter crimson panorama. It restores the complete earlier 0.8.0 ceiling silhouette, rather than a transparent interior or a thin contour. All 46 registered ceiling cells retain their earlier alpha exactly. Native geometry, head-bump behavior and enemy positions remain unchanged.

The eight rock-body identities shared by ceiling and ground retain the existing 464 bounded cap-above rules before the ceiling replacements. Thus gold platforms stay exact even where their native pattern IDs also form the roof. The new rules apply only in room 10, pointer 9D/8D, and palette 0F071737. Stairs, enemies, blue tears, lava/ice, the health jug, the red panorama and removal of foreground red columns remain untouched.

The built-in image-generation tool produced `art/generated/screen2_5_roof_generated.png`; the exact prompt is `screen2_5_roof_prompt.json`. `scripts/build_screen2_5_roof.py` deterministically crops a broad material section, registers it to the old ceiling alpha masks, adds edge lighting and writes `Stage2_Crimson_Ceiling_2x.png`. `previous_geometry.json` records the inherited atlas cells, while `registration.json` records the new registrations.

Removing SCREEN2_5_ROOF blocks restores the exact 0.8.1 mapping file. Only hires.txt and installed README change among earlier installed files; all 87 prior runtime assets remain byte-identical. One new atlas brings the install ZIP to 90 root files. The source on feature/screen2-4 remains its earlier 0.7.1 candidate; feature/screen2-5 includes the accepted newer stairs and this roof repair.

## Replay and limits

Use MesenCE 2.2.1, translated ROM SHA-1 `fe2fcd0ad334d792db16535d09f3ab9fb2bea3ac` and the unchanged `Holy_Diver_HD_1(20261024-155045).mss` (SHA-256 `8a67bbf57e6d756e36f4f6f42934d27b40c6266d95f6fc24118244c89e53ee40`). Run one emulator at a time. Replays use controller input and read-only inspection; no RAM edits fabricate positions or evidence.

```sh
python build.py
python scripts/verify_release.py
python scripts/run_screen2_5_qa.py --mesen /path/to/Mesen --rom '/path/to/Holy_Diver_(Tr).nes' --pack /path/to/0.8.1-pack --out work/screen2_5_roof/before --state '/path/to/Holy_Diver_HD_1(20261024-155045).mss' --route scripts/screen2_5_roof_routes.json --stride 2
python scripts/run_screen2_5_qa.py --mesen /path/to/Mesen --rom '/path/to/Holy_Diver_(Tr).nes' --pack 'build/Holy_Diver_(Tr)' --out work/screen2_5_roof/after --state '/path/to/Holy_Diver_HD_1(20261024-155045).mss' --route scripts/screen2_5_roof_routes.json --stride 2
python scripts/verify_screen2_5_roof.py --before work/screen2_5_roof/before --after work/screen2_5_roof/after --routes scripts/screen2_5_roof_routes.json --out evidence/screen2_5_roof/verification.json
```

Five paired controller routes pass 6,800 frames per build, with 3,400 identical RAM, PPU, OAM and PPU-view samples per type. Every APU write and all 21,724,228 PCM bytes match, with no shutdown-tail difference. All 300 stair-walk captures remain identical; so do 1,479 outside-room captures, 80 native black captures and 56 menu captures. All 1,652 changed captures stay within the registered ceiling identities; 1,748 images remain exact.

Source checks find 67,420 exact ceiling-cell matches across 12 of the 46 mapped identities, 143 complete folded-bat matches with visible ceiling contact, and 26,391 unchanged gold floor-body cell samples. The low-overhang jump at extended-route frames 620–628 retains feet Y 150, 145, 140, 140, 141 while jump remains held: the restored roof makes the native interruption visible. Installed manifests before and after each run match the final 90-file pack. ZIP CRC, flat layout, absence of nested ZIPs and all expected SHA-256 hashes pass; the H.264 comparison video decodes without errors.

The verifier accounts for the actual PPU page/fine scroll, including partially scrolled-off tiles at the left edge. Image bounds use the neighboring two-frame samples and at most two HD pixels of horizontal capture-phase padding, without admitting unrelated identities. Full-color source checks exclude native grayscale/death palettes, which remain paired and visually inspected.

The extended route reaches camera scroll 482 and the hot lava fall before death/return. The entrance freeze route exercises Blizzard flashes but does not establish a new frozen-lava crossing. The far 2-5 exit and uninterrupted traversal of the previously untested middle of 2-4 remain unverified. The handled health jug's live pickup remains unverified from the previous review; its asset and mappings are unchanged here. The 34 roof identities not observed in these routes retain static mapping/alpha validation only.

The comparison and silent video contain unretouched actual Mesen captures. The head-bump segment is explicitly shown at half speed; the other clips retain normal timing. The source bundle contains both feature refs and Downloads-based push commands. PRs and Actions artifact checks follow the user's push; no merge or release is authorized by this ceiling request.
