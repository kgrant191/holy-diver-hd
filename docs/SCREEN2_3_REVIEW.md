# Blue tears — approved 0.6.1

The user requested that the eyes drop blue tears instead of fire. The two eye-projectile atlas cells now use a cobalt/cyan liquid teardrop, with a pointed top, rounded base and small wet highlight. Both native footprints stay exact: `02DC` uses X1–6/Y0–7 and `02DD` uses X0–6/Y1–7. Native OAM controls movement, timing and mirroring.

Only `Stage2_Vertical_Cave_Tiles_2x.png` and the installed README change from 0.6.0. All 83 other pack files, including `hires.txt`, remain byte-identical. Within the atlas, only those two cells change; the eyes, cave backdrop, platforms, ghouls, player and other enemies' fireballs stay exact. The pack still contains 85 root files.

The built-in image-generation tool created `art/generated/screen2_3_tear_generated.png`. Its complete prompt and the user's request are retained in `screen2_3_tear_prompt.json`. `scripts/build_screen2_3.py` crops its alpha bounds and deterministically registers the two sizes. The original eye source and body registration remain unchanged.

## Verification

The existing 0.6.0 combat/respawn capture is the baseline. A fresh 0.6.1 replay uses the same supplied save and controller route, without RAM edits. The 2,400-frame route covers falling shots, both horizontal directions, vertical scrolling, damage, native death grayscale, death/respawn and return to gameplay.

- All 1,200 RAM/PPU/OAM samples per type match exactly.
- APU events and full equal-length PCM match, with no shutdown-tail difference.
- All 637 changed screenshots are confined to eye-projectile positions; 563 other screenshots are identical, including six black frames.
- Complete live sprite matches: DC native 56, DC mirrored 54, DD native 22, DD mirrored 32.
- Five projectile positions during fast downward scrolling are established from exact complete old AND new sprite pixels, since endFrame OAM describes their later positions. The verifier keeps the original OAM margin and still rejects any pixels outside verified projectile bounds.

The prior 0.6.0 full-room traversal remains in `evidence/screen2_3/`. This focused repair replay does not rerun the complete exit route. Its unchanged mappings and strict visual-difference bounds establish the scope of this repair. See `evidence/screen2_3_review/verification.json` and `comparison.png`; video is silent actual capture at 30 fps from two-frame samples. Close-ups are labeled 6× nearest-neighbor enlargements of live screenshots.

```sh
python build.py
python scripts/verify_release.py
python scripts/run_screen2_2_qa.py --mesen /path/to/Mesen --rom '/path/to/Holy_Diver_(Tr).nes' --pack 'build/Holy_Diver_(Tr)' --out work/screen2_3_review/after --state '/path/to/Holy_Diver_HD_1(9).mss' --route scripts/screen2_3_review_routes.json --stride 2
python scripts/verify_screen2_3_review.py --before work/screen2_3/after --after work/screen2_3_review/after --out evidence/screen2_3_review/verification.json
python scripts/export_screen2_3_review.py --before work/screen2_3/after --after work/screen2_3_review/after --out evidence/screen2_3_review
```

The user approved 0.6.1 on 2026-10-24 ("approved"), accepting the vertical cave and blue tears at reviewed commit `29bf3b688010fd46863103c2974c8ae88f3c1c62`. Both feature branches are pushed and the documentation-only approval record is published. PRs #6/#7 passed Actions, and their actual downloaded packs contain 84/85 verified root files without nested ZIPs. `0.6.1-reviewed-pack-sha256.json` preserves the accepted review; `0.6.1-pack-sha256.json` and `approved-pack-sha256.json` pin the approved installation. Only installed README changes during approval; all 84 runtime files remain exact. The user explicitly authorized both merges ("merge it"), resolving the automatic-approval block. PR #6 merged first; PR #7 was retargeted to main and merged at `40d67dbf516eaea5b2a20e3ad9a8093a7d7b347a`. PR run 40053346170 and main run 40053648543 passed; their actual downloaded 85-file artifacts match every approved hash, pass CRC checks and contain no nested ZIP. Main is now approved 0.6.1. Adoption records change no installed files. No release/tag was created.
