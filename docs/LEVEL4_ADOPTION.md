# Approved 0.20.5 on main

The user approved the complete delivered 0.20.5 pack and requested its source
bundle and merge on 2026-10-27 (America/New_York). The eight pushed feature tips
matched the approved bundle. PRs #18–#25 merged in dependency order, each successor
retargeted to main after its predecessor. Every merge tree equals the reviewed
branch tree. The final merge is `0b9ee788621f2ca2ef0cc61cb6b3de9ff12e5627`.

All eight PR builds and eight main merge builds passed. All sixteen actual
downloaded GitHub Actions ZIPs were checked independently: archive digest, CRC,
flat file layout, absence of nested ZIPs, exact file set and every expected
SHA-256 hash. Counts progress through 111, 112, 113, 114, 118, 119, 119 and 119 files.
The final pack matches all 119 hashes in `evidence/0.20.5-pack-sha256.json`.

| PR | Branch | Main merge |
| --- | --- | --- |
| [#18](https://github.com/kgrant191/holy-diver-hd/pull/18) | `feature/golden-temple` | `3f72739` |
| [#19](https://github.com/kgrant191/holy-diver-hd/pull/19) | `feature/golden-temple-courtyard` | `a492795` |
| [#20](https://github.com/kgrant191/holy-diver-hd/pull/20) | `feature/golden-temple-staff` | `b47c1de` |
| [#21](https://github.com/kgrant191/holy-diver-hd/pull/21) | `feature/temple-dragon-items` | `b1a8966` |
| [#22](https://github.com/kgrant191/holy-diver-hd/pull/22) | `feature/golden-temple-boss` | `5b98ee7` |
| [#23](https://github.com/kgrant191/holy-diver-hd/pull/23) | `feature/tree-potion-cleanup` | `a1d6692` |
| [#24](https://github.com/kgrant191/holy-diver-hd/pull/24) | `feature/boss-entry-repair` | `4d8ddf3` |
| [#25](https://github.com/kgrant191/holy-diver-hd/pull/25) | `feature/background-continuity` | `0b9ee78` |

Exact PR/head/merge identifiers and timestamps are in
`evidence/stage4_adoption/merges.json`. Each `prNN_artifact.json` and
`mainNN_artifact.json` records its actual Actions run, artifact, digest and checks.
The earlier source bundle remains an exact handoff of the approved feature tips;
main now additionally contains merge and adoption records.

Approval/adoption bookkeeping changes no installation bytes, including the
frozen installed README, so the existing paired Mesen evidence remains valid.
The temple victory movie acquires Thunder without casting it, and the potion
cleanup did not include a dedicated live collection replay. Those coverage
limits remain explicit; this adoption adds no new gameplay coverage.

Main is the approved 0.20.5 baseline. Start later requested work on a focused
branch from main. No release tag or GitHub Release was requested or created.
