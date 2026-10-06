# Working on ZeldaWWHDRecomp-Deck

## Scope

- Maintainer: @endercodezz. Technical foundation: ZeldaWWHDRecomp and its contributors.
- Primary target: Steam Deck LCD/OLED, SteamOS, Linux x86-64, AMD Van Gogh-class APU.
- Main graphics environment: RADV Vulkan, Gamescope, 1280x800 / 16:10.
- Primary goal: stable 60 FPS and consistent frametimes, at the lowest practical power draw.
- Deck policy belongs here; generic fixes may occasionally be contributed upstream.
- Preserve inherited authorship, copyright notices, dependency licenses and MPL-2.0.

## Before editing

- Inspect git status, relevant code and existing skills before choosing a workflow.
- Read only the skill that applies; these files contain reusable working knowledge:
  - [deck-optimization](.agents/skills/deck-optimization/SKILL.md): one measured performance change.
  - [deck-benchmark](.agents/skills/deck-benchmark/SKILL.md): repeatable hardware comparisons.
  - [upstream-sync](.agents/skills/upstream-sync/SKILL.md): deliberate upstream imports.
- Build/run setup: [docs/steam-deck.md](docs/steam-deck.md).
- Technical references: [architecture](docs/how-it-works.md), [Vulkan](docs/vulkan.md),
  [decompilation/timing](docs/decomp-notes.md). Some inherited notes concern other platforms.
- Respect the task boundary; cleanup does not authorize beginning a runtime optimization.

## Correctness and performance

- Distinguish native 30 FPS, interpolated 60 FPS and experimental true 60.
- Use inherited interpolation as the initial 60 FPS baseline; it retains 30 Hz game logic.
- Do not describe interpolation as true 60 or casually change guest timing.
- Preserve exact guest floating-point semantics, synchronization, audio and save behavior.
- Prefer one small, measurable optimization; avoid stacked speculative changes/refactors.
- Benchmark before claiming a gain. FPS, p95/p99 frametimes and total watts matter together.
- Lower CPU usage alone is not proof of better performance or battery efficiency.
- If hardware evidence is unavailable, provide a precise test recipe and label gains unverified.
- Compare equivalent settings/image quality; report where 60 FPS cannot be maintained.
- Keep LCD/OLED, cold/warm caches and native/interpolated/true-60 results separate.
- Keep Deck defaults centralized and user-overridable; preserve behavior on other machines.
- Keep upstream syncing practical; avoid widespread hardware checks and needless renaming.

## Essential Linux commands

Requires dependencies and your own supported game dump; see the setup guide.

```sh
python3 tools/recomp/recomp.py game/code/cking.rpx build/gen
cmake -S . -B build/linux -G Ninja \
  -DCMAKE_C_COMPILER=clang -DCMAKE_CXX_COMPILER=clang++ \
  -DCMAKE_BUILD_TYPE=Release -DWWHD_RENDERER=VULKAN
cmake --build build/linux --parallel 2
ctest --test-dir build/linux --output-on-failure
WWHD_VK_VALIDATION=1 ./build/linux/wwhd --renderer-smoke
```

- For checks without game files, use the separate stub build in the setup guide.
- Smoke output must report PASS with no validation VUID errors.
- Stub/software-Vulkan checks do not establish RADV gameplay or Deck performance.
- Disable validation/captures/tracing for primary performance runs.
- Documentation-only changes need link review and `git diff --check`, not a game build.
- Never commit dumps, keys, generated game code, game-derived caches, saves or states.

## Keep skills maintained

- Maintain `.agents/skills/` over time; inspect the existing workflows first.
- When a workflow recurs, consider a reusable skill rather than another project document.
- Update outdated instructions, merge heavily overlapping skills and remove obsolete skills.
- Do not create skills for trivial one-off tasks; keep them concise and specific.
- Keep detailed reusable procedures in skills so AGENTS.md remains a small operating index.

## Git identity and completion

Before committing, print:

```sh
git config user.name
git config user.email
```

- Expected identity: endercodezz with the maintainer's configured email.
- If identity is missing or incorrect, stop before committing and tell the user.
- Do not change author configuration, invent an author or add AI co-authorship.
- Do not rewrite inherited history. Preserve original authorship during imports.
- Use a `codex/` prefix when creating a branch unless the user requests otherwise.
- Report changed files, checks, hardware evidence and any unverified claims; then stop.
