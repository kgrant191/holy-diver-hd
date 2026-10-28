# Demonic Palace flash repair — 0.22.1 review

The user correctly identified original scenery appearing in the preview during Thunder casts and dragon pickup. Earlier checks excluded native flash palettes and therefore missed the visible regression. A native flash should preserve its timing and color effect while using the completed HD scenery.

## Repair

The universal background color changes from 0F to 30 for Thunder and 31 for dragon acquisition. The existing Palace panorama guards and some foreground replacements recognized only 0F. The game therefore exposed native wall patterns and stair graphics during the flash.

`build_palace_flash.py` clones every existing scoped Palace scenery rule for both flash palettes, retaining source cells, alpha masks, conditional ordering, animation conditions and bounded neighbor geometry. It also clones the existing rendered panorama guards. This covers the existing HD rooms in both physical 1100/1300 CHR copies. Sprite artwork is unchanged.

The flash panorama keeps the accepted source RGB exactly, with uniform alpha 176. Mesen blends it over the native universal flash color: white for 30 and pale blue for 31. The renderer still applies native grayscale/emphasis scanline effects. This retains a visible flash while keeping the Gothic artwork on screen. Ordinary 0F frames retain their original opaque panorama and are byte-identical in the paired captures. Native all-black palettes do not activate the new rules.

All 122 prior art/audio/patch assets remain byte-exact. Only hires.txt and README.txt change, with two additional transparent flash-panorama files. Removing the two PALACE_FLASH blocks recovers exact 0.22.0 mappings; the complete historical validator chain remains intact. No emulated RAM, input, collision, spell timing, item behavior or audio is edited.

## Live verification

Both source movies are replayed in the same stock MesenCE 2.2.1 core before and after. Consecutive captures cover opening frames 8760–9220 and stair-hall frames 280–700 at stride 1. They include Thunder casts and dragon pickup in both rooms. This avoids missing alternating flash frames in a 30 fps preview.

`verify_palace_flash_replay.py` compares every captured RAM/PPU/OAM/scroll sample and complete-movie APU/WAV output. Every changed picture must lie at a native flash and contain more than 40,000 exact panorama-source pixels using Mesen's integer alpha blend and native grayscale/emphasis formula. Ordinary captured frames remain exact. Detailed results are in `evidence/level5_flash/movie_validation.json`.

The new preview presents these exact captured sequences at 60 fps with native audio. It includes the problematic moments rather than skipping them. No later rooms or boss are claimed as new live coverage. Main remains approved 0.20.5; this is a local feature/demonic-palace review candidate with no publication or merge.

## Reproduce

```sh
python3 build.py
python3 scripts/verify_release.py
python3 scripts/verify_palace_flash_replay.py --captures CAPTURE_ROOT --out movie_validation.json
python3 scripts/export_palace_flash_preview.py --captures CAPTURE_ROOT --out preview.mp4
```

CAPTURE_ROOT contains opening_before/opening_after, hall_before/hall_after and candidate_pack. Use run_mesen_movie.py with stride 1 and the capture windows above. Inputs, ROM and emulator are local test material and excluded from the source handoff.

## Verified result

- Opening: 461 consecutive samples preserve native RAM/PPU/OAM/scroll state. Full 9,921-frame movie audio/APU output matches. 31 flash pictures are corrected, with at least 150,437 exact source pixels each; 430 ordinary pictures remain byte-identical.
- Hall: 421 consecutive samples preserve native RAM/PPU/OAM/scroll state. Full 10,206-frame movie audio/APU output matches. 31 flash pictures are corrected, with at least 140,498 exact source pixels each; 390 ordinary pictures remain byte-identical.
- Clean build, every historical validator, all 126 archive-member hashes, ZIP CRC and flat installation layout pass. The rebuilt pack matches both actual replay installations. The 14.7-second preview contains all 882 captured frames at 60 fps and decodes cleanly.
