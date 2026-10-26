# Holy Diver HD working instructions

Read README.md, STATUS.md, docs/ART_DIRECTION.md and docs/TESTING.md before changing the project. Update STATUS.md and CHANGELOG.md when work changes the approved build or leaves a concrete follow-up.

## Current review branch

- 0.11.2 on `feature/level3-opening` adds the actual round enemy shot, coherent two-row branches and the boot collectible. Approved main remains 0.10.2. See `docs/LEVEL3_DETAILS.md` and `evidence/level3_detail/`.
- Preserve the complete native wood masks, including partially visible top-row cells. The reported round shot is 0694/FF301116; 068A–068D/FF301525 form the boot collectible (not Randy’s boots). The 0.11.1 attribution of 06B6–06B9 as the reported projectile was incorrect. Preserve those historical sprites pending a separate identification; do not use them to claim round-shot coverage. Branches 0768–0770 use complete two-row registration with exact native alpha contours.
- The `.mmo` input embeds the correct starting state and matches the project's ROM. Use `run_mesen_movie.py` with the stock MesenCE 2.2.1 native core, configuration shim and synchronized screenshot observer. Do not replace it with MesenAI. Input bytes remain outside Git.
- NES endFrame fires before video submission; asynchronous HD decode can otherwise produce a one-frame capture mismatch. `sync_movie_capture.cpp` waits for the pending decode and then calls the original screenshot routine without changing pixels or native state.
- New Level 3 scenery rules are limited to the three measured room pointers; actor aliases use proven native CHR copies. Preserve original conditional priority and the last shared Stage 2 fallback block.

## Approved latest repair

- The user approved 0.10.2 and authorized its merge on 2026-10-24 ("approved. merge it"). PR #12 is merged; main is the approved 0.10.2 baseline. The repair keeps HD Randy through the three final Breaker pickup fades. Preserve all 93 reviewed installation bytes. Approval and artifact records are in `evidence/breaker_randy/`. See `docs/BREAKER_RANDY.md` and `evidence/breaker_randy/validation.json`.

## Approved main and source history

- Approved continuation baseline: **0.10.2 on `main`**. The user approved the delivered boss and defeat/pickup repairs on 2026-10-24; see `evidence/boss2_review/approval.json`. Preserve all 93 reviewed installation files exactly, including the original brown ceiling, accepted stairs and shared Stage 2 artwork. PRs #8–#11 are merged into main after the user authorized all four merges.
- The current source handoff includes `feature/screen2-4`, `feature/screen2-5`, `feature/screen2-6` and `feature/2-boss`. Older refs stay at their earlier source commits; screen2-6 includes the 0.9.0 approval record. No release/tag is requested. Boss artwork is approved; PRs #8–#11 merged in dependency order (screen2-4 → screen2-5 → screen2-6 → 2-boss), retargeting each successor to main. PR/main builds and all downloaded artifacts pass. See `evidence/stage2_adoption/merges.json` and the four `main_artifact.json` records. The 0.10.1 repair covers both gold defeat-fade palettes and removes the dead boss silhouette during Breaker flashes; preserve the native room flash.
- Finished artwork must be reused for matching native identities/palettes. `build_shared_stage2.py` runs last, after all specific rules. Verified new-bank aliases retain pose conditions; put broad aliases after existing specific rules. Never globally clear scenery. See `docs/SCREEN2_6.md` and `docs/BOSS2.md`.

## Preserve approved behavior

- Current approved development version on main: 0.10.2. Includes all approved Stage 2 work through the boss and Breaker fixes, plus the Stage 2 cave/lava flow (PR #6) and vertical cave with blue eye tears (PR #7). The user explicitly authorized both merges on 2026-10-24 ("merge it"); both are merged. PR/main Actions builds and actual downloaded 84/85-file artifacts were verified. See STATUS.md and evidence/screen2_3_review/approval.json. Imported artwork baseline: historical v15.1. Preserve approved artwork and native gameplay except for the user's requested change.
- Preserve the title sequence: clean splash, first Start reveals PRESS START, second Start starts play. Preserve the exact Entrance_SFX_Priority.ips bytes.
- Randy's normal/Twin Fire art is shared across matching native identities. Fix shared assets/mappings where appropriate instead of adding needless room-specific copies.
- The red winged-skull drop is a bracelet. Its collected Start/pause-menu icon must use the same bracelet artwork.
- Preserve native collision, animation timing, inventory, lives and audio. Use controller input for visual tests; do not patch RAM to fabricate evidence.
- Pose-specific hires.txt rules precede broader rules: Mesen uses the first matching replacement. Preserve native per-sprite flip behavior and OAM footprints.

## Build and verification

- Python 3.12; install requirements.txt. Run `python build.py` and `python scripts/verify_release.py` against the approved pack manifest.
- For visual changes run relevant live Mesen replays and inspect actual captures in both directions and affected palettes. Atlas mockups alone are not evidence of runtime correctness.
- For limb repairs, inspect the whole joint and silhouette against a clear backdrop. Alpha connectivity and pixel-exact rendering alone missed the rejected 0.3.3 knee/shin break; register adjoining limb sections together and check their outline across tile boundaries.
- For platform artwork, test the complete span, far-left stop, and slow walk-off at the right edge. A grounded sprite can overhang collision tiles; do not extend solid artwork to the full OAM or boot silhouette.
- Perform routine emulator testing here when inputs/tools are available; do not ask the user to perform it instead.
- Only one Mesen process at a time. Do not replace its pack or overwrite the audio-capture library during a run.
- The first screenshot after loading a state can be empty. endFrame OAM can describe the next pose; screenshots are authoritative for visual claims.
- Report coverage precisely. Stage cards 1–3 are verified in live play; cards 4–6 remain mapped but untested.
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
