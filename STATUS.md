# Current status

Updated: 2026-10-23 (UTC).

## Current review candidate

**0.3.1** on `feature/1-boss`, based on approved main `2427afd4739f273bf527810edcfae93e6592e344`. The user requested the first boss and supplied three states covering entry, crouched fire and defeat. Main remains **0.2.1**. Do not merge or publish a release without the user's approval.

The 0.3.1 review repair fixes the Blizzard menu's R/D font fallback and enables Mesen's supported sprite-limit removal to keep the boss fireball complete. It applies to rendering throughout this pack; it does not edit the ROM or controller route. Existing artwork stays exact, with two menu glyphs added in formerly empty boss-atlas cells. See `docs/BOSS1_REVIEW.md`.

Candidate art covers the six native boss poses in both directions, hit-palette flashes, the native 36-tile progressive disappearance, the organ hall, Blizzard bell chamber, spell pickup, ascent and announcement. The Stage 2 title/lives card is now verified in live play. Known Randy/HUD copies in the announcement and Stage 2 graphics banks reuse the approved art. Stage 2 scenery/enemies remain future work.

The pack contains 78 root files. Only hires.txt and README.txt change among the 75 approved files; 73 existing runtime files stay exact. Three PNGs are added. The old expected manifest is retained as `evidence/0.2.1-pack-sha256.json`. The historical `approved-pack-sha256.json` filename describes the candidate on this branch, not approval. See `docs/BOSS1.md` and `evidence/boss1/verification.json` for reproduction and coverage.

Initial 0.3.0 live checks passed: 11,030 frames per build, 9,500 paired RAM/PPU/OAM samples per type, identical APU events and common PCM. Earlier-room regression has 1,470 identical screenshots; the unchanged Stage 2 card adds 184. Two runs have one shutdown-buffer audio-tail difference, documented in the reports. All six boss poses are observed in both directions.

The 0.3.1 repair checks pass: 7,460 frames per build, 5,930 paired native-memory samples per type and identical APU/common PCM. Title, crypt and tree images remain exact; 39 nave images restore only native sprites dropped on overflowing scanlines. The rest of the 1,470 earlier-room captures are identical. See `evidence/boss1_review/verification.json` and `regression.json`.

Use the agreed ZIP-wrapped incremental Git bundle workflow. The user pushes the binary artwork with local credentials; the integration can then create the review PR and inspect the actual Actions artifact. No PR or candidate Actions artifact exists until that push.

## Current approved version

**0.2.1**, approved by the user in chat on 2026-10-23 ("approved"). Reviewed commit: `ad0e91c4921648c3d67bb426feb41be519a60eb9` on `feature/screen1-4`. Preserve its screen-1-4 tree court, front-facing blue/ivory 1-up figurines, continuous Gothic wall and shared HD enemies as the accepted visual baseline.

The user pushed the reviewed artwork commit to `feature/screen1-4`. [PR #3](https://github.com/kgrant191/holy-diver-hd/pull/3) was merged into main at `2427afd4739f273bf527810edcfae93e6592e344` after approval and artifact verification. The downloaded main Actions artifact (run 39967379016, artifact 12507780985) contains all 75 expected root files with matching hashes and no nested ZIP. No release tag or GitHub Release was created.

Approval bookkeeping changes only README.txt in the installed pack. All 74 runtime files remain byte-identical to the approved review. `0.2.1-reviewed-pack-sha256.json` preserves the reviewed bytes; `approved-pack-sha256.json` describes the build with approved installation text. Historical reports and captures remain unchanged. See evidence/screen1_4_review/approval.json for the bookkeeping check.

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
