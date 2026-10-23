# 0.0.2 approved — corrected ledge boundaries and single-extraction artifact

Approved by the user in chat on 2026-10-22. Approval changes documentation only; all runtime assets retain the tested bytes.

The first candidate extended the shelves too far right and did not provide a continuous visible surface at the far left. Its stationary-pose check confused Randy's sprite overhang with the collision span. That visual conclusion is superseded by the full-traversal tests below; historical captures in evidence/title_screen_1_1 retain the earlier geometry.

The revised shelf caps span HD X0–128 at Y192 (upper) and X0–160 at Y544 (lower). Using the user's two supplied states, each replay holds left for 120 frames, settles at the left stop, then pulses right two frames out of eight through the edge. Actual screenshots were inspected at the left stop, across the span, immediately before falling, and during descent. The caps support the far-left standing pose and end before the falling character. Native sprite overhang is preserved.

Two paired MesenCE 2.2.1 replays cover 920 frames per build. All 920 samples of each memory type (RAM, PPU, OAM), APU writes, and 1,469,580 common PCM bytes per case match exactly. The first downward frame remains 353 for the upper shelf and 417 for the lower. Only controller input is used; no RAM writes. Installed pack hashes were checked before/after each run in the isolated emulator directory. The replayed pack differs from the final build only in README.txt, subsequently updated for the one-extraction instructions; all runtime bytes are the tested bytes.

Evidence: evidence/ledge_boundaries/verification.json, comparison.png, four full captures, and before/after installed manifests. The comparison uses unretouched, nearest-neighbor crops of paired emulator screenshots. Reproduce using scripts/run_ledge_boundary_qa.py, scripts/verify_ledge_boundary_qa.py and scripts/export_ledge_boundary_preview.py.

The title backgrounds and title rules are byte-identical to the first 0.0.2 candidate. Its fresh/reset title checks remain valid: clean splash, first Start reveals PRESS START, second Start begins play, and unchanged stage cards. The original five-case report contains 6,440 frames per build and 1,610 paired samples; its title checks and behavior comparisons remain valid, but its claim that the old shelf geometry was visually correct does not.

Against approved 0.0.1, only EntranceScene.png, Title_HD.png, Title_Intro_HD.png and README.txt differ; all other 67 pack files are byte-identical. The validator restricts background changes to the prompt footprint and the two corrected shelf rectangles. Editable ORA layers reconstruct the installed scene exactly.

Actions now uploads build/Holy_Diver_(Tr)/ directly. GitHub wraps those files in the downloaded artifact ZIP; hires.txt, PNGs and the remaining assets are at its root, with no inner ZIP. The separate local build ZIP retains the same single-extraction layout.

---

# v15.1 — Randy rear arm repair

The approved source art ended the rear arm at the cape in five poses. A generated
elbow/forearm/fist cutout is registered into those poses in both costume atlases.
All changed pixels lie inside measured native OAM coverage. All other atlas
pixels are exact v15; hires.txt, all other PNGs, and the IPS are byte-identical.

Native controller replays cover both costumes facing right and left, standing
casts, airborne idle/casts, running and upward casting. Additional screen-2
combat and death replays verify the corrected frozen death pose and unchanged
explosions and lives cards. No RAM or inventory edits were used.

Across 2,040 emulated frames, 1,558 paired RAM/PPU/OAM captures match exactly;
APU writes and sound command logs are identical and recorded PCM matches.
The arm repair changes only the intended two Randy atlases. Unchanged run and
upward poses render byte-identically in the sampled frames. Both directional
casts and the airborne variants render the completed rear arm in live Mesen.

Evidence: evidence/arm_repair/verification.json and selected before/after
screenshots. Reproduction: scripts/run_arm_qa.py, scripts/run_v15_qa.py,
scripts/verify_arm_qa.py. The older v15 tests below describe the pre-repair build.

---

# v15 verification in MesenCE 2.2.1

Target translated ROM SHA-1: fe2fcd0ad334d792db16535d09f3ab9fb2bea3ac.
The approved v14.1 pack is the comparison baseline. The ROM is unchanged.

## Paired replay results

Five controller-only replays total 3,780 frames: fresh start plus reset (1,800),
normal death (720), Twin Fire death (720), enemy combat (360), and the owned
bracelet pause menu followed by resume (180). Every one of the 1,890 paired
snapshots of each type—CPU RAM, PPU memory and OAM—is byte-identical. Sound
commands and APU traces match exactly. Four complete PCM captures match; the
title/reset recording has one additional shutdown buffer in v15, with the
entire common 5,749,992-byte PCM prefix identical.

The title/reset replay has 708 identical rendered frames. Its 192 changed frames
are confined to the stage-introduction intervals. The fresh-start and reset
Stage 1 cards are pixel-identical, showing CURSED CHAPEL and RANDY × 3. The
approved title artwork, prompt flow and subsequent entrance remain unchanged.

Normal and Twin Fire deaths show matching gold compact/expanded effects and an
HD remaining-lives card. The native count falls to two; the card displays
RANDY × 2. The health/magic display uses the existing approved HD glyphs and
life pips. Native sprite blinking, positions and effect timing are retained.

Enemy combat changes only eight sampled rendered frames, the two explosion
phases for two defeated enemies. The pause menu and bracelet remain identical.
In the menu replay, the 21 changed frames occur after frame 140, when Randy dies
after resuming; they are the intended updated effect, not a menu regression.

The paired data and exact changed-frame lists are in evidence/v15/verification.json.
Separate every-frame recordings of enemy and normal death are used for motion
review/video so the native alternating Randy/effect frames are not lost by
sampling every second frame.

## Build and source integrity

All approved v14.1 PNG files and the exact approved audio IPS are byte-identical.
The pack contains 28 atlases, 2,231 tile mappings, 48 background-layer rules and
204 conditions. Image references, bounds and conditional priority validate.
The eight old room-specific effect mappings are replaced by complete coverage
of both phases, including all 16 identical native CHR-bank copies. The 256
native effect tile identities were verified byte-for-byte in the supported ROM;
art/v15_native_bank_verification.json records their hashes. No replacement audio
or new ROM patches are present.

## Coverage and limits

The six stage names are transcribed from the supported translated ROM's text
table. Stage 1 is directly verified after fresh start and reset. Stages 2–6 are
mapped from ROM data but have not yet been reached in live play. Life counts
0–9 have their own conditional layers; counts 3 and 2 are directly exercised.
Do not describe this as a full-game playthrough or verification of every future
Randy transformation. The earlier reported original-Randy reversion was not
reproduced; its approved v14 fallback remains intact.

All new UI text layers are selected using native nametable digits and complete
stage/lives signatures plus a palette and render-state guard. The pack changes
presentation only. The new frame may be visible during the native blank loading
frame once the card data is ready; native counters, inputs and transition timing
remain exactly equal to the baseline.

The comparison contains actual emulator captures and enlarged, unpainted crops.
The MP4 contains actual captured frames and native recorded audio with a label
band, nearest-neighbor enlargement and ordinary video compression. Source,
generated assets/prompts, exact rollback packs and selected evidence are retained.

## 0.1.0 screen-1-3 review candidate

Three new-state routes: 2,160 frames per build; 1,080 paired RAM/PPU/OAM samples and identical APU writes/full PCM. All six ghoul poses appeared with both native mirror states. New window/block/ornament art, both flying-skull poses, impact and shared death/lives transitions were inspected in actual Mesen captures. Fresh/reset title plus earlier crypt regression: 2,160 further frames per build, 630 paired memory samples, 270 byte-identical screenshots, identical APU writes/common PCM. The title capture differs only by one final shutdown audio buffer (3,196 bytes). See evidence/screen1_3/ and docs/SCREEN1_3.md. Approval remains pending.

## Screen 1-4 — 0.2.0 review candidate

The five native-controller routes cover 4,780 frames per build and 2,390 paired samples per memory type. All RAM/PPU/OAM samples, APU events and complete PCM agree. Both normal and Twin Fire 1-ups disappear on collection and raise the native life count from 3 to 4. All six ghoul poses occur in both directions. The full drop reaches the lower floor; every active-room nametable tile/palette pair is mapped (145 distinct pairs across the descent). The slow shelf traverse records first downward OAM motion at sampled frame 592. The left transition has 185 byte-identical previous-room captures.

Regression adds 2,880 frames, 990 samples per memory type and 468 byte-identical screenshots across title/reset, earlier crypt and nave. APU events and overlapping PCM are exact; the nave baseline contains one extra 3,196-byte shutdown audio buffer. Total paired coverage is 7,660 frames and 3,380 samples per memory type. Reports and actual screenshots: evidence/screen1_4/. The enemy contact sheet places approved 0.1.1 on the left and 0.2.0 on the right of each pair, enlarged 2× with nearest-neighbor sampling.

Build/reference/bounds/priority checks pass. All 71 prior files other than hires.txt and README.txt are byte-identical; stripping the added mapping sections recovers approved 0.1.1 hires.txt. The local candidate archive contains all 75 expected root files, exact hashes, valid CRC and no nested ZIP. Actions verification remains pending the user’s bundle push and review PR. Main stays approved 0.1.1.

## 0.2.1 wall/figurine revision results

Five paired routes: 4,780 frames per build, 2,390 identical samples per memory type, exact APU events and equal-length byte-identical PCM. Both front-facing pickup colors were observed and collected through controller input; lives increased 3→4. All six ghoul poses appeared in both directions. The left transition retains 185 byte-identical previous-room screenshots.

Earlier title/reset, crypt combat and nave: 2,880 frames, 990 identical samples per memory type, 468 byte-identical screenshots, exact APU events and equal-length identical PCM. Total accepted paired coverage: 7,660 frames per build and 3,380 samples per memory type. Every playback is driven by controller input, without RAM writes.

The first baseline left-transition audio capture ended early while its memory/frame capture completed. It was retained locally as an excluded capture and that one unchanged route was repeated. The replacement capture passes the original exact audio checks; no tolerance was relaxed. All other accepted cases are from the original paired runs.

The rebuilt pack matches all 75 expected hashes. Pixel checks confirm changes are limited to the decorative wall rectangle, 46 cleared wall cells and four figurine cells. All other pixels, native shelf cells, mapping bytes and the IPS are unchanged. Actual gameplay comparisons and reports are in evidence/screen1_4_review/. Main remains approved 0.1.1.
