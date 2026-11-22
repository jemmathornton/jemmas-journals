# What would make the family of sites better (research, 22 Nov 2026)

Read-only research: nothing was changed in any repo. Measurements were taken on her PC through the family address (http://localhost:8050, GET requests only) and on copies in a temporary folder. Everything below is **my suggestion (not decided)** unless it says “her decision”. Things already done or already turned down (see CLAUDE.md, family-rules, the round 3 reviews) are left out.

## Top 5 worth doing

1. **Small pictures for the Library and Pokédex home pages.** On a phone they download **10.5 MB** and **13 MB**, because full-size covers and maps are shrunk on screen; thumbnails would bring each to about 1–2 MB and look the same. Effort **M**. No decision needed (she should look once).
2. **One publish workflow in Jemma’s Journals** that puts home and each app’s `site/` together and publishes them to GitHub Pages. Try it on `jemmathornton.github.io` first, then add her domain. Effort **M**. **Needs her decision:** rename this repo to `jemmathornton.github.io`, or wait for the domain, and when to go online.
3. **Finish “view only online” for the Pokédex.** Online it would show the error “couldn’t read your ticks”. Also, its weekly backup doesn’t record its new version in the parent. Effort **S**. No decision needed.
4. **One “check everything” command:** each app’s tests, plus automatic accessibility checks (axe-core), the family-rules checks from the round 3 review, a check of capitals in file names, and a broken-link check. Effort **M**. **Needs her OK** to download axe-core (3.3 MB, npm, free licence).
5. **Protect the GitHub copies, which are her only backup:** a rule on each of the five repos that stops `main` being deleted or overwritten, and her ticks and marks saved every day instead of weekly. Effort **S**. **Needs her decision**, and she changes the GitHub settings herself.

---

## 1. Going online with this layout

**Findings**
- **GitHub’s own submodule build would publish too much.** GitHub Pages can build from a repo with public submodules ([GitHub: submodules with Pages](https://docs.github.com/en/pages/getting-started-with-github-pages/using-submodules-with-github-pages)). But that build publishes whole folders: `research/`, `for-jemma/`, `tests/`, each app’s `data/` and notes. It also runs Jekyll, which drops files whose names start with `_`. A **custom workflow** that copies only the `site/` folders is the right fit.
- **What the workflow needs** ([GitHub: custom workflows for Pages](https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages)):
  - `actions/checkout` with `submodules: true` (the [checkout README](https://github.com/actions/checkout) is at v7; GitHub’s Pages example uses v6). Her submodules are public, so no extra key is needed.
  - `actions/configure-pages@v5`, `actions/upload-pages-artifact@v4` and `actions/deploy-pages@v4`.
  - Permissions `pages: write` and `id-token: write`.
- **Size is fine.** Published sites can be up to 1 GB, deploys must finish within 10 minutes, and the soft limit is 100 GB of visits a month ([GitHub: limits](https://docs.github.com/en/pages/getting-started-with-github-pages/github-pages-limits)). Her five `site/` folders total about **390 MB** (Sim World 141, Library 135, Pokédex 97, home 14, Travels 2), or about 330 MB after the Top 5 #1 picture work.
- **Everything the sites need is in git.** Checked: the only `site/` files not in git are 24 working copies in `library/site/covers/_straightened`. So publishing from GitHub loses nothing.
- **Root addresses.** `/family/…`, home’s `/library/` links and the apps’ “← Jemma’s Journals” (`/`) only work at the **root** of an address: her own domain, or a repo named `jemmathornton.github.io`. A plain project address (`jemmathornton.github.io/jemmas-journals/`) breaks them (round 3, item 6). So to try it before buying the domain, the parent repo needs that name. GitHub forwards the old name, as it did for `sim-world` and `travels`.
- **Keep Pages switched off in the four app repos.** Otherwise `jemmathornton.github.io/library/` could come from two places. It is off on all five today (checked with `gh api`).
- **Caching:** GitHub Pages tells browsers to keep every file for 10 minutes (`max-age=600`), and it can’t be changed ([GitHub Support’s reply, quoted on Stack Exchange](https://dev.library.kiwix.org/content/stackoverflow_en_nopic_2021-08/questions/14798589/github-pages-http-headers); not in GitHub’s own docs). The apps already stamp `?v=…` on their own files. The `/family/` files have no stamp, so for up to 10 minutes after a change a page could get new app code with the old shared code. The workflow can add a `?v=<fingerprint>` to every `/family/…` link as it copies, so no repo file changes.
- **Pages can’t send custom headers.** Online, the noindex choice lives only in the page tags (already on every page) and `robots.txt` (home’s goes at the root, which is right). Pictures can’t carry a noindex of their own ([Google](https://developers.google.com/search/docs/crawling-indexing/block-indexing) uses an `X-Robots-Tag` header for those). If she wants pictures kept out of image search too, `robots.txt` can ask Google’s image crawler not to fetch them.
- **The local save servers online:** online there is no server, so each site has to show its data and hide its saving controls.

| Site | Online today, as built | Still to do |
|---|---|---|
| Library | Read-only unless its server answers (`checkLive`, her decision 21 Nov): no Add a book, pickers or notes | Round 3: hide the New covers switch in read-only mode; one console 404 per load. Leave out of the upload: `js/ocr` (11 MB, used only when adding a book) and `covers-trial/` (3 MB) |
| Pokédex | Ticks are built into `data.js`, so the published copy shows her ticks as of the last push | **Online it would show the “couldn’t read your ticks” error**: `app.js:1510` asks `api/collection` on any http address and sets `loadFailed` when it fails. Fix: ask only on `localhost`/`127.0.0.1` (Travels already does this with `LOCAL`) |
| Travels | `LOCAL` check: the Write page shows only on her PC; comments switched off | Its notes say photos lose GPS when saved (built and tested) |
| Sim World | Static, nothing to save | Admin is public (her call, 21 Nov) |
| Home | Static | – |

- **When it updates.** The workflow runs when the parent is pushed. The parent changes when `tools/record_apps.py` records an app’s new version, which Library and Sim World already run after their weekly jobs. **The Pokédex backup doesn’t run it** (checked: there is no call in `pokedex/tools/backup.py`, although CLAUDE.md says the apps do), and Travels has no backup job. A scheduled nightly run is the other option, but GitHub switches schedules off after 60 days with no activity in the repo ([GitHub](https://docs.github.com/en/actions/how-tos/manage-workflow-runs/disable-and-enable-workflows)). So I’d use “on push” plus a manual “Run workflow” button.
- `research/drafts/publish-site-folder.yml` is out of date (one app, old name `sim-tracker`). The draft below replaces it.

**Step by step for her**

1. **Decide the address while testing:** (a) rename `jemmas-journals` to `jemmathornton.github.io` now (my suggestion, not decided), or (b) wait and buy the domain first.
2. Claude adds `.github/workflows/publish.yml` to Jemma’s Journals (draft below) and makes the Pokédex fix. It runs every check first.
3. She opens the repo on GitHub, Settings > Pages, and sets Source to **GitHub Actions**. This is an account setting, so it is hers to click.
4. Push. Under the Actions tab, a green tick appears in about 2–4 minutes. She opens `https://jemmathornton.github.io/` on her phone and laptop and clicks through all five.
5. Later, the domain. The steps are already in `going-online.md` (A records, verifying, Enforce HTTPS). With a workflow, the domain is typed in Settings > Pages and no `CNAME` file is needed ([GitHub: managing a custom domain](https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site/managing-a-custom-domain-for-your-github-pages-site)). **Verify the domain** in her account settings, so nobody else can claim it.

```yaml
# .github/workflows/publish.yml (draft, not added)
name: Publish the family
on: { push: { branches: [main] }, workflow_dispatch: {} }
permissions: { contents: read, pages: write, id-token: write }
concurrency: { group: pages, cancel-in-progress: false }
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v6
        with: { submodules: true }
      - name: Put the five sites together
        run: |
          mkdir out && cp -r site/. out/
          for app in library sim-world pokedex travels; do cp -r "$app/site" "out/$app"; done
          rm -rf out/tools out/library/js/ocr out/library/covers-trial out/library/covers/_straightened
          v=$(cat site/family/* | sha1sum | cut -c1-8)
          grep -rl 'family/' out --include=*.html | xargs sed -i -E "s#(family/(mode|family)\.(js|css))\"#\1?v=$v\"#g"
      - uses: actions/configure-pages@v5
      - uses: actions/upload-pages-artifact@v4
        with: { path: out }
  deploy:
    needs: build
    runs-on: ubuntu-latest
    environment: { name: github-pages, url: "${{ steps.deployment.outputs.page_url }}" }
    steps:
      - id: deployment
        uses: actions/deploy-pages@v4
```

**Effort:** M (an evening, including her click-through). **Her decisions:** the address while testing, and when to go online.

## 2. Phone use: installing as an app, and working offline

**Findings**
- **Installing doesn’t need a service worker any more.** Chrome needs a manifest (name, a 192 px and a 512 px icon, `start_url`, `display`) and HTTPS ([MDN](https://developer.mozilla.org/en-US/docs/Web/Progressive_web_apps/Guides/Making_PWAs_installable)). On iPhone, since iOS 26 every Home Screen site opens as a web app (already noted in `site-ideas.md`). The Library already has `manifest.json` and a pass-through `sw.js`. Home has a draft manifest in `research/drafts/`.
- **Offline needs a service worker that keeps copies.** The risk is old copies: a new version waits until every tab is closed, and a reload doesn’t switch over ([web.dev](https://web.dev/learn/pwa/service-workers)). That would clash with how often her sites change.

**Worth it for each site?**

| Site | Install | Offline | Why |
|---|---|---|---|
| Home | **Yes**: one “Jemma’s Journals” icon on her phone | No | One icon to reach everything |
| Library | Already installable | **Worth it** | In a bookshop with poor signal: “do I already own this?” and the To Buy list. Keep the book list and every page in reserve (about 1 MB), and only covers she has already seen (all of them is 120 MB) |
| Pokédex | Optional | **Worth it** | At outdoor events and raids, checking what she still needs. Keep the list and the small pictures as she sees them |
| Sim World | No | No | Used on the PC |
| Travels | No | No | Read at leisure; writing is on the PC (her pick) |

**My suggestion (not decided):** after going online, the home manifest first (S). Offline for the Library, then the Pokédex, as “use the network first, fall back to the saved copy” (M each), so she never sees stale pages when she has signal. **Her decision:** whether offline is wanted at all.

## 3. Speed and size

**Measured (390 px phone, first visit, through 8050)**

| Page | Downloaded | Of which pictures | Main cause |
|---|---|---|---|
| Home | 0.5 MB | 0.4 MB | – (already WebP at the size shown) |
| Library home | **10.5 MB** (14.2 MB at 1600) | 9.1 MB | Covers about 390 px wide (some 1,664 px, up to 773 KB each) shown about **50 px** wide |
| Pokédex home | **13.2 MB** | 12.0 MB | Region cards load the full maps (1,600–2,800 px, up to **2.1 MB** each: `galar-map-1.jpg`, `sinnoh-map-3.jpg`, `kanto-map-2.jpg`) |
| Sim World home | 1.5 MB | 0.1 MB | Fine (it already lazy-loads its pictures) |
| Travels home | 1.4 MB | 0 | `world.js` country shapes, 1.2 MB (380 KB gzipped) |

**Folders on disk**
- **Library:** 120 MB covers (816 files, mostly 400×600, average 143 KB)
- **Sim World:** 85 MB shots (616, mostly 1160×675), 23 MB maps, 30 MB Gallery
- **Pokédex:** 51 MB region maps (170, average 304 KB), 41 MB sprites (already WebP)

**Trial re-encode** (samples of 30–60, in a temporary folder, same pixel size or capped)

| Pictures | Now (average) | As WebP q80 | AVIF |
|---|---|---|---|
| Library covers | 168 KB | 55 KB (−67%) | 41 KB |
| Sim World shots | 151 KB | 69 KB (−54%) | 59 KB |
| Pokédex region maps (capped at 1600 px) | 356 KB | 104 KB (−71%) | 86 KB |
| Sim World maps | 265 KB | 96 KB (−64%) | 75 KB |
| Gallery pictures | 43 KB | 31 KB (−27%) | small gain |

- **What would make the biggest difference: thumbnails.** For lists and cards, make a second small copy, about 2× the size shown: covers 120 px wide (about 8 KB) and region cards about 800 px (about 60–100 KB). Keep the full picture for the book or region page. This takes the Library home from about 10 MB to about 1.5 MB, and the Pokédex home from about 13 MB to about 1.5 MB. **Effort M** (each app’s build already makes `data.js`; one more output folder).
- **Then WebP for the big folders:** about 250 MB down to about 100 MB in total. Home already does this, and MDN recommends WebP or AVIF for photos ([MDN: image types](https://developer.mozilla.org/en-US/docs/Web/Media/Guides/Formats/Image_types)). AVIF is smaller still but slower to make; WebP is enough.
  - **Catch:** git keeps every old picture forever, so converting makes each repo **bigger** on GitHub (the Library repo is 356 MB today), even though the published site shrinks. GitHub suggests repos stay under 1 GB ([limits](https://docs.github.com/en/pages/getting-started-with-github-pages/github-pages-limits)). So either convert once, or have the publish workflow make the WebP copies while publishing and leave the repos unchanged (my suggestion, not decided).
  - Covers: her rule is “ask before every cover change”. A format change looks the same, but she should see a page of before and after once.
- **Lazy loading:** use `loading="lazy"` on pictures below the first screen, never on the first one ([web.dev](https://web.dev/articles/browser-level-image-lazy-loading)). Pokédex uses it widely and Sim World has its own lazy loader. Check that the Library’s cover grids (drawn as CSS backgrounds, which `loading` doesn’t cover) only load what is on screen.
- **Fonts: nothing to do.** They are local WOFF2, cut down, with `font-display: swap` everywhere (checked).
- **Data files:** the three `data.js` files are 830–870 KB, but 160–280 KB gzipped. Pages normally sends text compressed; check once online in the browser’s network tab. Travels could use simpler country shapes if `world.js` matters (S, low priority).

**Effort:** thumbnails M; WebP at publish S–M. **No decision needed**, apart from one look at the covers.

## 4. Accessibility and robustness

**What the reviews keep finding (rounds 1–3)**
- **Faint text from `opacity`:** Sim World’s sidebar “Not owned” at 2.18:1, still there after round 1; Library’s faded “missing” rows and spine titles; the Pokédex’s tag colours in round 2. WCAG asks for 4.5:1.
- **Focus lost after moving to a new page:** Sim World’s `route()` drops focus to the page’s body (round 3).
- **No `aria-current`:** the current page is shown by colour only (Sim World).
- **Leftovers after moves:** old folder paths, shortcuts pointing at old copies (Pokédex Broken 1, Sim World 2).

Each review found these by hand. They come back because no test checks for them.

**Tools**
- **axe-core with Playwright:** `@axe-core/playwright` works with the plain Playwright library she already has (no test runner): `new AxeBuilder({ page }).withTags(['wcag2a','wcag2aa']).analyze()` ([Deque README](https://github.com/dequelabs/axe-core-npm/blob/develop/packages/playwright/README.md)). It catches contrast (opacity included), missing names, wrong ARIA and duplicate ids. Package `axe-core` 4.14.1 (MPL-2.0, 3.3 MB) plus the small `@axe-core/playwright` 4.14.0. **A download, so it needs her OK.** Run it on each site’s main pages, in light **and** dark, at 1600 and 390.
- **What axe can’t see:** focus moves, the drawer, the footer and the dark-mode carry-over. The round 3 family script (`r3.js`, in a temporary folder that will be cleared) already checks all of these on all five sites. **Keep it as `tests/family_checks.js`.**
- **Capitals in file names:** Windows ignores capitals, GitHub Pages doesn’t. The Pokédex has 2,298 such names, checked by hand on 20 Nov. A check that every picture named in each `data.js` exists with exactly that spelling.
- **Broken links and pictures:** follow every page through 8050 and report any 404.

**Effort:** M. **Needs her OK** for the axe-core download.

## 5. Safety and backups

**Checked**
- **Photo location:** 12,934 pictures in the five folders (git-ignored folders included), **0 with GPS data**. Travels’ save server strips it from new photos (tested in its suite).
- **Secrets:** no tokens, keys or email addresses in any tracked file. The Library scan key is kept outside git. GitHub’s **secret scanning and push protection are already on** for all five repos (`gh api`).
- **Personal data on view:** her to-do list in Sim World Admin (public, her call, 21 Nov) and “Birmingham” as the Travels distance origin (city centre, 52.48, −1.9: fine). Once her real trips go in, post dates show when she was away. Worth knowing, not a problem.

**Backups today**
- **Library** and **Pokédex:** weekly on Sundays, commit and push.
- **Sim World:** every commit is pushed straight away (post-commit hook), plus the weekly Gallery refresh. Round 3 noted that its task’s 15 Nov run failed.
- **Travels:** no automatic backup (her no).
- Not one of the five repos has `main` protected (`gh api`).

**If her PC died today**
- **Pokédex:** ticks since last Sunday would be lost.
- **Library:** marks and added books since Sunday, `data/scanned.json`, and the scan key would be lost.
- **Travels:** posts not yet pushed by hand would be lost.
- **Sim World:** nothing. Its weekly refresh rebuilds from her game files.
- **Rebuilding:** clone with `git clone --recurse-submodules`, reinstall Node and Playwright, and re-run each app’s `make_backup_task.ps1`. Her shortcuts and Startup item would need making again, and there is no script for that yet.
- **Not covered by any of this:** her game saves and Pictures. Those are outside these projects, and her own choice.

**My suggestions (not decided)**
1. **A ruleset on each repo:** “Restrict deletions” and “Block force pushes” on `main`. It is free for public repos ([GitHub: managing rulesets](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets); [available rules](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/available-rules-for-rulesets)). The backups never force-push, so nothing breaks, and a mistake can’t wipe the only copy. **She sets it (account setting); S.**
2. **Daily instead of weekly backups** for the Library and Pokédex. Same scripts, a different trigger. They only commit when something changed. **S.**
3. **Travels:** ask her again whether a push after each saved post would be welcome. She said no on 21 Nov, so this is her call.
4. **A one-page “new PC” note** with a script that recreates the tasks, shortcuts and Startup item. **S–M.**
5. Dependabot: not relevant. There are no package files in the published sites, and Playwright is a local test tool. Leave it off.

## 6. Maintenance

**Recording app versions**
- `record_apps.py` exists. Library and Sim World run it; the **Pokédex backup and Travels don’t**, and nothing runs it after a hand-made commit.
- **My suggestion (not decided):**
  - call it from the Pokédex backup (S)
  - have the family server or the morning Startup item run it once a day (S), so nothing waits for Sunday
  - **or** a post-commit hook in each app. In a submodule the hook lives in `JemmasJournals/.git/modules/<app>/hooks/`, not in the app, which is why Sim World’s hook test now skips (round 3).

**Keeping the five sites the same**
- The shared code is in `site/family/`, used so far by home, Library and Travels; the Pokédex and Sim World haven’t moved yet.
- A change there affects all five, but nothing records which family version each app was tested with (round 3).
- The family checks (section 4) run on all five through 8050, so they cover that.

**One “check everything” command**
- `python tools/check_all.py`, with two speeds:
  - **quick (about 2 minutes):** home’s `check_page.js`, the family checks, axe, capitals in file names, broken links, `git status` clean in all five, and the submodule versions recorded
  - **full:** adds each app’s own suite (Travels about 11 minutes; Sim World 345 Python + 75 site tests)
- It prints one line per site, ✓ or ✗.
- Run the quick one before every push and the full one before publishing.
- **Effort M.**

## 7. Other ideas, checked against her rules

- **Search across all five sites:** a page of its own (not on home), built when publishing from each app’s data: book titles and authors, Sims and households, Pokémon, trips. Each result is a link into its site, with no counts. Travels already has a Search page on trial. **L; her decision.** This is the only cross-site feature that adds real value without breaking “home is a landing page”.
- **“What’s new” across the sites:** not on home (her rule: no latest, no dates). If ever wanted, a separate “Site notes” page linked from the footer, written in her words (already listed in `site-ideas.md`). Nothing to do now.
- **Content-Security-Policy as a `<meta>` tag** (Pages can’t send headers): Travels is already written for it. Low priority; only after the shared code has replaced the inline head scripts.
- **Not worth it:** visitor counting (she doesn’t need it), a guestbook or comments (they invite strangers to a site she isn’t advertising; comments on Travels are already “decide when going online”), and a second host (GitHub Pages fits everything).

## Sources

- GitHub: [custom workflows for Pages](https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages) · [submodules with Pages](https://docs.github.com/en/pages/getting-started-with-github-pages/using-submodules-with-github-pages) · [Pages limits](https://docs.github.com/en/pages/getting-started-with-github-pages/github-pages-limits) · [custom domain](https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site/managing-a-custom-domain-for-your-github-pages-site) · [actions/checkout](https://github.com/actions/checkout) · [rulesets](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets) · [available rules](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/available-rules-for-rulesets) · [scheduled workflows switched off after 60 days](https://docs.github.com/en/actions/how-tos/manage-workflow-runs/disable-and-enable-workflows)
- Pages cache header: [GitHub Support reply quoted on Stack Exchange](https://dev.library.kiwix.org/content/stackoverflow_en_nopic_2021-08/questions/14798589/github-pages-http-headers) (secondhand)
- [MDN: making PWAs installable](https://developer.mozilla.org/en-US/docs/Web/Progressive_web_apps/Guides/Making_PWAs_installable) · [web.dev: service workers](https://web.dev/learn/pwa/service-workers) · [web.dev: lazy loading](https://web.dev/articles/browser-level-image-lazy-loading) · [MDN: image types](https://developer.mozilla.org/en-US/docs/Web/Media/Guides/Formats/Image_types)
- [Deque: @axe-core/playwright](https://github.com/dequelabs/axe-core-npm/blob/develop/packages/playwright/README.md) · [Google: block indexing](https://developers.google.com/search/docs/crawling-indexing/block-indexing)
- On her PC: `du` and Pillow for sizes, dimensions and GPS; Playwright (Edge) through 8050 for page weights; `gh api` (read only) for the repo settings. The scripts are in the session’s temporary folder: `C:\Users\Jemma\AppData\Local\Temp\claude\9cff366c1b60a8f8\2df2d807-e7a9-4322-8b41-c4059cb2ba00\scratchpad\weigh.js` and `weigh2.js`.
