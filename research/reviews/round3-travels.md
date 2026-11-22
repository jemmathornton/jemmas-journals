# Review, round 3: Jemma’s Travels (22 Nov)

This review was read-only. Nothing in any repo was changed apart from this report: `git status` in `travels/` was clean before and after, and Jemma’s Journals was clean except for this new file. Reviewed at Travels commit **9060727** (“Repo renamed to travels”), with no uncommitted work. My checks never POSTed to any server: they ran with POST requests blocked. Her test suite’s Write-page tests post to their own throwaway copy of serve.py, as designed.

**How:** the family server, http://localhost:8050/travels/. The save server on 8041 was off, as is normal. Pages checked: home, trips, trips by country, a year, three trip pages (Japan, NYC and Nashville, Brazil and Argentina), two posts (Japan day 1, Italy template 5), map, two countries (JP, ES), a continent (Europe), stats, timeline, search, Write and Not found. Each was checked at 1600, 1280, 1000, 950, 901, 899 and 390 wide, in light and dark, with the device set to the opposite scheme. That is 252 page loads in Edge through Playwright. Extra checks:
- drawer at 899 and 390;
- crossing 900px with the drawer open;
- the `jj-mode` round trip and moving the old `jt-mode` over;
- storage blocked;
- the Journals link over http and as a `file://` page;
- the Write page with no save server;
- odd addresses;
- 320 wide.

Her test suite was run too (result at the end).

**Screenshots:** `C:\Users\Jemma\AppData\Local\Temp\claude\9cff366c1b60a8f8\2df2d807-e7a9-4322-8b41-c4059cb2ba00\scratchpad\review3\travels\`:
- `mode-width-page.png`: full page for home, Japan trip, map, stats and the Italy post at 1600 and 390;
- `drawer-open-899.png`, `drawer-open-390.png`;
- `zoom-sidebar-2026.png`, `zoom-search-focus.png`, `write-family-server.png`.

Raw results are one folder up: `travels-r3.json`, `travels-r3-extra.json`.

## What passed

- **No console errors, page errors or failed requests** on any of the 252 loads. **No requests to other sites. No broken images.**
- **No sideways scroll** at any of the seven widths, in either mode, on any page. None at 320 either (home, stats, map, Write, a trip).
- **No text below 4.5:1** anywhere in dark mode. In light mode the only text below 4.5:1 is the footer’s decorative “·” (see Looks).
- **21 Nov changes are all in:**
  - **Favourite month** is gone from Stats.
  - **Footer line 1** is exactly “No cookies, no tracking, no ads. Made with HTML, CSS and JavaScript, kept on GitHub.” on every page.
  - **Distance** on each trip page: “Distance 18,850 km from Birmingham and back, as the crow flies” (Japan). NYC and Nashville is 13,230 km, Brazil and Argentina 22,690 km.
  - The site’s own labels (sidebar, headings, notes, footer, Write page) have no “you”/“your”. The exception is the placeholder post text: see Should fix 3.
- **Round-2 fixes held:**
  - The map tracker stacks at 901–1000, so no 0px bars and no sideways scroll.
  - `#/trip/constructor` and `#/country/constructor` are Not found.
  - Japan is framed whole on its country page.
  - Month cells, stamps, the banner and sidebar counts pass contrast in both modes.
  - “Written so far” is 0 posts (placeholders left out).
  - The sidebar search box has a 2px solid accent focus ring.
  - The drawer opens to the page’s own link (Home on Not found and Search).
  - With the drawer open, the top bar, skip link and page are inert. Tab stays in the drawer, apart from the browser’s own stop.
  - The scrim is black 45% in light mode.
  - The bar name is 26px and the Journals link is 32px tall.
  - At 901 the credits wrap with no stray “·”.
- **“← Jemma’s Journals”:**
  - Over http it is `/` and lands on http://localhost:8050/ (“Jemma’s Journals”).
  - As a file it becomes `file:///C:/Users/Jemma/Documents/JemmasJournals/site/index.html` and lands on Jemma’s Journals. The C-drive listing problem is gone.
- **Write page as a file:** it says to start the server, and Save is disabled.
- **Asset fingerprints** in `site/index.html` match the files (sha1 of the checked-out files).
- **Old names:** nothing in the code, tests or tools points at `Documents\Travels` or `jemmas-travels`. The remote is `github.com/jemmathornton/travels`, and so is `.gitmodules` in the parent. Only the notes still use the old names (Should fix 5).

---

## Broken

1. **On the family server, the Write page looks ready to save for about 4 seconds when the Travels save server is off.**
   - Where: http://localhost:8050/travels/#/write.
   - What happens:
     - `wireWrite` (`site/js/app.js:434-435`) asks `api/ping`, and `tools/serve_all.py` passes it on to `http://localhost:8041`.
     - On Windows, `localhost` is tried as `::1` first, and the refusal takes about 2 seconds per address. So the 503 only arrives after **about 4.4 s** (measured with curl and in Edge).
     - Until then, the page shows the normal “This page only exists on this computer…” note and **Save is enabled**.
   - Evidence: `write-family-server.png`, taken 1.2 s after opening, shows Save enabled. The probe still showed it enabled at 4.0 s, and the 503 came at about 4.3 s.
   - What she would see: if she presses Save in that window, the POST also gets a 503 *HTML* page. `res.json()` then throws, and the message reads “Not saved: SyntaxError: Unexpected token '<'…”.
   - The same delay hits every save and ping through 8050 when the server *is* running, because serve.py listens on 127.0.0.1 only.
   - Fix:
     - In the parent: `serve_all.py` `forward()` should use `http://127.0.0.1:{port}`, not `localhost`.
     - In Travels: start with Save disabled until the ping answers `ok`. Check `res.ok` and the content type before `res.json()`, and say “The Travels server isn’t running” on a 503.

2. **An address with a broken % code crashes the page, and the old page stays on screen.**
   - Example: `#/search/%E0%A4%A` (also `#/trip/%`).
   - What: `render()` (`app.js:544`) and `navRoute()` (`app.js:535`) call `decodeURIComponent` without a guard. The page error is “URI malformed”, nothing is drawn, and the address no longer matches the page. It can only be reached by typing or by a bad link.
   - Fix: wrap the decoding in a function that returns null on error and show Not found. Add the address to the Not found test.

## Should fix

3. **The placeholder posts talk to “you”, and they show on the public pages.**
   - Where: Italy templates `data/posts/italy-2026/*.md` and Japan `data/posts/japan-2024/*.md`. Examples:
     - “Where you were”
     - “Your title for day 1”
     - “Your notes go here… so you can see how the words wrap…”
     - “A caption, if you want one”
     - “Your notes for this day go here, in your own words.”
   - Where it shows: home’s Latest posts, every trip page, the posts, and the **tab title** (“Your title for day 1 · Jemma’s Travels”).
   - Why it matters: this is not her writing. It is the site’s own stand-in text, so it falls under her 21 Nov “neutral, not addressed to you” rule. The tests didn’t catch it because they skip post text.
   - Fix: reword to neutral stand-ins, e.g. “Place”, “Title for day 1”, “Notes for this day”, “Caption”. Or ask her whether templates count as her posts.
4. **Addresses with extra parts aren’t Not found.**
   - These still show a page: `#/year/2024/x` shows 2024, `#/stats/x` shows Stats, `#/timeline/x` shows Timeline, `#/trip/japan-2024/01/x` shows the post.
   - `#/map/x` and `#/trips/x` already give Not found, so this is inconsistent and lets bad links look fine.
   - Fix: in `render()`, refuse routes with more parts than each page takes.
5. **The notes are out of date after the move:**
   - `travels/CLAUDE.md:3` says “its own repo is unchanged on GitHub”, but it was renamed to `travels`.
   - `:30` still names the repo `jemmas-travels`.
   - `:42` says the file-mode Journals link goes to `../../JemmasJournals/concepts/index.html`. The code (`app.js:623`) uses `../../site/index.html`, which is correct.
   - `:47` (the 21 Nov phone-menu decision) says “tap outside, **×** or Esc to close”, but there is no × in the drawer any more (the family rules don’t ask for one).
   - `for-jemma/writing-options.md:25` suggests a folder `Documents\Travels\new-posts`.
   - Parent `CLAUDE.md` still describes the home page at `concepts/`.
6. **The local servers still don’t check the Host header** (round 2, item 16, not done). It matters a little more now, because `serve_all.py` (port 8050) passes the `X-Travels` header and the POST on to 8041.
   - The risk: a DNS-rebinding page would count as same-origin on 8050 and could save a post while both servers run.
   - Fix: both servers should refuse requests whose `Host` isn’t `localhost:<port>` or `127.0.0.1:<port>`. `serve_all.py` should also refuse POSTs whose `Origin` isn’t its own.
7. **Code quality**, small:
   - Inline `onclick`/`onsubmit` handlers in generated HTML: the skip link (`index.html:19`), both search forms (`app.js:486`, `:529`), and the by-country chips (`app.js:236`). They block a strict Content-Security-Policy once online, and they are easy to replace with delegated listeners.
   - `app.js:614-619` fetches `index.html` on every page change on her PC. That is fine locally, but it doubles requests while she browses.
   - Km rounding differs by page: the Timeline says “about 18,800 km” (`app.js:481`, nearest 100), while the trip page says “18,850 km” (nearest 10) for the same trip. Use `fmtKm` on both.
   - The tests’ `WIDTHS` (`tests/e2e/run.js:12`) still don’t include 899/901 for the page sweeps. They are covered only by the family tests.

## Looks (list only, for her)

- Sidebar: long trip names are cut with “…” and have no tooltip, e.g. “Norway, Denmark and …” (`zoom-sidebar-2026.png`). Options: wrap onto two lines, or add a `title`.
- Trip pages at 901–1000: the trip map is small (about 290px) beside the title, so Japan is a speck at the right edge (`light-901-trip-japan.png`). The Distance line wraps as “Distance 18,850 km” / “from Birmingham and back, as the crow flies”.
- Footer “·” separators are 3.76:1 in light mode (decorative and hidden from screen readers, so it is not a rule break).
- Map tooltips (hover on a country you haven’t visited) use Natural Earth’s short names with a straight apostrophe: “Côte d'Ivoire”, “Dem. Rep. Congo”, “Bosnia and Herz.”, “S. Sudan”.
- In dark mode the scrim is a deep blue at 60% (`site.css:387`), not black at 45% like the family rule. It looks fine, but it differs from the other sites.
- Home is still long on phones (every trip again under Trips by year). She chose to keep it.

## Family rules

| Rule | Travels |
|---|---|
| Opens light with device dark | ✔ (`data-mode="light"`, `jj-mode` unset) |
| Footer button switches, `aria-pressed`, label/icon swap | ✔ Dark mode/moon ↔ Light mode/sun; `aria-pressed` false/true |
| Shared key `jj-mode`, carries across | ✔ Set dark on Travels: Journals, Library, Pokédex and Sim World on 8050 all opened dark |
| theme-color follows | ✔ #ECF1EA ↔ #15212C |
| Old `jt-mode` moved once and removed | ✔ |
| Storage blocked | ✔ no errors, button still works for the visit |
| `data-mode` always set | ✔ |
| Footer layout, line 1 wording, own credits, 12.5px | ✔ (credits: Photos are my own · Country shapes from Natural Earth · Fonts: Instrument Serif and Manrope · Icons by Lucide) |
| Credits stacked on phones, no “·” at line ends | ✔ (≤600px one per line; `&nbsp;·` + balance above) |
| Back to top / Dark mode 44px and level | ✔ 44/44, 0px apart, every page and width |
| Back to top scrolls and moves focus | ✔ scrollY 0, focus `#view` |
| Menu bar at ≤900, sidebar at 901 | ✔ |
| Menu 44px, name 26px, `aria-expanded`/`aria-controls` | ✔ |
| Drawer focus to page’s link (Home if none) | ✔ |
| Closes on link, Esc, scrim; focus back | ✔ (Esc/scrim → Menu; link → `#view`; Trips opener also closes it) |
| Inert when closed / everything else inert when open | ✔ |
| Page behind locked | ✔ (`overflow:hidden` on html) |
| Crossing 900 resets | ✔ (back to 899: focus on Menu) |
| Scrim black ~45% | ✔ light; dark uses blue 60% (see Looks) |
| “← Jemma’s Journals” at top, ≥24px | ✔ 32px |
| robots `noindex, noai, noimageai` | ✔ |
| Local fonts only | ✔ six woff2 in `site/fonts/`, OFL files beside them; no outside requests |

## Shared-code notes (how Travels does it now, for moving into Jemma’s Journals)

**Dark mode**
- Head script: `site/index.html:15`, inline and before the stylesheet (line 16). It:
  - reads `jj-mode`;
  - if that is missing, reads `jt-mode` and copies it over;
  - always removes `jt-mode`;
  - sets `data-mode` on `<html>`, and theme-color to `#15212C` when dark;
  - on any error, sets `data-mode="light"`.
- Default theme-color: `<meta name="theme-color" content="#ECF1EA">`, `index.html:8`.
- Button markup: `index.html:38`, `<button class="mode-btn mode-text" id="modeBtn" type="button" aria-pressed="false"><span class="ico"></span><span class="txt">Dark mode</span></button>`.
- JS, `site/js/app.js:577-588`:
  - `BAR = {light:"#ECF1EA", dark:"#15212C"}`;
  - `setMode(m, save)` sets `dataset.mode`, saves `jj-mode` (try/catch), swaps `.ico`/`svg` for `icon("sun"|"moon")`, sets `.txt` and `aria-pressed`, and updates theme-color;
  - `#modeBtn` onclick toggles;
  - an init call without saving.
- Icons come from `ICONS` in `site/js/icons.js` (Lucide inline SVG strings).
- CSS:
  - `.mode-btn` is at `site/site.css:374-375`;
  - all dark styles are `:root[data-mode=dark]` variable overrides at `site.css:376-385`, plus per-component overrides at `:386-395`, `:473`, `:491-492`;
  - there is no `prefers-color-scheme` anywhere.
- To share: the head script and `setMode` become generic with two per-site settings (old key and bar colours). Each site keeps its own `:root[data-mode=dark]` variables.

**Footer**
- Markup is static in `site/index.html:35-38`, inside `<main>` after `#view`. The structure:
  - `<footer class="foot" id="foot" role="contentinfo">` holds `<b class="foot-name">`;
  - then `<div class="about-site">` with two `<p>`. The second is `<span class="cr">…</span><span class="sep" aria-hidden="true">&nbsp;·</span> <span class="cr">…</span>…`;
  - then `<div class="foot-links">` with the two `button.mode-btn` elements (`#topBtn.totop`, `#modeBtn`).
- CSS:
  - `.foot`, `.foot-name`, `.about-site`, `.cr`, `.sep`: `site.css:60-65`;
  - `.foot-links` and 44px buttons: `:424-426`;
  - phone stacking (≤600px, `.sep` hidden, `.cr` block): `:427-430`;
  - print hides it: `:449`.
- The per-site part is only the name, the credits and the colours (`--muted`, `--accent`, `--brand-em`, `--line`, `--serif`).

**Back to top**
- Markup: `#topBtn`, `index.html:38`.
- JS: `app.js:572` puts in the `arrow-up` icon. `app.js:574` scrolls to top (smooth unless reduced motion), then `#view.focus({preventScroll:true})`. `#view` has `tabindex="-1"` (`index.html:33`).

**Menu drawer**
- Markup:
  - `index.html:21`: `.topbar#topbar` with `button.menu-btn#menuBtn[aria-expanded=false][aria-controls=side]` (icon span `#menuIco`, then “Menu”) and `a.brand-bar` (“Jemma’s <em>Travels</em>”);
  - `index.html:22`: `.scrim#scrim`;
  - the drawer is the sidebar `header.side#side` (`index.html:24-30`), with `.home-link` at the top of `.side-top`;
  - the skip link is `index.html:19`.
- JS, `app.js:591-611`:
  - `NARROW = matchMedia("(max-width: 900px)")`.
  - `setMenu(o, back)`:
    - toggles `body.menu-open` and `html.nav-lock`;
    - sets `aria-expanded`;
    - sets `#side.inert = narrow && !o`;
    - sets `#main`, `#topbar` and `.skip` inert while open;
    - on open, focuses `#nav a.on`, or failing that `#nav a[href="#/"]`;
    - on close with `back`, focuses `#menuBtn`.
  - The button toggles; the scrim closes; a window keydown for Escape closes.
  - `NARROW` change resets the drawer and refocuses Menu if focus was inside.
  - Links close it because `render()` calls `setMenu(false)` (`app.js:564`) and then focuses `#view` (`:565`). This depends on a hash router. Sites without one need a click listener on drawer links.
- CSS:
  - `.topbar{display:none}` at `site.css:48`, `.scrim{display:none}` at `:55`.
  - Everything else is in `@media (max-width: 900px)` at `site.css:306-324`:
    - top bar sticky, 58px, the site’s grid background;
    - `.menu-btn` 44px;
    - `.brand-bar` 26px;
    - `.side` fixed, `width:min(300px,84vw)`, `translateX(-104%)` with `visibility` delayed for the slide;
    - `.menu-open .side` shown;
    - `.menu-open .scrim` `rgba(0,0,0,.45)`;
    - `.nav-lock{overflow:hidden}`.
  - Reduced motion: `:353`. Dark scrim override: `:387`.
- To share: `setMenu` needs four hooks (drawer, button, scrim, the elements to make inert), plus the current link’s selector.

**Journals link**
- `index.html:26`: `<a class="home-link" href="/">`. `app.js:623-624` swaps it to `../../site/index.html` when `location.protocol === "file:"`. CSS: `site.css:43-44`.

## Tests result

`python -B -X utf8 tests/run_tests.py` in `travels/`: **92 tests, all OK** (658 s). It ran on throwaway copies, and `git status` in `travels/` was clean afterwards.

Gaps that let this round’s items through:
- the Not found test doesn’t try a broken `%` code or extra address parts (Broken 2, Should fix 4);
- the wording test skips post text, so the placeholder “you” got through (Should fix 3);
- the Write-page tests run serve.py directly, never through `serve_all.py` with the save server off (Broken 1).
