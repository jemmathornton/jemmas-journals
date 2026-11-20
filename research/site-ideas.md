# Ideas to make Jemma’s Journals a better website (research, 20 Nov 2026)

All of this is suggestion, for Jemma to choose from. Her rules come first: home is a landing space (no counts, no latest, no dates), text is her own words, no AI art, it must read like a website. Ideas marked **on the page** can be tried on the trial switch now.

## Already tried on the page (Extras on the switch)

- **Quick links** under each place, straight into its main sections, using each app’s own section names (Sim World: Calendar, Families, Businesses, Clubs, Dynasties; Library: All Shelves, Reading, History, To Buy, Authors; Pokédex: Every Pokémon, Event Pokémon, Looking for, What’s on). Plain links, no counts. The “mini sitemap” idea from the research. **On the page.**
- **About this site** (a “colophon”): fonts, icons, where the pictures come from, what it’s made with, and that there’s no tracking. A standard part of personal sites ([indieweb.org/colophon](https://indieweb.org/colophon)); it also takes over the credits line. **On the page.**
- **Empty slot** for the next place. **On the page.**
- **Edition mark** (“Edition I”) in the footer: some personal sites number each redesign, like a journal’s volumes (Lynn Fisher keeps every version, v. I to v. XIX, [lynnandtonic.com/archive](https://lynnandtonic.com/archive/)). Not a date or a “latest”. **On the page.**

## Joining the four sites into one place

Nielsen Norman Group’s advice for a family of sites: a clear link back to the main site on every one, kept small, with each site’s own menu staying in charge ([nngroup.com: universal navigation](https://www.nngroup.com/articles/universal-navigation/)). Two ways it could look in her apps (mock pictures only, apps unchanged): A, a small “← Jemma’s Journals” at the top of each sidebar; B, a slim navy strip across the top of every app, with the home link and links to the other places. Also worth considering: the same footer and the same light/dark behaviour everywhere (today her apps follow the device’s dark setting, while home opens light, her preference).

One mismatch to decide: home calls them “My Sim World / My Library / My Pokédex”; the apps call themselves “Jemma’s Sim World / Jemma’s Library / Jemma’s Pokédex”.

## Separate pages she could add later (linked from the footer, so home stays a landing page)

From the “slash pages” tradition ([slashpages.net](https://slashpages.net/)):
- **/now**: what she’s into at the moment ([nownownow.com/about](https://nownownow.com/about)). Not on home (it’s a “latest”), but fine as its own page if she wants one.
- **Site notes / changelog**: what changed on the site and when. Fits the journal theme; its own page only.
- **Links**: sites she likes (a “blogroll”, [indieweb.org/blogroll](https://indieweb.org/blogroll)).
- **AI**: a short note, in her words, on not using AI-made pictures or text ([slashpages.net](https://slashpages.net/)).
- **Guestbook** ([indieweb.org/guestbook](https://indieweb.org/guestbook)) and **contact**: charming, but they invite strangers to a site she isn’t advertising; a guestbook needs a service and moderating. Probably not.

## Small things websites often forget

- **Tab and home-screen icon** (options made: `for-jemma/concepts/choice-tab-icon.png`).
- **Share picture** for when the link is sent in a message (made from the banner: `concepts/img/share-preview.png`; it could instead be her own photo, e.g. of a real journal).
- **A “page not found” page** in the same style (`concepts/404.html`).
- **Not listed by search engines** (a `noindex` tag), if she prefers.

## Done overnight (no change to how it looks)

- **Lighter pictures:** the book covers and maps are now saved at the size they’re shown, as WebP: the whole page went from about 920 KB to about 410 KB, which matters on a phone ([MDN on image formats](https://developer.mozilla.org/en-US/docs/Web/Media/Guides/Formats/Image_types)).
- **Places higher up on a phone:** in the Improved version the About photo now sits beside her words on a phone, so the first place starts at 545 px instead of 738 px (the phone screen is 844 px).
- **Bigger tap areas** for the quick links (at least 24 px, the accessibility standard: [W3C target size](https://www.w3.org/WAI/WCAG22/Understanding/target-size-minimum.html)).
- Every text colour checked against its background (all pass); 108 automatic page checks pass.

## Before it goes online: checklist (drafts in `research/drafts/`)

- `head.html`: the page’s hidden settings: language (en-GB), light colour scheme, share-preview tags for WhatsApp/iMessage/Discord ([ogp.me](https://ogp.me/); keep the picture under ~300 KB for WhatsApp), icons, and the fonts started early ([web.dev](https://web.dev/articles/font-best-practices)).
- Icons: a 32 px favicon.ico, an SVG icon and a 180 × 180 apple-touch-icon ([Evil Martians, 2026](https://evilmartians.com/chronicles/how-to-favicon-in-2021-six-files-that-fit-most-needs)), once she picks A, B or C.
- `manifest.webmanifest`: lets “Add to Home Screen” open it like an app on Android and iPhone ([web.dev](https://web.dev/articles/add-manifest); since iOS 26 every Home Screen site opens as a web app, [WebKit](https://webkit.org/blog/17333/webkit-features-in-safari-26-0/)).
- `robots.txt`: optional lines asking AI companies’ crawlers (OpenAI, Google’s AI, Anthropic, Apple’s AI, Common Crawl) not to collect the pages. Requests, not locks.
- `noindex`: one line per page to ask search engines not to list it; each of her apps would need it too if they should stay unlisted ([Google](https://developers.google.com/search/docs/crawling-indexing/block-indexing)).
- `concepts/404.html`: the not-found page (GitHub Pages uses `404.html` at the root; [GitHub](https://docs.github.com/en/pages/getting-started-with-github-pages/creating-a-custom-404-page-for-your-github-pages-site)).
- After publishing: run [PageSpeed Insights](https://pagespeed.web.dev) on the phone tab (aim for 90+) and [WAVE](https://wave.webaim.org/extension/) for accessibility.
- Counting visitors: not needed. If she ever wants it, GoatCounter is free and cookie-free; under the UK’s 2025 changes, simple analytics to improve a site needs a short privacy note with a way to opt out rather than a consent banner ([ICO](https://ico.org.uk/for-organisations/direct-marketing-and-privacy-and-electronic-communications/guidance-on-the-use-of-storage-and-access-technologies/what-are-the-exceptions/)). Not legal advice. Her saved light/dark choice is the kind of “appearance” setting the ICO allows without asking.

## Examples worth a look (picked by the research helper; design taste, not a ranking)

- Laurel Schwulst, https://laurelschwulst.com: a column of picture cards, each with a title and one line. Her essay on personal websites is widely cited ([The Creative Independent](https://thecreativeindependent.com/essays/laurel-schwulst-my-website-is-a-shifting-house-next-to-a-river-of-knowledge-what-could-yours-be/)).
- Lynn Fisher, https://lynnandtonic.com: rebuilds her site every year and keeps every edition.
- Patrick Collison, https://patrickcollison.com: just a name and a plain list of links, very quick on a phone.
- Jim Nielsen, https://www.jim-nielsen.com: one small shared menu joins his separate sites ([his write-up](https://blog.jim-nielsen.com/2024/consistent-nav-across-inconsistent-sites/)).
- Maggie Appleton, https://maggieappleton.com: a footer that repeats the main sections and links a colophon.
- petrapixel, https://petrapixel.neocities.org: a hand-made site with a sitemap and switches for dark mode, font and reduced motion.
