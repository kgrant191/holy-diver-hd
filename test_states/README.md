# Local emulator test inputs

Restore these files from the previously delivered `Holy_Diver_v15_Sources_and_Rollback.zip` archive, under `Holy_Diver_v15_1_Source/test_states/`, into this directory. They are intentionally ignored by Git. A build does not require them.

| Relative path | SHA-256 |
| --- | --- |
| `Holy_Diver_Before_Death.mss` | `0098ca0063619b809a2daa0da79d0325ec66c316f0a5a661780485261e2d040e` |
| `Holy_Diver_Bracelet_Owned_Before_Pause.mss` | `82f134f6bc2a959f5829d0b21846adeaf09ffe4e21909dce3f86041806e0a2f3` |
| `Holy_Diver_HD_1_original.mss` | `86955b78e1730bb4483e6b35662c4b76a91544103a065e1556a2777141a6420a` |
| `Holy_Diver_HD_v10_Entrance.mss` | `90b87f4db27c0fac69c632bf9737f74ae8f305cd87a0beca8f4fb7fab3a9c6db` |
| `room2/Holy_Diver_HD_1(1).mss` | `42f86d11f4026f808e4ee4739c05bba878c63c6ccd61e53bf3b42ddc043f7f1c` |
| `room2/Holy_Diver_HD_2.mss` | `6d53c75313f68f4db097f12d153692568c2d461590ed724aa421fe582431c22c` |
| `room2/Holy_Diver_HD_3.mss` | `28abaae9aac96966dd20f9fbecd5ae7d47e2356afd09c1ca874f12de32005956` |
| `room2/Holy_Diver_HD_4.mss` | `b5936b0b0fc3e818b48b503df49945b8f888ad9b8aaccabb35ef8e5c0867dc77` |

## User-supplied ledge boundary states (2026-10-22)

Pass these locally with --upper-state/--lower-state to run_ledge_boundary_qa.py. State bytes remain excluded from Git.

| Input | SHA-256 |
| --- | --- |
| Holy_Diver_HD_1(2).mss — upper ledge | d08a41d3da8a51b72116fe18bf46822ce986eca5ddf68283fd73b20f2d47a3cd |
| Holy_Diver_HD_2(1).mss — lower ledge | c73a4837f13507e0e054d667bd4d514e4eccd9d132bc9db2cfc0efd11067f9b4 |

## Third chapel section states (2026-10-23)

Pass these with --state1, --state2 and --state3 to run_screen1_3_qa.py. These user-supplied binary inputs remain excluded from Git.

| Input | SHA-256 |
| --- | --- |
| Holy_Diver_HD_1(3).mss | afa81bdb7c0ae02ac846a9496a7284f9d669db2a2ac245e9cd13f4c82030a8c6 |
| Holy_Diver_HD_2(2).mss | 7a2e71c31782dfff36a4d45d82261d7cba8a9f23727b2bd57fada0d46f987a0a |
| Holy_Diver_HD_3(1).mss | b039731f89af147aa94b6e73cff78dd4da59468d21a5b1b06fbaf37dd27d7881 |

## Fourth section state (2026-10-23)

Pass `Holy_Diver_HD_1(4).mss` with `--state` to `run_screen1_4_qa.py`. SHA-256: `de4fedc63dc4a411a1ae944329e33e8d954acefccc7265760b77f32199c61899`. The supplied bytes remain ignored by Git.

## First boss states (2026-10-23)

Pass these with `--state1`, `--state2`, `--state3` to `run_boss1_qa.py`. State 2 is paused; the recorded route resumes it with Start. State 3 begins the native defeat sequence. Input bytes remain ignored.

| Input | SHA-256 |
| --- | --- |
| Holy_Diver_HD_1(5).mss | 52dd9e7cd675fda2a2cf243ff798b997a1dd9b2ec49e7c8f6079808d4e61bc19 |
| Holy_Diver_HD_2(3).mss | 4457b7dd6df58b8b2fb4d1c0478082a123ddfe724984b6ea46bfff0ced7a02f3 |
| Holy_Diver_HD_3(2).mss | f7470adbc882bac7158a8b54332c5d887e4605e07b1f001d774f9359da042b3c |

## Large recovery item states (2026-10-23)

Use `recovery_item_routes.json` with `run_boss1_qa.py`. Pass the red HP file as `--state1` and the blue Magic file as `--state2`; these routes do not use state3. State bytes remain ignored by Git.

| Input | SHA-256 |
| --- | --- |
| Holy_Diver_HD_2(4).mss — red HP flask, health 5 | 107b73207b47bfdcad7da2f503065d9899206c9549c434fb51e8b1585abfe54a |
| Holy_Diver_HD_3(3).mss — blue Magic flask, 10 magic | ad96f70a06f1f0412dcfea1c614b680dcf8f0c652e0f21acedbce71365debea1 |

## Stage 2 screen 1 (2026-10-23)

Inputs stay outside Git. Pass these unchanged files to `run_screen2_1_qa.py`:

| Input | SHA-256 |
| --- | --- |
| `Holy_Diver_HD_1(6).mss` | `5797d18ed527d8efd6d094745cd382db1e1364ac334d9f664ce56077e6e310db` |
| `Holy_Diver_HD_2(5).mss` | `47f9ef2f67b417befb6a31c4eee2c10954e7bab079e2f199a254167860e7d309` |
| `Holy_Diver_HD_3(4).mss` | `df845d77d9bdb85b548c164524513d62972b8d2049f6ceea625177f8e3823464` |
| `Holy_Diver_HD_4(1).mss` | `20f6de78ece0c59af7a153fce9267b4248b3459491592d52f03db3fb43b412f0` |

## Stage 2 cave-entry review (0.4.1)

- `Holy_Diver_HD_1(7).mss` — SHA-256 `383f3249ecabae9238d6ec2cdbd8d52ef0e57b8fb8634bec0e7203527fb12c10`. User supplied just before the exit cliff. Walk right after frame 20 for 420 frames; covers partial doorway reveal, full approach, native transition and next-room arrival. Bytes remain local and excluded from Git.

## Stage 2 screen 2 cave (0.5.0 candidate)

`Holy_Diver_HD_1(8).mss` — SHA-256 `bffc454e176bee738d053802aa12a3558dba58a17400e1033148f7c0291d4db7`. Pass unchanged to `run_screen2_2_qa.py --state`. The 9,052-byte user input remains outside Git. The approach regression uses the retained `Holy_Diver_HD_1(7).mss` above. Routes and exact scope are in `docs/SCREEN2_2.md`.

## Stage 2 screen 3 vertical cave (0.6.0 candidate)

`Holy_Diver_HD_1(9).mss` — SHA-256 `a84d2f19c107be53b9d76e78f8095ae9cf7861badbf8052555e0879dd5749df3`. The 9,067-byte user input is unchanged and excluded from Git. Use `scripts/screen2_3_routes.json` with the existing `run_screen2_2_qa.py --state` replay runner. See `docs/SCREEN2_3.md`.

## Stage 2 screen 4 horizontal cave (0.7.0 candidate)

`Holy_Diver_HD_1(10).mss` — SHA-256 `ce8fd0ed2f9316c7edd64eef51a532e38325185c394a224371fcd7a944d7f47a`. The 10,439-byte supplied file is unchanged and excluded from Git. Use `scripts/screen2_4_routes.json` with `run_screen2_2_qa.py --state`. The separate approach route uses the retained screen 3 state above. See `docs/SCREEN2_4.md`.

## Screen 2-4 stairs / 2-5 approach (2026-10-24)

`Holy_Diver_HD_1(20261024-155045).mss` — SHA-256 `8a67bbf57e6d756e36f4f6f42934d27b40c6266d95f6fc24118244c89e53ee40`, 9,383 bytes. Unchanged, excluded from Git. Starts at the upper stair flight in screen 2-4; jump left/up to enter 2-5.

## Screen 2-6 (2026-10-24)

`Holy_Diver_HD_1(20261024-223733).mss` — SHA-256 `60945ccab9020ab3fdde2247161a5f119c5ac32d4ec5af3e6385f0aa187df0b2`, 9,650 bytes. The unchanged user save starts the next cave (room 10, data pointer 8E8D). Use `run_screen2_5_qa.py` with `scripts/screen2_6_routes.json`; bytes remain local and excluded from Git. Previous-room regression uses the stair/2-5 approach save above.

## Level 2 boss (2026-10-24)

`Holy_Diver_HD_1(20261024-231216).mss` — SHA-256 `3dc10e1f35dda26171678ca6548fc3f974635b6e9face870525398c1a658f7e6`, 4,690 bytes. Unchanged, excluded from Git. Starts during entry into boss room 08/data pointer 8F7D. The controller routes in `scripts/boss2_routes.json` cover combat, victory, Breaker collection, announcement and Stage 3 arrival. Run with `run_screen2_5_qa.py`; the prior 2-6 save supplies the regression routes.

## Boss defeat/pickup repair — 0.10.1

`Holy_Diver_HD_2(6).mss` (12,013 bytes), SHA-256 `6cfdc375c9620d42e989e96ce4e855babe06f3d54fd49aa28d0de9bf7a408345`. Supplied on 2026-10-24; begins during the gold boss-defeat phase and automatically collects Breaker after the fade. Use `scripts/boss2_review_routes.json`. Bytes are excluded from Git. The earlier boss save remains the regression input.

## Level 3 movie input

`Holy_Diver_HD.mmo`: SHA-256 `c6c3f99a7204f5052c1758ef44ffb4387d2ebc5a8534127a0ddde60ccfde74cd`, 6,883 controller frames. Embedded SaveState SHA-256 `956c402469389e969b3443c8c5c5019458e5f1d65e8830f63f815b928a23f5f0`. MesenCE 2.2.1 / movie format 3; supported translated ROM SHA-1 matches the project. Ends paused in the later Level 3 corridor, before the boss. Keep the input outside Git; see `docs/LEVEL3_OPENING.md`.

## Level 3 lava corridor movie

`Holy_Diver_HD(2).mmo` (3,705 frames) embeds the boot-owned starting state. SHA-256: `b13e4d21d182ea84f5e9614d839db71c765f26d4874b4a6cbea5b91e8332699d`; state: `2306869106294ce3111a22fc02f298dcd3f60593e0adec6839afbc1a90426671`. Movie and derivative bytes stay outside Git. See `docs/LEVEL3_LAVA.md` and `art/level3_lava/routes.json` for controller-only Breaker, Blizzard and platform-edge probes.

## Large-fish motion movie (2026-10-25)

`Holy_Diver_HD(3).mmo`: 1,200 input frames, Mesen 2.2.1, SHA-256 `ace46ac61dabd9485e19cbd1599ad8518192d60b9894ef714c8204678ec14a18`. Embedded state SHA-256 `3539a1929e1ca0996449ec064f78c2e3ced076cee3f6232af8302a7bc4f7dadf`. Same supported translated ROM. Input bytes remain outside Git. Shows large-fish hovering in both directions, dive/turn and damage.

## Level 3 next caves recording — 0.13.0 review

Local input `Holy_Diver_HD(4).mmo`: 7,592 frames; movie SHA-256 `facbd98578ae0261fc5707b83cf11ffea8d00966b1af08b9dd555fd6c678f6db`. Embedded state SHA-256 `8f7b46bf47a489e4105a0023e4b2f37fa7d8507a3b52d799ac56be8fdf891c6d`; input SHA-256 `ccd0149db32fdbdca718b69dc947a8100d504fba16d9547b8990fc9b8ea5b4f9`. Standard MesenCE 2.2.1 and the existing supported ROM. Bytes remain outside Git. See docs/LEVEL3_CAVES.md.

## Level 3 finale movie — 0.15.0 review

`Holy_Diver_HD(5).mmo`: 4,812 frames; SHA-256 `32f2d9617ca290845983ab67918a8f0f9ed312ee7cd5a4ec5881ff51d299db42`. Embedded state SHA-256 `56b9f1bbf104d4d4671801e1eb8f30223d6620971c58c60b5a51a440950fd4d2`. Same supported translated ROM and stock MesenCE 2.2.1. Covers final climb, boss, Overdrive and Stage 4 arrival. `make_level3_finale_edge.py` derives the 1,740-frame input-only edge route; hashes are in evidence/level3_finale/edge_input.json. Movie, embedded state and ROM remain outside Git.


## Golden Temple recording — 2026-10-26

Holy_Diver_HD(6).mmo: 8,668 frames, SHA-256 `f413a215567b622fad4cea7dfce4561a05ede2c840a1f026e7e2a8ad6c30adca`. The locally attached movie embeds its starting state. Derive input-only spell/edge routes with scripts/make_level4_routes.py; their hashes and retained-state digest are in evidence/level4/routes.json. Movie/state bytes remain outside Git.

## Golden Temple missing stairs — 2026-10-26

`Holy_Diver_HD_1(20261026-181741).mss`: 9,478 bytes, SHA-256 `1e572fa95b436b4276051354d5fc19b409194fd5b57aabbcd05ec12b0c03ed4b`. Starts at the lower landing of the descending AA09 stair flight. Keep unchanged and outside Git. `make_level4_stair_routes.py` uses this exact state with the existing movie settings for controller-only inspection, walk and jump/return routes. See docs/LEVEL4_STAIRS.md.
