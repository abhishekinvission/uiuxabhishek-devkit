# Figma to code

**Use for:** implementing a Figma frame, component or flow in an existing codebase, or producing an implementation spec from one.

## Read the design
- With a Figma MCP connected, read the frame's design context, variables (tokens), components and auto-layout, plus a screenshot for reference. Follow that server's own instructions for its tools.
- Without one, work from screenshots, exported specs or token files the user provides, and say the values came from images.
- **Never invent values** the design doesn't specify (spacing, color, breakpoints, copy, behavior). Ask, or list them as open questions.

## Map to the project, in this order
1. **Tokens.** Match Figma variables to the project's tokens by name, then by value. Use an existing token only when it carries the same intent. Report every value with no matching token instead of hard-coding it silently.
2. **Components.** Use the project's existing component when it fits, through Code Connect mappings if the project has them. Create a new component only when none fits, and say so.
3. **Layout.** Translate auto-layout to flex or grid:

   | Figma | Code |
   | --- | --- |
   | Direction, gap, padding, alignment | `flex-direction`, `gap`, `padding`, `align-items`/`justify-content` |
   | Hug contents | Size to content |
   | Fill container | `flex: 1` or `width: 100%` |
   | Fixed width | A fixed or max width, only if the design means it |

4. **Type and assets.** Use the project's type scale and fonts. Use icons from the project's existing set when they match.

## Responsive intent
- Read constraints (left/right, scale, center), min and max widths, and any frames per breakpoint.
- With only one frame, ask how it should adapt, or follow the project's breakpoints and mark the behavior as inferred.

## States the design leaves out
List hover, focus, active, disabled, loading, empty, error, long-text and overflow states the file doesn't show, and hand them to `harden` instead of improvising them.

## Assets
- Export icons as optimized SVG that uses `currentColor` where it should follow the text color. Export images at 1× and 2× or in a modern format with explicit width and height, and give them real alt text.
- Don't ship a screenshot of a component as an image in place of code.

## Spec output (read-only work)
When the task is a spec for someone else to build, return: frames and nodes read, a token mapping table (Figma → project, with gaps), a component mapping (Figma → existing or new), layout and responsive rules, assets to export, the states missing from the design, and open questions.

## Verify
- Compare the rendered result with the frame at the same viewport sizes (side by side or overlaid) and list remaining differences with their cause.
- No hard-coded value has an existing token; new components are justified; keyboard, focus and contrast pass for the implemented states.
