---
name: deck-benchmark
description: Compare builds on real Steam Deck hardware using FPS, frametimes and power measurements. Use when establishing a baseline, validating an optimization or investigating missed 60 FPS targets in ZeldaWWHDRecomp-Deck.
---

# Benchmark on Steam Deck

## Matched comparison

- Primary target: stable **60 displayed FPS using inherited interpolation**, with original 30 Hz game logic. Native 30 FPS and experimental true 60 are separate test modes; do not mix them or call interpolation true 60.
- Pin upstream/Deck commits for project comparisons and parent/candidate commits for individual optimizations. Record dirty diffs, compiler, build flags, dependency versions, Deck model and SteamOS/kernel/Mesa/RADV versions. Test LCD and OLED separately on the same unit within each comparison.
- Match save/location, route/input, camera, graphics quality, output/internal resolution, aspect, GamePad mode, frame-rate mode, refresh, limiter, Steam performance profile, TDP and GPU clock overrides. Also match brightness, audio, radios, background activity and measurement tools.
- Isolate saves/settings/caches. Source builds can use distinct XDG_CONFIG_HOME roots and --save paths; portable mode uses its own config root, so compare separate package folders. Do not depend on cross-build save-state compatibility.
- Warm each build's own shader/driver cache along the same route. Separate cold-start tests; do not blindly share incompatible caches. Use Release builds and disable validation, captures and heavy tracing for primary runs.
- Declare the warm-up and measurement duration in advance (for example, 10 minutes after stabilization). Run at least three matched pairs, alternating order to expose thermal drift. Keep charge/temperature ranges comparable and preserve every valid run.

## Metrics

- Log actual displayed/presented FPS and raw frame intervals with a consistent tool such as MangoHud when available. Record what the logger measures; submitted frames and 30 Hz logic steps are not displayed FPS.
- Report median, p95/p99 and maximum frametime, plus the count/threshold of long frames. The 60 FPS budget is about 16.67 ms per displayed frame; declare the miss threshold before testing. Average FPS alone can hide stutter.
- Log CPU/GPU utilization, CPU/GPU clocks and relevant temperatures. State whether CPU percentage means one core or the whole machine.
- Measure **total system power in watts** while unplugged and discharging. Identify the battery under /sys/class/power_supply and confirm sensor units: power_now is usually microwatts; convert to W. If using current_now × voltage_now, document units and sign. Charging readings and GPU-only watts are not total handheld demand.
- Capture wakeups/context switches when relevant using process/thread counters or scheduler traces with available permissions. Aggregate the game's threads; context switches are not wakeups. Use separate diagnostic runs if profiling changes power materially.
- Mark unavailable metrics as missing, with reasons. Do not substitute lower utilization for measured power or change system permissions just to collect a counter.

## Report

Record per-run settings, scene, cache state, duration, sampling interval, tooling, raw-log paths and correctness observations under ignored build/benchmarks/. Keep game-derived files and personal data out of public reports.

Publish each run, paired differences and aggregate spread for FPS, p95/p99 frametimes and watts. If 60 FPS is not maintained, identify the scene, duration and observed cause; distinguish measured CPU/GPU/presentation limits from a hypothesis. Note image-quality changes and power/pacing tradeoffs explicitly.

A successful change preserves gameplay and quality, with credible pacing/FPS or power improvements beyond run variation. Lower CPU percentage alone proves neither a gain nor improved battery life. Watts are not measured battery runtime; any hours estimate must be labeled as an estimate. With no real Deck measurements, supply a reproducible test plan and mark outcomes unverified.
