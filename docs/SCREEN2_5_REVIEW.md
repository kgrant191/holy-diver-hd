# Cave review — 0.8.1 candidate

The user rejected the 0.8.0 rock-textured stairs, heavy gold/brown ceiling fill and foreground red columns, and reported a hollow-looking health item. This review remains on feature/screen2-5, stacked on the unmerged feature/screen2-4 branch. Main remains approved 0.6.1. No approval, merge, tag or release is implied.

## Changes

All twelve stair identities 0375–0380 in 2-4 and 2-5 now use cut-stone faces with pale tread edges. The complete 32×32 registrations have exactly the previous alpha contours, keeping the native step positions and silhouette. This makes the steps distinct from the gold cave walls without moving collision boundaries.

The twelve foreground red-column identities are transparent in 2-5. The accepted crimson panorama remains byte-identical. Heavy gold ceiling fill is also removed. Because 0330–0333 and 0381–0384 serve both ceiling and ground, scoped lookups preserve their original artwork wherever a native platform cap appears above them in the same column. Y guards prevent those probes wrapping across the screen. A narrow dark crimson rim follows overhead boundaries; the original gold platforms and breakable blocks remain visible. Earlier rooms are unaffected by the scenery override.

The health screenshot shows a different native pickup: a four-tile handled jug at 0276–0279, rather than the two-tile 49/4A bottles covered by 0.3.5. It was still displaying its original hollow white-outline sprite. The new red enamel/brass jug has binary alpha, a fully opaque vessel and a transparent handle opening. It fits the native 32×32 four-tile footprint. ROM comparison finds five identical groups at 0276, 068E, 0A8E, 0C8E and 129A; palette FF301116 and those exact identities share the replacement. Previously approved HP/Magic bottle art stays byte-identical.

The built-in image-generation tool produced `art/generated/screen2_5_stair_tread_generated.png` and `screen2_5_health_jug_generated.png`. Exact prompts are in `screen2_5_review_prompts.json`. `build_screen2_5_review.py` deterministically registers those sources, clips the native stair masks, derives narrow ceiling contours and adds the mappings ahead of their earlier matches. The new atlas is `Stage2_Cave_Review_2x.png`.

There are 548 additive rules and 87 conditions. Removing SCREEN2_5_REVIEW blocks recovers exact 0.8.0 mappings. All 86 inherited runtime assets remain unchanged; only hires.txt and installed README change, plus one new atlas. The install ZIP contains 89 root files.

## Validation

Use MesenCE 2.2.1 and the unchanged `Holy_Diver_HD_1(20261024-155045).mss` (SHA-256 `8a67bbf57e6d756e36f4f6f42934d27b40c6266d95f6fc24118244c89e53ee40`), with translated ROM SHA-1 `fe2fcd0ad334d792db16535d09f3ab9fb2bea3ac`. All replay routes use controller input and read-only state inspection; no RAM or ROM edits fabricate evidence. Run one emulator at a time.

```sh
python build.py
python scripts/verify_release.py
python scripts/run_screen2_5_qa.py --mesen /path/to/Mesen --rom '/path/to/Holy_Diver_(Tr).nes' --pack /path/to/0.8.0-pack --out work/screen2_5_review/before --state '/path/to/Holy_Diver_HD_1(20261024-155045).mss' --route scripts/screen2_5_review_routes.json --stride 2
python scripts/run_screen2_5_qa.py --mesen /path/to/Mesen --rom '/path/to/Holy_Diver_(Tr).nes' --pack 'build/Holy_Diver_(Tr)' --out work/screen2_5_review/after --state '/path/to/Holy_Diver_HD_1(20261024-155045).mss' --route scripts/screen2_5_review_routes.json --stride 2
python scripts/verify_screen2_5_review.py --before work/screen2_5_review/before --after work/screen2_5_review/after --routes scripts/screen2_5_review_routes.json --out evidence/screen2_5_review/verification.json
```

Five paired routes pass **6,800 frames per build** with **3,400 exact RAM/PPU/OAM/PPU-view samples per type**, identical APU writes and identical full PCM (zero shutdown-tail difference). All 80 black captures, 259 outside-room captures and 56 pause-menu captures stay exact. The verifier checks 25,569 gold platform-body cell interiors and finds 352 complete source matches across the two stair directions and landing. In 2-4, image changes stay inside native stair cells.

The extended controller route reaches camera scroll **482** (world X 610), revealing the lava fall beyond the earlier 281-pixel coverage, then dies and returns. Both stair flights, the upper transition, eye platforms, native hot fall, Blizzard flashes at the room entry, menu and death/return are covered. The far exit of 2-5 and uninterrupted traversal of the previously untested middle of 2-4 remain unverified.

**The handled jug is not observed in this replay.** Static checks prove the five exact native CHR groups, 32×32 footprint, binary alpha and fully opaque vessel core. Its in-game appearance, collection and later bank copies still require a save with that pickup visible. No synthetic gameplay image or fabricated collection evidence substitutes for that missing check. The user's screenshot is retained as the native identity reference; `health_jug_static.json` records the explicit limit.

The comparison and silent video use unretouched actual 0.8.0/0.8.1 captures. Neither includes a pretend live jug capture. The local install ZIP passes CRC, flat-root layout and all 89 SHA-256 checks; no nested ZIP is present. GitHub Actions checks remain pending the user's push.

## Handoff

The source bundle includes feature/screen2-4 and feature/screen2-5 against approved main 5fdae8a88920ad6612d9f01ee913d85af6837209. The final 0.8.1 branch includes the newer stair appearance; feature/screen2-4 itself retains the earlier 0.7.1 candidate. Downloads-based commands publish both review refs without merging or releasing. PRs and Actions artifact checks follow the user's push.
