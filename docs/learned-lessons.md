# Learned Lessons

## Header spacing in flex layouts
- When a nav cluster sits inside the same flex row as other elements (logo, search, actions), simply adding Tailwind margin utilities to that cluster might not work because the parent flex alignment will collapse the gap.
- Reserve space intentionally by giving the logo cluster padding or by wrapping the nav links in their own container with padding/margins/borders so the spacing is structural, not just utility-based.
- After structural spacing is in place, Tailwind utilities behave predictably and design tweaks become easier to reason about.
