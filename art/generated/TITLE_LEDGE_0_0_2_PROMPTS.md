# Title and entrance repair sources (0.0.2 candidate)

Generated with the built-in image-generation tool, then registered into the existing project assets. Only the measured repair footprints are composited into the pack. No other generated scene changes are accepted.

## Title background

Input edit target: art/Title_HD.png from approved 0.0.1 (also retained in rollback/approved_v14_1/Title_HD.png).
Output: art/generated/title_clean_0_0_2_generated.png.

Prompt: Remove the entire PRESS START plaque at the bottom: text, gold horizontal border lines, flourishes, dark rectangular panel and every trace of its rectangular outline. Seamlessly reconstruct the orange-gold rocks and deep blue mist/castle background. No straight horizontal seam, rectangular patch edge, box or ghost lettering. Preserve the Holy Diver HD logo, character, flame, moon, distant castles, outer rocks and 1989 IREM footer. Repair the former plaque around x120–390, y400–450 on the 512×480 canvas, matching the detailed pixel-art palette, texture and lighting. Output a full opaque image at the same aspect ratio.

Registration preserves the approved character, logo and footer exactly. The generated footer was not retained. The ready state reuses only the original gold PRESS START letters with a letter-shaped shadow; its background is identical to the intro state.

## Rock shelves

Input edit target: approved art/EntranceScene_registered.png (retained as rollback/approved_v14_1/EntranceScene.png).
Output: art/generated/ledge_extensions_0_0_2_generated.png.

Prompt: Extend only the two horizontal gold-lit rock ledges from the left wall. The upper shelf at y192 extends from x128 to x160, and the lower shelf at y544 from x160 to x192, using the supplied 512×960 scene coordinates. Keep their tops level at the original heights. Use solid orange-gold shelf caps, craggy undersides and deep purple crevices that join the existing wall. Preserve the cliff away from these ledges, all five tree branches, moon, distant castle background, columns and floor. No character, text or annotations.

The generated edges were registered into the exact target rectangles documented in art/title_ledge_registration.json. art/layers/11_ledge_extensions.png is a separate editable layer. The ORA source and installed scene are rebuilt together. Controller-only probes checked stationary edge positions before acceptance testing; native collision data is not changed.
