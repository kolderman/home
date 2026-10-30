const { chromium } = require('playwright');
(async () => { const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1200, height: 900 }, deviceScaleFactor: 2, colorScheme: 'light' });
  for (const s of process.argv.slice(2)) { await p.goto('file://' + process.cwd() + '/png-' + s + '.html'); await p.waitForTimeout(800);
    await (await p.$('#c')).screenshot({ path: 'primary-suite-' + s + '.png' }); } await b.close(); })();
