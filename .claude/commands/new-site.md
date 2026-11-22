---
description: Add a new site to the family with tools/new_site.py, asking her the name and colour, dry run first
argument-hint: "[folder] [Name] [#colour]"
---
Help Jemma add a new site to her family with `tools/new_site.py` in `C:\Users\Jemma\Documents\JemmasJournals`. Read her guide `for-jemma/new-site.md` and the "Adding a new site" section of `CLAUDE.md` first.

Arguments so far: $ARGUMENTS

1. **Ask for what's missing**, in one short message that lists each item:
   - the name after "Jemma's" (her words, e.g. "Recipes");
   - the folder and address (suggest one from the name: lower case, hyphens for spaces; not one already used, such as site, family, tools, library, sim-world, pokedex, travels);
   - the colour as a hex code, or none for the quiet default blue (#3D6A8A);
   - whether to add it to the home page now (`--add-to-home`). A new place on home is her decision, and it stays a placeholder until she gives a picture and words.
   Label anything you propose as "my suggestion (not decided)". Don't invent wording for the site.
2. **Dry run:** `python -X utf8 tools/new_site.py <folder> "<Name>" "<#colour>" --dry-run` (plus `--add-to-home` if she said yes). Tell her briefly what it will create and change, and any colour it adjusted for contrast. Wait for her yes.
3. **Run it** without `--dry-run`. Restart the family server (8050) so the new address works, and open `http://localhost:8050/<folder>/` in the browser pane for her.
4. Run the new site's checks (`..\.tools\node\node.exe tests/check_site.js` in its folder) and, if home changed, `tests/check_page.js` in the parent (its "four places" checks then need updating; say so).
5. Commit only the parent files it changed (the `tools/*.py` it wired, `site/home.js` if changed), then push with the gh credential helper. The new folder has its own local git repo. **Don't create a GitHub repo or submodule** unless she asks: show her the commands the script printed.
6. Tell her what's next: open a Claude chat in the new folder to make it hers. If home changed, republish the home artifact.
