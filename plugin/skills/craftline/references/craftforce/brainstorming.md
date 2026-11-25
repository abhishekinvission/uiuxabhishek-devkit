# Brainstorming

**Use for:** turning an idea or vague request into an agreed design **before** any code is written.

## Steps
1. **Read first.** Look at the project (structure, README, recent commits, related code) so questions are informed, not generic. Don't ask what the files already answer.
2. **Ask one question at a time.** Prefer multiple choice with a recommended option. Cover: the problem and who has it, what "done" looks like, constraints (stack, deadlines, compatibility), what's explicitly out of scope.
3. **Offer 2–3 approaches** with trade-offs and a recommendation. Let the user pick or mix.
4. **Present the design in short sections** (a few paragraphs each): architecture, components, data flow, error handling, testing. Confirm each section before the next; revise when the user disagrees.
5. **Size the output:**
   - *Small* (one or two files, clear behavior): agree in chat; restate the agreed design in 3–6 bullets.
   - *Large* (several components, new data model, multi-day work): write a design doc to `docs/craftforce/specs/<yyyy-mm-dd>-<topic>.md` (or the user's path) with: goal, non-goals, chosen approach and rejected alternatives, components, data flow, error and edge cases, test strategy, open questions.
6. **Get explicit approval** ("approved", "go ahead"). Then move to [using-git-worktrees.md](using-git-worktrees.md) and [writing-plans.md](writing-plans.md).

## Rules
- YAGNI: cut features nobody asked for. Ask before adding "nice to haves".
- Don't write production code, scaffolding or commits during brainstorming. Writing the design doc file is fine in `implement` mode; committing it needs a request.
- UI parts: for user flows, briefs and wireframes use `ux-shape` ([shape.md](../impeccable/reference/shape.md)) instead of repeating its questions here; visual work routes through Craftline's Design capabilities. Brainstorming covers the whole feature; `ux-shape` covers its UI.
- If the user says "just build it", confirm the 2–3 riskiest assumptions in one message, then proceed.
