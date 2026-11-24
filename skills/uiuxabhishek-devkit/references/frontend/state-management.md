# State management without framework lock-in

**Use for:** shared app or user context, persisted filters, session state and complex synchronized UI.

## Choose the smallest scope that works
1. **Local component state** for one component's interaction.
2. **URL state** for anything that should survive refresh or be shareable: filters, sort, page, selected tab.
3. **Server cache** for data owned by the backend: use the project's data-fetching cache if it has one, with explicit invalidation after mutations.
4. **Shared client store or context** for cross-screen client-only state (current workspace, UI preferences).
5. **Persisted state** only when it clearly helps, with privacy reviewed.

Form state stays in the form; see [forms.md](forms.md).

## Rules
- One source of truth per fact. Copying server data into a store and editing it there creates two truths that disagree after the next fetch.
- Derive, don't store, anything computable from other state:

  ```ts
  // Bad: kept in sync by hand, drifts on the first missed update
  const [items, setItems] = useState(list); const [count, setCount] = useState(list.length)
  // Good: derived on read
  const count = items.length
  ```
- Normalize entities that several views edit (by ID), so one update reaches every view.
- Validate state read from the URL or storage: it's user-controlled and may be from an older version. Fall back to defaults on anything invalid.
- Version persisted state and migrate or drop old shapes. Give it an expiry. Don't persist tokens or personal data by default.
- Reset scoped state on sign-out and on switching account, tenant or workspace, including caches, so one user's data never shows to the next.
- When state must agree across tabs (sign-out, workspace switch), use the `storage` event or `BroadcastChannel`.

## Failure modes
- After a mutation, the list shows old data because the cache wasn't invalidated.
- An effect writes state that retriggers itself, causing a render loop.
- Subscriptions outlive their component and leak memory or update unmounted views.
- A filter stored in the URL with a renamed value crashes the page for old bookmarks.

## Verify
- Refresh, back and forward, deep links with valid and invalid parameters, sign-out and sign-in as another user, workspace switch, two tabs, offline and back online, and stored data from the previous version.
