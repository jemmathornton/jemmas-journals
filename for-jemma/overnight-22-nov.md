# Overnight, 21–22 Nov

Everything below is done, tested, committed and pushed. Each app’s latest version is recorded in Jemma’s Journals.

## What changed

**1. The shared code now lives in Jemma’s Journals** (`site/family/`). All five sites load these from there:
- dark mode, and the Dark mode button;
- the footer’s first line, Back to top, and the credit dots (a “·” never starts or ends a line);
- the Menu drawer on narrow screens.

Fix one of these once and every site follows. Each site still has its own look. Before/after screenshots match apart from the fixes.

**2. How you open the sites now.**
- Your Library, Sim World and Pokédex shortcuts open through the family’s one address, http://localhost:8050.
- A new entry in your Startup folder, “Jemma’s Journals server”, starts that address when you log in. It also starts the Library, Pokédex and Travels save servers.
- Dark mode now carries between all your app windows, even though each window keeps its own taskbar button.
- Home’s Open links work on your PC too.

**3. Two reviews of every site** (round 3 before the work, round 4 after). Everything they called broken or worth fixing is fixed, except the look changes, which are listed for you below. Fixes include:
- **Home:** it opened shrunk on phones (it was missing a page header). The credits also left empty gaps on phones.
- **Family server:**
  - pictures sometimes failed to load under load;
  - saves through it were 2 seconds slow;
  - it now refuses other sites’ names and shows the not-found page;
  - the top-bar colour stuck on dark gold after switching back to light.
- **Library:**
  - “Witne”: long titles were cut off;
  - the home link when opened as a file;
  - read-only now really is read-only;
  - easier-to-read old-book spines and missing-book rows (using your colours);
  - the weekly backup is safer.
- **Sim World:**
  - its Claude notes backup still read the old folder;
  - the sidebar now marks the page you’re on;
  - keyboard focus after choosing a link;
  - the faint “Not owned” list and initials are easier to read;
  - the shortcut kept in its folder.
- **Pokédex:**
  - **a security hole:** a crafted link could run script and change ticks (this was there before tonight);
  - the shortcut in its folder still opened the old copy;
  - Tabler added to the icon credits;
  - dead trial code removed;
  - it shows view-only, quietly, once it’s online without its save server;
  - its keyboard focus is fixed.
- **Travels:**
  - Save no longer works for a few seconds when the save server is off;
  - broken addresses now show Not found;
  - placeholder posts no longer say “you” (e.g. “Where you were” is now “Where this was”).
- Your ticks and Library data were never touched (checked by fingerprint).

**4. New tools in Jemma’s Journals**
- `tools/check_all.py` runs every site’s tests and checks git, all in one go.
- `tools/record_apps.py` records each app’s new version in Jemma’s Journals. The weekly backups run it.
- `tools/open_site.pyw` is what the shortcuts run.

## What you need to do

- **Start each app’s chats from its new folder**, such as `Documents\JemmasJournals\pokedex`. The old chats point at the old folders.
- **Old folders:** `Documents\HomeLibrary`, `SimTracker`, `Pokedex` and `Travels` are still there and unused. Delete them only when you’re happy.
- Today’s weekly tasks (Sim World 07:54, Library 09:30, Pokédex 09:40) are the first to run from the new folders. I’ll check their logs if you ask.

## For you to decide (looks: nothing changed)

**All sites**
1. The footers still differ in small ways:
   - Sim World’s pin divider is half cut off at the top;
   - the Pokédex footer has the binder’s shaded strip;
   - only the Library has the ❦;
   - heights vary;
   - the dots are faint (3.8:1 on Travels).

   Make them match more closely?
2. On phones, the footer’s first line and the credits run together. Add a little space between them?

**Library**

3. The ornaments ❦ ❧ and the ← arrow use Windows’ symbol font. EB Garamond has nicer versions.
4. The stars ★ use the symbol font too; the empty stars are very faint. Keep them, or use a star icon?
5. A few old-book spines still read only 3.4–4.1:1. Add a label, or adjust the cloth?
6. Still open from before:
   - the sidebar runs below the fold at 1280×800;
   - “ISBN-13” in small capitals;
   - justified blurbs leave wide gaps;
   - “Got It” on the buttons vs “Got it” in the sentence;
   - the Stats panel is rounded on phones;
   - the New covers switch sits above the drawer’s dimming.

**Sim World**

7. The home banner still says “Sim World” in gold; the sidebar is now purple. Purple there too?
8. Group cards and family-tree cards on Sim pages are still rounded, while the rest is square town plan.
9. Still open: gold one-word world titles on bright maps, and the calendar on a phone.
10. Five world colours (Tomarang, Gibbi Point, StrangerVille, Henford-on-Bagley, Tartosa) can’t be read with white or dark letters on their initial discs. A helper nudged those discs slightly darker or lighter. OK, or use each world’s deep colour?

**Pokédex**

11. With a tab on (e.g. Lucky), a search only finds Pokémon that can have that box. Should a search ignore the tab?
12. In dark mode the type tint behind the Pokémon is quite muted.
13. Delete the unused scenery pictures in `site/regions/`?

**Travels**

14. Long trip names in the sidebar are cut with “…”. Wrap them, or show the full name on hover?
15. Between 901 and 1000 wide, the trip map is small beside the title.
16. In dark mode its menu dimming is deep blue at 60%, not black at 45% like the other sites.

**Wording**

17. The footer says “Made with HTML, CSS and JavaScript”, but the Library and Pokédex also need a small Python server to save. Keep the line as it is?

## Ideas from tonight’s research (`research/improvements-22-nov.md`)

1. **Smaller pictures on the Library and Pokédex home pages.** On a phone they download 10–13 MB; this would bring them to 1–2 MB and look the same.
2. **Going online:** one publish step from Jemma’s Journals. It would first go up at jemmathornton.github.io, then move to your domain when you buy it.
3. **An automatic accessibility check** (axe-core) in the check-everything command. It needs your OK to download it (3.3 MB, free).
4. **Protect the GitHub copies:** stop `main` being deleted or overwritten. You turn this on in GitHub’s settings.
5. **More frequent backups** for your ticks and books (daily, not weekly).

## Final check (22 Nov, early morning)

`tools/check_all.py`, run after all the work:
- **Home:** 104 checks passed.
- **Library:** 331 tests.
- **Sim World:** 396 Python and 115 page tests.
- **Pokédex:** 97 tests and 72 page tests.
- **Travels:** 100 tests.

All pass. The first run found two footer tests still expecting the old way of hiding a line-end “·”; I updated both and they pass now. All five repos are on main, nothing uncommitted, everything pushed and recorded.

The servers were restarted the way Windows will start them (the Startup shortcut). All four answer (8050, 8020, 8030, 8041), and the five sites load through http://localhost:8050 with no errors.

Before/after screenshots: `for-jemma/concepts/app-styles/built/round3/`. Review reports: `research/reviews/round3-*.md` and `round4-*.md`.
