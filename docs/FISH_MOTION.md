# Fish motion consistency — 0.12.1 review

The user clarified that the fish looked blurry or glitchy **during movement**.
The investigation therefore preserves the existing design and does not apply
the earlier proposed sharpening pass or replace the generated source art.

## Confirmed defect and repair

The small fish is registered from the two large-fish poses. The old registration
adaptively reduced each small pose to its own 64-color palette. That changed all
227 visible pixels across the pair, even though the resized source changes only
near the fin. Rapid animation alternated the stationary head/body colors.

The repaired registration preserves the exact first small pose, uses its palette
for the alternate pose and copies its pixels wherever the resized source is
unchanged. Only 32 visible pixels now differ between poses, inside HD columns
2–7; the head/body at columns 9–31 remains exact. Native fin timing, dimensions,
OAM mirroring, movement and gameplay stay unchanged. Both large-fish poses remain
byte-identical. This is a color-registration repair, not new painted artwork.

The two existing alternate-pose atlas cells retain their reserved locations at
X256 and X272, Y0. Deduplicating the now-identical head cell would move later
spell/scenery cells, so the builder deliberately preserves those slots. Only
Stage3_Lava_Tiles_2x.png and installed README.txt differ from 0.12.0; hires.txt and
the other 98 installation files remain exact. The archive still contains 100
root files. The approved 0.11.2 manifest is untouched.

## Large-fish blinking and coverage limit

Consecutive captures show that the first large fish is stable during ordinary
movement. After a Breaker hit, native OAM contains eight fish cells on frames
374/376/378/380 and no fish cells on 375/377/379/381. The screenshot observer
captures the preceding displayed frame, so image visibility trails that sample
by one frame. This is native hit blinking; no pack mapping can draw an omitted
sprite. It is preserved, not described as a repaired HD defect.

The user's recording does not establish that every perceived motion artifact on
their display is reproduced here. This patch addresses the confirmed small-fish
color shimmer; it does not claim to remove native damage flashes or diagnose
display/filter ghosting.

## Verification

Replay the unchanged 3,705-frame corridor movie at stride one against the
retained 0.12.0 pack and the new pack, using the synchronized stock MesenCE 2.2.1
runner. Setup and preload variables are documented in LEVEL3_OPENING.md.

```sh
python scripts/verify_fish_motion.py --before "$BEFORE" --after "$AFTER" \
  --out evidence/fish_motion/validation.json
python scripts/export_fish_motion.py --before "$BEFORE" --after "$AFTER" \
  --out Holy_Diver_HD_v0.12.1_Motion.mp4
```

The verifier compares every RAM/PPU/OAM/view sample, all APU writes and complete
PCM, bounds every changed image pixel to the alternate small-fish sprite cells,
checks actual full sprite matches in both small-fish directions and both large
poses, and proves the original hit-blink pattern remains native. Exact results
are retained in evidence/fish_motion/validation.json. The video uses consecutive
actual captures with integer nearest-neighbor enlargement, normal speed and
explicitly labeled quarter speed. No frame blending or interpolation is used.

0.12.1 is a review candidate on feature/level3-lava. Main remains 0.10.2;
approved continuation baseline remains 0.11.2. No approval, push, PR, merge,
release or tag is implied by the handoff.

Measured result: 3705 paired samples for each native memory type, 8144 identical APU writes and 11842628 identical PCM bytes. 562 changed images stay inside the alternate small-fish cells; 3142 valid images remain exact. The one empty initial screenshot is paired and excluded from pixel comparison. Both small poses match their registered sources in both directions, and both large poses match unchanged.

## Follow-up — 0.12.2

The new movie establishes native horizontal hover jitter in the large fish without a hit. The earlier observation of stable artwork referred to consistent tile registration; it did not measure horizontal positional stability. The native hit blink is a separate effect. See BIG_FISH_MOTION.md for the reproduced issue and graphics-only hover correction.
