# Level 3 detail corrections — 0.11.2

Updates the three objects identified in the user's screenshots: the round red-and-white enemy projectile, split-looking tree branches, and magenta boot collectible. The collectible is separate from Randy's worn boots. The user approved this build on 2026-10-25 (America/New_York), saying "approved". It is the continuation baseline on `feature/level3-opening`; main remains 0.10.2 pending adoption. `evidence/level3_detail/approval.json` pins the reviewed commit and ZIP. Approval changes only source documentation and preserves all 99 installed bytes, including the historical review label in the installed README.

## Mapping and artwork

| Object | Native identity / palette | Registration |
| --- | --- | --- |
| Round enemy shot | `0694 / FF301116` | Exact existing 12×12 HD fireball centered in its 16×16 cell |
| Boot collectible | `068A–068D / FF301525` | One coherent 32×32 sprite, left-pointing toe, magenta leather, ivory cuff and brass buckle |
| Tree branches | `0768–0770 / 0F091929`, room `04/997A` | Solid two-row oak surface following all nine original alpha masks |

The prior 0.11.1 pass changed B6–B9 while calling those sprites the requested projectile. The new screenshot and native OAM establish that the round projectile is 0694. B6–B9's precise role remains unconfirmed; their historical artwork is preserved, and it is not counted as coverage of the requested shot.

The old branch builder cropped a single thin row and applied it independently to upper and lower native cells. Its transparent RGB pixels became opaque black when the native alpha was imposed, leaving the split appearance. The new builder registers a full branch body across both rows and samples opaque paint into the native envelope. It splits that registration into the exact short and long native arrangements, including the distinct lower middle variant. Every branch alpha byte stays identical to 0.11.1. The trunk, ground, native collision and all other scenery remain unchanged.

Built-in image generation produced `art/generated/level3_boot_generated.png` and `level3_branch_generated.png`; `level3_detail_prompts.json` retains the exact prompts and reference paths. Native references and registered images are in `art/level3_detail/`. The round shot reuses existing art, with the source mapping recorded in `registration.json`.

`build_level3_details.py` inserts 14 mappings ahead of earlier rules and adds `Stage3_Detail_Tiles_2x.png`. All 96 prior runtime files except mappings/README remain byte-identical. Removing the two marked detail blocks restores the exact 0.11.1 mapping hash. Existing validation continues down to approved main and earlier baselines. The installation contains 99 root files, with no nested ZIP.

## Verification

Use the stock MesenCE 2.2.1 runner, configuration shim and synchronized screenshot observer from `LEVEL3_OPENING.md`. Replay the unchanged user movie with stride 4, then:

```sh
python scripts/verify_level3_details.py --before "$CAPTURE_0111" \
  --after "$CAPTURE_0112" --out evidence/level3_detail/validation.json
```

The full 6,883-frame movie passes:

- 1,721 identical paired samples per RAM, PPU, OAM and PPU-view type.
- 15,528 identical APU writes and 21,995,512 identical PCM bytes.
- 223 changed pictures confined to the requested objects; 1,498 exact pictures, including 52 black transitions and 101 final-pause pictures.
- 49 complete round-shot matches and 25 complete boot matches in actual screenshots.
- 186,996 unoccluded branch pixels across 36 pictures match the registered artwork exactly.
- Every old runtime asset and each of the nine branch masks remain exact.

Two input-only derivatives retain the same embedded starting state and ROM settings. The direct right-edge route is generated with `make_level3_detail_edge.py`; the span/stop/slow-right-walk route adds `--span`. Their exact tested hashes, input sequence and starting-state hash are recorded in `art/level3_detail/{edge_route,span_route}.json`. Capture every frame from 1620 for the direct route and 1624 for the span route, then apply the same verifier. Only one emulator process may run at once.

The direct edge route passes 1,792 frames, 173 paired samples/type, 4,634 APU writes and 5,731,096 identical PCM bytes. The right-side trunk does not block movement in this native scene; walking beyond the branch's actual support causes the normal fall. The native silhouette has decorative overhang, so the sprite silhouette is not used as a collision boundary.

The full-span route passes 1,796 frames, 173 paired samples/type, 4,630 APU writes and 5,743,876 identical PCM bytes. Randy stops at native X90/Y368 for frames 1665–1676, walks slowly across X90–137 while remaining at Y368, then falls at X138/Y369 on frame 1741. The verifier asserts this sequence from the paired native RAM. Actual left-stop, span and walk-off screenshots are retained in `branch_edge.png`. Both branch routes change only the requested branch artwork.

One additional replay attempt stalled before the capture script initialized; it was interrupted and rerun in a fresh directory. No evidence is taken from that incomplete run. Intermediate controller drafts were used to locate the native support edge; only completed paired routes are acceptance evidence.

`comparison.png` contains cropped/enlarged actual before-and-after screenshots without retouching. The 11.33-second silent video uses 170 actual captures at 15 fps and original playback speed. Final packaging changes only the installed README from the full replay's pack; runtime mapping/image hashes are identical. `artifact.json` records the ZIP CRC, flat layout and SHA-256 checks.

The movie covers the three opening rooms and following corridor. Later Level 3 scenery, the boss, and a new boot-collection/menu test are not claimed. Earlier levels retain exact artwork/mappings but were not replayed afresh. No push, merge, release or tag is implied.
