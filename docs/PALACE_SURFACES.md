# Palace masonry and Overdrive book — approved 0.32.0

The user approved 0.32.0 on 2026-10-30 and explicitly authorized push and merge. The pushed artwork commit is `ac5f6fdde59cb19c56c4d2d6f6b607522c5fceec`. Preserve all 174 reviewed installation files, including INSTALL.txt and the installed README. This approval update changes source documentation only. Verify the PR checks and actual downloaded artifact before the authorized merge; no further merge approval is needed. Main remains approved 0.31.0 until adoption. No release/tag is requested. See `docs/PALACE_SURFACES.md` and `evidence/palace_surfaces/approval.json`.

The user clarified that the opening Level 5 screens are liked, and identified
the repetitive floor, wall and stair material as the unwanted artwork. The
earlier opening redesign is withdrawn. This branch starts from approved main
`ca33fa293cf7ce42c4d63a5f3899d9a8370cc317` / 0.31.0.

| Scope | Change |
| --- | --- |
| Opening 850A, 8672, 86EA, 8762 | Exact approved 0.31.0 rules and artwork |
| Stair halls 8816, 888E; platform shaft 8BD6 | Silver-gray stone, following each native palette |
| Lava corridors 897E, 8A6E, 8AE6 | Violet masonry in native purple palettes |
| Green hall 8C4E and transition copies | Green masonry in native green palettes |
| Skull shaft 8D3E, boss 8E6A and exit 8EE2 | Silver-gray masonry; existing ornaments and actors retained |
| Moving lifts in 8BD6 and 8D3E | Same silver stone within the existing complete sprite footprint |
| Level 3 boss room 9F92 | Overdrive acquisition book, four cells 088B–088E |

All existing distant backgrounds remain exact. The palette of each individual
mapping selects silver, violet or green, including adjacent-room transition
copies and existing native 30/31 flashes. Brightness and death-fade factors are
unchanged. The native pure-white victory version remains exact because its
unchanged alpha is already a solid white silhouette.

The original Overdrive pickup is a square spell book bearing an emblem. Earlier
notes called it an orb; the saved native pattern bytes and original-game replay
disprove that identification. The new crimson/gold book occupies the same 32×32
HD cell union. Only the four room-scoped acquisition mappings change. The
actual orbiting Overdrive spell and its aliases remain exact.

## Sources and preservation

Four built-in ImageGen sources, prompts and hashes are retained under
`art/generated/palace_surface_*`. Three whole masonry units and one whole book
are registered before slicing. `art/palace_surfaces/native_uv.json` records
the native nametable alignment used to coordinate adjacent stone cells.

`build_palace_surfaces.py` changes 2,382 scoped existing mapping lines in place:
2,178 ordinary masonry, 192 boss/exit masonry, eight moving-lift cells and four
book cells. Every condition, rule position, identity, palette, brightness and
flip parameter stays unchanged. All existing terrain alpha masks remain
byte-identical. No new neighbor probe or gameplay patch is introduced.

All 171 earlier non-text installation assets remain exact. One atlas adds 80
registered cells; the flat install has 174 files. Removing the image declaration
and reversing the documented substitutions recovers the exact approved 0.31.0
mapping hash. The historical validator chain runs on that recovered baseline.
`approved-pack-sha256.json` and `0.32.0-pack-sha256.json` now pin all 174
user-approved installation files. Their bytes remain unchanged by approval.

## Verification

Use `python3 build.py`, `python3 scripts/verify_release.py` and the paired
`verify_palace_surfaces_replay.py` runner with the stock MesenCE 2.2.1 core,
synchronized screenshot observer, bounds observer and native WAV capture.
Source inputs and emulator binaries remain outside Git. No RAM edits stage
the evidence. Exact replay results and coverage are recorded in
`evidence/palace_surfaces/`.

The install and source handoff are approved. Push and merge are authorized;
PR checks and actual artifact verification precede adoption. No release/tag
is requested.

### Completed verification

The isolated build and full historical validator chain pass. All 174 flat ZIP
members pass CRC and the pinned SHA-256 manifest; the candidate ZIP SHA-256 is
`80497bd8db2d99baff792f96f74545b1985c24eef361ec74cc5a897f46ed0ace`.
All runtime-producing inputs in this branch match the isolated tested source.

Seven paired controller-only routes complete 58,334 frames. All 9,505 sampled
RAM, PPU, OAM and camera states match approved 0.31.0 exactly; complete APU
traces and PCM audio also match for every route.

| Route | Full movie frames | Paired native samples | Result |
| --- | ---: | ---: | --- |
| Silver stairs | 1,215 | 607 | Only registered masonry changes |
| Level 3 pickup | 4,812 | 2,406 | Only acquisition book changes; 46 whole-source matches |
| Violet corridors | 10,206 | 1,276 | Scoped terrain changes; active Overdrive exact |
| Green hall and moving platforms | 14,595 | 1,825 | Scoped terrain changes; 57 whole-lift matches |
| Final shaft, boss and exit | 15,585 | 1,949 | Scoped terrain changes, native fades and blackouts |
| Opening regression | 9,921 | 1,241 | 1,050 stable opening-room images exactly unchanged |
| Slow platform-edge walk | 2,000 | 201 consecutive | Exact stop, grounded motion and native fall timing |

The opening movie ends at 8816: its five changed transition images are the
requested later material. Menus/cards and blackouts remain exact throughout.
Two boss-camera frames (9520 and 9528) render vertical scroll beyond the sampled
camera mask. A stricter source-pair check proves all 101,777 changed pixels are
exact corresponding old/new opaque stone pixels at the same tile-grid phase;
no broad allowance or expanded spatial mask is used for these frames.

The edge route holds the far-left native stop at world (607,80), walks slowly
across the full platform, starts falling at (648,80) on frame 1905, and first
descends at (652,81) on frame 1909. Its complete 64×32 material source matches
46 consecutive captures. Native collision and visible support width agree.

The two review PNGs are composed from actual paired replay captures. The book
comparison includes the original NES pickup. Export verifies each pasted frame
and the decoded output; no synthetic game-frame mockup is used.
