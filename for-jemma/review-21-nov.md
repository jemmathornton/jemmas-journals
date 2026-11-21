# Review of all five sites (21 Nov, while you were away)

Separate reviewers checked each site (Journals, Library, Sim World, Pokédex, Travels) and how they work as a family. They only read; the full reports are in `research/reviews/`. Then I fixed the clear-cut problems.

## Built today
- **Library:** Bound book look (laptop and desktop, light and dark). Phone mode: its own session.
- **Sim World:** the town plan look (lot cards in the world colour; plan paler over maps), light and dark.
- **Pokédex:** cards in a binder, with the softer shiny, light and dark, plus a **Menu** drawer on narrow windows.

## Fixed after the review
- **Home page:** a hidden error with many places; Back to top now takes keyboard focus to the top; the empty space under the footer; bigger tap areas for Back to top and Dark mode; "Placeholder" tags on the Pokédex and Travels lines; a credit for the Travels map shapes (Natural Earth); the phone bar colour follows dark mode.
- **Sim World:** world banner descriptions were cut off at 1280 wide (now they always show); dark-mode badges and the calendar chip were unreadable; an empty column on worlds with 2–3 neighbourhoods; house names drawn like lot sizes; search box focus; the phone menu now closes with Escape and keeps the keyboard inside it; “1 download” (not “1 downloads”).
- **Pokédex:** Pokémon pages scrolled sideways at 900–965 wide; the banner tab labels shrank to 7px and were cut short (now never under 10px and never cut, in rows on narrower screens); banner words ran under the maps (on phones the maps are now a band above the words, which you haven’t seen yet: say if you’d like it different); What’s on works on a phone; card box labels no longer end in “…”; dark-mode red text readable; grey text slightly darker; gold keyboard focus in the sidebar; bigger tap areas; the page stays put behind the open menu.

Every app’s own tests pass after the fixes, and everything is committed and pushed. Before and after pictures: `for-jemma/concepts/app-styles/built/fixes-21nov/`.

## For the Library’s own session (paste after its phone mode is done)
From `research/reviews/library.md`. Nothing was broken; these should be fixed:
1. The figures row wraps at 1280 wide (the last figure drops to its own line) on 9 pages.
2. Grey text is slightly too faint in light mode (4.4:1; needs 4.5:1), and the “Book n of …” link is 3.7:1.
3. The big first letter splits numbers (“2” then “0 years”) and sits after a quote mark on 16 blurbs.
4. Stats still has the old dark walnut panels.
5. The Children’s shelf card is hard to read (gold on mustard).
6. Old books shelves in dark mode keep cream boards; “to find” titles nearly vanish.
7. The reading font is 2.6 MB; web versions would be about 0.3 MB in all (needs a small tool installed: your OK).

## For the Travels session
From `research/reviews/travels.md`. Its figures all check out against your data. To fix:
1. The Write page is too wide on phones.
2. On your PC the “← Jemma’s Journals” link doesn’t reach home (Sim World’s way would work).
3. One sentence in the Japan sample post isn’t yours and isn’t marked as a placeholder.
4. Maps cut off places you went (the Canaries/Tenerife, Hokkaido).
5. Photo location data: nothing strips it yet, and the repo is public. Needs doing before the first real photo.
6. Stats counts the 13 sample posts as written.
7. Small grey text is too faint in places; the September label is unreadable on its dark cell.
8. A working note shows on the page: “(your choice, 21 Nov)” on the comments box.

## Across the family
- **On your PC you can’t move between the sites yet:** home’s Open links aren’t connected, and the apps’ back links only reach home from Sim World. Online under one address, they all work (tested).
- **Small mismatches:** Travels has no dark mode or tab icon; only home and Travels ask search engines to stay away (the three apps would need the same tag before going online); the Library loads two fonts from Google while the others keep them locally.

## Questions for you
1. **Dark mode across the family:** home always opens light (your choice); the apps follow your device; Travels has none. On a phone set to dark you’d flip between light and dark as you move round. Keep it, or make them all open light like home?
2. **Do Sim World and Travels look too alike?** They’re the closest pair (pale grid sidebar, pale page, plan/map banner); colour keeps them apart. See `research/reviews/family-laptop.jpg`.
3. **Sim World:** one-word world titles are all gold and hard to read on bright maps (Britechester, StrangerVille). Brighter gold, white, or part gold? Should the lot, Sim and household pages get the town plan style too? Should the greyed “not owned” worlds be stronger?
4. **Pokédex:** should the shiny foil show on a grey, not-caught card (Mewtwo, with one form shiny)? Should a background card’s art stay in colour when not caught? Searching while “Hide ones I have” is on shows nothing: should search ignore that switch?
5. **Library:** the Display shelf card is now dark green (your no-green rule); keep the big first letter on blurbs that start with a quote mark?
6. **Home page:** with your four places, the 2 × 2 cards are narrower than the headings; and the footer says “Made with plain HTML and CSS” though the page needs JavaScript. Change the wording, or leave it?
7. **Menu button word:** Library “Shelves” (in its new phone mode), Sim World “Worlds”, Pokédex “Menu”, Travels an icon. One word for all, or each its own?
