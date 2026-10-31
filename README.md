# Holy Diver HD

**Version 1.0.1** — an HD graphics pack for Holy Diver on the NES, with updated characters, enemies, scenery, items and effects throughout all six stages.

## Download

Get **Holy_Diver_HD_v1.0.1.zip** from [Releases](https://github.com/kgrant191/holy-diver-hd/releases). This is the installable HD pack. GitHub's automatic source-code archives are for the project source.

## Requirements

- **Mesen with NES HD pack support. Tested with MesenCE 2.2.1.** [Download MesenCE](https://github.com/nesdev-org/MesenCE/releases/tag/2.2.1).
- **The supported Holy Diver translated ROM** (`.nes`), with SHA-1:
  `FE2FCD0AD334D792DB16535D09F3AB9FB2BEA3AC`

The ROM and emulator are supplied separately.

## Install

Extract the pack into a folder inside MesenCE's `HdPacks` directory. **That folder must match your ROM filename exactly, without the .nes extension.**

| Your ROM | Pack's main file |
| --- | --- |
| `HolyDiverHD.nes` | `HdPacks/HolyDiverHD/hires.txt` |
| `Holy_Diver_(Tr).nes` | `HdPacks/Holy_Diver_(Tr)/hires.txt` |

Place all the extracted files beside `hires.txt`, enable HD packs in MesenCE's NES settings, then reopen the ROM.

**[Windows and macOS installation instructions](docs/INSTALLATION.md)** explain how to find your emulator's active data folder, extract the ZIP, check your ROM's SHA-1 and troubleshoot installation. The same instructions are included as `README.txt` inside the install ZIP.

## Project information

- [Release history](CHANGELOG.md)
- [Development documentation and archived notes](docs/development/README.md)
- [Contents and provenance](NOTICE.md)
