# Library: overnight review (23 Nov)

I checked every kind of page at 6 widths (1600, 1280, 1000, 901, 899 and 390), in light and dark: 348 page views in all.

## What I fixed

- **The search count counted every copy, not every book.** Searching “pratchett” said “47 books”, but the Terry Pratchett button beside it said 46. Your rule from 21 Nov is that every figure counts each book once, so the search count now does too. All the copies still show in the results. I added a test for it.
- **Old styles that nothing used any more** are gone from site.css. They were the old reading date boxes and star picker, plus two leftovers from the shelf work. Nothing looks different.

Both are in commit 0af64b6 (pushed). The full test suite passed: 349 tests, all OK.

## What needs your decision

1. **Some old-book spines are a little hard to read.** On mid-tone cloths (a grey-blue, for example), neither the gold lettering nor the dark lettering is quite dark or light enough against the cloth. Those come out at about 3.9–4.1 to 1, and the aim is 4.5 to 1. It’s worst on the small series numbers. 32 old books have no cloth colour recorded, so they use the plain brown, and their numbers fall in this range too.
   - A: leave it as it is.
   - B: add a soft shadow behind the dark lettering and the numbers, like the gold titles already have. The cloth colours stay the same. *My suggestion (not decided).*
   - C: put a small paper label with the title on each spine, like a library label.
2. **Frames on their own shelves.** When the window is too narrow for the frames to stand among the books, they go on shelves of their own above the books. This happens at about 901–1150 wide and on phones. They then split unevenly: on a shelf page at 1000 wide it’s 4 frames and then 1 on its own shelf, and on Home at 901 it’s 3 and then 1.
   - A: leave it.
   - B: share them out evenly, so 3 + 2 or 2 + 2. *My suggestion (not decided).*
   - C: make the frames a little smaller there, so they all fit on one shelf.
3. **The Dystopia picture on the bookends.** The Try switch is still on the Dystopia page, as you left it. Pick one of: Clock (now), Security camera, Watchtower, Loudspeaker, Gas mask, Dead tree, Ruined skyline, or Padlock and chain.

## What I checked and found fine

- **Errors:** no errors in the browser console, and no missing files or pictures, on any page.
- **Speed:** every page opened in about 1.1 seconds or less, most of them in about half a second.
- **Layout:** nothing runs off the side of the page, and nothing is cut off or overlapping. That includes the header shelf, frames and bookends on every shelf, Home, All shelves, Authors, Stats, History, Reading and To buy, at every width. The bookends sit right against the end books, and only whole spines are shown.
- **Contrast:** apart from the old-book spines above, no text was too faint anywhere, in light or dark.
- **Keyboard:** Tab reaches everything and every item shows where you are, on Home, a shelf, a book page, the Add page, the old books and the phone layout. “What should I read next?” keeps the keyboard inside its box, and Escape takes you back to the button.
- **Menus and switches:** the phone menu, filters, sorting, covers or list, the A–Z, search, and the old books’ shelves all work. The New covers switch shows only on the old-books pages, and the Dystopia Try switch only on the Dystopia page.
- **Light mode:** every page opens in light mode.
- **Your checks:** your data check found no problems (648 books). The cover shapes list is unchanged (75 books in 33 groups, 40 covers with edges to look at), still waiting for you in `library/for-jemma/cover-shapes-to-check.md`.
- **One small thing I left alone:** the order of the header’s books is set from the date in UTC. In summer the order can change at 1am instead of midnight. You won’t notice it.
