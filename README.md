# Pixel Hideout

A single-page gaming website built with plain **HTML** and **CSS**. No JavaScript, no frameworks, no build tools — just two files that you can open in any browser.

Live demo: just double-click `index.html` (or open it via any web server, see below).

---

## Table of Contents

- [Project Structure](#project-structure)
- [How It Works](#how-it-works)
- [Running the Site](#running-the-site)
  - [Option 1: Open the file directly](#option-1-open-the-file-directly)
  - [Option 2: Local web server](#option-2-local-web-server)
- [Customizing the Site](#customizing-the-site)
  - [Change the text](#change-the-text)
  - [Change the colors](#change-the-colors)
  - [Add / remove a game card](#add--remove-a-game-card)
  - [Change the stats](#change-the-stats)
  - [Update the contact email](#update-the-contact-email)
- [Page Sections](#page-sections)
- [Styling Guide (CSS Variables)](#styling-guide-css-variables)
- [Responsive Design](#responsive-design)
- [Accessibility Notes](#accessibility-notes)
- [Troubleshooting](#troubleshooting)
- [Extending the Site](#extending-the-site)

---

## Project Structure

```
goggle jules/
├── index.html   # The webpage structure and all text content
└── style.css    # All visual styling (colors, layout, fonts, effects)
```

| File        | Purpose                                                                 |
| ----------- | ----------------------------------------------------------------------- |
| `index.html` | Contains the page markup: header/nav, hero section, about section, game cards, footer, and all the text people read. |
| `style.css`  | Contains every visual rule: dark background, neon green accent, card layout, hover effects, and mobile responsiveness. |

The two files are linked together by this line at the top of `index.html`:

```html
<link rel="stylesheet" href="style.css">
```

If you move `style.css` somewhere else, don't forget to update the `href` in that line.

---

## How It Works

This is a **static website**, which means:

1. The browser loads `index.html`.
2. The browser sees the `<link>` tag and loads `style.css`.
3. CSS rules match elements in the HTML (by tag, class, or id) and style them.
4. Clicking a nav link scrolls smoothly to the matching section because each section has an `id` and each link uses `href="#id"`.

No server-side logic runs. Nothing is stored or computed — what you write in the files is exactly what visitors see.

### Anchor navigation

| Link in nav | Scrolls to section with id |
| ----------- | -------------------------- |
| About       | `#about`                   |
| Games       | `#games`                   |
| Contact     | `#contact`                 |

The smooth scrolling is enabled by `scroll-behavior: smooth;` in the CSS.

---

## Running the Site

### Option 1: Open the file directly

The simplest way — works on any OS:

- **Windows:** double-click `index.html`
- **macOS:** double-click `index.html`
- **Linux:** double-click `index.html`, or run `xdg-open index.html`

No internet connection or installation required.

### Option 2: Local web server

Running a small server is nice when you preview often or plan to add more pages. From the project folder:

```bash
# Python 3 (most common)
python3 -m http.server 8000
```

Then open http://localhost:8000 in your browser.

```bash
# Alternatively, with Node.js
npx serve .
```

Then open the printed URL (usually http://localhost:3000).

---

## Customizing the Site

### Change the text

Open `index.html` in any text editor and edit the text between the HTML tags. For example, this is the main headline:

```html
<h1 class="hero-title">The Gaming <span class="accent">Hideout</span></h1>
```

Change it to anything you like, e.g. rename it to your own nickname:

```html
<h1 class="hero-title">The Gaming <span class="accent">Cave</span></h1>
```

Everything visitors read lives in `index.html`, so all copy changes happen there.

### Change the colors

All colors are defined once at the top of `style.css` in the `:root` block:

```css
:root {
  --bg: #0d0f14;        /* page background */
  --bg-raised: #161a22; /* boxes/panels */
  --card: #1c212c;      /* game cards */
  --text: #e6e9ef;      /* main text */
  --muted: #8b93a7;     /* secondary text */
  --accent: #59ffa8;    /* highlight color */
  --accent-dim: rgba(89, 255, 168, 0.12); /* faint accent background */
  --radius: 14px;       /* corner rounding */
}
```

Want a purple theme? Just change the accent values:

```css
--accent: #b169ff;
--accent-dim: rgba(177, 105, 255, 0.12);
```

That one change updates the whole site — buttons, links, stats, card hovers, footer — everywhere at once.

### Add / remove a game card

Each game is one `<article class="card">` block in the `#games` section of `index.html`. Copy and paste a card, then edit the title, text, and tag:

```html
<article class="card">
  <h3 class="card-title">Hollow Knight</h3>
  <p class="card-text">A cute bug in a big hole, and honestly one of the best soundtracks ever.</p>
  <span class="card-tag">Masterpiece</span>
</article>
```

Cards automatically lay out side-by-side if there's room — no CSS changes needed. To remove a card, just delete its `<article>` block.

### Change the stats

The stats grid is in the `#about` section:

```html
<div class="stat">
  <span class="stat-number">47</span>
  <span class="stat-label">Games finished</span>
</div>
```

Edit the numbers and labels to match your real-life numbers (or your made-up ones).

### Update the contact email

The footer on `index.html` uses a placeholder:

```html
<a href="mailto:gamer@example.com">gamer@example.com</a>
```

Replace `gamer@example.com` with your real email address.

---

## Page Sections

| Section      | id        | What it shows                                              |
| ------------ | --------- | ---------------------------------------------------------- |
| Header / nav | &mdash;   | Sticky top bar with the logo and anchor links              |
| Hero         | `top`     | Big headline, short intro, and a call-to-action button     |
| About        | `about`   | Intro paragraph and three fun stats                        |
| Favorite games | `games` | Three cards, each with title, blurb, and a category tag  |
| Footer        | `contact` | Email link and copyright note                              |

---

## Styling Guide (CSS Variables)

The whole visual design is driven by a handful of CSS custom properties (variables). Changing a variable changes the site everywhere it's used:

| Variable         | Used for                                    | Default  |
| ---------------- | ------------------------------------------- | -------- |
| `--bg`           | page background                             | `#0d0f14`|
| `--bg-raised`    | stat boxes                                  | `#161a22`|
| `--card`         | game cards                                  | `#1c212c`|
| `--text`         | main text color                             | `#e6e9ef`|
| `--muted`        | subtitles, descriptive text                 | `#8b93a7`|
| `--accent`       | highlight color (links, buttons, numbers)   | `#59ffa8`|
| `--accent-dim`   | faint accent glow/backgrounds               | `rgba(...)` |
| `--radius`       | corner rounding for boxes and cards         | `14px`    |

Key effects you can tweak:

- `--accent` controls the neon green theme.
- The hero title glow comes from `text-shadow` on `.accent`.
- Card hover lift/glow is `.card:hover { transform; box-shadow; border-color }`.
- The button hover swaps text/background colors — see `.btn:hover`.

---

## Responsive Design

The layout adapts automatically to screen size:

- **Game cards** use `grid-template-columns: repeat(auto-fit, minmax(240px, 1fr))`, so they show three side-by-side on wide screens and stack into one column on phones.
- **Stats** do the same with `minmax(160px, 1fr)`.
- **Hero title** scales with the viewport via `font-size: clamp(2.4rem, 6vw, 4rem)`.
- A small `@media (max-width: 600px)` rule tightens nav spacing on small screens.

Try resizing your browser window to see the cards collapse from three columns to two, then one.

---

## Accessibility Notes

- Text colors were chosen to stay readable on the dark background (`--muted` vs `--bg`).
- The site uses semantic elements (`<header>`, `<nav>`, `<main>`, `<section>`, `<footer>`) so screen readers understand the page structure.
- Nav links have clear labels and skip targets.
- Hover effects are purely visual enhancements; all content is visible without hovering.

---

## Troubleshooting

| Problem                                       | Fix                                                                 |
| --------------------------------------------- | ------------------------------------------------------------------- |
| Page shows unstyled text / no colors          | `style.css` must sit next to `index.html`, or fix the `<link href>` path. |
| Nav link doesn't jump anywhere                | The target section's `id` must match the link's `href` (e.g. `#games` → `id="games"`). |
| Colors don't match the theme description       | Check the `:root` block in `style.css` was not partially deleted.    |
| Cards are one column when you want more         | Increase the `minmax` value in `.cards` (e.g. `minmax(200px, 1fr)`). |
| The design looks fine in Chrome but odd in IE  | Old IE supports little modern CSS. Use a current browser (Chrome, Firefox, Edge, Safari). |

---

## Extending the Site

The site is intentionally small and static. Common next steps:

- **Add a new section** &mdash; copy an existing `<section class="section">` block, give it a new `id`, and add a matching nav link.
- **Use Google Fonts** &mdash; add a `<link>` in the `<head>` of `index.html`, then set `font-family` in `style.css`.
- **Add images** &mdash; put image files in a `images/` folder and use `<img src="images/name.png" alt="...">`. Remember the `alt` text.
- **Add JavaScript later** &mdash; create a `script.js`, add `<script src="script.js"></script>` before `</body>`, and you can add interactivity (counters, dark/light toggle, etc.).
- **Add a second page** &mdash; create `page2.html` and link it with a normal `<a href="page2.html">`. Note: the one-page layout may need a bit of navigation rework.

---

## License

Free to use and modify. No license restrictions — personalize it and make it yours.