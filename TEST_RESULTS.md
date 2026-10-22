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
