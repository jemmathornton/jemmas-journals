# Putting Jemma’s Journals and the three apps online (research, 20 Nov 2026)

Nothing here is decided: it is research for Jemma to choose from. Prices change; links are where each fact came from.

## GitHub Pages (free, her repos are already public)

- A repo called `jemmathornton.github.io` becomes the main site at `https://jemmathornton.github.io/`; every other repo with Pages turned on appears under it, e.g. `https://jemmathornton.github.io/library/`. ([GitHub: about Pages](https://docs.github.com/en/pages/getting-started-with-github-pages/about-github-pages))
- Publishing straight from a branch only works from the repo root or a `docs/` folder ([GitHub: publishing source](https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site), checked 20 Nov). Her apps keep their site in `site/`, so either rename it or add a small GitHub Actions workflow that publishes `site/` ([upload-pages-artifact](https://github.com/actions/upload-pages-artifact) takes any folder). The workflow also skips Jekyll, which would otherwise drop files whose names start with `_`.
- Limits ([GitHub: Pages limits](https://docs.github.com/en/pages/getting-started-with-github-pages/github-pages-limits)): published site up to 1 GB (her sites: Sim World ~140 MB, Library ~135 MB, Pokédex ~97 MB, home a few MB), soft 100 GB a month of visits, deploys time out after 10 minutes. Single files over 100 MB are refused by GitHub (none of hers are near that).
- HTTPS is automatic.
- A custom domain set on the main site is used for all the others by default, so `yourdomain.co.uk/library/` works ([GitHub: custom domains](https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site/about-custom-domains-and-github-pages), checked 20 Nov: “that same custom domain will be used for all project sites owned by the same account”).

## Other hosts (briefly)

- Cloudflare Pages (free): up to 20,000 files per site and 25 MB per file ([limits](https://developers.cloudflare.com/pages/platform/limits/)); the Pokédex’s ~6,700 files fit, but the drag-and-drop upload stops at 1,000 files, so it would need to be linked to GitHub. A good second choice.
- Netlify (free): a monthly credit allowance; when it runs out every site goes offline until the next month ([how credits work](https://docs.netlify.com/manage/accounts-and-billing/billing/billing-for-credit-based-plans/how-credits-work/)). Less suited to picture-heavy sites.

## Own web address (optional)

Roughly £4–8 a year for a `.co.uk`, £8–10 for a `.com` (Porkbun and Cloudflare Registrar list at-cost prices; watch for cheap first years that renew dearer). Not needed: `jemmathornton.github.io` works for free.

## “Anyone can see it, but not advertised”

- `<meta name="robots" content="noindex">` in each page asks search engines not to list it ([Google](https://developers.google.com/search/docs/crawling-indexing/block-indexing)). It is a request, not privacy: anyone with the link can still open it, and the GitHub repos are public anyway.
- Don’t also block those pages in robots.txt, or search engines can’t see the noindex.

## What each app would need before going online (checked in her projects, 20 Nov)

- **All three:** links and pictures already use paths that work under `/repo/` (none start with `/`). Saved settings use their own names (`jemmas-library-…`, `jemmas-pokedex-…`, `jsw-…`, `calendar-4`), so they won’t clash when the sites share one address. The home page uses `jj-…`.
- **Pokédex:** saving ticks calls `/api/collection` and `/api/tick` on her PC’s little server. Online there is no server, so it would show “The Pokédex server couldn’t read your ticks…”. It needs a view-only mode online (read ticks from the built `data.js`, hide the notice and the tick buttons). 2,298 picture names contain capitals (e.g. `pm1.cJAN_2020_NOEVOLVE.webp`); web hosts treat capitals as different letters, unlike Windows, so worth one check that every name in `data.js` matches its file exactly.
- **Library:** the Add a book page and phone scanning use her PC’s server (`api/…`); online they should be hidden. Its `manifest.json` and `sw.js` already use `./`, so installing it as an app works under `/library/`.
- **Sim World:** no server calls; should work as it is.

## Suggested route (Claude’s suggestion, not decided)

1. Rename this repo to `jemmathornton.github.io` (or make a new one with that name) so the home page is the main address.
2. In each app’s repo, add a small workflow that publishes `site/`, plus the view-only changes above (Pokédex, Library).
3. Point the home page’s “Open …” links at `/sim-tracker/`, `/library/`, `/pokedex/`.
4. Add the noindex tag if she’d rather search engines didn’t list it.
5. Test on `jemmathornton.github.io` first; an own address can be added later and covers all four.
