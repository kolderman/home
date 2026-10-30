const { chromium } = require('playwright'); const path = require('path');
(async () => {
  const b = await chromium.launch({ args: ['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'] });
  const p = await b.newPage({ viewport: { width: 1000, height: 640 } });
  p.on('console', m => { if (m.type() === 'error' || m.type() === 'warning') console.log('console:', m.text().slice(0, 300)); });
  p.on('pageerror', e => console.log('pageerror:', e.message));
  await p.route('https://cdn.jsdelivr.net/npm/three@0.160.0/**', r => { const f = r.request().url().split('three@0.160.0/')[1]; r.fulfill({ path: path.join(__dirname, 'node_modules/three', f), contentType: 'text/javascript' }); });
  await p.route('https://fonts.googleapis.com/**', r => r.fulfill({ body: '', contentType: 'text/css' }));
  const t0 = Date.now();
  await p.goto('file://' + path.join(__dirname, 'local.html'));
  await p.waitForFunction(() => document.getElementById('loading').hidden, null, { timeout: 240000 });
  console.log('loaded in', (Date.now() - t0) / 1000, 's');
  for (const m of ['doll', 'walk', 'out']) { await p.evaluate(m => document.querySelector(`#modes button[data-m="${m}"]`).click(), m); await p.waitForTimeout(6000); console.log('mode', m, 'ok'); }
  await p.evaluate(() => { const t = document.getElementById('tod'); t.value = 19.3; t.dispatchEvent(new Event('input')); }); await p.waitForTimeout(6000); console.log('dusk ok');
  console.log('err shown:', await p.evaluate(() => !document.getElementById('err').hidden));
  await b.close();
})();
