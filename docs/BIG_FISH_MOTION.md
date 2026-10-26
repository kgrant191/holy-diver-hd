# Large-fish hover stabilization — 0.12.2 review

The new `Holy_Diver_HD(3).mmo` directly demonstrates the user's reported shaking
and apparent blur in the **large fish**, without a hit. Version 0.12.1 repaired a
separate small-fish color problem; it did not resolve this report.

## Diagnosis

The movie contains 1,200 frames, with SHA-256
`ace46ac61dabd9485e19cbd1599ad8518192d60b9894ef714c8204678ec14a18`.
Its embedded state and translated ROM match the project. It was recorded with
Mesen 2.2.1. The full recording was replayed at one-frame capture intervals.

A separate probe removed only the ten large-fish tile mappings. The original
sprite exhibits the same one-NES-pixel horizontal oscillation. All 1,200 paired
RAM/PPU/OAM/view samples, APU writes and full PCM match the HD replay. The shake
therefore originates in native hover motion, not missing HD poses, palette
changes, tile misalignment or the separate native damage blink. Fine texture in
the HD sprite makes this rapid whole-sprite movement more conspicuous.

## Graphics-only correction

Shift each complete existing 48×48 HD pose by one HD pixel, in opposite
directions for the two native horizontal velocity signs. One HD pixel is half a
NES pixel. At hover equilibrium, native positions X242/X244 now draw at X243;
X56/X58 now draw at X57. Native position, velocity, collision, AI, timing, OAM,
attacks, inventory, audio and the ROM/IPS are unchanged.

The correction uses standard Mesen memory conditions and the existing hardware
mirror condition. No emulator fork, Lua runtime, interpolation or postprocessing
is required by the installation pack. It applies only when:

- Gameplay mode is 10 and room pointer is 9AA6.
- Exactly one of the sixteen object slots contains native object type 26.
- That object's observed horizontal hover/cruise speed bytes are CC and 00/80.
- Its damage timer is zero.

The local art offset reverses under hardware horizontal mirroring so the world
offset is consistent. The entire pose moves together. Both poses have sufficient
transparent margins; alpha counts remain exact and no paint enters the absent
upper-left native tile. Vertical bob and fin animation are retained.

The unchanged original rules remain as fallback for attacks, damage, other
speeds/rooms and ambiguous multiple-fish states. Initial horizontal approach in
the same CC movement state also receives the half-pixel offset. Multiple fish
and unobserved object slots are guarded/static implementations, not new live
coverage claims; the recorded routes exercise slots 6, 7 and 10.

`build_big_fish_motion.py` registers twenty cells in the previously empty final
atlas row, X0–319/Y496–511, and adds 80 conditions and 640 first-match rules. All
previous atlas pixels, original painted sources, pose files, small-fish repair,
menus, scenery and Breaker graphics remain exact. Only hires.txt, this atlas
and installed README differ from 0.12.1; 97 other runtime files are unchanged.
Removing the two marked new blocks recovers exact 0.12.1 mappings.

## Verification

`verify_big_fish_motion.py` pairs the new 1,200-frame movie, previous 3,705-frame
corridor movie and 821-frame Blizzard derivative at stride one. It requires all
native samples, every APU write and complete PCM to match, and bounds every
image difference to the large fish in the eligible movement state. Other states
must remain visually exact. Pixel matching checks the preserved fish source
outside other sprites' occlusion, using the same exposed pixels for each tested
offset.

Three uninterrupted hover windows in the new recording pass:

| Frames | Facing | Before: HD X | After: HD X | Pixel-proven frames |
| --- | --- | --- | --- | --- |
| 300–450 | Left | 242 / 244 | 243 | 151 / 151 |
| 780–840 | Right | 56 / 58 | 57 | 61 / 61 |
| 1000–1100 | Right | 56 / 58 | 57 | 101 / 101 |

All 313 frames retain their exact native vertical position. Both fin poses,
both directions and both corrected offsets have actual pixel-proven examples.
Dives, turns and damage states retain the original rendering. Detailed counts
are in `evidence/big_fish_motion/recording.json`, `corridor.json` and
`blizzard.json`.

The early direction-calibration probe and a stalled initialization are excluded
from acceptance. An initial stride-two Blizzard comparison could not identify
the fish on alternating native damage-blink frames; both sides were replayed at
stride one. The final verifier does not exempt those frames.

Run with the stock synchronized movie harness from LEVEL3_OPENING.md:

```sh
python scripts/verify_big_fish_motion.py --before "$BASELINE_CAPTURE" \
  --after "$CANDIDATE_CAPTURE" --out evidence/big_fish_motion/recording.json
python scripts/export_big_fish_motion.py --before "$BASELINE_CAPTURE" \
  --after "$CANDIDATE_CAPTURE" --out Holy_Diver_HD_v0.12.2_Big_Fish_Motion.mp4
```

The 20-second before/after preview consists of consecutive actual emulator
captures, with fixed viewport crops and integer nearest-neighbor enlargement.
Normal and quarter speed are labeled. No tracking, frame blending or synthetic
stabilization is applied to the preview itself.

0.12.2 remains an unapproved review candidate on feature/level3-lava. Approved
continuation remains 0.11.2 and main remains 0.10.2. No push, PR, merge, release
or tag is implied. The source bundle retains both Level 3 branches for the
existing local-credentials push workflow.

## Measured final runs

| Route | Frames / native samples per type | Equal APU writes | Equal PCM bytes | Changed / exact valid images |
| --- | ---: | ---: | ---: | ---: |
| recording | 1200 | 2103 | 3839808 | 720 / 479 |
| corridor | 3705 | 8144 | 11842628 | 585 / 3119 |
| blizzard | 821 | 1537 | 2629004 | 437 / 383 |

Total: 5726 frames per build. All changed pixels are confined to the large fish in the eligible movement state. 448 attack/damage images remain exact. The 3 paired empty initial screenshots are excluded only from pixel comparison, with their native samples still paired.
