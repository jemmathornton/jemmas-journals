// Checks Jemma’s __NAME__ in a real browser (Microsoft Edge through Playwright), the family rules first.
// Run from this folder:   ../.tools/node/node.exe tests/check_site.js            (uses Jemma’s Journals’ shared Node and Playwright)
//                         ../.tools/node/node.exe tests/check_site.js --shots <folder>   also saves screenshots (1600 and 390, light and dark)
// It serves site/ itself (nothing to start first), with /family/ taken from Jemma’s Journals (../site/family), as online.
// Changes nothing on disk (apart from the screenshots you ask for).
const path = require('path');
const fs = require('fs');
const PARENT = path.resolve(__dirname, '..', '..');   // Jemma’s Journals: this site is a folder in it
const need = name => require(path.join(PARENT, 'node_modules', name));
const { chromium } = need('playwright');
const AXE = fs.readFileSync(path.join(PARENT, 'node_modules', 'axe-core', 'axe.min.js'), 'utf8');

const SITE = path.join(__dirname, '..', 'site');
const FAMILY = path.join(PARENT, 'site', 'family');
const HOST = 'http://site.test';
const NAME = 'Jemma’s __NAME__';
const CSP = "default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'; img-src 'self' data: blob:; font-src 'self'; connect-src 'self'; object-src 'none'; base-uri 'self'; form-action 'self'; frame-src 'none'";
const TYPES = { '.html': 'text/html; charset=utf-8', '.css': 'text/css', '.js': 'text/javascript', '.svg': 'image/svg+xml', '.png': 'image/png', '.jpg': 'image/jpeg', '.webp': 'image/webp', '.woff2': 'font/woff2', '.txt': 'text/plain' };
const shotsAt = process.argv.indexOf('--shots');
const SHOTS = shotsAt > 0 ? path.resolve(process.argv[shotsAt + 1]) : null;

let failures = 0, passes = 0;
function check(ok, what) { if (ok) passes++; else { failures++; console.log('  FAIL ' + what); } }

async function newPage(browser, viewport, extra = {}) {
  // the device asks for dark: every site must still open light (the family rules)
  const ctx = await browser.newContext({ viewport, colorScheme: 'dark', reducedMotion: 'reduce', ...extra });
  await ctx.route(HOST + '/**', route => {
    const url = new URL(route.request().url());
    let p = decodeURIComponent(url.pathname), base = SITE;
    if (p.startsWith('/family/')) { base = FAMILY; p = p.slice('/family'.length); }
    if (p.endsWith('/')) p += 'index.html';
    const file = path.join(base, p);
    if (!file.startsWith(base) || !fs.existsSync(file) || fs.statSync(file).isDirectory()) return route.fulfill({ status: 404, body: 'missing' });
    route.fulfill({ body: fs.readFileSync(file), contentType: TYPES[path.extname(file)] || 'application/octet-stream' });
  });
  await ctx.addInitScript(() => { window.__csp = []; document.addEventListener('securitypolicyviolation', e => window.__csp.push(e.violatedDirective + ' ' + e.blockedURI)); });
  const page = await ctx.newPage();
  page.errors = [];
  page.on('pageerror', e => page.errors.push(e.message));
  page.on('console', m => { if (m.type() === 'error') page.errors.push(m.text()); });
  return { ctx, page };
}
async function go(page, hash) {
  await page.goto(HOST + '/' + hash, { waitUntil: 'networkidle' });
  await page.evaluate(() => document.fonts.ready);
}

(async () => {
  const browser = await chromium.launch({ channel: 'msedge' });
  const PAGES = ['', '#/list', '#/item/example-1', '#/no-such-page'];
  const firstItem = await (async () => { const { ctx, page } = await newPage(browser, { width: 1600, height: 930 }); await go(page, ''); const id = await page.evaluate(() => (window.SITE_DATA.items[0] || {}).id); await ctx.close(); return id; })();
  if (firstItem) PAGES[2] = '#/item/' + firstItem;

  for (const viewport of [{ width: 1600, height: 930 }, { width: 390, height: 844 }]) {
    const tag = viewport.width + ': ';
    const { ctx, page } = await newPage(browser, viewport, viewport.width < 600 ? { isMobile: true, hasTouch: true, deviceScaleFactor: 2 } : {});
    for (const hash of PAGES) {
      await go(page, hash);
      const r = await page.evaluate(() => {
        const h = el => el ? Math.round(el.getBoundingClientRect().height) : 0;
        const top = document.querySelector('[data-jj-top]'), mode = document.querySelector('[data-jj-mode]'), home = document.querySelector('.home-link');
        return {
          mode: document.documentElement.getAttribute('data-mode'),
          page: document.body.getAttribute('data-page'),
          h1: (document.querySelector('#view h1') || {}).textContent || '',
          title: document.title,
          sideways: document.documentElement.scrollWidth - document.documentElement.clientWidth,
          robots: (document.querySelector('meta[name="robots"]') || {}).content,
          csp: (document.querySelector('meta[http-equiv="Content-Security-Policy"]') || {}).content,
          cspHits: window.__csp,
          skip: !!document.querySelector('a.skip[href="#view"]'),
          footName: (document.querySelector('.jj-foot .jj-name') || {}).textContent,
          line1: (document.querySelector('[data-jj-line1]') || {}).textContent,
          familyLine1: window.JJFamily && window.JJFamily.LINE1,
          credits: !!document.querySelector('[data-jj-credits] .cr'),
          topH: h(top), modeH: h(mode),
          level: top && mode ? Math.abs(top.getBoundingClientRect().top - mode.getBoundingClientRect().top) < 2 : false,
          footOrder: [...document.querySelectorAll('.jj-foot > *')].map(e => e.matches('.jj-name') ? 'name' : e.matches('[data-jj-line1]') ? 'line1' : e.matches('[data-jj-credits]') ? 'credits' : e.matches('.jj-foot-links') ? 'links' : '?').join(','),
          modeText: mode && mode.textContent.trim(),
          home: home && { href: home.getAttribute('href'), text: home.textContent.trim(), h: h(home), first: home === document.querySelector('#side a') },
          straight: /'/.test(document.body.innerText),   // British English with curly apostrophes in shown text
          brokenImages: [...document.images].filter(i => !i.complete || i.naturalWidth === 0).map(i => i.getAttribute('src')),
          fonts: [...document.fonts].filter(f => f.status === 'loaded').map(f => f.family.replace(/"/g, '')),
        };
      });
      const p = tag + (hash || '#/') + ': ';
      check(r.mode === 'light', p + 'opens light with the device set to dark');
      check(r.robots === 'noindex, noai, noimageai', p + 'robots meta (noindex, noai, noimageai)');
      check(r.csp === CSP, p + 'the family’s Content-Security-Policy, exactly');
      check(r.cspHits.length === 0, p + 'no Content-Security-Policy violations (' + r.cspHits.slice(0, 2).join(' / ') + ')');
      check(page.errors.length === 0, p + 'no errors (' + page.errors.slice(0, 2).join(' / ') + ')');
      check(r.sideways <= 0, p + 'no sideways scroll (' + r.sideways + 'px)');
      check(r.skip, p + 'skip link');
      check(r.footName === NAME, p + 'footer name “' + NAME + '” (got ' + r.footName + ')');
      check(r.line1 && r.line1 === r.familyLine1, p + 'footer line 1 is the family’s words');
      check(r.credits, p + 'footer credits');
      check(r.footOrder === 'name,line1,credits,links', p + 'footer order name, line 1, credits, buttons (got ' + r.footOrder + ')');
      check(r.topH >= 44 && r.modeH >= 44 && r.level, p + 'Back to top and Dark mode 44px tall and level (' + r.topH + ', ' + r.modeH + ')');
      check(r.modeText === 'Dark mode', p + 'the button says Dark mode while light');
      check(r.home && r.home.href === '/' && r.home.text === '← Jemma’s Journals' && r.home.first && (viewport.width <= 900 || r.home.h >= 24), p + '“← Jemma’s Journals” first in the sidebar, to /, 24px tall');
      check(!r.straight, p + 'no straight apostrophes in the shown text');
      check(r.brokenImages.length === 0, p + 'no broken pictures (' + r.brokenImages.join(', ') + ')');
      check(r.fonts.includes('Instrument Serif') && r.fonts.includes('Manrope'), p + 'local fonts loaded (' + [...new Set(r.fonts)].join(', ') + ')');
      if (hash === '') check(r.page === 'home' && r.title === NAME, p + 'home page, titled “' + NAME + '”');
      if (hash === '#/list') check(r.page === 'list', p + 'the list page');
      if (hash.startsWith('#/item/')) check(r.page === 'item' && r.title.endsWith(' · ' + NAME), p + 'an item page');
      if (hash === '#/no-such-page') check(r.page === 'notfound' && r.h1 === 'Not found', p + 'Not found for an unknown address');
      // accessibility (axe-core): no serious or critical problems, light and dark
      for (const m of ['light', 'dark']) {
        await page.evaluate(x => document.documentElement.setAttribute('data-mode', x), m);
        if (!(await page.evaluate(() => !!window.axe))) await page.evaluate(AXE);   // not addScriptTag: the CSP (rightly) blocks inline scripts
        const bad = await page.evaluate(async () => (await window.axe.run(document, { resultTypes: ['violations'] })).violations
          .filter(v => v.impact === 'serious' || v.impact === 'critical').map(v => v.id + ' (' + v.nodes.slice(0, 2).map(n => n.target.join(' ')).join(' | ') + ')'));
        check(bad.length === 0, p + 'axe, ' + m + ': no serious or critical problems (' + bad.join('; ') + ')');
      }
      await page.evaluate(() => document.documentElement.setAttribute('data-mode', 'light'));
    }
    // following the links: sidebar and list
    await go(page, '');
    if (viewport.width > 900) {
      await page.click('#nav a[href="#/list"]');
      check(await page.evaluate(() => document.body.dataset.page === 'list' && document.activeElement.id === 'view'), tag + 'the sidebar’s list link opens the list, focus on the page');
      await page.click('.cards a');
      check(await page.evaluate(() => document.body.dataset.page === 'item'), tag + 'a card opens its page');
    }
    await ctx.close();
  }

  // dark mode: the footer button switches, saves jj-mode, and a reload keeps it (the family rules, section 1)
  {
    const { ctx, page } = await newPage(browser, { width: 1280, height: 800 });
    await go(page, '');
    const bar0 = await page.getAttribute('meta[name="theme-color"]', 'content');
    await page.click('[data-jj-mode]');
    const d = await page.evaluate(() => ({ mode: document.documentElement.dataset.mode, key: localStorage.getItem('jj-mode'), pressed: document.querySelector('[data-jj-mode]').getAttribute('aria-pressed'), text: document.querySelector('[data-jj-mode]').textContent.trim(), bar: document.querySelector('meta[name="theme-color"]').content, bg: getComputedStyle(document.body).backgroundColor }));
    check(d.mode === 'dark' && d.key === 'dark' && d.pressed === 'true' && d.text === 'Light mode', 'dark: the footer button switches to dark and saves jj-mode');
    check(d.bar !== bar0, 'dark: the phone bar colour follows (theme-color)');
    await page.reload({ waitUntil: 'networkidle' });
    check(await page.evaluate(() => document.documentElement.dataset.mode) === 'dark', 'dark: a reload keeps dark');
    await page.click('[data-jj-mode]');
    check(await page.evaluate(() => document.documentElement.dataset.mode === 'light' && localStorage.getItem('jj-mode') === 'light'), 'dark: pressing again goes back to light');
    await page.click('[data-jj-top]');
    check(await page.evaluate(() => scrollY === 0 && document.activeElement.id === 'view'), 'Back to top scrolls up and moves focus to the page');
    check(page.errors.length === 0, 'dark: no errors (' + page.errors.slice(0, 2).join(' / ') + ')');
    await ctx.close();
  }

  // the Menu drawer: at 899 the bar, at 901 the sidebar (the family rules, section 3)
  {
    const { ctx, page } = await newPage(browser, { width: 899, height: 800 });
    await go(page, '#/list');
    const vis = sel => page.evaluate(s => { const e = document.querySelector(s); const r = e.getBoundingClientRect(); return getComputedStyle(e).display !== 'none' && getComputedStyle(e).visibility !== 'hidden' && r.right > 0 && r.width > 0; }, sel);
    check(await vis('#topbar') && !(await vis('#side')), '899: the slim bar shows and the sidebar is hidden');
    check(await page.evaluate(() => document.querySelector('#side').inert), '899: the closed drawer is inert (Tab can’t reach it)');
    const bar = await page.evaluate(() => ({ btn: Math.round(document.querySelector('#menuBtn').getBoundingClientRect().height), word: document.querySelector('#menuBtn').textContent.trim(), name: getComputedStyle(document.querySelector('.brand-bar')).fontSize }));
    check(bar.btn >= 44 && bar.word === 'Menu' && bar.name === '26px', '899: Menu button 44px with the word Menu, the name 26px (' + JSON.stringify(bar) + ')');
    await page.click('#menuBtn');
    await page.waitForTimeout(350);
    let s = await page.evaluate(() => ({ exp: document.querySelector('#menuBtn').getAttribute('aria-expanded'), focus: document.activeElement.getAttribute('href'), mainInert: document.querySelector('#main').inert, barInert: document.querySelector('#topbar').inert, scrim: !document.querySelector('#scrim').hidden }));
    check(s.exp === 'true' && s.focus === '#/list' && s.mainInert && s.barInert && s.scrim, '899: Menu opens the drawer, focus on the current page’s link, the rest inert (' + JSON.stringify(s) + ')');
    // the family's drawer width and the 44px “← Jemma’s Journals” in it (site/family/README.md, round 5; the template had 84vw and no jj-home-link)
    const dw = await page.evaluate(() => ({ w: Math.round(document.querySelector('#side').getBoundingClientRect().width), home: Math.round(document.querySelector('#side .jj-home-link').getBoundingClientRect().height) }));
    check(dw.w === 300 && dw.home >= 44, '899: the drawer is the family’s width (300px) and its “← Jemma’s Journals” 44px tall (' + JSON.stringify(dw) + ')');
    await page.keyboard.press('Escape');
    s = await page.evaluate(() => ({ exp: document.querySelector('#menuBtn').getAttribute('aria-expanded'), focus: document.activeElement.id, inert: document.querySelector('#side').inert }));
    check(s.exp === 'false' && s.focus === 'menuBtn' && s.inert, '899: Escape closes it and focus goes back to Menu');
    await page.click('#menuBtn'); await page.waitForTimeout(350);
    await page.mouse.click(880, 400);   // the scrim, to the right of the drawer
    check(await page.evaluate(() => document.querySelector('#menuBtn').getAttribute('aria-expanded') === 'false' && document.querySelector('#scrim').hidden), '899: tapping the scrim closes it');
    await page.click('#menuBtn'); await page.waitForTimeout(350);
    await page.click('#nav a[href="#/"]');
    await page.waitForTimeout(100);
    check(await page.evaluate(() => document.body.dataset.page === 'home' && document.querySelector('#menuBtn').getAttribute('aria-expanded') === 'false' && document.activeElement.id === 'view'), '899: a link closes it, opens the page and focuses it');
    await page.setViewportSize({ width: 901, height: 800 });
    await page.waitForTimeout(100);
    check(!(await vis('#topbar')) && await vis('#side') && !(await page.evaluate(() => document.querySelector('#side').inert)), '901: the sidebar shows, no bar, not inert');
    check(page.errors.length === 0, 'drawer: no errors (' + page.errors.slice(0, 2).join(' / ') + ')');
    await ctx.close();
  }

  // screenshots, only when asked: --shots <folder>
  if (SHOTS) {
    fs.mkdirSync(SHOTS, { recursive: true });
    for (const width of [1600, 390]) for (const mode of ['light', 'dark']) for (const [name, hash] of [['home', ''], ['list', '#/list']]) {
      const { ctx, page } = await newPage(browser, { width, height: width > 600 ? 930 : 844 }, width < 600 ? { isMobile: true, hasTouch: true, deviceScaleFactor: 2 } : {});
      await ctx.addInitScript(m => { try { localStorage.setItem('jj-mode', m); } catch (e) {} }, mode);
      await go(page, hash);
      await page.screenshot({ path: path.join(SHOTS, `${name}-${width}-${mode}.jpg`), quality: 85, fullPage: true });
      await ctx.close();
    }
    console.log('screenshots in ' + SHOTS);
  }

  await browser.close();
  console.log(`${passes} passed, ${failures} failed`);
  process.exit(failures ? 1 : 0);
})().catch(e => { console.error(e); process.exit(1); });
