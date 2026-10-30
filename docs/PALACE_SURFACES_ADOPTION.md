# Approved Palace surfaces and Overdrive book — 0.32.0

PR [#30](https://github.com/kgrant191/holy-diver-hd/pull/30) is merged, adopting the approved later Level 5 masonry and Level 3 Overdrive spell book. The pushed artwork commit and merge tree match the reviewed source. The PR build and independently downloaded artifact pass all 174 approved hashes, CRCs and flat installation layout. Preserve every reviewed installation byte, including INSTALL.txt and the installed README. Follow the PR description for main validation runs and artifact checks; see `docs/PALACE_SURFACES_ADOPTION.md` and `evidence/palace_surfaces_adoption/`.

Continue final cleanup before preparing the completed release. No release/tag was created. Historical review and pending-merge labels below are superseded by this adoption.

- Reviewed artwork: `ac5f6fdde59cb19c56c4d2d6f6b607522c5fceec`.
- Approved PR head: `eb196858945e00843c6384b4ea26be9c8749212d`.
- Merge: `a903b111f5f101d78f59b2f402143d27bf78a659`.
- Identical PR/merge tree: `d5ae18f423fcac0f8583f3e891261b1290753df8`.
- [Successful PR build](https://github.com/kgrant191/holy-diver-hd/actions/runs/41044145510).
- [Main merge build](https://github.com/kgrant191/holy-diver-hd/actions/runs/41045213755).
- [Current post-merge verification record](https://github.com/kgrant191/holy-diver-hd/pull/30).

The original seven-route, 58,334-frame replay coverage, 9,505 paired native
samples, complete APU/PCM comparisons, platform-edge test and clean-build
records remain in `evidence/palace_surfaces/`. The PR artifact independently
matches all 174 approved files. Its digest, CRC and flat layout are recorded
in `evidence/palace_surfaces_adoption/pr_artifact.json`.

This adoption commit changes documentation and compact evidence only. Runtime
artwork, mappings, audio, patches, VERSION, INSTALL.txt and both approved
manifests remain byte-identical. Post-merge checks are recorded in the linked
PR description so completing those records does not change the approved pack.
