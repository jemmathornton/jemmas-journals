// Checks the home page (site/index.html) in a real browser, at her laptop window, a smaller laptop and a phone.
// Run:  C:/Users/Jemma/Documents/JemmasJournals/.tools/node/node.exe tests/check_page.js
// Uses the Playwright that her Sim World project already has (Microsoft Edge, no download). Changes nothing on disk.
const path = require('path');
const fs = require('fs');
const { chromium } = require('playwright');

const ROOT = path.join(__dirname, '..', 'site');
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
          openLinksLevel: (() => { const rows = {}; cards.forEach(c => { const k = Math.round(c.getBoundingClientRect().top); (rows[k] ||= []).push(Math.round(c.querySelector('.go').getBoundingClientRect().top)); }); return Object.values(rows).every(ys => new Set(ys).size === 1) || window.innerWidth < 900; })(),
          modeButton: (() => { const b = document.querySelector('[data-jj-mode]'); return !!b && !!(b.getAttribute('aria-label') || b.textContent.trim()) && !document.querySelector('.cover [data-jj-mode]') && !!document.querySelector('.foot [data-jj-mode]'); })(),
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
      check(r.cards === 4, tag + 'four places (got ' + r.cards + ')');
      check(r.linksPerCard.every(n => n === 2), tag + 'only the photo and "Open" are links in each card (' + r.linksPerCard + ')');
      check(r.linkKinds.every(k => k === 'snap,go'), tag + 'the links are the photo and "Open" (' + r.linkKinds.join(' | ') + ')');
      check(r.brokenImages.length === 0, tag + 'every picture loads (' + r.brokenImages.slice(0, 3).join(', ') + ')');
      check(r.picturesWithoutWords === 0, tag + 'every photo link says where it goes');
      check(r.headings.join('|') === 'My Sim World|My Library|My Pokédex|My Travels', tag + 'names are My Sim World, My Library, My Pokédex, My Travels (' + r.headings.join(', ') + ')');
      check(r.openLinksLevel, tag + '"Open" links line up across each row');
      check(r.modeButton, tag + 'light/dark button is in the footer, not the banner, and says what it does');
      check(/Instrument Serif/.test(r.about) && /No cookies/.test(r.about), tag + 'About this site is in the footer');
      check(/Region maps/.test(r.about) && /Book covers/.test(r.about) && /Icons by Lucide/.test(r.about), tag + 'each credit starts with a capital (her ask, 20 Nov)');
      check(r.openWords === 'Open My Sim World|Open My Library|Open My Pokédex|Open My Travels', tag + 'links say Open My … (' + r.openWords + ')');
      check(!r.creditsShown, tag + 'the credits aren’t repeated above About this site');
      if (size.viewport.width >= 1280) {   // four places (Travels added 21 Nov): 2 × 2 at full size
        const four = await page.evaluate(() => { const r = [...document.querySelectorAll('.card')].map(c => c.getBoundingClientRect()); return { first: r.filter(x => Math.round(x.top) === Math.round(r[0].top)).length, rows: new Set(r.map(x => Math.round(x.top))).size, wide: r[0].width > 300 }; });
        check(four.first === 2 && four.rows === 2 && four.wide, tag + 'four places sit as 2 × 2 at full size (first row ' + four.first + ')');
      }
      check(r.corners === 4, tag + 'the cover has its four gold corners (Improved)');
      check(r.entrance, tag + 'the gentle entrance is on when the page opens (her pick, 20 Nov)');
      check(r.stitched === 'dashed', tag + 'the cover has its stitching (her pick, 20 Nov)');
      check(/noindex/.test(r.noindex) && /noai/.test(r.noindex) && fs.existsSync(path.join(ROOT, 'robots.txt')), tag + 'asks search engines and AI to stay away (' + r.noindex + ')');
      check(r.icons.length === 3 && r.icons.every(h => fs.existsSync(path.join(ROOT, h))), tag + 'tab icon files are there (' + r.icons.join(', ') + ')');
      // the dark button works and is remembered
      await page.click('[data-jj-mode]');
      check(await page.evaluate(() => document.documentElement.getAttribute('data-mode')) === 'dark', tag + 'dark button switches to dark');
      check(await page.evaluate(() => localStorage.getItem('jj-mode')) === 'dark', tag + 'dark is saved in the shared family setting jj-mode');
      const darkIcons = await page.evaluate(() => [...document.querySelectorAll('link[rel="icon"]')].map(l => l.getAttribute('href')));
      check(darkIcons.every(h => /icon-dark-/.test(h)), tag + 'the tab icon flips to the dark version (' + darkIcons.join(', ') + ')');
      check(darkIcons.every(h => fs.existsSync(path.join(ROOT, h))), tag + 'the dark tab icon files are there');
      await page.reload({ waitUntil: 'networkidle' });
      check(await page.evaluate(() => document.documentElement.getAttribute('data-mode')) === 'dark', tag + 'dark is remembered after reloading');
      await page.click('[data-jj-mode]');
      // how it grows when places are added (stand-ins via #more1 / #more2; the trial button is gone), still without sideways scrolling
      const grow = async n => { await page.goto(HOST + '#more' + n, { waitUntil: 'networkidle' }); await page.reload({ waitUntil: 'networkidle' }); await page.evaluate(() => Promise.all(document.getAnimations().map(a => a.finished))); };
      check(await page.evaluate(() => !document.querySelector('.sw') && !document.getElementById('more')), tag + 'the trial switch is gone');
      await grow(1);
      const grown = await page.evaluate(() => ({ cards: document.querySelectorAll('.card').length, sideways: document.documentElement.scrollWidth - document.documentElement.clientWidth }));
      check(grown.cards === 5 && grown.sideways <= 0, tag + '"More places" adds a fifth without sideways scrolling');
      if (size.viewport.width >= 1280) {
        const five = await page.evaluate(() => { const ys = [...document.querySelectorAll('.card')].map(c => Math.round(c.getBoundingClientRect().top)); const first = ys.filter(y => y === ys[0]).length; const r = [...document.querySelectorAll('.card')].slice(3).map(c => c.getBoundingClientRect()); const mid = (r[0].left + r[r.length-1].right) / 2; return { first, centred: Math.abs(mid - innerWidth / 2) < 40 }; });
        check(five.first === 3 && five.centred, tag + 'five places sit as 3 + 2, centred');
        await grow(2);
        const six = await page.evaluate(() => { const ys = [...document.querySelectorAll('.card')].map(c => Math.round(c.getBoundingClientRect().top)); return { first: ys.filter(y => y === ys[0]).length, rows: new Set(ys).size }; });
        check(six.first === 3 && six.rows === 2, tag + 'six places sit as 3 + 3');
      }
      // the most stand-ins (#more3) must still work, and Back to top must move focus to the top (review, 21 Nov)
      await grow(3);
      check(await page.evaluate(() => document.querySelectorAll('.card').length) === 7, tag + '#more3 shows seven places');
      await page.click('[data-jj-top]');
      check(await page.evaluate(() => document.activeElement && document.activeElement.id === 'top'), tag + 'Back to top moves focus to the top');
      check(errors.length === 0, tag + 'no errors in the browser (' + errors.slice(0, 2).join(' / ') + ')');
      await ctx.close();
    }
  }
  // the family rules (research/family-rules.md): dark set on another site carries here and to the 404 page, which has the family footer
  {
    const ctx = await browser.newContext({ viewport: { width: 1280, height: 800 }, colorScheme: 'dark' });
    await ctx.addInitScript(() => { try { if (!sessionStorage.getItem('seeded')) { localStorage.setItem('jj-mode', 'dark'); sessionStorage.setItem('seeded', '1'); } } catch (e) {} });
    const page = await ctx.newPage(); const errors = [];
    page.on('pageerror', e => errors.push(e.message));
    await page.route(HOST + '**', route => {
      const url = new URL(route.request().url());
      if (url.pathname === '/' || url.pathname === '/index.html') return route.fulfill({ body: wrap(), contentType: TYPES['.html'] });
      const file = path.join(ROOT, decodeURIComponent(url.pathname));
      if (!file.startsWith(ROOT) || !fs.existsSync(file)) return route.fulfill({ status: 404, body: 'missing' });
      route.fulfill({ body: fs.readFileSync(file), contentType: TYPES[path.extname(file)] || 'application/octet-stream' });
    });
    await page.goto(HOST, { waitUntil: 'networkidle' });
    check(await page.evaluate(() => document.documentElement.getAttribute('data-mode')) === 'dark', 'family: home opens dark when jj-mode is already dark');
    await page.goto(HOST + '404.html', { waitUntil: 'networkidle' });
    const nf = await page.evaluate(() => ({ mode: document.documentElement.getAttribute('data-mode'), foot: (document.querySelector('footer') || {}).innerText || '', btn: (document.getElementById('modeBtn') || {}).textContent || '' }));
    check(nf.mode === 'dark', 'family: the 404 page opens dark when jj-mode is dark');
    check(/No cookies, no tracking, no ads/.test(nf.foot) && /Back to top/.test(nf.foot) && nf.btn === 'Light mode', 'family: the 404 page has the family footer with the mode button');
    await page.click('#modeBtn');
    check(await page.evaluate(() => localStorage.getItem('jj-mode')) === 'light' && await page.evaluate(() => document.documentElement.getAttribute('data-mode')) === 'light', 'family: the 404 page’s button switches and saves jj-mode');
    check(errors.length === 0, 'family: no errors on the 404 page (' + errors.slice(0, 2).join(' / ') + ')');
    await ctx.close();
  }
  await browser.close();
  console.log(passes + ' checks passed, ' + failures + ' failed');
  process.exit(failures ? 1 : 0);
})();
