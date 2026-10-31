HOLY DIVER HD v1.0.0
Requirements and installation

REQUIREMENTS
- Mesen with NES HD pack support. Tested with MesenCE 2.2.1.
  Download: https://github.com/nesdev-org/MesenCE/releases/tag/2.2.1
  Follow the emulator download page's requirements for your operating system.
- The supported Holy Diver translated ROM, extracted as a .nes file.
  Required full-file SHA-1:
  FE2FCD0AD334D792DB16535D09F3AB9FB2BEA3AC

The ROM and emulator are supplied separately.

FIND YOUR MESENCE DATA FOLDER
Open MesenCE's Preferences, select Files, and find Data storage location.
Use the folder shown there, including for portable or migrated installations.
Open or create a folder named HdPacks inside that data folder.

MATCH THE ROM NAME
The folder inside HdPacks must match your ROM filename exactly, with the .nes
extension removed. Preserve spaces, punctuation and capitalization.

ROM: HolyDiverHD.nes
Folder: <Mesen data folder>/HdPacks/HolyDiverHD/
Main file: <Mesen data folder>/HdPacks/HolyDiverHD/hires.txt

ROM: Holy_Diver_(Tr).nes
Folder: <Mesen data folder>/HdPacks/Holy_Diver_(Tr)/

All extracted pack files go directly inside that ROM-named folder, beside
hires.txt. The release ZIP contains the pack files directly. If your extraction
tool creates a Holy_Diver_HD_v1.0.0 folder, copy the files inside it into your
ROM-named folder.

WINDOWS
1. Download Holy_Diver_HD_v1.0.0.zip.
2. In File Explorer, right-click the ZIP, choose Extract All, then Extract.
3. Find the active data folder in MesenCE's Preferences > Files.
   Paste that location into File Explorer's address bar and press Enter.
4. Open or create HdPacks. Inside it, create the folder matching your ROM name.
   For HolyDiverHD.nes, create HolyDiverHD.
5. Copy ALL extracted pack files into that folder. Confirm that hires.txt is
   directly inside HdPacks\HolyDiverHD\, alongside the other assets.
6. In MesenCE's NES settings, on General, enable HD packs and apply the setting.
7. Open the matching .nes ROM. If it was running, fully close the game first
   and then reopen it.

MACOS
1. Download Holy_Diver_HD_v1.0.0.zip.
2. Double-click the ZIP in Finder to extract it. If your browser extracted it
   automatically, use the resulting folder.
3. Find the active data folder in MesenCE's Preferences > Files.
   In Finder, choose Go > Go to Folder (Shift-Command-G), paste that location,
   and press Return.
4. Open or create HdPacks. Inside it, create the folder matching your ROM name.
   For HolyDiverHD.nes, create HolyDiverHD.
5. Copy ALL extracted pack files into that folder. Confirm that hires.txt is
   directly inside HdPacks/HolyDiverHD/, alongside the other assets.
6. In MesenCE's NES settings, on General, enable HD packs and apply the setting.
7. Open the matching .nes ROM. If it was running, fully close the game first
   and then reopen it.

UPDATING
Back up the old pack folder before replacing its contents.

VERIFY YOUR ROM
Hash the extracted .nes file itself. Renaming it does not change its hash.
Windows PowerShell:
  Get-FileHash -Algorithm SHA1 -LiteralPath "C:\path\to\HolyDiverHD.nes"
macOS Terminal:
  shasum -a 1 "/path/to/HolyDiverHD.nes"
Compare with the required SHA-1 above; letter case in the hash does not matter.

TROUBLESHOOTING
If original graphics still appear, check the ROM hash, active data folder,
matching folder name and enabled HD pack setting. Confirm hires.txt is directly
inside the ROM-named folder, alongside every other extracted asset. Fully
close the game and reopen it after changing pack files or settings.
Keep all files together with their existing filenames.

Project and downloads:
https://github.com/kgrant191/holy-diver-hd
https://github.com/kgrant191/holy-diver-hd/releases
