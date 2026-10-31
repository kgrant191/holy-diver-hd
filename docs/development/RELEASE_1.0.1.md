# Version 1.0.1 — Poison Moss lava-curtain repair

The user supplied Holy_Diver_HD(20261031-143722).mmo and explicitly requested a fix and release 1.0.1 on 2026-10-31. Scope is room 9DEE, mode 14, from released main 53ab5788efb6b078227ac8e9915d78316983278a.

## Repair

The recorded later section still rendered native lava-curtain tiles and moss details. The Blizzard regression additionally exposed the original frozen horizontal lava pool.

- Six curtain CHR identities are byte-identical to finished Level 2 falls. Copy every original frameRange phase, hot palette and frozen source without changing order or source coordinates.
- Six horizontal frozen-pool identities reuse existing exact Level 2 ice sources.
- Four moss ceiling details and three platform contours reuse finished Level 3 material and masks.
- One newly observed upper-left contour uses the same native hull algorithm and approved moss unit as its three neighbors. The new atlas is one 16x16 cell.

The repair adds 212 room-scoped mappings. It introduces no neighbor probes, background substitutions, gameplay patches or native timing changes. All original rule text is exactly recovered by removing the two marked repair blocks. All 172 old non-text installation files stay exact. hires.txt and the versioned README change; one atlas brings the total to 175.

## Verification

Pair the 601-frame supplied movie at stride one and the 2856-frame earlier corridor recording at stride two. Compare every captured native RAM/PPU/OAM/view sample and complete APU/PCM audio. Require every changed image pixel to lie within repaired native cells. The earlier route covers both hot palettes, Blizzard, pauses, damage/death and transitions. It provides 572 frozen-palette samples and 130 exact blackouts.

Whole 32x32 fall-source matching covers all 16 original animation phases, both hot palettes and the frozen form. Keep all historical validators through an exact 1.0.0 projection, run a clean build, and download the actual CI artifact to verify all 175 names/hashes and ZIP layout.

The host filesystem leaves dot-prefixed copy sidecars in replay working directories. They are not referenced pack assets and are not shipped. Every declared runtime file remains hash-pinned. The first full-stride capture has the usual empty initial screenshot; all native state samples are retained. The replay comparison records these details explicitly.

The replay harness explicitly stops WAV recording before releasing the native core, so PCM data and RIFF lengths are fully flushed before comparison. This affects capture finalization only.

Evidence is in evidence/moss_curtain_fix. No ROM, input movie, savestate, emulator binary or raw frame dump is committed.

## Publication

The user authorized this release as part of the repair request. The release job runs only after a validated push to main with VERSION 1.0.1. It downloads the same build artifact, rechecks every expected file and packages a flat install ZIP. GitHub CLI creates v1.0.1 at that exact commit and attaches the ZIP and RELEASE_NOTES.md. Existing releases are left untouched; PRs and other versions cannot publish. Per-job permissions grant only the release job contents:write and actions:read. The normal build stays read-only.

PR/main checks and the final published-asset verification are maintained in the PR description.
