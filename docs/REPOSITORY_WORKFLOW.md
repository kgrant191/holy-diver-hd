# Repository workflow

Repository: kgrant191/holy-diver-hd. main starts at development version 0.0.1 using the approved historical v15.1 artwork. Use temporary branches for later screen or character work and merge accepted changes into main. Keep release changes in CHANGELOG.md and current state in STATUS.md.

## Semantic versioning

VERSION is the build's source of truth. Start at 0.0.1 while the game pack is in development:

- Patch (0.0.1 → 0.0.2): compatible bug fixes and small visual polish.
- Minor (0.0.2 → 0.1.0): new screens, features or substantial compatible additions; reset the patch to zero.
- During 0.x, document any compatibility changes explicitly and bump the minor version.
- 1.0.0: the completed, tested game pack, approved for release by the user.
- After 1.0.0, patches fix compatible issues, minors add compatible functionality, and majors (2.0.0) introduce breaking compatibility changes. A large amount of new art alone does not require a major bump.

Historical v12–v15.1 build names remain unchanged in original assets and evidence. They are provenance labels, not semantic versions. Keep version-bearing documentation, INSTALL.txt and approved pack hashes aligned with VERSION. Review intentional pack changes before refreshing evidence/approved-pack-sha256.json; retain evidence/v15.1-pack-sha256.json as the original import reference.

## Publishing and storage

GitHub integration access does not automatically authenticate shell git commands. Use the authorized GitHub tools when shell credentials are absent. Never store account tokens in the repo.

Build ZIPs are excluded from commits. CI produces a downloadable artifact. Releases/tags can be added for accepted versions when requested; this import does not configure automatic release publishing.

Rollback folders remain because current build and validation scripts read them. Git deduplicates unchanged file content. Migrate those dependencies deliberately before removing old snapshots.

Keep raw captures/audio/video under local work/ or the existing handoff archives. Commit selected evidence and verification reports alongside visual changes. Build outputs are disposable; source art and registration metadata are not.
