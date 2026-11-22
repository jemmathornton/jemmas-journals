# Review, round 3: home, the family, and the 21 Nov move (22 Nov 2026, just after midnight)

This was a read-only review. I changed nothing in any repo: `git status` was clean in the parent and all four submodules at the start, and they are still clean (see "Moving target" below). I made GET requests only. The Playwright run blocked every non-GET request, and none was attempted. I did not change any scheduled task or shortcut.

**How:** Edge (Playwright from the parent's `node_modules`) through the real `http://localhost:8050` (`tools/serve_all.py`, pid 658860), with the real app servers behind it: Library 8020 and Pokédex 8030 were running, Travels 8041 was **not** running. I tested home at 1600, 1280, 1000 and 390 wide, in light and dark. Dark mode was pressed on each of the five sites, and then the other four were opened. Footers were checked on all five at 1600 and 390, light and dark. The Menu drawer was tried on the four apps at 899 and 901 wide. `serve_all.py` was probed with curl (traversal, encodings, Host header, odd requests), plus one temporary copy on port 8059 to read its error output. That copy is now stopped.

**Pictures and raw data:** `C:\Users\Jemma\AppData\Local\Temp\claude\9cff366c1b60a8f8\2df2d807-e7a9-4322-8b41-c4059cb2ba00\scratchpad\review3\family\`
- `footers-1600-light.jpg`, `footers-1600-dark.jpg`: the five footers stacked
- `footers-390-light.jpg`, `footers-390-dark.jpg`: the five footers side by side
- `shots\home-<width>-<mode>.png` (full page), `shots\404-*.png`, `shots\home-8040-toast.png`, `shots\drawer-<app>-899.png`, `shots\bar-<app>-899.png`, `shots\foot-*.png`
- `results.json`, `r3.js` (the script)

**Moving target:** another session was building the shared code while I worked. `site/family/` appeared, `site/index.html` and `404.html` were edited, and then everything was committed as **b869397** ("The family's shared code in site/family/ …"). So the home findings are for the version committed before that (**da9233b**), which my script served at the same address. `tests/check_page.js` failed during the edit, waiting for `[data-mode-btn]`, because that edit renamed the button's attribute to `data-jj-mode`. b869397 also changes `check_page.js`, so run it again on the new version. I re-checked b869397 for the two big home findings (no doctype, no viewport), and **both still apply**. `serve_all.py` did not change. The four apps did not change during the review. One other file appeared in the parent: `research/reviews/round3-travels.md`, from the Travels reviewer. As I finished, another session had already started acting on this review: `tools/serve_all.py` is modified (uncommitted) to forward to `127.0.0.1` (Should fix 1). Nothing else in it has changed yet, so Broken 2 and Should fix 2–7 still apply.

---

## Broken

1. **Home has no `<!doctype html>` and no `<meta name="viewport">`, so through 8050 (and online) it opens in quirks mode, and phones show the desktop layout shrunk down.** `site/index.html` is still an artifact fragment: it starts with `<meta charset>`, then has only `claude:viewport-fit-sides`. Until now that was hidden, because the checks and the artifact wrap it in a skeleton. `serve_all.py` serves the file as it is.
   - Measured on 8050: `document.compatMode` is `BackCompat` at every width.
   - At 390 on a phone, the layout width is **980px**. The four places sit 2 × 2, the credits don't stack, and all the text is tiny (`shots\home-390-light.png`, `footers-390-light.jpg`).
   - Also no `<html lang="en-GB">`.
   - Still true in b869397. The 404 page is fine (it has a doctype, viewport and lang).
   - Fix: give `index.html` a real skeleton. Check that the artifact publish still works with one, or keep a wrapped copy for the artifact.
2. **`serve_all.py` gets round the apps' own "only this computer's names" check (DNS rebinding).** The Library (`host_ok`, all requests) and the Pokédex (`host_ok` on `/api/`) refuse a request whose `Host` isn't `localhost`/`127.0.0.1`. `serve_all` forwards to `http://localhost:<port>`, so urllib writes a fresh, valid Host, and it has no Host check of its own. Tested with GET only:
   - `Host: evil.example:8050` → `/pokedex/api/collection` **200** (direct to 8030: 403)
   - `/library/` **200** (direct to 8020: 403)
   - `/library/api/reading-status` with `X-Library: 1` **200**

   A web page whose name is pointed at 127.0.0.1 becomes "same site" and can send the `X-Pokedex`/`X-Library`/`X-Travels` headers, so it could POST ticks, books or posts through 8050. (Travels has no Host check even on its own port, so this was already open for Travels.) Fix: in `serve_all`, refuse any request whose Host isn't `localhost:8050` or `127.0.0.1:8050` (one check at the top of `do_GET`/`do_POST`/`do_HEAD`).

## Should fix

**serve_all.py**
1. **Every forwarded call waits about 2 seconds.** `forward()` uses `http://localhost:{port}`. On Windows, `localhost` tries `::1` first and the apps listen only on 127.0.0.1, so each `/api/` call stalls about 2.06s before falling back. Measured:
   - `/pokedex/api/collection`: 2.07s through 8050, 0.005s direct
   - `/library/api/`: 2.06s
   - `/travels/api/`: 4.1s, then 503

   Library and Pokédex take about 3.3–3.6s to open through 8050, against about 1.2–1.4s for the static sites. Fix: forward to `127.0.0.1`. That also keeps the Library's Host check happy, because it accepts `127.0.0.1:8020`.
2. **A malformed request crashes the handler.** A request line such as `GET / HTTP/9.9` or a 70 KB URL makes `send_error()` call the overridden `end_headers()`, which calls `self.split()` before `self.path` exists: `AttributeError: 'Handler' object has no attribute 'path'`. A traceback is printed and the connection is dropped with no reply (confirmed on a temporary copy on port 8059). It only affects odd requests, but it's a two-word fix: `getattr(self, 'path', '')`, or guard in `end_headers`.
3. **Unknown addresses get Python's bare "Error response" page, not `site/404.html`** (`/no-such-page`, `/library/no-such-page`). Online, GitHub Pages will use 404.html. Locally it would be nice to send `site/404.html` with status 404.
4. **Folder listings are switched on:** `/family/`, `/img/` and `/library/covers/` list their files. This is only local, but it is unlike how the sites will be online. Suggest answering 404 for a folder without an `index.html`.
5. **Headers:**
   - Only Content-Type and Cache-Control come back from an app. `Content-Disposition`, `Location`, `ETag`, `Retry-After` and so on are dropped. No app uses them today, so this matters only if one does later.
   - Going out, `Origin`/`Referer` aren't passed. That's fine for now, because no app checks them.
   - The query is dropped on the `/library` → `/library/` redirect.
   - PUT/DELETE answer 501. None of the apps uses them today.
6. **Travels saves don't work through 8050 unless its server is started by hand.** Port 8041 wasn't running, and nothing starts it: no Startup shortcut, no launcher like the Pokédex's `open_app.pyw`. The Write page through 8050 gets a 503 after about 4s.
7. **Port 8041 is claimed twice.**
   - The parent's launch config `sims-view` runs `http.server 8041 --directory sim-world/site`. Travels' `serve.py` (and its `travels` launch config) uses 8041. If `sims-view` is running, Travels can't start, and 8050 then forwards Travels' `/api/post` to a static Sim World server.
   - Also, Travels' `simworld-look` (8042) clashes with the parent's `pokedex-view` (8042).
   - Suggest moving `sims-view` and `pokedex-view` to free ports, or removing them now that `family` covers them.

**The move**
8. **Her shortcuts don't use the one address yet.** The plan's step 4 said "Her shortcuts open the apps through it, so dark mode carries across on her PC". In fact:
   - Library Desktop and Start menu shortcuts open `http://localhost:8020/`
   - Pokédex opens `http://localhost:8030/` (via `open_app.pyw`)
   - Sim World opens `file:///…/sim-world/site/index.html`
   - There's no shortcut for home or Travels, and nothing starts `serve_all.py` at login

   So in daily use dark mode still doesn't carry, home's Open links aren't used, and the "← Jemma's Journals" links on the own ports go to `/` (the app's own home, not Jemma's Journals). Everything **does** point at the new folders, though (see The move).
9. **Leftover old-folder references that still do something:**
   - `sim-world/tools/sync_notes.py:14` copies Claude memory from `C--Users-Jemma-Documents-SimTracker\memory`, the **old** project's memory. Since the move, her Sim World chats write to `C--Users-Jemma-Documents-JemmasJournals-sim-world`, so the copy in `claude-notes/` will quietly go stale.
   - `sim-world/claude-notes/app-shows-main-checkout.md` still says the shortcut opens `Documents\SimTracker\site\index.html`. The `library-*.md` notes there say `Documents\HomeLibrary`.
   - `travels/CLAUDE.md:42` says the file link goes to `../../JemmasJournals/concepts/index.html`. The code says `../../site/index.html`.
   - Parent `research/app-styles/*/*.js` (14 scripts) still require `Documents/SimTracker/node_modules/playwright` and read `HomeLibrary`/`Pokedex`/`SimTracker`. They are old mock-up tools, but they break as soon as the old folders go. `research/drafts/publish-site-folder.yml` names `sim-tracker`.
   - `research/submodules-plan.md` line 3 reads "renamed from `site/` to `site/`" (a search-and-replace slip; it should say `concepts/`), and line 23 still says Node lives in SimTracker.
   - Everything else that matched is history (old reviews, research, patches, logs) and is fine as it is.
10. **Home, credit dot at a line end (da9233b):** at 1600 the first credits line ends "Country shapes from Natural Earth ·", because home joined the credits with plain spaces on both sides of the dot. That breaks family rule 2 (`footers-1600-light.jpg`). b869397's message says "credit dots never at a line end", so this is probably fixed now. Check it in the new version.
11. **Home, Try-switch leftovers in the code** (nothing shows on the page, and nothing in the DOM):
    - the unused `--sw-bg/-ink/-mute/-line/-on/-on-ink` colours in both `:root` blocks
    - comments that still talk about the switch: "Improved (v2): refinements to try, beside 'As now'", "Ideas to try for the whole page (switch)", "title on scroll" in the script, "the banner is navy cloth", and the round-9 header that mentions "As now" and the switch
    - `.totop{display:none}`, then overridden by `.v2`
    - the whole `.v2` layer is now the only version, and could be folded in

## Looks (for her to judge; list only)

- Footers: same order, the same 24px name, 12.5px text and 44px buttons on all five. But each sits differently:
  - Sim World's pin divider is half cut by the footer's top edge.
  - Pokédex's footer has the binder's shaded strip on its left.
  - Library's has a ❦ between rules; home and Travels have none.
  - Footer heights vary (about 205–250px at 1600).
- Pokédex credits are the longest. On phones its first credit wraps over two lines, and line 1 wraps in a different place from the others.
- Library at 1600: the "publishers·" and "Library·" dots sit tight against the word before them, while the other sites show a space either side.
- The drawers: Library's drawer starts at the name lockup (which is its Home); the others start at a "Home" link.

## Family consistency (through 8050)

✓ = same on all.

| Check | Result |
|---|---|
| Opens light with the device set to dark | ✓ all five |
| Dark pressed on site X opens the other four dark | ✓ 5 × 4: `data-mode="dark"`, button "Light mode", `aria-pressed="true"` |
| Light pressed on another site carries back to all five | ✓ 5 × 5 |
| Shared key | ✓ only `jj-mode` in storage after pressing |
| Home's Dark mode | ✓ dark icon swapped in, theme-color #6A4A17, focus stays on the button |
| Home's Back to top | ✓ scroll 0, focus `header#top` |
| robots meta | ✓ `noindex, noai, noimageai` on all five and on 404.html |
| Outside fonts and files | ✓ none requested, none in the DOM (all five, both sizes) |
| Footer order | ✓ name > line 1 > credits > Back to top > Dark mode, on all five |
| Footer line 1 | ✓ exactly "No cookies, no tracking, no ads. Made with HTML, CSS and JavaScript, kept on GitHub." on all five |
| Footer sizes | ✓ name 24px Instrument Serif, not italic; text 12.5px; buttons 44px tall and level (same middle), 13px |
| Credits on phones | ✓ one per line on the four apps; ✗ **home**, because of Broken 1 |
| Sideways scroll | ✓ none (1600 and 390) |
| Menu at 899 / sidebar at 901 | ✓ all four |
| Menu button | ✓ "Menu", 44px, `aria-controls="side"`, `aria-expanded` false → true → false. Pokédex alone also has `aria-label` "Open/Close the menu" |
| Bar name | ✓ 26px on all four |
| Closed drawer inert | ✓ Tab never reached it in 25 presses (all four) |
| Opening moves focus | ✓ to the current page's link: Library "All Shelves" on `#shelves`, the name lockup on its home; Travels "Map" on `#/map`; "Home" on Sim World's and Pokédex's home |
| While open | ✓ everything else inert (skip link, top bar, main; on Library also its hidden New covers switch). Tab only leaves to the browser's own toolbar, which is normal |
| Escape | ✓ closes, focus back to Menu (all four) |
| Scrim | ✓ black at 45%; a tap closes it and focus goes back to Menu (all four). The round-2 Pokédex scrim bug is fixed |
| Crossing 900 while open | ✓ closed, focus on Menu (all four). The round-2 Travels bug is fixed |
| Page behind | ✓ doesn't scroll. The lock is on `body` (Library, Pokédex) or `html` (Sim World, Travels); same effect |
| Home → apps on 8050 | ✓ the four "Open My …" links go to `/library/`, `/sim-world/`, `/pokedex/`, `/travels/` and the right page opens |
| Home → apps elsewhere | ✓ on 127.0.0.1:8040 the link shows the toast "My Sim World opens here once the sites are online" |
| Home layout | ✓ four places 2 × 2, spanning the full width and lined up with the headings and their rules: 1600 → 220–1380 (cards 220–780 and 820–1380); 1280 → 60–1220; 1000 → 40–960 |
| Page errors | ✓ none. One early run logged `ERR_CONNECTION_REFUSED` resource errors on home in light mode; two repeat runs had none, so it was a passing blip |

## The move

| Check | Result |
|---|---|
| `.gitmodules` | ✓ library, sim-world, pokedex, travels → `https://github.com/jemmathornton/<name>.git`, `branch = main` |
| Each submodule's origin | ✓ the same URL |
| Submodule versions recorded in the parent | ✓ `git submodule status`, no `+` or `-`: library 506463a, pokedex eba32a1, sim-world 1df0098, travels 9060727, all on `main`, clean |
| `.gitignore` | ✓ `.tools/`, `node_modules/`, `__pycache__/`, `*.pyc`, `*.tmp`, `*.lnk` |
| Scheduled tasks | ✓ "Jemma's Library - weekly backup", "Jemma's Pokedex - weekly backup", "Jemma's Sim World - weekly Gallery refresh": all Ready, all run pythonw on `Documents\JemmasJournals\<app>\tools\…`, with the working folder in the new place |
| Shortcuts | ✓ Desktop and Start menu "Jemma's Library", "Jemma's Sim World", "Jemma's Pokédex", and Startup "Jemma's Library server": every target, working folder and icon is in `Documents\JemmasJournals\…`. No old folder anywhere. (Through 8050? No: see Should fix 8) |
| serve_all: only this computer | ✓ binds `127.0.0.1:8050` (netstat confirms) |
| serve_all: traversal | ✓ nothing escapes, all 404: `/library/../../.git/config`, `/library/%2e%2e/%2e%2e/.git/config`, `/%2e%2e/.git/config`, `..%2f`, `..%5c`, `/library/../CLAUDE.md`, `/.git/config`, `/tools/serve_all.py`, `/library/C:/Windows/win.ini`. `%5c` and `C:%5c…` forms are dropped as a whole path piece and redirect back inside the app's own `site/`. `//evil.com/` and `/library//evil.com` give 404, not a redirect |
| serve_all: redirects | ✓ `/library` → `/library/` (301; query dropped) |
| serve_all: forwarding | ✓ `X-Library`, `X-Pokedex`, `X-Travels`, `Content-Type`, `Accept` passed; body read by Content-Length; 300s timeout; apps' error codes passed through (Library 403 JSON). **✗ Host check bypassed (Broken 2), ✗ 2s delay (Should fix 1)** |
| serve_all: app server down | ✓ clear 503 "The travels server (port 8041) is not running" (after about 4s, because of the `localhost` delay) |
| serve_all: Sim World `/api/` | ✓ 404 (it has no server) |
| Launch configs | ✓ `family` (8050, `-I`) and `home` (8040) fine; `travels` `simworld-look` now uses `../sim-world/site`, which works inside the parent. ✗ port clashes (Should fix 7) |
| Sim World's `map-squares` config | ~ serves the whole sim-world folder (no `--directory`); this is not new |
| Old repo names and folders | ✓ none in live code apart from Should fix 9 |

## Ready for shared code (`/family/…` loaded from Jemma's Journals)

The other session has already started this: `site/family/` (`mode.js`, `family.js`, `family.css`, README) is committed in b869397, and home uses it. Here is what will get in the way for the apps:

1. **The apps' own servers serve only their own `site/`.** Library 8020, Pokédex 8030 and Travels 8041 answer `/family/…` with 404 (or 403 for an odd Host on the Library). Her shortcuts open the Library and Pokédex on those ports, so each `serve.py` needs a `/family/` route to `../site/family/`, as the README plans. Copy the parent's traversal safety, and keep the Library's Host check in front of it. Or, better, move the shortcuts to 8050 (Should fix 8) and then the own ports matter only for tests.
2. **Sim World opens as `file://`** (Desktop and Start menu). There, `/family/mode.js` becomes `file:///C:/family/mode.js` and fails, so it opens with no dark-mode script, no footer behaviour and no drawer. Options:
   - point its shortcut at `http://localhost:8050/sim-world/` (needs `serve_all` running, for example from Startup)
   - or have it fall back to `../../site/family/` when the address is `file:` (it already does this for its home link)

   The Library and Pokédex also say they still work "opened as a file", and the Pokédex has a file-mode notice. All three would lose the shared code that way.
3. **Test servers and sandboxes don't contain the parent:**
   - Library, Pokédex and Travels tests copy the app into a `mkdtemp` sandbox (`tests/support.py`) and run `serve.py` there, so `../site/family` doesn't exist. The sandbox needs `JJ_FAMILY` or a copy of `site/family`, and the test server a `/family/` route.
   - Sim World's tests and its `app` (8001) and `live-snapshot` (8000) previews are plain `http.server --directory site`.
   - Parent configs `sims-view` (8041), `pokedex-view` (8042), `simworld-live` (8045), `travels-view` (8046) and `simworld-trial` (`trial_server.py`) all serve one app folder at `/`, so `/family/` gives 404 on all of them.
   - Each app's Playwright checks that serve from disk (route.fulfill) need a `/family/` mapping. Each app's own suite has to run against the parent's current `site/family/`, so the README's "run every site's tests" is real work.
4. **Submodule independence:** each app's own GitHub repo will no longer work on its own (cloned alone it has no `/family/`). That is accepted by her choice, but worth a line in each app's README and CLAUDE.md. The parent records each app's version, but nothing records which family version an app was tested with. Any change to `site/family/` affects all five at once.
5. **Caching:**
   - Library, Pokédex and Travels stamp fingerprints (`?v=…`) into their own file links at build time. `/family/` files won't be stamped, so an app window could keep an old `family.js`.
   - `serve_all` sends `no-cache` and the Library's service worker passes everything to the network, so it's fine locally. Online (GitHub Pages caches for about 10 minutes) it's worth a `?v=` on the family links too.
6. **Root-absolute paths online:** `/family/…`, home's `/library/`-style Open links and the apps' "← Jemma's Journals" `href="/"` all assume the family sits at the **root** of a domain. That's true on her own domain, or on a `jemmathornton.github.io` user site, but **not** on a project page (`jemmathornton.github.io/jemmas-journals/`), where all of them break. Decide where it goes online before relying on them.
7. **No CSP anywhere** (no `Content-Security-Policy` meta or header in any app). Nothing blocks loading `/family/` same-origin. If a CSP is added later, `script-src 'self'` covers it. Home's and the apps' inline head scripts would then need hashes, but those are being replaced by `/family/mode.js` anyway.
8. **Order and timing:** `mode.js` must stay a plain blocking `<script>` in `<head>` before each stylesheet. Each app's own inline mode code and old-key handling must be removed when it moves over, or two scripts will both write `jj-mode` and `data-mode`. Pokédex still left its old key behind in round 2; `data-old-key` handles that now.
9. **Library's app shell:** its `sw.js` registers at `/library/` scope. It passes `/family/` requests through to the network, so it is harmless, but if it ever starts caching, `/family/` must be in its list.
10. **The 8050 server itself is ready:** `/family/` is served from `site/family/` already (it falls through to home's folder), with `no-cache`.
