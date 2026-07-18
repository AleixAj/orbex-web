# Orbex — Landing page

> Static landing page for **Orbex**, a pixel-art orb-shooter puzzle for Android.
> Deployed at **[orbex.aleixaj.com](https://orbex.aleixaj.com)**.

Zero build step, zero JavaScript framework, zero runtime dependencies — just
HTML + CSS + a small vanilla `<script>` for the theme toggle, language toggle
and modals. Drop the folder on any static host and it works.

---

## What this is

A one-page marketing site + privacy policy for [Orbex](https://github.com/AleixAj/orbex),
a solo-developed Godot game. The landing has 8 sections:

1. **Hero** — logo, tagline, Play Store CTA, trailer modal.
2. **The game** — one-liner explanation with a phone mockup.
3. **10 Worlds** — 5-column grid of world crests with taglines.
4. **Features** — 6 feature cards (single-player, ranking, power-ups, etc.).
5. **Gallery** — mixed screenshot / trailer grid with lightbox.
6. **10 Languages** — grid of all localised flags.
7. **Download** — Play Store button, badge, QR.
8. **Footer** — legal/support links, socials, credits.

Plus a separate **`/privacy`** route with a full-length privacy policy template.

## Features

- 🌗 **Light / dark theme** — respects `prefers-color-scheme`, persists in localStorage.
- 🌐 **Bilingual (EN default / ES)** — toggle in the header, persisted, updates `<title>` and `<meta description>` as well as visible copy.
- ⚡ **Zero build** — no bundler, no npm, no framework. Ship the folder as-is.
- 📱 **Responsive** — mobile-first, tested from 320px up to ultra-wide.
- ♿ **Accessible** — semantic HTML, ARIA labels on all icon buttons, modals close with Escape, respects `prefers-reduced-motion`.
- 🎨 **"Light Bronze Forge" theme** — matches the game's in-app palette (parchment cream, bronze, cocoa ink, gold accents).
- 🔍 **SEO-ready** — canonical URL, full Open Graph + Twitter Card meta, `hreflang` alternates, `sitemap.xml`, `robots.txt`.

## Tech stack

Deliberately minimal:

- **HTML5** — hand-written, no templating.
- **CSS** — inline `<style>` block using CSS custom properties for theming.
- **Vanilla JavaScript** — single inline `<script>` (~120 lines) for theme/lang toggles, IntersectionObserver-based scroll reveal, hero parallax, cursor trail, modals.
- **Fonts** — [Press Start 2P](https://fonts.google.com/specimen/Press+Start+2P) + [Space Grotesk](https://fonts.google.com/specimen/Space+Grotesk) from Google Fonts.
- **No external dependencies at runtime.**

---

## Structure

```
orbex-web/
├── index.html               # landing page (EN + ES)
├── privacy/
│   └── index.html           # /privacy — legal template (EN + ES)
├── assets/
│   └── images/
│       ├── orbex-title.png  # brand wordmark
│       ├── zones/           # 10 world crest emblems
│       ├── orbs/            # 5 marble sprites
│       ├── icons/           # UI icons (map, ranking, gift, coin, chest, star)
│       ├── avatars/         # 3 character portraits
│       ├── bg/              # 3 world background photos
│       ├── flags/           # 10 language flags (Eng, Esp, Cat, Prt, Fra, Ita, Deu, Jpn, Kor, Rus)
│       └── placeholders/    # ⚠️ replace with real content before launch
│
├── robots.txt               # SEO — allows all, points to sitemap
├── sitemap.xml              # SEO — 2 URLs
│
├── _headers                 # Cloudflare Pages / Netlify: cache + security headers
├── _redirects               # Cloudflare Pages / Netlify: legacy URL redirects
├── netlify.toml             # Netlify config
├── vercel.json              # Vercel config (cleanUrls, redirects, cache headers)
├── .netlifyignore           # excludes _source/ from Netlify deploys
├── .vercelignore            # excludes _source/ from Vercel deploys
├── .gitignore
└── README.md
```

---

## Getting started

The site works with any static file server. From the repo root:

```bash
# Python (bundled with most systems)
python -m http.server 8000

# Node
npx serve .

# PHP (also fine)
php -S localhost:8000
```

Then open **http://localhost:8000/** (landing) and **http://localhost:8000/privacy/**.

Or just double-click `index.html` — the site works over `file://` too, though
`localStorage` for the theme/lang persistence needs a real HTTP origin.

---

## Deployment

The site is 100% static so any host works. Here are the three that ship
with pre-configured files in this repo.

### Cloudflare Pages

1. Dashboard → **Workers & Pages** → **Create** → **Pages** → **Connect to Git**.
2. Framework preset: **None**. Build command: *(empty)*. Output directory: **`/`**.
3. Deploy. Custom domain → add `orbex.aleixaj.com` and follow the CNAME steps.

`_headers` and `_redirects` are picked up automatically.

### Netlify

1. **Add new site** → **Import from Git** (or drag-and-drop for a manual deploy).
2. Publish directory: **`.`**. Build command: *(empty)*.
3. **Domain settings** → **Add custom domain** → `orbex.aleixaj.com`.

`.netlifyignore` keeps `_source/` (if you kept it locally) out of the deploy.

### Vercel

1. **Add New Project** → import the repo.
2. Framework preset: **Other**. Build command: *(empty)*. Output directory: **`.`**.
3. **Settings** → **Domains** → add `orbex.aleixaj.com`.

`vercel.json` handles clean URLs (so `/privacy` works without the `.html`
extension), sensible cache headers on assets, and legacy redirects.

---

## ⚠️ Placeholders to replace before launch

Search the two HTML files (`index.html`, `privacy/index.html`) for these:

### Links (`#PLACEHOLDER-*`)

| Placeholder | Replace with |
|---|---|
| `#PLACEHOLDER-play-store` | Real Google Play URL (3 occurrences in `index.html`) |
| `#PLACEHOLDER-terminos` | Terms of use page |
| `#PLACEHOLDER-borrar-cuenta` | "How to delete my account" page |
| `#PLACEHOLDER-x` | X / Twitter profile |
| `#PLACEHOLDER-github` | GitHub profile |
| `#PLACEHOLDER-itch` | itch.io profile |

### Placeholder assets (`assets/images/placeholders/`)

| Current file | Should become | Size |
|---|---|---|
| `hero-gameplay.png` | Real trailer poster | 1280×720 |
| *(missing)* `assets/videos/trailer.mp4` | Real trailer video | 1920×1080, MP4 H.264, `preload="none"` |
| `google-play-badge.png` | Official Google Play badge | ~564×168 |
| `qr.png` | Real QR pointing to your Play listing | 240×240+ |
| `og-image.png` | Open Graph / social share image | 1200×630 |
| `favicon-32.png`, `favicon-192.png` | Real favicons | 32×32 and 192×192 |
| `gameplay-1..3.png` | Real gameplay screenshots | 1280×720 |

### In `privacy/index.html`

- `[DATE]` / `[FECHA]` → real "last updated" date.
- Every `[PLACEHOLDER — …]` / `[PLACEHOLDER — …]` block → definitive legal
  text. **The current text is a structured template, not legal advice —
  have it reviewed by a professional before publishing.**

---

## Editing guide

### Copy (visible text)

All user-facing text lives in dual `<span>` tags:

```html
<h2>
  <span data-lang="en">A journey through history</span>
  <span data-lang="es">Un viaje por la historia</span>
</h2>
```

Edit the one you need. CSS (`html[lang="en"] [data-lang="es"]{display:none}`)
hides the inactive language.

### Meta title & description

Also localised — they swap via JS when the toggle is clicked. Edit the `META`
object at the bottom of each HTML file:

```js
var META = {
  en: { title: "...", desc: "..." },
  es: { title: "...", desc: "..." }
};
```

### World cards (`index.html`, section 3)

Each of the 10 `<article class="world-card">` blocks holds the crest, name and
tagline. Edit in place — accent colour is the `background:` value on the top
6-pixel band.

### Feature cards (section 4)

Each `<div class="feature-card">` has an icon + title + description. Add or
remove cards freely; the grid auto-fits.

### Gallery (section 5)

Each `<button class="gallery-card">` opens the lightbox (or the trailer modal
for the video card). Change images by editing the `src`. `grid-row:span 2`
makes a card take a double row.

### Languages section (section 6)

Card list in `.flags-grid`. Add a new `<div class="flag-card">` if you
localise the game to more languages.

### Theme colours

The Light Bronze Forge palette is defined as CSS custom properties near the
top of the `<style>` block in each HTML file. Change once, applies everywhere
in both light and dark modes.

### Adding a third language

1. Duplicate the `<span data-lang>` pairs with a third variant, e.g. `<span data-lang="ca">…</span>`.
2. Add CSS: `html[lang="ca"] [data-lang="en"], html[lang="ca"] [data-lang="es"]{display:none}`.
3. Extend `toggleLang()` in the `<script>` to cycle through 3 languages.
4. Add the new locale to the `META` object.
5. Add a flag button in the header.

For SEO on multi-language sites, prefer separate URLs (`/es/`, `/ca/`) plus
proper `hreflang` alternates — this repo currently uses a single URL with a
runtime toggle, which is simpler but ranks the alternate language less well.

---

## Technical notes

- **Language** — English by default (`<html lang="en">`), Spanish as an
  alternative via the header toggle. Both languages live in the same HTML
  via `<span data-lang="en">` / `<span data-lang="es">`; CSS hides the
  inactive one. `document.title` and `<meta name="description">` also swap
  through the `META` dict in the `<script>`.
- **Theme** — auto-detected from `prefers-color-scheme` on first visit,
  persisted afterwards in `localStorage` under `orbex-theme`. Same for
  language under `orbex-lang`. Both bootstrap **before paint** (inline
  `<script>` in `<head>`) to avoid a light-mode flash on dark-mode users.
- **Animations** — CSS keyframes for floating orbs, logo pulse, forge shift,
  scroll cue. Intersection-observer-based scroll reveal. All respect
  `prefers-reduced-motion: reduce`.
- **Modals** — trailer + lightbox use a plain hidden `<div>` with a `.open`
  class, close on click-outside or `Escape`.
- **Fonts** — Google Fonts with `display=swap`. No self-hosted fallback
  (acceptable trade-off for a landing page).
- **Accessibility** — all icon-only buttons have `aria-label`; modals have
  `role="dialog"` + `aria-modal="true"`; images are decorative
  (`aria-hidden="true"`) unless they carry meaning.
- **Browser support** — modern evergreen browsers (Chrome/Edge, Firefox,
  Safari 16+). Uses CSS `color-mix()`, `aspect-ratio` and `100svh`.

## SEO

- Full Open Graph and Twitter Card meta on both pages.
- `<link rel="canonical">` on both.
- `<link rel="alternate" hreflang="en|es|x-default">` on both.
- Static HTML: content is in the initial response, not injected after
  hydration — Google and social crawlers see everything on first fetch.
- `sitemap.xml` and `robots.txt` in the root.
- Structured `<h1>` → `<h2>` → `<h3>` hierarchy, semantic `<section>`,
  `<article>`, `<nav>`, `<footer>`.

---

## Credits

- **Game & site** — [Aleix Auqué](https://aleixaj.com) ([@AleixAj](https://github.com/AleixAj))
- **Engine** — [Godot 4.6](https://godotengine.org)
- **Fonts** — Press Start 2P (Cody "CodeMan38" Boisclair), Space Grotesk (Florian Karsten)
- **Landing page design** — starting point generated as an internal
  Design Component, converted to plain static HTML for deployment.

## License

The **code** in this repo (HTML / CSS / JS) can be reused as a reference for
building similar static landing pages. See `LICENSE` if present.

The **Orbex brand, sprites, artwork, and copy** in `assets/` are **© Aleix
Auqué** and *not* covered by any open license — please don't reuse them
outside of the Orbex project.

## Contact

- Email: aleixauque@gmail.com
- Site: [aleixaj.com](https://aleixaj.com)
- Game repo: [github.com/AleixAj/orbex](https://github.com/AleixAj/orbex) *(link if/when public)*
