# Round 5 review: the new-site template and tools/new_site.py (22 Nov 2026)

Read-only review. Tested on a throwaway copy of the parent (site/, tools/, templates/, tests/, with node_modules and .tools linked in), in the scratchpad; nothing in Jemma’s Journals was changed apart from this file. The family server ran from that copy on port 8071, not 8050.

**What was run:** `new_site.py` with `--dry-run`, a real run (“Café Recipes”, pale accent #F4D35E), a second run, `--add-to-home` twice, `--remove` (dry and real) twice, 23 odd names, folders and colours, and the tool files with Windows (CRLF) line endings. The generated `tests/check_site.js`: **177 passed, 0 failed**. Also checked by hand through the family server: 1600, 899 and 390, light and dark; the drawer (focus goes to the current page’s link, the rest inert, the page doesn’t scroll); dark mode carrying from home to the new site (localStorage and the server’s saved mode); `/recipes` redirecting to `/recipes/`; an unknown item showing Not found; a missing file showing home’s 404; opening `site/index.html` as a file (the `../../site/family/` fallback works); a 40-letter name in the top bar (cut off with “…”, no sideways scroll).

**Overall:** the generated site follows the family rules well: robots meta, the exact family CSP (same as Travels, Pokédex and Sim World), `/family/` code in the same order as the real apps, local fonts, opens light with the device set to dark, `jj-mode`, the family footer with true credits, the Menu drawer behaving as the rules say, Lucide icons, curly apostrophes, every placeholder marked. The wiring is careful: every edit is worked out before anything is written, adding twice changes nothing, and `--remove` puts the files back exactly. The main problems are line endings and a few gaps in what is wired in and explained.

## Broken

1. **The wiring fails once the tool files have Windows line endings.** This repo has `core.autocrlf=true`. Today’s working files happen to be LF, but git warns “LF will be replaced by CRLF the next time Git touches it”, and a fresh clone (`setup_pc.ps1`, new-pc.md) will be CRLF. In `block()` the end pattern `^\}$` never matches `}\r`, so:
   - adding stops with “could not find the end of “APPS = {””. That is safe, but the site folder has already been copied and git-inited (see Should fix 1);
   - **`--remove` silently does nothing.** `remove_line` and `home_remove` swallow the error, and `build_remove`’s `\}$` fails as well, so it prints “nothing to change” for every file while the wiring stays in place.
   - Reproduced on the copy by converting the five files to CRLF. Fix: read with normal newline translation (or match `\r?$`), and write back in the file’s own line ending.

## Should fix

1. **Check the wiring before making the folder.** The folder is copied, git-inited and committed first. If the wiring then fails, it prints “stopped, nothing written”, which isn’t true. Plan the edits first (as `apply(dry=True)` already can) and only copy if they will all apply.
2. **`--add-to-home` on a later run uses the wrong colour.** The accent isn’t stored. `new_site.py recipes "Recipes" --add-to-home` (the second-run route that new-site.md suggests) puts `pc:"#3D6A8A"` (the default) on home, while the site itself was made with #7A6A2F. Read `--accent` back from the existing `<folder>/site/site.css` when the folder exists and no colour is given.
3. **Names with control characters are accepted.** A newline or tab in the name passes the check. A newline would break `tools/check_all.py` (a newline inside a Python string is a SyntaxError) and, with `--add-to-home`, `site/home.js`. Reject `[\x00-\x1f]` along with `< > " & \ ` $`.
4. **Places that list the sites but aren’t wired in or mentioned:**
   - `tests/axe_all.js` has a fixed list of addresses, so the new site gets no accessibility report from `check_all.py`;
   - `tools/setup_pc.ps1` makes no Desktop/Start shortcut for it (and has none for Travels either), so there is no way to open it as an app window, although open_site.pyw now knows it;
   - `tools/weekly.py` doesn’t back it up. While it is local-only, nothing backs it up at all; worth saying in new-site.md;
   - `.claude/launch.json` has no entry (the `family` config covers it at 8050, so that is fine; just say so).
   - `record_apps.py` and the check_all git loop are printed as manual steps, which is correct until it is a submodule.
5. **The parent sees the new folder as untracked (`?? recipes/`).** It holds its own `.git`, so a careless `git add -A` in the parent would add it as an embedded repo (a gitlink with no `.gitmodules`), and `check_all` reports the parent as having changed paths. Either add `/<folder>/` to the parent’s `.git/info/exclude` until it becomes a submodule (and drop that line then), or warn about it in the printed Next steps and the docs.
6. **No one says how to restart the family server.** The docs and the script say “restart the family server” three times, but it is a windowless pythonw process started at login, with no stop button or tool. For Jemma that means signing out and back in, or Task Manager. Add a plain way to do it: a `--restart` in serve_all.py or open_site.pyw, or one line in new-site.md (“sign out and in again”).
7. **Placeholder wording uses two voices.** Home and the cards say “…in your own words” (speaking to Jemma). The item page says “Her words about it go here.” Pick one; “your” fits, since she is the one reading it.

## Nice to have

- **Two Placeholder badges on every card** (one on the title, one on the line). On phones the second wraps onto its own line and is pushed 8px in by its left margin. One badge per card, or no left margin when it wraps (use `gap` or `margin-inline-start` on a wrapper), would read more calmly.
- **The name appears twice at the top of Home:** in the sidebar and as the h1 at 1600, and stacked in the top bar and the h1 on phones. The real apps put a banner there. Fine for a starter, but the h1 could be the Introduction heading, or the CLAUDE.md could say “add a banner here”.
- **Tab icon:** SVG only. The other apps add PNG sizes (16/32/192) for browsers and phones that ignore SVG icons. No dark tab icon, which is allowed (“if the site has one”).
- **Bad colour message:** `"red"` gives “rreedd” is not a colour (the 3-digit doubling happens before the check). Show what was typed.
- **Accents in names are dropped for the Chrome profile folder:** “Café Recipes” becomes `Jemmas Caf Recipes`. Use `unicodedata.normalize('NFKD', …)` so it becomes “Cafe”.
- **Letters the fonts don’t have:** a name with letters outside the latin/latin-ext subsets (Greek, for example) falls back to Georgia. Could warn.
- **Folder names:** `a--b` and `recipes2-` are allowed. `concepts` (home’s old folder name) isn’t reserved. Harmless.
- **The accent search** darkens towards black, so a bright yellow becomes a muddy olive (#F4D35E becomes #7A6A2F). It does tell her. Could also print the darkest pleasant shade, or point her at trying it live.
- **Removed folders break the tools:** `build_site.py` and `check_all.py` crash (no try) if a wired folder is deleted without `--remove`. Skip a missing folder with a note.
- **Tests:** `check_site.js` doesn’t check 1280 or the credit wording, and doesn’t run through the family server (its own `site.test` route), so `data-jj-server-mode` isn’t covered. Fine for a template; `axe_all.js` would cover the live server if the site were in it.
- **Placeholder wiring is never cleared:** the open_site/serve_all lines keep the “added by tools/new_site.py” mark forever. Fine, but `--remove` also takes out a line she later edits by hand (it matches the folder, not the mark). Worth one sentence in the docs.

## Docs

- **new-site.md is clear and in her voice.** Gaps:
  - how to restart the server (Should fix 6);
  - that the new site has no shortcut and no backup until it is on GitHub (Should fix 4);
  - step 4 leaves out the parent push and the record_apps / check_all edits that the script prints and CLAUDE.md lists. Say “Claude does the rest” or list them;
  - “run it again with `--add-to-home`” should also say to give the colour again (or fix Should fix 2).
- **CLAUDE.md “Adding a new site”** is accurate about what the script does. “Undo … exactly” isn’t true with CRLF files (Broken 1).
- **Footer line 1 doesn’t match between files.** CLAUDE.md (“Her picks after the second review”) says “Made with HTML, CSS and JavaScript, kept on GitHub.” `family.js` and `research/family-rules.md` say “…JavaScript and Python…”. The template just shows whatever family.js has, so this isn’t a template bug, but one of the two needs correcting so new sites follow her actual pick.
- **The template’s CLAUDE.md** is good: rules, tokens, where things are, the test command. It gives the full Python path while new-site.md says `python`. Both work on this PC (`python` is Python313 on PATH).
- **site.css and data.js** are well commented: tokens first, “change these first”, the null-means-placeholder rule. Easy for Claude or her to restyle.

## Note on git status

My work was only in the scratchpad copy and this report. While I worked, other sessions changed the real repo: `CLAUDE.md` and the `library` and `pokedex` submodules are now modified and `ARCHITECTURE.md` is new. I didn’t touch any of them.
