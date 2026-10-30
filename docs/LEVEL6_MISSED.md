# Final recorded Level 6 rooms — 0.31.0

The user supplied `Holy_Diver_HD(20261030-015933).mmo` for the skipped rooms
and asked whether its first room needed changes too. The first corridor still
had blue-gray brick mass despite its original red palette, and its eyes were
missing the native `FF060C30` palette. Both are corrected.

This is a new review candidate on `feature/level6-missed-rooms`, based on
approved main `56ee5aaa20d392ac916f32160d31c64a4c1ea22a` (0.30.1, PR #28).
No push, PR, merge or release has been performed for this candidate.

| Native room | Recorded frames | Updated treatment |
| --- | --- | --- |
| 9CA7 / mode0C | 135–1445 | Red brick mass, retained ivory trim and a crimson gallery |
| 9D5B / mode08 | 1446–6872, with pauses/deaths | Dark violet chapel, purple terrain, completed eyes and lava/ice mappings |
| 9DD3 / mode18 | 6873–8714, with pauses | Open layered amethyst arcade, purple terrain, returning serpent and dragon flash art |

The initial 9A8B interval and stable final 9F3B interval remain unchanged.
These findings apply to the supplied route, including its deaths and retries;
they do not establish coverage of any other unrecorded route.

## Artwork and mappings

- The corridor uses the already approved red material registered over its
  complete four-cell brick group. Existing ivory architectural trim remains.
- The purple rooms share a new subdued violet masonry material but have
  distinct compositions. Native terrain hulls remain exact. The complete
  brick, repeating ceiling body, three-cell lip, corner and hanging edge are
  visible as whole sources in actual playback.
- The visible blue decorative wall palette clears to the new backgrounds.
  The lava and Blizzard ice use the existing sources and animation conditions.
- Eyes and both tears reuse atlas34. The newly observed serpent palette reuses
  the completed Palace serpent. Dragon pickup flashes retain the finished
  green dragon artwork. Native tile identities prove these aliases.
- All normal/resume/30/31 room guards use the observed physical background
  bank families. Death/card-only palettes are excluded. No neighbor probes
  are added, and copied animation conditions retain their order.
- Removing the three marked `LEVEL6_MISSED` blocks recovers exact 0.30.1
  mappings. All 164 previous art/audio/patch files and the original green
  enemy standby remain unchanged. The install pack now contains 173 files.

New imagery was made with the built-in image-generation tool. The saved
sources are `art/generated/level6_crimson_gallery.png`,
`art/generated/level6_violet_chapel.png`,
`art/generated/level6_amethyst_arcade.png`, and
`art/generated/level6_violet_stone.png`. Exact prompts, source hashes and
reuse provenance are in `art/level6_missed/prompts.json` and `sources.json`.
The chapel floor was removed in a generated revision so the scenery does not
suggest a foreground walking surface. Registration, slicing and native masks
are deterministic build operations.

## Verification

The paired 8998-frame movie uses the stock MesenCE 2.2.1 core, synchronized HD
capture and the existing neighbor-bounds observer. All RAM, PPU, OAM and view
samples, APU writes and complete PCM audio match the approved baseline.

- 6525 images change, all within the requested room scopes; 2472 are identical
  and one initial capture is empty in both runs.
- 927 detected menu images, 329 blackouts, 386 stable death-card images and
  283 stable images of the accepted next room remain exact.
- Every changed image contains its expected background, including 78 flash
  samples. All 17 selected whole sources match actual gameplay captures,
  covering the new terrain groups, eyes/tears, serpent head/body, all three
  dragon poses and all three Thunder sources.
- A separate controller-only route retains the original movie prefix and
  embedded state. It walks right to the wall, pauses, then slowly walks left
  off the violet ledge without jumping. Both replays have exact native/audio
  data. The right stop is world(489,96), falling begins at frame1828 at
  world(408,96), and descent begins at frame1832. The entire 192×256 HD
  ledge/wall region has exact native alpha and 141 whole-source matches.
- A clean isolated rebuild reproduces all 173 hashes and passes every
  historical validator. The installation archive has valid CRCs and a flat
  layout, without another ZIP inside it.
- The preview contains actual frames2–8998 and the verified original audio:
  512×480, 719503/11972fps, 149.703 seconds. Full audio/video decode passes.

Evidence is in `evidence/level6_missed/`, including the replay, edge route,
clean build, static rules, preview and actual-capture contact sheet.

Next: user review of this update, then the requested cleanup elsewhere before
the completed release. Version1.0.0 remains reserved for that finished pack.
