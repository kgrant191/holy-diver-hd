# Build and live testing

## Build (no ROM required)

Use Python 3.12 and requirements.txt. Run `python build.py`, then `python scripts/verify_release.py`. The latter compares every built file against evidence/approved-pack-sha256.json. The original evidence/v15.1-pack-sha256.json remains as the historical import reference: version 0.0.1 changes only README.txt, and all 70 runtime files match exactly. The DejaVu font/license are bundled in art/fonts/.

CI runs these commands and retains the ZIP. Older builders remain for provenance; build.py is the current entry point.

## Live inputs and setup

Use local MesenCE 2.2.1 and the supported translated ROM (SHA-1 fe2fcd0ad334d792db16535d09f3ab9fb2bea3ac). Restore savestates using test_states/README.md. All these inputs are excluded from Git.

Linux replay helpers require a C++ compiler for record_audio.cpp; video export requires ffmpeg. The runners preload /usr/lib/x86_64-linux-gnu/libstdc++.so.6 when starting Mesen. Adapt that runtime path for another host if needed.

Mesen settings: NES HD packs enabled; Port1 Type NesController; AutoConfigureInput false; Lua AllowIoOsAccess true; ScriptTimeout 10. Install the pack in the ROM-matching HdPacks directory before playback.

```sh
python scripts/run_arm_qa.py --mesen /path/to/Mesen --rom '/path/to/Holy_Diver_(Tr).nes' --out work/arms
python scripts/run_v15_qa.py --mesen /path/to/Mesen --rom '/path/to/Holy_Diver_(Tr).nes' --out work/v15
```

run_v15_qa.py accepts --case title|normal|twin|enemy|menu and --capture-every-frame.

Run sequentially; never reinstall the pack during playback. The first loaded-state screenshot can be empty. endFrame OAM may describe the next pose, so evaluate joins from captured images.

Paired tests use identical states, controller routes, emulator settings and capture intervals. Compare RAM/PPU/OAM and sound events for behavior preservation; inspect images/video for visual quality. Do not modify RAM to stage pickups/death.

## Recorded coverage

- Fresh start/reset and native two-press title sequence.
- Screen-2 combat and both death phases; normal/Twin Fire death; collected bracelet pause/resume.
- Repaired rear arm in both directions/palettes, ground and airborne; unchanged run/upward samples.
- Stage 1 card and life counts 3/2. Other card mappings are implemented but not all live-tested.

Detailed results are in TEST_RESULTS.md and evidence/. Full raw runs/videos remain in prior handoff archives. A clone builds immediately; live testing needs separately supplied emulator, ROM and states.
