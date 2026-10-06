# Development and build guide

This foundation changes documentation and project direction. Runtime performance changes and automatic platform defaults are outside its scope. See [performance.md](performance.md) before proposing optimizations.

## Linux build requirements

The inspected `CMakeLists.txt` requires CMake 3.20+, Clang for generated-code `musttail`, C11/C++20, Python 3 for code generation, and Vulkan 1.3. Linux uses the Vulkan renderer with the SDL3 host. Dependencies are SDL3, glslang/SPIRV, Vulkan headers/loader, zlib, LZ4, threads and zstd for `.wua` extraction. The normal build defaults to RelWithDebInfo; explicitly use Release for comparisons.

Use a separate Linux development machine or suitable development environment rather than disabling SteamOS's read-only root. Building inside a container does not automatically make the result compatible with SteamOS: loader/ABI, glibc and dynamic library dependencies must match the target. An inherited portable Linux package targets glibc 2.35+, but a locally built binary inherits its build environment's requirements.

The inherited Ubuntu 24.04 CI installs:

```sh
sudo apt-get update
sudo apt-get install -y clang cmake ninja-build pkg-config zlib1g-dev liblz4-dev \
  libvulkan-dev glslang-dev glslang-tools mesa-vulkan-drivers \
  vulkan-validationlayers xvfb libx11-dev libxext-dev libxrandr-dev \
  libxcursor-dev libxi-dev libxss-dev libxfixes-dev libxkbcommon-dev \
  libwayland-dev libasound2-dev libpulse-dev libudev-dev libdbus-1-dev
```

This is an Ubuntu recipe, not a SteamOS installation command. CI builds SDL3 from the pinned `release-3.2.24` tag into a user prefix:

```sh
mkdir -p build
git clone --depth 1 --branch release-3.2.24 https://github.com/libsdl-org/SDL.git build/sdl3-src
cmake -S build/sdl3-src -B build/sdl3-build -G Ninja \
  -DCMAKE_BUILD_TYPE=Release -DSDL_TESTS=OFF -DSDL_EXAMPLES=OFF \
  -DCMAKE_INSTALL_PREFIX="$PWD/build/deps"
cmake --build build/sdl3-build --parallel 2
cmake --install build/sdl3-build
```

The bundled-dependency path uses a different pinned SDL version; record which path was used. `-DWWHD_BUNDLED_DEPS=ON` builds pinned glslang/zlib/LZ4 and SDL3 if missing; it still needs a development toolchain and Vulkan installation. zstd is resolved separately through `cmake/Zstd.cmake` (system package/pkg-config, otherwise pinned source). Dependency fetching requires network access.

## Prepare your own game

Only USA title `00050000-10143500`, version 0 is supported. Use a validated extracted game folder containing `code/cking.rpx`, `content/` and `meta/`. The inherited portable installer validates executable hashes and accepts `.wua`, `.wud` and `.wux` sources; see [installer documentation](../tools/installer/README.md).

Alternatively, the inherited Python disc extractor accepts `.wud`/`.wux`. It needs `pycryptodome`, your dump's disc key and your own Wii U common key in the documented key files/environment. Do not put keys in shell command history or source files:

```sh
python3 -m venv build/extract-venv
build/extract-venv/bin/python -m pip install pycryptodome
build/extract-venv/bin/python tools/wudextract.py game.wux extract game
python3 tools/recomp/recomp.py game/code/cking.rpx build/gen
```

For this example, `game.key` is next to `game.wux`; a valid `common.key` is supplied locally as described in [the preserved requirements](upstream-readme.md#requirements-building-from-source). An extracted folder avoids this step. The native extractor's `.wua` support is built by CMake, so initial source-build bootstrap is simplest with an already extracted folder. Generated code stays local in ignored `build/gen/`.

## Compile, test and launch

```sh
cmake -S . -B build/linux -G Ninja \
  -DCMAKE_C_COMPILER=clang -DCMAKE_CXX_COMPILER=clang++ \
  -DCMAKE_BUILD_TYPE=Release -DWWHD_RENDERER=VULKAN \
  -DCMAKE_PREFIX_PATH="$PWD/build/deps"
cmake --build build/linux --parallel 2
ctest --test-dir build/linux --output-on-failure
LD_LIBRARY_PATH="$PWD/build/deps/lib:$PWD/build/deps/lib64${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}" \
  ./build/linux/wwhd --game "$PWD/game" --save "$PWD/save"
```

Use the prefix only when SDL3 was installed there; otherwise rely on installed packages. Ensure its actual shared-library directory is on the loader path. Increase build parallelism only if memory permits. If Clang linking reports `_Unwind_*`/`-lunwind` errors, the inherited workaround is `-DCMAKE_EXE_LINKER_FLAGS="--unwindlib=libgcc"` where that unwinder is installed.

Full gameplay needs your generated game code and game files. Clang's exact floating-point flags (`-ffp-contract=off`, no fast-math) and guest synchronization must remain intact. Windows/macOS/Android instructions are retained in [upstream-readme.md](upstream-readme.md#building).

## Build checks without game files

The inherited Linux workflow uses placeholder guest code and Mesa lavapipe. It checks compilation, unit tests and Vulkan behavior; it cannot play the game or measure Deck performance:

```sh
python3 tools/recomp/stubgen.py build/gen-stub
cmake -S . -B build/linux-stub -G Ninja \
  -DCMAKE_C_COMPILER=clang -DCMAKE_CXX_COMPILER=clang++ \
  -DCMAKE_BUILD_TYPE=Release -DWWHD_RENDERER=VULKAN \
  -DGEN_DIR="$PWD/build/gen-stub" -DCMAKE_PREFIX_PATH="$PWD/build/deps"
cmake --build build/linux-stub --parallel 2
ctest --test-dir build/linux-stub --output-on-failure
LD_LIBRARY_PATH="$PWD/build/deps/lib:$PWD/build/deps/lib64${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}" \
  WWHD_VK_VALIDATION=1 xvfb-run -a -s "-screen 0 1920x1080x24" \
  ./build/linux-stub/wwhd --renderer-smoke
```

Confirm the smoke output says PASS and has no validation VUID errors. Run hardware smoke/gameplay checks separately on RADV. The installed Vulkan ICD determines which device the example uses; a deterministic lavapipe run must select the local lavapipe ICD explicitly, as appropriate to the environment. Do not mix stub output with the playable `build/linux` directory.

## Configuration audit and planned Deck profile

The following describes the inspected code, not newly implemented features:

- `CMakeLists.txt`: Linux selects `WWHD_RENDERER=VULKAN` and SDL3. Renderer selection/CLI handling is centralized in `runtime/src/gfx/renderer.cpp`.
- `runtime/src/platform/host.h`: source configuration root is `$XDG_CONFIG_HOME/wwhd` or `~/.config/wwhd`. `portable.txt` beside the executable instead selects the package's `user/` root. Existing upstream installs can share these paths; do not silently migrate them.
- `runtime/src/gfx/vulkan/overlay_sdl.cpp`: `settings.ini` stores `resScale`, `fps60`, `fps60Paced`, `vkPresentMode`, AO/filtering/FXAA and GamePad layout. `WWHD_SETTINGS` chooses another file. `fps60` values are 0/native 30, 1/interpolation, 2/true 60. Relevant environment overrides suppress loading/saving the corresponding UI values.
- `runtime/src/interp.cpp`, `true60.cpp`, `main.cpp`: Linux starts without interpolation/true 60 unless configured. The automatic interpolation enable in `main.cpp` is Android-only.
- `runtime/src/gfx/vulkan/settings.cpp`: presentation defaults to FIFO; `WWHD_VK_PRESENT_MODE=fifo|mailbox|immediate` is an explicit launch override. Historical notes claiming mailbox defaults should not override current code.
- `runtime/src/gfx/vulkan/backend.cpp`: creates a 1280×720 TV window. Fullscreen is exposed through the SDL host UI. The inspected settings writer does not persist fullscreen or window dimensions.
- `runtime/src/aspect.cpp`: original 16:9 unless `WWHD_ASPECT` selects otherwise; 16:10 expands vertical field of view. The SDL overlay exposes aspect selection, but the inspected settings writer does not persist it.
- `runtime/src/gfx/display_modes.cpp`: non-Android GamePad default is `window`; saved modes and `WWHD_DRC_MODE`/`WWHD_DRC_PIP` overrides are applied by the host.
- `runtime/src/input_map.cpp`, `platform/input_sdl.cpp`: generic SDL gamepad mapping and `controls.json` remapping. `WWHD_CONTROLS` overrides its path. No Deck-specific mapping/detection was found.

### Proposed design, not implemented

Add one small platform/profile component under `runtime/src/platform/` for capability detection and default selection. Detect actual Deck hardware using reviewed hardware identifiers; treat SteamOS and Gamescope as environment capabilities, not hardware proof. Inspect real LCD/OLED identifiers before writing the detector. Unknown machines use existing generic defaults. Detection must be safe when system identity files are absent or inaccessible, including container environments.

Provide an explicit opt-in/opt-out profile choice so users can select generic behavior or test a Deck profile without spoofing hardware. Exact API/settings names are to be decided in the implementation PR; no new environment switch is promised here.

Resolve values centrally in this order: generic fallback, detected/explicit profile defaults, existing saved user settings, explicit environment overrides, and supported command-line overrides. Apply profile defaults only to missing values; never rewrite a user's settings file every launch. Preserve the current meaning of existing overrides and allow subsequent UI changes when no launch override is active.

The proposed Deck defaults are fullscreen 1280×800 output, 16:10, Vulkan, FIFO, native 30 FPS, 1× internal scale, an accessible single-window GamePad mode (initial candidate: picture-in-picture), and built-in gamepad controls. Add persistence for aspect/output/fullscreen where required before claiming saved overrides work. Do not change AO, filtering, TDP, CPU/GPU clocks or quality based on guesses. 60 FPS and alternate GamePad layouts stay user-selectable.

Feed the resolved profile into existing host/configuration boundaries rather than inserting `if (steamDeck)` across renderer/scheduler code. Account for static environment-based initializers: provide resolved defaults before those values are consumed or initialize them explicitly once at startup. Add only the needed sources to CMake. Keep non-Deck behavior and upstream merging practical.

Implementation validation should cover hardware identity and missing-data fallback, saved/environment/CLI precedence, opt-out, both models, no overwrite of existing settings, 30/60 FPS switching, aspect/fullscreen persistence, controls and suspend/resume. Unit tests are appropriate when this logic exists; this documentation task adds no placeholder runtime implementation.

## Contributions and validation

Keep PRs small, state observed before/after behavior and use [the benchmark manifest](benchmarking.md) for performance work. Preserve all licenses, upstream author credits and commit history. Use [upstream.md](upstream.md) for imports. Never commit game-derived data; inspect actual diffs instead of relying only on `.gitignore`.

Documentation-only changes need local-link checks, command/configuration review and `git diff --check`; full game builds are unnecessary. Runtime changes need appropriate inherited unit/smoke checks and hardware validation. Missing hardware evidence must be stated explicitly.
