# Current status

Updated: 2026-10-23 (America/New_York).

## Current review candidate

**0.4.0** on `feature/screen-2-1`, based on approved main `19176d026eb5670523ad8358d82447c63732d506` (PR #4, 0.3.5). The user requested Stage 2 screen 1 and supplied four states covering its start, hot lava, frozen lava and later platforms. No merge or public release is authorized for this candidate.

The exterior uses new volcanic scenery and enemies, plus approved gold-ground texture and existing Randy/HUD/item/effect artwork. The native lava palette selects hot/ice textures, including the original thaw flashes. A rendered-sky tile condition suppresses the custom panorama on actual black frames; the CPU shadow of PPUMASK alone was one frame out of phase during this effect. Breakable blocks and the exit cliff remain tied to their native tiles. Small heart/magic drops and 1-up figurines reuse approved art in this CHR bank; large flasks and defeat rings already had shared mappings.

The build has 82 root files. Only `hires.txt` and `README.txt` change among the 80 approved files; all 78 previous runtime files stay byte-identical. `evidence/0.3.5-pack-sha256.json` preserves the approved baseline. The historical `approved-pack-sha256.json` filename describes this branch's review candidate and does not grant approval. Full results and limitations are in `docs/SCREEN2_1.md` and `evidence/screen2_1/verification.json`.

The six exterior replays pass across 6,040 frames per build, with exact RAM/PPU/OAM and APU events, identical common PCM, and 350 exact native black frames. The neutral cast/thaw case accounts for 92 of those black frames. Both imp directions and all three unmirrored lava-creature poses are observed. The crossing reaches native scroll 1280 and the exit cliff, then death/respawn; next-room entry is not claimed. Two audio captures differ only by one shutdown buffer (3,192 and 3,196 bytes).

Earlier boss/reward/recovery regression adds 2,470 frames per build, 1,235 exact native-memory samples per type and 1,169 exact previous-scene screenshots. Total coverage is 8,510 frames per build and 7,275 paired samples per memory type. A single inconsistent reward-fade capture in the initial run did not recur in a complete repeat with unchanged candidate bytes; the discrepancy and its unconfirmed cause are retained in `evidence/screen2_1/reward_capture_repeat.json`. Final reports pass without exceptions. The local install ZIP has all 82 verified root files; the user push, PR and actual Actions artifact check remain pending.

## Current approved version

**0.3.5**, approved by the user on 2026-10-23 for adoption through [PR #4](https://github.com/kgrant191/holy-diver-hd/pull/4). Reviewed artwork commit: `9a290ec8a9160fbbd387cf7ab1ec954da9b11199` on `feature/1-boss`, based on previous approved main `2427afd4739f273bf527810edcfae93e6592e344` (0.2.1). The user approved the final visuals, then confirmed the Actions artifact packaging and explicitly authorized the merge ("verified, merge it"). No release tag or GitHub Release is authorized.

The user confirmed the 0.3.4 leg repair ("thats fixed") and supplied two more states showing original HP/Magic flasks. The approved 0.3.5 build adds red HP and blue Magic bottle artwork for native tiles 49–4C, distinct from the already-covered small heart/crystal drops. Shared mappings cover all sixteen byte-identical CHR copies; live coverage is the supplied chapel/tree states. The confirmed Randy artwork and every other previous asset remain exact. See `docs/RECOVERY_ITEMS.md`.

The user confirmed the 0.3.2 transition fix, then reported a missing standing toe while crouching was correct. They rejected the 0.3.3 repair because the isolated boot fit cut the knee/shin outline. The 0.3.4 correction registers the full forward standing leg as one continuous piece in both costumes. It also keeps the idle knee rule active at the left-screen edge by probing the torso directly above it. Other poses and rule priority stay exact. See `docs/RANDY_LEG.md`.

The user confirmed the 0.3.1 fireball fix. The 0.3.2 transition repair extends the bell-room backdrop through the complete native vertical wrap and adds the missing bank-00 white/gray fade palettes for Randy. The repeated bell and ornaments occur in the original sequence; the HD backdrop previously ended beneath them. See `docs/BOSS1_TRANSITION.md`. The final boss feature and repairs are approved in 0.3.5.

The 0.3.1 review repair fixes the Blizzard menu's R/D font fallback and enables Mesen's supported sprite-limit removal to keep the boss fireball complete. It applies to rendering throughout this pack; it does not edit the ROM or controller route. Existing artwork stays exact, with two menu glyphs added in formerly empty boss-atlas cells. See `docs/BOSS1_REVIEW.md`.

Approved art covers the six native boss poses in both directions, hit-palette flashes, the native 36-tile progressive disappearance, the organ hall, Blizzard bell chamber, spell pickup, ascent and announcement. The Stage 2 title/lives card is now verified in live play. Known Randy/HUD copies in the announcement and Stage 2 graphics banks reuse the approved art. Stage 2 scenery/enemies remain future work.

The pack contains 80 root files. The requested standing-foot repair also changes the two Randy atlases. Along with hires.txt and README.txt, these are the only changed files among the 75 main-baseline files; 71 existing runtime files stay exact. Five PNGs are added. The old expected manifest is retained as `evidence/0.2.1-pack-sha256.json`. `evidence/approved-pack-sha256.json` now records the approved build. `evidence/0.3.5-reviewed-pack-sha256.json` preserves the exact reviewed candidate. Approval bookkeeping changes only the installed README.txt; all 79 other pack-file hashes remain identical. See `docs/BOSS1.md` and `evidence/boss1/verification.json` for reproduction and coverage.

Initial 0.3.0 live checks passed: 11,030 frames per build, 9,500 paired RAM/PPU/OAM samples per type, identical APU events and common PCM. Earlier-room regression has 1,470 identical screenshots; the unchanged Stage 2 card adds 184. Two runs have one shutdown-buffer audio-tail difference, documented in the reports. All six boss poses are observed in both directions.

The 0.3.1 repair checks pass: 7,460 frames per build, 5,930 paired native-memory samples per type and identical APU/common PCM. Title, crypt and tree images remain exact; 39 nave images restore only native sprites dropped on overflowing scanlines. The rest of the 1,470 earlier-room captures are identical. See `evidence/boss1_review/verification.json` and `regression.json`.

The 0.3.2 repair checks pass: 5,500 frames per build and paired samples per native-memory type, identical APU events and common PCM. Both pickup directions/costumes keep the HD silhouette through all 24 final fade frames. Background differences replace only previously black bell-room pixels. The full 649-image fireball replay remains exact. See `evidence/boss1_transition/verification.json`.

The rejected 0.3.3 repair passed 6,460 frames of bounds, source-pixel and native memory/audio checks, but those checks missed the visibly broken knee/shin join. Its report under `evidence/randy_foot/` remains historical evidence of preservation, not visual acceptance. The new correction adds whole-leg contour checks and live views against a clear backdrop.

The 0.3.4 checks pass across 6,940 frames per build and paired samples per native-memory type, with identical APU events and common PCM. The normal/Twin Fire entrance routes each have 248 pixel-exact complete-leg captures and 75 unchanged crouching/crouch-cast captures. Each clear-background route adds 177 complete-leg captures in both directions. Changes are confined to the standing forward leg in 2,736 images; 4,197 other valid screenshots remain identical. Both frame-616 offscreen-hand cases retain the complete registered leg. The clear-background close-ups were visually inspected in both directions and costumes. See `evidence/randy_leg/verification.json` and `comparison.png`.

The 0.3.5 pickup checks pass across 1,320 frames per build and paired samples per native-memory type. HP restores 5→6 and Magic restores 10→50 in both normal/Twin Fire costumes; neutral cases preserve each item's native expiry. All 405 changed screenshots are confined to the flask tiles, 909 valid images remain identical, and 397 captures match the complete bottle artwork exactly. APU events and common PCM match; the HP neutral case has one 3,192-byte shutdown-tail difference. All 77 previous files other than mapping/readme remain byte-identical. See `evidence/recovery_items/verification.json` and the live comparison.

The user pushed the reviewed artwork, and PR #4 was opened. Actions run [40004314865](https://github.com/kgrant191/holy-diver-hd/actions/runs/40004314865) passed: all 80 pack hashes matched, and all 80 files were uploaded directly from the extracted pack directory. The user downloaded artifact [12523247888](https://github.com/kgrant191/holy-diver-hd/actions/runs/40004314865/artifacts/12523247888) and confirmed that one extraction exposes 80 files including hires.txt, with no nested ZIP. The assistant retrieved the artifact through the integration but could not independently extract it because the execution environment was unavailable. Archive-layout confirmation is attributed to the user; CI verified file hashes before upload. See `evidence/boss1/approval.json`.

Use 0.3.5 as the approved baseline for subsequent work. Preserve the ZIP-wrapped incremental Git bundle workflow for artwork-heavy updates; small text-only approval changes may use the integration. No additional emulator replay is required for the install-text update.

## Previous approved version

**0.2.1**, approved by the user in chat on 2026-10-23 ("approved"). Reviewed commit: `ad0e91c4921648c3d67bb426feb41be519a60eb9` on `feature/screen1-4`. Preserve its screen-1-4 tree court, front-facing blue/ivory 1-up figurines, continuous Gothic wall and shared HD enemies as the accepted visual baseline.

The user pushed the reviewed artwork commit to `feature/screen1-4`. [PR #3](https://github.com/kgrant191/holy-diver-hd/pull/3) was merged into main at `2427afd4739f273bf527810edcfae93e6592e344` after approval and artifact verification. The downloaded main Actions artifact (run 39967379016, artifact 12507780985) contains all 75 expected root files with matching hashes and no nested ZIP. No release tag or GitHub Release was created.

Approval bookkeeping changes only README.txt in the installed pack. All 74 runtime files remain byte-identical to the approved review. `0.2.1-reviewed-pack-sha256.json` preserves the reviewed bytes; `0.2.1-pack-sha256.json` preserves the approved installation bytes. Historical reports and captures remain unchanged. See evidence/screen1_4_review/approval.json for the bookkeeping check.

Live verification of the approved art: 7,660 frames per build, 3,380 paired samples per memory type, exact APU events and equal-length identical PCM. Both pickup palettes award lives 3→4. Earlier title/crypt/nave regression has 468 identical screenshots; the previous-room transition adds 185 unchanged captures. The pack has 75 root files and no nested ZIP. The actual Actions artifact check is recorded in PR #3.

## Previous approved version

**0.1.1**, approved by the user in chat on 2026-10-23 ("approved. pushed") for adoption through PR #2. It adds the third chapel section, sharpens the standing purple ghoul while retaining the rolling frames, and supplies both crouching attack phases in normal/Twin Fire colors and both directions. No release tag or GitHub Release is published.

The pushed candidate is `2251a0419f6cf6e6b832dcac84ebf8ac49662357`. Actions run 39893523922 passed; its actual downloaded artifact contains 73 root files with all reviewed hashes matching and no nested ZIP. Approval bookkeeping changes only README.txt in the installed pack. All 72 other files remain identical. `evidence/0.1.1-reviewed-pack-sha256.json` preserves the reviewed bytes and `evidence/0.1.1-pack-sha256.json` retains its approved installation bytes.

## Previous approved version

**0.0.2**, approved by the user in chat on 2026-10-22 and adopted as the main baseline through PR #1 (`fix/title-screen-1-1`). It repairs the title prompt background, aligns both entrance rock shelves across their full native spans, and removes the nested ZIP from Actions artifacts. This is an approved development build; no release tag or GitHub Release is published.

The previous candidate's rightward shelf extensions were incorrect. Full traversals from the user's two save states establish upper HD X0–128 at Y192 and lower X0–160 at Y544. Continuous caps now cover the far-left standing position and stop before Randy falls. Do not use the earlier stationary-boot footprint as the platform boundary.

Current ledge verification: 920 frames per build, with 920 paired RAM/PPU/OAM samples and identical APU writes/common PCM. Both replays walk fully left, hold, and step slowly right through the fall. See evidence/ledge_boundaries/verification.json and comparison.png. The title PNGs and rules retain the exact bytes tested in the original fresh/reset title replay. Against previous approved 0.0.1, only three background PNGs and the pack README change; 67 files remain byte-identical.

## Previous approved baseline

Development version **0.0.1**, using the approved historical v15.1 artwork, accepted after the Randy arm repair (the user said "much better"). Initial GitHub import preserves all 70 runtime pack files exactly; README.txt only updates the development version and source location. Version 1.0.0 is reserved for the completed, tested game pack.

Completed: entrance/title sequence, entrance environment, known shared Randy poses and normal/Twin Fire palettes, screen-2 crypt environment/enemies, bracelet drop and matching pause icon, shared defeat-effect phases, stage/lives cards, post-death HUD, and rear forearm/hand repair.

## Historical arm verification

- Both Randy costumes, left/right, standing and airborne idle/horizontal casts. Sampled run/upward frames unchanged.
- Screen-2 combat and Randy death retain RAM/PPU/OAM, APU writes and recorded audio. Frozen death pose includes the repaired arm.
- 2,040 emulated frames and 1,558 paired state captures: evidence/arm_repair/verification.json and TEST_RESULTS.md.
- Earlier v15 tests covered fresh start/reset, normal/Twin Fire death, enemy combat and collected-bracelet pause/resume. Historical results remain in evidence/v15/.

## Approved screen-1-3 work

`feature/screen-1-3` builds approved **0.1.1**. The 0.1.0 screen addition was refined in response to the standing-ghoul and crouching-attack feedback. This is an approved development build, not a public release.

Three supplied states cover the third chapel section. Native inspection and movement revealed emerald/ruby windows, reinforced blocks, a large gold background ornament, a purple ghoul with two standing and four rolling poses, and small blue flying skulls with two poses. The approved addition supplies a solid nave wall behind those details. Randy, weapons, HUD, stone blocks, the large gold flying enemy and the expanding death rings reuse existing art.

The initial screen implementation adds 87 scoped tile rules, three palette checks, one background rule and two runtime PNGs. The 0.1.1 repairs add 50 pose rules and 66 signatures. Two Randy atlases and the nave atlas gain sprites only in previously unused cells: all earlier Randy poses and all four rolling ghoul frames are pixel-identical. The pack still has 73 files. Removing the marked screen-1-3 and review-fix sections recovers the approved mapping file exactly. The current approved build manifest is `approved-pack-sha256.json`. `0.0.2-pack-sha256.json` retains the approved baseline, and `0.1.0-pack-sha256.json` retains the prior review candidate.

Initial 0.1.0 candidate: 2,160 frames across the new states, 1,080 paired samples per memory type and identical full PCM. Regression: 1,800 fresh/reset title frames plus 360 earlier-crypt combat frames, all 270 screenshots identical; title audio has one shutdown buffer of length difference with identical common PCM.

The 0.1.1 live checks cover both crouching attack phases, both directions and both costumes, plus all three chapel routes: 2,640 frames per build and 1,560 paired RAM/PPU/OAM samples. Changes are confined to the requested sprites; 64 rolling-attack screenshots remain exactly identical. See `evidence/review_fixes/verification.json` and the live comparison images. Fresh/reset title and earlier crypt regression add 2,160 frames, 630 paired samples per memory type and 270 identical screenshots, with equal-length identical audio. Total reviewed coverage is 4,800 frames per build. Existing 0.1.0 evidence remains under `evidence/screen1_3/`.

The user has authorized adoption through PR #2. Use 0.1.1 as the baseline for the next requested change. Preserve the agreed bundle/push workflow for artwork-heavy updates. See `docs/REVIEW_FIXES.md` for reproduction commands and limits.

## Known limits

- This is a partial HD overhaul, not a finished all-stage pack.
- All six stage names and life counts 0–9 are mapped; live card coverage is Stages 1–2 and counts 4/3/2. Stages 3–6 remain untested.
- Native player tiles $33–$35 are now measured and covered as crouching wind-up legs. Tile $3C remains unclassified; investigate only when a live route uses it.
- The earlier report of Randy fully reverting to original art during death was not independently reproduced. Shared defeat fallbacks exist, and current recorded death poses remain HD.
- Old scripts remain for provenance. build.py is the supported build entry point.
- Full historical capture runs/videos and original savestates remain in the prior source/handoff archives. The repository keeps compact evidence and exact rollback inputs.
