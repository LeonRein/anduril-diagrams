// Geometric layout checker for the generated SVGs.
//
// usage: node tools/check.js [--allow tools/layout-allowlist.txt] file.svg ...
//
// Reports overlapping text, labels that are off / under foreign arrows,
// arrows through cards or text, arrow crossings, near-parallel arrows and
// text overflowing its card. Exits with code 1 if a finding is not listed in
// the allowlist (one "kind | description" per line, '#' starts a comment).
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

async function checkFile(b, svgPath) {
  const svg = fs.readFileSync(svgPath, 'utf8');
  const m = svg.match(/width="(\d+)" height="(\d+)"/);
  const W = +m[1], H = +m[2];
  const p = await b.newPage({ viewport: { width: W, height: H } });
  await p.setContent(`<html><body style="margin:0">${svg}</body></html>`);
  await p.waitForTimeout(300);
  const res = await p.evaluate(() => {
    const R = (el) => { const r = el.getBoundingClientRect(); return { x: r.left, y: r.top, w: r.width, h: r.height }; };
    const ov = (a, b, pad = 0) => !(a.x + a.w <= b.x - pad || b.x + b.w <= a.x - pad || a.y + a.h <= b.y - pad || b.y + b.h <= a.y - pad);
    const inside = (pt, r, shrink = 0) => pt.x > r.x + shrink && pt.x < r.x + r.w - shrink && pt.y > r.y + shrink && pt.y < r.y + r.h - shrink;
    const area = (a, b) => Math.max(0, Math.min(a.x + a.w, b.x + b.w) - Math.max(a.x, b.x)) * Math.max(0, Math.min(a.y + a.h, b.y + b.h) - Math.max(a.y, b.y));

    const cards = [...document.querySelectorAll('.card')].map((el) => ({ el, r: R(el), node: el.classList.contains('node'), tag: el.tagName }));
    const groups = [...document.querySelectorAll('.grp')].map((el) => R(el));
    const icons = [...document.querySelectorAll('g.icon')].map((el) => R(el));
    const pills = [...document.querySelectorAll('g.pillg')].map((el) => ({ id: el.dataset.id, label: el.dataset.label, r: R(el.querySelector('rect')), full: R(el) }));
    const texts = [...document.querySelectorAll('text')]
      .filter((t) => !t.closest('g.pillg') && !t.closest('g.icon') && t.textContent.trim())
      .map((t) => ({ s: t.textContent.trim().slice(0, 48), r: R(t), x: +t.getAttribute('x'), y: +t.getAttribute('y'), rot: t.hasAttribute('transform') }));
    const arrows = [...document.querySelectorAll('path.arr')].map((el) => {
      const L = el.getTotalLength(); const pts = [];
      for (let s = 0; s <= L; s += 2) { const q = el.getPointAtLength(s); pts.push({ x: q.x, y: q.y, s }); }
      const label = (pills.find((pp) => pp.id === el.dataset.id) || {}).label || '';
      return { id: el.dataset.id, L, pts, label, start: pts[0], end: pts[pts.length - 1] };
    });
    const nm = (a) => `${a.label || '(unlabelled)'}[${a.start.x.toFixed(0)},${a.start.y.toFixed(0)}→${a.end.x.toFixed(0)},${a.end.y.toFixed(0)}]`;
    const out = [];

    // 1. text overlapping text
    for (let i = 0; i < texts.length; i++) for (let j = i + 1; j < texts.length; j++) {
      const a = texts[i], c = texts[j];
      if (area(a.r, c.r) > 6) out.push(['text×text', `"${a.s}" / "${c.s}"`, a.r]);
    }
    // 2. text overflowing its card (card = smallest card containing the anchor point)
    for (const t of texts) {
      if (t.rot) continue;
      const host = cards.filter((c) => !c.node && c.tag === 'rect' && inside({ x: t.r.x + 2, y: t.r.y + t.r.h / 2 }, c.r))
        .sort((a, b) => a.r.w * a.r.h - b.r.w * b.r.h)[0];
      if (!host) continue;
      const pad = 6;
      const ox = Math.max(host.r.x + pad - t.r.x, t.r.x + t.r.w - (host.r.x + host.r.w - pad));
      const oy = Math.max(host.r.y + pad - t.r.y, t.r.y + t.r.h - (host.r.y + host.r.h - 3));
      if (ox > 0.5 || oy > 0.5) out.push(['text-overflow/tight', `"${t.s}" ${ox > 0.5 ? 'x+' + ox.toFixed(1) : ''} ${oy > 0.5 ? 'y+' + oy.toFixed(1) : ''}`, t.r]);
    }
    // 3. pills vs pills / text / cards / icons
    for (let i = 0; i < pills.length; i++) {
      const a = pills[i];
      for (let j = i + 1; j < pills.length; j++) if (ov(a.full, pills[j].full, 3)) out.push(['pill×pill', `${a.label} / ${pills[j].label}`, a.r]);
      for (const t of texts) if (area(a.full, t.r) > 4) out.push(['pill×text', `${a.label} / "${t.s}"`, a.r]);
      for (const c of cards) if (c.tag !== 'polygon' && area(a.r, c.r) > 4) out.push(['pill×shape', `${a.label} over ${c.tag} @${c.r.x.toFixed(0)},${c.r.y.toFixed(0)}`, a.r]);
      for (const ic of icons) if (area(a.full, ic) > 4) out.push(['pill×icon', a.label, a.r]);
    }
    // 4. pill not on its own arrow / other arrows running under a pill
    for (const pl of pills) {
      const c = { x: pl.r.x + pl.r.w / 2, y: pl.r.y + pl.r.h / 2 };
      const own = arrows.find((a) => a.id === pl.id);
      if (own) {
        const d = Math.min(...own.pts.map((q) => Math.hypot(q.x - c.x, q.y - c.y)));
        if (d > 3) out.push(['pill-off-arrow', `${pl.label} is ${d.toFixed(1)}px from its arrow`, pl.r]);
      }
      for (const a of arrows) if (a.id !== pl.id && a.pts.some((q) => inside(q, pl.r, -2))) out.push(['other-arrow-under-pill', `${pl.label} covers ${nm(a)}`, pl.r]);
    }
    // 4b. arrows through the small sub-captions that belong to pills
    const subs = [...document.querySelectorAll('g.pillg text')].filter((t) => t.getAttribute('font-weight') === '500')
      .map((t) => ({ s: t.textContent, r: R(t), id: t.closest('g.pillg').dataset.id }));
    for (const a of arrows) for (const t of subs) {
      const pl = pills.find((pp) => pp.id === t.id);
      if (a.id === t.id && pl && inside({ x: t.r.x + t.r.w / 2, y: t.r.y + t.r.h / 2 }, pl.r)) continue;
      if (a.pts.filter((q) => inside(q, t.r, 0)).length > 1) out.push(['arrow-through-subcaption', `${nm(a)} through "${t.s}"`, t.r]);
    }
    for (const t of subs) for (const u of texts) if (area(t.r, u.r) > 4) out.push(['subcaption×text', `"${t.s}" / "${u.s}"`, t.r]);
    // 5. arrows through cards / text / icons (ignore 8px at both ends)
    for (const a of arrows) {
      const mid = a.pts.filter((q) => q.s > 8 && q.s < a.L - 8);
      for (const c of cards) {
        let hit;
        if (c.node || c.tag !== 'rect') { // ellipse/circle/polygon → test against inset bbox
          hit = mid.filter((q) => inside(q, c.r, Math.min(c.r.w, c.r.h) * 0.2));
        } else hit = mid.filter((q) => inside(q, c.r, 1));
        if (hit.length > 2) out.push(['arrow-through-shape', `${nm(a)} through ${c.tag} @${c.r.x.toFixed(0)},${c.r.y.toFixed(0)} (${hit.length} pts)`, { x: hit[0].x, y: hit[0].y, w: 1, h: 1 }]);
      }
      for (const t of texts) { const hit = mid.filter((q) => inside(q, t.r, 1)); if (hit.length > 1) out.push(['arrow-through-text', `${nm(a)} through "${t.s}"`, t.r]); }
      for (const ic of icons) { const hit = mid.filter((q) => inside(q, ic, 1)); if (hit.length > 1) out.push(['arrow-through-icon', nm(a), ic]); }
      // endpoints: should end on/near a shape edge (within 6px of some card / group / pill)
      for (const [which, q] of [['end', a.end]]) {
        const nearShape = cards.concat(groups.map((r) => ({ r }))).some((c) => {
          const r = c.r; const dx = Math.max(r.x - q.x, 0, q.x - (r.x + r.w)); const dy = Math.max(r.y - q.y, 0, q.y - (r.y + r.h));
          return Math.hypot(dx, dy) < 7;
        });
        if (!nearShape) out.push(['dangling-arrow-end', `${nm(a)} ${which} not at a shape`, { x: q.x, y: q.y, w: 1, h: 1 }]);
      }
    }
    // 6. arrow × arrow crossings (outside node ellipses) and near-parallel runs
    const nodes = cards.filter((c) => c.node || c.tag === 'circle').map((c) => ({ x: c.r.x - 6, y: c.r.y - 6, w: c.r.w + 12, h: c.r.h + 12 }));
    const segx = (p1, p2, p3, p4) => {
      const d = (p2.x - p1.x) * (p4.y - p3.y) - (p2.y - p1.y) * (p4.x - p3.x); if (Math.abs(d) < 1e-9) return null;
      const t = ((p3.x - p1.x) * (p4.y - p3.y) - (p3.y - p1.y) * (p4.x - p3.x)) / d;
      const u = ((p3.x - p1.x) * (p2.y - p1.y) - (p3.y - p1.y) * (p2.x - p1.x)) / d;
      return t >= 0 && t <= 1 && u >= 0 && u <= 1 ? { x: p1.x + t * (p2.x - p1.x), y: p1.y + t * (p2.y - p1.y) } : null;
    };
    for (let i = 0; i < arrows.length; i++) for (let j = i + 1; j < arrows.length; j++) {
      const A = arrows[i], B = arrows[j]; const xs = [];
      for (let k = 0; k + 1 < A.pts.length; k += 1) for (let l = 0; l + 1 < B.pts.length; l += 1) {
        const q = segx(A.pts[k], A.pts[k + 1], B.pts[l], B.pts[l + 1]);
        if (q && !nodes.some((n) => inside(q, n)) && !xs.some((z) => Math.hypot(z.x - q.x, z.y - q.y) < 10)) xs.push(q);
      }
      for (const q of xs) out.push(['arrow×arrow', `${nm(A)} × ${nm(B)}`, { x: q.x, y: q.y, w: 1, h: 1 }]);
      // close parallel run: >= 40px of A within 5px of B (outside nodes)
      let run = 0, best = 0, at = null;
      for (const q of A.pts) {
        if (nodes.some((n) => inside(q, n))) { run = 0; continue; }
        const close = B.pts.some((r) => Math.abs(r.x - q.x) < 5 && Math.abs(r.y - q.y) < 5 && Math.hypot(r.x - q.x, r.y - q.y) < 5);
        if (close) { run += 2; if (run > best) { best = run; at = q; } } else run = 0;
      }
      if (best >= 40) out.push(['arrows-too-close', `${nm(A)} ~ ${nm(B)} for ${best}px`, { x: at.x, y: at.y, w: 1, h: 1 }]);
    }
    return out.map(([k, d, r]) => ({ k, d, at: `${r.x.toFixed(0)},${r.y.toFixed(0)}` }));
  });
  await p.close();
  return res;
}

(async () => {
  const args = process.argv.slice(2);
  let allowFile = path.join(__dirname, 'layout-allowlist.txt');
  const ai = args.indexOf('--allow');
  if (ai >= 0) { allowFile = args[ai + 1]; args.splice(ai, 2); }
  const allow = new Set(fs.existsSync(allowFile)
    ? fs.readFileSync(allowFile, 'utf8').split('\n').map((l) => l.trim()).filter((l) => l && !l.startsWith('#'))
    : []);
  const b = await chromium.launch();
  let fresh = 0;
  for (const f of args) {
    const res = await checkFile(b, f);
    console.log(`\n=== ${path.basename(f)}: ${res.length} finding(s)`);
    for (const r of res) {
      const key = `${r.k} | ${r.d}`;
      const known = allow.has(key);
      if (!known) fresh++;
      console.log(`  ${known ? 'allowed' : 'NEW    '}  @${r.at}  ${key}`);
    }
  }
  await b.close();
  if (fresh) { console.log(`\n${fresh} new layout finding(s). Fix them or add them to the allowlist.`); process.exit(1); }
  console.log('\nLayout check passed.');
})();
