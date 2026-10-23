# Connected standing leg — 0.3.4 review candidate

The user rejected 0.3.3 because Randy's leg looked cut off and disconnected from his boot. The isolated boot registration caused that regression. Main remains approved 0.2.1; this correction stays on `feature/1-boss` for review.

## Cause and correction

The previous patch started below the knee at HD Y44. Its shin shifted left while the original kneecap stayed far right, creating an abrupt six-pixel sideways jump in the outer contour. Alpha was still connected by dark pants pixels, so connectivity, changed-area bounds and pixel-exact rendering all passed despite the visibly broken anatomy.

Register the entire forward leg from the retained generated source as one continuous thigh, knee, shin and boot. The two costume patches now occupy HD X16–31/Y32–63 in idle pose 0, corresponding to native tiles 07 and 09. The rear boot, upper body, other poses, sprite footprint and ground height remain unchanged. Both patches use their existing costume colors. `art/randy_foot/registration.json` records the exact source polygon, crop and target rectangle; `register_randy_foot.py` reproduces the retained PNGs from `art/generated/randy_standing_boot_generated.png`. No new generated image was required.

The live left-room exit also exposed a mapping weakness: idle knee tile 07 used the outer hand tile 05 as its pose probe. At screenshot 616 in both Blizzard routes, that hand is offscreen while the knee remains visible. Probe torso tile 04 directly above the knee instead. This keeps the complete registered leg together at that boundary. Normal/Twin Fire rules and their existing bank/monochrome aliases retain their original priority. Fourteen existing rule scopes change and fourteen definitions are added; all other mapping text and definitions are preserved.

## Verification

Compare against the rejected 0.3.3 pack. The five prior routes reuse captures pinned to that exact pack manifest. Two additional controller-only routes walk onto the tree branch, where the dark backdrop makes the complete leg readable, turn around, and crouch. No RAM edits are used.

| Route | Frames | Purpose |
| --- | ---: | --- |
| normal | 480 | Both directions, standing, crouching/crouched casts, running, jumping and other casts |
| twin | 480 | Same route in Twin Fire colors |
| menu_blizzard | 2,300 | Left exit, normal pickup, ascent/fade, announcement, Stage 2 and menu |
| reverse_blizzard | 2,550 | Left exit, opposite-side Twin Fire pickup, transition and menu |
| crouch | 650 | Confirmed boss-fire correction and native player poses |
| clear_normal | 240 | Normal standing in both directions and crouching against a clear backdrop |
| clear_twin | 240 | Same clear-background comparison in Twin Fire colors |

`verify_randy_leg.py` checks all 6,940 paired RAM/PPU/OAM samples per type, APU events and common PCM, with at most one 3,200-byte shutdown-buffer difference. Installed pack hashes must stay exact throughout every replay. The first empty state-load screenshot is excluded. Screenshot differences must be confined to native standing forward-leg tiles; every other pose remains pixel-identical.

The source contour check rejects 0.3.3's six-pixel knee jump and requires a continuous replacement whose outer edge shifts by at most two pixels between adjacent rows above the toe. Live opaque pixels must match the registered leg in both directions and costumes, including both frame-616 screen-edge cases. These checks supplement visual inspection of the complete knee, shin and boot in actual captures. See `evidence/randy_leg/verification.json` for measured results.

All checks pass: 2,736 changed screenshots are confined to the standing forward leg, and 4,197 valid screenshots remain identical. There are 2,731 pixel-exact complete-leg captures, including 248 per original entrance route and 177 per clear-background route. The complete replay set retains 625 exact crouching/crouch-cast captures. Native memory and APU events match; common PCM is byte-identical. Only `reverse_blizzard` has an audio shutdown-tail length difference (3,196 bytes, within one buffer); all other lengths match. The new source contour's largest adjacent-row shift is one pixel in each costume, compared with six in the rejected repair.

Five changed images have part of the leg covered by the native Blizzard collectible or Stage 2 projectile. Their remaining opaque leg pixels match exactly; every mismatching pixel lies under an earlier-priority native sprite. These captures and the clear-background visual inspection are recorded in `evidence/randy_leg/visual_review.json`. Native occlusion and sprite ordering are preserved.

`comparison.png` contains unretouched live crops enlarged 4× with nearest-neighbor scaling. It shows normal right/left, Twin Fire right, and unchanged crouching against the dark entrance backdrop. Twin Fire left is checked in the same replay. Cropping and enlargement do not alter the captured sprite pixels.

The full unretouched captures `standing_normal.png` and `standing_twin_left.png` retain the surrounding scene. Both directions and costumes were visually inspected in live captures, including the complete toe and knee/shin join.

## Reproduce

Build and retain an extracted 0.3.3 pack, then build this candidate. Run each pack sequentially with MesenCE 2.2.1 and the supported ROM/states from `TESTING.md`:

```sh
python scripts/run_boss1_qa.py --mesen /path/to/Mesen --rom '/path/to/Holy_Diver_(Tr).nes' --pack /path/to/pack --state1 '/path/to/Holy_Diver_HD_1(2).mss' --state2 '/path/to/Holy_Diver_HD_2(3).mss' --state3 '/path/to/Holy_Diver_HD_3(2).mss' --route scripts/randy_leg_routes.json --out work/randy_leg/before-or-after
python scripts/verify_randy_leg.py --before work/randy_leg/before --after work/randy_leg/after --old-pack /path/to/0.3.3-pack --out evidence/randy_leg/verification.json
python scripts/export_randy_leg.py --before work/randy_leg/before --after work/randy_leg/after --out evidence/randy_leg/comparison.png
```

## Package and change boundary

The pack has the same 79 root files. Five change from 0.3.3: the normal/Twin Fire atlases, the matching monochrome cells in `Boss_Tiles_2x.png`, `hires.txt` and `README.txt`. The other 74 files remain byte-identical. Eight monochrome cells change only alpha; their RGB values and all other atlas cells stay exact. Existing fireball, Blizzard font, backdrop and transition repairs are retained.

`evidence/0.3.3-pack-sha256.json` preserves the rejected baseline. `approved-pack-sha256.json` retains its historical filename but describes this candidate; it is not user approval. The ZIP exposes all pack files after one extraction, with no nested ZIP. The ZIP-wrapped incremental Git bundle contains all unmerged boss work through this correction. The user pushes it locally; the review PR and actual Actions artifact inspection follow that push. No merge, release or tag is authorized by this repair request.
