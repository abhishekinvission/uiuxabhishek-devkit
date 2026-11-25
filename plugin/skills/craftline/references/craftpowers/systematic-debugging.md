# Systematic debugging

**Use for:** any bug, failing test, crash, flaky behavior or unexpected output. Find the root cause first; fix it second. No fixes during phases 1–3.

## Phase 1 — Investigate
- Read the full error, stack trace and logs. Note the exact message, file and line.
- Reproduce it reliably with the smallest command or steps. Can't reproduce → gather more data (inputs, environment, timing); don't guess.
- Check what changed: `git log`, `git diff`, recent dependency or config changes.
- In multi-layer systems (UI → API → service → data), add temporary logging at each boundary to see where the data first goes wrong. Remove it afterwards.
- Trace the bad value backwards to where it originates, not where it surfaces.

## Phase 2 — Compare
- Find similar code in the project that works. List every difference, however small.
- Read the relevant docs or reference implementation fully, not skimmed.
- Note assumptions the failing code makes about inputs, order, state or environment.

## Phase 3 — Hypothesize and test
- State one hypothesis: "X is the root cause because Y."
- Test it with the smallest possible change or experiment, one variable at a time.
- Wrong → discard it (undo the experiment) and form a new one. Don't stack fixes.

## Phase 4 — Fix
1. Write a failing test that reproduces the bug ([test-driven-development.md](test-driven-development.md)).
2. Make one change that addresses the root cause.
3. Run the new test and the full suite ([verification-before-completion.md](verification-before-completion.md)).

## Stop signs
- "Quick fix for now", "just try this", several changes at once, or fixing a symptom you can't explain → go back to Phase 1.
- **Three failed fixes** → stop. The problem is likely architectural or a wrong assumption; report what you tried and what you learned, and discuss with the user before attempt four.

Report: symptom, root cause with evidence, fix, test that proves it.
