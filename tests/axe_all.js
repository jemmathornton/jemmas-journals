// Accessibility check of the whole family with axe-core (her OK, 22 Nov), through the one address http://localhost:8050.
// Run:  .tools/node/node.exe tests/axe_all.js [--strict]
// Checks a few pages of every site at 1600 and 390 wide, light and dark, and lists serious and critical problems
// (contrast, names on buttons and links, labels…). Never saves anything: every POST is answered in the browser.
// Without --strict it only reports (exit 0); with --strict any serious/critical problem fails (exit 1).
const { chromium } = require('playwright');
const fs = require('fs'), path = require('path');
const AXE = fs.readFileSync(require.resolve('axe-core/axe.min.js'), 'utf8');
const BASE = 'http://localhost:8050';
const PAGES = [
  '/', '/library/#home', '/library/#stats', '/sim-world/#home', '/sim-world/#w-willow-creek', '/sim-world/#s-bella-goth',
  '/pokedex/#home', '/pokedex/#gen-1', '/pokedex/#p-6', '/travels/', '/travels/#/stats',
];
(async () => {
  const browser = await chromium.launch({ channel: 'msedge' });
  const found = new Map();
  for (const width of [1600, 390]) for (const mode of ['light', 'dark']) {
    const ctx = await browser.newContext({ viewport: { width, height: 900 }, reducedMotion: 'reduce' });
    await ctx.route('**/*', r => r.request().method() === 'POST' ? r.fulfill({ status: 503, body: '' }) : r.continue());
    const page = await ctx.newPage();
    for (const p of PAGES) {
      await page.goto(BASE + p, { waitUntil: 'networkidle' }).catch(() => {});
      await page.evaluate(m => { document.documentElement.setAttribute('data-mode', m); }, mode);
      await page.waitForTimeout(300);
      await page.addScriptTag({ content: AXE });
      const res = await page.evaluate(async () => (await window.axe.run(document, { resultTypes: ['violations'] })).violations
        .filter(v => v.impact === 'serious' || v.impact === 'critical')
        .map(v => ({ id: v.id, impact: v.impact, help: v.help, nodes: v.nodes.slice(0, 3).map(n => n.target.join(' ')), count: v.nodes.length })));
      for (const v of res) {
        const key = (p.split('/')[1] || 'home') + ' · ' + v.id;
        const f = found.get(key) || { ...v, where: new Set() };
        f.where.add(`${p} ${width} ${mode} (${v.count})`); found.set(key, f);
      }
    }
    await ctx.close();
  }
  await browser.close();
  const lines = [...found.entries()].sort().map(([k, v]) => `${v.impact.padEnd(8)} ${k}: ${v.help}\n           e.g. ${v.nodes.join(' | ')}\n           on ${[...v.where].slice(0, 4).join('; ')}${v.where.size > 4 ? ' …' : ''}`);
  const out = lines.length ? `${lines.length} kinds of serious/critical problem:\n` + lines.join('\n') : 'No serious or critical accessibility problems found.';
  console.log(out);
  fs.mkdirSync(path.join(__dirname, '..', 'logs', 'check-all'), { recursive: true });
  fs.writeFileSync(path.join(__dirname, '..', 'logs', 'check-all', 'axe.txt'), out + '\n');
  process.exit(process.argv.includes('--strict') && lines.length ? 1 : 0);
})();
