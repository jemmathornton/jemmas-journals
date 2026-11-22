# Jemma’s __NAME__

**Where this lives:** `Documents\JemmasJournals\__FOLDER__`, a site in the family of Jemma’s Journals (the parent). Made on __DATE__ by `tools/new_site.py` from the family template (`templates/new-site` in the parent). Node and Playwright for tests are shared in the parent (`JemmasJournals\.tools`, `JemmasJournals\node_modules`). The whole family on one address: `tools/serve_all.py` in the parent, http://localhost:8050/__FOLDER__/.

**What it’s for:** [Placeholder: in her words, what this site is for and what goes on it.]

**Its repo:** local only for now (`git init` here, no GitHub repo yet). Making a GitHub repo and adding it to the parent as a submodule is **her decision**: the commands are in the parent’s `for-jemma/new-site.md`.

## Working rules (as for her other sites)

- **Never edit Jemma’s own files without asking** (Downloads, Documents, Pictures, her other projects). Copy into this project and work on the copy.
- **British English**; **curly apostrophes** in shown text (ids, links and data keys stay straight).
- **No made-up text on the site:** her words, or an app’s own text word for word. Missing means a marked placeholder (the dashed **Placeholder** badge: `null` in `site/js/data.js`). Labels like “Contents” or “Open …” are fine.
- **No AI-generated art.** Pictures are hers or from the source they belong to (publishers’ covers, the games’ own maps …). Icons: Lucide (ISC); never a real logo. The tab icon (`site/icon.svg`) is a Lucide book in the accent colour: a stand-in until she chooses one.
- **Show, don’t ask, for looks:** build each option into the running site (a trial switch, only while she is choosing, removed after) and **open it in the browser pane for her to click through**. Screenshots only as a record.
- **When asking her to choose, list every option** in the message. **Label suggestions** “my suggestion (not decided)”.
- **Light mode by default**: dark only when the footer button is pressed.
- **Downloads need her OK first** (say what, from where, how big).
- Short, plain answers. When she’s away for hours, keep working through checks and small fixes in one turn.

## The family rules (summary; the whole thing is the parent’s `research/family-rules.md`)

- **Shared code from the parent**, never copied: `/family/mode.js` (in `<head>`, before the stylesheet), `/family/family.css` (before `site.css`), `/family/family.js` (deferred). See the parent’s `site/family/README.md`.
- **Dark mode:** opens light whatever the device says; the footer’s Dark mode button; shared `localStorage` key `jj-mode`; dark styles hang off `:root[data-mode="dark"]`, never `prefers-color-scheme`.
- **Footer:** the site’s name, line 1 (filled in by family.js, the same words on every site), this site’s own true credits (`<span class="cr">…</span><span class="dot" aria-hidden="true">&nbsp;·</span> …`), then Back to top and Dark mode, 44px tall and level.
- **Menu drawer at 900px and below:** slim top bar with Menu and “Jemma’s *__NAME__*”; the sidebar slides in (`JJFamily.menu` in `site/js/app.js`). “← Jemma’s Journals” stays first in the sidebar and drawer.
- **Every page:** `<meta name="robots" content="noindex, noai, noimageai">` and the family’s Content-Security-Policy (only the site’s own files; no inline scripts or handlers). **No files from other sites**: fonts are local copies (`site/fonts/`, Instrument Serif and Manrope, SIL OFL).

## Where things are

- `site/index.html`: the page shell (sidebar, top bar, footer). `site/site.css`: the look; **tokens at the top** (`--accent` light and dark, backgrounds, ink): restyle from there. `site/js/app.js`: the pages and the hash router (`#/` Home, `#/list`, `#/item/<id>`, anything else Not found). `site/js/data.js`: the content (all placeholders to start with).
- `tests/check_site.js`: the checks (see below).

## How to work here

- Python 3.13: `C:/Users/Jemma/AppData/Local/Programs/Python/Python313/python.exe -X utf8`. Ask before installing anything.
- **Tests:** `../.tools/node/node.exe tests/check_site.js` from this folder (Edge through the parent’s Playwright; serves site/ itself with `/family/` from the parent). It checks: no errors or Content-Security-Policy violations, opens light, footer rules, the drawer at 899/901, dark mode and `jj-mode`, no sideways scroll at 390, curly apostrophes, axe-core (no serious or critical problems). Add `--shots <folder>` for screenshots at 1600 and 390, light and dark. Run after every change; add a check for each bug fixed. The parent’s `tools/check_all.py` runs it too.
- To view it: through the family server, http://localhost:8050/__FOLDER__/ (`tools/serve_all.py` in the parent; restart it after `new_site.py` added this site).
- Git: commit after each piece of work. After its GitHub repo exists and it is a submodule: push here, then record the new version in the parent (`git add __FOLDER__` there) and push both.

## Her decisions so far

- [Placeholder: none yet.]
