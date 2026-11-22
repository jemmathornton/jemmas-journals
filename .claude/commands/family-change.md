---
description: Make a change to the shared family code (site/family/) and test every site
argument-hint: "<what to change>"
---
Make this change to the family's shared code: $ARGUMENTS

Read first: `site/family/README.md`, `research/family-rules.md`, and the shared-code part of `ARCHITECTURE.md`. Every site (home, Library, Sim World, Pokédex, Travels) loads this code from `/family/`, so one change reaches all of them.

1. **Is it quiet?** `git status` and `git log --oneline -5` in the parent and each app. Leave alone any uncommitted work that isn't yours.
2. **Is it shared?** Only behaviour every site shares belongs in `site/family/` (dark mode, footer, Back to top, credit dots, Menu drawer). Colours and fonts stay in each site's `--jj-*` variables. If the change is really one app's look, stop and say so. If it changes how something looks, follow her show-don't-ask rule: build the options in with a Try switch, open it in the browser pane, and list every option.
3. **Change `site/family/` only.** If an app needs a change too, say which file and why, and ask first: each app has its own sessions and notes.
4. **Test every site:** `.tools/node/node.exe tests/check_page.js` for home, then `python -B -X utf8 tools/check_all.py --quick` (each app's own suite plus accessibility; needs the family server on 8050). Look at home and one app at 1600 and 390 wide, light and dark, through http://localhost:8050.
5. **Update the notes** if behaviour or markup changed: `site/family/README.md`, and `research/family-rules.md` if a rule changed (her decision, dated).
6. **Commit only your files** in the parent (message ends "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>") and push with `git -c "credential.helper=!'C:/Program Files/GitHub CLI/gh.exe' auth git-credential" push`. Republish the home artifact if home changed.
7. Report in plain words: what changed, which checks passed, and what she should look at.
