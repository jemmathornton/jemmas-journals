# Plan: Jemma’s Journals as the parent, the four apps as submodules (21 Nov, not started)

Her layout: Jemma’s Journals is the parent and holds all the shared code; Library, Sim World, Pokédex and Travels are submodules that use it. Nothing on GitHub changes: each app keeps its own repo. All public, which GitHub Pages needs ([docs](https://docs.github.com/en/pages/getting-started-with-github-pages/using-submodules-with-github-pages)).

```
Documents\JemmasJournals\        (parent)
  concepts\                       home page (served at /)
  concepts\family\                shared code (later: dark mode, footer, Menu drawer, sidebar …), served at /family/
  library\        ← submodule (jemmathornton/library)
  sim-world\      ← submodule (jemmathornton/sim-tracker)
  pokedex\        ← submodule (jemmathornton/pokedex)
  travels\        ← submodule (jemmathornton/jemmas-travels)
```

## What was checked on her PC (21 Nov)

- **Servers:** the Library (8020, phone scanning 8021), the Pokédex (8030) and Travels (8041) each run their own `tools/serve.py`; each finds its folder from its own location, so they keep working after a move. Sim World is static.
- **Save calls:** the Library and Travels call `api/…` (relative: fine under /library/); the Pokédex calls `/api/…` (from the root), which needs changing to `api/…` to work under /pokedex/.
- **Windows tasks:** “Jemma's Library - weekly backup”, “Jemma's Pokedex - weekly backup”, “Jemma's Sim World - weekly Gallery refresh”.
- **Desktop shortcuts:** Jemma's Library, Jemma's Sim World, Jemma’s Pokédex.
- **Shared tools:** Node and Playwright live in SimTracker (`.tools/`, `node_modules/`); the Travels and Journals tests use them from there.
- **Files only on her PC (not in git):** Pokédex `go.json.lock`; Library `data/scanned.json`, `logs/`, old-cover pictures, `Jemma's Library.lnk`; Sim World `.tools/`, `node_modules/`, `logs/`, a save zip, `last-import-previous.json`; Travels `for-jemma/looks*`, `extras`, `templates`. Her Pokédex ticks and Library marks are in git and saved weekly, but anything since the last save is only on her PC.
- **Hard-coded paths:** Pokédex `tools/forms_sheet.py`; Travels tests (Playwright path); the apps’ “← Jemma’s Journals” link when opened as a file (`../../JemmasJournals/concepts/index.html`); launch configs.

## Steps

**0. Get ready (with her)**
- Every app quiet: no Claude session working in it, app windows closed, everything committed and pushed.
- Stop the three save servers; pause the three Windows tasks.
- Note a fingerprint of her Pokédex ticks and Library data, to prove they arrive unchanged.

**1. Copy each app into Jemma’s Journals and register it** (the old folders aren’t touched)
- Copy the whole folder exactly (robocopy), including the files that aren’t in git, so nothing is lost.
- Register each copy as a submodule pointing at its GitHub repo (`git submodule add <url> <folder>`, then `git submodule absorbgitdirs`). Commit `.gitmodules` in Jemma’s Journals and push.
- Check: each app on the same commit as GitHub, nothing uncommitted, ticks and Library data fingerprints match.

**2. Shared tools into the parent**
- Node and Playwright move to Jemma’s Journals (`.tools/`, `node_modules/`, not in git); every app’s tests point there.

**3. Re-point everything**
- The three Windows tasks and three desktop shortcuts to the new folders.
- Launch configs, `forms_sheet.py`, the test paths, and the “← Jemma’s Journals” file link (now `../../concepts/index.html`).
- Each app’s notes (CLAUDE.md) updated with its new place.

**4. One local server for the whole family** (Jemma’s Journals `tools/serve_all.py`)
- `/` home, `/library/`, `/sim-world/`, `/pokedex/`, `/travels/`, `/family/`: the same addresses as online.
- Saves are passed on to each app’s own server, which keeps running as now.
- Pokédex save calls changed to `api/…`.
- Her shortcuts open the apps through it, so dark mode carries across on her PC and home’s Open links work locally.

**5. Claude sessions**
- Copy each app’s Claude memory to its new folder; she opens each app’s session from its new folder from then on.

**6. Check everything**
- Every app’s tests from its new place; the Journals checks; a save tested on each (on a throwaway copy, never her ticks).
- Open each app for her through the one server.

**7. The old folders**
- Left untouched until she has used the new setup; then renamed or removed only with her OK.

## Afterwards (separate jobs)

- **Shared code into Jemma’s Journals**, one app at a time: dark mode and the footer first, then the Menu drawer, then the sidebar layout. Apps load `/family/…`; each app keeps its own colours and look. Each app’s own server also serves `/family/` from the parent, so it still works on its own port.
- **Going online:** a GitHub Actions workflow in Jemma’s Journals fetches the submodules, puts home and each app’s `site/` folder together (research, tests and notes stay out of the published site) and publishes to her domain.
- **A small script** for the extra step: after an app changes, record its new version in Jemma’s Journals and push both.

## Her choices

1. **Folder and web names:** (a) friendly names, `library`, `sim-world`, `pokedex`, `travels` (my suggestion, not decided); (b) the GitHub repo names, `library`, `sim-tracker`, `pokedex`, `jemmas-travels`.
2. **Old folders after the move:** (a) keep untouched for a week, then delete with her OK (my suggestion, not decided); (b) rename to “… (old)” straight away so nothing uses them by mistake; (c) delete once checked.
3. **Home’s own folder:** (a) keep `concepts/` (my suggestion, not decided, least change); (b) rename to `site/` to match the apps.
