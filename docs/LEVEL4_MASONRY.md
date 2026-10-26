# Golden Temple masonry revision — 0.16.1

The user accepted the backgrounds and outdoor columns, but rejected the flat square foreground blocks and indoor block-stack pillars. This revision preserves the accepted backdrop and exterior column pixels, makes destructible blocks visibly different from solid stone, and replaces the indoor structural supports with carved columns.

## Artwork and registration

- Solid terrain uses one worn, beveled horizontal gold sandstone block over the original four-by-two native cell layout. The original half-block offsets create staggered courses; the old pair of square slabs is removed.
- Breakable blocks use a darker recessed stone face, a chipped gold frame and a clear branching fracture. They are exactly native 0B4E/0B4F/0B50/0B51. Three observed four-cell destruction events prove this identity; see `evidence/level4_masonry/breakable_identity.json`.
- Indoor supports use carved capitals, continuous fluted gold shafts and molded bases. Neighbor conditions find the ends of each native 0B78–0B7B column, including those that cross the floor. Artwork stays inside the original cells and follows native scrolling.
- Existing stair alpha masks remain exact. Upper/lower stone portions are registered together so the lower stair row does not repeat a bright top rim. Native 0B4A–0B4D remain nonsolid scenery; mapping them as solid stone would create floating gold strips outdoors.
- The moving platform shares the new solid stone. Actors, Overdrive, menu lettering, outdoor fluted pillars, both backgrounds, earlier stages and audio retain their previous assets and mappings.

`scripts/build_level4_masonry.py` runs after the unchanged 0.16.0 builder. It adds one atlas and three marked blocks before the old temple mappings, after the room conditions are defined. Scenery changes are restricted to the three recorded temple room/mode pairs. Removing the new blocks recovers byte-exact 0.16.0 hires.txt; all 107 earlier art/audio files remain exact. The flat install now contains 110 files.

The exact selected screenshot was used as the image-edit source. `art/level4_masonry/user_reference.png` retains that input. `concept_only.png` is an image-generated design study, not runtime evidence; its inherited screenshot caption does not establish emulator playback. The three generated material assets and exact built-in tool prompts are retained in `art/generated/level4_masonry_prompts.json`. Final previews and evidence use actual Mesen captures only.

## Verification

Replay the full supplied 8,668-frame movie at stride four with stock MesenCE 2.2.1 and the synchronized observer. Pair it with the retained final 0.16.0 capture. Replay the 1,485-frame controller-only platform route at stride one against its retained 0.16.0 capture. The input and embedded state are unchanged; no RAM writes are used.

```
python build.py
python scripts/verify_level4_masonry.py --before BEFORE --after AFTER --out evidence/level4_masonry/movie.json
python scripts/verify_level4_masonry.py --before EDGE_BEFORE --after EDGE_AFTER --out evidence/level4_masonry/edge.json
python scripts/verify_level4_edge_geometry.py --capture EDGE_AFTER --out evidence/level4_masonry/edge_geometry.json
python scripts/verify_release.py
```

The checks require exact RAM, PPU, OAM, PPU-view metadata, all APU writes and full PCM. Image changes must remain within eligible foreground cells and moving-platform cells, accounting for the measured endFrame camera interval. Menus, blank transitions and unrelated images remain exact. Actual pictures must contain complete source matches for solid and breakable blocks; the full movie additionally exercises column caps, bases and shafts. Ten representative scenes compare the unchanged panorama pixels directly with their sources. The platform route verifies the left stop, every supported anchor across the top, and the same native right-edge fall.

The preview compares 0.16.0 with 0.16.1 in actual playback, including breakable-block destruction, the outdoor approach and both indoor sections. See `evidence/level4_masonry/` for exact results and frame ranges. The existing 0.16.0 evidence remains frozen.

## Review status

This is a revision on `feature/golden-temple`, following review commit `7c27c29dc2c98f490bb9a709e1fb52d99d05b076`. The original 0.16.0 foreground treatment is superseded. The user accepted its backgrounds and outdoor columns only; this is not blanket approval of the revised pack. Main remains approved 0.15.0. Later temple rooms and boss remain outside the recording and untested. No push, PR, merge, tag or release is implied.

The source ZIP wraps an incremental bundle from approved main, so it includes both the original Golden Temple work and this revision. Its README contains exact non-force fetch/push commands. ROMs, movies, emulator binaries and raw captures are excluded.
