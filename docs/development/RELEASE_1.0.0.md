# Version 1.0.0 — approved and merged

The user requested v1.0.0 and a public-facing documentation cleanup on 2026-10-30.

Base: `29243afd7f861c7697b2d3bf58e541ba4eea0fd0`, approved 0.32.0 through PR #30.

## Scope

- VERSION changes to 1.0.0.
- Root README and changelog become concise player-facing pages.
- Windows/macOS setup and ROM verification live in docs/INSTALLATION.md.
- INSTALL.txt becomes the bundled public README.txt.
- Historical root README, changelog, status and agent instructions are retained verbatim under docs/development.
- Root STATUS and AGENTS point to current development information and preservation rules.

The tested emulator is MesenCE 2.2.1; no separate Mesen2 test is claimed.
ROM SHA-1 is FE2FCD0AD334D792DB16535D09F3AB9FB2BEA3AC, confirmed in existing replay evidence.
Preferences > Files exposes the active data-storage location in the MesenCE 2.2.1 UI source. The guide uses it instead of assuming a platform-specific default path.
The emulator's NES General settings contain its HD-pack enable option.

## Runtime preservation and verification

There are 174 install files. Only README.txt changes from 0.32.0; all 173 other installation hashes, including hires.txt, remain identical.
The expected README.txt SHA-256 is `f81db7b3edbc9b7b05074b9e9d6ec13e20c549395254d73ed49df6490ff28004`.
Historical manifests remain intact. The new 1.0.0 and expected-build manifests pin these exact installation bytes.

Run the clean Actions build, complete historical validator chain and verify_release.py. Download its actual artifact; check all 174 member hashes, CRC, flat layout and the exact 173-file preservation comparison.
Existing live replay evidence remains applicable to the unchanged game assets and mappings. This preparation does not claim a new full gameplay replay.

Approved by the user on 2026-10-30: “approved, merge it”. PR #31 is merged.
The reviewed head is `90b8ffd865db52528fcd57f183b99a3e57199355`; its merge is `0baaf439c99f6ba72bfb9d358ed316f2ba9170c8`.
Both have the exact same tree, `5ade37a436827bb060170bbd42eb302167233687`.
The PR build and downloaded artifact pass all 174 hashes, CRC and flat layout.
Post-merge build and artifact verification records are maintained in [PR #31](https://github.com/kgrant191/holy-diver-hd/pull/31).

The existing install ZIP remains approved with SHA-256
`fff9e65c5a5fadac7178b91977c0a0c6227f1e115a03466a3eb9049bf0f6f49d`.
No tag or GitHub Release has been created.
