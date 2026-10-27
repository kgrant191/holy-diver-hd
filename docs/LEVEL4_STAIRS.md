# Golden Temple stair visibility — 0.16.3

The supplied save shows a descending stair flight in the first indoor room,
AA09. Native cells 0B7C–0B7F form the four parts of each step. The original
Golden Temple builder mistakenly classified these cells as decoration and
cleared them, exposing the panorama despite their physical stair role.

## Repair

`build_level4_stairs.py` runs after the unchanged 0.16.2 builders. It restores
the four cells with 24 overrides covering their previously recorded room and
palette combinations. These rules precede the mistaken transparent mappings.
The earlier opposite-facing stair family 0B80–0B87 remains unchanged.

The new 32×32 atlas uses the exact RGB pixels of the existing registered gold
moving-platform stone. The complete native 16×16 step silhouette is joined
before scaling and slicing, retaining its top surface and sloped underside.
There is no new generated artwork. Source pixels, native patterns, alpha masks
and original overridden rules are recorded in `art/level4_stairs/`.

All 108 previous art/audio/patch assets remain byte-identical. The only
previous installation files that change are hires.txt and README.txt; one
new atlas brings the flat installation to 111 files. The temple-entry bounds
repair, HD pickups, backgrounds, pillars, other masonry, Overdrive and native
gameplay remain intact. Removing the marked stair blocks recovers exact
0.16.2 hires.txt, and the validator retains every earlier regression check.

## Save-state and runtime checks

`Holy_Diver_HD_1(20261026-181741).mss` is unchanged: 9,478 bytes, SHA-256
`1e572fa95b436b4276051354d5fc19b409194fd5b57aabbcd05ec12b0c03ed4b`.
The native no-HD replay identifies the stair graphics independently. The
state, ROM and derived movies remain local and excluded from Git.

`make_level4_stair_routes.py` wraps that exact state in controller-only movies:
walk left off the lower landing and return, or jump up the stairs, enter AA81,
fall back into AA09 and descend to the lower landing. No game memory is edited.
The edge derivative holds left at the upper stair stop, pauses, then walks
slowly across the complete supported span and off its right edge. Both builds
stop at world anchor390/Y48, remain at Y48 through anchor411, and first fall
at anchor412/Y49. Every supported anchor is exercised. The visible stone keeps
its native footprint rather than extending to the player's overhanging boots.
`verify_level4_stairs.py` requires paired RAM/PPU/OAM/PPU-view, every APU write,
full PCM equality, differences confined to the restored stair cells, and
complete source-step matches in actual playback. The unchanged full 8,668-frame
recording supplies outdoor, entrance and both indoor-room regression coverage.
The invalid-neighbor observer remains enabled during the accepted replays.

The four accepted pairs cover 9,614 frames per build and 3,114 native samples
per type, with exact APU and complete PCM. All image changes stay within the
restored stair cells. See `evidence/level4_stairs/summary.json` for exact totals.

Inspect the supplied landing at frame30, upper step contact at frame120 and
descending contact at frame320 of the jump route. Paired native positions and
room transitions are recorded in `evidence/level4_stairs/route_geometry.json`.
The preview compares unretouched before/after game images at half speed, with
labels outside the game frame.

```sh
python build.py
python scripts/verify_release.py
python scripts/make_level4_stair_routes.py --state USER_STATE --template USER_MOVIE --out ROUTES
python scripts/verify_level4_stairs.py --before BEFORE --after AFTER --out REPORT
```

The initial stationary investigation capture had a mismatched WAV startup
phase and was not accepted as a paired audio pass. The walk and jump acceptance
routes include the same stationary starting view and require exact complete
PCM. One full-movie attempt stalled before its observer started; it produced
no accepted gameplay evidence and was terminated. Acceptance uses the completed
fresh replay and the unchanged strict verifier. Raw investigation captures
remain outside Git; final reports identify the accepted movie hashes.

The source bundle includes this repair and earlier Golden Temple changes from
approved main. 0.16.3 awaits review on feature/golden-temple; main remains
approved 0.15.0. No push, PR, merge, tag or release is implied. Later temple
rooms and boss remain outside the tested recording.
