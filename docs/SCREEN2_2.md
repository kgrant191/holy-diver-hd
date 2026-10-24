# Stage 2 screen 2 cave — original 0.5.0 candidate

Superseded by the [0.5.1 review fixes](SCREEN2_2_REVIEW.md), which remove the red decorative layer and animate hot falls. The measurements below describe the original candidate.

Branch `feature/screen2-2` starts at approved main `14434d6ff9604db085a968eda12b317d43474c47` (0.4.1). The user supplied the cave-entry state and asked why recurring enemies and lava appeared to require the same work again. The implementation reuses approved art wherever the native graphics match. New rooms primarily need identity/palette registration, scenery and live validation; they do not require redrawing every recurring object.

## Reuse and new work

| Element | Implementation |
| --- | --- |
| Randy, HUD, large flasks and defeat effects | Existing shared rules already apply |
| Gold terrain, pools, snow, small drops and figurines | Aliases point directly to the approved exterior atlas |
| Purple ghoul | Reuses all six approved poses and repaired standing heads; 24 byte-identical native patterns move from `0094–00AB` to `028E–02A5` |
| Ghoul standing conditions | Translate the neighboring sprite identities along with the tile rules; keep repairs before broad rolling mappings |
| Vertical lava falls `0389–038E` | Derive from approved pool body texture turned 90 degrees; preserve the native two hot palettes and ice palette |
| Cave scenery | New indigo/plum underground backdrop and burgundy hanging formations |
| Ceiling/underside edges | Approved gold material registered to native outer silhouettes |
| Ceiling bat `02A6–02B5` | New folded/open artwork fitted to the measured native OAM footprint |
| Bat projectile `02B6` | Reuses the approved boss fireball source at the native small size |

There are 86 shared aliases and 57 new tile rules, including transparency/palette variants. The new atlas uses 44 distinct cells. Scope requires native room `$0072=10` and room-data pointer `$0078/$0079=09/8B`; this bank is also used outside the cave, so identities alone are insufficient.

The 84-file pack adds `Stage2_Cave_Tiles_2x.png` and `Stage2_Cave_Background.png`. Among the 82 approved files, only `hires.txt` and installed `README.txt` change. All 80 prior asset files, including both Randy atlases, the nave/ghoul atlas, exterior art and the entrance IPS, retain exact hashes. Removing the marked `SCREEN2_2` additions recovers the approved mapping text exactly; the build validator enforces this.

## Artwork and registration

The built-in image generator produced the cave backdrop, burgundy rock material and bat sheet. Exact prompts and the refinement history are retained in `art/generated/screen2_2_prompts.json`. The coarse bat draft is provenance; the refined sheet is the build input. `art/screen2_2/native_ceiling_enemy.png` is an enlarged original-game anatomy reference from the supplied save.

`scripts/build_screen2_2.py` deterministically registers the assets. The bat's folded pose occupies 32×48 HD pixels. The open pose occupies 64×48, with only the two central cells in the bottom row; the builder requires zero opaque pixels outside that footprint. Native OAM continues to position every piece and time every attack.

The red rock's outer cap/tip masks follow the original silhouette. Internal black cracks become dark texture rather than transparent holes. Gold ceiling edges use the approved gold material and original outer boundary. Native tile placement and collision remain unchanged.

The background covers horizontal scrolling at native speed. Alternatives at the same rendered ceiling location enable it only when cave terrain is actually displayed. This preserves Blizzard's black frames and death/room transitions without relying on the delayed CPU PPUMASK shadow. The lava/ice palettes are `0F161606`, `0F060616` and `0F122131`.

`native_inventory.json` records streamed nametable identities, including stale exterior tiles in hidden nametable regions. It is discovery provenance, not proof that every listed tile was visible. `shared_chr.json` pins all 24 ghoul pattern hashes; the verifier checks them against the live cave PPU.

## Reproduction and coverage

Use MesenCE 2.2.1 and the supported translated ROM SHA-1 `fe2fcd0ad334d792db16535d09f3ab9fb2bea3ac`. The unchanged 9,052-byte `Holy_Diver_HD_1(8).mss` has SHA-256 `bffc454e176bee738d053802aa12a3558dba58a17400e1033148f7c0291d4db7`. Binary ROM/state/emulator inputs remain outside Git.

Build approved 0.4.1 separately, then run the same routes with that pack and this candidate:

```sh
python build.py
python scripts/verify_release.py
python scripts/run_screen2_2_qa.py --mesen /path/to/Mesen --rom '/path/to/Holy_Diver_(Tr).nes' --pack /path/to/0.4.1-pack --state '/path/to/Holy_Diver_HD_1(8).mss' --route scripts/screen2_2_routes.json --stride 2 --out work/screen2_2/before
python scripts/run_screen2_2_qa.py --mesen /path/to/Mesen --rom '/path/to/Holy_Diver_(Tr).nes' --pack 'build/Holy_Diver_(Tr)' --state '/path/to/Holy_Diver_HD_1(8).mss' --route scripts/screen2_2_routes.json --stride 2 --out work/screen2_2/after
```

Repeat with `screen2_2_approach_routes.json` and `Holy_Diver_HD_1(7).mss`, outputting `approach-before` and `approach-after`. That input's checksum is in `test_states/README.md`.

```sh
python scripts/verify_screen2_2_qa.py --before work/screen2_2/before --after work/screen2_2/after --approach-before work/screen2_2/approach-before --approach-after work/screen2_2/approach-after --out evidence/screen2_2/verification.json
python scripts/export_screen2_2_preview.py --before work/screen2_2/before --after work/screen2_2/after --out evidence/screen2_2
```

Five controller-only routes total 5,680 emulated frames per build, sampled every second frame for graphics/RAM/PPU/OAM. APU writes and PCM are continuous. No RAM, position, health, inventory or timing edits are used. The crossing controller reads native state to choose button presses for Blizzard; its exact callback and input checksums are recorded in the report.

The verifier requires equal native memory/APU events, byte-identical common PCM with at most one 3,200-byte shutdown buffer difference, exact native blackouts, unchanged pause/outside-room captures, observed hot/ice palettes, every new bat/shot identity, and complete registered sprites in actual screenshots. Screenshots are authoritative: fast diving bats are located by exact sprite pixels because their endFrame OAM coordinates can describe a different pose/time. Ghoul matching checks both directions and reports each pose separately. The final report passes 2,840 paired native samples per memory type, 258 exact black captures and 262 exact outside-cave captures. It locates 1,866 complete folded-bat and 74 open-bat sprites, and all six ghoul poses in both directions. See `evidence/screen2_2/verification.json` for per-case audio tails and sample coordinates.

Live coverage reaches native scroll 569: the cave entry, repeated ceiling formations, shared ghouls, first lava fall and opposite ledge, freeze/thaw, pause menu and death/respawn. The approach route also verifies the approved exterior before the room transition. **The full cave exit has not been reached; later cave layout and exit behavior remain untested.** Do not interpret registered identities or static preservation checks as complete-room gameplay coverage.

The comparison and silent preview use unretouched Mesen frames. The preview runs captured two-frame samples at 30 fps, preserving gameplay speed. This remains a development review candidate; main is approved 0.4.1. User push, PR, actual Actions artifact checks and approval are pending. No release tag is created.
