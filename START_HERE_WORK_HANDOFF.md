# Current correction: v15.1

Randy's rear arm was incomplete in the approved source art (not a tile mapping
failure). art/randy_arm_patch.png completes elbow, forearm and fist in poses
0, 4, 6, 8 and 9 for normal and Twin Fire palettes. build.py includes this repair.
Only the two Randy atlases and README change in the distributable. All other
assets, hires.txt and audio IPS remain exactly v15. rollback/approved_v15 is
the exact pre-repair pack. See evidence/arm_repair and TEST_RESULTS.md.

# Resume from v15 death effects and intermission polish

The user approved v14.1's screen-2 art and matching bracelet menu icon, then
requested completion of enemy/Randy explosions, the post-death lives screen,
and the stage-name/lives card after starting or resetting.

Read README.md, TEST_RESULTS.md, INSTALL.txt and art/v15_registration.json.
Current build: python build.py. Exact approved base: rollback/approved_v14_1.

Effect phase 0 uses tiles 64–6B in a 3x3 ring with an empty center. Phase 1 uses
6C–73 in the native sparse 4x4 footprint. Both use palette FF301116 and are now
shared across rooms. Their positions/timing remain native. New atlas 27 is
Death_Bursts_2x.png. All prior PNGs are unchanged.

Intermission text uses CHR 1Fxx, background palette 0F213029. The full stage header
and lives-name signatures, plus the background-render shadow bit $FE&08, scope
new art. Blank 1F00 must also be cleared or the old black HD tile hides the frame.
The health/magic glyphs are duplicated in every even CHR bank; map those copies
only under the lives-card signature. Do not broaden a lone menu/nametable probe.

Stage names come from the translated ROM table near file offset 1B3F8. All six
are mapped to separate typography layers; the live replay covers Stage 1 only.
Life count layers are selected from the game's digit at 2254 (stage card) or
21D4 (post-death card), preserving actual counts. Three and two are tested live.

Keep the v14.1 bracelet/menu changes and Randy death fallback. Preserve the
exact approved v12 audio IPS including the thunder mask, plus the clean title
splash / first Start reveals PRESS START / second Start begins play sequence.
Never substitute the earlier two-byte audio patch or overwrite approved art.
