# Golden Temple final halls and boss — 0.20.0 review

The supplied `Holy_Diver_HD(9).mmo` traverses two more indoor halls and enters the boss room. It ends with the player's death and game over. This continuation covers the recorded encounter, not boss defeat or a reward sequence.

| Native room | Mode | Recording frames | Treatment |
| --- | --- | --- | --- |
| AE41 | 0C | 1–3530 | Finished interior, stone/stairs, sentinel and rings |
| AEF5 | 0C | 3531–6248 | Same interior material and returning actors |
| AFA9 | 04 | 6249–7373 | Dimmed interior, rotating eye tower, moving stone ledges |
| Game over | — | 7374–7591 | Native transition and existing game-over artwork |

Pause samples temporarily use roomFFFF. First-byte-match inventories call the hall background bank0B; its actual physical bank is0D, byte-identical across all 256 patterns. Boss actor/HUD0E00–74 equals0A00–74. Registration records retain the exact source mappings and native pattern proofs.

## Artwork and registration

`prepare_boss4.py` registers four generated sources: one continuous teal/bronze cylinder material, an open crimson eye, the matching closed cover, and two gold/crimson ring poses. Prompts and original sources are committed. Each boss band is112×64HD pixels, seven native tiles wide and four tall. The three bands change independently among eight native layouts. A complete band is composed before tile cuts; its native whole-layout signature selects the correct phase. Normal and white-hit art use the game's original palette events. Native partial eyes wrap at the band edges.

The rings keep one 32×32 scale across both poses. Their aliases are byte-proven; native OAM mirroring, positions and timing remain authoritative. Returning sentinels reuse the previous whole 96×96 sources and native hit/decoy palettes. Moving platforms reuse the accepted 64×32 stone source, using native neighboring sprites to distinguish repeated left/right halves. The existing interior panorama is unchanged; boss rules render it at brightness0.5 and priority1, behind sprites.

The boss panorama requires an actual rendered tower cell at one of five vertical sample positions, including the first partially drawn band. A blank-tile guard incorrectly revealed it during the native black entry frame 6254 and lost it briefly when the tower crossed that point. Requiring the body preserves the transition and death blackout while following the tower vertically.

`build_level4_finale.py` adds one atlas, index53, and four removable mapping blocks. Removing those blocks recovers the exact0.19.1 hires.txt. All 112 earlier art/audio/patch assets remain byte-exact. No ROM, RAM, collision, timing, inputs or audio are modified. The earlier56-byte entrance patch is unchanged.

## Verification

`verify_finale_rules.py` reconstructs all16 complete band images from the shipped atlas, checks native aliases and exhausts every reachable screen-coordinate neighbor probe. Live paired results, actual comparison captures and preview provenance are in `evidence/level4_finale/`. The runtime diagnostic catches the one-past-screen condition that caused the earlier temple-entry crash; it is test-only and is not shipped or required.

The review branch is `feature/golden-temple-boss`, based on frozen 0.19.1. Main remains approved 0.15.0; the last explicit Level 4 approval is0.16.3. No source publication, merge or release has been performed.

## Final paired results

Two paired replays pass 8,578 frames per build, with exact RAM/PPU/OAM/view samples and full PCM/APU. All 16 boss band/color combinations, returning sentinel poses and both ring phases match complete sources; moving-platform matches are restricted to the boss room. The earlier dragon route changes only inside the native ring sprites. All 115 install hashes and flat ZIP/CRC checks pass.

| Route | Frames and native samples/type | Changed images | Unchanged valid images |
| --- | ---: | ---: | ---: |
| Supplied final-halls/boss movie | 7,591 | 6,768 | 822 |
| Earlier dragon flight | 987 | 409 | 577 |

Continuous panorama checks cover AE41: 3,170 frames, AEF5: 2,463 frames, AFA9: 940 frames. Native blank frames and background-disabled death frames are checked separately. The final entry guard retains frame 6254 as black and removes twelve intermittent backdrop-loss frames; all 7,578 other pictures remain exact against the earlier artwork candidate.

The 24.1-second silent preview uses unretouched actual Mesen captures at normal speed, with a two-second final still. The source handoff includes all five cumulative Level 4 feature branches and requires the approved main0.15.0 commit.
