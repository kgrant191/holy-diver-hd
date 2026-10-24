# Stage 2 screen 3 — vertical cave (0.6.0 implementation)

The original implementation and its verification are retained below. The approved 0.6.1 build replaces only the eye projectiles with blue tears; see [review repair](SCREEN2_3_REVIEW.md).

The user approved 0.5.1 and supplied `Holy_Diver_HD_1(9).mss` for the next screen. The original candidate was on `feature/screen2-3`, stacked on approved `feature/screen2-2`. Both were subsequently merged through PRs #6/#7 after the user explicitly authorized them. Main now contains approved 0.6.1, including the blue-tear repair. No public release or tag was created.

## Artwork and reuse

The room descends through staggered gold platforms to a lava pool, then exits to the right. Its new enemy is a floating eye with an ivory/teal center and compact crimson spiked rim. The native four-tile body stays 16×16 native / 32×32 HD. The two shot identities retain their measured bounds, OAM flips, trajectory and cadence while using the accepted fireball source.

The backdrop, gold terrain, ghouls, lava/ice, pickups, player and HUD reuse approved artwork. This room needs identity registration and runtime checks, not a new drawing of every familiar object. Ninety-eight scoped aliases reuse existing atlas cells and ghoul pose anchors. Six nonsolid purple wall-pattern identities become transparent to reveal the accepted cave panorama. The distant layer stays stationary while native platforms scroll vertically; this avoids exposing an edge during vertical camera wrap. No new background PNG is added.

| Native identity | Registration |
| --- | --- |
| `032E–034D`, `035B–035E`, `03A1–03A2` | Approved gold terrain, pool and ice cells |
| `028E–02A5` | Approved six ghoul poses and standing anchors |
| `0300`, `0247–0248`, `024E–024F`, `0274` | Existing empty-space, pickup and Blizzard cells |
| `039B–03A0`, palette `0F041625` | Clear nonsolid wall motif |
| `02D8–02DB`, palette `FF060C30` | New floating eye, registered as one complete body |
| `02DC`, palette `FF301116` | Shared fireball fitted within native X1–6/Y0–7 |
| `02DD`, palette `FF301116` | Shared fireball fitted within native X0–6/Y1–7 |

Scope is RAM `$0072=04`, `$0078=F9`, `$0079=8B`. The pointer guard distinguishes this room from earlier rooms/cards that also use ID 04. Eighteen alternative rendered-tile probes gate the cave panorama, preserving native black frames. All additions have removable `SCREEN2_3` sections; removing them recovers the exact approved 0.5.1 mapping file.

Source image and full generation prompt are retained in `art/generated/screen2_3_eye_generated.png` and `screen2_3_prompts.json`. The decoded native anatomy reference and measured patterns are in `art/screen2_3/`. Registration is deterministic in `scripts/build_screen2_3.py`. The only new installed file is `Stage2_Vertical_Cave_Tiles_2x.png`.

## Replay and coverage

Use the existing controller-only cave runner with the new route file. Run one Mesen process at a time. Retain the approved 0.5.1 pack before building this candidate, then capture each pack separately:

```sh
python build.py
python scripts/verify_release.py
python scripts/run_screen2_2_qa.py --mesen /path/to/Mesen --rom '/path/to/Holy_Diver_(Tr).nes' --pack /path/to/0.5.1-pack --out work/screen2_3/before --state '/path/to/Holy_Diver_HD_1(9).mss' --route scripts/screen2_3_routes.json --stride 2
python scripts/run_screen2_2_qa.py --mesen /path/to/Mesen --rom '/path/to/Holy_Diver_(Tr).nes' --pack 'build/Holy_Diver_(Tr)' --out work/screen2_3/after --state '/path/to/Holy_Diver_HD_1(9).mss' --route scripts/screen2_3_routes.json --stride 2
python scripts/verify_screen2_3_qa.py --before work/screen2_3/before --after work/screen2_3/after --out evidence/screen2_3/verification.json
python scripts/export_screen2_3_preview.py --before work/screen2_3/before --after work/screen2_3/after --out evidence/screen2_3
```

Four routes cover the full descent, eye projectiles, ghouls, both movement directions, upward/crouching casts, pause/resume, hot/frozen lava, native black flashes, death/respawn and next-room arrival. The descent reaches vertical scroll 512 and exits into room `10`, pointer `AD/8C`, using ordinary controller input and two Blizzard casts. Initial scroll 768 is stale previous-room state and is not counted as traversed distance. There are no RAM edits.

The CPU changes the room pointer before replacing the outgoing picture. Completed next-room arrival is therefore checked using its rendered palette `0F061828`; the outgoing transition retains this room's HD artwork. The next room's scenery is unchanged and remains future work. This new save does not retroactively establish traversal of the entire preceding horizontal cave.

Death briefly applies native grayscale/emphasis without changing palette RAM, then disables background rendering while sprites continue. Exact panorama-RGB checks apply only while the original colored wall is visibly rendered; grayscale/death captures were inspected separately. The first draft verifier incorrectly treated unchanged palette RAM as proof of full-color rendering. Correcting that test assumption required no candidate artwork changes. Final checks retain strict native-memory, audio, blackout and next-room comparisons.

Final verification passes 5,560 frames per build, 2,780 paired samples of each native-memory type, 106 native black captures, 270 unchanged next-room captures and 1,957 exact full-color panorama samples. APU events and common PCM are identical; only the menu recording has a 3,196-byte audio shutdown-tail length difference (less than one capture buffer). Complete sprite matches include all six ghoul poses in both directions, the eye body and both shot shapes/flips.

See `evidence/screen2_3/verification.json` for exact counts and sprite examples, `comparison.png` for actual paired frames, and `preview_sources.json` for the unretouched video/still selections. The video is silent and runs two-frame captures at 30 fps; audio equality is tested separately from the recorded PCM and APU events.

## Preservation and delivery

There are 85 files at the install ZIP root. Among the 84 approved 0.5.1 files, only `hires.txt` and `README.txt` change; all other 82 files, including the cave panorama, earlier lava-fall animation atlas, player artwork and entrance audio patch, remain byte-identical. Native collision, timing, inventory, lives and audio remain controlled by the unchanged game.

`evidence/0.5.1-reviewed-pack-sha256.json` pins the accepted runtime build, and `0.5.1-pack-sha256.json` pins its approval bookkeeping. `0.6.0-pack-sha256.json` and the historical filename `approved-pack-sha256.json` describe this review candidate; that filename does not grant user approval. Local build/replay checks are separate from GitHub Actions, which remains pending until the user pushes the bundle.
