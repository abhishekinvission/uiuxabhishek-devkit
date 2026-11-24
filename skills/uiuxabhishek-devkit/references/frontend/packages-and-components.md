# Shared components and publishable packages

**Use for:** extracting reusable UI components, design-system libraries and cross-project packages.

## Decide whether to extract
- Extract when two or more real consumers need the same behavior now. A component with one call site stays in the app.
- Share behavior and contract, not app specifics: no hard-coded endpoints, routes, copy or a host's private store. The host injects data, auth and callbacks.

## Component API
- Prefer composition (children and slots) over a growing list of boolean props.
- Support controlled and uncontrolled use for inputs (`value`/`onChange` and `defaultValue`), forward refs to the focusable element, and pass through unknown attributes such as `aria-*`, `data-*` and `className`.
- Accessibility is part of the contract: roles, keyboard behavior, focus management and labelling ship inside the component, so consumers can't forget them.
- Theme through design tokens (CSS custom properties or the project's token system), not hard-coded colors.

## Versioning
- Follow semver. A breaking change includes renaming or removing a prop, changing a default, changing emitted events, renaming a CSS variable or class, or changing the DOM structure that consumers style or test against.
- Deprecate before removing: keep the old prop working with a development warning for at least one minor release, and give the migration in the changelog.

## Build and publish
- Ship ESM (and CJS only if consumers need it), type declarations, `sideEffects` set correctly for tree shaking, and CSS delivered in a documented way.
- Put framework and design-system packages in `peerDependencies`. Listing them in `dependencies` gives consumers two copies.
- Include license and provenance; publish only with the user's authorization, to the registry and scope they name.

## Failure modes
- A "minor" release that renamed a prop breaks every consumer on the next install.
- Styles that rely on the app's global reset look different in another app.
- The component bundles its own copy of the framework and breaks context or hooks in the host.

## Verify
- Install the built package into a minimal consumer and use it there, not only inside the monorepo.
- Props, events, refs and keyboard behavior; theming and dark mode; SSR if consumers render on the server.
- The public API diff matches the version bump; tree shaking drops unused components.
