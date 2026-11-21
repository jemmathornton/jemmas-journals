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

Checked again 21 Nov 2026 (third-party price trackers, so confirm on the registrar's own page before buying):
- **Cloudflare Registrar** supports `.co.uk` and renews at the registry's price with no mark-up; about $5.30 (≈ £4) a year, same on renewal ([Cloudflare: .uk domains](https://www.cloudflare.com/application-services/products/registrar/buy-uk-domains/), [CostGoat](https://costgoat.com/pricing/cloudflare-domains), [DomainOffer](https://domainoffer.net/tld/uk/cloudflare)). It auto-renews by default.
- **Porkbun**: `.co.uk` first year about $4.66; renewal ranked among the cheapest but the exact figure wasn’t listed ([DomainOffer](https://domainoffer.net/tld/co.uk/porkbun), [Porkbun: renewal prices](https://porkbun.helpscoutdocs.com/article/108-how-to-check-domain-renewal-price)).

## “Anyone can see it, but not advertised”

- `<meta name="robots" content="noindex">` in each page asks search engines not to list it ([Google](https://developers.google.com/search/docs/crawling-indexing/block-indexing)). It is a request, not privacy: anyone with the link can still open it, and the GitHub repos are public anyway.
- Don’t also block those pages in robots.txt, or search engines can’t see the noindex.

## What each app would need before going online (checked in her projects, 20 Nov)

- **All three:** links and pictures already use paths that work under `/repo/` (none start with `/`). Saved settings use their own names (`jemmas-library-…`, `jemmas-pokedex-…`, `jsw-…`, `calendar-4`), so they won’t clash when the sites share one address. The home page uses `jj-…`.
- **Pokédex:** saving ticks calls `/api/collection` and `/api/tick` on her PC’s little server. Its ticks are already built into `data.js` and it starts read-only (`app.js` line 67: `readOnly = true` until the server answers), so online it would show everything she has ticked. The only problem: when `/api/collection` fails (as it would online) it sets `loadFailed` and shows “The Pokédex server couldn’t read your ticks…” (line 418). Small change: don't ask the server, and don't show that notice, unless the page is on her own PC (`localhost`). 2,298 picture names contain capitals (e.g. `pm1.cJAN_2020_NOEVOLVE.webp`); checked 20 Nov: every name listed in `data.js` (3,635 small pictures, 2,736 big, 100 backgrounds) and every region picture in `app.js` (89) matches its file exactly, capitals included.
- **Library:** the Add a book page, phone scanning, and the condition / inscription / signed pickers call her PC’s server (`api/…`). It decides it has a server whenever the page is on `http(s)` (`app.js` line 658: `served = location.protocol.startsWith("http")`), so online it would show those controls and they would fail. Small change: treat only `localhost` as served, and hide the Add a book link (line 373) and the pickers online. Its `manifest.json` and `sw.js` already use `./`, so installing it as an app works under `/library/`. Picture names checked 20 Nov: none differ only by capitals.
- **Sim World:** no server calls; should work as it is. One thing for her to decide: the Admin pages (At a glance, Progress, Notes) show her own list of things to do and decide (`for-jemma/your-list.md`). Online anyone with the link could read them (the GitHub copy is already public). She may want Admin hidden online. Picture names checked 20 Nov: none differ only by capitals.

## Her direction so far (20 Nov, not final)

- She’d like **her own domain** rather than a `github.io` address; hosting not chosen yet.
- **Separate repos, no submodules**: one website to visitors, each app still updates on its own when pushed.
- Already done in readiness: noindex + AI-crawler requests (`concepts/robots.txt`, meta tags), not-found page, share picture, tab icons, and the “← Jemma’s Journals” link in each app (it points at `/`, which is home when all four share one address).

## Own domain on GitHub Pages: the steps (from GitHub’s docs, checked 21 Nov)

1. Buy the domain (see prices above).
2. In the home site’s repo settings → Pages → Custom domain, enter it; GitHub adds a `CNAME` file. The app repos then appear under it automatically (`yourdomain.co.uk/library/`).
3. At the registrar, add four **A records** for the bare domain pointing to `185.199.108.153`, `185.199.109.153`, `185.199.110.153`, `185.199.111.153`, and a `www` CNAME to `jemmathornton.github.io` ([GitHub: managing a custom domain](https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site/managing-a-custom-domain-for-your-github-pages-site)). No wildcard records (they risk someone else claiming the domain).
4. **Verify** the domain in GitHub’s account settings with the TXT record it gives, and leave that record in place ([GitHub: verifying](https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site/verifying-your-custom-domain-for-github-pages)).
5. Tick **Enforce HTTPS** once it becomes available (can take up to 24 hours; if it stays greyed out, look for extra A/AAAA records, or remove and re-add the domain) ([GitHub: HTTPS](https://docs.github.com/en/pages/getting-started-with-github-pages/securing-your-github-pages-site-with-https), [troubleshooting](https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site/troubleshooting-custom-domains-and-github-pages)).
6. Check from her PC with PowerShell: `Resolve-DnsName yourdomain.co.uk` should list the four addresses.

## Suggested route (Claude’s suggestion, not decided)

1. Rename this repo to `jemmathornton.github.io` (or make a new one with that name) so the home page is the main address.
2. In each app’s repo, add a small workflow that publishes `site/`, plus the view-only changes above (Pokédex, Library).
3. Point the home page’s “Open …” links at `/sim-tracker/`, `/library/`, `/pokedex/`.
4. ~~Add the noindex tag~~ done (her choice, 20 Nov), plus the AI-crawler requests.
5. Test on `jemmathornton.github.io` first; then add her own address (steps above), which covers all four.
