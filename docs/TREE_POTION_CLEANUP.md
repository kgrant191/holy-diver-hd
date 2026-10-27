# Chapel branch joins and health-jug visibility — 0.20.3

The user approved the delivered0.20.2 pack on2026-10-27, then requested better tree-branch attachment in the new movie and a more visible red potion in the screenshot. All118 approved installation files are frozen at that baseline. This cleanup is a review candidate on `feature/tree-potion-cleanup`; main remains approved0.15.0. No publication or merge is authorized.

## Branch repair

The1079-frame movie stays in the chapel tree court, room84C2/mode04. Native left branches are0122/0123/014D/014E and right branches015B–015E. Their narrow original strips were placed against a repeating trunk sampled from a different vertical section of the original tree. The trunk's irregular transparent edge left the branch ends visibly detached.

The repair reuses the same `art/layers/20_tree_and_branches.png`. It registers the original branch shoulders into the two nearest trunk columns, across the branch row and one row above/below. Contextual native branch anchors select each complete attachment; ordered X/Y bounds precede every neighbor probe. The source's natural shoulder blends into the unchanged repeating bark. All branch strips, landing surfaces, lengths, crown, roots and surrounding scenery remain exact.

There are48 context-specific trunk rules, scoped to84C2 and0F071737. The actual movie verifies both directions repeatedly, including scrolling and character overlap. Source checks find97 complete left joins and102 complete right joins in sampled real captures. These compare all opaque source pixels; the inherited trunk's seven partially transparent top-edge pixels retain normal background blending and are not mistaken for opaque RGB.

## Potion repair

The screenshot shows the four-tile handled health jug, previously red enamel with dark bronze fittings. The updated source keeps its red health identity and right-hand handle, with brighter pale-gold fittings, ivory edge reflections and stronger glass highlights. The built-in image-generation edit used the accepted jug as its reference; prompt and provenance are retained in `art/tree_potion_cleanup/provenance.json`.

The full jug remains within the same30×30 painted area of a32×32 HD footprint. Twenty mappings replace its five established byte-identical native groups:0276–79,068E–91,0A8E–91,0C8E–91 and129A–9D, all inFF301116. Other health/magic bottles and small pickups are unchanged.

**Coverage limit:** neither the supplied tree movie nor the recovered earlier cave route shows this jug. Its native aliases, footprint, alpha and increased highlights are checked statically; the preview's potion section is explicitly labeled an artwork comparison, not a gameplay capture. The user's screenshot supplies the red-cave visibility reference. No item was fabricated by changing emulated RAM.

## Verification and handoff

`build_tree_potion_cleanup.py` adds one atlas at index56 and three removable sections. Removing them recovers exact0.20.2 hires.txt. All116 prior art/audio/patch files remain byte-identical, and all older validators stay active. The new validator checks2,748,416 bounded neighbor positions with zero unsafe reads, unchanged branch identities, continuous alpha contact at both joins and the jug's native footprint/aliases.

Two paired replays cover2879 frames and2879 RAM/PPU/OAM/view samples per type. Native state, APU writes and full PCM match exactly. In the tree movie, changed pixels stay within the adjacent trunk attachment cells. All1799 nonempty cave-regression images remain exact. The cave route enters8D9D from the unchanged8CAD user state using only controller input; it is a regression check, not jug-collection evidence.

Build with `python build.py`, then `python scripts/verify_release.py`. Live checks use `verify_tree_potion_cleanup.py`; complete join checks use `verify_cleanup_sources.py`. See `evidence/tree_potion_cleanup/`, the frozen0.20.3 manifest and `test_states/README.md`. The install ZIP is flat. The source handoff includes all five cumulative Level4 branches plus the cleanup branch against main2f38abeb. ROM, states, movies and emulator binaries are excluded.
