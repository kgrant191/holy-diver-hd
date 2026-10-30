# Holy Diver HD working instructions

## Current work

Version 1.0.0 is approved and merged on main through PR #31. The user approved the prepared version, public requirements and Windows/macOS installation instructions on 2026-10-30 and explicitly requested the merge. Preserve all 174 approved installation files, including INSTALL.txt and the bundled README.txt. PR and main validation records are maintained in the PR description and docs/development/RELEASE_1.0.0.md. Creating the v1.0.0 tag or GitHub Release requires a separate publication request.

The tested emulator is MesenCE 2.2.1. The full-file ROM SHA-1 is FE2FCD0AD334D792DB16535D09F3AB9FB2BEA3AC. State only tested compatibility. The HD pack folder must exactly match the ROM filename without .nes, with hires.txt directly inside.

## Preserve the approved pack

- Keep the exact approved 0.32.0 artwork, hires mappings, audio, patches, native gameplay and timing.
- INSTALL.txt and its built README.txt are now approved. Preserve all 174 installation bytes. Every non-README installed file retains its exact 0.32.0 SHA-256.
- Preserve historical version manifests. The 1.0.0 manifest and expected-build manifest differ from 0.32.0 only in README.txt.
- Keep the install ZIP flat. Include no ROM, emulator, source bundles or development notes.
- Public instructions live in README.md, docs/INSTALLATION.md and INSTALL.txt. The build copies INSTALL.txt into the pack as README.txt.
- Preserve historical documentation under docs/development. See [historical instructions](docs/development/AGENTS_HISTORY.md), [art direction](docs/ART_DIRECTION.md) and [testing](docs/TESTING.md) before changing relevant artwork or behavior.

## Build and verification

Run `python3 build.py` and `python3 scripts/verify_release.py`; retain the full historical validator chain. Download the actual Actions artifact and verify all 174 root files, SHA-256 values, CRC and flat layout. Confirm all 173 non-README files remain exact to 0.32.0.

Artwork changes require relevant controller-driven live MesenCE replays. Use one Mesen process at a time. Preserve native masks, rule priority and specific sprite conditions. Never edit RAM to manufacture evidence.

## Repository workflow

Use focused branches and preserve unrelated work. Text-only changes may use the GitHub integration directly. Artwork-heavy work uses ZIP-wrapped incremental bundles and the user's local Git credentials. Open PRs, verify checks and the actual artifact, and merge after user approval. Publish release tags or GitHub Releases only when explicitly requested.

Commit source and compact evidence; exclude ROMs, emulator binaries, savestates, raw frame dumps and build archives. Existing rollback folders are build inputs: preserve them. User instructions in the active conversation take precedence over these defaults.
