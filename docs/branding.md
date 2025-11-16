# Mindfolio Brand Guidelines

## Brand Philosophy

Mindfolio is a personal knowledge management system designed to help users organize, reflect on, and grow from their reading experiences. The brand identity reflects the core values of wisdom, learning, creativity, and personal growth.

## Color Palette

### Primary Colors

#### Indigo
- **Hex**: `#7C7FF1`
- **HSL**: `hsl(239, 84%, 67%)`
- **Usage**: Primary buttons, links, active states, brand elements
- **Meaning**: Wisdom, knowledge, creativity, trust
- **When to use**: Main CTAs, navigation highlights, important UI elements

#### Amber
- **Hex**: `#F59E0B`
- **HSL**: `hsl(38, 92%, 50%)`
- **Usage**: Accents, highlights, important notifications
- **Meaning**: Enlightenment, value, energy, warmth
- **When to use**: Highlighting key content, secondary CTAs, status indicators

### Light Theme

| Element | HSL Value | Hex Equivalent | Usage |
|---------|-----------|----------------|-------|
| Background | `240 20% 99%` | `#FCFCFD` | Main page background |
| Foreground | `240 10% 10%` | `#17181C` | Primary text |
| Card | `0 0% 100%` | `#FFFFFF` | Card backgrounds |
| Card Foreground | `240 10% 10%` | `#17181C` | Card text |
| Primary | `239 84% 67%` | `#7C7FF1` | Primary actions |
| Primary Foreground | `0 0% 100%` | `#FFFFFF` | Text on primary |
| Secondary | `240 5% 96%` | `#F4F4F5` | Secondary elements |
| Secondary Foreground | `240 10% 10%` | `#17181C` | Text on secondary |
| Muted | `240 5% 96%` | `#F4F4F5` | Muted backgrounds |
| Muted Foreground | `240 4% 46%` | `#71717A` | Muted text |
| Accent | `38 92% 50%` | `#F59E0B` | Accent elements |
| Accent Foreground | `0 0% 100%` | `#FFFFFF` | Text on accent |
| Border | `240 6% 90%` | `#E4E4E7` | Borders, dividers |
| Input | `240 6% 90%` | `#E4E4E7` | Input borders |
| Ring | `239 84% 67%` | `#7C7FF1` | Focus rings |

### Dark Theme

| Element | HSL Value | Hex Equivalent | Usage |
|---------|-----------|----------------|-------|
| Background | `224 71% 4%` | `#030712` | Main page background |
| Foreground | `213 31% 91%` | `#E0E7FF` | Primary text |
| Card | `224 71% 6%` | `#0F1729` | Card backgrounds |
| Card Foreground | `213 31% 91%` | `#E0E7FF` | Card text |
| Primary | `239 84% 67%` | `#7C7FF1` | Primary actions |
| Primary Foreground | `0 0% 100%` | `#FFFFFF` | Text on primary |
| Secondary | `222 47% 11%` | `#0F172A` | Secondary elements |
| Secondary Foreground | `213 31% 91%` | `#E0E7FF` | Text on secondary |
| Muted | `222 47% 11%` | `#0F172A` | Muted backgrounds |
| Muted Foreground | `215 20% 65%` | `#94A3B8` | Muted text |
| Accent | `38 92% 50%` | `#F59E0B` | Accent elements |
| Accent Foreground | `0 0% 100%` | `#FFFFFF` | Text on accent |
| Border | `222 47% 11%` | `#0F172A` | Borders, dividers |
| Input | `222 47% 11%` | `#0F172A` | Input borders |
| Ring | `239 84% 67%` | `#7C7FF1` | Focus rings |

## Typography

### Font Family
- **Primary**: Inter
- **Fallback**: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif

### Font Weights
- **Light**: 300
- **Regular**: 400
- **Medium**: 500
- **Semibold**: 600
- **Bold**: 700

## Design Principles

### 1. Clarity Over Complexity
The interface should prioritize readability and ease of use. Content is king.

### 2. Thoughtful Contrast
Both light and dark themes maintain WCAG AA compliance for text contrast ratios.

### 3. Purposeful Color
- **Indigo** is reserved for primary actions and brand elements
- **Amber** draws attention to important content and highlights
- Neutrals provide the foundation for content to shine

### 4. Consistent Spacing
Use the radius value of `0.5rem` for consistent rounded corners throughout the interface.

## Usage Guidelines

### Primary Buttons
Use indigo (`primary`) for the most important action on a page.
```html
<button class="btn btn-primary">Add Book</button>
```

### Accent Elements
Use amber (`accent`) sparingly for:
- Important highlights
- Featured content
- Status indicators that need attention
- Secondary calls-to-action

### Cards
Cards use a subtle elevation with `shadow-sm` and maintain the card background color.
```html
<div class="card">
  <div class="card-header">
    <h3 class="card-title">Title</h3>
  </div>
</div>
```

## Accessibility

### Contrast Ratios
All color combinations meet WCAG 2.1 Level AA standards:
- Normal text: minimum 4.5:1
- Large text: minimum 3:1
- UI components: minimum 3:1

### Focus States
All interactive elements include visible focus indicators using the `ring` color with a 2px width.

## Theme Implementation

### CSS Variables
Colors are implemented using CSS custom properties in HSL format for easy theming:

```css
:root {
  --primary: 239 84% 67%;
}

.dark {
  --primary: 239 84% 67%;
}
```

### Usage in Tailwind
Colors are referenced through Tailwind utilities:
```html
<div class="bg-background text-foreground">
  <button class="bg-primary text-primary-foreground">Click me</button>
</div>
```

### JavaScript Theme Toggle
Theme preference is stored in localStorage and defaults to dark mode:
```javascript
const theme = localStorage.getItem('theme') || 'dark';
```

## File Locations

- **CSS Source**: `static/src/input.css`
- **Tailwind Config**: `tailwind.config.js`
- **Base Template**: `templates/base.html`
- **Compiled CSS**: `static/css/output.css`

## Updates and Maintenance

When updating brand colors:
1. Edit `static/src/input.css` for both `:root` and `.dark` selectors
2. Run `npm run build:css` to rebuild Tailwind CSS
3. Run `python manage.py collectstatic` to deploy changes
4. Update this documentation to reflect any changes
