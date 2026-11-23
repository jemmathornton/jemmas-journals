# The overnight review (22–23 Nov): start here

The PC restarted overnight, so the review stopped partway and was finished on the evening of 23 Nov. Every site was checked at six widths (1600, 1280, 1000, 901, 899, 390), in light and dark. The full details for each site are in the other files in this folder.

## Fixed (tested and pushed)
- **Library:** search said “47 books” for Pratchett where his author button says 46, because it counted copies; it now counts each book once. Some styling nothing used any more was removed.
- **Sim World:** no real bugs. Some leftover code nothing used was removed, with a test that catches any more.
- **Travels:** a photo marker like `[photo 2 right]` needed a blank line above and below it; with words on the next line it showed as text in the post. A line of its own is now enough. None of your posts changed.
- **Pokédex:** every cap Pikachu is now male in Pokémon HOME (they wrongly had a Female box). Your ticks were untouched. Your Pokédex HOME chat has the review’s other notes and is fixing them itself.
- **Shared family code:** on a slow load, the footer’s Dark mode and Back to top buttons were briefly nameless for screen readers on the four apps. Fixed, with a test.
- **New-site template:** the drawer’s “← Jemma’s Journals” link was too small to tap. Fixed.
- **Notes:** ARCHITECTURE.md and the guides had drifted from the code, so they were corrected.

## For you to decide
Every option is in each site’s file. In brief:
1. **Library, Dystopia bookend:** pick from the picture sheet `for-jemma/concepts/app-styles/built/round5/library-dystopia-options-light.jpg` (and `-dark`).
2. **Library, old-book spines on mid-tone cloth** are slightly hard to read. Leave / a soft shadow behind the lettering (my suggestion, not decided) / a paper label.
3. **Library, frames on their own ledges** (narrow windows and phones) split unevenly, like 4 + 1. Leave / share out evenly (my suggestion, not decided) / smaller frames on one ledge.
4. **Library, page counts:** 43 books still need a count. Google Books refused without a key. Options: your own free Google Books key (my suggestion, not decided) / UK shop listings / leave them.
5. **Library, cover shapes:** `library/for-jemma/cover-shapes-to-check.md` lists 75 books that don’t match their group’s shape and 40 covers with edges to look at.
6. **Sim World:** long household names in family-tree cards are cut with “…”; let them wrap (my suggestion, not decided)? Fountainview Penthouse has no lot size. Four partner links go one way only (pages read correctly).
7. **Travels:** Stats says the longest gap is “11 years, 2012 to 2023”, but the Timeline says “2013 – 2022: no trips”. Keep / count only the empty years, 10 (my suggestion, not decided).
8. **All sites, phone top bar:** screen readers don’t treat the Menu bar as a page area. Leave / fix on every site (my suggestion, not decided).
9. **Pokédex:**
   - Five box colours are just under the contrast aim with white text: Male, Purified, XXL, 4★ and Mega.
   - HOME’s teal is still only a suggestion.
   - Alcremie’s form names are cut short.

## Backup
Today’s backup ran at 14:44, not 09:30, because the PC was off. It finished fine.
