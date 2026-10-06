---
name: deck-optimization
description: Implement one focused Steam Deck performance optimization with correctness checks and a hardware test recipe. Use when asked to reduce runtime overhead, improve 60 FPS pacing or lower power consumption in ZeldaWWHDRecomp-Deck.
---

# One Deck optimization

1. Inspect the relevant runtime/configuration code and current worktree before editing. Identify a measured bottleneck or a testable hypothesis; keep native 30 FPS, interpolated 60 FPS and experimental true 60 distinct.
2. Define the baseline, comparison scene and expected mechanism. Choose actual FPS, p95/p99 frametime and total system watts as primary metrics; add CPU/GPU time, clocks, wakeups or context switches to test the hypothesis. Use [deck-benchmark](../deck-benchmark/SKILL.md) for the comparison procedure.
3. Make **one focused change**. Do not stack unrelated caches, scheduler changes and rendering experiments. Preserve guest timing, exact FP semantics, synchronization, audio, saves and image quality. Keep any Deck policy centralized and user-overridable.
4. Build/test using the root AGENTS.md commands. Run relevant unit tests and Vulkan smoke/validation checks; use a stub build if game files are unavailable. Record toolchain/platform limitations instead of treating a Windows or software-Vulkan pass as Deck evidence.
5. Explain possible regressions specific to the touched code, including pacing, input/audio, rendering correctness, memory/cache growth, startup and suspend/resume where relevant. Add targeted tests only where they verify meaningful behavior.
6. Provide exact parent/candidate commit IDs, build commands, launch/settings, save/route/camera, warm-up, duration, tools and log locations for an LCD/OLED hardware comparison. Check equivalent visual output and gameplay as well as counters.
7. Report measured results and repeat variation. If the build misses 60 FPS, state the scene and evidence for the limiting factor. If hardware is unavailable, mark the gain unverified and deliver the test recipe; do not invent results or claim success from CPU percentage alone.
8. Stop after this optimization and its validation/report. Further performance ideas are follow-up work, not permission to begin another change.
