# Holy Diver HD working instructions

## Current continuation — Golden Temple courtyard 0.17.0

- AAF9/mode08 is indoors; AB71/mode10 is outdoors; the recorded AC61/mode04 re-entry is indoors. The rest of AC61 is not traversed. Clone final 0.16.3 rules, including ordered bounds and stair repairs, rather than the original 0.16.0 builder.
- Room palettes distinguish decoration from physical cells: AAF9 0F071723 windows reuse staircase patterns. These are decoration; 0F172737 is the recorded solid palette. AB71 clouds/fences are decoration; native 0B92–0BA1 forms the four-by-four statue.
- Wings are 0A92/0A93 in a 32x16 HD footprint; eight byte-identical banks are proven. Fire-chain beads are 0AE1/FF162830, each independently moved by native OAM. Never replace the whole moving chain with a static ring.
- New atlas50 leaves every earlier asset unchanged. Keep exact recovery of 0.16.3 and all older validators. Work remains pending review, no merge or release authorized.

## Approved continuation baseline — 0.16.3

- On 2026-10-26 the user accepted the delivered repair ("ok good") and requested the next recorded rooms. Preserve all 111 installed files as the reviewed baseline; approval bookkeeping must not alter the frozen installed README. Main remains 0.15.0; no push/merge/release is authorized. See evidence/level4_stairs/approval.json.

## Current stair repair — Golden Temple 0.16.3

- The supplied 20261026-181741 state proves 0B7C–0B7F are descending stairs, not decoration. build_level4_stairs.py overrides the erroneous clear rules with 24 room/palette mappings. Preserve their native top surface and joined sloped underside. Do not apply the historical scenery classification to these cells.
- Reuse existing stone RGB; preserve every 0.16.2 asset and its neighbor bounds/pickup fixes. The additional atlas is index49. Opposite-facing 0B80–0B87 remain exact.
- Require paired save-state movement and full-movie checks through verify_level4_stairs.py, with native state/full audio equality and stair-only image differences. See docs/LEVEL4_STAIRS.md. Candidate is unapproved on feature/golden-temple; main remains 0.15.0.

## Current repair — Golden Temple 0.16.2

- The user reports old small drops outdoors and a crash entering the temple. The diagnostic catches a stock Mesen tileNearby read at index61440 (one past the screen) on entry. Do not call the earlier successful uninstrumented replay proof of memory safety.
- build_level4_repairs.py bounds all new pillar neighbor evaluations, including inverted checks, while preserving off-screen/no-neighbor behavior. Keep the exhaustive bounds regression in validate_pack.py. Do not ship or require the diagnostic observer.
- Reuse exact atlas25 heart/crystal pixels for byte-proven pickup aliases; earlier conditional/menu rules retain priority. Every 0.16.1 image/audio/patch file stays exact. See docs/LEVEL4_REPAIRS.md and evidence/level4_repairs/.
- 0.16.2 remains a review candidate on feature/golden-temple. Main stays approved 0.15.0; no merge/release authorization is implied.

## Current revision — Golden Temple 0.16.1

- The user accepted the 0.16.0 backgrounds and outdoor fluted columns, but rejected its square slabs and indoor block-stack supports. Preserve those accepted assets exactly; this is partial art acceptance, not whole-pack approval.
- build_level4_masonry.py adds atlas48 and scoped overrides after the unchanged 0.16.0 builder. Solid blocks use the native staggered four-by-two layout. 0B4E–0B51 are confirmed destructible blocks; 0B78–0B7B are indoor structural columns with contextual caps/bases. Keep 0B4A–0B4D cleared as nonsolid scenery.
- Preserve all 107 earlier art/audio files, actors, Overdrive/menu fixes, and native gameplay/audio. Existing stair masks remain exact. Source/evidence: docs/LEVEL4_MASONRY.md, art/level4_masonry/, evidence/level4_masonry/. concept_only.png is generated design reference, never runtime evidence.
- 0.16.1 is awaiting review on feature/golden-temple. Main remains 0.15.0; no push/merge/release is implied.

## Current review — Golden Temple 0.16.0

- Work is on feature/golden-temple from approved main 2f38abeb. The user requested an outdoor first area, indoor next area, corrected Overdrive spelling and updated spell graphics. The 109-file candidate is awaiting review; do not merge or label approved.
- Scenery scopes: mode1C/A865 outdoors, mode08/AA09 and mode08/AA81 indoors. Keep rendered guards including 0F071723 at frame6500. Background priority1 stays behind actors. Preserve native collision contours and continuous shafts.
- The actual Overdrive cast is 0A8A–0A8D, an orbiting orb, with ten CHR-proven bank copies. Select enables selected magic. 088B–088E is the acquisition orb; CB–CF is the gargoyle crescent attack, not the player spell.
- Preserve all 104 previous art/audio files and exact recoverable 0.15.0 mappings. New scope/provenance/evidence: docs/LEVEL4_GOLDEN_TEMPLE.md, art/level4/, evidence/level4/. The source handoff is a ZIP-wrapped incremental bundle. Later temple areas/boss remain untested.

## Approved baseline — 0.15.0 on main

- The user approved 0.15.0 and authorized all five Level 3 merges on 2026-10-26. PRs #13–#17 are merged into main in dependency order. All PR/main builds pass, and all ten downloaded artifacts match their frozen hashes and flat install layouts. Preserve all 106 reviewed installation bytes, including the historical installed README. See evidence/level3_finale/approval.json and evidence/stage3_adoption/.
- Next area: Level 4 / Golden Temple. Start a focused branch from approved main. Stage 4 scenery remains unfinished; only its title card and the recorded initial arrival are covered. Historical sections below retain their original delivery-time labels; this baseline takes precedence.
- Final climb 9F1A / boss 9F92 use mode 04. Reuse exact approved moss terrain and native contours. The pink head uses twenty cells in a 64×96 footprint; each entire curved shot fits its staggered native cell union. Preserve native OAM flips, occlusion, emergence and defeat removal.
- Boss heads carry NES behind-background priority. The ruin panorama must use background priority 1, behind those sprites; native living growths remain in front. Normal backdrop guards must include the organic ceiling cells. Native universal-color flashes remain visible.
- Preserve all 102 previous art/audio assets and exact recoverable 0.14.0 mappings. Add shared native-byte-proven 0800/0A00 actor aliases after the existing specific mappings. Preserve the 56-byte entrance IPS and native audio.
- Overdrive is the native four-tile orb 088B–088E. Stage 4 card uses palette 0F131C29; reuse the approved card sources. Stage 4 scenery is outside this change. Cards 1–4 are now live-verified; cards 5–6 remain unverified.
- Evidence and precise limits: docs/LEVEL3_FINALE.md, evidence/level3_finale/. The five Level 3 branches are merged. Future merges require user authorization; no release tag is requested.

Read README.md, STATUS.md, docs/ART_DIRECTION.md and docs/TESTING.md before changing the project. Update STATUS.md and CHANGELOG.md when work changes the approved build or leaves a concrete follow-up.

## Approved Poison Moss Land continuation — 0.14.0

- Work is on `feature/poison-moss-land`, based on 0.13.0 at 06a53b9. The user explicitly requested a greener Level 3 distinct from the reused caves/rocks. This direction supersedes the historical Level 3 brown/cave reuse instructions below; Stage 1/2 remain unchanged.
- `build_poison_moss.py` runs after shared fallbacks and inserts its scoped overrides before existing mappings, preserving original priority. Three newly painted sources supply a moss forest, overgrown Gothic ruins and green masonry. Preserve every terrain alpha contour and all original native guards, including solid supports 0796/0797. Preserve continuous oak overlays and branch wood.
- All 99 prior art/audio files and all fish mappings remain exact. Only Level 3 scenery references change, plus installed README. Removing the marked overrides and reversing recorded background substitutions must recover exact 0.13.0 hires.txt.
- The user approved the complete delivered 0.14.0 pack on 2026-10-26. Preserve all 104 reviewed installation files exactly for approval bookkeeping; keep installed README frozen. Main remains 0.10.2. This is the continuation baseline, including previous Level 3 work and fish corrections. See evidence/poison_moss/approval.json and docs/POISON_MOSS.md.

## Previous Level 3 caves review — 0.13.0

- Work is on `feature/level3-caves`, based on review 0.12.2 at fb1fb4d. The user still saw fish shaking in the next room, where several fish appear together. 0.12.2's one-fish/one-room guard was insufficient.
- `build_big_fish_motion.py` now registers each complete fish independently at its native player-relative horizontal hover equilibrium. Match the actual tile origin; preserve the stock Mesen 2.2.1 mirrored-origin workaround pairing originPositionCheckX with positionCheckX. An origin-only mirrored guard changes isolated pixel stripes and is incorrect. Do not change native movement, hit blinking or source poses. Partly clipped boundary sprites retain original registration.
- `build_level3_caves.py` covers room pointers 9B96, 9C86, 9CFE and the recorded beginning of 9DEE, with modes 10/04/10/14. Inventory all four PPU nametables: the vertical room uses the second vertical page. Native 0796/0797 with 0F0A1A29 in 9CFE/9DEE are solid supports, not removable decoration; only the measured 9C86 dark wall palette is decorative.
- Reuse approved cave, brown rock, carved stone, lava/ice, bats and blade rings. The green floating creature is the only new painted source; its twelve-cell 64×64 footprint and missing upper-left/lower-right cells are preserved. All 98 previous art/audio files remain exact.
- This is unapproved. Main 0.10.2 and approved continuation 0.11.2 remain pinned. See docs/LEVEL3_CAVES.md and evidence/level3_caves/.

## Previous large-fish hover review — 0.12.2

- The user's new movie demonstrates native horizontal hover oscillation in the large fish without damage. 0.12.1 repaired a separate small-fish color problem; do not claim it addressed this report.
- Keep the original painted fish and native gameplay exact. `build_big_fish_motion.py` adds ±1 HD-pixel registrations only for the measured one-fish hover/cruise state in room 9AA6. Preserve both mirrors, original fin/vertical motion, attacks and hit blinking. Multiple-fish ambiguity falls back to original art.
- Do not shift individual limbs or redraw the fish. The complete 48×48 source shifts together inside its measured margin, with no clipping. Original atlas cells remain exact; the twenty new cells occupy X0–319/Y496–511.
- See docs/BIG_FISH_MOTION.md and evidence/big_fish_motion/. 0.12.2 is unapproved; main 0.10.2 and approved continuation 0.11.2 remain pinned.

## Previous small-fish motion review — 0.12.1

- The user clarified motion blur/glitching, not a request to sharpen or redesign the fish. Preserve original generated art, both large poses and the first small pose. The small alternate pose now shares the base palette and static head/body pixels. Keep reserved atlas slots so all existing mappings stay exact.
- Native large-fish hit blinking is present in OAM and must remain. Do not describe generic alternate-frame flicker as an HD mapping bug. Capture consecutive frames for motion defects; stride two cannot reveal every alternating phase.
- See docs/FISH_MOTION.md and evidence/fish_motion/. 0.12.1 is unapproved, based on review 0.12.0; 0.11.2 remains the approved continuation baseline. Main is 0.10.2.

## Previous Level 3 lava review — 0.12.0

- Work is on `feature/level3-lava`, based on approved `feature/level3-opening` at 9eb0678. The new corridor, menu boot, fish and Breaker casts are a review candidate, not approved. Preserve the frozen 0.11.2 manifest; main remains 0.10.2. See docs/LEVEL3_LAVA.md.
- Lava room scenery is limited to RAM mode 10 / room 9AA6 and exact hot/ice palette guards. Menu boots are background IDs 0971–0974; reuse the approved collectible art. Small unflipped fish point right; native OAM mirroring makes the left-moving form face left.
- Breaker uses 0675–0689 (charge, horizontal release/bolts, upward release/bolts) and twelve proven identical bank copies with both FF221136/FF300036 palettes. Preserve native OAM flips, timing, MP costs and stair destruction.
- Runtime changes from 0.11.2 are hires.txt, README.txt and one new Stage3_Lava_Tiles_2x.png atlas. All 97 other approved runtime files stay exact. Shared Stage 2 fallback remains last.

## Approved Level 3 continuation baseline

- The user approved 0.11.2 on `feature/level3-opening` on 2026-10-25 (America/New_York), saying "approved". Preserve all 99 reviewed installation files exactly. This is the continuation baseline; main remains at merged 0.10.2 pending the source push, PR and merge. See `evidence/level3_detail/approval.json`, `docs/LEVEL3_DETAILS.md` and the paired live evidence. Approval bookkeeping changes source documentation only; keep the installed README frozen.
- Preserve the complete native wood masks, including partially visible top-row cells. The reported round shot is 0694/FF301116; 068A–068D/FF301525 form the boot collectible (not Randy’s boots). The 0.11.1 attribution of 06B6–06B9 as the reported projectile was incorrect. Preserve those historical sprites pending a separate identification; do not use them to claim round-shot coverage. Branches 0768–0770 use complete two-row registration with exact native alpha contours.
- The `.mmo` input embeds the correct starting state and matches the project's ROM. Use `run_mesen_movie.py` with the stock MesenCE 2.2.1 native core, configuration shim and synchronized screenshot observer. Do not replace it with MesenAI. Input bytes remain outside Git.
- NES endFrame fires before video submission; asynchronous HD decode can otherwise produce a one-frame capture mismatch. `sync_movie_capture.cpp` waits for the pending decode and then calls the original screenshot routine without changing pixels or native state.
- New Level 3 scenery rules are limited to the three measured room pointers; actor aliases use proven native CHR copies. Preserve original conditional priority and the last shared Stage 2 fallback block.

## Approved latest repair

- The user approved 0.10.2 and authorized its merge on 2026-10-24 ("approved. merge it"). PR #12 is merged; main is the approved 0.10.2 baseline. The repair keeps HD Randy through the three final Breaker pickup fades. Preserve all 93 reviewed installation bytes. Approval and artifact records are in `evidence/breaker_randy/`. See `docs/BREAKER_RANDY.md` and `evidence/breaker_randy/validation.json`.

## Approved main and source history

- Approved continuation baseline: **0.10.2 on `main`**. The user approved the delivered boss and defeat/pickup repairs on 2026-10-24; see `evidence/boss2_review/approval.json`. Preserve all 93 reviewed installation files exactly, including the original brown ceiling, accepted stairs and shared Stage 2 artwork. PRs #8–#11 are merged into main after the user authorized all four merges.
- The current source handoff includes `feature/screen2-4`, `feature/screen2-5`, `feature/screen2-6` and `feature/2-boss`. Older refs stay at their earlier source commits; screen2-6 includes the 0.9.0 approval record. No release/tag is requested. Boss artwork is approved; PRs #8–#11 merged in dependency order (screen2-4 → screen2-5 → screen2-6 → 2-boss), retargeting each successor to main. PR/main builds and all downloaded artifacts pass. See `evidence/stage2_adoption/merges.json` and the four `main_artifact.json` records. The 0.10.1 repair covers both gold defeat-fade palettes and removes the dead boss silhouette during Breaker flashes; preserve the native room flash.
- Finished artwork must be reused for matching native identities/palettes. `build_shared_stage2.py` appends fallbacks after all specific rules; the Poison Moss postprocessor preserves that priority. Verified new-bank aliases retain pose conditions; put broad aliases after existing specific rules. Never globally clear scenery. See `docs/SCREEN2_6.md` and `docs/BOSS2.md`.

## Preserve approved behavior

- Current approved development version on main: 0.10.2. Includes all approved Stage 2 work through the boss and Breaker fixes, plus the Stage 2 cave/lava flow (PR #6) and vertical cave with blue eye tears (PR #7). The user explicitly authorized both merges on 2026-10-24 ("merge it"); both are merged. PR/main Actions builds and actual downloaded 84/85-file artifacts were verified. See STATUS.md and evidence/screen2_3_review/approval.json. Imported artwork baseline: historical v15.1. Preserve approved artwork and native gameplay except for the user's requested change.
- Preserve the title sequence: clean splash, first Start reveals PRESS START, second Start starts play. Preserve the exact Entrance_SFX_Priority.ips bytes.
- Randy's normal/Twin Fire art is shared across matching native identities. Fix shared assets/mappings where appropriate instead of adding needless room-specific copies.
- The red winged-skull drop is a bracelet. Its collected Start/pause-menu icon must use the same bracelet artwork.
- Preserve native collision, animation timing, inventory, lives and audio. Use controller input for visual tests; do not patch RAM to fabricate evidence.
- Pose-specific hires.txt rules precede broader rules: Mesen uses the first matching replacement. Preserve native per-sprite flip behavior and OAM footprints.

## Build and verification

- Python 3.12; install requirements.txt. Run `python build.py` and `python scripts/verify_release.py` against the approved pack manifest.
- For visual changes run relevant live Mesen replays and inspect actual captures in both directions and affected palettes. Atlas mockups alone are not evidence of runtime correctness.
- For limb repairs, inspect the whole joint and silhouette against a clear backdrop. Alpha connectivity and pixel-exact rendering alone missed the rejected 0.3.3 knee/shin break; register adjoining limb sections together and check their outline across tile boundaries.
- For platform artwork, test the complete span, far-left stop, and slow walk-off at the right edge. A grounded sprite can overhang collision tiles; do not extend solid artwork to the full OAM or boot silhouette.
- Perform routine emulator testing here when inputs/tools are available; do not ask the user to perform it instead.
- Only one Mesen process at a time. Do not replace its pack or overwrite the audio-capture library during a run.
- The first screenshot after loading a state can be empty. endFrame OAM can describe the next pose; screenshots are authoritative for visual claims.
- Report coverage precisely. Stage cards 1–4 are verified in live play; cards 5–6 remain mapped but untested.
- Review and document intentionally changed files before updating expected hashes; do not weaken validation merely to make it pass.

## Repository workflow

- Keep main as the approved baseline. Use focused branches for later changes unless the user directs otherwise. Preserve unrelated work.
- Use this chat for bugs, priorities and approvals. Do not introduce GitHub Issues or a TASKS.md backlog unless requested. Push changes on the requested branch and open a PR for review; merge only after user approval.
- For artwork-heavy changes, prepare a ZIP-wrapped incremental Git bundle and exact fetch/push commands. The user pushes with their local Git credentials; use the GitHub integration for PRs and Actions. Avoid transferring large encoded images through tool arguments or chat. Small text-only changes may use the integration directly.
- Actions artifacts are development test builds. Publish release tags or GitHub Releases only when explicitly requested; reserve the completed release for 1.0.0.
- Upload the extracted pack contents to Actions artifacts, never a ZIP inside the artifact ZIP. One extraction must expose hires.txt and the installable assets.
- Follow semantic versioning in docs/REPOSITORY_WORKFLOW.md. Keep VERSION, INSTALL.txt, README.md, STATUS.md, CHANGELOG.md and approved pack hashes consistent when approving a new version. Reserve 1.0.0 for the completed, tested game pack.
- Commit source art, mappings, scripts, compact evidence and notes. Exclude ROMs, emulator binaries, savestates, credentials, raw frame dumps and build archives.
- Local test-input names/checksums are in test_states/README.md; input bytes are ignored by Git.
- Existing rollback folders are build inputs and provenance. Do not delete them until their consumers have deliberately been migrated.
- CI validates/builds without a ROM. Live emulator review remains separate for visual work.
- User instructions and authorization in the active conversation take precedence over these defaults.
