# Upstream relationship and synchronization

[ZeldaWWHDRecomp-Deck](https://github.com/endercodezz/ZeldaWWHDRecomp-Deck) is a separate Steam Deck-focused project based on [ZeldaWWHDRecomp](https://github.com/ZeldaWWHDRecomp/ZeldaWWHDRecomp). The original project supplied the recompilation/runtime work. This repository owns its Deck development policy, documentation and future platform defaults; it does not claim authorship of inherited work.

The foundation was inspected at inherited commit `5a8d06055906b46eed2a39c99cf24b91a7acc355`. The local checkout already had `origin` pointing to this project and `upstream` pointing to the original project. No upstream synchronization was performed during this task.

## What remains inherited

The CMake project/target names (`wwhd_recomp`, `wwhd`), `WWHD_*` variables, launcher/window naming, shared configuration/save formats, installers, recompiler, runtime, Vulkan/Metal renderers, SDL host, tools, CI/release workflows and non-Deck platforms remain inherited. They have not been globally renamed: doing so would unnecessarily complicate compatibility and imports. Automatic Deck detection/defaults remain future work.

Technical documents [how-it-works.md](how-it-works.md), [vulkan.md](vulkan.md) and [decomp-notes.md](decomp-notes.md) remain useful inherited references. The [preserved README](upstream-readme.md) retains release history, other-platform build instructions, optional tools and credits. [Historical performance notes](upstream-performance.md) retain Mac/Windows data. Their status/performance claims are not Deck evidence and may be stale relative to code; current project guidance starts at [README.md](../README.md).

## Importing changes

Synchronization is periodic and reviewed, not an automatic overwrite of Deck policy. A maintainer should:

1. Start from a clean worktree or an isolated review checkout. Record the last imported upstream commit and chosen new commit. Fetch `upstream` and inspect the range before choosing a merge or narrow cherry-picks.
2. Use a review branch such as `codex/upstream-sync-<date>`. Prefer a merge for a coherent upstream series; cherry-pick isolated generic fixes when appropriate and retain origin/author information (for example, `git cherry-pick -x`). Do not rewrite authorship.
3. Resolve Deck policy/configuration conflicts explicitly. Preserve the project's README and documentation while bringing useful upstream changes into the historical/technical references. Retain license and copyright notices, dependency licenses and original commit history.
4. Regenerate local guest code if recompiler/hooks changed. Run the inherited Linux unit and Vulkan smoke checks; evaluate gameplay, input, GamePad layout, save compatibility and suspend/resume on actual Deck hardware.
5. If runtime behavior changed, repeat matched power/frametime baselines. Record imported commit IDs, conflict decisions, dependency changes and Deck validation in the PR/release notes. A synchronization PR without hardware measurements must say so.

Do not import or publish game dumps, generated game code, keys, saves/states or shader caches. Maintain practical syncing by keeping Deck logic in a small centralized profile rather than spreading hardware checks through the runtime.

## Contributing back

Generic correctness, portability or renderer improvements may be proposed upstream when useful independently of Deck. Prepare a narrow change with its original attribution and reproducible evidence. Deck detection, handheld defaults and SteamOS policy remain in this repository unless upstream explicitly adopts them. Sending an upstream PR is a maintainer action, not an automatic part of local development.
