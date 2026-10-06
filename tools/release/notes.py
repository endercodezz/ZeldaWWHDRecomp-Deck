#!/usr/bin/env python3
"""Steam Deck release notes. Usage: notes.py README VERSION SHA256SUMS.txt."""
from pathlib import Path
import sys


def main():
    _, version, sums = sys.argv[1:4]
    checksums = Path(sums).read_text().strip()
    print(f"""# ZeldaWWHDRecomp-Deck {version}

Steam Deck LCD/OLED package for SteamOS (Linux x86-64, glibc 2.35+, Vulkan 1.3).
Based on ZeldaWWHDRecomp and its contributors; maintained by endercodezz.

1. Download `ZeldaWWHDRecomp-Deck-*-steamdeck-x86_64.zip` and extract the whole folder in Desktop Mode.
2. Open `wind-waker-hd`, choose your own USA version-0 dump and let setup build the game locally.
3. Press Play; add `wind-waker-hd` to Steam as a non-Steam game without forcing Proton.

Supported inputs: extracted `code/content/meta` folder, `.wua`, or `.wud`/`.wux` with your own keys.
A raw RPX alone is insufficient. No game code, assets or keys are included in this download.
Setup downloads its verified compiler; no system compiler installation is needed.
Read `START-HERE.txt` inside the archive for controls, settings and updating.

Fresh installs select interpolated 60 FPS, 1x rendering, FIFO and GamePad picture-in-picture.
Interpolation keeps 30 Hz game logic. Stable 60 FPS and suspend/resume on Deck remain unverified.
CI validates package installation using placeholder game code and software Vulkan, not gameplay.

## SHA-256

```
{checksums}
```
""")


if __name__ == '__main__':
    main()
