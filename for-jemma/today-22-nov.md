# 22 Nov (afternoon): what changed

Everything is tested, saved and pushed. The full check passes on every site:
- **Home:** 157 checks.
- **Shared family tests:** 25.
- **Tools:** 79.
- **Library:** 338.
- **Sim World:** 399 + 118 (on a rerun: the first run timed out with the PC busy).
- **Pokédex:** 98.
- **Travels:** 109.

## How things run now
- **One daily backup at 09:30** (“Jemma’s Journals - backup”), with no sign-in popups. It backs up the Library, Pokédex and Travels posts every day, and runs Sim World’s Gallery refresh on Sundays (or the next day the PC is on).
- **Your shortcuts** open each app through http://localhost:8050, which starts at login.
- **Old folders:** they couldn’t be deleted because something still had them open. Close your old app chats, then ask me.
- **GitHub:** all five repos are protected; `main` can’t be deleted or overwritten.
- **New PC:** `tools/setup_pc.ps1` sets everything up again (see `new-pc.md`).
- **New site:** `tools/new_site.py` makes a new site from a template, already wired in (see `new-site.md`).
- **Going online:** `tools/build_site.py --serve` shows the online version at http://localhost:8060.
- **For future work:** a guide (`ARCHITECTURE.md`) and ready-made commands for future Claude sessions (status, check-all, record, new-site, family-change).

## Your picks today
- **Home:**
  - the cloth journals (no numbers), all pictures the same landscape shape;
  - pictures aren’t links, don’t move and can’t be selected;
  - softer black corners on the plain mat.
  - The overall look is parked, as you said.
- **Library:**
  - one header with the title, figures and covers;
  - no ornament line;
  - the stars back on the cover, with no shadow under it;
  - Stats in the bound-book look;
  - smaller pictures (All shelves 105 MB → 17 MB);
  - A/S/L and the other title fixed.
- **Pokédex:**
  - dark-mode art Brighter;
  - Shiny and Lucky a little deeper;
  - tabs in one row at every laptop width;
  - Every Pokémon no longer freezes (10 s → 0.06 s);
  - the event card the same width as the others;
  - the date off Home.
- **Sim World:**
  - purple banner name;
  - town plan on Sim pages;
  - initials in the world’s deep colour;
  - lot pages load 3 photos up front, not 23.
- **Travels:**
  - Canada now in “Canada and Boston” (14,140 km);
  - failed saves fully undone;
  - dates checked;
  - full trip names on hover.
- **All sites:**
  - phone fixes (back keeps your place, bigger tap targets, no zoom on tap, room for the notch, swipe to close the menu);
  - a security policy so only the site’s own code runs.

## Waiting for you
1. **Library: covers in the header.** Pick one of As now, Shelf, Spines, Fan, Row or Stack (Try switch, bottom right).
2. **Library: two covers with white borders** (*The New School at Scawdale*, *A Visit From the Goon Squad*). Crop them?
3. **Library: the Shelf option.** Keep the books at varied heights, or make them all the same height?
4. **Pokédex for more games:** your choices are in `pokedex-more-games.md`.
5. **Sim World data:** four partner links only go one way, e.g. Gunther Goth → Cornelia. The pages still read correctly, so I left them.
