# Adding a new site to the family

## 1. Run one command

In PowerShell, in `Documents\JemmasJournals`:

```
python -X utf8 tools/new_site.py recipes "Recipes" "#8A3B2E"
```

- `recipes` is the folder and the address (lower case, a hyphen between words).
- `"Recipes"` is the name after “Jemma’s”.
- `"#8A3B2E"` is its colour (you can leave it out: it uses a quiet blue). If the colour is too pale to read, it picks a darker one of the same colour and tells you.
- Add `--dry-run` at the end first if you’d like to see what it will do without changing anything.
- If anything can’t be done, it stops before changing anything.

Then restart the family server so it knows the new site:

```
python tools/restart_family.py
```

## 2. What it makes

- A new folder, `Documents\JemmasJournals\recipes`, with a working site: the “← Jemma’s Journals” link, the sidebar, the Menu on phones, the family footer, dark mode, and three example pages. Every bit of wording is marked **Placeholder**.
- Its own history (git), only on your PC: nothing goes online, and **nothing backs it up until it has a GitHub repo** (step 4).
- It opens at http://localhost:8050/recipes/ (after the restart above). The family checks test it too, accessibility included.
- Jemma’s Journals ignores the new folder (it has its own history) until it becomes part of the family on GitHub.
- The home page stays as it is. To add the new site to Contents too: `python -X utf8 tools/new_site.py recipes --add-to-home` (it uses the site’s own colour), or ask Claude.
- No Desktop or Start shortcut yet. For one: `python -X utf8 tools/new_site.py recipes --shortcut`, then run `tools\setup_pc.ps1` again (as in new-pc.md).

Made one by mistake? `python -X utf8 tools/new_site.py recipes --remove` takes it out of the family again. It never deletes the folder; it tells you how, if you want to. (It takes out the lines it added, even if they were changed by hand since.)

## 3. Make it yours

Open a Claude chat in the new folder (it has its own notes, `CLAUDE.md`) and say what the site is for. Then:

- **Words:** `site/js/data.js`, your own words in place of the placeholders.
- **Look:** `site/site.css`; the colours are at the top. Claude can build looks into the page for you to click through.
- **Pages:** `site/js/app.js`.

## 4. Putting it on GitHub (only when you say so)

Nothing goes on GitHub until you decide. A public repo can be read by anyone. When you’re ready, ask Claude, or run the steps the command printed:

```
cd Documents\JemmasJournals\recipes
& "C:\Program Files\GitHub CLI\gh.exe" repo create jemmathornton/recipes --public --source . --push     (or --private)
cd ..
python -X utf8 tools/new_site.py recipes --unignore
git submodule add https://github.com/jemmathornton/recipes.git recipes
git commit -m "Add Jemma’s Recipes as a submodule" -- .gitignore .gitmodules recipes
git -c "credential.helper=!'C:/Program Files/GitHub CLI/gh.exe' auth git-credential" push
```

Claude then adds it to `tools/record_apps.py` and the git checks in `tools/check_all.py`, and checks the daily backup includes it (`tools/backup_new_sites.py` saves and pushes each new site that has a GitHub repo).

Pictures of a test site made this way: `for-jemma/concepts/new-site-template/`.
