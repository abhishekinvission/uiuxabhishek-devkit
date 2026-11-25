# Test-driven development

**Use for:** every behavior change and bug fix written under Craftpowers. Test layer, runners and style come from the project and, for frontend code, [testing.md](../frontend/testing.md).

## The cycle
1. **RED.** Write one test for one behavior, named for what it proves. Run it. It must **fail, for the expected reason** (assertion about the missing behavior — not a typo, import error or broken setup). A test that passes immediately proves nothing: fix the test.
2. **GREEN.** Write the minimum code that makes it pass. No extra options, branches or refactors. Run it: it passes, and the rest of the suite still passes.
3. **REFACTOR.** With everything green, clean names and duplication. Run the tests again after each change.
4. Repeat for the next behavior.

## Code written before its test
If you (or an agent in this task) wrote production code before a failing test existed, don't keep it and backfill a test that was never seen failing. Set that code aside — revert your own uncommitted change for this task (`git diff` first; never touch the user's pre-existing work) or move it to a scratch note — write the test, watch it fail, then re-implement. Ask first if setting it aside would lose anything not written in this task.

## Rules
- Test behavior through the public interface, not private internals or mocks of the thing under test.
- Mock only at boundaries you don't own (network, clock, randomness), and make mocks honest about the real contract.
- A bug fix starts with a test that reproduces the bug ([systematic-debugging.md](systematic-debugging.md)).
- Don't weaken, skip or delete an existing test to get to green. If an existing test is wrong, say why and ask.
- Exceptions (state them): pure config, docs, generated code, throwaway spikes the user asked for — spikes are never merged as-is.
- Report the actual RED and GREEN output, not "tests pass".
