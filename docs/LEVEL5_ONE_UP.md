# Palace 1-up mapping repair — 0.22.2 review

The user reported two native 1-up figurines and accepted the rest of 0.22.1.
The Palace player/HUD aliases were copied from the 0A bank, which lacked the
earlier shared 1-up rules. The collectible therefore remained native in both
Palace sprite banks. Its green appearance while Randy is a dragon also uses a
different palette.

`build_palace_one_up.py` adds twelve final fallback rules for 104E/104F and
124E/124F. The recorded ROM cells are byte-identical to the approved 024E/024F
collectible. FF300036 uses the approved ivory figurine; FF221136 uses the blue
figurine; the dragon-form FF190927 palette uses the same ivory figurine. These
are the exact existing atlas 29 cells, assembled as a complete 16×32 HD object.
No art, alpha, scale, native palette, OAM, timing or pickup behavior changes.

The green screenshot independently confirms the native identity and palette:
all 100 opaque native pixels match the recorded CHR patterns and FF190927
colors at the supplied screenshot's fivefold scale. A screenshot alone cannot
identify which identical physical CHR copy was active; both Palace copies are
covered. See `evidence/level5_one_up/screenshot_identity.json`.

All 124 previous image/audio/patch files remain byte-exact. The install keeps
126 root files; only hires.txt and README.txt change. Removing the marked
PALACE_ONE_UP block recovers exact 0.22.1 hires.txt. The validator reconstructs
the complete frozen 0.22.1 pack and invokes every historical validator, including
the Thunder/dragon flash tests. There are no new conditions or neighbor reads.

Build with `python build.py` and `python scripts/verify_release.py`.
Replay the retained 20261027-235225 movie using `run_mesen_movie.py` and compare
frozen 0.22.1/0.22.2 outputs with `verify_palace_one_up_replay.py`. It requires
exact RAM/PPU/OAM/scroll, complete native audio and APU writes, unchanged pixels
outside each native 1-up footprint, and the actual approved figurine pixels.
Compact results and coverage limits are in `evidence/level5_one_up/summary.json`.

`make_palace_one_up_route.py` retains the movie's embedded state, settings and
first 744 input frames, then holds Up for 140 frames, Right for 480, and neutral
for 100. This reaches the green 1-up in the upper hall without RAM or save-state
edits. Pair frames 740–1464 at stride one against the same two frozen packs.
The native green figurine enters at frame 1265. The ordinary movie covers the
ivory and blue variants in the lava room at stride two, including collection
with lives changing from 6 to 7. The green upper-hall route validates appearance
and movement, without collecting that item. Both preserve native behavior.

Final paired checks cover 5,828 native samples per type across 11,670 emulated
frames per build. All 395 changed captures are confined to the figurine;
5,433 captures stay pixel-identical. There are 379 complete, unobstructed
approved-source matches, plus visible-source checks for clipped/overlapped
instances. For overlaps, every changed opaque pixel must match the source;
any hidden source pixel must remain identical between packs and fall within
another actual OAM sprite's bounds. RAM/PPU/OAM/scroll, full APU and PCM match.
The native lava-room collection increments lives 6→7 at sampled frame 5208.

The 0.22.1 scenery, flash repair, enemies, slime ceiling and THUNDER glyph are
accepted and preserved. The new 1-up repair awaits review on
`feature/demonic-palace`. Main remains approved 0.20.5. No push, PR, merge, tag
or release has been performed.
