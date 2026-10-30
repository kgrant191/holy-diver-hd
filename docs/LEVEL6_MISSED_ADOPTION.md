# Approved final Level 6 rooms — 0.31.0

PR [#29](https://github.com/kgrant191/holy-diver-hd/pull/29) is merged, adopting the approved final recorded Level 6 rooms in 0.31.0. The pushed head and merge tree match the reviewed handoff. PR and main builds pass; both independently downloaded artifacts match all 173 approved SHA-256 hashes, CRCs and flat installation layout. Preserve every reviewed installation file, including the installed README and original green enemy standby.

- Approved head: `6c6cfe5c455aa716cf7fe2d7b7c82ece46db99c3`.
- Merge: `87f6259dc01486951c70cfd8b7aedae91bc87bfa`.
- Identical tree: `f472e8afe39fe013c8ab901d7d91a0a5f631be3b`.
- PR build: https://github.com/kgrant191/holy-diver-hd/actions/runs/40995011266
- Main merge build: https://github.com/kgrant191/holy-diver-hd/actions/runs/40995578007
- Both downloaded artifacts contain exactly the 173 approved files, without nested ZIPs.

The full 8998-frame native/audio comparison, separate ledge route and original
clean-build evidence remain in `evidence/level6_missed/`. Adoption evidence is
in `evidence/level6_missed_adoption/`. Bookkeeping changes source documentation
only; all runtime artwork, audio, mappings, patches and installation notes stay
byte-identical to the user-approved pack.

Next work is final cleanup before preparing the completed release. No release/tag was created. Start focused cleanup branches from this approved main. Historical review and pending-merge labels below are superseded by this adoption. See docs/LEVEL6_MISSED_ADOPTION.md and evidence/level6_missed_adoption/.
