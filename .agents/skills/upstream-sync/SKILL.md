---
name: upstream-sync
description: Import reviewed ZeldaWWHDRecomp changes while preserving Deck behavior and original authorship. Use when asked to synchronize, merge or cherry-pick upstream changes into ZeldaWWHDRecomp-Deck.
---

# Import upstream deliberately

1. Inspect git status and remotes. Expected origin: https://github.com/endercodezz/ZeldaWWHDRecomp-Deck.git; upstream: https://github.com/ZeldaWWHDRecomp/ZeldaWWHDRecomp.git. Verify the actual remote default branch rather than assuming its name. Preserve unrelated local work; use an isolated checkout or review branch if needed.
2. Fetch upstream, then inspect commits/diffs since the last import. Record the chosen source commit/range, dependency/build changes and conflicts with Deck policy before choosing an import method. Fetching does not authorize publishing changes or an upstream PR.
3. Use a deliberate merge for a coherent series or git cherry-pick -x for isolated fixes. Preserve original authorship and source provenance. Never rewrite inherited history or configure a replacement author.
4. Resolve conflicts manually after comparing both implementations. Protect Deck-specific behavior, README.md, AGENTS.md, .agents/skills/ and the stable interpolated-60-FPS policy; do not blindly replace them with upstream files. Adapt relevant upstream documentation without copying its whole project identity.
5. Preserve license/copyright notices and dependency attribution. Regenerate local guest code if the recompiler/hooks changed, keeping generated/game-derived data out of commits.
6. Build and run the relevant unit/Vulkan smoke tests from AGENTS.md. Check gameplay, controls, GamePad layout, save compatibility and suspend/resume on Deck where affected. Use deck-benchmark for imports that alter performance; report missing hardware evidence explicitly.
7. Inspect the final diff and report imported commits, conflict decisions, checks and Deck regressions/limitations. Before committing, print git config user.name and git config user.email; stop if the endercodezz identity is missing or incorrect. Follow existing user authorization for commit/push actions.

Do not mix unrelated optimizations into a sync. Generic fixes may be offered upstream as a separate maintainer action; Deck-specific policy remains here.
