# Approved 0.22.2 on main

The user approved the complete Demonic Palace continuation and requested its
merge on 2026-10-27 (America/New_York). The initial source matched approved handoff
`14333fd96068a8c5f03a5e92cda00edd500ac303`. Final PR head
`f2fa8a6434d07a61b7779befd6d27e47abd52175` adds only a validation portability fix for cross-filesystem
temporary packs, preserving all install bytes. Runtime approval is
for `918b3d123062eaef62df8c18dbc53a2c3444c531`. PR [#26](https://github.com/kgrant191/holy-diver-hd/pull/26)
merged at `d70883b632f3b207b82feabdf84534951aec4798`. The merge tree equals the validated PR source tree.

The PR build and main merge build passed. Both actual downloaded Actions ZIPs
were independently checked for archive digest, CRC, flat layout, no nested ZIP,
exact 126-file set and all expected SHA-256 hashes. Records are in
`evidence/level5_adoption/pr_artifact.json` and `main_artifact.json`; merge
identifiers and build results are in `merge.json`.

All 126 reviewed installation files remain exact, including the frozen installed
README. Adoption bookkeeping changes source documentation only. Existing native
Mesen state/audio comparisons, consecutive flash checks and 1-up source checks
remain applicable without another gameplay replay.

The approved work includes the recorded Palace rooms/enemies, green slime
ceiling, ascent continuity, Thunder/dragon flash scenery, THUNDER H and both
1-up appearances. The green upper-hall figurine is visually verified; the lava
item also increments lives 6 to 7. Coverage ends in 8A6E; later rooms and the
boss remain unfinished. No release tag or GitHub Release was created.

Start subsequent requested work from approved main 0.22.2. Historical review
labels elsewhere record the original delivery state.
