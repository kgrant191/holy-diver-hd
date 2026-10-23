# Holy Diver HD working instructions

Read README.md, STATUS.md, docs/ART_DIRECTION.md and docs/TESTING.md before changing the project. Update STATUS.md and CHANGELOG.md when work changes the approved build or leaves a concrete follow-up.

## Preserve approved behavior

- Current approved development version: 0.2.1, accepted in chat on 2026-10-23; see STATUS.md for approval and verification. Imported artwork baseline: historical v15.1. Preserve approved artwork and native gameplay except for the user's requested change.
- Preserve the title sequence: clean splash, first Start reveals PRESS START, second Start starts play. Preserve the exact Entrance_SFX_Priority.ips bytes.
- Randy's normal/Twin Fire art is shared across matching native identities. Fix shared assets/mappings where appropriate instead of adding needless room-specific copies.
- The red winged-skull drop is a bracelet. Its collected Start/pause-menu icon must use the same bracelet artwork.
- Preserve native collision, animation timing, inventory, lives and audio. Use controller input for visual tests; do not patch RAM to fabricate evidence.
- Pose-specific hires.txt rules precede broader rules: Mesen uses the first matching replacement. Preserve native per-sprite flip behavior and OAM footprints.

## Build and verification

- Python 3.12; install requirements.txt. Run `python build.py` and `python scripts/verify_release.py` against the approved pack manifest.
- For visual changes run relevant live Mesen replays and inspect actual captures in both directions and affected palettes. Atlas mockups alone are not evidence of runtime correctness.
- For platform artwork, test the complete span, far-left stop, and slow walk-off at the right edge. A grounded sprite can overhang collision tiles; do not extend solid artwork to the full OAM or boot silhouette.
- Perform routine emulator testing here when inputs/tools are available; do not ask the user to perform it instead.
- Only one Mesen process at a time. Do not replace its pack or overwrite the audio-capture library during a run.
- The first screenshot after loading a state can be empty. endFrame OAM can describe the next pose; screenshots are authoritative for visual claims.
- Report coverage precisely. Stage cards 1–2 are verified in live play; cards 3–6 remain mapped but untested.
- Review and document intentionally changed files before updating expected hashes; do not weaken validation merely to make it pass.

## Repository workflow

- Keep main as the approved baseline. Use focused branches for later changes unless the user directs otherwise. Preserve unrelated work.
- Use this chat for bugs, priorities and approvals. Do not introduce GitHub Issues or a TASKS.md backlog unless requested. Push changes on the requested branch and open a PR for review; merge only after user approval.
- For artwork-heavy changes, prepare a ZIP-wrapped incremental Git bundle and exact fetch/push commands. The user pushes with their local Git credentials; use the GitHub integration for PRs and Actions. Avoid transferring large encoded images through tool arguments or chat. Small text-only changes may use the integration directly.
- Actions artifacts are development test builds. Publish release tags or GitHub Releases only when explicitly requested; reserve the completed release for 1.0.0.
- Upload the extracted pack contents to Actions artifacts, never a ZIP inside the artifact ZIP. One extraction must expose hires.txt and the installable assets.
- Follow semantic versioning in docs/REPOSITORY_WORKFLOW.md. Keep VERSION, INSTALL.txt, README.md, STATUS.md, CHANGELOG.md and approved pack hashes consistent when approving a new version. Reserve 1.0.0 for the completed, tested game pack.
- Commit source art, mappings, scripts, compact evidence and notes. Exclude ROMs, emulator binaries, savestates, credentials, raw frame dumps and build archives.
- Local test-input names/checksums are in test_states/README.md; input bytes are ignored by Git.
- Existing rollback folders are build inputs and provenance. Do not delete them until their consumers have deliberately been migrated.
- CI validates/builds without a ROM. Live emulator review remains separate for visual work.
- User instructions and authorization in the active conversation take precedence over these defaults.
