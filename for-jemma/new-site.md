# Adding a new site to the family

## 1. Run one command

In PowerShell, in `Documents\JemmasJournals`:

```
python -X utf8 tools/new_site.py recipes "Recipes" "#8A3B2E"
```

- `recipes` is the folder and the address (lower case, hyphens for spaces).
- `"Recipes"` is the name after “Jemma’s”.
- `"#8A3B2E"` is its colour (you can leave it out: it uses a quiet blue). If the colour is too pale to read, it picks a darker one of the same colour and tells you.
- Add `--dry-run` at the end first if you’d like to see what it will do without changing anything.

## 2. What it makes

- A new folder, `Documents\JemmasJournals\recipes`, with a working site: the “← Jemma’s Journals” link, the sidebar, the Menu on phones, the family footer, dark mode, and three example pages. Every bit of wording is marked **Placeholder**.
- Its own history (git), only on your PC: nothing goes online.
- It’s added to the family server, so after a restart of the server it opens at http://localhost:8050/recipes/, and the family checks test it too.
- The home page stays as it is. To add the new site to Contents as well, run it again with `--add-to-home` at the end (or ask Claude).

Made one by mistake? `python -X utf8 tools/new_site.py recipes --remove` takes it out of the family again. It never deletes the folder; it tells you how, if you want to.

## 3. Make it yours

Open a Claude chat in the new folder (it has its own notes, `CLAUDE.md`) and say what the site is for. Then:

- **Words:** `site/js/data.js`, your own words in place of the placeholders.
- **Look:** `site/site.css`; the colours are at the top. Claude can build looks into the page for you to click through.
- **Pages:** `site/js/app.js`.

## 4. Putting it on GitHub (only when you say so)

Nothing goes on GitHub until you decide. A public repo can be read by anyone. When you’re ready, the command prints these steps (or Claude can run them with your OK):

```
cd Documents\JemmasJournals\recipes
& "C:\Program Files\GitHub CLI\gh.exe" repo create jemmathornton/recipes --public --source . --push     (or --private)
cd ..
git submodule add https://github.com/jemmathornton/recipes.git recipes
git commit -m "Add Jemma’s Recipes as a submodule"
```

Then it’s part of the family like the Library and the others, and its weekly backup can be set up the same way.

Pictures of a test site made this way: `for-jemma/concepts/new-site-template/`.
