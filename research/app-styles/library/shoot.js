// usage: node shoot.js <style: now|l1|l2> [hash for inner page]
const { chromium } = require('C:/Users/Jemma/Documents/SimTracker/node_modules/playwright');
const fs = require('fs'), path = require('path');
const SITE = 'C:/Users/Jemma/Documents/HomeLibrary/site';
const ORIGIN = 'http://library.test/';
const TYPES = {'.html':'text/html; charset=utf-8','.css':'text/css; charset=utf-8','.js':'application/javascript; charset=utf-8','.json':'application/json','.svg':'image/svg+xml','.png':'image/png','.jpg':'image/jpeg','.jpeg':'image/jpeg','.webp':'image/webp','.ico':'image/x-icon','.txt':'text/plain'};
const style = process.argv[2] || 'now';
const inner = process.argv[3] || '';
const css = style === 'now' ? '' : fs.readFileSync(path.join(__dirname, style + '.css'), 'utf8').replace(/(@import url\("[^"]*"\);)?/, m => m + '\n' + fs.readFileSync(path.join(__dirname, 'phone.css'), 'utf8') + '\n');
const prep = fs.existsSync(path.join(__dirname, style + '.js')) ? fs.readFileSync(path.join(__dirname, style + '.js'), 'utf8') : '';
const OUT = path.join(__dirname, 'out');

async function setup(ctx){
  await ctx.route('**/*', async route => {
    const u = new URL(route.request().url());
    if (u.origin + '/' !== ORIGIN) return route.continue();
    let p = decodeURIComponent(u.pathname); if (p === '/') p = '/index.html';
    const f = path.join(SITE, p);
    if (!f.startsWith(path.normalize(SITE)) || !fs.existsSync(f) || fs.statSync(f).isDirectory()) return route.fulfill({status:404, body:'not found'});
    route.fulfill({status:200, contentType: TYPES[path.extname(f).toLowerCase()] || 'application/octet-stream', body: fs.readFileSync(f)});
  });
  await ctx.addInitScript(() => { try { navigator.serviceWorker.register = () => Promise.reject(); } catch {} });
}
async function shot(page, hash, file, full){
  await page.goto(ORIGIN + 'index.html' + hash, {waitUntil:'networkidle'});
  if (css) await page.addStyleTag({content: css});
  if (prep) await page.evaluate(prep);
  await page.evaluate(() => document.fonts.ready);
  await page.evaluate(() => { if (typeof fitRows === 'function') fitRows(); });
  await page.waitForTimeout(700);
  await page.screenshot({path: path.join(OUT, file), fullPage: !!full});
}
(async () => {
  const b = await chromium.launch({channel:'msedge'});
  const lap = await b.newContext({viewport:{width:1600,height:930}, colorScheme:'light', reducedMotion:'reduce'});
  await setup(lap);
  const p1 = await lap.newPage();
  p1.on('pageerror', e => console.log('pageerror', e.message));
  await shot(p1, '#home', `${style}-home-1600.png`);
  await shot(p1, '#home', `${style}-home-1600-full.png`, true);
  if (inner) { await shot(p1, inner, `${style}-inner-1600.png`); await shot(p1, inner, `${style}-inner-1600-full.png`, true); }
  const ph = await b.newContext({viewport:{width:390,height:844}, deviceScaleFactor:2, isMobile:true, hasTouch:true, colorScheme:'light', reducedMotion:'reduce'});
  await setup(ph);
  const p2 = await ph.newPage();
  await shot(p2, '#home', `${style}-home-phone.png`);
  await b.close();
})();
