// Checks the home page (concepts/index.html) in a real browser, at her laptop window, a smaller laptop and a phone.
// Run:  C:/Users/Jemma/Documents/SimTracker/.tools/node/node.exe tests/check_page.js
// Uses the Playwright that her Sim World project already has (Microsoft Edge, no download). Changes nothing on disk.
const path = require('path');
const fs = require('fs');
const { chromium } = require('C:/Users/Jemma/Documents/SimTracker/node_modules/playwright');

const ROOT = path.join(__dirname, '..', 'concepts');
const HOST = 'http://jj.test/';
const TYPES = { '.html': 'text/html; charset=utf-8', '.jpg': 'image/jpeg', '.png': 'image/png', '.webp': 'image/webp', '.woff2': 'font/woff2', '.svg': 'image/svg+xml' };
// The published page is wrapped in a document skeleton; this does the same for the local file.
const wrap = () => '<!doctype html><html lang="en-GB"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">'
  + '<style>body{margin:0}img{max-width:100%}[hidden]{display:none!important}</style></head><body>' + fs.readFileSync(path.join(ROOT, 'index.html'), 'utf8') + '</body></html>';

const SIZES = [
  { name: 'laptop 1600', viewport: { width: 1600, height: 930 } },
  { name: 'laptop 1280', viewport: { width: 1280, height: 800 } },
  { name: 'phone 390', viewport: { width: 390, height: 844 }, isMobile: true, hasTouch: true, deviceScaleFactor: 2 },
];
let failures = 0, passes = 0;
function check(ok, what) { if (ok) passes++; else { failures++; console.log('  FAIL ' + what); } }

(async () => {
  const browser = await chromium.launch({ channel: 'msedge' });
  for (const size of SIZES) {
    for (const version of ['page']) {
      // the device asks for dark: the page must still open light (her choice, 20 Nov)
      const ctx = await browser.newContext({ ...size, colorScheme: 'dark' });
      const page = await ctx.newPage();
      const errors = [];
      page.on('pageerror', e => errors.push(e.message));
      page.on('console', m => { if (m.type() === 'error') errors.push(m.text()); });
      await page.route(HOST + '**', route => {
        const url = new URL(route.request().url());
        if (url.pathname === '/' || url.pathname === '/index.html') return route.fulfill({ body: wrap(), contentType: TYPES['.html'] });
        const file = path.join(ROOT, decodeURIComponent(url.pathname));
        if (!file.startsWith(ROOT) || !fs.existsSync(file)) return route.fulfill({ status: 404, body: 'missing' });
        route.fulfill({ body: fs.readFileSync(file), contentType: TYPES[path.extname(file)] || 'application/octet-stream' });
      });
      await page.goto(HOST, { waitUntil: 'networkidle' });
      await page.evaluate(async () => { await document.fonts.ready; for (let y = 0; y < document.body.scrollHeight; y += 400) { window.scrollTo(0, y); await new Promise(r => setTimeout(r, 40)); } window.scrollTo(0, 0); });
      await page.waitForLoadState('networkidle');
      await page.evaluate(() => Promise.all(document.getAnimations().map(a => a.finished)));   // let the gentle entrance finish
      const tag = size.name + ', ' + version + ': ';
      const r = await page.evaluate(() => {
        const cards = [...document.querySelectorAll('.card')];
        return {
          mode: document.documentElement.getAttribute('data-mode'),
          sideways: document.documentElement.scrollWidth - document.documentElement.clientWidth,
          title: document.querySelector('h1') && document.querySelector('h1').textContent,
          skip: !!document.querySelector('a.skip[href="#contents"]') && !!document.getElementById('contents'),
          cards: cards.length,
          linksPerCard: cards.map(c => c.querySelectorAll('a').length),
          linkKinds: cards.map(c => [...c.querySelectorAll('a')].map(a => a.className).join(',')),
          brokenImages: [...document.images].filter(i => !i.complete || i.naturalWidth === 0).map(i => i.getAttribute('src')),
          picturesWithoutWords: cards.filter(c => { const s = c.querySelector('.snap'); return !s.getAttribute('aria-label'); }).length,
          headings: cards.map(c => c.querySelector('h3').textContent),
          openLinksLevel: (() => { const ys = cards.map(c => Math.round(c.querySelector('.go').getBoundingClientRect().top)); return new Set(ys).size === 1 || window.innerWidth < 900; })(),
          modeButton: !!document.querySelector('[data-mode-btn][aria-label]'),
          about: (document.querySelector('.foot .about-site') || {}).textContent || '',
          openWords: cards.map(c => c.querySelector('.go').textContent.trim()).join('|'),
          creditsShown: !!document.querySelector('.foot .credits') && getComputedStyle(document.querySelector('.foot .credits')).display !== 'none',
          corners: document.querySelectorAll('.cover .cn').length,
          entrance: document.getElementById('page').classList.contains('i-enter'),
          stitched: getComputedStyle(document.querySelector('.cover'), '::after').borderTopStyle,
          noindex: ((document.querySelector('meta[name="robots"]') || {}).content || ''),
          icons: [...document.querySelectorAll('link[rel="icon"],link[rel="apple-touch-icon"]')].map(l => l.getAttribute('href')),
        };
      });
      check(r.mode === 'light', tag + 'opens in light mode (got ' + r.mode + ')');
      check(r.sideways <= 0, tag + 'no sideways scrolling (' + r.sideways + 'px)');
      check(r.title === 'Jemma’s Journals', tag + 'title is Jemma’s Journals (got ' + r.title + ')');
      check(r.skip, tag + '"Skip to contents" link goes somewhere');
      check(r.cards === 3, tag + 'three places (got ' + r.cards + ')');
      check(r.linksPerCard.every(n => n === 2), tag + 'only the photo and "Open" are links in each card (' + r.linksPerCard + ')');
      check(r.linkKinds.every(k => k === 'snap,go'), tag + 'the links are the photo and "Open" (' + r.linkKinds.join(' | ') + ')');
      check(r.brokenImages.length === 0, tag + 'every picture loads (' + r.brokenImages.slice(0, 3).join(', ') + ')');
      check(r.picturesWithoutWords === 0, tag + 'every photo link says where it goes');
      check(r.headings.join('|') === 'My Sim World|My Library|My Pokédex', tag + 'names are My Sim World, My Library, My Pokédex (' + r.headings.join(', ') + ')');
      check(r.openLinksLevel, tag + '"Open" links line up across the row');
      check(r.modeButton, tag + 'light/dark button has a label');
      check(/Instrument Serif/.test(r.about) && /No cookies/.test(r.about), tag + 'About this site is in the footer');
      check(/Region maps/.test(r.about) && /Book covers/.test(r.about) && /Icons by Lucide/.test(r.about), tag + 'each credit starts with a capital (her ask, 20 Nov)');
      check(r.openWords === 'Open My Sim World|Open My Library|Open My Pokédex', tag + 'links say Open My … (' + r.openWords + ')');
      check(!r.creditsShown, tag + 'the credits aren’t repeated above About this site');
      check(r.corners === 4, tag + 'the cover has its four gold corners (Improved)');
      check(r.entrance, tag + 'the gentle entrance is on when the page opens (her pick, 20 Nov)');
      check(r.stitched === 'dashed', tag + 'the cover has its stitching (her pick, 20 Nov)');
      check(/noindex/.test(r.noindex) && /noai/.test(r.noindex) && fs.existsSync(path.join(ROOT, 'robots.txt')), tag + 'asks search engines and AI to stay away (' + r.noindex + ')');
      check(r.icons.length === 3 && r.icons.every(h => fs.existsSync(path.join(ROOT, h))), tag + 'tab icon files are there (' + r.icons.join(', ') + ')');
      // the dark button works and is remembered
      await page.click('[data-mode-btn]');
      check(await page.evaluate(() => document.documentElement.getAttribute('data-mode')) === 'dark', tag + 'dark button switches to dark');
      const darkIcons = await page.evaluate(() => [...document.querySelectorAll('link[rel="icon"]')].map(l => l.getAttribute('href')));
      check(darkIcons.every(h => /icon-dark-/.test(h)), tag + 'the tab icon flips to the dark version (' + darkIcons.join(', ') + ')');
      check(darkIcons.every(h => fs.existsSync(path.join(ROOT, h))), tag + 'the dark tab icon files are there');
      await page.reload({ waitUntil: 'networkidle' });
      check(await page.evaluate(() => document.documentElement.getAttribute('data-mode')) === 'dark', tag + 'dark is remembered after reloading');
      await page.click('[data-mode-btn]');
      // "More places" shows how it grows, still without sideways scrolling
      await page.click('#more');
      const grown = await page.evaluate(() => ({ cards: document.querySelectorAll('.card').length, sideways: document.documentElement.scrollWidth - document.documentElement.clientWidth }));
      check(grown.cards === 4 && grown.sideways <= 0, tag + '"More places" adds a fourth without sideways scrolling');
      if (size.viewport.width >= 1280) {
        const four = await page.evaluate(() => { const r = [...document.querySelectorAll('.card')].map(c => c.getBoundingClientRect()); const first = r.filter(x => Math.round(x.top) === Math.round(r[0].top)).length; return { first, rows: new Set(r.map(x => Math.round(x.top))).size, sameSize: Math.abs(r[0].width - document.querySelector('.card').getBoundingClientRect().width) < 1 && r[0].width > 300 }; });
        check(four.first === 2 && four.rows === 2 && four.sameSize, tag + 'four places sit as 2 × 2 at full size (first row ' + four.first + ')');
        await page.click('#more');
        const five = await page.evaluate(() => { const ys = [...document.querySelectorAll('.card')].map(c => Math.round(c.getBoundingClientRect().top)); const first = ys.filter(y => y === ys[0]).length; const r = [...document.querySelectorAll('.card')].slice(3).map(c => c.getBoundingClientRect()); const mid = (r[0].left + r[r.length-1].right) / 2; return { first, centred: Math.abs(mid - innerWidth / 2) < 40 }; });
        check(five.first === 3 && five.centred, tag + 'five places sit as 3 + 2, centred');
      }
      check(errors.length === 0, tag + 'no errors in the browser (' + errors.slice(0, 2).join(' / ') + ')');
      await ctx.close();
    }
  }
  await browser.close();
  console.log(passes + ' checks passed, ' + failures + ' failed');
  process.exit(failures ? 1 : 0);
})();
