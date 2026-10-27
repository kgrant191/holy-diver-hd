# Approved 0.20.5 adoption

On 2026-10-27 (America/New_York), the user approved the complete delivered
0.20.5 pack and asked to make a bundle and merge. That authorizes PR creation
and merging the cumulative work after verification; no further permission is
needed. Approval bookkeeping changes no installed files. The 119 hashes in
`evidence/0.20.5-pack-sha256.json` remain authoritative for the delivered pack.

GitHub main was still version 0.15.0 when checked. The eight feature branches
below were absent and there were no open PRs. Per the repository's existing
artwork handoff workflow, the user imports and pushes the ZIP-wrapped incremental
bundle with their local Git credentials. PRs and merges cannot occur before
those source refs exist remotely. Do not represent bundle preparation as a merge.

## Dependency order

| Order | Branch | Version | Scope |
| --- | --- | --- | --- |
| 1 | feature/golden-temple | 0.16.3 | Exterior/interiors, Overdrive, masonry, entry bounds, drops and stairs |
| 2 | feature/golden-temple-courtyard | 0.17.0 | Next hall, outdoor courtyard, wings and fire chain |
| 3 | feature/golden-temple-staff | 0.18.0 | Staff/menu, scrolling hall and outdoor sentinel arena |
| 4 | feature/temple-dragon-items | 0.19.1 | Dragon, visible drops, decorative columns and stray ornament |
| 5 | feature/golden-temple-boss | 0.20.2 | Final halls, tower boss, doorway, all stair copies and victory transition |
| 6 | feature/tree-potion-cleanup | 0.20.3 | Chapel branch joins and brighter health jug |
| 7 | feature/boss-entry-repair | 0.20.4 | Missing Level 2 wall-boss entrance palettes |
| 8 | feature/background-continuity | 0.20.5 | Missing Poison Moss scrolling-background guards |

After push, confirm all remote heads equal the bundle manifest. Open the first
PR against main and each successor against the preceding branch. Inspect each
Actions build and download its actual artifact. Require ZIP CRC validity, flat
installation layout, no nested ZIP, and every hash in that branch's expected
pack manifest. Merge in dependency order using merge commits and expected-head
guards, retargeting each successor to main. Check the actual main build/artifact
after each merge. Preserve unrelated remote changes; inspect a moved base/head
instead of forcing it. Record PR URLs, head/merge SHAs, Actions runs and artifact
checks in `evidence/stage4_adoption/` when they actually exist.

Local full build/manifest verification and the existing paired live evidence
cover the approved content. No new emulator replay is needed for documentation
only approval changes. The potion's earlier cleanup tests were artwork/alias
checks rather than a dedicated collection replay, and the temple victory movie
acquired Thunder without casting it. Preserve those stated coverage limits.

Main remains 0.15.0 until the authorized merges complete. Do not create release
tags or GitHub Releases; the user requested source adoption only.
