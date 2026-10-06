# Repeatable upstream versus Deck benchmarks

No Steam Deck results are published in this foundation. This protocol defines how to collect comparable evidence. It does not install instrumentation or run game tests automatically.

## Comparison and manifest

Compare a pinned upstream ZeldaWWHDRecomp commit with a pinned ZeldaWWHDRecomp-Deck commit on the **same physical Deck**. For a particular optimization, also compare the Deck parent and candidate to isolate the change. Use the same compiler/dependencies/build type and guest-code generation procedure where possible; record unavoidable differences. Never call an experimental build an unmodified upstream baseline.

Copy this manifest into each local result directory and fill every applicable item:

```text
Run ID / date / operator:
Role: upstream | Deck baseline | Deck candidate
Repository URL / full commit / dirty diff:
Compiler / flags / CMake options / dependency versions:
Deck model / hardware revision / battery health and capacity:
SteamOS / kernel / Mesa-RADV / SDL / Vulkan device:
Gaming or Desktop Mode / Gamescope version and launch arguments:
Game title / version / local RPX hash (no game files):
Scene / in-game save identity / route / camera / input sequence:
Output resolution / internal scale / aspect / fullscreen:
30 or 60 FPS mode / presentation / limiter owner and value:
Refresh rate / brightness / auto-brightness / audio volume:
AO mode and depth / FXAA / anisotropy / scaling filter:
GamePad mode / controller mode / gameplay mods:
Steam performance profile / TDP / GPU clock / SMT or other overrides:
Wi-Fi / Bluetooth / downloads / overlays / background applications:
Battery or AC / state-of-charge range / temperatures / room conditions:
Shader cache origin / warm-up route and duration:
Measurement duration / sampling interval / repeat and execution order:
Measurement tools and versions / sensor paths / units / permissions:
Raw logs / missing metrics and reason / correctness observations:
```

Keep game saves, save states and shader caches local. A textual save identity or local checksum permits reproducibility without distributing game-derived data. Do not include keys, personal paths or game imagery in public results.

## Controlled runs

1. Select a repeatable scene and camera: use a backed-up in-game save and a documented idle interval or fixed route/input script. Do not depend on cross-build save-state compatibility. Include both a static scene and a repeatable gameplay route before generalizing results.
2. Isolate save/config/cache directories per build. In source builds, `XDG_CONFIG_HOME=/absolute/run/config` changes the `wwhd` config root, `WWHD_SETTINGS=/absolute/run/settings.ini` can isolate settings, and `--save /absolute/run/save` isolates normal saves. Portable mode overrides the config root, so use separate portable package folders instead. Copy the same starting save and explicitly match every relevant option.
3. Warm each build's own shader/driver caches by traversing the same route until first-use work settles. Do not share incompatible driver/pipeline caches blindly. Restore an equivalent warmed starting state for each repeat. Keep cold-start results separate.
4. Disable validation layers, captures, debug tracing and costly profilers for primary power/FPS comparisons. Match logging tools and overhead in both builds; record visible overlays. Use separate instrumented runs to explain a result.
5. Set identical resolution, frame rate, graphics, Deck performance settings, brightness, refresh and test duration. Keep network, volume, radios and background activity consistent. Allow temperatures and discharge rate to settle, using a recorded warm-up period.
6. Use a declared fixed measurement window, for example **10 minutes after warm-up**, and at least **three matched pairs**. These are protocol choices, not performance targets. Alternate upstream/Deck order (A-B, B-A, A-B) to expose thermal and battery drift. Return to a comparable state of charge and temperature; if drift prevents matching, rerun or qualify the result.
7. Record correctness and all raw samples. Repeat exclusions only for documented external interruptions, applying the same exclusion rule to both builds. Keep unfavorable valid runs.

For the primary 30 FPS comparison, explicitly select native 30 FPS in both builds; saved interpolation choices can otherwise invalidate the comparison. Run optional 60 FPS tests as a separate configuration. Refresh, resolution and quality must match within a pair.

## Metrics and measurement sources

- **Total system power (W):** on battery, identify the actual battery under `/sys/class/power_supply/`, record `status`, and use its `power_now` if available (normally micro-watts, convert to W). If absent, derive magnitude from simultaneous `current_now` and `voltage_now` with documented units. Cross-check against `energy_now` change over the interval. Missing sensors are missing data, never zero.
- **FPS/frametime:** use a fixed-version logger such as MangoHud where available. Record what it measures: game logic, submitted frames and displayed presentation are not interchangeable, particularly with interpolation. Capture raw frame intervals as well as average FPS.
- **CPU/GPU utilization and clocks:** use supported SteamOS/Mesa telemetry or a consistent logger. State whether CPU percent is normalized to one core or all cores, and whether samples are per-thread, per-process or system-wide. Record CPU/GPU clocks and temperatures with timestamps.
- **Context switches:** use process counters, `pidstat` where installed, or `perf stat` with appropriate permissions. Aggregate threads; counters from `/proc/PID/status` alone may omit other threads.
- **Wakeups:** use a documented scheduler trace, such as `sched:sched_wakeup`/`sched:sched_wakeup_new` if exposed, and attribute events to the game's threads. System wakeups, timer expirations and context switches are different measurements. Use a separate diagnostic pass if tracing materially affects power.

Tool availability and privileges differ between SteamOS installations. Record unsupported metrics and the reason; do not change kernel/security settings merely to satisfy this protocol. Confirm tool units and sample scopes on the actual device before using them. Align timestamps for power, clocks and frametimes.

## Power, energy and battery duration

Primary handheld power tests run **unplugged**, while the battery is discharging, over a matched state-of-charge range. A charging battery sensor is not a measure of gameplay system demand. AC tests are a separate category; external wall-meter readings include adapter losses and cannot be compared directly with battery discharge watts.

Integrate discharge power over time to obtain Wh, or compare `energy_now` deltas when supported. Report mean/median watts per run, total energy, duration, temperature and sensor sampling uncertainty. A watts result does not by itself establish runtime in hours.

For a separate battery-duration test, declare start/end charge thresholds in advance, use identical settings and a repeatable route for the whole discharge window, and repeat on the same unit. Report elapsed time over those thresholds, battery health and remaining capacity. `usable Wh / mean W` is an estimate, not a measured full-discharge duration. Never pool LCD and OLED runtime: battery capacity, display and refresh differ. Do not promise a battery gain from another machine's results.

## Reporting and decision

Publish each valid run and the paired differences, then aggregate mean/median and run-to-run spread. Frametime summaries include median/p95/p99, maximum, number and definition of long frames, and a time series when useful. At 30 FPS the nominal interval is about 33.33 ms; declare the threshold for a long frame before comparing. Include startup, first-use shader work and resume as separate scenarios.

Accept an efficiency claim only with lower power/energy beyond observed variation, preserved image quality/game behavior and acceptable frametime tails. If CPU use falls but watts or pacing worsens, report that result. If power was not measured, label the conclusion as a CPU/pacing result, not battery optimization. State which scenes/models were tested and avoid extrapolating across the whole game.

Raw result files stay local under ignored `build/benchmarks/<run-id>/` by default. Public reports may live in `docs/` after sanitization; include commit IDs and the manifest, never generated game material. No baseline results have been collected yet.
