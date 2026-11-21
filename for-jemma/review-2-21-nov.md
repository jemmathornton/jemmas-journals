# Second review of all five sites (21 Nov, evening)

The same reviewers checked every site again, plus how well they work as a family. Full reports: `research/reviews/round2-*.md`. Every fix is committed and pushed, and each app’s own tests pass.

## Fixed
- **All five: the family rules, now exact.**
  - Dark mode is shared through `jj-mode`, so it carries from one site to the next.
  - Every site has the same footer.
  - The Menu drawer opens on the page you’re on, never on “← Jemma’s Journals”. Tab stays inside the drawer while it’s open. The scrim dims the page the same on every site.
  - Same name size in the bar on every site.
  - Every site keeps out of search engines and AI.
  - Every site uses its own copies of its fonts.
- **Home** (5fcead0, 1aceb40):
  - The not-found page now follows the family rules.
  - The Open links go to each app’s online address. On your PC a note says “opens here once the sites are online”.
  - A credit dot never starts or ends a line.
- **Library** (2b0e4bd):
  - Fonts now come from the Library’s own folder, not Google.
  - Between 901 and 1100 wide, headings, Stats and the title page fit.
  - The big first letter skips a leading number.
  - Pale shelf cards are darker.
  - Old-book shelves go dark in dark mode.
- **Sim World** (42d49cf): the family rules, plus the review’s smaller fixes.
- **Pokédex** (5e7f309):
  - **Kanto’s tabs now match the other regions.** Kanto alone was switching to big tabs because “Gigantamax” needed a fraction of a pixel more room. Every region and Every Pokémon now lays its tabs out the same way: one line on your laptop, the same rows when narrower. Checked in your app at 1600.
  - The evolution family stacks downwards on narrow pages. Branches like Eevee’s each sit in a light frame.
- **Travels** (a39277d):
  - The Map tracker no longer breaks between 900 and 1100 wide.
  - Japan’s page shows all its islands.
  - Pale text is now readable everywhere.
  - “Written so far” counts only your real posts (0 for now).
  - Photos with location data in them are refused, so none goes online by accident.
  - “← Jemma’s Journals” reaches home on your PC.

Screenshots: `for-jemma/concepts/app-styles/built/round2/`.

## Your questions (nothing changed until you say)

**All sites**
1. The footer says “Made with plain HTML and CSS”, but the apps also use JavaScript and the Pokédex and Library need a small server. Keep the words, or change them?
2. Credit lines a helper wrote that need your OK: Sim World “Screenshots and Gallery pictures are my own”, Travels “Photos are my own”, Library “Some book details from Open Library”.

**Home**

3. With four places in 2 × 2, the cards are narrower than the headings. Fine, or widen them?
4. Pictures (parked), your Introduction words and the place lines (placeholders for now).

**Sim World**

5. Gold one-word titles on bright maps can be hard to read.
6. Should lot, Sim and household pages get the town-plan look too?
7. The calendar on a phone.
8. The italic name in the bar: purple or gold?

**Pokédex**

9. At 1280 wide the tabs now sit in two rows, because one row would cut “Gigantamax” below 10px. You asked for one small row: is two rows OK there? (On your laptop window it’s one line.)
10. Should “Hide ones I have” be on or off when the app opens?
11. How should search behave when Hide is on?
12. The white text on the Lucky box.
13. Should the foil show on cards you haven’t caught?
14. The background art colour.

**Library**

15. The Display shelf card is green. Keep it?
16. Skip the big first letter after a quote mark?
17. What should happen when the server isn’t running?
18. Can I install a small tool (fontTools) to shrink the EB Garamond font from 2.5 MB to about 0.3 MB?

**Travels**

19. “Favourite month”: keep it?
20. “You” or neutral wording?
21. Should home list all trips?
22. Distances by place?
23. Writing from your phone.

## Your answers (21 Nov, late)

**Decided, to do**
- Footer line 1 on every site: “No cookies, no tracking, no ads. Made with HTML, CSS and JavaScript, kept on GitHub.”
- Helper-written credits: no preference, left as they are.
- Pokédex tabs at 1280: one row, smaller text allowed (below 10px).
- Pokédex “Hide ones I have”: always off when the app opens.
- Pokédex search: shows everything matching, even with Hide on.
- Pokédex foil: only once the Shiny box is ticked.
- Library font: install fontTools and shrink EB Garamond (2.5 MB to about 0.3 MB).
- Library with no server: read-only, quietly (edit buttons hidden).
- Travels: remove “Favourite month”; neutral wording instead of “you”; home keeps every trip; total distance on each trip’s page; look into writing from a phone (research only).
- Sim World: world titles stay as they are (fade + shadow); phone calendar stays as it is.

**Show me both (a Try switch in the running app, opened in the browser)**
- Home: place cards as now vs widened to the headings. **Reminder: still to check.**
- Sim World: lot, Sim and household pages with the town-plan look. **Reminder: on the to-do list.**
- Sim World: the italic name in the bar, purple vs gold.
- Library: big first letter after a quote mark, skipped vs kept.
- Library: Display shelf card green vs matching the others.
- Pokédex: Lucky box, white vs dark text.
- Pokédex: card art, region colour vs type colour.

**Parked:** home pictures, Introduction words and place lines.

## Built (21 Nov, late): things to check with the Try switch (bottom right)
1. Home, Contents: place cards **As now** or **Widened** (http://localhost:8040).
2. Sim World, a lot, Sim and household page: **As now** or **Town plan** (e.g. #l-willow-creek--crick-cabana, #s-dustin-broke, #h-willow-creek--goth on http://localhost:8045).
3. Sim World: “Sim World” in the sidebar **Gold** or **Purple**.
4. Library, Wild Boar (#b-to2ynr193y): big first letter after a quote mark **Kept** or **Skipped**.
5. Library home: Display shelf card **Green** or **Like the others** (walnut brown, my suggestion, not decided).
6. Pokédex, Kanto (#gen-1): Lucky box text **White** or **Dark**.
7. Pokédex, Kanto: card art **Region colour** or **Type colour**.
Also new to look at: Pokédex tabs in one row at 1280; more room under the tags on Pokémon pages (e.g. #p-6); Travels trip pages show the distance.
