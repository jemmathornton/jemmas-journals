// builds s1.css / s2.css from *.src.css, filling in generated SVG decorations (contours, compass, postmark)
const fs = require('fs');
const enc = s => `url("data:image/svg+xml,${encodeURIComponent(s).replace(/'/g, '%27')}")`;
// --- contour lines: nested wobbly rings around a few "hills"
function ring(cx, cy, r, seed, rx = 1, ry = 0.62) {
  const pts = [];
  for (let i = 0; i < 64; i++) {
    const a = i / 64 * Math.PI * 2;
    const w = 1 + 0.13 * Math.sin(3 * a + seed) + 0.08 * Math.sin(5 * a + seed * 1.7) + 0.05 * Math.cos(2 * a + seed * .4);
    pts.push([cx + Math.cos(a) * r * rx * w, cy + Math.sin(a) * r * ry * w]);
  }
  let d = `M${pts[0][0].toFixed(1)},${pts[0][1].toFixed(1)}`;
  for (let i = 0; i < pts.length; i++) {
    const p0 = pts[(i - 1 + 64) % 64], p1 = pts[i], p2 = pts[(i + 1) % 64], p3 = pts[(i + 2) % 64];
    const c1 = [p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6], c2 = [p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6];
    d += `C${c1[0].toFixed(1)},${c1[1].toFixed(1)} ${c2[0].toFixed(1)},${c2[1].toFixed(1)} ${p2[0].toFixed(1)},${p2[1].toFixed(1)}`;
  }
  return d + 'Z';
}
function contours(col) {
  let paths = '';
  const hills = [[880, 120, 9, 0.8], [1180, 420, 7, 2.1], [560, 470, 5, 3.3]];
  for (const [cx, cy, n, s] of hills) for (let k = 1; k <= n; k++) {
    const idx = k % 5 === 0;
    paths += `<path d='${ring(cx, cy, 26 * k, s + k * .35)}' fill='none' stroke='${col}' stroke-width='${idx ? 1.6 : 0.9}'/>`;
  }
  return `<svg xmlns='http://www.w3.org/2000/svg' width='1400' height='620' viewBox='0 0 1400 620'>${paths}</svg>`;
}
function compass(col) {
  let s = `<svg xmlns='http://www.w3.org/2000/svg' width='220' height='220' viewBox='-110 -110 220 220'><g fill='none' stroke='${col}'>`;
  s += `<circle r='96' stroke-width='1'/><circle r='88' stroke-width='.6'/><circle r='40' stroke-width='.6'/>`;
  for (let i = 0; i < 72; i++) { const a = i * 5 * Math.PI / 180, r1 = i % 18 === 0 ? 76 : i % 2 ? 84 : 81; s += `<line x1='${(Math.sin(a) * r1).toFixed(1)}' y1='${(-Math.cos(a) * r1).toFixed(1)}' x2='${(Math.sin(a) * 88).toFixed(1)}' y2='${(-Math.cos(a) * 88).toFixed(1)}' stroke-width='.7'/>`; }
  s += `</g>`;
  // 8-point star: long cardinal points, short diagonals; each point half filled
  const pt = (deg, len, w) => { const a = deg * Math.PI / 180, ca = Math.cos(a), sa = Math.sin(a);
    const tip = [sa * len, -ca * len], l = [Math.sin(a - Math.PI / 2) * w, -Math.cos(a - Math.PI / 2) * w], r = [Math.sin(a + Math.PI / 2) * w, -Math.cos(a + Math.PI / 2) * w];
    return `<path d='M0,0L${l[0].toFixed(1)},${l[1].toFixed(1)}L${tip[0].toFixed(1)},${tip[1].toFixed(1)}Z' fill='${col}'/><path d='M0,0L${r[0].toFixed(1)},${r[1].toFixed(1)}L${tip[0].toFixed(1)},${tip[1].toFixed(1)}Z' fill='none' stroke='${col}' stroke-width='.9'/>`; };
  for (const d of [45, 135, 225, 315]) s += pt(d, 46, 9);
  for (const d of [0, 90, 180, 270]) s += pt(d, 78, 12);
  s += `<circle r='4' fill='${col}'/></svg>`;
  return s;
}
function postmark(col) {
  let s = `<svg xmlns='http://www.w3.org/2000/svg' width='140' height='60' viewBox='0 0 140 60'><g fill='none' stroke='${col}' stroke-linecap='round'>`;
  s += `<circle cx='110' cy='30' r='25' stroke-width='2'/><circle cx='110' cy='30' r='20' stroke-width='1'/>`;
  for (const y of [21, 30, 39]) { let d = `M14,${y}`; for (let x = 14; x < 80; x += 12) d += ` q6,-4 12,0`; s += `<path d='${d}' stroke-width='1.8'/>`; }
  return s + `</g></svg>`;
}

// --- town / estate plan: streets, blocks split into plots, a few house footprints, a crescent and a cul-de-sac
function townplan(col, W, H, seed, opts = {}) {
  let s = seed; const rnd = () => (s = (s * 16807) % 2147483647) / 2147483647;
  const sw = opts.street || 20, xs = opts.xs, ys = opts.ys;
  let out = `<svg xmlns='http://www.w3.org/2000/svg' width='${W}' height='${H}' viewBox='0 0 ${W} ${H}'><g fill='none' stroke='${col}' stroke-width='1'>`;
  // street edges
  for (const y of ys) out += `<path d='M0,${y}H${W}M0,${y + sw}H${W}'/>`;
  for (const x of xs) out += `<path d='M${x},0V${H}M${x + sw},0V${H}'/>`;
  const bx = [-sw, ...xs, W], by = [-sw, ...ys, H];
  for (let i = 0; i < bx.length - 1; i++) for (let j = 0; j < by.length - 1; j++) {
    const x0 = bx[i] + sw + 6, x1 = bx[i + 1] - 6, y0 = by[j] + sw + 6, y1 = by[j + 1] - 6;
    if (x1 - x0 < 60 || y1 - y0 < 50) continue;
    const mid = (y0 + y1) / 2;
    for (const [ya, yb, front] of [[y0, mid, 'top'], [mid, y1, 'bottom']]) {
      let x = x0;
      while (x < x1 - 30) {
        const w = Math.min(x1 - x, 34 + Math.floor(rnd() * 40));
        out += `<rect x='${x.toFixed(1)}' y='${ya.toFixed(1)}' width='${w.toFixed(1)}' height='${(yb - ya).toFixed(1)}'/>`;
        if (rnd() < .55) { const hw = w * (.45 + rnd() * .2), hh = (yb - ya) * (.35 + rnd() * .15), hx = x + (w - hw) / 2, hy = front === 'top' ? ya + 7 : yb - 7 - hh;
          out += `<rect x='${hx.toFixed(1)}' y='${hy.toFixed(1)}' width='${hw.toFixed(1)}' height='${hh.toFixed(1)}' fill='${col}' fill-opacity='.35'/>`; }
        x += w;
      }
    }
  }
  if (opts.crescent) { const [cx, cy, r] = opts.crescent; out += `<circle cx='${cx}' cy='${cy}' r='${r}'/><circle cx='${cx}' cy='${cy}' r='${r - sw}'/>`;
    for (let a = 0; a < 360; a += 30) { const t = a * Math.PI / 180; out += `<path d='M${(cx + Math.cos(t) * r).toFixed(1)},${(cy + Math.sin(t) * r).toFixed(1)}L${(cx + Math.cos(t) * (r + 46)).toFixed(1)},${(cy + Math.sin(t) * (r + 46)).toFixed(1)}'/>`; } }
  return out + `</g></svg>`;
}
const vars = {
  CONTOURS: enc(contours('rgba(122,98,52,.30)')),
  CONTOURS_LIGHT: enc(contours('rgba(255,255,255,.22)')),
  COMPASS: enc(compass('#2C3A42')),
  CONTOURS_SEPIA: enc(contours('rgba(92,62,30,.34)')),
  COMPASS_SEPIA: enc(compass('#4A3420')),
  TOWN: enc(townplan('rgba(61,42,92,.26)', 1600, 820, 7, { xs: [150, 420, 700, 980, 1260], ys: [110, 330, 560], street: 18, crescent: [1130, 720, 80] })),
  TOWN_LIGHT: enc(townplan('rgba(255,255,255,.30)', 1400, 700, 11, { xs: [260, 600, 940, 1250], ys: [150, 420], street: 24 })),
  TOWN_SIDE: enc(townplan('rgba(61,42,92,.07)', 280, 420, 3, { xs: [140], ys: [130, 300], street: 14 })),
  TOWN_WARM: enc(townplan('rgba(94,76,52,.28)', 1600, 820, 7, { xs: [150, 420, 700, 980, 1260], ys: [110, 330, 560], street: 18, crescent: [1130, 720, 80] })),
  TOWN_SIDE_WARM: enc(townplan('rgba(94,76,52,.08)', 280, 420, 3, { xs: [140], ys: [130, 300], street: 14 })),
  POSTMARK: enc(postmark('rgba(255,255,255,.88)')),
  POSTMARK_DARK: enc(postmark('rgba(43,36,32,.55)')),
};
const fill = css => css.replace(/\{\{(\w+)\}\}/g, (_, k) => vars[k]);
const RES = 'C:/Users/Jemma/Documents/JemmasJournals/research/app-styles/simworld/';
const base = fs.readFileSync('s1.src.css', 'utf8');
fs.writeFileSync(RES + 's1.css', fill(base));
for (const v of ['s1a', 's1b', 's1c', 's1d', 's1e', 's1f', 's1g']) {
  const css = fill(base) + String.fromCharCode(10, 10) + fill(fs.readFileSync('v-' + v + '.css', 'utf8'));
  fs.writeFileSync(v + '.css', css); fs.writeFileSync(RES + v + '.css', css);
}
for (const f of ['s1', 's2']) {
  if (!fs.existsSync(f + '.src.css')) continue;
  let css = fs.readFileSync(f + '.src.css', 'utf8');
  css = css.replace(/\{\{(\w+)\}\}/g, (_, k) => vars[k]);
  fs.writeFileSync(f + '.css', css);
}
