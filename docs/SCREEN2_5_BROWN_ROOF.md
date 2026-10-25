# Original brown ceiling restored — 0.8.3

The user rejected the charcoal/plum 0.8.2 ceiling and requested the original brown appearance. This restores the exact 0.8.0 ceiling artwork while preserving the user-accepted 0.8.1 cut-stone stairs. The red cave panorama, removed red foreground columns, gold platforms, blue tears and handled health jug remain as in 0.8.1.

`scripts/build_screen2_5_brown_roof.py` adds 46 first-match rules pointing directly to the original atlas cells recorded in `art/screen2_5_roof/previous_geometry.json`. No new texture, recoloring or alpha editing is involved. The rejected ceiling generator is no longer called; its source remains historical provenance. The builder removes the rejected atlas from an existing output directory. All 87 runtime assets from 0.8.1 remain byte-identical; only hires.txt and installed README change. The pack returns to 89 root files, 38 atlases and 6,997 tile rules.

`validate_pack.py` checks every original atlas reference, its priority and bounds, all 87 earlier runtime hashes, and that stripping the new block recovers the exact 0.8.1 mapping file. Original ceiling and floor body identities now use the same original brown artwork; the earlier floor conditions and accepted stair mappings remain intact.

## Live checks

Use MesenCE 2.2.1 and the same translated ROM/save as `SCREEN2_5_ROOF.md`. Reuse the unchanged five routes in `scripts/screen2_5_roof_routes.json` and `run_screen2_5_qa.py`, capturing every second frame. The baseline is the retained final 0.8.1 playback; the candidate is a fresh 0.8.3 controller-only run, with no RAM writes.

```sh
python build.py
python scripts/verify_release.py
python scripts/run_screen2_5_qa.py --mesen /path/to/Mesen --rom '/path/to/Holy_Diver_(Tr).nes' --pack 'build/Holy_Diver_(Tr)' --out work/screen2_5_brown_roof/after --state '/path/to/Holy_Diver_HD_1(20261024-155045).mss' --route scripts/screen2_5_roof_routes.json --stride 2
python scripts/verify_screen2_5_brown_roof.py --before work/screen2_5_brown_roof/before --after work/screen2_5_brown_roof/after --routes scripts/screen2_5_roof_routes.json --out evidence/screen2_5_brown_roof/verification.json
```

Five paired routes pass 6,800 frames per build, with 3,400 identical RAM/PPU/OAM/PPU-view samples per type, identical APU writes and all 21,724,228 PCM bytes (zero shutdown-tail difference). All 300 stair captures remain exact, along with 1,479 outside-room pictures, 80 black captures and 56 menu captures. Every one of the 1,652 changed images stays within ceiling cells; 1,748 images remain identical. Source checks find 67,420 exact original ceiling-cell matches across 12 observed identities, 143 complete folded bats with visible ceiling contact, and 26,391 unchanged gold floor-body cells. The native head-bump Y progression remains exact. All before/after installation hashes match the final 89-file pack.

The install ZIP passes CRC, root-layout and all 89 SHA-256 checks; the comparison video decodes without errors. An initial replay was discarded when a stale, unused 0.8.2 atlas reappeared in the installation. The final replay follows explicit stale-file removal and passes both installation-manifest checks for every route, with no exceptions. The verifier compares native RAM/PPU/OAM/PPU-view/APU/full PCM, bounds every image change to ceiling identities, checks original source pixels and visible folded-bat attachment, preserves gold platforms and requires all 300 stair pictures to stay exact. Preview images compare the rejected 0.8.2 roof with 0.8.3 using actual paired Mesen captures; the head-bump video segment is explicitly half speed.

Coverage limits remain the far 2-5 exit, uninterrupted middle of 2-4 and live handled-health-jug pickup. The extended route reaches the hot lava fall before death/return; the entrance freeze route does not establish a fresh frozen-lava crossing. Only observed roof identities receive new live source-pixel coverage; every mapped identity is validated statically.

The source bundle contains feature/screen2-4 and feature/screen2-5, based on approved main 0.6.1. The accepted stairs and current ceiling are on feature/screen2-5; feature/screen2-4 retains the earlier 0.7.1 source. The overall build remains under review; no merge or release is authorized.
