const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1300, height: 1000 }, deviceScaleFactor: 1.5 });
  await p.goto('file://' + process.argv[2]); await p.waitForTimeout(500);
  const figs = await p.$$('figure.d-fig, .d-fig');
  let i = 0; for (const f of figs) { await f.screenshot({ path: process.argv[3] + '-' + (i++) + '.png' }); }
  console.log('figs', i); await b.close();
})();
