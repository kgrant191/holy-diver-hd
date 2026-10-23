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
