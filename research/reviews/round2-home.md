# Review, round 2: Jemma’s Journals home page (21 Nov 2026, evening)

Read-only second review of `concepts/index.html` and `concepts/404.html`, judged against CLAUDE.md and `research/family-rules.md`, and checked against the first review (`research/reviews/home.md`). Nothing in the project was changed apart from this file.

How: Edge via Sim World’s Playwright, page wrapped in a doctype skeleton from disk (as `tests/check_page.js` does), at 1600×930, 1280×800 and 390×844; device set to light and to dark; site mode light and dark (dark by setting `jj-mode=dark` **before** loading, to test the carry). Also `#more1`–`#more3`, keyboard, storage blocked, the old `jj-mode2` key, reduced motion, the 404 page with `jj-mode=dark`. Screenshots and `measure.json` are in
`C:\Users\Jemma\AppData\Local\Temp\claude\9cff366c1b60a8f8\2df2d807-e7a9-4322-8b41-c4059cb2ba00\scratchpad\review2\home\` (called `shots\` below). Script: `rev-home.js` in the folder above it.

`tests/check_page.js`: **99 checks passed, 0 failed.**

Overall: the home page is in good shape and nothing is broken. All the round-1 fixes held. It follows the family rules for dark mode and the footer, with one real gap: the 404 page ignores them.

---

## Round-1 fixes: did they hold?

| Round 1 | Now |
|---|---|
| 1 `#more3` error | **Held.** 7 places (3 + 3 + 1 centred), no errors, Dark mode works afterwards at all three sizes. `check_page.js` now covers it. |
| 3 Back to top focus | **Held.** Header has `id="top"`, `tabindex="-1"`; after Enter focus is on `#top`, `scrollY 0`, the next Tab goes to the first photo. |
| 5 Space under footer | **Held.** 56px (was 150). `env(safe-area-inset-bottom)` not added: harmless. |
| 6 Footer tap size | **Held.** Back to top 94×44, Dark mode 91×44, level (same top) at every size. |
| 7 Placeholder tags on place lines | **Held.** Pokédex and Travels lines carry the dashed PLACEHOLDER tag. |
| 8 Travels map credit | **Held.** “Country shapes from Natural Earth” is in the credits. |
| 9 Theme colour in dark | **Held.** `#6A4A17` in dark, `#8E6520` in light, swaps both ways. |
| 2 Four cards narrower than headings | Not changed: it is her open question 6 in `for-jemma/review-21-nov.md`. Still true (1600: headings x = 220, cards x = 420–1180). |
| 4 “plain HTML and CSS” though JavaScript builds the page | Not changed: same open question 6. |
| 10 Code leftovers, 11 unused pictures, 12 old 404, 13 icon sizes, 14 letterboxed maps, 15 404 wording, 16 toast says “your” | All still as described in round 1. 12 has grown into item 1 below. |

---

## Broken

None.

---

## Should fix

### 1. The 404 page doesn’t follow the family rules (no dark carry, no footer)
- **Where:** `concepts/404.html`.
- **What:** family rules: dark mode carries on every site via `jj-mode`, and the footer is “present on every page”. The 404 page has no mode script, no dark styles, no footer. With `jj-mode=dark` set, it still opens cream (`data-mode` null, body `rgb(244,238,227)`). So once online, someone browsing in dark who mistypes an address gets a bright page. It is also still the older cover (no gold corner brackets, no stitching).
- **Evidence:** `shots\404-390-dark.png`, `shots\404-1600-dark.png` (set to dark, shows light); `measure.json` → `404-*-dark`.
- **Fix:** give it the same small head script (read `jj-mode`, set `data-mode`, theme-color), the dark colour set and cover pieces from the home page, and the family footer (name, the two About lines, Back to top and Dark mode). Add a 404 check to `check_page.js` (opens dark when `jj-mode=dark`, footer present).

---

## Polish

### 2. Mode is set at the end of the page, not in a script before the styles
- **Where:** `index.html`: the `jj-mode` read and `applyMode()` are in the one script at the bottom.
- **What:** family rule 1 says a tiny script before the stylesheet sets `data-mode` on `<html>`. In practice no flash was seen: `#page` is empty until the script runs, and `data-mode` was already `dark` at `interactive` (`measure.json` → `paintSeq`). There is still a small risk of a cream frame on a slow phone, because the cream `html` background is styled before the script runs.
- **Fix:** move the 3-line read (`jj-mode`, then old `jj-mode2`, set `data-mode`) into a `<script>` at the very top of the fragment, before `<style>`. Do it properly in `<head>` when the page gets its real skeleton for going online.

### 3. Credits line on the laptop leaves “· Icons by Lucide” alone on a second line
- **Where:** footer, About this site line 2, at 1600 (and 1280).
- **What:** the six credits don’t fit on one line, so the last one wraps alone and the second line **starts** with a “·”. It looks unfinished under the full-width first line. The phone (one per line, no dots) is fine.
- **Evidence:** `shots\page-1600-light.png`, footer; the last credit sits at y = 1927, the others at y = 1905.
- **Fix (my suggestion, not decided):** `text-wrap:balance` on that line (3 + 3), with each dot kept on the same line as the credit before it, so no line starts with a dot.

### 4. Footer text is 12px on phones
- **Where:** `@media (max-width:760px){ .about-site{font-size:12px} }`.
- **What:** family rule 2 says 12.5px. Desktop is 12.5px. On phones it drops to 12px. Contrast passes (5.01 light, 6.0 dark).
- **Fix:** remove that override, or set it to 12.5px.

### 5. The “This would open …” toast uses another app’s colours and covers the footer
- **Where:** `.toast` uses `--sw-on` / `--sw-on-ink`, left over from the trial switch.
- **What:** in light it is navy `#1A1F2C`, in dark a blue-white `#ECEEF3`. Neither colour is on the page anywhere else. It sits 120px from the bottom, so when clicked near the footer it covers the credits line (`shots\toast-1600-dark.png`). It still says “your Sim World” where the page says “My”. It is only a placeholder until the real links are in, so low priority.
- **Fix:** when the real addresses go in, delete the toast and the `--sw-*` variables together. Until then, use `--ink`/`--bg`.

### 6. Code leftovers (unchanged from round 1)
- `--sw-*` variables, `ICON.plus` / `ICON.image` (unused), the “title on scroll” comment above `render()`, comments saying “navy cloth”, “round 9”, “As now (switch, bottom right)”, “Ideas to try (switch)”, `.intro` 180px column (overridden by `.v2`).
- New one: the Travels entry’s comment says “the picture is Travels’ own map (look A) until she picks a look”. Her Travels look is decided (Old Atlas), and `travels-map.*` (21 Nov 12:45) is the atlas map, so the comment is out of date.
- **Fix:** one tidy commit, then confirm the page is pixel-identical before and after.

### 7. `check_page.js` gaps
It doesn’t test the 404 page, and it doesn’t test loading with `jj-mode=dark` already set (it only tests click then reload, which is close but not the cross-site case). Worth adding both, along with the footer font size.

---

## Question for her

### 8. Open questions from earlier (not new, still waiting)
- Four cards narrower than the headings, and the “plain HTML and CSS” wording: question 6 in `for-jemma/review-21-nov.md`.
- Pokédex and Travels maps letterboxed in their photos (whole vs fill). In dark the black mat makes it read most like letterboxing, and the Johto/Kanto painting’s soft white edges show as pale bands against it (`shots\page-1600-dark.png`).
- 404 wording (“There’s nothing at this address.” is not her words).

### 9. Screenshots vs showing in the site
Her Travels CLAUDE.md (21 Nov) records a firm ask: show options in the running site, never as screenshots in chat (“they come out blurry”). Home’s CLAUDE.md still says to screenshot options and send them labelled. Worth confirming which applies to home, so the next round of choices (items 3 and 8) is shown the way she wants.

---

## Checked and fine
- **Layout:** no sideways scroll (0px) in all 12 combinations (3 sizes × device light/dark × site light/dark), nor with `#more1`–`#more3`. Open links level in every row. Growth: 5 = 3 + 2 centred, 6 = 3 + 3, 7 = 3 + 3 + 1 centred; phone one column.
- **The four places:** My Sim World, My Library, My Pokédex, My Travels, each with only the photo and “Open My …” as links. All pictures load (WebP: Willow Creek 800×562, Johto/Kanto 1200×526, Travels 1000×436; enough for the phone at 2×). No 4xx responses, no console errors or warnings.
- **Dark mode (family rule 1):** opens light with the device set to dark. With `jj-mode=dark` set before loading, it opens dark at every size (the cross-site carry works). The button reads “Dark mode” / moon, “Light mode” / sun, with `aria-pressed` false/true. Switching saves `jj-mode`, swaps theme-color and the tab icons, and keeps focus on the button. The old `jj-mode2` is moved to `jj-mode` once, then removed. With storage blocked it opens light, the button still switches, and there are no errors.
- **Footer (family rule 2):** diamond divider; “Jemma’s Journals” in Instrument Serif, upright; line 1 word for word; credits each with a capital and true to what the page uses; on phones one per line with no dots; Back to top and Dark mode 44px and level; links in the accent colour.
- **Contrast:** light: grey text 5.01, gold links 4.55, headings 14.5; dark: grey 6.0, links 8.3. “Journals” on the label: 4.18 in light (large text, 3:1 needed), 9.0 in dark.
- **Keyboard:** Skip → photo → Open for each place → Back to top → Dark mode; gold focus ring on all of them. Skip link jumps to Contents and the next Tab lands on the first photo.
- **Alt text:** maps “Map of Willow Creek”, “Map of Johto and Kanto”, “Map of the places on my trips”; the cover wall is role img, “Covers of books from my shelves”; photo links named “Open My …”.
- **Reduced motion:** no animations, smooth scrolling off.
- **Text rules:** British English (“neighbourhoods”), curly apostrophes throughout shown text, Sim World and Library lines unchanged from round 1 (their apps’ own words), placeholders marked.
- **404 layout:** tidy, no sideways scroll, noindex set (only the dark mode and footer gaps in item 1).
