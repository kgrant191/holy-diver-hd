# Approved Level 6 adoption — 0.30.1

PR [#28](https://github.com/kgrant191/holy-diver-hd/pull/28) is merged, adopting all approved Level 6 work through 0.30.1. The pushed head matches the approved handoff, and the merge tree matches the reviewed source exactly. PR and main Actions builds pass; both actual downloaded artifacts match all 166 approved SHA-256 hashes, CRCs and flat installation layout. Preserve all reviewed installation bytes, including the installed README and original green enemy standby. See docs/LEVEL6_ADOPTION.md and evidence/level6_adoption/.

- Approved head: `3940c3bb54dd82c42788df7de1cdd90031c2e528`.
- Merge: `a36ac26ef3948886756cccfdc2054f1f1e346b25`.
- Identical tree: `1ffd5cabd087614609e147fa14ef26da21358272`.
- PR run: 40988730615; main run: 40989533483.
- Both downloaded artifacts contain exactly the approved 166 files, without nested ZIPs.

Approval/adoption bookkeeping changes source documentation only. Native gameplay
and audio remain as verified in the retained Level 6 replay evidence.

The user has supplied Holy_Diver_HD(20261030-015933).mmo for the remaining rooms and explicitly requests checking its first room too. Work next on a focused branch from this approved main: red corridor 9CA7/mode0C, purple rooms 9D5B/mode08 and 9DD3/mode18; the ending reaches already accepted 9F3B. Then perform the requested cleanup elsewhere before the completed release. No release/tag was created. Historical pending/review labels below are superseded by this adoption.
