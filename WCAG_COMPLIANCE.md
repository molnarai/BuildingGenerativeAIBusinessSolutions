# WCAG 2.1 Level AA Compliance Audit

**Site:** MSA 8700 - Building Generative AI Business Solutions
**URL:** https://msa8700.molnar.ai
**Audit Date:** April 2, 2026
**Scope:** Hugo theme `pmolnar`, all templates, CSS, and content files

---

## Current Compliance Estimate

| After Fixing | Estimated Compliance |
|---|---|
| Current state | ~40% |
| Critical issues | ~75% |
| Critical + Major | ~90% |
| All issues | ~95%+ |

---

## Critical Issues (Must Fix)

### 1. No Skip Navigation Link

**WCAG Criterion:** 2.4.1 Bypass Blocks
**Location:** `www/themes/pmolnar/layouts/_default/baseof.html`

There is no mechanism for keyboard users to skip past the navigation menu to reach main content.

**Remediation:**
Add a visually hidden skip link as the first child of `<body>`:
```html
<a href="#main-content" class="skip-link">Skip to main content</a>
```
Add `id="main-content"` to the `<main>` element, and add CSS:
```css
.skip-link {
  position: absolute;
  top: -40px;
  left: 0;
  padding: 8px 16px;
  background: #003478;
  color: #fff;
  z-index: 1000;
  transition: top 0.2s;
}
.skip-link:focus {
  top: 0;
}
```

---

### 2. No Visible Focus Indicators

**WCAG Criterion:** 2.4.7 Focus Visible
**Location:** All CSS files (`main.css`, `site.css`, `wiki.css`) — no `:focus` or `:focus-visible` styles exist

Keyboard users cannot see which element is currently focused. The theme defines hover styles for links but no focus styles anywhere.

**Remediation:**
Add to `www/themes/pmolnar/assets/css/main.css`:
```css
:focus-visible {
  outline: 3px solid #003478;
  outline-offset: 2px;
}

a:focus-visible {
  outline: 3px solid #003478;
  outline-offset: 2px;
  border-radius: 2px;
}

button:focus-visible,
select:focus-visible,
input:focus-visible {
  outline: 3px solid #003478;
  outline-offset: 2px;
}
```

---

### 3. Tables Missing Semantic Markup

**WCAG Criterion:** 1.3.1 Info and Relationships
**Locations:**
- `www/themes/pmolnar/layouts/_default/home.html` (schedule table, lines 11-36; milestones table, lines 79-88)
- `www/themes/pmolnar/layouts/assignments/list.html` (lines 13-24)
- `www/themes/pmolnar/layouts/project/list.html` (lines 16-28)

Tables are missing `<thead>`, `<tbody>`, `scope` attributes on `<th>`, and `<caption>` elements. Screen readers cannot distinguish headers from data.

**Remediation:**
Change all tables from:
```html
<table class="table">
  <tr><th>Session</th><th>Monday</th>...</tr>
  <tr><td>...</td></tr>
</table>
```
To:
```html
<table class="table">
  <caption>Class Schedule</caption>
  <thead>
    <tr><th scope="col">Session</th><th scope="col">Monday</th>...</tr>
  </thead>
  <tbody>
    <tr><td>...</td></tr>
  </tbody>
</table>
```

---

### 4. Heading Hierarchy Skips Levels

**WCAG Criterion:** 1.3.1 Info and Relationships
**Locations:**
- `www/themes/pmolnar/layouts/_default/home.html` — jumps from H1 to H3 (skips H2)
- `www/themes/pmolnar/layouts/wiki/wiki.html` — jumps from H1 to H4 for "On this page"
- Several content files start with H3 or skip from H2 to H4

**Remediation:**
- In `home.html`: change `<h3>Schedule</h3>`, `<h3>Topics</h3>`, `<h3>Resources</h3>` to `<h2>`; change `<h4>Project Milestones</h4>` to `<h3>`
- In `wiki.html`: change `<h4>On this page</h4>` to `<h2>`
- Audit content markdown files for sequential heading usage

---

### 5. Form Controls Missing Labels

**WCAG Criterion:** 1.3.1 Info and Relationships, 4.1.2 Name Role Value
**Location:** `www/themes/pmolnar/layouts/publications/publications.html` (lines 9-27)

The publication filter dropdowns (`<select id="type-filter">`, `<select id="year-filter">`) have no associated `<label>` elements or `aria-label` attributes.

**Remediation:**
```html
<div class="filter-controls">
  <label for="type-filter">Filter by type:</label>
  <select id="type-filter">
    <option value="">All Types</option>
    ...
  </select>
  <label for="year-filter">Filter by year:</label>
  <select id="year-filter">
    <option value="">All Years</option>
    ...
  </select>
</div>
```

---

### 6. Audio Content Without Transcripts

**WCAG Criterion:** 1.2.1 Audio-only and Video-only (Prerecorded)
**Locations:**
- `www/content/blog/docker-desktop-zero-to-hero.md` (lines 16-19)
- `www/content/blog/mastering-secure-shell.md` (lines 36-39)
- `www/content/podcasts/podcast-03-prompt-optimization.md` (lines 14-17)

All `<audio>` elements lack transcript links or inline transcripts. Deaf and hard-of-hearing users cannot access podcast content.

**Remediation:**
For each audio element, add a transcript link or expandable transcript section:
```html
<audio controls>
  <source src="..." type="audio/mp4" />
  Your browser does not support the audio element.
</audio>
<details>
  <summary>Read transcript</summary>
  <p>Full transcript text...</p>
</details>
```
Alternatively, link to a separate transcript page for each podcast.

---

### 7. Video Modal Not Keyboard Accessible

**WCAG Criterion:** 2.1.1 Keyboard
**Location:** `www/content/blog/mastering-secure-shell.md` (lines 63-92)

Video thumbnails use `onclick` on `<img>` elements, which are not keyboard-focusable. The modal has no focus trap, no `aria-modal` attribute, and no keyboard close handler (Escape key).

**Remediation:**
- Wrap thumbnails in `<button>` elements instead of using `onclick` on `<img>`
- Add `role="dialog"`, `aria-modal="true"`, and `aria-label` to the modal
- Trap focus within the modal when open
- Close on Escape key press
- Return focus to the triggering button on close

```html
<button type="button" onclick="openVideoModal('RfolgB-rVe8')" aria-label="Play SSH Tutorial Video">
  <img src="https://img.youtube.com/vi/RfolgB-rVe8/mqdefault.jpg" alt="SSH Tutorial Video thumbnail" />
</button>
```

---

## Major Issues (High Priority)

### 8. Breadcrumb Link Contrast on Hover

**WCAG Criterion:** 1.4.11 Non-text Contrast
**Location:** `www/themes/pmolnar/assets/css/main.css` (lines 71-98)

Breadcrumb text color `#666` on hover background `#f0f0f0` produces a contrast ratio of ~2.76:1, below the 4.5:1 minimum.

**Remediation:**
Darken the breadcrumb text to at least `#555` or remove the hover background, or darken hover text color specifically:
```css
.breadcrumbs a:hover {
  color: #333;
  background-color: #f0f0f0;
}
```

---

### 9. Table Border Contrast

**WCAG Criterion:** 1.4.11 Non-text Contrast
**Location:** `www/themes/pmolnar/assets/css/main.css` (lines 244-279)

Table border color `#ddd` on white background yields ~1.25:1 contrast, well below the 3:1 minimum for graphical UI components.

**Remediation:**
Darken table borders:
```css
.content table td,
.content table th {
  border: 1px solid #999;
}
```

---

### 10. Slide Card Placeholder Text Contrast

**WCAG Criterion:** 1.4.3 Contrast (Minimum)
**Location:** `www/themes/pmolnar/assets/css/main.css` (lines 360-361)

Placeholder text `#6c757d` on dark background `#1a1a2e` has ~3.2:1 contrast, below the 4.5:1 minimum for normal text.

**Remediation:**
Lighten the placeholder text:
```css
.slide-card-placeholder {
  color: #a0a8b4;
}
```

---

### 11. Filter Changes Provide No Status Message

**WCAG Criterion:** 4.1.3 Status Messages
**Location:** `www/themes/pmolnar/layouts/publications/publications.html` (line 74)

When publication filters change, content is dynamically updated but screen readers are not notified.

**Remediation:**
Add a live region that announces results:
```html
<div aria-live="polite" aria-atomic="true" class="sr-only" id="filter-status"></div>
```
Update it in JavaScript after filtering:
```javascript
document.getElementById('filter-status').textContent =
  `Showing ${visibleCount} publications`;
```

---

### 12. Navbar Brand Links to `#`

**WCAG Criterion:** 2.4.4 Link Purpose
**Location:** `www/themes/pmolnar/layouts/partials/menu.html` (line 16)

The site title/brand link has `href="#"` which does nothing on click.

**Remediation:**
Change to:
```html
<a class="navbar-brand" href="{{ site.Home.RelPermalink }}">{{ site.Title }}</a>
```

---

### 13. Missing `initial-scale=1` in Viewport Meta

**WCAG Criterion:** 1.4.4 Resize Text
**Location:** `www/themes/pmolnar/layouts/partials/head.html` (line 2)

Current: `<meta name="viewport" content="width=device-width">`

**Remediation:**
```html
<meta name="viewport" content="width=device-width, initial-scale=1">
```

---

### 14. Inline HTML in Content Uses onclick Without Keyboard Support

**WCAG Criterion:** 2.1.1 Keyboard
**Location:** `www/content/blog/mastering-secure-shell.md`, `www/content/topics/topic-04.md`

Inline `onclick` handlers on non-interactive elements (`<img>`, `<div>`) are inaccessible to keyboard users.

**Remediation:**
Replace with `<button>` or `<a>` elements, or add `role="button"`, `tabindex="0"`, and `onkeydown` handlers for Enter/Space.

---

## Minor Issues (Medium Priority)

### 15. Math Notation (KaTeX) Limited Screen Reader Support

**WCAG Criterion:** 1.3.1 Info and Relationships
**Location:** `www/themes/pmolnar/layouts/partials/head.html` (lines 9-12); content files using LaTeX

KaTeX renders math as HTML/CSS which has limited screen reader support. Consider adding `aria-label` attributes with text descriptions for key equations, or switching to MathJax which produces MathML output.

---

### 16. Inline Color Styles in Content

**WCAG Criterion:** 1.4.3 Contrast (Minimum)
**Location:** `www/content/topics/topic-04.md` (lines 30-42)

Inline styles like `style="color: #333;"` bypass theme-level contrast management and are harder to audit.

**Remediation:**
Replace inline styles with CSS classes defined in the theme stylesheet.

---

### 17. Generic Link Text in Resource Pages

**WCAG Criterion:** 2.4.4 Link Purpose
**Locations:** Various files in `www/content/resources/`

Some links use bare `[Link](url)` text without describing the destination.

**Remediation:**
Replace `[Link](url)` with descriptive text: `[Knowledge Graphs Tutorial by Frank van Harmelen](url)`.

---

### 18. SVG Icons Missing Accessible Labels

**WCAG Criterion:** 1.1.1 Non-text Content
**Location:** `www/themes/pmolnar/layouts/slides/list.html` (lines 20-24)

The SVG placeholder icon in slide cards has no `<title>`, `role="img"`, or `aria-label`. If decorative, add `aria-hidden="true"`; if meaningful, add `role="img"` and `aria-label`.

---

### 19. Wiki Search Function Non-functional

**WCAG Criterion:** 2.1.1 Keyboard
**Location:** `www/themes/pmolnar/layouts/wiki/wiki.html` (lines 3-12)

A `searchWiki()` JavaScript function is defined but never connected to an input element. Either implement it with a properly labeled search field or remove the dead code.

---

### 20. Commented-Out HTML in Content Files

**Location:** `www/content/blog/mastering-secure-shell.md` (lines 10-21, 43-61), `www/content/blog/ai-papers-workflow.md`

Extensive commented HTML blocks should be cleaned up. While browsers ignore them, they add noise and risk being accidentally uncommented without alt text.

---

## What Is Already Compliant

- Primary text contrast: `#222` on white (13.7:1)
- Link colors: `#00e` (8.6:1) and `#0066cc` (8.59:1) on white
- Language attribute: `<html lang="en-us" dir="ltr">`
- Breadcrumb navigation: proper `<nav>` with `aria-label="Breadcrumb"`
- Menu active state: `aria-current="page"` on active item
- Mobile navigation: `aria-expanded`, `aria-controls`, `aria-label` on toggle
- "Read more" links: include `aria-label="Read more about {{ .Title }}"`
- Image alt text: figure shortcode supports `alt` parameter
- Responsive design: mobile breakpoints at 768px
- Text spacing: adequate `line-height` and `margin` throughout
- Bootstrap 5.3.3: accessible component foundation

---

## Remediation Priority Summary

| Priority | Issues | Estimated Effort |
|---|---|---|
| Critical (1-7) | Skip link, focus indicators, tables, headings, form labels, transcripts, video modal | 8-12 hours |
| Major (8-14) | Contrast fixes, status messages, nav link, viewport, keyboard handlers | 4-6 hours |
| Minor (15-20) | KaTeX, inline styles, link text, SVG labels, dead code cleanup | 2-4 hours |

---

## Files Requiring Changes

### Theme Templates
| File | Issues |
|---|---|
| `layouts/_default/baseof.html` | #1 skip link |
| `layouts/_default/home.html` | #3 tables, #4 headings |
| `layouts/partials/head.html` | #13 viewport meta |
| `layouts/partials/menu.html` | #12 brand link |
| `layouts/publications/publications.html` | #5 form labels, #11 status messages |
| `layouts/wiki/wiki.html` | #4 headings, #19 search |
| `layouts/assignments/list.html` | #3 tables |
| `layouts/project/list.html` | #3 tables |
| `layouts/slides/list.html` | #18 SVG labels |

### Theme CSS
| File | Issues |
|---|---|
| `assets/css/main.css` | #2 focus indicators, #8 breadcrumb contrast, #9 table borders, #10 slide card contrast |
| `assets/css/site.css` | #2 focus indicators |
| `assets/css/wiki.css` | #2 focus indicators |

### Content Files
| File | Issues |
|---|---|
| `content/blog/docker-desktop-zero-to-hero.md` | #6 audio transcript |
| `content/blog/mastering-secure-shell.md` | #6 audio transcript, #7 video modal |
| `content/podcasts/podcast-03-prompt-optimization.md` | #6 audio transcript |
| `content/topics/topic-04.md` | #16 inline styles |
| `content/resources/*` | #17 generic link text |
| `content/blog/knowledge-graphs-for-agents.md` | #4 heading hierarchy |
