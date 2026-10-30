# Installation — Holy Diver HD v1.0.0

## Requirements

- **Mesen emulator with NES HD pack support.** This pack was tested with **MesenCE 2.2.1**. Download MesenCE for your operating system from the [official releases](https://github.com/nesdev-org/MesenCE/releases/tag/2.2.1), and follow its platform requirements.
- **The supported Holy Diver translated ROM**, as an uncompressed `.nes` file. Its full-file **SHA-1** must be:
  `FE2FCD0AD334D792DB16535D09F3AB9FB2BEA3AC`
- **Holy_Diver_HD_v1.0.0.zip** from this project's [Releases page](https://github.com/kgrant191/holy-diver-hd/releases).

The ROM and emulator are supplied separately. Renaming a ROM changes its filename, not its checksum.

## Find MesenCE's data folder

In MesenCE, open **Preferences → Files** and look for **Data storage location**. Use the folder shown there. This is the active location for your installation, including portable installations or setups migrated from Mesen2.

Inside that folder, open or create **HdPacks**.

## The folder name must match the ROM

Create a folder inside `HdPacks` with **exactly the ROM filename, minus the .nes extension**. Preserve spaces, punctuation and capitalization.

| ROM filename | HD pack folder |
| --- | --- |
| `HolyDiverHD.nes` | `HdPacks/HolyDiverHD/` |
| `Holy_Diver_(Tr).nes` | `HdPacks/Holy_Diver_(Tr)/` |

For `HolyDiverHD.nes`, the main pack file must be at:

`<Mesen data folder>/HdPacks/HolyDiverHD/hires.txt`

All the other extracted files belong beside `hires.txt`. The ZIP contains the pack files directly. If your extraction tool creates a folder named `Holy_Diver_HD_v1.0.0`, copy the **files inside it** into your ROM-named folder.

## Windows

1. Download `Holy_Diver_HD_v1.0.0.zip`.
2. Right-click the ZIP in File Explorer and choose **Extract All…**, then **Extract**.
3. Find MesenCE's data folder as described above. Paste that location into File Explorer's address bar and press Enter.
4. Open or create `HdPacks`, then create the folder matching your ROM name. For `HolyDiverHD.nes`, create `HolyDiverHD`.
5. Copy **all extracted pack files** into that folder. Confirm that `hires.txt` is directly inside `HdPacks\HolyDiverHD\`.
6. In MesenCE's **NES settings → General**, enable **HD packs**. Apply the setting.
7. Open the matching `.nes` ROM. If it was already running, fully close the game and open it again.

## macOS

1. Download `Holy_Diver_HD_v1.0.0.zip`.
2. Double-click the ZIP in Finder to extract it. If your browser extracted it automatically, use the resulting folder.
3. Find MesenCE's data folder as described above. In Finder choose **Go → Go to Folder…** (Shift-Command-G), paste that location, and press Return.
4. Open or create `HdPacks`, then create the folder matching your ROM name. For `HolyDiverHD.nes`, create `HolyDiverHD`.
5. Copy **all extracted pack files** into that folder. Confirm that `hires.txt` is directly inside `HdPacks/HolyDiverHD/`.
6. In MesenCE's **NES settings → General**, enable **HD packs**. Apply the setting.
7. Open the matching `.nes` ROM. If it was already running, fully close the game and open it again.

For an upgrade, back up the old pack folder before replacing its contents.

## Check your ROM's SHA-1

Windows PowerShell:

```powershell
Get-FileHash -Algorithm SHA1 -LiteralPath "C:\path\to\HolyDiverHD.nes"
```

macOS Terminal:

```bash
shasum -a 1 "/path/to/HolyDiverHD.nes"
```

Compare the result with the required SHA-1 above. Letter case in the hash does not matter. Hash the extracted `.nes` file itself.

## If the original graphics still appear

- Confirm that HD packs are enabled in NES settings.
- Check the ROM's SHA-1 and the active data folder.
- Check that the pack folder matches the ROM name without `.nes`.
- Check that `hires.txt` is directly inside that folder, alongside all the pack assets.
- Fully close the game and reopen it after changing the files or settings.

Keep all files from the install ZIP together; the pack uses their existing filenames.
