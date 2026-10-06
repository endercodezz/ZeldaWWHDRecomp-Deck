# Steam Deck setup and assumptions

## Target environment

Primary targets are Steam Deck LCD and OLED running SteamOS on Linux x86-64. The hardware baseline is the Deck's AMD Van Gogh-class APU, RADV Vulkan and Gamescope in Gaming Mode, with a 1280×800, 16:10 handheld display and built-in controls. Treat OLED as a distinct hardware/display variant; do not infer identical clocks, refresh settings, power or battery life from LCD measurements.

Both models are intended targets, not a claim of verified compatibility. Record the actual model, SteamOS/kernel/Mesa versions, Vulkan device/driver and active display mode. External monitors, desktop compositors, alternative OS installations and other AMD handhelds need separate results. SteamOS or RADV alone is not sufficient evidence that a machine is a Deck.

## Launching through Steam

Complete installation in Desktop Mode using [the README](../README.md#installation). Add the native launcher as a non-Steam game; do not force Proton. For a source build, add `build/linux/wwhd` and provide absolute `--game` and `--save` arguments. Set Steam's **Start In** directory to the repository root, since some inherited paths are relative.

In Gaming Mode, use a game-specific performance profile and explicitly record resolution, refresh rate, limiter, TDP and GPU clock settings. Steam/Gamescope controls may change with SteamOS versions; confirm effective settings instead of assuming menu defaults. Test on the internal display first. This workflow has not yet been validated on Deck hardware here.

## Starting 30 FPS configuration

Use fullscreen output at 1280×800, 16:10 aspect, internal resolution 1×, Vulkan FIFO/VSync and the overlay's 30 FPS option. Set Graphics/Display choices in **F1** or the controller settings shortcut. Fullscreen is available through the overlay or F11/Alt+Enter; the initial SDL window is still 1280×720.

At 16:10 the aspect code keeps the horizontal field of view and expands the vertical view. Guest coordinates remain based on 1280×720; aspect-aware render targets and final composition are separate from the output window. Selecting 1× alone does not select a 1280×800 output.

For a source build, this optional one-launch example makes existing configuration overrides explicit:

```sh
WWHD_INTERP=0 WWHD_TRUE60=0 WWHD_RES_SCALE=1 \
WWHD_ASPECT=16:10 WWHD_VK_PRESENT_MODE=fifo WWHD_DRC_MODE=pip \
./build/linux/wwhd --game "$PWD/game" --save "$PWD/save"
```

It does not resize the window or enable fullscreen. These variables override saved choices; remove the relevant override to let the UI take precedence. They are evaluation settings, not an automatically detected profile.

Choose an available refresh setting that is an integer multiple of 30 Hz for an initial pacing comparison, and record the effective refresh. Evaluate LCD and OLED separately. The game's native pacing and FIFO provide the initial limit; if adding Steam's limiter, apply the same setting to both benchmark builds and inspect pacing/input latency. Avoid silently stacking different limiters. No specific TDP, GPU clock, brightness or battery duration is recommended without measurements.

Keep ambient occlusion, filtering, FXAA and other quality options at identical documented values between builds. Do not assume that lower utilization or disabled effects improves battery life.

## Built-in controls

Start with Steam Input presenting a gamepad, then inspect **Controls** for live feedback. The inherited face-button mapping follows Wii U physical positions: Deck B is Wii U A, Deck A is B, Deck Y is X, Deck X is Y. Remap if you prefer label-based controls. Sticks, D-pad, bumpers, triggers, stick clicks and Start/Select use the generic mapping.

Hold Select/Minus about half a second to open settings; F1 is a reliable keyboard fallback that can be assigned to a rear button. Steam's system button may not reach the app. Assign a trackpad to mouse and left click to use the GamePad picture. Direct Deck touchscreen behavior, gyro, rear-button layouts and text entry need hardware tests; no Deck-specific template is shipped yet. If input duplicates or disappears, inspect Steam Input and the Controls display before changing the runtime.

## GamePad display and UX

Picture-in-picture is the proposed first-run Deck layout because it uses one host window and keeps touch access visible. Automatic overlay is an alternative to test; off and GamePad-only remain user choices. The current inherited default is a separate window. Verify map/item selection, overlay readability, pointer positioning and text entry at 1280×800 in Gaming Mode. Do not claim that hiding the GamePad avoids its rendering work without profiling.

## Suspend/resume checks

Save normally before testing. Repeat suspend/resume in gameplay, menus and with the settings overlay open. Record suspend duration and wake-to-play time; verify audio, controls, touch, pacing, window focus, Vulkan surface recovery and in-game saving. Compare against upstream under the same conditions. Suspend/resume support is currently unverified; report observed failures rather than promising seamless recovery.

Portable data lives inside the package; source settings use `$XDG_CONFIG_HOME/wwhd` or `~/.config/wwhd`. See [development.md](development.md) for isolation and the future profile design.
