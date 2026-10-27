# Golden Temple stairs and victory transition — 0.20.2

The user's new recording reaches the tower's defeat, Thunder acquisition, the dragon travel sequence and the beginning of Level5. This repair also covers the opposite-facing stairs left coarse by0.20.1. Work remains a review candidate on `feature/golden-temple-boss`; main stays approved0.15.0. No push, merge, tag or release was performed.

## What changed

| Report | Native identity | Repair |
|---|---|---|
| Other stairs still have missing lower pixels | `0B82,83 / 84,85`, with exact0D copies | Register the actual ascending four-cell layout and give it a continuous lower diagonal. Preserve the full upper half and original stone RGB. |
| Thunder pickup is original | `0E8F–92 / FF301116` | Violet/gold tome with a bright lightning rune, registered inside the original32×32 HD footprint. |
| Original boss during defeat | AFA9 hit palette and three fade steps | Reuse complete registered tower bands, platforms, actors and HUD with native brightness timing and cloned neighbor palettes. |
| Original brief impact | `0E60–63 / FF301116` | Reuse the earlier gold impact; all four native CHR patterns are byte-identical to0060–63. |
| Original dragon near the end | AFE5 `0E93–AE / FF303030` | Use the finished dragon's exact alpha/registration as the native white silhouette. |
| Native Thunder announcement | Exact `THUNDER` word in1F bank | Reuse the intermission framing/font and a rendered guard; preserve blank transition timing. |

The ascending stair overrides cover nine existing temple room scopes: A865, AA09, AA81, AAF9, AB71, AC61, ACD9, AE41 and AEF5. The already repaired descending7C–7F family and boss doorway stay exact. Wall/window patterns80/81 and86/87 are not extra stair shapes in the observed layouts and remain decorative. No global scenery clear/restore rules are added.

## Registration and native timing

`build_level4_transition.py` runs after the unchanged0.20.1 finishing layer. It adds atlas55 and `Thunder_Acquired.png`, preserving all114 earlier art/audio/patch assets. Removing its three marked sections recovers the exact0.20.1 mappings. All older validators remain active.

Each ascending step retains its top16 rows and RGB. Its lower limit is `31 - round(12*x/31)`, with a continuous filled body. The actual nametable layout,82/83 above84/85, supersedes the mistaken historical assembly of unrelated cells.

The tower's normal hit artwork continues through native31 pickup flashes and fade palettes0F0F0020,0F0F0F10 and0F0F0F00. All eight native band signatures retain their ordered bounds and27 neighbor checks. Palette substitutions include those checks. Explicit3F0F guards prevent an all-black palette from matching a still-visible faded source. The panorama fades with the tower; native universal-color flashes retain their original background color.

The travel dragon switches to white for the final256 frames, including alternating background flashes. Its exact finished pose alpha, OAM flips, positions and visibility remain native. The build changes no RAM, input, collision, animation timing or audio.

## Verification

Four paired recordings cover20,428 native frames per build and7,916 captured RAM/PPU/OAM/view samples per type. Movie10 is captured every frame; earlier movies6–8 every fourth frame. All native samples, APU writes and full PCM match the0.20.1 baseline. The bounds observer reports no invalid reads.

| Replay | Frames | Samples/type | Coverage |
|---|---:|---:|---|
| Movie6 | 8,668 | 2,168 | Exterior and first two temple halls; ascending steps inAA81 |
| Movie7 | 4,386 | 1,097 | AA81, AAF9, outdoor courtyard and re-entry; both upper/lower ascending flights |
| Movie8 | 3,632 | 909 | Staff hall and dragon arena; every captured image remains exact |
| Movie10 | 3,742 | 3,742 | Boss defeat, Thunder pickup/card, dragon flight and Level5 arrival |

Changed pixels are constrained to ascending stairs, boss impacts/reward/flash/fade, the Thunder card and white dragon cells. Level5 arrival and native full-black frames remain exact. Complete-source matches verify the tome, ascending stairs, tower bands through each fade stage and both white dragon wing poses. See `evidence/level4_transition/` for counts, hashes, source positions and actual captures.

The three stair replays used the retained pre-impact manifest. The only later change is four AFA9-scoped impact rules, with no asset changes. Removing those four rules recovers the exact retained mapping file, and none of the earlier replay rooms can match their boss scope. This equivalence is recorded in `stair-final-scope-equivalence.json`; the final boss recording uses the exact delivered manifest.

Run `python build.py`, `python scripts/verify_release.py`, and the paired/source verifiers in `scripts/verify_level4_transition.py` and `scripts/verify_transition_sources.py`. Source and input provenance are in `art/level4_transition/` and `test_states/README.md`. No ROM, emulator, movie or state bytes are distributed.

Coverage is limited to the supplied recordings and nine established temple mappings. The new movie acquires Thunder but does not cast it. Later Level5 gameplay is outside this repair. Earlier documents retain their historical testing limits; this movie now supplies the missing tower-victory and travel coverage.
