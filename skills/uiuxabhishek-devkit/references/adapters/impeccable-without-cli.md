# Impeccable steps without its CLI

**Use for:** any loaded Impeccable file (`SOURCE_SKILL.md`, `new-work.md`, `critique.md`, `layout.md`, `typeset.md`, `polish.md`) that tells you to run a `scripts/*.mjs` command. Those scripts, Impeccable's live mode and its shipped subagents aren't bundled with this skill.

## Precedence

This adapter **overrides** any upstream wording that calls a skipped script a contract violation, a failed run or a degraded run. Here, the manual substitute below is the complete, intended path, not a fallback. Never invent script output, roll results or detector counts. In your report, name each step you replaced and how.

## Substitutes

| Upstream step | Do this instead |
| --- | --- |
| `context.mjs` (session setup) | Read `PRODUCT.md` and `DESIGN.md` if the project has them. Otherwise take the facts from the code: tokens, theme, global CSS, a representative component, and the target platform (web, iOS, Android). Say which source you used |
| `concept-seed.mjs --scope surface` | Draft the five to seven structures as instructed, then offer the **three most distinct**, not the three you like best, as equal options. The user picks one |
| `concept-seed.mjs --scope direction` | Offer two or three clearly different directions, plus the conventional category-standard option played straight. Don't recommend or rank the conventional one. Ask the user to choose before writing artifact code |
| `serve-question.mjs` (decision page) | Ask with the agent's structured question tool when it has one, otherwise as a plain chat question with numbered options. One decision per question, with each option's trade-off in a single line |
| `surface-brief.mjs read` | Look for an existing brief in `PRODUCT.md`, `DESIGN.md` or the artifact's opening comment. If there's none, say so and continue |
| `surface-brief.mjs write`, `critique-storage.mjs`, `embed-prompt.mjs` | Skip them. Keep the direction contract in the artifact's opening comment as `new-work.md` describes, and state in the report that brief storage, critique history or trends, and prompt embedding were skipped |
| `detect.mjs` (critique, layout, type, new work) | Check the target by hand against [craft-floor.md](../impeccable/reference/craft-floor.md) and the relevant checks in [audit.md](../impeccable/reference/audit.md). Report the findings as **manual review** with file and line, never as detector output |
| `live-server.mjs`, live mode, browser injection | Use a preview the user already has running, or screenshots they provide. Start the project's own dev script only in `implement` mode, in the background, and stop it before you report |
| Image generation and comps (`visualize.md`) | Not bundled. Build code-led from the locked direction and say that no comp was made |
| Shipped finish reviewer or documenter subagents | Do the finish pass yourself with `polish.md`. Update `DESIGN.md` only when the user asks (`design-system` with the document step) |

## Two-assessment critiques

`critique.md` wants its design review (A) and evidence pass (B) to run in isolation. In Claude Code with this plugin's agents, the head may run both as two parallel read-only `design-auditor` tasks (SKILL.md §5). Anywhere else, finish A completely, then do B by hand from the substitutes above, and keep the two lists separate in the report.

## Verify

- Every script step the loaded file names is either replaced from the table above or reported as skipped.
- Each choice the user had to make (direction, structure, scope) was asked, not decided for them.
- Findings say "manual review", and the report lists the steps that used a substitute.
