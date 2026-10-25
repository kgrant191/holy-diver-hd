# Boss defeat and Breaker pickup repair — approved 0.10.1

The user reported two reappearances after the Level 2 boss defeat: its original
NES art briefly returned, then its outline appeared during the Breaker pickup.
The supplied `Holy_Diver_HD_2(6).mss` reproduces both without changing RAM.

## Cause and change

The new save begins during defeat on the gold hit palette `0F270027`.
Its subsequent fade steps are `0F170F17` and `0F070F07`. Neither had an HD
replacement in 0.10.0, so the original background tiles became visible for
eight frames each. The earlier victory route ended on the ordinary coral
palette and used different, already mapped fade steps.

`build_boss2_review.py` derives the two darker steps from the existing gold
boss source and registers them in unused atlas cells. It adds 387 room-scoped
rules before the original boss rules. Every previous atlas cell stays exact.
No new painting, geometry, gameplay or audio is introduced.

The original pack also deliberately mapped `310F0F0F` to a black boss
silhouette during the native Breaker flash. The user rejected that echo.
The repair now maps those same boss identities to the existing transparent
cell. The pale cave flash, foreground terrain, sprites and native timing
remain intact. The boss stays gone after its fade.

The install remains 93 root files. Only `hires.txt`, `Boss2_Tiles_2x.png` and
`README.txt` differ from 0.10.0; the other 90 runtime files are byte-identical.
Static validation strips the repair block to recover the exact 0.10.0 mapping,
checks the previous assets, and confines atlas differences to unused cells.

## Paired live verification

Use MesenCE 2.2.1 and translated ROM SHA-1
`fe2fcd0ad334d792db16535d09f3ab9fb2bea3ac`.
The new 12,013-byte state has SHA-256
`6cfdc375c9620d42e989e96ce4e855babe06f3d54fd49aa28d0de9bf7a408345`.
The controller-only `pickup` route captures every frame through defeat,
automatic collection, announcement and Stage 3 arrival (1,600 frames).
The original three boss routes add 4,420 frames at stride two, covering live
combat, poses, the full arena, a separate victory/pickup and the pause menu.

```sh
python build.py
python scripts/verify_release.py
python scripts/run_screen2_5_qa.py --mesen /path/to/Mesen --rom '/path/to/Holy_Diver_(Tr).nes' --pack work/boss2_review/baseline_0100 --out work/boss2_review/before --state '/path/to/Holy_Diver_HD_2(6).mss' --route scripts/boss2_review_routes.json --stride 1
python scripts/run_screen2_5_qa.py --mesen /path/to/Mesen --rom '/path/to/Holy_Diver_(Tr).nes' --pack 'build/Holy_Diver_(Tr)' --out work/boss2_review/after --state '/path/to/Holy_Diver_HD_2(6).mss' --route scripts/boss2_review_routes.json --stride 1
python scripts/run_screen2_5_qa.py --mesen /path/to/Mesen --rom '/path/to/Holy_Diver_(Tr).nes' --pack 'build/Holy_Diver_(Tr)' --out work/boss2_review/regression_after --state '/path/to/Holy_Diver_HD_1(20261024-231216).mss' --route scripts/boss2_routes.json --stride 2
python scripts/verify_boss2_review.py
python scripts/export_boss2_review.py
```

The baseline is the exact delivered 0.10.0 pack. Original-route baselines are
retained under `work/boss2/after`. The arena pair was repeated into
`work/boss2_review/arena_repeat_before/arena` and `arena_repeat_after/arena`
using only the `arena` entry of `boss2_routes.json`; see the capture-repeat
record for why. Recreate retained baselines with the corresponding old pack
if needed. Only one Mesen process may run at once.

The verifier requires exact RAM/PPU/OAM/PPU-view, APU writes and common PCM,
with at most one shutdown audio buffer. Every changed pixel must stay inside
the measured boss tile coverage. Every non-sprite pixel in those tiles must
match either the complete HD fade source on black or the exposed pale cave
source. OAM from adjacent capture samples excludes overlaid sprites. This
checks transparent areas as well, so remaining native boss pixels fail.
Unchanged combat, scenery, transitions and menus must remain pixel-exact.
The first loaded-state screenshot is empty in both new-save replays; native
state is still compared for that frame, and the omission is recorded.

Final results: 6,020 frames/build, 3,810 identical samples per native-state type,
identical APU writes and 19,232,332 common PCM bytes. The new-save run has one
3,196-byte shutdown-buffer tail difference; other PCM lengths are equal.
All 38 changed pictures are confined to boss tile coverage: eight samples per
gold fade and 22 pickup-echo samples across both routes. All 3,771 other valid
pictures remain exact, plus one identical empty initial capture.

The retained 0.10.0 arena frame 484 differed around Randy/projectiles despite
identical native state/audio. The complete paired repeat has 360 exact pictures
and both builds match the first candidate replay. The initial discrepancy did
not recur; its cause remains unconfirmed. No exception is skipped by the final
verifier. See `evidence/boss2_review/arena_capture_repeat.json`.

The comparison PNG and normal-speed silent video contain unretouched actual
Mesen captures. No artwork mockups are used as runtime evidence. Previous
coverage limits remain; this repair does not test every later use of Breaker.

## Source handoff

The source ZIP includes all four pending feature refs through `feature/2-boss`
against main 0.6.1, with exact Downloads-based fetch/push commands. Earlier
branches remain unchanged. User push, PRs and Actions artifact verification
remain pending. The user approved 0.10.1 on 2026-10-24; the approval record preserves every reviewed installation byte. No merge or release has been performed.
