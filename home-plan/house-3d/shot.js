const { chromium } = require('playwright'); const path = require('path'); const fs = require('fs');
(async () => {
  const [,, q, out, w = 1600, h = 900] = process.argv;
  const b = await chromium.launch({ args: ['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'] });
  const p = await b.newPage({ viewport: { width: +w, height: +h } });
  p.on('console', m => { if (m.type() === 'error' || m.type() === 'warning') console.log('console:', m.text().slice(0, 300)); });
  p.on('pageerror', e => console.log('pageerror:', e.message));
  await p.route('https://cdn.jsdelivr.net/npm/three@0.160.0/**', r => { const f = r.request().url().split('three@0.160.0/')[1]; r.fulfill({ path: path.join(__dirname, 'node_modules/three', f), contentType: 'text/javascript' }); });
  await p.route('https://fonts.googleapis.com/**', r => r.fulfill({ body: '', contentType: 'text/css' }));
  await p.goto((process.env.BASE || ('file://' + __dirname + '/')) + (process.env.PAGE || 'local.html') + q, { timeout: 300000, waitUntil: 'commit' });
  try { await p.waitForFunction(() => window.__ready || document.getElementById('loading').hidden, null, { timeout: 180000 }); } catch (e) { console.log('timeout'); }
  await p.waitForTimeout(q.includes('still') ? 500 : 2500);
  await p.screenshot({ path: out, timeout: 300000 });
  await b.close();
})();
