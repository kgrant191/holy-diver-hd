# Holy Diver HD v15.1 — Randy arm repair

This finishes the approved screen-2 art with two matching gold defeat-effect
phases and improved intermission typography. Enemy and Randy effects use the
same native CHR identities and their 16 exact bank copies regardless of the room's background palette. The
native sprite positions, animation cadence and flashing remain unchanged.

Stage introductions and post-death lives cards now share a navy-and-gold Gothic
arch. The heading and life count are separate transparent UI layers selected
by the game's nametable values. The translated ROM's six stage names are kept
verbatim apart from uppercase presentation. Life counts zero through nine are
supported; the live tests directly exercise Stage 1 and counts three and two.
The native health and magic display after death reuses the approved HUD cells.

v15.1 completes the missing rear forearm and clenched fist in five poses in
both Randy costume atlases. Only the extracted arm cutout changes; all other
v15 assets, hires rules, and the exact audio IPS remain byte-identical. The two
Start presses on the title, bracelet pickup/menu icon, shared Randy art and
room geometry are retained. The ROM and emulator are not distributed.

## Build and install

Follow INSTALL.txt. Install requirements.txt and run `python build.py`.
The build starts from rollback/approved_v14_1 and produces
build/Holy_Diver_HD_v15_Deaths_and_Stage_Cards.zip. Older source scripts are
retained for provenance; build.py is the current entry point.

Generated source images and prompts are in art/generated. Their registration,
font layout, menu-safe conditions and mappings are built deterministically by
scripts/build_v15_polish.py and scripts/build_arm_repair.py.
The imagegen edit source and prompt are recorded in art/arm_repair.json.
Exact pre-repair v15 is retained in rollback/approved_v15.

## Tests

scripts/run_v15_qa.py accepts --mesen, --rom, --out and optionally --case.
Cases: title (fresh start plus reset), normal death, Twin Fire death, enemy
combat, and the owned-bracelet pause menu. Configure Mesen NES Port1 as
NesController, AutoConfigureInput false, and allow Lua I/O. All replays use
native controller input, with no RAM or inventory edits.

Read TEST_RESULTS.md and evidence/v15/verification.json for results and scope.
Native stage names and life values are never overwritten by this pack. Future
stage cards have matching ROM-derived mappings, but stages 2–6 have not yet been
reached in live play; retain that distinction when reporting coverage.

## Arm repair tests

Run scripts/run_arm_qa.py --out PATH with the same emulator settings. The route
checks both costumes facing right/left, standing and airborne casts, walking,
jumping, and the unchanged upward cast. See evidence/arm_repair/verification.json.
