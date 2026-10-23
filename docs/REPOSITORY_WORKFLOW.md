# Repository workflow

Repository: kgrant191/holy-diver-hd. Approved development version 0.3.5 adds the first boss, Blizzard chamber and recovery pickups through PR #4, following screen 1-4 in 0.2.1 (PR #3), screen 1-3 in 0.1.1 (PR #2), the 0.0.2 title/ledge corrections and the initial 0.0.1 import of historical v15.1 artwork. Use temporary branches for later screen or character work and merge accepted changes into main. Keep release changes in CHANGELOG.md and current state in STATUS.md.

Use the active chat for bug reports, task priorities, feedback and approval. GitHub Issues and a TASKS.md backlog are not part of the current workflow. Prepare each requested change on a focused branch, test it, and open a PR with evidence and an Actions artifact. Revise the same branch for feedback. The user can merge or explicitly authorize the assistant to merge after approval. A proposed version on a branch is a review candidate until accepted.

## Semantic versioning

VERSION is the build's source of truth. Start at 0.0.1 while the game pack is in development:

- Patch (0.0.1 → 0.0.2): compatible bug fixes and small visual polish.
- Minor (0.0.2 → 0.1.0): new screens, features or substantial compatible additions; reset the patch to zero.
- During 0.x, document any compatibility changes explicitly and bump the minor version.
- 1.0.0: the completed, tested game pack, approved for release by the user.
- After 1.0.0, patches fix compatible issues, minors add compatible functionality, and majors (2.0.0) introduce breaking compatibility changes. A large amount of new art alone does not require a major bump.

Historical v12–v15.1 build names remain unchanged in original assets and evidence. They are provenance labels, not semantic versions. Keep version-bearing documentation, INSTALL.txt and approved pack hashes aligned with VERSION. Review intentional pack changes before refreshing evidence/approved-pack-sha256.json; retain evidence/v15.1-pack-sha256.json as the original import reference.

## Publishing and storage

GitHub integration access does not automatically authenticate shell git commands. For artwork-heavy changes, export an incremental Git bundle based on the remote feature head, wrap it in a downloadable ZIP, and provide exact fetch/push commands. The user downloads and pushes using their existing local credentials. Verify the remote head afterward, then manage the existing PR and inspect the actual Actions artifact with the GitHub integration. Small text-only changes may use the integration directly. Do not send large encoded image payloads through chat or tool arguments. Never store account tokens in the repo.

Build ZIPs are excluded from commits. CI produces downloadable artifacts for testing, including PR builds. Upload the extracted pack directory, not the locally built ZIP: GitHub creates the outer artifact ZIP, so its root must contain hires.txt and the pack assets directly. Artifacts have 30-day retention and can be rebuilt from source. Publishing release tags or GitHub Releases is a separate step requiring an explicit user request; there is no automatic release publishing. Version 1.0.0 is reserved for the completed, tested game pack.

Rollback folders remain because current build and validation scripts read them. Git deduplicates unchanged file content. Migrate those dependencies deliberately before removing old snapshots.

Keep raw captures/audio/video under local work/ or the existing handoff archives. Commit selected evidence and verification reports alongside visual changes. Build outputs are disposable; source art and registration metadata are not.
