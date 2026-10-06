# Steam Deck performance policy

Battery efficiency and stable 30 FPS on SteamOS are the primary goals. No Deck power, FPS or battery gains have been measured in this foundation. Historical Mac/Windows findings remain in [upstream-performance.md](upstream-performance.md); they suggest investigation topics, not Deck results.

## Measurable goals

- Reduce unnecessary wakeups: compare wakeups per second and scheduling traces in matched gameplay, idle and menu scenes. Keep audio and guest synchronization correct.
- Reduce idle work and busy waiting: compare CPU time per second/per game step and identify spinning stacks. Preserve deadlines and frametime tails.
- Avoid useless rendering: compare GPU utilization, GPU time where available, and total system power; verify GamePad, HUD, effects and synchronization.
- Stabilize pacing: report median/p95/p99 displayed frametimes and long-frame counts against the 30 FPS target (approximately 33.33 ms per frame). Average FPS cannot hide hitches.
- Improve RADV behavior: inspect Vulkan traces on actual Deck hardware. Software Vulkan CI and Windows GPU results are not RADV performance evidence.
- Reduce background work: measure matched foreground/menu scenarios and suspend/resume behavior, with wakeups/context switches alongside power.
- Reduce energy at equivalent quality: compare repeated mean/median battery-discharge watts and integrated Wh, preserving frame rate, resolution and image quality.
- Improve startup/resume: measure launch-to-interactive time with cold/warm caches separately, and wake-to-play time with audio/input/save checks.

These are baseline-relative goals, not promised reductions. Establish a baseline before setting numerical targets. Keep LCD and OLED results separate.

## Accepting changes

Use [benchmarking.md](benchmarking.md). Compare pinned upstream and Deck baselines; add a Deck parent-versus-candidate comparison to isolate individual changes. Match compiler/build flags and settings, documenting unavoidable differences.

Accept an efficiency claim only when repeated power/energy improves beyond observed variation without unacceptable pacing or correctness regressions. Publish individual runs, aggregates, instrumentation and limitations. Lower CPU percentage, a different clock or one favorable run is insufficient.

State power tradeoffs for pacing changes. Label quality reductions separately from equivalent-quality optimization. Preserve exact guest floating-point semantics and gameplay timing. Optional interpolated 60 FPS remains available; true 60 remains experimental.

## Next work

Implement the small centralized profile, then collect hardware baselines. Profile one demonstrated issue before changing runtime behavior. Do not rewrite the renderer, scheduler, threading system or SDL host during this foundation task.
