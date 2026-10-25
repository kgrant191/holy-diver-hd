# Randy during Breaker pickup — approved 0.10.2

The user reported original Randy briefly appearing after collecting Breaker.
Actual Mesen frames reproduce the fallback during the final 24-frame fade,
immediately before the spell announcement. The native palettes change for
eight frames each; the boss bank had aliases for the full-color player only.

`build_breaker_randy.py` reuses all 314 existing normal/Twin Fire/upward pose
rules in their original order. Each receives three room-scoped fade aliases,
including the same standing-leg and crouch pose conditions. Nearby-sprite
probes use the corresponding fade palette. No sprite is repainted and native
mirroring remains unchanged. Mesen's tile brightness parameter dims the exact
existing atlas cells at .65, .30 and .12; the native game controls timing.

| Costume | First fade | Second fade | Third fade |
| --- | --- | --- | --- |
| Normal | FF200F26 | FF100F16 | FF000F06 |
| Twin Fire | FF120126 | FF020F16 | FF0F0F06 |

Only `hires.txt` and the installed README change. All 91 other installed files
match approved 0.10.1, including every image, audio patch and prior boss fix.
Static validation removes the new block to recover the exact 0.10.1 mapping.
The 93-file ZIP passes every expected hash, CRC and flat-layout check.

## Actual replay verification

Use MesenCE 2.2.1 and the unchanged ROM/states recorded in `test_states/README.md`.
The supplied defeat state reproduces the Twin Fire fade. The earlier boss
state produces normal-costume victories and combat/pose regression. All inputs
are controller-only; no RAM edits are used.

Run `run_screen2_5_qa.py` with the following route files, once against the
0.10.1 pack and once against the built 0.10.2 pack:

- `breaker_randy_routes.json`: defeat state, stride 1, 1,600 frames.
- `breaker_randy_left_routes.json`: earlier boss state, stride 1, 1,600 frames.
  This attempted alternate approach collects earlier but does not turn Randy
  during the automatic pickup. Its internal case name is `left_pickup`.
- `breaker_randy_regression_routes.json`: earlier boss state, stride 2;
  1,600-frame victory and 900-frame combat/pose routes. The retained 0.10.1
  victory is longer; compare its matching first 1,600 frames and PCM prefix.

Output paths expected by `verify_breaker_randy.py` are `work/breaker_randy/`
`before`, `after`, `left_before`, `left_after` and `regression_after`.
The original victory/pose baselines remain in `work/boss2_review/regression_after`.
The extra exploratory input attempts in the local `before` directory are not
part of the reported verification. They leave the same automatic pickup pose.

Results: 5,700 paired frames, 4,450 identical samples per native RAM/PPU/OAM/view
type, identical APU writes and 18,213,212 matching PCM bytes across the compared
intervals. Equal-duration routes have equal PCM lengths; the retained longer
victory has an expected additional 1,200-frame audio suffix.

All 60 changed sampled pictures are confined to Randy's native tile coverage:
24 from each every-frame pickup and 12 from the stride-two victory. Each fade
phase is verified against the existing HD sprite source. Across 61,512 visible
opaque pixels, RGB matches within one level of Mesen's quantized brightness.
Orbiting native effects are excluded by neighboring OAM coverage; the most
occluded frames still require visible source matches. There are no skipped
changed frames. The remaining 4,388 valid images are identical, plus two
matching empty initial captures. Boss disappearance, cave flashes, announcement
and the new-save Stage 3 arrival remain exact.

Combat/pose regression verifies both horizontal directions and both costume
palettes with all 450 pictures unchanged. Pickup fades were observed only in
the native right-facing pose; mirrored fade playback is not claimed.

Run `python build.py`, `python scripts/verify_release.py`, and
`python scripts/verify_breaker_randy.py`. Compact results are under
`evidence/breaker_randy/`. The delivered comparison uses actual before/after
Mesen captures with explicitly labeled nearest-neighbor detail enlargement.

Mesen format reference: https://www.mesen.ca/docs/hdpacks/
The user approved the delivered 0.10.2 pack and authorized merging PR #12 on
2026-10-24. Main now contains the repair. Approval records and PR/main artifact
checks are under `evidence/breaker_randy/`. All 93 reviewed installation files
remain exact; the installed README retains its historical review label.
