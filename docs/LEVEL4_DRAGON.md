# Golden Temple dragon and readable items — 0.19.0 review

The two supplied states start just before the dragon pickup in the outdoor ACD9 arena. This update replaces the pickup and player transformation, improves the staff and small recovery drops, and removes the thin non-solid foreground columns that looked like obstacles. It is a review candidate on `feature/temple-dragon-items`, based on frozen 0.18.0 commit 0ed92934. Main remains approved 0.15.0, with 0.16.3 the last explicitly approved Level 4 pack. No push, PR, merge or release is performed.

## Dragon registration

The form uses native palette FF190927 in a 112x48 HD footprint. Two wing positions and a separate open-jaw firing pose were observed with both saves, both directions, U/D/L/R/A/B and pause. The whole generated variants share a common source crop and registration at (1,4), 110x42. Every opaque pixel fits the native cell union. Shared native cells use exactly the same bytes; folded-wing cells change only where the game provides alternate identities. The firing layout replaces the native lower-jaw cell. OAM controls animation timing, direction, movement and visibility.

The pickup is 0CB1–B4/FF301116, 32x32. The fire projectile 0CB0 reuses the finished boss 1 orange flame, registered to 16x16. Native 0C74 transformation twinkles reuse the approved gold burst. Exact CHR matches establish the supported bank aliases. Unobserved layouts are not invented. Native damage blinking deliberately hides the whole player on some frames and remains intact.

The native pickup flash changes universal background color 0F to 31 for 15 frames. Scoped copies of the final arena foreground rules preserve HD masonry during that flash; no full-color panorama is added for 31. Position bounds remain ahead of all neighbor reads. Transformation stars, native flashing and control lock are retained.

## Item visibility and columns

The staff's complete 16x32 image now has a stronger ivory/gold shaft and emerald crown. Its Start-menu image uses the same source centered in 32x32, retaining exact origin guards. Small heart/magic drops have brighter highlights and navy outlines. Their proven aliases are scoped to A865,AA09,AA81,AAF9,AB71,AC61 and ACD9 so earlier conditional art stays unchanged.

The removed foreground family is the original `outdoor gold column` art and its exact later clones, including alternate capitals. Player/body overlap in recorded controller movement proves these are non-solid decoration; the evidence includes Randy walking through AB71 shafts and dragon flight through ACD9 columns. Only 146 identified scoped rules are overridden. The 0B78–7B structural masonry and 0B7C–87 stair families are retained. Accepted panorama files, physical artwork, actors and every earlier installed art/audio/patch asset remain byte-exact.

## Verification and limits

Run `python build.py`, `python scripts/verify_dragon_neighbor_rules.py` and `python scripts/verify_release.py`. The installed candidate adds atlas 52; stripping the three TEMPLE_DRAGON blocks restores exact 0.18.0 hires.txt. The 114-file installation preserves 111 earlier art/audio/patch files, changing only mappings and installed README among prior files.

`make_level4_dragon_routes.py` embeds each supplied state unchanged and writes controller-only routes. `inventory_level4_dragon.py` recovers native layouts, physical0D background identities and CHR proofs. `verify_level4_dragon.py` pairs stock MesenCE 2.2.1 captures with 0.18.0, requiring exact RAM/PPU/OAM/view metadata, APU writes and full PCM. It confines image differences to the requested sprite/decorative cells and native flash foreground, checks retained panorama pixels, and finds complete registered sources in actual captured frames. One emulator runs at a time with a private immutable pack copy and the invalid-neighbor observer active. Diagnostic binaries are not shipped.

Five paired routes cover both new states plus the three earlier temple recordings. Actual before/after screenshots and the silent normal-speed preview are unretouched; labels sit outside the game image. See evidence/level4_dragon for machine-readable results, input hashes, bounds checks and archive validation.

These states begin after the sentinel has gone; its defeat sequence was not supplied or tested here. The dragon routes stay in ACD9. Later rooms, other possible dragon palettes/layouts, and the native white ring enemies are outside this request and remain unverified.

## Source handoff

The incremental Git bundle contains feature/golden-temple, feature/golden-temple-courtyard, feature/golden-temple-staff and feature/temple-dragon-items. Prerequisite: approved main 2f38abeb06cd1093fc33416da20c5124fca2f4d7. The source ZIP includes exact verify/fetch/push commands. ROM, states, movies, emulator binaries, raw capture directories and build archives are excluded from Git.

Final paired checks cover **18,283 frames per build** and **7,774 samples per native-memory type**, with 58,440,012 full PCM bytes identical. All six pose/direction combinations, pickup, transformation star and fire projectile match complete registered sources. Both gameplay and menu staff match. The copied flash probes pass 614,400 screen-coordinate cases with zero unsafe reads; all five diagnostic replays complete. Staff shaft coverage increases from 36 to 74 opaque pixels in rows 12–28, and bright pixels from 4 to 39 using the same RGB-mean threshold 150; see visibility.json.
