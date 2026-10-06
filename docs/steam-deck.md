# Steam Deck build and setup

Target: LCD/OLED on SteamOS, Linux x86-64, RADV Vulkan and Gamescope. Stable 60 FPS is the goal, not a measured result. Use inherited interpolation as the initial 60 FPS mode; it retains 30 Hz game logic. True 60 remains experimental.

## Build dependencies

Build in a Linux development environment rather than modifying SteamOS's read-only root. Use Clang (generated code requires `musttail`), CMake 3.20+, Ninja, Python 3, Vulkan 1.3 headers/loader, SDL3, glslang, zlib, LZ4 and zstd. The [Linux CI workflow](../.github/workflows/linux.yml) contains the Ubuntu dependency and SDL build recipe.

CMake's `-DWWHD_BUNDLED_DEPS=ON` fetches pinned glslang/zlib/LZ4 and SDL3 if missing; it still needs the toolchain and Vulkan development installation. zstd uses a system package when available, otherwise pinned source. Set `CMAKE_PREFIX_PATH` for dependencies installed in a custom prefix and ensure their shared libraries are on the loader path.

Use your own extracted USA title `00050000-10143500`, version 0, with `code/cking.rpx`, `content/` and `meta/` under `game/`. The [installer guide](../tools/installer/README.md) covers validated extraction and supported dump formats. Then follow [the README build commands](../README.md#building--running). Generated game code remains local in ignored `build/gen/`.

A binary built elsewhere must have loader/glibc/library dependencies compatible with SteamOS; compiling successfully in a container does not prove compatibility. If Clang reports unwinder-link errors, the inherited workaround is `-DCMAKE_EXE_LINKER_FLAGS="--unwindlib=libgcc"` when that unwinder is installed.

## Build checks

After a playable build:

```sh
ctest --test-dir build/linux --output-on-failure
WWHD_VK_VALIDATION=1 ./build/linux/wwhd --renderer-smoke
```

Without a game dump, use a separate placeholder build (it cannot run gameplay):

```sh
python3 tools/recomp/stubgen.py build/gen-stub
cmake -S . -B build/linux-stub -G Ninja \
  -DCMAKE_C_COMPILER=clang -DCMAKE_CXX_COMPILER=clang++ \
  -DCMAKE_BUILD_TYPE=Release -DWWHD_RENDERER=VULKAN \
  -DGEN_DIR="$PWD/build/gen-stub"
cmake --build build/linux-stub --parallel 2
ctest --test-dir build/linux-stub --output-on-failure
WWHD_VK_VALIDATION=1 ./build/linux-stub/wwhd --renderer-smoke
```

The smoke test needs a working display/Vulkan driver; headless CI uses Xvfb and Mesa software Vulkan. Require PASS and no validation VUID errors. CI checks are not Deck gameplay or performance evidence; disable validation for benchmarks.

## Launch and controls

Add the native executable as a non-Steam game without forcing Proton. For source builds set **Start In** to the repository root and provide absolute `--game`/`--save` paths. For an inherited portable package use its `wind-waker-hd` launcher. Back up saves before updating; portable setup/import details are in the installer guide.

Select interpolated 60 FPS in the settings overlay, or use `WWHD_INTERP=1 WWHD_TRUE60=0` as in the README. Configure fullscreen 1280×800 output, 16:10, internal scale 1× and FIFO as an initial evaluation configuration, not a validated automatic preset. `WWHD_ASPECT=16:10`, `WWHD_RES_SCALE=1` and `WWHD_VK_PRESENT_MODE=fifo` override corresponding settings; they do not resize the window or enable fullscreen. The inherited SDL settings writer does not persist aspect/fullscreen, so verify them after launch.

Use a gamepad Steam Input layout. Open settings with F1 or hold Select/Minus for about half a second. Generic face buttons follow Wii U physical positions: Deck B → Wii U A, A → B, Y → X, X → Y; remap in Controls if desired. Start with GamePad picture-in-picture and a trackpad mapped to mouse/left click. Deck-specific gyro, touchscreen and rear-button layouts still need validation.

Keep LCD/OLED results separate and record effective refresh/limiter settings. Check controls, audio, GamePad touch and frame pacing after suspend/resume. Source settings use `$XDG_CONFIG_HOME/wwhd` or `~/.config/wwhd`; portable packages keep data under `data/`. Use separate save/settings/cache directories when comparing builds.
