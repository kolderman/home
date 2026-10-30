// 11x17 markup PDF: one figure per page, vector, from the plan page
const { chromium } = require('playwright');
(async () => {
  const [,, page, out] = process.argv;
  const b = await chromium.launch(); const p = await b.newPage();
  await p.goto('file://' + page); await p.waitForTimeout(500);
  const PAGES = [[0, 'Floor plan, sketch'], [1, 'Floor plan, to scale'], [3, 'Roof plan'], [2, 'Low-voltage plan'], [4, 'Upstairs options (bonus room over the garage)']];
  const files = [];
  for (const [i, name] of PAGES) {
    await p.goto('file://' + page); await p.waitForTimeout(300);
    await p.evaluate(([i, name]) => {
      const figs = [...document.querySelectorAll('.d-fig')]; const f = figs[i];   // moved, not cloned: url(#id) references must stay live
      f.querySelectorAll('figcaption').forEach(c => c.remove());
      let host = document.getElementById('pdfhost'); if (host) host.remove();
      for (const c of document.body.children) c.style.display = 'none';
      host = document.createElement('div'); host.id = 'pdfhost'; host.className = 'doc';
      host.style.cssText = 'display:block;width:16.4in;max-width:none;margin:0;padding:0;border:0;background:#fff;font-family:system-ui,sans-serif';
      host.innerHTML = `<div style="display:flex;justify-content:space-between;align-items:baseline;font-size:13pt;margin-bottom:.12in"><b>New home · Draft M · ${name}</b><span style="font-size:10pt;color:#555">Oct 30, 2026 · mark up anywhere · 1 grid square = 2 ft</span></div>`;
      f.style.cssText = 'margin:0;max-width:none;width:100%;break-inside:auto';
      const minis0 = f.querySelector('.d-minis');
      f.querySelectorAll('svg').forEach(s => { s.style.width = '100%'; s.style.height = minis0 ? '9.4in' : '9.5in'; });
      const minis = f.querySelector('.d-minis'); if (minis) { minis.style.width = '100%'; minis.style.display = 'grid'; minis.style.gridTemplateColumns = '1fr 1fr'; minis.style.gap = '.3in'; }
      host.appendChild(f); document.body.appendChild(host); document.body.style.background = '#fff'; document.body.style.margin = '0';
    }, [i, name]);
    const fn = `/tmp/claude-0/work/pdf/p${files.length}.pdf`;
    await p.pdf({ path: fn, width: '17in', height: '11in', margin: { top: '.3in', bottom: '.3in', left: '.3in', right: '.3in' }, printBackground: true, pageRanges: '1' });
    files.push(fn);
  }
  await b.close(); console.log(files.join(' '));
})();
