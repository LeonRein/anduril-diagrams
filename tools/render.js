// SPDX-License-Identifier: GPL-3.0-only
// Render an SVG to PNG with headless Chromium.
// usage: node tools/render.js in.svg out.png [scale]
const { chromium } = require('playwright');
const fs = require('fs');
(async () => {
  const [,, svgPath, pngPath, scale] = process.argv;
  const svg = fs.readFileSync(svgPath, 'utf8');
  const m = svg.match(/width="(\d+)" height="(\d+)"/);
  const w = +m[1], h = +m[2];
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: w, height: h }, deviceScaleFactor: +(scale||1) });
  await p.setContent(`<html><body style="margin:0">${svg}</body></html>`);
  await p.waitForTimeout(200);
  await p.screenshot({ path: pngPath, clip: { x: 0, y: 0, width: w, height: h } });
  await b.close();
})();
