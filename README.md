# ZeldaWWHDRecomp-Deck

A Steam Deck-focused native recompilation project for **The Legend of Zelda: The Wind Waker HD**, based on [ZeldaWWHDRecomp](https://github.com/ZeldaWWHDRecomp/ZeldaWWHDRecomp). Maintained by [@endercodezz](https://github.com/endercodezz).

## About

Steam Deck LCD and OLED are the primary targets: SteamOS, Linux x86-64, AMD Van Gogh-class hardware, RADV Vulkan and Gamescope. This project develops its own Deck defaults, handheld UX and performance work using ZeldaWWHDRecomp as its technical foundation.

The main goal is **stable 60 FPS on Steam Deck**, with the lowest practical power consumption while maintaining consistent frametimes and correct gameplay.

The baseline approach is inherited **60 FPS interpolation**, which keeps the original 30 Hz game logic. Native 30 FPS remains available; experimental true 60 changes parts of game timing and requires separate correctness testing. Interpolation is not true 60.

## Goals

- Stable 60 FPS and consistent frame pacing.
- Lower CPU/GPU overhead, power draw and unnecessary wakeups.
- Useful Deck defaults, 1280×800 / 16:10 output and built-in controls.
- Reliable suspend/resume, fast startup and less background work.

## Status

Early and experimental. Stable 60 FPS, battery efficiency and suspend/resume on LCD/OLED have not been verified here. Automatic Deck detection and Deck-specific defaults are not implemented yet. The inherited Linux defaults still select native 30 FPS; this cleanup changes documentation and agent workflows only.

## Building / Running

Use Linux with Clang, CMake 3.20+, Ninja, Python 3, Vulkan 1.3, SDL3, glslang, zlib, LZ4 and zstd. With dependencies installed and your own supported **USA version-0** game extracted into `game/`:

```sh
python3 tools/recomp/recomp.py game/code/cking.rpx build/gen
cmake -S . -B build/linux -G Ninja \
  -DCMAKE_C_COMPILER=clang -DCMAKE_CXX_COMPILER=clang++ \
  -DCMAKE_BUILD_TYPE=Release -DWWHD_RENDERER=VULKAN
cmake --build build/linux --parallel 2
WWHD_INTERP=1 WWHD_TRUE60=0 ./build/linux/wwhd --game "$PWD/game" --save "$PWD/save"
```

See [Steam Deck setup](docs/steam-deck.md) for dependencies, testing, Steam launch settings and controls. Game extraction/setup is covered in [the installer guide](tools/installer/README.md).

## Development

Deck-specific changes and policy are developed independently here. Generic improvements may occasionally be contributed back to ZeldaWWHDRecomp; upstream changes can be imported deliberately while preserving Deck behavior and original authorship.

Keep changes small and measured. FPS, frametimes and total power draw matter together; lower CPU usage alone is not an improvement claim. Agent instructions and recurring workflows are indexed in [AGENTS.md](AGENTS.md).

Technical references: [architecture](docs/how-it-works.md), [Vulkan renderer](docs/vulkan.md), [decompilation and timing](docs/decomp-notes.md). Other-platform instructions and upstream history remain available in [ZeldaWWHDRecomp](https://github.com/ZeldaWWHDRecomp/ZeldaWWHDRecomp).

## Credits

ZeldaWWHDRecomp-Deck is maintained by [@endercodezz](https://github.com/endercodezz), based on [ZeldaWWHDRecomp and its contributors](https://github.com/ZeldaWWHDRecomp/ZeldaWWHDRecomp/graphs/contributors). Inherited code keeps its original authorship and notices.

Upstream contributions include [rhemfur](https://github.com/rhemfur) (Android, interpolation and Vulkan/Linux work), [Sean13128](https://github.com/Sean13128) (performance and cheats), [arcadematicas](https://github.com/arcadematicas) (rumble) and [resadent](https://github.com/resadent) (Windows LLVM/Vulkan). The inherited Vulkan renderer credits OpenAI Codex.

GPU addressing and shader components come from [Cemu](https://github.com/cemu-project/Cemu). Other dependencies/references include metal-cpp, fmt, Dear ImGui (Omar Cornut and contributors), xxHash (Yann Collet), zstd (Meta), ZArchive (Exzap) and [zeldaret/tww](https://github.com/zeldaret/tww). Component license files and source notices retain their attribution.

## Legal / License

Unofficial fan project, not affiliated with or endorsed by Nintendo. You must supply your own legally obtained game dump and any needed keys. No Nintendo game code, assets or keys are provided; do not redistribute locally generated game code or game-derived data.

Project code is licensed under [MPL-2.0](LICENSE). Third-party components retain their own licenses in [runtime/third_party](runtime/third_party) and inherited dependency packaging.
