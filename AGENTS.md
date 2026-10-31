# Holy Diver HD working instructions

## Current work

The user requested repair of the original graphics shown in Holy_Diver_HD(20261031-143722).mmo and publication of v1.0.1 on 2026-10-31. This authorizes the focused repair, necessary PR/merge and release publication. Work is based on released 1.0.0 at 53ab5788efb6b078227ac8e9915d78316983278a. Preserve v1.0.0 and its assets.

The repair is limited to room 9DEE / mode 14: animated lava curtain, its frozen form and frozen lava pool, moss ceiling details and four native platform-contour cells. Reuse existing art and animation. Only hires.txt and the versioned README change among the 174 old install files; one 16x16 atlas adds the missing contour cell, for 175 total. Preserve every other old file exactly. See docs/development/RELEASE_1.0.1.md.

The workflow may publish only v1.0.1 after a validated main push, using the exact artifact from that build. PRs and other versions cannot publish. If the tag/release already exists, do not overwrite it automatically. No further permission is needed for this requested release.

The tested emulator is MesenCE 2.2.1. ROM SHA-1: FE2FCD0AD334D792DB16535D09F3AB9FB2BEA3AC.

## Preserve previous approvals

- Keep the exact approved 0.32.0 artwork, hires mappings, audio, patches, native gameplay and timing.
- The current repair is the authorized exception to the earlier 174-file freeze. Preserve all 172 old non-text assets and exact removable 1.0.0 mapping text.
- Preserve historical manifests. The 1.0.1 manifest pins all 175 candidate files; future approval bookkeeping must keep those reviewed installation bytes exact.
- Keep the install ZIP flat. Include no ROM, emulator, source bundles or development notes.
- Public instructions live in README.md, docs/INSTALLATION.md and INSTALL.txt. The build copies INSTALL.txt into the pack as README.txt.
- Preserve historical documentation under docs/development. See [historical instructions](docs/development/AGENTS_HISTORY.md), [art direction](docs/ART_DIRECTION.md) and [testing](docs/TESTING.md) before changing relevant artwork or behavior.

## Build and verification

Run `python3 build.py` and `python3 scripts/verify_release.py`; retain the full historical validator chain. Download the actual Actions artifact and verify all 175 root files, SHA-256 values, CRC and flat layout. Confirm all 172 old non-text assets remain exact to 1.0.0.

Artwork changes require relevant controller-driven live MesenCE replays. Use one Mesen process at a time. Preserve native masks, rule priority and specific sprite conditions. Never edit RAM to manufacture evidence.

## Repository workflow

Use focused branches and preserve unrelated work. Text-only changes may use the GitHub integration directly. Artwork-heavy work uses ZIP-wrapped incremental bundles and the user's local Git credentials. Open PRs, verify checks and the actual artifact, and merge after user approval. Publish release tags or GitHub Releases only when explicitly requested.

Commit source and compact evidence; exclude ROMs, emulator binaries, savestates, raw frame dumps and build archives. Existing rollback folders are build inputs: preserve them. User instructions in the active conversation take precedence over these defaults.
