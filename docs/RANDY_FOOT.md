# Standing boot repair — rejected 0.3.3 candidate

**Rejected by the user:** the isolated boot fit introduced a cut/discontinuity between the knee and shin. The historical checks below passed because they tested changed-area bounds, source-pixel equality and gameplay preservation, not joint quality. They are not evidence that this repair looked correct. See [RANDY_LEG.md](RANDY_LEG.md) for the 0.3.4 correction.

The user confirmed the Blizzard transition fix, then supplied three close-ups showing Randy's forward toe cropped off when standing in either direction. The crouching pose was correct. This remains part of `feature/1-boss`; main stays approved 0.2.1 pending full feature approval.

## Cause and repair

Idle pose 0 has two native tiles across its lower body: HD X0–31. Its generated forward toe reached X37 before the original registration clipped it to the native footprint. Both mirrored directions therefore showed a flat cut through the boot. The standing-cast and crouching poses have their own registered artwork; they are preserved.

The replacement is a complete compact forward boot, fitted entirely inside HD X18–31/Y44–63 of idle pose 0. It retains the original knee, body, rear boot and ground height. The shin leans slightly back to leave space for the complete toe. There are no added sprites, changed hitboxes, platform extensions or mapping changes.

The built-in imagegen edit and exact prompt are retained in `art/generated/randy_standing_boot_generated.png` and `art/randy_foot/prompt.txt`. Only the isolated lower boot is used from that output. `register_randy_foot.py` applies the recorded source polygon/crop, resizes it to 14×20 pixels, thresholds alpha and quantizes each costume's patch to its existing boot colors. The source reproduces the two retained patch PNGs exactly. It does not replace the generated character's face, body or other limbs in the pack.

`build_randy_foot.py` replaces only that rectangle in the two Randy atlases, after the prior repairs and before boss registration. Existing graphics-bank aliases automatically reuse these corrected cells. The boss builder regenerates the matching monochrome idle silhouettes consistently. Exactly eight monochrome cells change alpha; their RGB values, atlas positions, mappings and other cells remain exact. Actual airborne Blizzard silhouettes are unchanged.

## Verification

The 0.3.2 pack is the baseline. Two new 480-frame entrance routes use the supplied upper-ledge state to cover both costumes and both directions, standing, crouching, crouched casts, running, jumping, horizontal casting and upward casting. The candidate also replays both full Blizzard routes and the boss-fire regression. Those three baselines reuse the exact pinned 0.3.2 captures.

| Route | Frames | Purpose |
| --- | ---: | --- |
| normal | 480 | Normal costume, both facing directions and alternate poses |
| twin | 480 | Twin Fire costume, both facing directions and alternate poses |
| menu_blizzard | 2,300 | Normal pickup, repaired ascent/fade, announcement, Stage 2 and menu |
| reverse_blizzard | 2,550 | Opposite-side Twin Fire pickup, transition, Stage 2 and menu |
| crouch | 650 | Confirmed boss-fire correction and native player poses |

`verify_randy_foot.py` compares all **6,460 paired RAM/PPU/OAM samples per type**, APU events and common PCM, allowing at most one 3,200-byte shutdown buffer difference. Every replay records installed pack hashes before and after playback. Inputs are controller-only; game RAM is never edited. The empty first screenshot after each state load is explicitly excluded from image comparisons.

Every changed screenshot pixel must lie inside the standing pose's lower-boot rectangle, mapped through native sprite positions and flips. All non-idle poses must remain identical. Complete boot captures must match the registered pixels exactly. The two entrance cases must each show the corrected boot in both directions, plus unchanged crouching and other animations. The stored verification report records actual image counts and audio lengths.

All checks passed: 2,382 screenshots change only inside the standing boot, and 4,073 other valid screenshots are identical. The normal and Twin Fire routes each contain 248 pixel-exact repaired standing captures and 75 unchanged crouching/crouch-cast captures. Every native-memory sample and APU event matches. Common PCM is byte-identical; shutdown-tail differences are normal 0 bytes, twin 0 bytes, menu_blizzard 0 bytes, reverse_blizzard 3,196 bytes, crouch 3,192 bytes. No tail exceeds one buffer.

The comparison uses unretouched live captures, cropped and enlarged 3× with nearest-neighbor scaling: right-facing frame 110, left-facing frame 85, Twin Fire frame 110 and unchanged crouching frame 155. These are emulator screenshots, separate from the generated source-art preview.

## Reproduce

Use the supported ROM and MesenCE 2.2.1 settings in `TESTING.md`. Build 0.3.2 separately and retain its extracted pack. Run each pack sequentially with the same states and controller routes:

```sh
python scripts/run_boss1_qa.py --mesen /path/to/Mesen --rom '/path/to/Holy_Diver_(Tr).nes' --pack /path/to/pack --state1 '/path/to/Holy_Diver_HD_1(2).mss' --state2 '/path/to/Holy_Diver_HD_2(3).mss' --state3 '/path/to/Holy_Diver_HD_3(2).mss' --route scripts/randy_foot_routes.json --out work/randy_foot/before-or-after
python scripts/verify_randy_foot.py --before work/randy_foot/before --after work/randy_foot/after --old-pack /path/to/0.3.2-pack --out evidence/randy_foot/verification.json
python scripts/export_randy_foot.py --before work/randy_foot/before --after work/randy_foot/after --out evidence/randy_foot/comparison.png
```

The retained generator result is sufficient to reproduce the patches with `python scripts/register_randy_foot.py`; no further image-generation call is needed. `python build.py` uses the retained patch bytes directly.

## Change boundary and package

The pack still has 79 root files. Only `Randy_Entrance_2x.png`, `Randy_Equipped_2x.png`, `Boss_Tiles_2x.png` and `README.txt` change from 0.3.2. The other 75 files, including the complete `hires.txt`, remain byte-identical. Normal/Twin Fire atlas changes are confined to the 14×20 idle-boot rectangle; monochrome changes are confined to the same silhouette region. Every other pose remains exact.

`evidence/0.3.2-pack-sha256.json` preserves the previous candidate. The historical `approved-pack-sha256.json` filename describes the current review build; STATUS.md is authoritative for user approval. The incremental Git bundle includes all unmerged boss work and fixes. The user pushes it locally; review PR creation and actual Actions artifact inspection follow the push. Do not merge, tag or publish a release pending approval.
