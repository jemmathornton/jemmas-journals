// Record screenshots of the Pokédex games as chosen (22 Nov evening): each game's Home = the totals and the region hub; the
// "All games" link above the HOME | GO switch, and the All games page. Dark mode is set directly on the page (never her button
// or the family server's mode file). Every POST is blocked: nothing is saved.
// Run from Jemma's Journals: .tools/node/node.exe for-jemma/concepts/pokedex-games/shoot.js
// (Round 1 is in this folder and round 2 in round2/, made by earlier versions of this script.)
const path = require('path'), fs = require('fs');
const { chromium } = require(path.join(__dirname, '../../../node_modules/playwright'));
const OUT = path.join(__dirname, 'chosen'), BASE = 'http://localhost:8050/pokedex/';
fs.mkdirSync(OUT, { recursive: true });
const shots = [];   // [name, hash, width, mode, drawer]
for (const [n, hash] of [['home-home', '#home'], ['home-go', '#go'], ['all-games', '#games'], ['go-kanto', '#gen-1']])
  for (const w of [1600, 1000, 390]) for (const m of ['light', 'dark']) shots.push([`${n}-${w}-${m}`, hash, w, m, false]);
for (const m of ['light', 'dark']) shots.push([`drawer-390-${m}`, '#home', 390, m, true]);
(async () => {
  const browser = await chromium.launch({ channel: 'msedge' });
  let posts = 0;
  for (const [name, hash, w, mode, drawer] of shots) {
    const ctx = await browser.newContext({ viewport: { width: w, height: w <= 390 ? 844 : 930 }, deviceScaleFactor: 1 });
    await ctx.route('**/*', r => { if (r.request().method() !== 'GET') { posts++; return r.abort(); } return r.continue(); });
    const page = await ctx.newPage();
    await page.goto(BASE + hash, { waitUntil: 'networkidle' });
    if (mode === 'dark') await page.evaluate(() => document.documentElement.setAttribute('data-mode', 'dark'));
    await page.waitForTimeout(400);
    if (drawer) { await page.click('#menuBtn'); await page.waitForTimeout(400); }
    await page.screenshot({ path: path.join(OUT, name + '.jpg'), type: 'jpeg', quality: 82, fullPage: w <= 390 && !drawer && hash !== '#gen-1' });
    await ctx.close();
  }
  await browser.close();
  console.log(shots.length, 'shots; POSTs blocked:', posts);
})();
