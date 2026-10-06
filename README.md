# ZeldaWWHDRecomp-Deck

A Steam Deck-focused native recompilation project for **The Legend of Zelda: The Wind Waker HD**, based on [ZeldaWWHDRecomp](https://github.com/ZeldaWWHDRecomp/ZeldaWWHDRecomp). Development here targets SteamOS, Linux x86-64, the Deck's AMD APU, RADV Vulkan, Gamescope and handheld use.

This project has its own direction: battery efficiency, stable frame pacing and usable built-in controls on Steam Deck LCD and OLED. The original game runs its main logic at 30 Hz; **stable, efficient 30 FPS is the primary target**. Optional inherited 60 FPS modes remain available, subject to compatibility and measurements.

## Status and scope

This is the project-foundation stage. The runtime, recompiler, installer and multi-platform build infrastructure are inherited from upstream. Deck detection and automatic Deck defaults are **planned, not implemented**. This documentation change does not optimize runtime code.

Steam Deck LCD and OLED on SteamOS are the intended supported models; gameplay compatibility, battery consumption, suspend/resume and sustained pacing on either model are **unverified in this repository**. No Deck benchmark results or battery-life gains are claimed. Other Linux systems can use the inherited Vulkan build; macOS, Windows, Android and Linux arm64 code remain present but are secondary to this project's Deck goals.

## Why this project exists

A handheld needs predictable pacing, low background activity, a useful single-screen layout and settings that respect its power budget. This repository develops and measures those choices specifically for Steam Deck while retaining the original project's technical work and attribution. Generic fixes may be offered upstream; Deck-specific policy lives here.

## Installation

Use [this project's releases](https://github.com/endercodezz/ZeldaWWHDRecomp-Deck/releases) **if a Linux x86-64 package has been published**. Package availability and Deck validation are not established by this README. An upstream download is an upstream build, not a Deck release. If no package is available, follow [the source build instructions](docs/development.md).

For a package using the inherited portable installer:

1. In SteamOS Desktop Mode, extract the Linux x86-64 archive into a writable folder. The inherited package requires Python 3, glibc 2.35+ and a Vulkan 1.3 driver; setup needs network access to download its pinned compiler.
2. Run `wind-waker-hd` from that folder (make it executable if extraction lost its permissions). Supply your own extracted folder containing `code/`, `content/`, `meta/`, a `.wua` archive, or a `.wud`/`.wux` dump and your own keys. Extracted folders and `.wua` need no encryption keys.
3. Only **USA title 00050000-10143500, version 0** is supported. Setup validates the executable; updated or different-region dumps are not interchangeable.
4. Add the launcher as a non-Steam game, select its native Linux executable without forcing Proton, and test in Gaming Mode. See [Steam Deck setup](docs/steam-deck.md) for controls and display configuration.

Portable packages keep generated game code, saves, settings, caches and logs inside `data/`. An extracted game folder can be used in place. Source builds use separate save/configuration paths. Details: [installer documentation](tools/installer/README.md).

## Building from source

Use a Linux development environment with CMake 3.20+, Ninja, Clang/Clang++ (required for `musttail`), Python 3, Vulkan 1.3 headers/loader, glslang, SDL3, zlib and LZ4. zstd is required by the extractor and can be fetched by CMake if absent. Avoid changing SteamOS's read-only system just to install a development toolchain.

With your own validated version-0 game extracted into `game/` and dependencies installed:

```sh
python3 tools/recomp/recomp.py game/code/cking.rpx build/gen
cmake -S . -B build/linux -G Ninja \
  -DCMAKE_C_COMPILER=clang -DCMAKE_CXX_COMPILER=clang++ \
  -DCMAKE_BUILD_TYPE=Release -DWWHD_RENDERER=VULKAN
cmake --build build/linux --parallel 2
ctest --test-dir build/linux --output-on-failure
./build/linux/wwhd --game "$PWD/game" --save "$PWD/save"
```

Parallelism `2` is a conservative build example, not a runtime tuning value. Dependency setup, extraction, stub-only CI builds and smoke tests are in [development.md](docs/development.md). A build or software-Vulkan smoke test does not establish Deck gameplay support.

## Updating

Back up in-game saves and settings first. For portable packages, extract a new release next to the old one, run setup, select the existing game folder and import old saves/settings. Keep the old folder until the new one works. `wind-waker-hd --setup` reopens setup; it is not an automatic remote update service.

For source builds, update the checkout, review migration notes, regenerate local game code if recompiler/hooks changed, then configure, build and test again. Source controls/settings/states normally live in `$XDG_CONFIG_HOME/wwhd` or `~/.config/wwhd`; `--save` controls in-game saves. These inherited paths can be shared with upstream: isolate them for comparisons. Save states may be incompatible across builds; retain ordinary in-game saves.

## Controls and handheld layout

The inherited SDL3 host accepts controllers and allows remapping in **F1 → Controls**. Hold Select/Minus for about half a second to open settings; Home also opens it if the host delivers that button. Steam system buttons may be intercepted.

Face buttons map by physical position to Wii U controls: on an Xbox-style Deck layout, host **B → Wii U A**, **A → B**, **Y → X**, **X → Y**. Sticks, D-pad, shoulders, triggers and Start/Select use inherited mappings. Confirm the live Controls display and remap as desired. Use a gamepad Steam Input layout; rear buttons and trackpads require user assignments. No project-specific Steam Input template or verified gyro profile is shipped yet.

Start with picture-in-picture for the GamePad screen and a trackpad mapped to mouse/left click for touch interaction. Automatic overlay is another inherited option. The current Linux default is a separate GamePad window, which needs Gaming Mode testing. See [steam-deck.md](docs/steam-deck.md).

## Graphics defaults and recommended starting settings

Current Linux behavior: Vulkan/SDL3, a 1280×720 TV window, original 16:9 aspect, 1× internal resolution, FIFO/VSync and 30 FPS unless saved settings or overrides select another mode. GamePad uses a separate window. These are inherited defaults, not a completed Deck profile.

For Deck evaluation, start with fullscreen **1280×800 output**, **16:10**, **1× rendering**, **FIFO** and **30 FPS**, initially with GamePad picture-in-picture. Output size, internal resolution and aspect are separate settings. Keep quality settings identical between comparison builds; disabling visual effects is a quality tradeoff, not evidence of an equivalent-quality optimization. The aspect implementation expands the vertical view at 16:10 rather than stretching the picture.

The [configuration audit and profile plan](docs/development.md#configuration-audit-and-planned-deck-profile) explains how future detected defaults remain overridable. Existing `WWHD_*` variables override relevant saved options; remove launch overrides to let UI choices control subsequent launches.

## Performance and battery philosophy

Priorities, in order: battery life, stable frame pacing, low CPU overhead, low CPU wakeup frequency, avoiding needless GPU work, stable 30 FPS, fast startup, suspend/resume, built-in controls and handheld UX. Optional 60 FPS must not compromise the primary configuration.

Measure unnecessary wakeups/context switches, idle CPU use, busy waiting, background work, total system power and frametime tails. Preserve game behavior and image quality. Lower CPU percentage alone does not establish a successful optimization.

No battery-runtime target is invented. Changes need matched upstream/Deck measurements using [the benchmark protocol](docs/benchmarking.md) and [performance acceptance policy](docs/performance.md).

## Known issues and development status

- Deck controls, Gamescope window handling, LCD/OLED pacing and suspend/resume need hardware validation.
- First-use shader compilation can hitch; distinguish cold-cache startup from warm-cache gameplay tests.
- Inherited documentation reports black-screen waits during audio initialization, incomplete geometry-shader/rectangle-primitive support, harder shadow edges and incomplete later-game testing. These are inherited reports, not newly reproduced Deck findings.
- True 60 FPS is experimental. Save states can be build-dependent and do not replace in-game saves.
- Linux aspect/fullscreen selections are not persisted by the inspected SDL settings writer; see the configuration audit.

Next milestones: an overridable Deck profile, hardware baselines on LCD/OLED, then one measured performance issue at a time. This task stops at the documentation foundation.

## Documentation

- [Steam Deck setup and hardware assumptions](docs/steam-deck.md)
- [Performance goals and acceptance](docs/performance.md)
- [Benchmarking and battery testing](docs/benchmarking.md)
- [Build, configuration audit and development](docs/development.md)
- [Upstream relationship and synchronization](docs/upstream.md)
- [Inherited architecture](docs/how-it-works.md), [Vulkan implementation](docs/vulkan.md), [decompilation notes](docs/decomp-notes.md)
- [Preserved upstream README](docs/upstream-readme.md) and [historical profiling](docs/upstream-performance.md), including non-Deck builds, save conversion and shader preparation

## Contributing

Use [this repository's issues](https://github.com/endercodezz/ZeldaWWHDRecomp-Deck/issues) and pull requests. Include commit IDs, Deck model, SteamOS/Mesa versions, settings and reproduction steps. Performance proposals need repeated power/frametime results, a benchmark manifest and correctness checks. Keep changes narrow and platform policy centralized; preserve credits and license headers. See [development.md](docs/development.md) and [upstream.md](docs/upstream.md).

Do not upload game dumps, keys, generated game code, game-derived caches, save states or game imagery to issues or commits. Share text reproduction steps and sanitized diagnostics instead.

## Relationship with upstream

[ZeldaWWHDRecomp](https://github.com/ZeldaWWHDRecomp/ZeldaWWHDRecomp) provides the original recompilation/runtime work. ZeldaWWHDRecomp-Deck is a separate Steam Deck-focused project based on that work, with its own priorities, documentation and planned defaults. It may import upstream changes periodically and contribute generic fixes back; Deck-specific behavior remains here. This repository does not claim authorship of the original port. See [synchronization policy](docs/upstream.md).

## Credits

- The original [ZeldaWWHDRecomp project and contributors](https://github.com/ZeldaWWHDRecomp/ZeldaWWHDRecomp/graphs/contributors); original notices and commit history are retained.
- [rhemfur](https://github.com/rhemfur): Android port, paced interpolation, Vulkan presentation/feedback-image work and Linux/Windows fixes; [Sean13128](https://github.com/Sean13128): performance and cheats; [arcadematicas](https://github.com/arcadematicas): rumble; [resadent](https://github.com/resadent): native Windows LLVM and Vulkan contributions, as credited in the inherited README. The Vulkan renderer is credited there to OpenAI Codex.
- [Cemu](https://github.com/cemu-project/Cemu): GPU address library, shader decompiler and reference structures (MPL-2.0); extraction, floating-point and OS-layer adaptations retain in-file attribution.
- [metal-cpp](https://developer.apple.com/metal/cpp/) (Apache-2.0), [{fmt}](https://github.com/fmtlib/fmt) (MIT), [Dear ImGui](https://github.com/ocornut/imgui), Omar Cornut and contributors (MIT), [xxHash](https://github.com/Cyan4973/xxHash), Yann Collet (BSD-2-Clause).
- [ZArchive](https://github.com/Exzap/ZArchive), Exzap (MIT No Attribution): archive-format reference, not vendored; [zstd](https://github.com/facebook/zstd), Meta Platforms (BSD-3-Clause): extractor dependency.
- [zeldaret/tww](https://github.com/zeldaret/tww) (CC0): reference for optional function matching. See [preserved upstream credits](docs/upstream-readme.md#credits) and component licenses for details.

## Legal notice

An unofficial fan project, unaffiliated with and not endorsed or sponsored by Nintendo. Nintendo owns the game; names and trademarks belong to their respective owners and identify compatibility.

Provide your own legally obtained dump and necessary keys. This repository and distributable runtime packages do not supply Nintendo game code, assets or keys. Game extraction, translation and compilation happen locally. Do not redistribute game files, generated/recompiled game code or game-derived caches. An ignored file is not automatically safe to distribute.

## License

Code remains under [Mozilla Public License 2.0](LICENSE). Dependencies retain their notices/licenses: [Cemu](runtime/third_party/cemu/LICENSE.txt), [metal-cpp](runtime/third_party/metal-cpp/LICENSE.txt), [fmt](runtime/third_party/fmt/LICENSE), [Dear ImGui](runtime/third_party/imgui/LICENSE.txt), [xxHash](runtime/third_party/xxhash/LICENSE). zstd's license is included by inherited release packaging. Rebranding does not change upstream ownership or licensing.
