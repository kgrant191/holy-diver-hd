# Golden Temple boss entrance and stair underside — 0.20.1

The user's final-hall screenshot shows the boss entrance missing. The earlier
interior scenery copy treated the native doorway as wall decoration: its
four-by-four crown (0DDF–E2 and0D5B–68) was cleared, and its six rows of empty
passage cells revealed the panorama. The final approach is AEF5/mode0C.

`build_level4_finish.py` restores the existing entrance crown and dark passage.
The upper opening uses0F172737; the bottom two rows use0F071723. Each blank
cell must find the corresponding crown-bottom identity directly above it,
within the six-row native opening. Ordered Y bounds precede all upward probes.
The repair is confined to AEF5 and leaves decorative column removal intact.

The close-up identifies the descending0B7C–7F step family and its byte-identical
0D copies. Its previous native alpha outline had coarse lower cutouts and a
single dangling bottom pixel. The repair retains every RGB pixel and the
entire upper half, including the standing edge, while giving the lower half
one continuous diagonal. Existing opposite-facing stair families are unchanged.
This requested underside polish supersedes the previous lower-mask constraint
for the reported family only. Native collision and inputs are not edited.

There are144 removable tile overrides,80 for the already mapped stairs, and
30 doorway conditions. The first24 stair rules precede the original first-room stair block; the remaining rules follow the later room condition declarations. Atlas54 contains the repaired32×32 step. The installed
pack has116 flat files. All113 earlier art/audio/patch assets remain byte-exact;
only hires.txt and README.txt change among the earlier installation files.
Removing the four TEMPLE_FINISH blocks recovers exact0.20.0 mappings. The
validator retains every earlier regression, checks unchanged upper geometry,
continuous lower alpha, source correspondence and2,605,056 safe neighbor reads.

## Actual emulator checks

Use stock MesenCE2.2.1 core SHA-256
`f45cd3fd53d48176f66a1d2ff9713394e4428fae98bee53df69bed5a442e7e79`
with the synchronized screenshot/audio observers and the invalid-neighbor
observer. Run only one emulator at a time; each replay installs an immutable
private copy of its pack. No emulator binaries or ROMs are included.

Pair the supplied7591-frame `Holy_Diver_HD(9).mmo` and the existing298-frame
controller-only stair edge derivative against frozen0.20.0. The latter starts
from the user's unchanged20261026-181741 save, holds the upper left stop and
slowly crosses the full stair support before walking off the right edge.
`verify_level4_finish.py` checks RAM/PPU/OAM/view, every APU write and full PCM,
confines changed pixels to the requested cells, checks complete source images,
and requires the boss room and native blackouts to remain exact.

Commands:

```sh
python build.py
python scripts/verify_release.py
python scripts/verify_level4_finish.py --before BEFORE --after AFTER --out REPORT
python scripts/verify_level4_finish.py --before EDGE_BEFORE --after EDGE_AFTER --stairs-only --out EDGE_REPORT
```

The supplied movie enters the boss room and ends at game over. This repair
neither changes nor newly tests boss defeat, rewards or later rooms. Work stays
on feature/golden-temple-boss; main remains approved0.15.0. The user described
the prior graphics as almost perfect and requested these two repairs; this is
not a publication or merge instruction.

## Final evidence and limitations

The full7591-frame pair passes exact RAM/PPU/OAM/view, all APU writes and
24,257,384 bytes of full PCM. There are2155 images with changes confined to
stairs/doorway and5435 identical images, plus one empty initial image. All267
native blackouts and1125 boss-room images stay exact. Complete source checks
find167 stairs and six full doorway matches. See movie_validation.json.

The earlier edge save exposed first-match priority: the original24 first-room
stair rules were ahead of the new overrides. Moving those exact overrides
before the original block fixes the earlier rooms. No other mapping line or
artwork changed. The full recording visits none of the three affected rooms
(A865,AA09,AA81), so its tested rendering is exactly equivalent to the final
pack. movie_scope_equivalence.json records that check and both mapping hashes;
movie_tested_pack.json pins the actual full-replay installation. To reproduce
that retained comparison, pass it explicitly with --after-manifest. The final
pack is replayed on the affected298-frame stair edge route.

An initial edge-pair audio recording had a different startup sample phase and
is not accepted as an audio pass. A fresh baseline repeat supplies the retained
edge baseline. The strict full-PCM comparison is unchanged. Investigation runs
and raw captures remain outside Git.

The accepted final edge pair passes all298 native samples, all APU writes and
958,156 full PCM bytes. Its297 valid images change only inside the stair cells;
68 complete stair-source matches pass. Both builds stop at worldX390/Y48,
remain supported throughX411, and begin falling atX412/Y49. All supported
anchors are traversed. See edge_validation.json and edge_geometry.json.

The packaging path now completes the ZIP in memory, flushes and syncs a temporary
file, atomically replaces the output, and checks its full byte hash and CRCs.
This prevents a partial archive from being mistaken for a completed delivery;
the development pack files and their expected hashes remain independently checked.
