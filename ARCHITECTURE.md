# How it all fits together

Jemma’s family of websites, in one page (written 22 Nov 2026 from the code as it stands; where something could not be checked it says **unsure**). Her decisions and the reasons for them are in `CLAUDE.md`; this page is only how the parts connect.

## The pieces

```
Documents\JemmasJournals\                 the parent repo (jemmathornton/jemmas-journals, public)
  site\               home page            served at  /
  site\family\        shared code          served at  /family/   (mode.js, family.css, family.js)
  library\    ─┐                           served at  /library/    saves → Library server   :8020  (phone scans :8021)
  sim-world\   │  submodules, each its     served at  /sim-world/  (no save server: static)
  pokedex\     │  own GitHub repo          served at  /pokedex/    saves → Pokédex server   :8030
  travels\    ─┘                           served at  /travels/    saves → Travels server   :8041
  tools\  tests\  templates\new-site\  research\  for-jemma\  logs\ (not in git)

            her shortcut ──► tools/open_site.pyw <app> ──► Chrome app window on http://localhost:8050/<app>/
                                         │ starts if needed
                                         ▼
             tools/serve_all.py  :8050  (the family server: pages, /family/, her dark-mode choice)
                 │ passes …/api/… on to, and starts if needed
                 ▼
             library/tools/serve.py :8020    pokedex/tools/serve.py :8030    travels/tools/serve.py :8041
```

## Parent and submodules

- Jemma’s Journals is the **parent**; Library, Sim World, Pokédex and Travels are **git submodules** (`.gitmodules`, branch `main`). Each app keeps its own repo, history and `CLAUDE.md`; the parent only records which commit of each app goes with it. Plan and history: [research/submodules-plan.md](research/submodules-plan.md).
- Each app’s published part is its own `site/` folder; `data/`, `tools/`, `tests/`, notes and research stay out of anything published.
- After an app commits, the parent still points at the old commit until it is **recorded**: `python tools/record_apps.py` does that for every app that is on `main`, clean and pushed, then commits “Record app versions: …” in the parent and pushes. It touches nothing else in the parent.

## Shared code: `site/family/`

- One copy of what every site shares (her rules: [research/family-rules.md](research/family-rules.md); how to use it: [site/family/README.md](site/family/README.md)): dark mode (`jj-mode`, opens light), the footer and its first line, Back to top, credit dots, and the Menu drawer under 900px.
- Every app loads it **from the root**: `/family/mode.js` (in `<head>`), `/family/family.css`, `/family/family.js`. Home loads it relatively (`family/…`). Each site keeps its own look through its `--jj-*` CSS variables.
- Where `/family/` comes from: the family server (8050), each app’s own server (8020, 8030, 8041 each serve `../site/family`), each app’s test server, and the online build. Opened as a plain file, Travels loads `../../site/family/`; **unsure** how the others behave as a file (the Library and Pokédex notes say the footer buttons and drawer need `/family/`).
- Change it once there, then test every site (below).

## Servers on her PC

| Port | What | Started by |
|---|---|---|
| 8050 | `tools/serve_all.py`: the whole family on one address, as online. Serves pages and `/family/`; passes `/<app>/api/…` to the app’s server; keeps her dark-mode choice in `logs/family-mode.txt` and writes it into each page (`data-jj-server-mode`) so it carries between app windows with different Chrome profiles. Only answers to `localhost` / `127.0.0.1`. | Startup item “Jemma's Journals server”, or `open_site.pyw` |
| 8020 (+8021) | Library `tools/serve.py`: saves, StoryGraph import, phone scanning on 8021 (home Wi-Fi only) | `serve_all.py` starts it if down |
| 8030 | Pokédex `tools/serve.py`: saves her ticks, each game its own file (`data/collection/go.json`; Pokémon HOME's `home.json` since 22 Nov, `?game=home`) | `serve_all.py` |
| 8041 | Travels `tools/serve.py`: the Write page (posts and photos) | `serve_all.py` |
| 8060 | `tools/build_site.py --serve`: the online-style copy (see below) | by hand / launch config `online-test` |

Sim World has no save server. Other ports in `.claude/launch.json` (8040 home alone, 8043–8048 views and trials) are for Claude previews only. Test servers use their own ports (Sim World 8011, Pokédex 8031: **8031 writes to her real ticks file**, see the Pokédex notes).

## How she opens things

- Desktop and Start-menu shortcuts run `pythonw tools/open_site.pyw <app>` (`home`, `library`, `sim-world`, `pokedex`, `travels`). It starts `serve_all.py` if 8050 isn’t answering, then opens a Chrome (or Edge) app window on `http://localhost:8050/<app>/`. The Library, Pokédex, Travels and home windows use their own Chrome profiles (their own taskbar buttons); Sim World uses her normal Chrome.
- `tools/setup_pc.ps1` makes the Startup item and shortcuts for the **Library, Sim World and Pokédex only**; it makes no Travels or home shortcut (**unsure** whether she has those from elsewhere). New PC steps: [for-jemma/new-pc.md](for-jemma/new-pc.md).

## The daily backup

- Windows task **“Jemma's Journals - backup”**, every day at 09:30 (catches up after the PC was off), runs `pythonw tools/weekly.py` (the name is older than the daily schedule). In turn: Sim World’s Gallery refresh (Sundays only, or `--all`), Library `tools/backup.py`, Pokédex `tools/backup.py`, `tools/backup_new_sites.py` (sites made by `new_site.py`, once they have a GitHub repo; none yet), Travels’ Write-page files committed and pushed, then `tools/record_apps.py`. One failure doesn’t stop the rest. Log: `logs/weekly.log` (each app also keeps its own).
- Every push signs in through the GitHub CLI credential helper, never a Windows sign-in window.
- The three old per-app weekly tasks still exist but are **disabled** (checked 22 Nov).

## The online-style build and going online

- `python tools/build_site.py` copies home’s `site/` to `_site/` and each app’s `site/` under its name; `--serve` serves it at http://localhost:8060 like a plain host (no saving, no forwarding, its `404.html` for missing pages). What works there should work online: the Library and Pokédex show view-only, Travels’ Write page says it needs her PC.
- Not online yet (her decision when). It will need, per [research/improvements-22-nov.md](research/improvements-22-nov.md) and [research/going-online.md](research/going-online.md): a GitHub Actions workflow in the parent that checks out the submodules, does what `build_site.py` does and deploys to GitHub Pages; the site at the **root** of an address (her domain, or the parent repo renamed `jemmathornton.github.io`), because `/family/` and `/` links need it; Pages kept off in the app repos; finishing view-only for the Pokédex; perhaps a `?v=` stamp on `/family/` links for caching. Draft files: `research/drafts/`.

## Tests

| Site | Command (from its folder) | Notes |
|---|---|---|
| Home | `.tools/node/node.exe tests/check_page.js` | Edge at 1600, 1280, 1000, 390; expects four places |
| Family rules | `.tools/node/node.exe tests/family/family.test.js` | all five sites through a test copy of the family server, and the online-style build |
| Family tools | `python -B -X utf8 -m unittest discover -s tests/tools -t tests/tools` | serve_all, record_apps, weekly, build_site, new_site, open_site |
| Library | `python -B -X utf8 tests/run_tests.py` | on a throwaway copy |
| Sim World | `python -B -X utf8 tools/run_tests.py` | about 2 minutes |
| Pokédex | `python -B -X utf8 tests/run_tests.py` | never leave test ticks in `go.json` |
| Travels | `python -B -X utf8 tests/run_tests.py` (`unit` for the quick half) | about 11 minutes in full |
| Accessibility | `.tools/node/node.exe tests/axe_all.js [--strict]` | needs 8050 running; report only without `--strict` |

**All at once:** `python tools/check_all.py` (about 25 minutes) or `--quick` (a few minutes: home, family rules, family tools, accessibility and git; skips the four apps’ own suites). It runs each suite above, the accessibility report (on its own test copy of the family server, so 8050 isn’t needed), and checks each app is on `main`, clean and pushed (and notes any not yet recorded in the parent). Logs: `logs/check-all/`. Node and Playwright are shared from the parent (`.tools/node`, `node_modules/`, both git-ignored; see new-pc.md step 5).

## Adding a new site

`python -X utf8 tools/new_site.py <folder> "<Name>" ["#colour"] --dry-run`, then without `--dry-run`. It copies `templates/new-site`, makes a local git repo (no GitHub until she says), and wires the folder into `serve_all.py`, `open_site.pyw`, `build_site.py`, `check_all.py` (its tests), `tests/axe_all.js`, `backup_new_sites.py` (so the daily backup pushes it once it has a GitHub repo) and the parent’s `.gitignore`. Home only changes with `--add-to-home` (a new place on home is her yes; `tests/check_page.js` expects four); a shortcut only with `--shortcut` (listed in `setup_pc.ps1`). Not wired automatically: `record_apps.py` and the git checks in `check_all.py` (they list the submodules by name; added by hand once it is a submodule). Her guide: [for-jemma/new-site.md](for-jemma/new-site.md).

## Where else to look

- `CLAUDE.md`: her rules and decisions, and the checklist for making changes.
- Each app’s `CLAUDE.md`: its own rules, data and tests.
- `for-jemma/`: what was shown to her and her answers. `research/`: reviews, ideas, hosting.
