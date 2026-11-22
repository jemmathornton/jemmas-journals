// The family rules, checked once for all five sites (research/family-rules.md, site/family/README.md).
// Run:  .tools/node/node.exe tests/family/family.test.js [--only <words>] [--build-dir <folder>]
//
// Starts its OWN servers on spare ports, so it never touches her family server (8050), her dark-mode file or her apps' save servers:
//   1. tests/family/serve_family.py: the real tools/serve_all.py handler, with the dark-mode choice in a temp file and the save
//      servers replaced by a port nothing listens on (saves get the 503 page);
//   2. tests/family/serve_build.py: tools/build_site.py's online-style build in a temp folder, served like a plain web host
//      (as http://localhost:8060 does). --build-dir (or JJ_BUILD_DIR) reuses a build already made.
// Every POST from a page goes only to these test servers. Prints one line per test and a summary; exit 1 on any failure.
const { chromium } = require('playwright');
const { spawn } = require('child_process');
const fs = require('fs'), os = require('os'), path = require('path'), net = require('net');

const ROOT = path.join(__dirname, '..', '..');
const PY = process.env.JJ_PYTHON || 'C:/Users/Jemma/AppData/Local/Programs/Python/Python313/python.exe';
const LINE1 = /var LINE1 = "([^"]+)"/.exec(fs.readFileSync(path.join(ROOT, 'site', 'family', 'family.js'), 'utf8'))[1];
const ROBOTS = 'noindex, noai, noimageai';
const SITES = [
  { key: 'home', path: '/', name: 'Jemma’s Journals', sidebar: false },
  { key: 'library', path: '/library/', name: 'Jemma’s Library', sidebar: true, oldKey: 'jemmas-library-mode' },
  { key: 'sim-world', path: '/sim-world/', name: 'Jemma’s Sim World', sidebar: true, oldKey: 'jsw-mode' },
  { key: 'pokedex', path: '/pokedex/', name: 'Jemma’s Pokédex', sidebar: true, oldKey: 'jemmas-pokedex-mode' },
  { key: 'travels', path: '/travels/', name: 'Jemma’s Travels', sidebar: true, oldKey: 'jt-mode' },
];
const APPS = SITES.filter(s => s.sidebar);
const arg = n => { const i = process.argv.indexOf(n); return i > 0 ? process.argv[i + 1] : null; };
const ONLY = arg('--only');

// ---------- a small harness: test(name, fn); fn gets t with t.ok(cond, msg); a test fails on any false t.ok or a throw ----------
const TESTS = [];
const test = (name, fn) => TESTS.push({ name, fn });
const freePort = () => new Promise(done => { const s = net.createServer(); s.listen(0, '127.0.0.1', () => { const p = s.address().port; s.close(() => done(p)); }); });
const children = [];
function startServer(script, args, timeoutMs) {
  return new Promise((resolve, reject) => {
    const child = spawn(PY, ['-I', '-X', 'utf8', path.join(__dirname, script), ...args], { cwd: ROOT, stdio: ['ignore', 'pipe', 'pipe'] });
    children.push(child);
    let out = '';
    const timer = setTimeout(() => reject(new Error(`${script} did not start in ${timeoutMs / 1000}s: ${out.slice(-400)}`)), timeoutMs);
    const onData = d => { out += d; if (/ready \d+/.test(out)) { clearTimeout(timer); resolve(child); } };
    child.stdout.on('data', onData); child.stderr.on('data', d => { out += d; });
    child.on('exit', code => { clearTimeout(timer); reject(new Error(`${script} stopped (exit ${code}): ${out.slice(-400)}`)); });
  });
}
const stopAll = () => children.forEach(c => { try { c.kill(); } catch (e) {} });
process.on('exit', stopAll);

let browser, FAM, WEB, MODE_FILE;   // FAM: the test family server's address; WEB: the online-style copy's
const readMode = () => { try { return fs.readFileSync(MODE_FILE, 'utf8').trim(); } catch (e) { return ''; } };
const resetMode = () => fs.writeFileSync(MODE_FILE, 'light');

// a browser context that records, for every page in it: page errors, console errors, failed responses, requests to other
// sites and Content Security Policy violations. Expected: the save requests (…/api/…), which have no server here.
async function context(opts = {}) {
  const ctx = await browser.newContext({ viewport: { width: 1600, height: 1000 }, colorScheme: 'dark', reducedMotion: 'reduce', ...opts });
  ctx.log = { errors: [], bad: [], outside: [], requests: [] };
  await ctx.addInitScript(() => {
    window.__csp = [];
    document.addEventListener('securitypolicyviolation', e => window.__csp.push(`${e.violatedDirective} blocked ${e.blockedURI || 'inline'} at ${e.sourceFile || ''}:${e.lineNumber || ''}`));
  });
  ctx.on('page', page => watch(ctx, page));
  return ctx;
}
const isApi = u => /\/api\//.test(u);
function watch(ctx, page) {
  page.on('pageerror', e => ctx.log.errors.push('page error: ' + e.message));
  page.on('console', m => {
    if (m.type() !== 'error') return;
    const u = (m.location() || {}).url || '';
    if (/Failed to load resource/.test(m.text()) && (isApi(u) || ctx.allow404)) return;   // reported by the response check below
    ctx.log.errors.push('console: ' + m.text().slice(0, 200));
  });
  page.on('request', r => {
    const u = r.url(); ctx.log.requests.push(u);
    if (!/^(data|blob|about):/.test(u) && new URL(u).origin !== ctx.origin) ctx.log.outside.push(u);
  });
  page.on('response', r => { if (r.status() >= 400 && !isApi(r.url()) && !ctx.allow404) ctx.log.bad.push(r.status() + ' ' + r.url()); });
}
async function open(ctx, base, p, opts = {}) {
  ctx.origin = new URL(base).origin;
  const page = opts.page || await ctx.newPage();
  await page.goto(base + p, { waitUntil: 'networkidle' });
  await page.waitForFunction(() => { const b = document.querySelector('[data-jj-mode]'); return b && b.hasAttribute('data-jj-painted'); }, null, { timeout: 15000 })
    .catch(() => { throw new Error(`${base + p}: the family code never drew the Dark mode button (family.js did not run)`); });
  await page.evaluate(() => document.fonts.ready);
  await page.waitForTimeout(150);
  return page;
}
// a real click; if something covers the control (it can't be pressed), that is a failure, and the test goes on with a
// script click so the rest of the checks still run
async function press(t, page, sel, where) {
  try { await page.click(sel, { timeout: 4000 }); return; } catch (e) {
    const msg = e.message.replace(/\x1b\[[0-9;]*m/g, '');
    const why = (/(<[^>]+>[^\n]*intercepts pointer events)/.exec(msg) || [, msg.split('\n')[0]])[1];
    t.ok(false, `${where}: ${sel} can be clicked (${why.slice(0, 160)})`);
    await page.evaluate(s => document.querySelector(s).click(), sel);
  }
}
const csp = page => page.evaluate(() => window.__csp || []);
const sideways = page => page.evaluate(() => document.documentElement.scrollWidth - document.documentElement.clientWidth);
const mode = page => page.evaluate(() => document.documentElement.getAttribute('data-mode'));
const clean = (t, ctx, where) => {
  t.ok(!ctx.log.errors.length, `${where}: no errors (${ctx.log.errors.slice(0, 3).join(' / ')})`);
  t.ok(!ctx.log.bad.length, `${where}: every file loads (${ctx.log.bad.slice(0, 3).join(', ')})`);
  t.ok(!ctx.log.outside.length, `${where}: nothing from other sites (${ctx.log.outside.slice(0, 3).join(', ')})`);
  ctx.log.errors = []; ctx.log.bad = []; ctx.log.outside = [];
};

// ---------- on her PC: the family server (a test copy) ----------
for (const width of [1600, 1280, 901, 899, 390]) {
  test(`every site opens light with the device set to dark, cleanly, with no sideways scroll and no CSP violation (${width}px)`, async t => {
    const ctx = await context({ viewport: { width, height: 900 } });
    for (const s of SITES) {
      const page = await open(ctx, FAM, s.path);
      t.ok(await mode(page) === 'light', `${s.key}: opens light (got ${await mode(page)})`);
      t.ok(await sideways(page) <= 0, `${s.key}: no sideways scroll (${await sideways(page)}px)`);
      // use the shared parts, then look for violations (the policy is enforced in this context)
      await press(t, page, '[data-jj-mode]', s.key); await press(t, page, '[data-jj-mode]', s.key);
      if (s.sidebar && width < 900) { await press(t, page, '#menuBtn', s.key); await page.keyboard.press('Escape'); }
      const v = await csp(page);
      t.ok(!v.length, `${s.key}: no CSP violations (${v.slice(0, 2).join(' / ')})`);
      clean(t, ctx, s.key);
      await page.close();
    }
    resetMode();
    await ctx.close();
  });
}

test('robots meta, a Content Security Policy before any script, no inline scripts, on every site and the 404 page', async t => {
  const ctx = await context();
  ctx.allow404 = true;
  for (const p of [...SITES.map(s => s.path), '/no-such-page', '/library/no-such-page']) {
    const page = await ctx.newPage(); ctx.origin = new URL(FAM).origin;
    const res = await page.goto(FAM + p, { waitUntil: 'networkidle' });
    if (/no-such/.test(p)) t.ok(res.status() === 404, `${p}: 404 status (got ${res.status()})`);
    const r = await page.evaluate(() => {
      const m = document.querySelector('meta[http-equiv="Content-Security-Policy"]'), first = document.querySelector('script');
      return { robots: (document.querySelector('meta[name="robots"]') || {}).content, policy: m && m.content,
        before: !!(m && (!first || (m.compareDocumentPosition(first) & Node.DOCUMENT_POSITION_FOLLOWING))),
        inline: [...document.scripts].filter(s => !s.src && s.textContent.trim()).length,
        handlers: [...document.querySelectorAll('*')].flatMap(e => [...e.attributes].filter(a => /^on/i.test(a.name)).map(a => e.tagName + ' ' + a.name)).length };
    });
    t.ok(r.robots === ROBOTS, `${p}: robots meta is “${ROBOTS}” (got ${r.robots})`);
    t.ok(!!r.policy, `${p}: has a Content Security Policy`);
    const script = ((r.policy || '').match(/script-src ([^;]*)/) || [, ''])[1];
    t.ok(/'self'/.test(script) && !/unsafe-inline|unsafe-eval|https?:|\*/.test(script), `${p}: scripts only from the site itself (script-src ${script})`);
    t.ok(/default-src 'self'/.test(r.policy || '') && /object-src 'none'/.test(r.policy || ''), `${p}: default-src 'self' and object-src 'none'`);
    t.ok(r.before, `${p}: the policy comes before the first script`);
    t.ok(r.inline === 0 && r.handlers === 0, `${p}: no inline scripts or on…= handlers (${r.inline}, ${r.handlers})`);
    await page.close();
  }
  for (const f of ['robots.txt']) {
    const res = await (await ctx.newPage()).goto(FAM + '/' + f);
    t.ok(res.status() === 200 && /Disallow: \//.test(await res.text()), `/${f}: there, asking AI crawlers to stay away`);
  }
  await ctx.close();
});

test('the shared code: /family/ files served with the right types, loaded in the right order, JJFamily there, old keys named', async t => {
  const ctx = await context();
  const page = await ctx.newPage();
  for (const [f, type] of [['mode.js', /javascript/], ['family.css', /text\/css/], ['family.js', /javascript/]]) {
    const r = await page.request.get(FAM + '/family/' + f);
    t.ok(r.status() === 200 && type.test(r.headers()['content-type'] || ''), `/family/${f}: 200 with ${type} (got ${r.status()} ${r.headers()['content-type']})`);
  }
  for (const s of SITES) {
    await open(ctx, FAM, s.path, { page });
    const r = await page.evaluate(() => {
      const list = [...document.head.querySelectorAll('script[src], link[rel="stylesheet"]')].map(e => (e.getAttribute('src') || e.getAttribute('href')).split('?')[0]);
      const ms = document.querySelector('script[src$="family/mode.js"]');
      return { list, family: typeof window.JJFamily === 'object' && typeof JJFamily.menu === 'function' && JJFamily.LINE1, oldKey: ms && ms.getAttribute('data-old-key') };
    });
    const at = n => r.list.findIndex(x => x.endsWith('family/' + n));
    const own = r.list.findIndex(x => !/family\//.test(x) && /\.css$/.test(x));
    t.ok(at('mode.js') >= 0 && at('family.css') > at('mode.js') && at('family.js') >= 0, `${s.key}: loads mode.js, then family.css and family.js (${r.list.join(', ')})`);
    t.ok(own < 0 || at('family.css') < own, `${s.key}: family.css before the site’s own stylesheet`);
    t.ok(r.family === LINE1, `${s.key}: window.JJFamily is there`);
    if (s.oldKey) t.ok(r.oldKey === s.oldKey, `${s.key}: mode.js keeps the old key ${s.oldKey} working once (got ${r.oldKey})`);
  }
  clean(t, ctx, 'shared code');
  await ctx.close();
});

for (const width of [1600, 390]) {
  test(`the footer: name, line 1, credits, then Back to top and Dark mode, 44px and level, 12.5px text (${width}px)`, async t => {
    const ctx = await context({ viewport: { width, height: 900 } });
    const page = await ctx.newPage();
    for (const s of SITES) {
      await open(ctx, FAM, s.path, { page });
      const r = await page.evaluate(() => {
        const f = [...document.querySelectorAll('footer')], foot = f[0];
        const name = foot.querySelector('.jj-name') || foot.querySelector('b'), l1 = foot.querySelector('[data-jj-line1]'), cr = foot.querySelector('[data-jj-credits]');
        const top = foot.querySelector('[data-jj-top]'), btn = foot.querySelector('[data-jj-mode]');
        const order = [name, l1, cr, top, btn].every((e, i, a) => e && (i === 0 || (a[i - 1].compareDocumentPosition(e) & Node.DOCUMENT_POSITION_FOLLOWING)));
        const box = e => e.getBoundingClientRect();
        return { footers: f.length, name: name && name.textContent.trim(), italic: name && getComputedStyle(name).fontStyle, line1: l1 && l1.textContent,
          credits: [...cr.querySelectorAll('.cr')].map(c => c.textContent), order,
          sizes: [l1, cr].map(e => getComputedStyle(e).fontSize), topText: top.textContent.trim(), btnText: btn.textContent.trim(),
          icons: !!top.querySelector('svg') && !!btn.querySelector('svg'), tall: Math.min(box(top).height, box(btn).height),
          level: Math.abs(box(top).top - box(btn).top), pressed: btn.getAttribute('aria-pressed'), type: btn.getAttribute('type') };
      });
      t.ok(r.footers === 1, `${s.key}: one footer (got ${r.footers})`);
      t.ok(r.name === s.name && r.italic === 'normal', `${s.key}: the footer name is ${s.name}, plain (got ${r.name}, ${r.italic})`);
      t.ok(r.line1 === LINE1, `${s.key}: line 1 is family.js’s words (got “${r.line1}”)`);
      t.ok(r.credits.length >= 2 && r.credits.every(c => /^[A-Z]/.test(c)), `${s.key}: credits each start with a capital (${r.credits.join(' | ')})`);
      t.ok(r.order, `${s.key}: in order: name, line 1, credits, Back to top, Dark mode`);
      t.ok(r.sizes.every(x => x === '12.5px'), `${s.key}: footer text 12.5px (${r.sizes})`);
      t.ok(r.topText === 'Back to top' && r.btnText === 'Dark mode' && r.icons, `${s.key}: “Back to top” and “Dark mode” with icons (${r.topText} / ${r.btnText})`);
      t.ok(r.tall >= 44, `${s.key}: both footer buttons at least 44px tall (${r.tall})`);
      t.ok(r.level < 2, `${s.key}: Back to top and Dark mode level (${r.level}px apart)`);
      t.ok(r.pressed === 'false' && r.type === 'button', `${s.key}: the mode button is a button with aria-pressed false`);
    }
    clean(t, ctx, 'footers');
    await ctx.close();
  });
}

test('the static footer line 1 in each page’s own HTML is family.js’s words (right even before the script runs)', async t => {
  const sources = { home: fs.readFileSync(path.join(ROOT, 'site', 'home.js'), 'utf8'), '404': fs.readFileSync(path.join(ROOT, 'site', '404.html'), 'utf8') };
  for (const s of APPS) sources[s.key] = fs.readFileSync(path.join(ROOT, s.key, 'site', 'index.html'), 'utf8');
  for (const [k, src] of Object.entries(sources)) {
    const m = /data-jj-line1>([^<]*)</.exec(src);
    t.ok(m, `${k}: has a data-jj-line1 paragraph`);
    if (m && m[1]) t.ok(m[1] === LINE1, `${k}: its written line 1 matches (got “${m[1]}”)`);
  }
});

test('footer credits: a “·” never starts or ends a line at laptop widths; on a phone one credit per line and no dots', async t => {
  const ctx = await context();
  const page = await ctx.newPage();
  for (const s of SITES) {
    await open(ctx, FAM, s.path, { page });
    for (const width of [1600, 1440, 1280, 1100, 1000, 950, 901, 800, 701]) {
      await page.setViewportSize({ width, height: 900 }); await page.waitForTimeout(250);
      const bad = await page.evaluate(() => [...document.querySelectorAll('[data-jj-credits] .dot, [data-jj-credits] .jj-dot')]
        .filter(d => getComputedStyle(d).display !== 'none' && getComputedStyle(d).visibility !== 'hidden')
        .filter(d => { const t = d.getBoundingClientRect(), a = d.previousElementSibling.getBoundingClientRect(), b = d.nextElementSibling.getBoundingClientRect(); return Math.abs(a.bottom - t.bottom) > 3 || Math.abs(b.bottom - t.bottom) > 3; })
        .map(d => d.nextElementSibling.textContent));
      t.ok(!bad.length, `${s.key} at ${width}px: no “·” at a line end (before ${bad.join(', ')})`);
    }
    await page.setViewportSize({ width: 390, height: 844 }); await page.waitForTimeout(250);
    const phone = await page.evaluate(() => { const cr = [...document.querySelectorAll('[data-jj-credits] .cr')];
      return { lines: new Set(cr.map(c => Math.round(c.getBoundingClientRect().top))).size, n: cr.length,
        dots: [...document.querySelectorAll('[data-jj-credits] .dot, [data-jj-credits] .jj-dot')].filter(d => d.getClientRects().length && getComputedStyle(d).visibility !== 'hidden' && getComputedStyle(d).display !== 'none').length }; });
    t.ok(phone.lines === phone.n, `${s.key} at 390px: one credit per line (${phone.n} credits on ${phone.lines} lines)`);
    t.ok(phone.dots === 0, `${s.key} at 390px: no dots shown (${phone.dots})`);
    await page.setViewportSize({ width: 1600, height: 1000 });
  }
  await ctx.close();
});

test('Back to top scrolls to the top and moves keyboard focus there, on every site', async t => {
  const ctx = await context({ viewport: { width: 1280, height: 800 } });
  const page = await ctx.newPage();
  for (const s of SITES) {
    await open(ctx, FAM, s.path, { page });
    await page.locator('[data-jj-top]').scrollIntoViewIfNeeded();
    const scrolled = await page.evaluate(() => scrollY);
    await page.click('[data-jj-top]');
    const r = await page.evaluate(() => {
      const a = document.querySelector('[data-jj-top]'), sel = a.getAttribute('data-jj-top') || a.getAttribute('href') || '#top';
      const target = (sel.charAt(0) === '#' && sel.length > 1 && document.querySelector(sel)) || document.getElementById('top');
      return { y: scrollY, focused: !!target && document.activeElement === target, target: target && (target.id || target.tagName) };
    });
    t.ok(scrolled > 0 || (await page.evaluate(() => document.documentElement.scrollHeight <= innerHeight)), `${s.key}: the footer was scrolled to`);
    t.ok(r.y < 5, `${s.key}: back at the top (scrollY ${r.y})`);
    t.ok(r.focused, `${s.key}: focus moved to the top (${r.target})`);
  }
  await ctx.close();
});

test('dark mode on every site: the button switches, says Light mode, saves jj-mode and the family server’s choice, follows the bar colour and tab icon; reload keeps it', async t => {
  resetMode();
  const ctx = await context({ viewport: { width: 1280, height: 800 } });
  const page = await ctx.newPage();
  for (const s of SITES) {
    await open(ctx, FAM, s.path, { page });
    const before = await page.evaluate(() => ({ server: document.documentElement.getAttribute('data-jj-server-mode'), theme: document.querySelector('meta[name="theme-color"]').getAttribute('content') }));
    t.ok(before.server === 'light', `${s.key}: the family server wrote its choice into the page (data-jj-server-mode=${before.server})`);
    await page.click('[data-jj-mode]');
    const r = await page.evaluate(() => {
      const b = document.querySelector('[data-jj-mode]'), tc = document.querySelector('meta[name="theme-color"]');
      return { mode: document.documentElement.getAttribute('data-mode'), key: localStorage.getItem('jj-mode'), text: b.textContent.trim(), pressed: b.getAttribute('aria-pressed'),
        theme: tc.getAttribute('content'), dark: tc.getAttribute('data-dark'),
        icons: [...document.querySelectorAll('link[rel~="icon"][data-dark]')].every(l => l.getAttribute('href') === l.getAttribute('data-dark')) };
    });
    t.ok(r.mode === 'dark' && r.key === 'dark', `${s.key}: dark, saved as jj-mode (${r.mode}, ${r.key})`);
    t.ok(r.text === 'Light mode' && r.pressed === 'true', `${s.key}: the button says Light mode, aria-pressed true (${r.text}, ${r.pressed})`);
    t.ok(r.dark && r.theme === r.dark && r.theme !== before.theme, `${s.key}: the bar colour follows (${before.theme} → ${r.theme})`);
    t.ok(r.icons, `${s.key}: tab icons with a dark version switch to it`);
    for (let i = 0; i < 20 && readMode() !== 'dark'; i++) await page.waitForTimeout(50);
    t.ok(readMode() === 'dark', `${s.key}: the family server kept the choice (file says ${readMode()})`);
    await page.reload({ waitUntil: 'networkidle' });
    t.ok(await mode(page) === 'dark', `${s.key}: still dark after reloading`);
    await page.click('[data-jj-mode]');
    t.ok(await mode(page) === 'light', `${s.key}: and back to light`);
    for (let i = 0; i < 20 && readMode() !== 'light'; i++) await page.waitForTimeout(50);
    t.ok(readMode() === 'light', `${s.key}: the family server kept light (file says ${readMode()})`);
  }
  clean(t, ctx, 'dark mode');
  await ctx.close();
});

test('dark mode carries across the sites on her PC, even between app windows with their own Chrome profiles (the family server’s choice)', async t => {
  resetMode();
  const a = await context(), b = await context();
  const home = await open(a, FAM, '/');
  await home.click('[data-jj-mode]');
  for (let i = 0; i < 20 && readMode() !== 'dark'; i++) await home.waitForTimeout(50);
  for (const s of APPS) {
    const page = await open(b, FAM, s.path);   // another profile: its own (empty) storage
    t.ok(await mode(page) === 'dark', `${s.key}: opens dark after Dark mode on home in another window (got ${await mode(page)})`);
    await page.close();
  }
  const lib = await open(b, FAM, '/library/');
  await lib.click('[data-jj-mode]');
  for (let i = 0; i < 20 && readMode() !== 'light'; i++) await lib.waitForTimeout(50);
  await home.reload({ waitUntil: 'networkidle' });
  t.ok(await mode(home) === 'light', 'home: back to light after Light mode in the Library’s window');
  resetMode();
  await a.close(); await b.close();
});

test('a mode change in one tab is followed straight away by the other open sites (storage event)', async t => {
  resetMode();
  const ctx = await context();
  const pages = [];
  for (const s of SITES) pages.push([s, await open(ctx, FAM, s.path)]);
  await pages[0][1].click('[data-jj-mode]');
  for (const [s, page] of pages.slice(1)) {
    await page.waitForFunction(() => document.documentElement.getAttribute('data-mode') === 'dark', null, { timeout: 3000 }).catch(() => {});
    const r = await page.evaluate(() => [document.documentElement.getAttribute('data-mode'), document.querySelector('[data-jj-mode]').textContent.trim()]);
    t.ok(r[0] === 'dark' && r[1] === 'Light mode', `${s.key}: followed home to dark without reloading (${r})`);
  }
  await pages[2][1].click('[data-jj-mode]');
  await pages[0][1].waitForFunction(() => document.documentElement.getAttribute('data-mode') === 'light', null, { timeout: 3000 }).catch(() => {});
  t.ok(await mode(pages[0][1]) === 'light', 'home: followed Sim World back to light');
  resetMode();
  await ctx.close();
});

test('the Menu drawer on the four apps: bar at 899px, sidebar at 901px; opens on the page’s link, Tab stays inside, Escape/scrim/link close it, focus back, reset over 900px; family sizes', async t => {
  const ctx = await context({ viewport: { width: 901, height: 800 } });
  for (const s of APPS) {
    const page = await open(ctx, FAM, s.path);
    const state = () => page.evaluate(() => {
      const btn = document.getElementById('menuBtn'), drawer = document.getElementById(btn.getAttribute('aria-controls'));
      return { bar: !!btn.getClientRects().length && getComputedStyle(btn).visibility !== 'hidden', inert: !!drawer.inert, open: document.documentElement.classList.contains('jj-menu-open'),
        expanded: btn.getAttribute('aria-expanded'), inside: drawer.contains(document.activeElement), onButton: document.activeElement === btn,
        focusHome: document.activeElement && document.activeElement.classList.contains('home-link') };
    });
    let st = await state();
    t.ok(!st.bar && !st.inert, `${s.key} at 901px: no Menu bar, the sidebar is reachable (${JSON.stringify(st)})`);
    await page.setViewportSize({ width: 899, height: 800 }); await page.waitForTimeout(200);
    st = await state();
    t.ok(st.bar && st.inert && st.expanded === 'false', `${s.key} at 899px: the Menu bar shows, the closed drawer is inert (${JSON.stringify(st)})`);
    const sizes = await page.evaluate(() => {
      const btn = document.getElementById('menuBtn'), drawer = document.getElementById(btn.getAttribute('aria-controls'));
      const name = btn.parentElement.querySelector('a'), first = drawer.querySelector('a[href]');
      return { btn: btn.getBoundingClientRect().height, word: btn.textContent.trim(), icon: !!btn.querySelector('svg'), name: name && getComputedStyle(name).fontSize,
        nameText: name && name.textContent.trim(), italic: name && name.querySelector('em') && getComputedStyle(name.querySelector('em')).fontStyle,
        first: first && first.textContent.trim(), firstHref: first && first.getAttribute('href'), firstTall: first && first.getBoundingClientRect().height };
    });
    t.ok(sizes.btn >= 44 && sizes.word === 'Menu' && sizes.icon, `${s.key}: the Menu button says Menu with an icon, 44px or more (${sizes.word}, ${sizes.btn})`);
    t.ok(sizes.name === '26px' && sizes.nameText === s.name && sizes.italic === 'italic', `${s.key}: the bar name “${s.name}” is 26px with an italic second word (${sizes.nameText}, ${sizes.name}, ${sizes.italic})`);
    t.ok(sizes.first === '← Jemma’s Journals' && sizes.firstHref === '/', `${s.key}: “← Jemma’s Journals” (href /) is first in the drawer (${sizes.first}, ${sizes.firstHref})`);
    await page.click('#menuBtn'); await page.waitForTimeout(100);
    st = await state();
    t.ok(st.open && st.expanded === 'true' && st.inside && !st.focusHome, `${s.key}: Menu opens it, focus inside on the page’s link, not ← Jemma’s Journals (${JSON.stringify(st)})`);
    const looks = await page.evaluate(() => ({ scrim: getComputedStyle(document.getElementById('scrim')).backgroundColor, locked: [document.documentElement, document.body].some(e => getComputedStyle(e).overflow === 'hidden'), main: !!(document.querySelector('main') && document.querySelector('main').closest('[inert]')) }));
    t.ok(looks.scrim === 'rgba(0, 0, 0, 0.45)', `${s.key}: the scrim is black at 45% (${looks.scrim})`);
    t.ok(looks.main, `${s.key}: the page behind is inert while open`);
    t.ok(looks.locked, `${s.key}: the page behind doesn't scroll while open`);
    let escaped = 0;
    for (const key of ['Tab', 'Shift+Tab']) for (let i = 0; i < 20; i++) { await page.keyboard.press(key); if (!(await state()).inside) escaped++; }
    t.ok(escaped === 0, `${s.key}: Tab and Shift+Tab stay inside the open drawer (${escaped} escapes)`);
    await page.keyboard.press('Escape'); st = await state();
    t.ok(!st.open && st.onButton && st.inert, `${s.key}: Escape closes it, focus back on Menu`);
    await page.click('#menuBtn'); await page.mouse.click(885, 400); await page.waitForTimeout(100); st = await state();
    t.ok(!st.open && st.onButton, `${s.key}: tapping the scrim closes it, focus back on Menu`);
    await page.click('#menuBtn');
    const link = await page.evaluateHandle(() => { const d = document.getElementById(document.getElementById('menuBtn').getAttribute('aria-controls'));
      return [...d.querySelectorAll('a[href^="#"]')].filter(a => a.getClientRects().length && !a.closest('[hidden]'))[1]; });
    if (link.asElement()) { await link.asElement().click(); await page.waitForTimeout(150); st = await state(); t.ok(!st.open, `${s.key}: choosing a link closes it`); }
    else t.ok(false, `${s.key}: found a link in the drawer to choose`);
    await page.click('#menuBtn');
    await page.setViewportSize({ width: 1280, height: 800 }); await page.waitForTimeout(250); st = await state();
    t.ok(!st.open && !st.inert && st.expanded === 'false', `${s.key}: widening past 900px resets it (${JSON.stringify(st)})`);
    await page.setViewportSize({ width: 901, height: 800 });
    const v = await csp(page);
    t.ok(!v.length, `${s.key}: no CSP violations using the drawer`);
    await page.close();
  }
  clean(t, ctx, 'drawer');
  await ctx.close();
});

test('fonts are the sites’ own copies (every @font-face on the same address, all loaded); no styles follow the device’s dark setting', async t => {
  const ctx = await context();
  const page = await ctx.newPage();
  for (const s of SITES) {
    await open(ctx, FAM, s.path, { page });
    const r = await page.evaluate(() => {
      const faces = [];
      for (const sheet of document.styleSheets) { let rules; try { rules = sheet.cssRules; } catch (e) { faces.push('unreadable sheet ' + sheet.href); continue; }
        for (const rule of rules) if (rule instanceof CSSFontFaceRule) (rule.style.getPropertyValue('src').match(/url\(([^)]+)\)/g) || []).forEach(u => faces.push(new URL(u.slice(4, -1).replace(/["']/g, ''), sheet.href || location.href).href)); }
      const media = [];   // dark styles hang off data-mode, never the device setting (family rules, section 1)
      const walk = (rules, href) => { for (const r of rules) { if (r.media && /prefers-color-scheme/.test(r.media.mediaText)) media.push((href || 'inline').split('/').pop() + ' ' + r.media.mediaText); if (r.cssRules) walk(r.cssRules, href); } };
      for (const sheet of document.styleSheets) { try { walk(sheet.cssRules, sheet.href); } catch (e) {} }
      return { outside: faces.filter(u => !u.startsWith(location.origin)), n: faces.length, failed: [...document.fonts].filter(f => f.status === 'error').map(f => f.family), media };
    });
    t.ok(r.n > 0 && !r.outside.length, `${s.key}: ${r.n} font files, all local (${r.outside.slice(0, 2).join(', ')})`);
    t.ok(!r.failed.length, `${s.key}: no font failed to load (${r.failed.join(', ')})`);
    t.ok(!r.media.length, `${s.key}: no styles follow the device’s dark setting (${r.media.slice(0, 3).join(', ')})`);
  }
  await ctx.close();
});

test('links between the sites on her PC: home’s four Open links go to each app; every app’s “← Jemma’s Journals” comes home', async t => linksCheck(t, () => FAM));

async function linksCheck(t, base) {
  const ctx = await context();
  const page = await open(ctx, base(), '/');
  const hrefs = await page.evaluate(() => [...document.querySelectorAll('.card a.go')].map(a => a.getAttribute('href')));
  t.ok(JSON.stringify(hrefs) === JSON.stringify(['/sim-world/', '/library/', '/pokedex/', '/travels/']), `home: the Open links point at the four apps (${hrefs})`);
  for (const [i, h] of hrefs.entries()) {
    await open(ctx, base(), '/', { page });
    await Promise.all([page.waitForURL(u => new URL(u).pathname === h, { timeout: 5000 }).catch(() => {}), page.locator('.card a.go').nth(i).click()]);
    t.ok(new URL(page.url()).pathname === h, `home: clicking “Open …” number ${i + 1} opens ${h} (stayed at ${new URL(page.url()).pathname})`);
    await page.waitForLoadState('networkidle');
    if (new URL(page.url()).pathname === h) {
      const back = page.locator('a.home-link').first();
      await Promise.all([page.waitForURL(u => new URL(u).pathname === '/', { timeout: 5000 }).catch(() => {}), back.click()]);
      await page.waitForLoadState('networkidle');
      const title = await page.evaluate(() => (document.querySelector('h1') || {}).textContent);
      t.ok(new URL(page.url()).pathname === '/' && title === 'Jemma’s Journals', `${h}: “← Jemma’s Journals” comes home (at ${page.url()}, h1 ${title})`);
    }
  }
  // the apps’ own home links straight from each app (in case an Open link above failed)
  for (const s of APPS) {
    await open(ctx, base(), s.path, { page });
    const href = await page.evaluate(() => { const a = document.querySelector('a.home-link'); return a && [a.getAttribute('href'), a.href, a.getBoundingClientRect().height]; });
    t.ok(href && href[0] === '/' && href[1] === new URL(base()).origin + '/', `${s.key}: “← Jemma’s Journals” goes to / (${href})`);
    t.ok(href && href[2] >= 24, `${s.key}: “← Jemma’s Journals” is at least 24px tall (${href && href[2]})`);
  }
  clean(t, ctx, 'links');
  await ctx.close();
}

test('the 404 page: missing addresses get it with status 404, the family footer and a working mode button', async t => {
  const ctx = await context(); ctx.allow404 = true;
  const page = await ctx.newPage(); ctx.origin = new URL(FAM).origin;
  for (const p of ['/no-such-page', '/pokedex/no-such-page.html']) {
    const res = await page.goto(FAM + p, { waitUntil: 'networkidle' });
    const r = await page.evaluate(() => ({ foot: (document.querySelector('footer') || {}).innerText || '', line1: (document.querySelector('[data-jj-line1]') || {}).textContent,
      btn: (document.querySelector('[data-jj-mode]') || {}).textContent }));
    t.ok(res.status() === 404, `${p}: status 404 (got ${res.status()})`);
    t.ok(r.line1 === LINE1 && /Back to top/.test(r.foot) && /Dark mode/.test(r.btn || ''), `${p}: the family footer`);
  }
  await page.click('[data-jj-mode]');
  t.ok(await mode(page) === 'dark', '404: the mode button switches');
  resetMode();
  await ctx.close();
});

// ---------- online: the online-style build, on a plain web host ----------
test('online-style copy: every site loads with no errors (except the save requests’ 404s), nothing from elsewhere, no CSP violation, every picture shown loads', async t => {
  for (const width of [1600, 390]) {
    const ctx = await context({ viewport: { width, height: 900 } });
    for (const s of SITES) {
      let page;
      try { page = await open(ctx, WEB, s.path); } catch (e) {   // one broken site: say so (with what failed to load) and go on to the next
        t.ok(false, `${e.message.split('\n')[0]} (${[...ctx.log.bad, ...ctx.log.errors].slice(0, 3).join(' / ')})`);
        ctx.log.errors = []; ctx.log.bad = []; ctx.log.outside = [];
        continue;
      }
      const r = await page.evaluate(() => ({ server: document.documentElement.hasAttribute('data-jj-server-mode'),
        broken: [...document.images].filter(i => i.complete && i.getAttribute('src') && i.naturalWidth === 0).map(i => i.getAttribute('src')).slice(0, 3) }));
      t.ok(!r.server, `${s.key}: no family-server help online (no data-jj-server-mode)`);
      t.ok(!r.broken.length, `${s.key} at ${width}px: no broken pictures (${r.broken})`);
      t.ok(await mode(page) === 'light', `${s.key}: opens light`);
      t.ok(await sideways(page) <= 0, `${s.key} at ${width}px: no sideways scroll`);
      const v = await csp(page);
      t.ok(!v.length, `${s.key}: no CSP violations (${v.slice(0, 2)})`);
      clean(t, ctx, `online ${s.key} ${width}px`);
      await page.close();
    }
    await ctx.close();
  }
});

test('online-style copy: the apps are view-only (Library: no Add a book; Pokédex: view-only; Travels: Write says it needs her server)', async t => {
  const ctx = await context();
  let page = await open(ctx, WEB, '/library/');
  await page.waitForTimeout(500);
  const lib = await page.evaluate(() => ({ add: !!document.querySelector('a[href="#add"]'), controls: document.querySelectorAll('select.cond-pick, .inscr-pick, .sign-pick').length }));
  t.ok(!lib.add, 'library: no “Add a book” link');
  page = await open(ctx, WEB, '/pokedex/', { page });
  await page.waitForFunction(() => document.documentElement.classList.contains('view-only'), null, { timeout: 5000 }).catch(() => {});
  t.ok(await page.evaluate(() => document.documentElement.classList.contains('view-only')), 'pokedex: view-only');
  page = await open(ctx, WEB, '/travels/#/write', { page });
  await page.waitForFunction(() => { const w = document.getElementById('wServer'); return w && w.textContent.trim(); }, null, { timeout: 5000 }).catch(() => {});
  const tr = await page.evaluate(() => ({ save: (document.getElementById('saveBtn') || {}).disabled, note: (document.getElementById('wServer') || {}).textContent || '' }));
  t.ok(tr.save === true && /To save, open the site from its own server/.test(tr.note), `travels: Save off, and the Write page says so (“${tr.note.trim().slice(0, 80)}”)`);
  clean(t, ctx, 'online view-only');
  await ctx.close();
});

test('online-style copy: dark mode carries from one site to the next by jj-mode alone, and other tabs follow', async t => {
  const ctx = await context();
  const home = await open(ctx, WEB, '/');
  const other = await open(ctx, WEB, '/travels/');
  await home.click('[data-jj-mode]');
  await other.waitForFunction(() => document.documentElement.getAttribute('data-mode') === 'dark', null, { timeout: 3000 }).catch(() => {});
  t.ok(await mode(other) === 'dark', 'travels (open in another tab): followed home to dark');
  const page = await ctx.newPage();
  for (const s of APPS) {
    await open(ctx, WEB, s.path, { page });
    t.ok(await mode(page) === 'dark', `${s.key}: opens dark after Dark mode on home`);
  }
  await page.click('[data-jj-mode]');
  await home.reload({ waitUntil: 'networkidle' });
  t.ok(await mode(home) === 'light', 'home: light again after Light mode on the last app');
  clean(t, ctx, 'online dark mode');
  await ctx.close();
});

test('online-style copy: links between the sites work (home’s Open links, every “← Jemma’s Journals”)', async t => linksCheck(t, () => WEB));

test('online-style copy: missing addresses get the 404 page with status 404', async t => {
  const ctx = await context(); ctx.allow404 = true;
  const page = await ctx.newPage();
  const res = await page.goto(WEB + '/no-such-page', { waitUntil: 'networkidle' });
  t.ok(res.status() === 404 && /Page not found/.test(await page.title()), `404 with the not-found page (got ${res.status()}, ${await page.title()})`);
  await ctx.close();
});

// ---------- mode.js on its own: which setting wins ----------
test('mode.js: light by default; jj-mode next; the family server’s choice wins and is copied to jj-mode; an old key is used once then removed; junk and blocked storage mean light', async t => {
  const html = (server, old) => `<!doctype html><html${server ? ` data-jj-server-mode="${server}"` : ''}><head><script src="/family/mode.js"${old ? ' data-old-key="old-mode"' : ''}></script></head><body></body></html>`;
  const cases = [   // [name, server attribute, storage before, old key?, expected mode, expected jj-mode after, old-mode after]
    ['nothing saved', null, {}, true, 'light', null, null],
    ['jj-mode dark', null, { 'jj-mode': 'dark' }, false, 'dark', 'dark', null],
    ['jj-mode light', null, { 'jj-mode': 'light' }, false, 'light', 'light', null],
    ['junk in jj-mode', null, { 'jj-mode': 'purple' }, false, 'light', 'purple', null],
    ['the server says dark over jj-mode light', 'dark', { 'jj-mode': 'light' }, false, 'dark', 'dark', null],
    ['the server says light over jj-mode dark', 'light', { 'jj-mode': 'dark' }, false, 'light', 'light', null],
    ['a junk server value is ignored', 'blue', { 'jj-mode': 'dark' }, false, 'dark', 'dark', null],
    ['an old key, once', null, { 'old-mode': 'dark' }, true, 'dark', 'dark', null],
    ['jj-mode beats an old key, which is still removed', null, { 'jj-mode': 'light', 'old-mode': 'dark' }, true, 'light', 'light', null],
    ['a junk old key is ignored and removed', null, { 'old-mode': 'x' }, true, 'light', null, null],
    ['an old key is left alone by a page that doesn’t name it', null, { 'old-mode': 'dark' }, false, 'light', null, 'dark'],
  ];
  const ctx = await context();
  await ctx.route(WEB + '/__mode/**', route => { const u = new URL(route.request().url()); route.fulfill({ contentType: 'text/html', body: u.pathname.endsWith('blank') ? '<!doctype html><p>blank' : html(u.searchParams.get('s'), u.searchParams.get('o') === '1') }); });
  ctx.origin = new URL(WEB).origin;
  const page = await ctx.newPage();
  for (const [name, server, store, old, want, keyAfter, oldAfter] of cases) {
    await page.goto(WEB + '/__mode/blank');
    await page.evaluate(s => { localStorage.clear(); Object.entries(s).forEach(([k, v]) => localStorage.setItem(k, v)); }, store);
    await page.goto(WEB + `/__mode/page?o=${old ? 1 : 0}` + (server ? '&s=' + server : ''));
    const r = await page.evaluate(() => [document.documentElement.getAttribute('data-mode'), localStorage.getItem('jj-mode'), localStorage.getItem('old-mode')]);
    t.ok(JSON.stringify(r) === JSON.stringify([want, keyAfter, oldAfter]), `${name}: expected ${JSON.stringify([want, keyAfter, oldAfter])}, got ${JSON.stringify(r)}`);
  }
  await ctx.close();
  const blocked = await context();
  await blocked.addInitScript(() => Object.defineProperty(window, 'localStorage', { get() { throw new Error('blocked'); } }));
  await blocked.route(WEB + '/__mode/**', route => route.fulfill({ contentType: 'text/html', body: html('dark', true) }));
  const bp = await blocked.newPage();
  await bp.goto(WEB + '/__mode/page');
  t.ok(await mode(bp) === 'light', `storage blocked: light (got ${await mode(bp)})`);
  await blocked.close();
});

// ---------- run ----------
(async () => {
  const started = Date.now();
  const tmp = fs.mkdtempSync(path.join(os.tmpdir(), 'jj-family-'));
  MODE_FILE = path.join(tmp, 'family-mode.txt'); resetMode();
  const buildDir = arg('--build-dir') || process.env.JJ_BUILD_DIR || path.join(tmp, 'build');
  const [p1, p2] = [await freePort(), await freePort()];
  let failed = 0, passed = 0;
  try {
    await Promise.all([
      startServer('serve_family.py', ['--port', p1, '--mode-file', MODE_FILE], 20000),
      startServer('serve_build.py', ['--port', p2, '--out', buildDir, '--reuse'], 600000),
    ]);
    FAM = `http://localhost:${p1}`; WEB = `http://localhost:${p2}`;
    browser = await chromium.launch({ channel: 'msedge' });
    for (const tc of TESTS) {
      if (ONLY && !tc.name.toLowerCase().includes(ONLY.toLowerCase())) continue;
      const fails = [], t = { ok: (c, m) => { if (!c) fails.push(m); } }, t0 = Date.now();
      resetMode();   // every test starts light, even after one that stopped half way
      try { await tc.fn(t); } catch (e) { fails.push('crashed: ' + (e.stack || e.message).split('\n').slice(0, 3).join(' | ')); }
      const secs = ((Date.now() - t0) / 1000).toFixed(0);
      if (fails.length) { failed++; console.log(`FAIL ${tc.name} (${secs}s)`); fails.slice(0, 12).forEach(f => console.log('       ' + f)); if (fails.length > 12) console.log(`       … and ${fails.length - 12} more`); }
      else { passed++; console.log(`ok   ${tc.name} (${secs}s)`); }
    }
  } catch (e) {
    failed++; console.log('FAIL could not start: ' + e.message);
  } finally {
    if (browser) await browser.close();
    stopAll();
    await new Promise(r => setTimeout(r, 300));
    try { fs.rmSync(tmp, { recursive: true, force: true }); } catch (e) {}
  }
  console.log(`family suite: ${passed} passed, ${failed} failed in ${((Date.now() - started) / 1000).toFixed(0)}s`);
  process.exit(failed ? 1 : 0);
})();
