# Holy Diver HD

Mesen HD-pack artwork and reproducible source for the translated NES Holy Diver ROM. **Review candidate: 0.1.0. Approved main: 0.0.2.** Built on the historical v15.1 artwork baseline, with the approved title and ledge corrections.

The 0.1.0 candidate adds the third chapel section, with a solid masonry backdrop, stained-glass windows, reinforced blocks, a gold serpent ornament, a six-pose rolling ghoul and two-pose blue flying skulls. Includes the entrance and screen-2 overhaul, shared Randy/weapon art, bracelet pickup and pause icon, defeat effects, and stage/lives cards. The rest of the game remains work in progress.

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

Output: `build/Holy_Diver_HD_v0.1.0.zip`, with the contents of `build/Holy_Diver_(Tr)/` at the ZIP root. The version comes from VERSION. GitHub Actions uploads that directory's files directly, so its downloaded artifact ZIP also exposes hires.txt and the assets after one extraction. It does not contain a second ZIP. Development artifacts are for testing; official GitHub Releases require the user's explicit release approval.

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
