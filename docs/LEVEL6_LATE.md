# Level 6 green reliquary and descent — 0.28.0

The user accepted 0.27.0 and supplied the next two rooms. Work continues locally on `feature/level6-opening`. Main remains approved 0.24.0; no push, PR, merge, tag or release has been performed. The accepted continuation is recorded in `evidence/level6_variety/approval.json`.

| Room | Native role | New design |
| --- | --- | --- |
| A20B / 10 | Green structure `0F0B1B3B`, green decorative wall `0F0A1A29` | Dense olive-green skull-relief reliquary; accepted green masonry |
| A2FB / 04 | Green structure `0F0A1A39`, ivory skull blocks `0F081030` | Open, dark green vertical tower; accepted green masonry and skull blocks |

Both new backgrounds are generated separately. The first uses monumental skull slabs and enclosed architecture; the second uses long distant ribs and open darkness. They preserve the original green color identities while remaining distinct from the earlier blue-accented crypt.

The new room scopes reuse complete ordered A0DF tile rules, including all specific player/effect dependencies, flying skulls, both bronze crawler poses and sentinel hit palettes. The eye 18F3–18F6 and falling tear 18F7–18F8 match approved native identities 02D8–02DD exactly; atlas 34 is reused without redrawing them. Skull blocks retain their whole 2×2 registration.

The only new foreground group is 17F6/17F7 over 17F8/17F9. Its 32×32 HD image is cropped from accepted green stone and registered as a whole unit with exact native hulls. Both physical background banks, 1700 and 1900, are covered. Only the measured decorative green wall palette clears to the backdrop. Normal/resume and 30/31 families are explicit; flash backgrounds retain RGB with alpha 176. Death/card palettes 213029 and 041424 are excluded.

All 141 previous art/audio/patch assets remain byte-identical. Five install images are added; stripping three LEVEL6_LATE blocks recovers the exact accepted 0.27.0 mapping text. No new tile-neighbor probes, native state edits, animation changes or audio changes are introduced.

The provided 7,648-frame movie covers A20B, a death/restart, menu transitions, Blizzard/Overdrive and the recorded A2FB descent. The earlier 3,393-frame movie supplies the unchanged-image regression. The 700-frame controller-only branch tests the green entry floor's left stop and right walk-off. Results and coverage limits are recorded under `evidence/level6_late/`. This route has no Thunder or dragon cast in the new rooms; those families are statically complete. Later unrecorded rooms and the final boss remain unfinished.

Generated sources and exact prompts are in `art/generated/level6_reliquary.png`, `level6_green_shaft.png` and `level6_late_prompts.json`. Tile registrations are in `art/level6_late/`. Build with `python build.py`, then `python scripts/verify_release.py`; the build runs the full historical validator chain using exact baseline projections.

## Completed validation

- The full 7,648-frame replay matches native RAM, PPU, OAM, view state, APU and complete PCM audio exactly. Both room backgrounds remain present throughout visible scrolling. All 15 inspected whole actor and terrain sources match actual rendered pixels. All 890 recognized menu images and 516 black frames remain exact.
- The earlier 3,393-frame replay matches all native state and audio; all 3,392 nonempty images are identical to accepted 0.27.0.
- The 700-frame controller-only edge branch matches native state and audio. The left stop stays at world (23,96); the original right walk-off starts at frame 531, world (136,96), with first descent at frame 535. The full 224×256 HD entry-floor source matches in 197 captured frames and retains its tapered native lower outline.
- An isolated clean build passes the full historical validator chain. All 148 installation file hashes match the tested runtime. The flat install ZIP passes CRC and manifest verification. The actual 7,647-frame preview includes original audio and passes a complete video decode.

Machine-readable results, the clean-build log and an actual two-room capture are in `evidence/level6_late/`. Live Thunder/dragon flash coverage remains absent from this recording; their rules are checked statically.
