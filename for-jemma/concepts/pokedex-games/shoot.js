// Screenshots of the Pokédex games (record only): the sidebar switch, HOME as the default (a Placeholder), and the Home page
// Try row (As now / Region hub / Progress panel / Box view) for GO (#go) and HOME (#home). Every POST is blocked: nothing is saved.
// Run from Jemma's Journals: .tools/node/node.exe for-jemma/concepts/pokedex-games/shoot.js
const path = require('path'), fs = require('fs');
const { chromium } = require(path.join(__dirname, '../../../node_modules/playwright'));
const OUT = path.join(__dirname, 'round2'), BASE = 'http://localhost:8050/pokedex/';
fs.mkdirSync(OUT, { recursive: true });
const shots = [];   // [name, look, hash, width, mode, extra, all]
for (const look of ['now', 'hub', 'panel', 'boxes']) for (const [game, hash] of [['go', '#go'], ['home', '#home']])
  for (const w of [1600, 1280, 1000, 390]) for (const m of ['light', 'dark']) shots.push([`home-${look}-${game}-${w}-${m}`, look, hash, w, m]);
for (const all of ['link', 'tab']) for (const w of [1600, 1280, 1000, 390]) for (const m of ['light', 'dark']) shots.push([`allgames-${all}-${w}-${m}`, 'now', '#games', w, m, w <= 900 ? 'drawer' : null, all]);
for (const all of ['link', 'tab']) shots.push([`allgames-${all}-page-390-light`, 'now', '#games', 390, 'light', null, all]);
for (const m of ['light', 'dark']) { shots.push([`switch-go-kanto-1600-${m}`, 'now', '#gen-1', 1600, m]); shots.push([`switch-drawer-390-${m}`, 'now', '#home', 390, m, 'drawer']); }
(async () => {
  const browser = await chromium.launch({ channel: 'msedge' });
  let posts = 0;
  for (const [name, look, hash, w, mode, extra, all] of shots) {
    const ctx = await browser.newContext({ viewport: { width: w, height: w <= 390 ? 844 : 930 }, deviceScaleFactor: 1 });
    await ctx.route('**/*', r => { if (r.request().method() !== 'GET') { posts++; return r.abort(); } return r.continue(); });
    await ctx.addInitScript(([l, a]) => { localStorage.setItem('jemmas-pokedex-try-homepage', JSON.stringify(l)); localStorage.setItem('jemmas-pokedex-try-allgames', JSON.stringify(a || 'none')); }, [look, all]);
    const page = await ctx.newPage();
    await page.goto(BASE + hash, { waitUntil: 'networkidle' });
    if (mode === 'dark') await page.evaluate(() => document.documentElement.setAttribute('data-mode', 'dark'));
    await page.waitForTimeout(400);
    if (extra === 'drawer') { await page.click('#menuBtn'); await page.waitForTimeout(400); }
    await page.screenshot({ path: path.join(OUT, name + '.jpg'), type: 'jpeg', quality: 82, fullPage: !extra && w >= 1000 ? false : !extra });
    await ctx.close();
  }
  await browser.close();
  console.log(shots.length, 'shots; POSTs blocked:', posts);
})();
