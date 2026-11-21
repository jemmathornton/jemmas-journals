// usage: node shoot.js <name> [cssfile] [outdir]
const { chromium } = require('C:/Users/Jemma/Documents/SimTracker/node_modules/playwright');
const fs = require('fs'), path = require('path');
const SITE = 'C:/Users/Jemma/Documents/SimTracker/site';
const name = process.argv[2] || 'now';
const cssFile = process.argv[3];
const out = process.argv[4] || path.join(__dirname, 'out');
const inner = process.env.INNER || '#n-willow-creek-foundry-cove';
async function anchor(page, sel, off){ await page.evaluate(([sel,off])=>{const e=document.querySelector(sel); if(e) window.scrollTo(0, e.getBoundingClientRect().top + scrollY - off);},[sel,off]); await page.waitForTimeout(500); }
fs.mkdirSync(out, { recursive: true });
const types = {'.html':'text/html; charset=utf-8','.css':'text/css; charset=utf-8','.js':'text/javascript; charset=utf-8','.jpg':'image/jpeg','.jpeg':'image/jpeg','.png':'image/png','.webp':'image/webp','.svg':'image/svg+xml','.ico':'image/x-icon','.woff2':'font/woff2','.woff':'font/woff','.ttf':'font/ttf','.json':'application/json'};
const css = cssFile ? fs.readFileSync(cssFile, 'utf8') : '';
const JS = cssFile && fs.existsSync(cssFile.replace(/\.css$/, '.js')) ? fs.readFileSync(cssFile.replace(/\.css$/, '.js'), 'utf8') : '';
async function setup(ctx) {
  await ctx.route('http://simworld.test/**', async route => {
    const u = new URL(route.request().url());
    let p = decodeURIComponent(u.pathname); if (p === '/') p = '/index.html';
    const f = path.join(SITE, p);
    if (!fs.existsSync(f)) return route.fulfill({ status: 404, body: 'nf' });
    let body = fs.readFileSync(f);
    if (p === '/index.html' && css) body = Buffer.from(body.toString('utf8').replace('</head>', `<style id="mock">${css}</style></head>`));
    route.fulfill({ status: 200, body, headers: { 'content-type': types[path.extname(f).toLowerCase()] || 'application/octet-stream' } });
  });
}
async function go(page, hash) {
  await page.goto('http://simworld.test/index.html' + hash, { waitUntil: 'load' });
  await page.evaluate(() => document.fonts.ready);
  if (JS) await page.evaluate(JS);
  await page.waitForTimeout(700);
}
(async () => {
  const browser = await chromium.launch({ channel: 'msedge' });
  const lap = await browser.newContext({ viewport: { width: 1600, height: 930 }, colorScheme: 'light' });
  await setup(lap);
  const p = await lap.newPage();
  p.on('pageerror', e => console.log('ERR', e.message));
  await go(p, '#home');
  const scrollY = Number(process.env.HOMESCROLL || 0);
  if (scrollY) { await p.evaluate(y => window.scrollTo(0, y), scrollY); await p.waitForTimeout(300); }
  await p.screenshot({ path: path.join(out, `${name}-home-1600.png`) });
  if (process.env.FULL) await p.screenshot({ path: path.join(out, `${name}-home-1600-full.png`), fullPage: true });
  const IH = Number(process.env.INNERH || 1240);
  await p.setViewportSize({ width: 1600, height: IH });
  await go(p, inner);
  await p.screenshot({ path: path.join(out, `${name}-inner-1600.png`),  });
  if (process.env.FULL) await p.screenshot({ path: path.join(out, `${name}-inner-1600-full.png`), fullPage: true });
  const ph = await browser.newContext({ viewport: { width: 390, height: 844 }, deviceScaleFactor: 2, isMobile: true, hasTouch: true, colorScheme: 'light' });
  await setup(ph);
  const q = await ph.newPage();
  await go(q, '#home');
  await anchor(q, '.hero-foot', Number(process.env.PHONEOFF || 76));
  await q.screenshot({ path: path.join(out, `${name}-home-phone.png`) });
  if (process.env.FULL) await q.screenshot({ path: path.join(out, `${name}-home-phone-full.png`), fullPage: true });
  await browser.close();
})();
