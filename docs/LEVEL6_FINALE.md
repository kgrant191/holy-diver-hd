# Level 6 finale — 0.30.0 review

The final climb, both boss rooms and ending now use the updated artwork. The ascent has an open crimson vertical cathedral; the attached demon inhabits a dark red sanctum; its detached form floats in a blue-violet void. The creature keeps one visual identity across both forms. The ending adds two front-view green/gold dragon poses and preserves the existing Gothic story lettering and IREM logo.

This is a review candidate on `feature/level6-opening`, continuing approved 0.29.1. Main remains approved 0.24.0. No push, PR, merge, tag or release is authorized. Earlier Level 6 rooms skipped by the user remain unfinished. This is not the completed 1.0.0 pack.

| Native room | Scope | Updated content |
| --- | --- | --- |
| A49F / mode04 | Final vertical climb | Separate crimson backdrop, approved chitin ledges, complete flying skeleton/skull aliases |
| A553 / mode04 | Attached boss | Registered whole brain/root demon, four articulated joint poses, connector and attacks; crimson chamber |
| A58F / mode04 | Detached boss | Complete compact form, scrolling entrance and lateral movement, approved blob spores and player dragon; dark void |
| B01C / mode04 | Ending through “the end” | Two front-view dragon poses, native palette cycling/fades; existing font/logo preserved |

## Registration and preservation

All 150 previous art/audio/patch assets are byte-identical to 0.29.1. Only `hires.txt`, the installed README and thirteen new files change. The three removable `LEVEL6_FINALE` blocks recover the exact approved 0.29.1 mapping text; its frozen README restores the complete historical validation chain.

Boss forms are registered as whole images before native slicing. Repeated native cells share canonical artwork. Native damage removes the original body parts; alternate stumps keep their native outlines. Permanent blank cells inside the body use unique stable body anchors, so their painted interior follows scrolling and horizontal movement. Every relative anchor observation is preceded by all four screen bounds. No gameplay memory is written. The live observer checks native neighbor accesses.

Normal, hit and fade palettes retain updated art. All-black native fades stay black. Room/mode and rendered/nametable anchors prevent new artwork from leaking into menus or other rooms. The final climb retains exact approved terrain masks and collision edges; this update adds no new platform geometry.

Randy, HUD, spells, the player dragon, 1-ups, the crawler, flying skeletons and flying skulls reuse completed art. The ending dragon stays inside its measured two native sprite-cell unions and retains its three shared tail cells, OAM flips, priority and original motion. Story text and logo receive no new mappings.

The original green orb/rock source remains intact in `art/level6_organic/`, with its original rules/hashes recorded by `art/level6_enemy_revision/standby.json`. A future requested revert can restore it independently of the brighter face. The shipped candidate manifest describes the approved blob choice.

## Verification

`verify_level6_finale_rules.py` checks exact prior assets, removable mapping recovery, native-byte aliases, source bounds, shared ending cells and unique bounded body anchors. `validate_pack.py` runs the entire historical chain through exact baseline projections.

The full 19,215-frame 20261029-225605 movie is paired against frozen 0.29.1 using stock MesenCE 2.2.1. Every frame records RAM, PPU, OAM and view state; the comparison also checks APU writes, full PCM, menus, blackouts, whole sources and ending-only dragon changes. The first ending pose is visible as a complete source. The second pose is registered and checked statically; native behind-background priority conceals it during the scrolling text, so this movie does not prove a complete visible second pose. The prior 4,761-frame organic-room movie is an exact-image regression. No RAM edits or fabricated controller states are used.

Results, compact actual captures, complete manifests and isolated build evidence are in `evidence/level6_finale/`. The distributed preview uses the complete actual replay with original captured audio. ROM, movie input, emulator, raw frame dumps and savestates are excluded from source archives.

## Final blackout correction

A full candidate replay exposed five native background-disable frames between the boss forms and eight all-black dragon-fade frames. The final correction adds two rendered-bank observations to the detached backdrop and removes only the ending dragon's `FF0F0F07` aliases. These native dragon patterns never use color index 3, so that palette must remain black.

The final pack is replayed across frames 7400–9200, covering every native occurrence of both changed scopes. `verify_level6_finale_blackouts.py` requires byte-exact recovery of all other mapping text, all other installed files unchanged, identical native samples and full audio, and exactly those thirteen changed images. The full comparison and preview use untouched actual PNGs from the complete capture, replacing the affected window with actual final-pack PNGs. No frame is repainted or synthesized. The earlier regression's rooms cannot activate either changed scope.

The isolated build reproduces all 165 install hashes and passes every historical validator. A stale seed README exposed an unreliable fast-copy write on the mounted workspace; the build now writes and checks that note atomically before validation/packaging. The corrected packaging tail was rerun on the freshly built assets, and the final flat ZIP and all file hashes pass. See `clean_build.json` for the exact sequence.

## Completed results

The full 19,215-frame native RAM/PPU/OAM/view comparison and original APU/PCM pass. All 1,229 native black images remain black. Every measured gameplay backdrop is present, with zero continuity exceptions. Ending changes stay inside native dragon sprite bounds. Both boss forms, three joint poses, connector, all three rotating attack poses, shot and first ending pose have exact live source matches; the fourth joint pose and second ending pose have static registration coverage but no complete unobscured live match.

The final 1,801-frame scope capture covers all 1,411 detached-room native samples and all eight affected ending-fade samples. Exactly thirteen images change to restore native blackouts; every other captured image in that window is exact. The previous movie preserves all 4,761 native samples, full audio and all 4,760 rendered images. The 19,214-frame, 319.707-second actual preview passes full audio/video decode.
