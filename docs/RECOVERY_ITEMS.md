# HP and Magic recovery flasks — 0.3.5 candidate

After confirming Randy's 0.3.4 standing-leg repair, the user supplied two states showing large recovery items still using original sprites. They are different from the small heart/crystal pickups covered earlier. This repair stays on `feature/1-boss`; main remains approved 0.2.1 pending full feature approval.

## Artwork and mapping

The large HP flask uses native tiles 49/4A; the large Magic flask uses 4B/4C. Both use sprite palette `FF301116`, with two vertically adjacent 8×8 native tiles. The native bottles have four transparent rows at the top. The new sprites preserve those rows in their 16×32 HD canvases and fit the complete bottle in X1–14/Y8–31.

The HP bottle has a rounded ruby-red body, narrow neck and antique brass trim. Magic uses a faceted cobalt/cyan vial with matching brass details. The registered 14×24 shapes use thresholded alpha and 32 colors, with no external glow or added sprite geometry.

The built-in imagegen tool created two transparent source assets on 2026-10-23:

- `art/generated/hp_flask_generated.png`
- `art/generated/magic_flask_generated.png`

The complete prompt set and tool provenance are in `art/pickups/prompts.json`. Existing small HP/Magic artwork served only as color/material references. `build_recovery_items.py` deterministically crops, scales and quantizes the sources; `art/pickups/registration.json` retains exact source hashes, crops, target geometry, native patterns and mapping identities. The new runtime atlas is `Recovery_Items_2x.png`.

Reading the supported ROM's CHR data established sixteen byte-identical copies of each native tile, at `0049–004C`, `0249–024C`, through `1E49–1E4C`. The builder adds 64 mappings for those exact identities and the pickup palette. No room condition is needed. Existing mappings remain byte-identical and in their original order. Only the base-bank copies in the supplied chapel/tree states have live coverage; later matching copies are mapped without claiming they have all been observed in play.

## Live checks

The baseline is 0.3.4, including the user-confirmed leg repair. The runner uses the supplied states and controller input only, records every frame, captures native RAM/PPU/OAM, APU writes and PCM, and checks the installed pack hashes before and after each case.

| Route | Frames | Coverage |
| --- | ---: | --- |
| hp_collect | 300 | Red flask in the chapel, Twin Fire costume, jump to collect from the right |
| magic_collect | 300 | Blue flask at the tree, normal costume, collect from the left |
| hp_normal_collect | 240 | Same jumping HP collection after switching to normal costume |
| magic_twin_collect | 240 | Same Magic collection after switching to Twin Fire |
| hp_drop | 120 | Falling/settled red flask through natural expiry without collecting |
| magic_drop | 120 | Settled blue flask through natural expiry without collecting |

Total: 1,320 frames per build. `verify_recovery_items.py` requires identical paired native memory, APU events and common PCM, allowing at most one 3,200-byte shutdown buffer of audio-length difference. All screenshot changes must lie inside the native flask tiles. After collection or expiry every image must remain exact. Each case requires at least 40 captures whose complete opaque bottle pixels match the registered artwork, except the two early jumping HP pickups, which require at least 10.

Magic collection raises RAM `$0490` from 10 to 50 in both costumes. HP collection raises `$0440` from 5 to 6 in both costumes. The initial inference that health 5 was already full was incorrect; the successful jumping collection establishes the actual increase. Native memory/audio equality establishes that this graphics change does not alter the observed pickup effects. See `evidence/recovery_items/verification.json` for measured counts and sound lengths.

The first HP walking route reached the item too late and observed expiry instead of collection. The final route jumps to it sooner: HP's last visible OAM sample is 23, versus 73 without input. Magic's last visible sample is 91 when collected, versus 104 without input. Screenshots lag those OAM samples by one frame. The verifier distinguishes collection from natural expiry and checks both timings.

All checks pass. Among 1,314 valid screenshots, 405 change only inside the native item rectangles and 909 remain exact. The six empty first-load captures are excluded. There are 397 pixel-exact complete-bottle captures; eight HP approach images have native player overlap. Every RAM/PPU/OAM sample and APU event matches. Common PCM is byte-identical; only the neutral HP run differs in shutdown-tail length (3,192 bytes, within one buffer).

The comparison contains unretouched live captures at 3× nearest-neighbor enlargement. Full captures and the clear native bottles were inspected at ordinary display size as well. Randy's confirmed leg and all earlier art remain exact.

## Reproduce

Build 0.3.4 separately and retain its extracted pack, then build this candidate. Pass the HP save as state1 and Magic as state2. The runner requires a state3 argument but these routes do not use it, so the Magic path can be supplied again.

```sh
python scripts/run_boss1_qa.py --mesen /path/to/Mesen --rom '/path/to/Holy_Diver_(Tr).nes' --pack /path/to/pack --state1 '/path/to/Holy_Diver_HD_2(4).mss' --state2 '/path/to/Holy_Diver_HD_3(3).mss' --state3 '/path/to/Holy_Diver_HD_3(3).mss' --route scripts/recovery_item_routes.json --out work/pickups/before-or-after
python scripts/verify_recovery_items.py --before work/pickups/before --after work/pickups/after --old-pack /path/to/0.3.4-pack --out evidence/recovery_items/verification.json
python scripts/export_recovery_items.py --before work/pickups/before --after work/pickups/after --out evidence/recovery_items/comparison.png
```

## Package and preservation

The candidate has 80 root pack files. Relative to 0.3.4, only `hires.txt` and `README.txt` change; one new atlas is added and all 77 other files remain byte-identical. This includes Randy, crouching/casts, the boss, fireball, Blizzard font, backdrop/fades, environments, small pickups and audio patch. Removing the marked recovery-item sections restores the exact previous mapping file.

The local ZIP must contain the complete pack at its root with no nested ZIP. The ZIP-wrapped incremental Git bundle contains all unmerged boss work through 0.3.5 and local push instructions. Actual GitHub Actions artifact verification follows the user's push and review PR; local checks do not substitute for downloading that artifact. No merge, tag or release is performed by this repair request.
