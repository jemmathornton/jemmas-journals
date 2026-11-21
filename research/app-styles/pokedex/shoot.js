// Mock-up shots of Jemma's Pokédex: serves site/ straight from disk (read only), injects a style's CSS, screenshots.
// usage: node shoot.js <style: now|p1|p2> [what: all|home|inner|phone|dump]
const { chromium } = require('C:/Users/Jemma/Documents/SimTracker/node_modules/playwright');
const fs = require('fs'), path = require('path');
const SITE = 'C:/Users/Jemma/Documents/Pokedex/site';
const COLL = 'C:/Users/Jemma/Documents/Pokedex/data/collection/go.json';
const HERE = __dirname;
const OUT = 'C:/Users/Jemma/Documents/JemmasJournals/for-jemma/concepts/app-styles';
const style = process.argv[2] || 'now', what = process.argv[3] || 'all';
const TYPES = { '.html': 'text/html; charset=utf-8', '.css': 'text/css; charset=utf-8', '.js': 'text/javascript; charset=utf-8', '.png': 'image/png', '.jpg': 'image/jpeg', '.jpeg': 'image/jpeg', '.webp': 'image/webp', '.svg': 'image/svg+xml', '.ico': 'image/x-icon', '.woff2': 'font/woff2', '.woff': 'font/woff', '.ttf': 'font/ttf', '.json': 'application/json' };
const ORIGIN = 'http://pokedex.localhost';
const css = style === 'now' ? '' : fs.readFileSync(path.join(HERE, style + '.css'), 'utf8');
const HIDE = `.toast{display:none!important}`;

async function setup(ctx) {
  await ctx.route('**/*', async route => {
    const u = new URL(route.request().url());
    if (u.origin !== ORIGIN) return route.abort();
    if (u.pathname === '/api/collection') return route.fulfill({ status: 200, contentType: 'application/json', body: fs.readFileSync(COLL) });
    if (u.pathname.startsWith('/api/')) return route.fulfill({ status: 503, contentType: 'application/json', body: '{"ok":false}' });
    let p = decodeURIComponent(u.pathname); if (p === '/') p = '/index.html';
    const f = path.join(SITE, p);
    if (!f.startsWith(path.normalize(SITE)) || !fs.existsSync(f) || fs.statSync(f).isDirectory()) return route.fulfill({ status: 404, body: '' });
    route.fulfill({ status: 200, contentType: TYPES[path.extname(f).toLowerCase()] || 'application/octet-stream', body: fs.readFileSync(f) });
  });
}
async function open(ctx, hash) {
  const page = await ctx.newPage();
  await page.addInitScript(() => { try { localStorage.setItem('jemmas-pokedex-view', JSON.stringify({workShow: 'all'})); } catch {} });
  await page.goto(ORIGIN + '/' + hash, { waitUntil: 'networkidle' });
  await page.addStyleTag({ content: HIDE + css });
  if (style !== 'now') await page.evaluate(s => document.documentElement.classList.add('mock-' + s), style);
  await page.waitForTimeout(500);
  await page.evaluate(() => document.fonts.ready);
  await page.evaluate(() => Promise.race([new Promise(r => setTimeout(r, 4000)), Promise.all([...document.images].filter(i => !i.complete && i.getBoundingClientRect().top < innerHeight).map(i => new Promise(r => { i.onload = i.onerror = r; })))]));
  await page.waitForTimeout(300);
  return page;
}
(async () => {
  fs.mkdirSync(OUT, { recursive: true });
  const browser = await chromium.launch({ channel: 'msedge' });
  const lap = await browser.newContext({ viewport: { width: 1600, height: 930 }, colorScheme: 'light' });
  await setup(lap);
  const INNER = process.env.INNER || '#gen-8';
  if (what === 'all' || what === 'home') { const p = await open(lap, '#home'); await p.screenshot({ path: `${OUT}/pokedex-${style}-laptop.png` }); }
  if (what === 'all' || what === 'inner') {
    const tall = await browser.newContext({ viewport: { width: 1600, height: +(process.env.H || 1560) }, colorScheme: 'light' });
    await setup(tall);
    const p = await open(tall, INNER);
    await p.screenshot({ path: `${OUT}/pokedex-${style}-inner.png` });
  }
  if (what === 'all' || what === 'phone') {
    const ph = await browser.newContext({ viewport: { width: 390, height: 844 }, deviceScaleFactor: 2, isMobile: true, hasTouch: true, colorScheme: 'light' });
    await setup(ph);
    const p = await open(ph, '#home'); await p.screenshot({ path: `${OUT}/pokedex-${style}-phone.png` });
    // the same phone scrolled to where the page itself starts (under the sidebar), so the restyle shows there too
    const y = await p.evaluate(() => document.querySelector('main').getBoundingClientRect().top + scrollY);
    await p.evaluate(y => scrollTo(0, y), y); await p.waitForTimeout(400);
    await p.evaluate(() => Promise.race([new Promise(r => setTimeout(r, 3000)), Promise.all([...document.images].filter(i => !i.complete && i.getBoundingClientRect().top < innerHeight).map(i => new Promise(r => { i.onload = i.onerror = r; })))]));
    await p.screenshot({ path: `${OUT}/pokedex-${style}-phone-2.png` });
  }
  await browser.close();
})().catch(e => { console.error(e); process.exit(1); });
