const { chromium } = require('playwright'); const path = require('path');
(async () => {
  const b = await chromium.launch({ args: ['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'] });
  const p = await b.newPage({ viewport: { width: +(process.argv[4] || 1600), height: +(process.argv[5] || 900) } });
  p.on('console', m => { const t = m.text(); if (!t.includes('GPU stall')) console.log('console:', m.type(), t.slice(0, 300)); });
  p.on('pageerror', e => console.log('pageerror:', e.message, (e.stack || '').slice(0, 500)));
  await p.route('https://cdn.jsdelivr.net/npm/three@0.160.0/**', r => { const f = r.request().url().split('three@0.160.0/')[1]; r.fulfill({ path: path.join(__dirname, 'node_modules/three', f), contentType: 'text/javascript' }); });
  await p.route('https://fonts.googleapis.com/**', r => r.fulfill({ body: '', contentType: 'text/css' }));
  await p.goto('http://localhost:8765/local.html' + process.argv[2], { timeout: 300000, waitUntil: 'commit' });
  for (let i = 0; i < 60; i++) { await p.waitForTimeout(5000); const s = await p.evaluate(() => [window.__ready, document.getElementById('loading') && document.getElementById('loading').hidden, document.getElementById('loading') && document.getElementById('loading').textContent]); console.log(i, JSON.stringify(s)); if (s[0]) break; }
  await p.screenshot({ path: process.argv[3], timeout: 400000 }); await b.close();
})();
