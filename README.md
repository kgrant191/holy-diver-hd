# Holy Diver HD

Mesen HD-pack artwork and reproducible source for the translated NES Holy Diver ROM. **Approved development version: 0.4.1. Adoption into main pending.** Built on the historical v15.1 artwork baseline, with the approved title and ledge corrections.

Version 0.4.1 fixes the cave entrance showing clouds before its far wall appears, replaces the flyers with brown winged demons that face their travel direction and drop downward arrows, and restores the red enemies to faceless pink-shell forms with pulsing crimson lobes. See [review repairs](docs/SCREEN2_1_REVIEW.md). Approved by the user on 2026-10-23; main remains at 0.3.5 until the PR and Actions artifact checks complete.

Version 0.4.0 adds Stage 2 screen 1: a volcanic Gothic backdrop, native gold platforms, palette-driven lava and Blizzard ice, flying imps, three tumbling lava-creature poses, destructible gold blocks and the exit cliff. Reuses approved Randy, HUD, pickups and defeat effects. See [screen notes](docs/SCREEN2_1.md) and [actual Mesen comparison](evidence/screen2_1/comparison.png). The feature and subsequent repairs are approved together in 0.4.1 on `feature/screen-2-1`.

Version 0.3.5 adds the large red HP and blue Magic flasks with shared mappings for their identical native graphics copies. Previous artwork, including the confirmed standing-leg repair, remains exact. See [recovery items](docs/RECOVERY_ITEMS.md) and [live comparison](evidence/recovery_items/comparison.png).

Version 0.3.4 corrects the disconnected knee/shin introduced by the rejected 0.3.3 boot repair. The forward standing leg is registered as one continuous thigh, knee, shin and boot in both costumes and directions. Crouching and all other poses stay exact. See [standing leg correction](docs/RANDY_LEG.md) and [live comparison](evidence/randy_leg/comparison.png).

Version 0.3.2 keeps the Blizzard ascent backdrop filled across the vertical wrap and preserves Randy's HD silhouette through the final white/gray fade. The native repeated bell, ornaments and flash timing remain intact. See [transition repair](docs/BOSS1_TRANSITION.md) and [live comparison](evidence/boss1_transition/comparison.png).

Version 0.3.1 fixes the Blizzard pause menu's original-font R/D letters and enables Mesen's sprite-limit removal so the boss fireball stays complete on crowded scanlines. The option applies automatically while this pack is loaded. See [review fixes](docs/BOSS1_REVIEW.md) and [live comparison](evidence/boss1_review/comparison.png).

Version 0.3.0 adds the first boss and Blizzard chamber: six native boss poses, crouched/standing fire, white hit flashes, progressive defeat, brass organ pipes, the bell and spell collectible, and the ascent/announcement into Stage 2. Existing Randy/HUD artwork follows the identical graphics-bank copies used in the transition. See [boss notes](docs/BOSS1.md) and [live comparison](evidence/boss1/comparison.png). The complete feature, including the subsequent fixes and recovery pickups, was approved by the user on 2026-10-23 for adoption through [PR #4](https://github.com/kgrant191/holy-diver-hd/pull/4).

Version 0.2.1 revises screen 1-4 with a front-facing 1-up figurine in both colors and a continuous Gothic wall with complete arches. The tree court retains the approved entrance tree, native branches and floor, and shared HD ghoul poses. See [revision notes](docs/SCREEN1_4_REVIEW.md) and [live comparison](evidence/screen1_4_review/comparison.png). Approved by the user on 2026-10-23; adoption and Actions artifact verification are tracked in [PR #3](https://github.com/kgrant191/holy-diver-hd/pull/3).

Version 0.1.1 sharpens the standing ghoul and covers both crouching attack phases for normal/Twin Fire Randy. Its 0.1.0 base adds the third chapel section, with a solid masonry backdrop, stained-glass windows, reinforced blocks, a gold serpent ornament, a six-pose rolling ghoul and two-pose blue flying skulls. Includes the entrance and screen-2 overhaul, shared Randy/weapon art, bracelet pickup and pause icon, defeat effects, and stage/lives cards. The rest of the game remains work in progress.

![Randy arm repair in actual Mesen captures](evidence/arm_repair/Holy_Diver_v15_Comparison.png)

## Build

Use Python 3.12:

```sh
python -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements.txt
python build.py
python scripts/verify_release.py
```

On Windows, activate the virtual environment with its Scripts/Activate.ps1 file. No ROM or emulator is required to build or validate.

Output: `build/Holy_Diver_HD_v0.4.1.zip`, with the contents of `build/Holy_Diver_(Tr)/` at the ZIP root. The version comes from VERSION. GitHub Actions uploads that directory's files directly, so its downloaded artifact ZIP also exposes hires.txt and the assets after one extraction. It does not contain a second ZIP. Development artifacts are for testing; official GitHub Releases require the user's explicit release approval.

## Versioning

Development starts at **0.0.1**. Increment the patch for compatible fixes or small visual polish (0.0.2), and the minor for new screens or substantial features (0.1.0). Reserve **1.0.0** for the completed, tested game pack. After 1.0.0, major versions indicate breaking compatibility changes. Historical v12–v15.1 labels remain in provenance and evidence; they are not semantic releases.

## Install

Extract the ZIP directly into the Mesen HD-pack folder matching the ROM filename, for example `Mesen/HdPacks/Holy_Diver_(Tr)/`. hires.txt must be directly inside that folder. Enable NES HD packs and fully close/reopen the ROM.

Supported translated ROM SHA-1: `fe2fcd0ad334d792db16535d09f3ab9fb2bea3ac`. Tested with MesenCE 2.2.1. Supply the ROM and emulator separately; neither is included. See INSTALL.txt for the original pack instructions.

## Project files

| Path | Purpose |
| --- | --- |
| AGENTS.md | Instructions for future coding-agent sessions |
| STATUS.md | Approved work, known limits and next task |
| CHANGELOG.md | Development version and release history |
| VERSION | Current semantic version used by the build |
| art/ | Source images, registered sprites, metadata and font license |
| scripts/ | Builders, validators, Lua replay templates and capture tools |
| rollback/ | Exact older pack inputs used by the current build |
| evidence/ | Compact live reports/captures and approved pack hashes |
| docs/ | Art direction, testing setup, repository workflow and prior notes |
| test_states/ | Tracked setup guide; ignored local emulator inputs |

## Continuing work

Start against this repository and read AGENTS.md and STATUS.md. Use a focused branch, test affected visuals in Mesen, and keep main at the approved version. Update status and changelog when work is accepted.

CI checks mappings, tile bounds, conditional ordering, approved asset hashes and the audio patch. It does not replace live emulator testing. Read docs/TESTING.md.

Historical rollback inputs are retained for reproducibility. Future Git commits provide additional version history. See docs/REPOSITORY_WORKFLOW.md and NOTICE.md.
