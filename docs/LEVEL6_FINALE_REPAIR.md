# Level 6 finale repairs — 0.30.1

The user requested four corrections to 0.30.0: less wall material in the face,
the approved slime design in blue, a visible entrance before the final platform,
and connected ending dragons that remain visible around the story text.

The user approved all delivered work through 0.30.1. PR #28 merged on
2026-10-29; PR and main builds and both downloaded 166-file artifacts pass.
All reviewed installation files remain frozen, including the installed README
whose wording predates approval. See LEVEL6_ADOPTION.md and
`evidence/level6_adoption/`. The new missed-room movie is next, followed by
cleanup and the completed release. No release or tag was created.

## Rendering changes

- **Face:** register the supplied clean reference as one 48×128 image. Remove
  the old red-material underlay and inherited wall alpha. Seven repeated native
  left-column cells use bounded right-neighbor anchors to retain their individual
  source rows. Covers A3AF/mode10 and A49F/mode04 with all nine existing palettes.
- **Blue enemy:** both 32×32 blue mucus poses replace 1A9C–1AA3/FF110130 in A49F.
  The approved green poses and the original green orb sources remain byte-exact.
- **Entrance:** a 64×96 bone-framed portal occupies the original four-by-six
  blank cells above the last ledge. Each cell checks the top ceiling and side
  jamb identities, with four screen bounds before each neighbor probe. This
  follows the camera and appears before landing. Original activation shutters
  become transparent so they cannot cover the entrance with flat rectangles.
  Native OAM, collision, activation timing and room transition are unchanged.
- **Ending:** whole raised/lowered wing poses replace the old scanline-squeezed
  art. Both registered silhouettes have a single connected component and fit
  their native sprite-cell unions. The three tail cells are shared exactly.
  Registration trims 46/32 edge pixels outside those unions; it does not claim
  that all pixels of the generated source survive. Native colors, flips, movement,
  priority and all-black fades are retained.
- **Text:** only in B01C, clear alpha on pure-black pixels in the existing ending
  font cells. All RGB values and every nonblack glyph pixel remain exact. This
  lets background-priority dragons show through the formerly opaque black
  padding, while lettering still draws over them.

The repair adds one atlas and removable `LEVEL6_FINALE_REPAIR` blocks. Removing
those blocks and reactivating the 171 explicitly marked earlier face rules
recovers the exact 0.30.0 hires.txt. Those earlier rules preceded the finale
atlas declarations and would otherwise override the clean face in A3AF. All
163 prior art/audio/patch assets remain unchanged; the eight green-blob rules
remain active. Original boss-room art is not repainted.

## Original-graphics comparison

`evidence/level6_finale_repair/original_graphics.json` records a complete input
movie using the stock core with every HD replacement removed. The existing audio
priority IPS and sprite-limit option remain active. Disabling HD entirely also
removes that IPS, which desynchronizes this supplied recording; that unsuccessful
comparison is not used as evidence. The valid original-graphics run matches all
641 sampled RAM, PPU, OAM and camera states of the HD run, and shows both dragons
around the ending text. The previous HD font padding was therefore a pack defect.

## Validation and review artifacts

The rules check verifies prior-file hashes, exact rule recovery, registered source
cells, single-component dragon poses, shared tails, unchanged colored glyphs,
bounded probes and the original green orb standby. The full replay checker
compares every native state and full APU/PCM stream and bounds each actual image
change to the requested face, slime, doorway or ending dragon cells. Both boss
rooms and native blackouts must remain image-exact. A second complete replay
covers the earlier face room and confines changes to the face cells.

The complete finale capture precedes only the final disabling of those 171
A3AF face rules. The replay verifier proves that exact text delta, unchanged
other installation files, and the absence of A3AF throughout that movie. The
final earlier-room capture uses the complete final manifest. This preserves a
full validation of the final runtime without repeating the unaffected finale.

The isolated clean build runs the complete historical validator chain and must
reproduce all 166 installation hashes. The user-facing preview is encoded from
actual replay PNGs and original captured audio. Exact completed results and
source-frame selections are recorded in `evidence/level6_finale_repair/`.

Generated sources use the built-in image-generation tool; the supplied face is
registered directly. Source hashes and prompt specifications are in
`art/level6_finale_repair/sources.json`. No ROM, emulator or movie is distributed.
