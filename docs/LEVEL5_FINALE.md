# Demonic Palace finale — 0.24.0 review

The user's 20261028-142617 movie shows the still-native moving platforms, remainder of the skull shaft, boss, victory ascent and Level 6 entrance. The candidate continues 0.23.0 on feature/palace-finale; approved main remains 0.22.2.

## Scope and registration

- 8D3E/mode04: retain the accepted palace panorama; add the missing 12F7–12FA lift rules in this room and 116A–116D/136A–136D masonry. The full repeating lift is the existing 64×32 HD span. Native OAM movement, flips, collisions and repeated cells remain unchanged.
- 8E6A/mode08: reuse approved stone and a darker palace interior. Register six whole boss components (two skull, claw and fist phases) to their native unions, then slice into cells. Shared animation identities remain byte-identical. Add the horned altar and cruciform effigy, and retain independent component motion and timing.
- 8EE2/mode04: cover the victory ascent, moving effigy, white silhouette and fades. Distant blue native skull tiles reveal the palace background. Background disable and full blackouts remain native.
- 9A8B/mode04: cover only the recorded Level 6 threshold, using the approved crimson cave source and native terrain masks. Restore HD Randy, HUD and red Breaker charge. Later Level 6 rooms/enemies are not part of this review.

The 1400 and 1600 player/effect banks are byte-proven aliases of accepted 0A00 identities. Conditional pose priority and native-neighbor dependencies are cloned before broad fallbacks. New background guards are rendered tile-at-position checks, not new neighbor probes. Both 30/31 flash variants are mapped in the boss room; the supplied route determines live coverage.

## Preservation and reproduction

`build_palace_finale.py` adds marked, removable blocks and two new atlas/background files. `verify_palace_finale_rules.py` checks exact 0.23.0 recovery, all 125 prior art/audio/patch hashes, whole sources, shared cells, terrain masks, references and full historical validation through a byte-exact baseline projection. Generated source provenance is retained alongside the PNGs.

The movie is 15,585 input frames, SHA-256 0328029ecdc68941515093d8f03efafdf0cd0a2c4bffa937cf42d2151610c77a. It embeds its initial state and uses the existing supported ROM. ROM, movie, emulator, state and raw captures stay outside Git. Testing uses the stock MesenCE 2.2.1 native core with synchronized screenshot observer and native WAV capture. No RAM or game patches are used to fabricate routes.

`verify_palace_finale_replay.py` compares all paired RAM/PPU/OAM/view samples, full APU writes and PCM; it checks unchanged native blackouts/menus and searches actual captures for complete registered boss, ornament and lift sources. The preview is assembled only from actual final Mesen frames and original audio.

Approval and merge remain pending. The source handoff includes both unmerged 0.23.0 and 0.24.0 work from approved main.

## Verified full-movie result

The full pre-card-repair candidate completes the 15,585-frame movie with 7,792 paired samples per RAM/PPU/OAM/view type. Every sample, all APU writes and the complete 96 kHz PCM are exact against the 0.23.0 baseline. All 43 native blackouts and 539 stable preceding-room/menu/lives pictures remain exact. The changed pictures cover the requested scopes and bank aliases. The later one-frame card repair is verified separately against this exact candidate; its retained manifest is `pre_card_pack_sha256.json`.

The actual captures contain exact complete matches for the moving lift, both skull poses, both claw poses, both fist poses, altar, static effigy and moving effigy. The background audit reports no missing normal scenery, and all 36 sampled rendered boss-flash pictures contain HD panorama pixels, including native grayscale/emphasis variants. Screenshot appearance determines the flash phase because palette writes can precede video submission.

The rebuilt 129-file pack matches its candidate manifest exactly; all 125 prior art/audio/patch files remain unchanged. Gameplay and collision follow the unmodified native execution. The newly covered lift uses the exact previous source footprint; this route includes riding and jumping from it, but no new isolated slow walk-off experiment is claimed.

## Final Stage 6 card submission

Consecutive inspection found one visible native card at frame 15374: the RAM render latch had already cleared while the previous card was still being submitted. The final delta clones 61 existing stage-card mappings/backgrounds, reusing their exact images, and substitutes a rendered S-tile guard scoped to Stage 6 for the RAM latch. It remains inactive when rendering is actually disabled. The existing card artwork, lives count and timing are preserved.

The final complete movie replay captures frames 15120–15585 consecutively. `verify_palace_finale_card.py` requires exact complete audio and every available paired ending-state sample, removes exactly the final 62-line delta to recover the tested candidate, and confines the changed picture to frame 15374, which must equal the existing complete HD Stage 6 card. The preview uses unchanged earlier consecutive gameplay plus the final ending capture.

Final checks pass: 2550 consecutive selected frames, 1282 exact shared native/picture samples, and 1280 boss-backdrop checks including 48 flash frames. The final ending comparison passes 365 paired native/picture samples and changes only frame15374. Complete audio remains identical. All historical validators and the final 129-file manifest pass. The ZIP has a flat install layout, valid CRCs and exact member hashes.

## Approval — 2026-10-28

The user approved 0.24.0 and the preceding continuation, and authorized merging. Some platform and main-walkway graphics may be revisited later; current artwork is accepted. Next development is Level 6. Source push is pending; no further merge approval is required. All 129 reviewed installation bytes remain unchanged, including the installed README.

## Adoption

Merged through PR #27 on 2026-10-28. PR and main builds pass, and both downloaded artifacts match all 129 approved files. See LEVEL5_FINALE_ADOPTION.md and evidence/level5_finale_adoption/.
