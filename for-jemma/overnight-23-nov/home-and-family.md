# Home and the family: overnight review (22–23 Nov)

Home page, the shared family code (footer, dark mode, Menu drawer, Back to top), the family tools, the new-site template and the notes. The PC restarted overnight, so this was finished on the evening of 23 Nov. Home looks the same. Only the shared footer code it loads changed, invisibly.

## What I fixed

- **Back to top and Dark mode were nameless while a page was still loading** (found in the Sim World review). On a slow load the four apps showed both footer controls empty until the shared `family.js` arrived, so a screen reader met them with no name. The same happened for one frame when a site drew its footer later. Now `mode.js` names them as soon as they are on the page, and `family.js` fills them in at once. I reproduced it with `family.js` held back by 2.5 s: before, the four apps had no names; after, all five sites did. There is a new test for it in `tests/family/family.test.js`. Nothing looks different. Commit `7c54ab5`.
- **The new-site template didn’t follow two of the round 5 family rules.** “← Jemma’s Journals” in its drawer was 32px tall (the other four sites: 44px, using the shared `jj-home-link`), and its drawer width used 84vw (the family’s is 86vw). Both fixed, with a new check in its `tests/check_site.js`. I tested it on a throwaway site in a temp folder: 178 passed. No real site was made.
- **Notes that had drifted from the code:**
  - `/check-all` and `/family-change` said `--quick` runs each app’s tests and needs the 8050 server. It does neither: it runs home, the family rules, the tool tests, accessibility and git, on its own test server.
  - `ARCHITECTURE.md` said the same about `--quick`. It was also missing the new-sites step of the daily backup, the family and tool test suites, and what `new_site.py` sets up. Home’s check also runs at 1000 wide.
  - `CLAUDE.md`: two facts only. Home’s check runs at 1000 wide too, and the full list of what `new_site.py` sets up. None of your decisions changed.
  - `site/family/README.md`: on your PC the family server’s dark-mode choice wins, and which tests to run after a change.
  - `tools/weekly.py`: its notes listed the steps in a different order from how they run.

The template and notes fixes are in commit `e3ca3c7`. Both commits are pushed.

**Final quick check** (`tools/check_all.py --quick`):
- Home: 157 passed.
- Family rules: 26 passed.
- Tools: 80 passed.
- Library and Sim World: tidy in git.
- The Pokédex (1 file) and Travels (7 files) had uncommitted work from their own helpers, so their git checks showed as failed. That isn’t a problem with the sites.
- The accessibility report found one kind of problem: low contrast on the Pokédex’s small box labels (Male, Lucky, XXL …). That is the Pokédex helper’s to look at.

## The daily backup

- It didn’t run at 09:30 (the PC was off) and caught up at 14:44. Result 0 (fine). Library and Pokédex were backed up, Sim World wasn’t due (last good run Sun 22 Nov), there were no new sites and nothing new in Travels.
- Travels was **not recorded** in Jemma’s Journals because it had uncommitted changes (another helper was working there). The next run records it once that work is committed.
- Next run: 24 Nov 09:30.

## Needs your decision

**The phone top bar isn’t a named page area for screen readers** (found in the Travels review). Below 900px each app shows a slim bar with Menu and its name. The accessibility check says it sits outside the page’s named areas (header, menu, main, footer). That makes it a little harder to reach when jumping from area to area with a screen reader. This is a moderate problem, not a serious one, and nothing looks wrong.
- It comes from each site’s own page, not from the shared family code. The Library, Sim World, the Pokédex, Travels and the new-site template each have a plain `<div class="topbar">` in their own `index.html`. The family code only puts the icon and the word into the Menu button. Home has no top bar.
- The fix would be one line in each of the five pages: mark the bar as a menu area with a name, e.g. `<nav class="topbar" aria-label="Menu">`. It stays a plain `div` on screen, so nothing looks different. (Making it a second “header” would clash with the sidebar, which already counts as one on some sites.)
- Options:
  - **A.** Leave it.
  - **B.** Fix it on every site and the template, with a check in the family tests. My suggestion (not decided).

The rest of the shared code needs no choice from you. One small thing for the Pokédex (its own helper is reviewing that folder, so I didn’t touch it):
- On phones and narrow windows (899px and below), a small heading on the Pokédex home (`header > .label`) has contrast 4.09:1, below the 4.5:1 the family aims for, in light and dark. Options:
  1. Darken it in light and lighten it in dark until it reaches 4.5:1, keeping the same colour family. My suggestion (not decided).
  2. Make the label bigger or bolder so the lower contrast is allowed (large text only needs 3:1).
  3. Leave it as it is.

## What was fine

- **All five sites at 1600, 1280, 1000, 901, 899 and 390 wide, light and dark** (home, the Library, Sim World, the Pokédex, Travels and the not-found page), through a test copy of the family server. Her own server and dark-mode file weren’t touched. Results:
  - no errors and no security-policy blocks;
  - no sideways scrolling;
  - every page opens in the mode it was set to;
  - Back to top and the Dark mode button are level, 44px tall and show the keyboard focus ring;
  - contrast is fine everywhere apart from the one Pokédex heading above.
- **The Menu drawer on all four apps at 899 and 390:** it opens from the keyboard, focus goes inside it and stays there with Tab, and Escape closes it and puts focus back on Menu. It is the family’s 300px wide, and “← Jemma’s Journals” is 44px tall. The Menu button is hidden at 901.
- **The online-style copy** (`tools/build_site.py`: 11,413 files, 383 MB) served from a plain test server on a spare port, then stopped. Every site loads light with no errors at 1600 and 390, and missing pages get the 404 page.
- The family tools (`serve_all`, `record_apps`, `weekly`, `build_site`, `new_site`, `open_site`, `backup_new_sites`, `restart_family`): no bugs found. Tool tests: 80 passed.
- `new_site.py` dry runs (`--dry-run`, `--add-to-home`, `--remove`, and a folder name that isn’t allowed) behaved as they should and changed nothing.
- The not-found page’s links all work from any address.
