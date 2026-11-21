# The family rules: what every site shares (her decision, 21 Nov 2026)

Jemma’s Journals (home), Library, Sim World, Pokédex and Travels each keep their own look and colours, but these three things work **the same on every site**. Each site’s own session follows this page.

## 1. Dark mode: the same everywhere, and it carries across

- **Every site opens light**, whatever the device or browser is set to. Dark only when she presses the button. (Do not follow `prefers-color-scheme`.)
- **The button** is in the footer, beside Back to top (see 2): a text button with a Lucide icon, reading **“Dark mode”** (moon icon) when light and **“Light mode”** (sun icon) when dark. `aria-pressed` true when dark.
- **One shared setting**: `localStorage` key **`jj-mode`**, value `"light"` or `"dark"`. Every site reads and writes this same key, so once the sites share one address online, choosing dark on one carries to all of them. (On her PC each local server is a separate address, so it can only carry once online, or between sites opened from the same server.)
- **No flash of the wrong mode:** a tiny script in `<head>`, before the stylesheet paints, reads `jj-mode` and sets `data-mode="dark"` or `"light"` on `<html>`. All dark styles hang off `:root[data-mode="dark"]`, not a media query.
- When the mode changes: update `data-mode`, save `jj-mode`, update `<meta name="theme-color">` to the site’s dark or light bar colour, and (if the site has one) swap to its dark tab icon.
- Wrap every `localStorage` read/write in try/catch; if storage is blocked, light is used.
- Keep the old per-site key working once (read it if `jj-mode` is missing, then save as `jj-mode`), so her current choice isn’t lost.

## 2. The footer: the same layout everywhere

At the bottom of every page, centred, in the site’s own fonts and colours:

```
            ── ◆ ──                     (the site’s own small divider, optional)
         Jemma’s Journals               (or Jemma’s Library, Jemma’s Sim World …: the site’s own name, in its display font, plain not italic)
  No cookies, no tracking, no ads. Made with plain HTML and CSS, kept on GitHub.
  <credit> · <credit> · <credit>        (the site’s own true credits, each starting with a capital)
       ↑ Back to top     ☾ Dark mode    (both 44px tall tap areas, level with each other)
```

- Line 1 is the same words on every site (home’s wording, her pick 20 Nov). If a site isn’t true to it (e.g. it needs a server), say so to her rather than changing the words.
- Line 2 lists only that site’s real credits, e.g. Library: “Book covers from their publishers · Fonts: Instrument Serif, Manrope and EB Garamond · Icons by Lucide”; Pokédex: “Pokémon pictures and region maps from the Pokémon games · Fonts: Instrument Serif and Manrope · Icons by Lucide”. Check each against what the site actually uses.
- On phones the credits stack one per line (no “·” at line ends).
- **Back to top** scrolls to the top and moves keyboard focus to the top of the page.
- 12.5px text in the site’s muted colour (at least 4.5:1 contrast in both modes); links/buttons in the site’s accent colour.

## 3. The menu on narrow screens: the same everywhere (sites with a sidebar)

- **At 900px wide and below**, the sidebar hides and a **slim top bar** appears: on the left a button with the Lucide `menu` icon and the word **“Menu”**, then the site’s name lockup “Jemma’s *X*” (italic second word, a link to that site’s home).
- **The drawer** slides in from the left over the page, with a dimmed scrim behind. It closes on: choosing a link, Escape, tapping the scrim. The page behind doesn’t scroll while it’s open.
- **Keyboard:** the button has `aria-expanded` and `aria-controls`; opening moves focus to the first link in the drawer; closing returns focus to the button; while closed the drawer is `inert` (Tab can’t reach it). Crossing the 900px line resets it.
- **“← Jemma’s Journals”** stays at the very top of the drawer (and at the top of the sidebar on wide screens).
- The home site has no sidebar, so no menu.

## Checks every site should run

- Opens light with the device set to dark; the footer button switches; reload keeps it; `jj-mode` is the key.
- Footer present on every page, same order, both buttons 44px tall and level.
- At 899px the Menu bar shows; at 901 the sidebar; drawer open/close by button, Escape, scrim, link; focus moves in and back; Tab can’t reach a closed drawer; no sideways scroll at 390.
