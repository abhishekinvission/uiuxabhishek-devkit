# Cross-platform native apps (React Native, Expo, Flutter)

**Use for:** screens and components in React Native, Expo or Flutter apps that ship to iOS and Android.

## Platform conventions
- One codebase still ships two platforms. Follow iOS conventions from [ios.md](../impeccable/reference/ios.md) and Android conventions from [android.md](../impeccable/reference/android.md) where they differ: navigation patterns, back behavior, controls, typography and haptics.
- Decide per screen whether the UI is shared with small platform tweaks or deliberately split. Default to shared.

## Navigation
- Use the project's navigator (React Navigation, Expo Router, Flutter's `Navigator`, `go_router` or similar). Don't add a second one.
- Android has a system back gesture and button, including predictive back; iOS has edge-swipe back. Both must work on every pushed screen, and modals must close with them.
- Define deep links for screens that can be opened from a notification or URL, and test cold start through a link.

## Safe areas and system bars
- Respect notches, the home indicator and rounded corners with the safe-area tools (`react-native-safe-area-context`, Flutter `SafeArea`/`MediaQuery.paddingOf`). Apply insets to the screen edges that need them, not as a global margin.
- Set status-bar style per screen so text stays readable over light and dark headers.

## Keyboard
- Keep the focused input visible: `KeyboardAvoidingView` behaves differently per platform (often `padding` on iOS; Android usually relies on `adjustResize`). In Flutter, let the scaffold resize and scroll the field into view.
- Set keyboard type, return key action and autofill hints (`textContentType`/`autoComplete` in React Native, `autofillHints` in Flutter). Dismiss the keyboard on scroll or tap outside where expected.

## Platform-specific code
- Keep splits small and close to the difference: `Platform.select` or `.ios.tsx`/`.android.tsx` files in React Native; `defaultTargetPlatform` checks or adaptive Cupertino and Material widgets in Flutter.

## Accessibility
- React Native: `accessibilityLabel`, `accessibilityRole`, `accessibilityState` and `accessibilityHint`; group related elements with `accessible`. Flutter: `Semantics`, `MergeSemantics` and `ExcludeSemantics`.
- Support the user's font scale without clipping, and keep touch targets at least 44 pt on iOS and 48 dp on Android.

## Performance
- Long lists virtualize: `FlatList` or the project's faster list with a stable `keyExtractor` and `getItemLayout` when rows have fixed height; `ListView.builder` in Flutter.
- Avoid needless re-renders: stable callbacks and memoized rows in React Native; `const` widgets and small rebuild scopes in Flutter.
- Run animations off the JavaScript thread (native driver or the project's animation library); size and cache images.

## Verify
- On both platforms, on at least one real device: back and gestures, deep links, safe areas on notched and small phones, keyboard on every form, and dark mode.
- VoiceOver and TalkBack read controls with the right names and roles; the largest font scale doesn't clip; long lists scroll smoothly in a release build.
