# Impeccable steps without its CLI

**Use for:** a loaded Impeccable file (`SOURCE_SKILL.md`, `new-work.md`, `critique.md`, `layout.md`, `typeset.md`, `polish.md`) that says to run `scripts/*.mjs`. Those scripts, live mode and Impeccable's own subagents aren't bundled.

## Precedence
This adapter **overrides** upstream wording that calls a skipped script a contract violation, a failed run or a degraded run: the substitute below is the intended path. Never invent script output, rolls or detector counts, and name each replaced step in your report.

## Substitutes

| Upstream step | Instead |
| --- | --- |
| `context.mjs` | Read `PRODUCT.md`/`DESIGN.md` if present; otherwise take tokens, theme, global CSS, a representative component and the platform from the code. Say which |
| `concept-seed.mjs --scope surface` | Draft the five to seven structures, then offer the **three most distinct** as equal options; the user picks |
| `concept-seed.mjs --scope direction` | Offer two or three clearly different directions plus the conventional option played straight, unranked. The user chooses before any artifact code |
| `serve-question.mjs` | The agent's structured question tool, or a plain question with numbered options: one decision, one-line trade-off per option |
| `surface-brief.mjs read` | Look for a brief in `PRODUCT.md`, `DESIGN.md` or the artifact's opening comment; if none, say so |
| `surface-brief.mjs write`, `critique-storage.mjs`, `embed-prompt.mjs` | Skip, keep the direction contract in the artifact's opening comment, and report the skipped storage, history and embedding |
| `detect.mjs` | Check by hand against [craft-floor.md](../impeccable/reference/craft-floor.md) and the relevant [audit.md](../impeccable/reference/audit.md) checks; report as **manual review** with file and line |
| `live-server.mjs`, live mode | Use the user's running preview or screenshots. Start the project's dev script only in `implement`, in the background, and stop it before reporting |
| Image generation, comps | Not bundled: build code-led and say no comp was made |
| Finish reviewer, documenter subagents | Do the finish pass with `polish.md`; update `DESIGN.md` only when asked |

## Two-assessment critiques
`critique.md` wants its design review (A) and evidence pass (B) isolated. With the plugin's agents, the head may run both as parallel read-only `design-auditor` tasks; otherwise finish A, then do B by hand, and keep the lists separate.

## Verify
- Every script step the loaded file names is replaced or reported as skipped.
- Every user choice (direction, structure, scope) was asked, not made for them.
- Findings say "manual review".
