# Repository workflow

Current approved main is **0.30.1**, adopted through PR #28 on 2026-10-29. Both builds and independently downloaded artifacts pass all 166 approved hashes and flat layout. Preserve reviewed installation bytes. Next: the supplied missed-room movie, cleanup, then completed release. See LEVEL6_ADOPTION.md. Historical baselines below remain for provenance.

Current approved baseline is **0.22.2 on main**, adopted through PR #26 on 2026-10-27. The published source matched the approved handoff and the merge tree matched the validated PR head. PR/main builds and both actual downloaded install artifacts pass all 126 file hashes, CRC and flat layout. Preserve every reviewed installation byte and use focused branches for subsequent changes. See docs/LEVEL5_ADOPTION.md and evidence/level5_adoption/. No release/tag was requested. Earlier workflow history below remains for provenance.

Repository: kgrant191/holy-diver-hd. Approved development version on main is 0.20.5, adopted through PRs #18–#25 on 2026-10-27 after the user approved the complete pack and requested a bundle and merge. All eight PR builds and eight main merge builds, plus all sixteen downloaded artifacts, passed verification. Preserve all 119 reviewed installation files. Use focused branches for subsequent requested work and keep approval/adoption records in STATUS.md and evidence/.

Use the active chat for bug reports, task priorities, feedback and approval. GitHub Issues and a TASKS.md backlog are not part of the current workflow. Prepare each requested change on a focused branch, test it, and open a PR with evidence and an Actions artifact. Revise the same branch for feedback. The user can merge or explicitly authorize the assistant to merge after approval. A proposed version on a branch is a review candidate until accepted.

## Semantic versioning

VERSION is the build's source of truth. Start at 0.0.1 while the game pack is in development:

- Patch (0.0.1 → 0.0.2): compatible bug fixes and small visual polish.
- Minor (0.0.2 → 0.1.0): new screens, features or substantial compatible additions; reset the patch to zero.
- During 0.x, document any compatibility changes explicitly and bump the minor version.
- 1.0.0: the completed, tested game pack, approved for release by the user.
- After 1.0.0, patches fix compatible issues, minors add compatible functionality, and majors (2.0.0) introduce breaking compatibility changes. A large amount of new art alone does not require a major bump.

Historical v12–v15.1 build names remain unchanged in original assets and evidence. They are provenance labels, not semantic versions. Keep version-bearing documentation, INSTALL.txt and approved pack hashes aligned with VERSION. Review intentional pack changes before refreshing evidence/approved-pack-sha256.json; retain evidence/v15.1-pack-sha256.json as the original import reference.

## Completed stacked handoff

The user pushed feature/screen2-2 at 2a60229 and feature/screen2-3 at 29bf3b6, then approval/check bookkeeping was published through the integration. After explicit merge authorization, PR #6 merged first and PR #7 was retargeted to main and merged. The approved baseline is now 0.6.1. Preserve the same ZIP-wrapped bundle workflow for future artwork changes; keep review candidates separate until approved.

## Publishing and storage

GitHub integration access does not automatically authenticate shell git commands. For artwork-heavy changes, export an incremental Git bundle based on the remote feature head, wrap it in a downloadable ZIP, and provide exact fetch/push commands. The user downloads and pushes using their existing local credentials. Verify the remote head afterward, then manage the existing PR and inspect the actual Actions artifact with the GitHub integration. Small text-only changes may use the integration directly. Do not send large encoded image payloads through chat or tool arguments. Never store account tokens in the repo.

Build ZIPs are excluded from commits. CI produces downloadable artifacts for testing, including PR builds. Upload the extracted pack directory, not the locally built ZIP: GitHub creates the outer artifact ZIP, so its root must contain hires.txt and the pack assets directly. Artifacts have 30-day retention and can be rebuilt from source. Publishing release tags or GitHub Releases is a separate step requiring an explicit user request; there is no automatic release publishing. Version 1.0.0 is reserved for the completed, tested game pack.

Rollback folders remain because current build and validation scripts read them. Git deduplicates unchanged file content. Migrate those dependencies deliberately before removing old snapshots.

Keep raw captures/audio/video under local work/ or the existing handoff archives. Commit selected evidence and verification reports alongside visual changes. Build outputs are disposable; source art and registration metadata are not.

## Completed Stage 2 adoption stack (2026-10-24)

The user pushed all four refs and requested PRs/checks. PR #8 initially targeted
main; #9 targeted feature/screen2-4; #10 targeted feature/screen2-5; #11 targeted
feature/screen2-6. Initial builds pass at the pushed heads, and actual downloaded
artifacts independently match all 86, 89, 90 and 93 expected files respectively.
The archive digests, CRCs and flat layouts also pass. Records are in
`evidence/screen2_4/pr_artifact.json`,
`evidence/screen2_5_brown_roof/pr_artifact.json`,
`evidence/screen2_6/pr_artifact.json` and
`evidence/boss2_review/pr_artifact.json`.

After the user instructed “merge them all”, PRs #8 → #9 → #10 → #11 merged
in order, retargeting each successor to main. Each merge tree exactly matches
its reviewed head. All four main builds and actual downloaded artifacts pass
every expected hash, archive digest, CRC and flat-layout check. Main is now
approved 0.10.1. Exact commits/runs are in `evidence/stage2_adoption/merges.json`;
archive checks are in the corresponding `main_artifact.json` records.
No release or tag was created. Adoption bookkeeping changes none of the
93 approved installation files.
