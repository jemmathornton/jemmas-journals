# Jemma’s Travels: overnight review (23 Nov)

Every page (home, trips by year and by country, a year, trips, posts, map, continents, countries, stats, timeline, search, Write, Not found) at 1600, 1280, 1000, 901, 899 and 390 wide, light and dark. Nothing was saved: the Write page was only looked at.

## What I fixed

- **Photo markers next to words.** The guide and the Write page say to put a marker like `[photo 2 right]` “on a line of its own”. But it only worked with an empty line above and below it; with words on the very next line, the marker showed up as text in the post. Now a line of its own is enough. None of your posts changed.
- **Tidying:** removed some unused style rules (an old comment box and an old countries layout) and two old screenshot tools for choices you’ve already made.

Commit: b02678d in Travels (pushed). All 110 of Travels’ tests pass.

## Needs your decision

1. **“Longest gap” on Stats** says “11 years, 2012 to 2023”, but the Timeline says “2013 – 2022: no trips” (10 years). Options:
   - A: keep it as now (years between the two trips: 11)
   - B: count only the years with no trips (10, “2013 to 2022”), matching the Timeline (my suggestion, not decided)
2. **The top bar on phones** (Menu and the name) isn’t marked as a page area for screen readers. It’s a small thing, and it’s the same on all your sites, so it would be one change for the whole family. Options:
   - A: leave it
   - B: mark it as a page area on every site (my suggestion, not decided)

Still open from before, unchanged: long trip names cut with “…” in the sidebar (the full name shows on hover), the small trip map at 901–1000 wide, and trips across New Year.

## Checked and fine

- No errors, broken pictures or broken links on any page, in either mode.
- Nothing too wide for the screen, nothing overlapping, no text cut off (apart from the sidebar names above).
- Contrast is at least 4.5:1 everywhere, in light and dark (checked with an accessibility checker at 1600, 899 and 390).
- Pages appear quickly: under 40 ms to change page, under half a second to open.
- Figures match the trips: 11 trips, 13 countries, 4 continents, 5 years; busiest years 2024, 2025 and 2026 (3 each); September the busiest month (5); distances (e.g. Strasbourg 1,610 km, Italy 3,040 km there and back from Birmingham).
- Dates read correctly (“November – December 2025”, “Days 11–12”).
- Light by default; dark mode the same as before; footer, Back to top and the Menu on phones as the family rules say.
- All 110 of Travels’ own tests pass.
