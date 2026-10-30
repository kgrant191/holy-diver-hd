# Level 6 enemy revision — 0.29.1 review

The user requested a boogery green blob instead of the rocky orb, a more visible wall face, and preservation of the old green enemy for an exact revert. This revises the 0.29.0 candidate; accepted continuation remains 0.28.0 and main remains 0.24.0. Work stays local on feature/level6-opening.

The blob uses two complete 32×32 HD mucus poses with rounded folds, wet highlights and bubbles. The face retains its shape, amber eye and native alpha contours, with bone-gray plates and pale ridges to distinguish it from the crimson walls. Source prompts are in art/generated/level6_enemy_revision_prompts.json.

## Scope and restoration

Only A3AF/mode10 is affected. Atlas 68 holds nineteen unique face cells and eight green-enemy cells. The 171 face rules retain the original normal/resume/30/31 palette combinations. The eight blob rules use FF0A1930. Two marked override blocks precede the original mappings; removing them recovers exact 0.29.0 hires.txt. All 149 earlier art/audio/patch assets remain byte-identical.

The original generated orb, both registered poses, original atlas and eight mappings remain intact. Their hashes and source commit are recorded in art/level6_enemy_revision/standby.json. Set `green_enemy` to `rock` in art/level6_enemy_revision/choice.json and run `python3 build.py` to restore the original green enemy while retaining the face recolor. The shipped manifest describes the blob candidate; an intentional rock build needs its own reviewed manifest before release verification. Do not overwrite the blob manifest merely to make the alternate build pass.

Face masks are byte-identical to 0.29.0. Blob art fits the same native four-cell union. No terrain, movement, collisions, timings, audio, inventory or other artwork changes. The original 0.29.0 source commit is e18e1db60c1c5c48ec428c67fd8bd2d868340d35.

## Verification

The focused rule verifier checks exact baseline recovery, all previous assets, canonical repeated face cells, unchanged face alpha, complete pose registration, override priority and independent orb restoration. The historical validator chain runs through the exact 0.29.0 projection.

The supplied 4,761-frame movie is paired against the frozen 0.29.0 capture at stride one. The replay verifier compares every RAM/PPU/OAM/view sample, APU and full PCM, then requires every changed image pixel to lie inside the nineteen face cells or eight green-enemy OAM cells. Current and previous native samples account for the documented one-frame video-submission delay; no arbitrary motion margin is allowed. Whole registered face and both blob poses must match actual rendered pixels. Menus and blackouts must remain exact.

This change does not alter platform geometry or earlier-room rules. The earlier-room regression and controller-only platform-edge evidence from 0.29.0 remain applicable through exact old-asset/rule recovery and unchanged face masks. No new live Thunder or dragon cast occurs in this recording; those face palette families have static coverage only. Later Level 6 rooms and the final boss remain unfinished.

The full replay passed: 4,761 exact native samples per type and exact complete audio. All 3,012 changed screenshots are confined to the two enemies; 1,748 other nonempty screenshots, 955 menus and 115 blackouts remain exact. Whole blob poses match at frames 212 and 218; the complete face matches at frame 586. See evidence/level6_enemy_revision/ for replay, static, clean-build and archive results. No push, PR, merge, tag or release is performed.

Isolated clean build: all 152 files reproduce exactly, historical validators and release verification pass. The 4,760-frame preview decodes completely; install ZIP hashes and CRCs pass.
