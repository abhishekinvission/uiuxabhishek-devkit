# Writing skills

**Use for:** creating or improving an Agent Skill (a `SKILL.md` with optional reference files), and testing that it changes agent behavior. To add guidance to Craftline itself, follow the repository's `CLAUDE.md` (one skill ID, routed playbooks) instead of creating a new skill.

## Treat a skill like code: test first
1. **RED — baseline.** Write 3–5 realistic task prompts the skill should handle, including at least one that tempts a shortcut (time pressure, "just do it quickly", a plausible wrong approach). Run them **without** the skill (a fresh agent or session). Record what the agent actually did wrong, in its words.
2. **GREEN — minimal skill.** Write only the instructions that fix the observed failures. Re-run the same prompts with the skill. Each failure should now be handled.
3. **REFACTOR — close loopholes.** Look for new excuses or workarounds in the transcripts; add explicit counters. Add one prompt where the skill must **not** apply and confirm it stays out.

## Structure
- **Frontmatter:** `name` (lowercase, hyphens, matching the folder) and `description` — say *when* to use it with concrete trigger words; keep it short (≤1024 characters, less is better).
- **Body:** purpose in one line, then the steps or rules. Imperative, specific, testable ("run X and read the output"), not advice ("be careful").
- **Keep `SKILL.md` small;** move long reference material into separate files and link them with the condition for loading each.
- **Scripts only when needed,** reviewed, with prerequisites stated. Never fetch-and-run remote code.

## Checklist before shipping
- Baseline failures recorded and now fixed; non-trigger case stays out.
- Every link resolves; no secrets, private data or project-specific paths in a general skill.
- Third-party content keeps its license and attribution.
- Version and changelog updated where the project tracks them.
