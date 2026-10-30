// ---------------------------------------------------------------- textures (color + relief, all drawn here so nothing loads from outside)
let seed = 7; const rnd = () => (seed = (seed * 16807) % 2147483647) / 2147483647;
const rr = (a, b) => a + (b - a) * rnd();
const TEXSCALE = mobile ? .5 : 1;
function cnv(w, h) { const c = document.createElement('canvas'); c.width = w; c.height = h; return c; }
function wrapTex(c, srgb) { const t = new THREE.CanvasTexture(c); t.wrapS = t.wrapT = THREE.RepeatWrapping; t.anisotropy = maxAniso; if (srgb) t.colorSpace = THREE.SRGBColorSpace; return t; }
function canvasTex(w, h, draw, srgb = true) { const c = cnv(w, h); draw(c.getContext('2d'), w, h); return wrapTex(c, srgb); }
// normal map from a grayscale height canvas (white = raised)
function normalFrom(hc, strength) {
  const w = hc.width, h = hc.height, src = hc.getContext('2d').getImageData(0, 0, w, h).data, out = cnv(w, h), g = out.getContext('2d'), img = g.createImageData(w, h);
  const H = (x, y) => src[(((y + h) % h) * w + ((x + w) % w)) * 4] / 255;
  for (let y = 0; y < h; y++) for (let x = 0; x < w; x++) {
    const dx = (H(x + 1, y) - H(x - 1, y)) * strength, dy = (H(x, y + 1) - H(x, y - 1)) * strength, l = Math.hypot(dx, dy, 1), i = (y * w + x) * 4;
    img.data[i] = (-dx / l * .5 + .5) * 255; img.data[i + 1] = (dy / l * .5 + .5) * 255; img.data[i + 2] = (1 / l * .5 + .5) * 255; img.data[i + 3] = 255; }
  g.putImageData(img, 0, 0); return wrapTex(out, false);
}
// one call draws color and height together: draw(colorCtx, heightCtx, w, h)
function surface(size, draw, strength = 4) {
  const w = Math.max(64, Math.round(size * TEXSCALE)), c = cnv(w, w), hc = cnv(w, w), g = c.getContext('2d'), hg = hc.getContext('2d');
  hg.fillStyle = '#808080'; hg.fillRect(0, 0, w, w); draw(g, hg, w, w);
  return { map: wrapTex(c, true), normalMap: normalFrom(hc, strength) };
}
function speckle(g, w, h, amp, n, size = 2) {
  for (let i = 0; i < n; i++) { const v = rr(-amp, amp); g.fillStyle = v > 0 ? `rgba(255,255,255,${v})` : `rgba(0,0,0,${-v})`; g.fillRect(rr(0, w), rr(0, h), size, size); }
}
function clouds(g, w, h, cols, n, rmin, rmax, a) { // soft tileable blotches
  for (let i = 0; i < n; i++) { const x = rr(0, w), y = rr(0, h), r = rr(rmin, rmax) * w, col = cols[Math.floor(rr(0, cols.length))];
    for (const ox of [-w, 0, w]) for (const oy of [-h, 0, h]) { const gr = g.createRadialGradient(x + ox, y + oy, 0, x + ox, y + oy, r);
      gr.addColorStop(0, `rgba(${col},${a})`); gr.addColorStop(1, `rgba(${col},0)`); g.fillStyle = gr; g.fillRect(x + ox - r, y + oy - r, 2 * r, 2 * r); } }
}
const rgb = (a) => `rgb(${a[0] | 0},${a[1] | 0},${a[2] | 0})`;
const T = {};
// board-and-batten: one batten per texture repeat (16 in on center)
T.siding = surface(256, (g, hg, w, h) => {
  g.fillStyle = '#efeee8'; g.fillRect(0, 0, w, h); speckle(g, w, h, .018, 900, 2);
  for (let i = 0; i < 26; i++) { g.fillStyle = `rgba(120,110,95,${rr(.01, .03)})`; g.fillRect(rr(0, w), 0, rr(1, 3), h); }
  const b = w * .14; g.fillStyle = '#f5f4f0'; g.fillRect(0, 0, b, h); g.fillStyle = 'rgba(0,0,0,.07)'; g.fillRect(b, 0, w * .02, h);
  const gr = hg.createLinearGradient(0, 0, b + w * .02, 0); gr.addColorStop(0, '#d8d8d8'); gr.addColorStop(.12, '#ffffff'); gr.addColorStop(.88, '#ffffff'); gr.addColorStop(1, '#808080');
  hg.fillStyle = gr; hg.fillRect(0, 0, b + w * .02, h);
}, 6);
// standing seam: one seam per 18 in panel, faint stiffening ribs
T.roof = surface(256, (g, hg, w, h) => {
  g.fillStyle = '#2f3134'; g.fillRect(0, 0, w, h); speckle(g, w, h, .02, 800, 2);
  const lg = g.createLinearGradient(0, 0, w, 0); lg.addColorStop(0, 'rgba(255,255,255,.05)'); lg.addColorStop(.5, 'rgba(0,0,0,.04)'); lg.addColorStop(1, 'rgba(255,255,255,.03)'); g.fillStyle = lg; g.fillRect(0, 0, w, h);
  g.fillStyle = 'rgba(255,255,255,.16)'; g.fillRect(0, 0, w * .02, h); g.fillStyle = 'rgba(0,0,0,.35)'; g.fillRect(w * .02, 0, w * .015, h);
  hg.fillStyle = '#ffffff'; hg.fillRect(0, 0, w * .03, h); hg.fillStyle = '#9a9a9a'; for (const f of [.33, .66]) hg.fillRect(w * f, 0, w * .01, h);
}, 10);
T.plaster = surface(512, (g, hg, w, h) => {
  g.fillStyle = '#ece5d8'; g.fillRect(0, 0, w, h); clouds(g, w, h, ['250,246,238', '222,212,196', '236,228,214'], 40, .08, .3, .35); speckle(g, w, h, .015, 3000, 2);
  clouds(hg, w, h, ['255,255,255', '0,0,0'], 60, .02, .08, .08);
}, 2);
T.pine = surface(1024, (g, hg, w, h) => { // 8 ft square, 6 in planks, random lengths
  const rows = 16, rh = h / rows;
  for (let r = 0; r < rows; r++) { let x = -rr(0, 300);
    while (x < w) { const L = rr(200, 520), k = rr(0, 1), c = [150 + 50 * k, 98 + 38 * k, 54 + 26 * k];
      g.fillStyle = rgb(c); g.fillRect(x, r * rh, L, rh);
      for (let s = 0; s < 22; s++) { g.fillStyle = `rgba(${rnd() > .5 ? '90,50,20' : '200,150,100'},${rr(.03, .1)})`; const yy = r * rh + rr(0, rh); g.fillRect(x, yy, L, rr(.6, 2)); }
      if (rnd() < .35) { g.fillStyle = 'rgba(70,35,10,.25)'; g.beginPath(); g.ellipse(x + rr(20, L - 20), r * rh + rr(10, rh - 10), rr(3, 7), rr(2, 4), 0, 0, 7); g.fill(); }
      hg.fillStyle = '#404040'; hg.fillRect(x, r * rh, 2, rh); x += L; }
    hg.fillStyle = '#404040'; hg.fillRect(0, r * rh, w, 2); }
  g.fillStyle = 'rgba(255,220,170,.06)'; g.fillRect(0, 0, w, h);
}, 3);
T.stone = surface(512, (g, hg, w, h) => { // honed limestone, 2 ft tiles
  g.fillStyle = '#d6cdbb'; g.fillRect(0, 0, w, h); clouds(g, w, h, ['232,224,208', '196,186,166'], 30, .05, .2, .4); speckle(g, w, h, .05, 6000, 1);
  g.fillStyle = 'rgba(110,100,80,.45)'; hg.fillStyle = '#303030';
  for (let i = 0; i < 2; i++) { g.fillRect(0, i * h / 2, w, 3); g.fillRect(i * w / 2, 0, 3, h); hg.fillRect(0, i * h / 2, w, 3); hg.fillRect(i * w / 2, 0, 3, h); }
}, 4);
T.brick = surface(512, (g, hg, w, h) => { // old Louisiana brick, 2 ft square
  g.fillStyle = '#cfc4b2'; g.fillRect(0, 0, w, h); hg.fillStyle = '#383838'; hg.fillRect(0, 0, w, h);
  const cw = w / 3, ch = h / 9;
  for (let r = 0; r < 9; r++) for (let c = -1; c < 4; c++) { const x = c * cw + (r % 2) * cw / 2, y = r * ch, k = rr(0, 1);
    const col = [118 + 50 * k + rr(-8, 8), 66 + 26 * k, 50 + 18 * k]; g.fillStyle = rgb(col); g.fillRect(x + 3, y + 3, cw - 6, ch - 6);
    g.fillStyle = `rgba(30,15,5,${rr(0, .2)})`; g.fillRect(x + 3, y + ch * .55, cw - 6, ch * .4);
    hg.fillStyle = '#c8c8c8'; hg.fillRect(x + 3, y + 3, cw - 6, ch - 6); }
  speckle(g, w, h, .06, 5000, 2);
}, 5);
T.flag = surface(1024, (g, hg, w, h) => { // irregular bluestone and limestone pieces, tileable
  const n = 34, S = Array.from({ length: n }, () => [rr(0, w), rr(0, h)]), C = S.map(() => { const k = rr(0, 1), b = rnd() < .5; return b ? [150 + 30 * k, 152 + 30 * k, 150 + 26 * k] : [196 + 26 * k, 184 + 24 * k, 160 + 20 * k]; });
  const img = g.createImageData(w, h), him = hg.createImageData(w, h);
  for (let y = 0; y < h; y++) for (let x = 0; x < w; x++) { let d1 = 1e9, d2 = 1e9, k1 = 0;
    for (let i = 0; i < n; i++) { let dx = Math.abs(x - S[i][0]); dx = Math.min(dx, w - dx); let dy = Math.abs(y - S[i][1]); dy = Math.min(dy, h - dy); const d = dx * dx + dy * dy;
      if (d < d1) { d2 = d1; d1 = d; k1 = i; } else if (d < d2) d2 = d; }
    const edge = Math.sqrt(d2) - Math.sqrt(d1), j = (y * w + x) * 4, grout = edge < 5;
    const c = grout ? [118, 112, 100] : C[k1], v = rr(-8, 8);
    img.data[j] = c[0] + v; img.data[j + 1] = c[1] + v; img.data[j + 2] = c[2] + v; img.data[j + 3] = 255;
    const hv = grout ? 40 : Math.min(255, 150 + edge * 4); him.data[j] = him.data[j + 1] = him.data[j + 2] = hv; him.data[j + 3] = 255; }
  g.putImageData(img, 0, 0); hg.putImageData(him, 0, 0);
}, 3);
T.lawn = surface(1024, (g, hg, w, h) => {
  g.fillStyle = '#5f8238'; g.fillRect(0, 0, w, h); clouds(g, w, h, ['120,150,60', '70,110,40', '140,150,70'], 50, .05, .25, .25);
  for (let i = 0; i < 60000 * TEXSCALE; i++) { const x = rr(0, w), y = rr(0, h), k = rr(0, 1); g.strokeStyle = `rgba(${70 + 90 * k | 0},${110 + 70 * k | 0},${35 + 30 * k | 0},.55)`; g.lineWidth = 1;
    g.beginPath(); g.moveTo(x, y); g.lineTo(x + rr(-2, 2), y - rr(3, 7)); g.stroke(); }
  speckle(hg, w, h, .5, 40000 * TEXSCALE, 2);
}, 2);
T.conc = surface(256, (g, hg, w, h) => { g.fillStyle = '#bdb9b0'; g.fillRect(0, 0, w, h); clouds(g, w, h, ['210,206,198', '170,166,158'], 20, .1, .3, .3); speckle(g, w, h, .05, 4000, 1); speckle(hg, w, h, .3, 3000, 1); }, 1);
T.drive = surface(512, (g, hg, w, h) => { // broom-finished concrete with saw-cut joints every 10 ft
  g.fillStyle = '#cbc6bb'; g.fillRect(0, 0, w, h); clouds(g, w, h, ['220,214,204', '180,174,164'], 26, .08, .3, .3);
  for (let y = 0; y < h; y += 2) { g.fillStyle = `rgba(0,0,0,${rr(0, .035)})`; g.fillRect(0, y, w, 1); }
  g.fillStyle = 'rgba(60,55,50,.5)'; g.fillRect(0, 0, w, 3); g.fillRect(0, 0, 3, h); hg.fillStyle = '#202020'; hg.fillRect(0, 0, w, 3); hg.fillRect(0, 0, 3, h);
}, 3);
T.cypress = surface(512, (g, hg, w, h) => {
  g.fillStyle = '#8c6440'; g.fillRect(0, 0, w, h);
  for (let i = 0; i < 300; i++) { const x = rr(0, w), a = rr(.04, .16); g.fillStyle = `rgba(${rnd() > .5 ? '55,32,14' : '196,146,96'},${a})`; g.fillRect(x, 0, rr(.6, 3), h); hg.fillStyle = `rgba(0,0,0,${a})`; hg.fillRect(x, 0, rr(.6, 3), h); }
  for (let i = 0; i < 6; i++) { g.fillStyle = 'rgba(60,35,15,.25)'; g.beginPath(); g.ellipse(rr(0, w), rr(0, h), rr(4, 9), rr(12, 30), 0, 0, 7); g.fill(); }
}, 2);
T.walnut = surface(256, (g, hg, w, h) => { g.fillStyle = '#56392a'; g.fillRect(0, 0, w, h); for (let i = 0; i < 160; i++) { const x = rr(0, w); g.fillStyle = `rgba(${rnd() > .5 ? '30,18,10' : '120,85,60'},${rr(.05, .2)})`; g.fillRect(x, 0, rr(.5, 2.5), h); } }, 1);
T.oak = surface(256, (g, hg, w, h) => { g.fillStyle = '#b89a74'; g.fillRect(0, 0, w, h); for (let i = 0; i < 220; i++) { const x = rr(0, w); g.fillStyle = `rgba(${rnd() > .5 ? '120,95,65' : '215,195,165'},${rr(.05, .2)})`; g.fillRect(x, 0, rr(.5, 2), h); } }, 1);
T.marble = surface(512, (g, hg, w, h) => { // honed white marble with soft gray veining
  g.fillStyle = '#efece6'; g.fillRect(0, 0, w, h); clouds(g, w, h, ['255,255,255', '220,216,210'], 20, .1, .35, .4);
  for (let k = 0; k < 9; k++) { let x = rr(0, w), y = rr(0, h), a = rr(0, 6.28); g.strokeStyle = `rgba(120,118,115,${rr(.15, .4)})`; g.lineWidth = rr(.6, 2.2); g.beginPath(); g.moveTo(x, y);
    for (let s = 0; s < 60; s++) { a += rr(-.35, .35); x += Math.cos(a) * 9; y += Math.sin(a) * 9; g.lineTo(x, y); } g.stroke(); }
}, .5);
T.cabinet = surface(256, (g, hg, w, h) => { // 18 in shaker door: rails, stiles and a recessed panel
  g.fillStyle = '#d4ccbc'; g.fillRect(0, 0, w, h); speckle(g, w, h, .02, 500, 2);
  const b = w * .14; g.fillStyle = 'rgba(0,0,0,.06)'; g.fillRect(b, b, w - 2 * b, h - 2 * b); g.fillStyle = 'rgba(0,0,0,.35)'; g.fillRect(0, 0, w, 2); g.fillRect(0, 0, 2, h);
  hg.fillStyle = '#c0c0c0'; hg.fillRect(0, 0, w, h); hg.fillStyle = '#606060'; hg.fillRect(b, b, w - 2 * b, h - 2 * b); hg.fillStyle = '#202020'; hg.fillRect(0, 0, w, 3); hg.fillRect(0, 0, 3, h);
}, 5);
T.rug = surface(512, (g, hg, w, h) => { // faded wool rug: field, medallion, border
  g.fillStyle = '#c3ad8e'; g.fillRect(0, 0, w, h); clouds(g, w, h, ['210,190,160', '170,140,110', '160,150,140'], 30, .05, .2, .35);
  g.strokeStyle = 'rgba(120,80,60,.35)'; g.lineWidth = w * .03; g.strokeRect(w * .06, h * .06, w * .88, h * .88); g.strokeStyle = 'rgba(80,90,110,.25)'; g.lineWidth = w * .012; g.strokeRect(w * .11, h * .11, w * .78, h * .78);
  g.fillStyle = 'rgba(120,80,60,.18)'; g.beginPath(); g.ellipse(w / 2, h / 2, w * .2, h * .28, 0, 0, 7); g.fill(); speckle(g, w, h, .05, 8000, 1); speckle(hg, w, h, .4, 8000, 1);
}, 1);
T.gravel = surface(512, (g, hg, w, h) => { g.fillStyle = '#9e927b'; g.fillRect(0, 0, w, h);
  for (let i = 0; i < 5000 * TEXSCALE; i++) { const x = rr(0, w), y = rr(0, h), r = rr(1.5, 5), k = rr(0, 1); g.fillStyle = rgb([130 + 90 * k, 120 + 80 * k, 100 + 70 * k]); g.beginPath(); g.ellipse(x, y, r, r * rr(.6, 1), rr(0, 3), 0, 7); g.fill();
    hg.fillStyle = `rgb(${180 + rr(0, 75) | 0},${180 | 0},180)`; hg.beginPath(); hg.ellipse(x, y, r, r * .8, 0, 0, 7); hg.fill(); } }, 3);
T.sand = surface(256, (g, hg, w, h) => { g.fillStyle = '#d8c7a0'; g.fillRect(0, 0, w, h); speckle(g, w, h, .06, 6000, 1); speckle(hg, w, h, .3, 4000, 1); }, 1);
T.basin = surface(256, (g, hg, w, h) => { g.fillStyle = '#7a6c50'; g.fillRect(0, 0, w, h); for (let i = 0; i < 2000; i++) { const k = rr(0, 1); g.fillStyle = rgb([90 + 80 * k, 80 + 70 * k, 60 + 50 * k]); g.beginPath(); g.arc(rr(0, w), rr(0, h), rr(1, 4), 0, 7); g.fill(); } }, 2);
T.paint = surface(128, (g, hg, w, h) => { g.fillStyle = '#f4f2ec'; g.fillRect(0, 0, w, h); speckle(g, w, h, .01, 200, 1); }, .2);
const waterNormal = canvasTex(256, 256, (g, w, h) => {
  const hgt = new Float32Array(w * h);
  for (let k = 0; k < 40; k++) { const fx = Math.round(rr(1, 9)), fy = Math.round(rr(1, 9)), ph = rr(0, 6.28), a = 1 / (fx + fy);
    for (let y = 0; y < h; y++) for (let x = 0; x < w; x++) hgt[y * w + x] += a * Math.sin(6.283 * (fx * x / w + fy * y / h) + ph); }
  const img = g.createImageData(w, h);
  for (let y = 0; y < h; y++) for (let x = 0; x < w; x++) {
    const dx = hgt[y * w + (x + 1) % w] - hgt[y * w + (x + w - 1) % w], dy = hgt[((y + 1) % h) * w + x] - hgt[((y + h - 1) % h) * w + x];
    const n = new THREE.Vector3(-dx * 3, -dy * 3, 1).normalize(), i = (y * w + x) * 4;
    img.data[i] = (n.x * .5 + .5) * 255; img.data[i + 1] = (n.y * .5 + .5) * 255; img.data[i + 2] = (n.z * .5 + .5) * 255; img.data[i + 3] = 255; }
  g.putImageData(img, 0, 0);
}, false);
const fallsTex = canvasTex(64, 256, (g, w, h) => { g.fillStyle = 'rgba(210,235,240,.55)'; g.fillRect(0, 0, w, h);
  for (let i = 0; i < 260; i++) { g.fillStyle = `rgba(255,255,255,${rr(.2, .7)})`; g.fillRect(rr(0, w), rr(0, h), rr(1, 2.5), rr(10, 50)); } });
const artTex = [0, 1, 2, 3].map(k => canvasTex(256, 320, (g, w, h) => { // quiet abstract canvases
  const pal = [['#d9cbb3', '#a8866a', '#3e4a45', '#e8e1d3'], ['#c9d0cf', '#5f7570', '#d7c8a6', '#2e3534'], ['#e6dccb', '#b5694b', '#4b4036', '#efe9dd'], ['#b9c1b0', '#7d8a6c', '#efe8da', '#40463b']][k];
  g.fillStyle = pal[0]; g.fillRect(0, 0, w, h);
  for (let i = 0; i < 7; i++) { g.fillStyle = pal[1 + (i % 3)]; g.globalAlpha = rr(.25, .7); const x = rr(-40, w - 40), y = rr(-40, h - 40); g.beginPath(); g.ellipse(x, y, rr(40, 130), rr(30, 110), rr(0, 3), 0, 7); g.fill(); }
  g.globalAlpha = 1; speckle(g, w, h, .05, 3000, 1);
}));

// ---------------------------------------------------------------- materials
const M = {};
const std = (k, o) => (M[k] = new THREE.MeshStandardMaterial(Object.assign({ roughness: .85 }, o)));
const surf = (t, o) => Object.assign({ map: t.map, normalMap: t.normalMap }, o);
std('siding', surf(T.siding, { roughness: .78 }));
std('gable', surf(T.siding, { roughness: .78, side: THREE.DoubleSide }));
std('trim', surf(T.paint, { roughness: .55 }));
std('plaster', surf(T.plaster, { roughness: .95 }));
std('ceiling', surf(T.plaster, { roughness: .95, side: THREE.DoubleSide }));
std('roof', surf(T.roof, { roughness: .38, metalness: .6, envMapIntensity: .9 }));
std('pine', surf(T.pine, { roughness: .45, envMapIntensity: .6 }));
std('tile', surf(T.stone, { roughness: .55 }));
std('conc', surf(T.conc, { roughness: .4, color: 0xdedad2 }));   // sealed garage floor
std('drive', surf(T.drive, { roughness: .95 }));
std('brick', surf(T.brick, { roughness: .9 }));
std('skirt', surf(T.brick, { roughness: .9 }));
std('lawn', surf(T.lawn, { roughness: 1 }));
std('gravel', surf(T.gravel, { roughness: 1 }));
std('sand', surf(T.sand, { roughness: 1 }));
std('flag', surf(T.flag, { roughness: .85 }));
std('cypress', surf(T.cypress, { roughness: .6 }));
std('cypressDS', surf(T.cypress, { roughness: .6, side: THREE.DoubleSide }));
std('basin', surf(T.basin, { roughness: 1, side: THREE.DoubleSide }));
std('frame', { color: 0x1b1b1b, roughness: .45, metalness: .35 });
std('bronze', { color: 0x3a2c20, roughness: .35, metalness: .7 });
std('glass', { color: 0x16222a, roughness: .02, metalness: .95, transparent: true, opacity: .32, depthWrite: false, side: THREE.DoubleSide });
std('cap', { color: 0x2a2621, roughness: 1 });
std('fabric', { color: 0xcdbfa6, roughness: 1, sheen: 1 });
std('fabric2', { color: 0xb9a88c, roughness: 1 });
std('velvet', { color: 0x4e5a48, roughness: .9 });
std('linen', { color: 0xf3efe6, roughness: 1 });
std('rug', surf(T.rug, { roughness: 1 }));
std('walnut', surf(T.walnut, { roughness: .5 }));
std('oak', surf(T.oak, { roughness: .55 }));
std('cabinet', surf(T.cabinet, { roughness: .5 }));
std('green', { color: 0x1d3a2e, roughness: .18, metalness: .05, envMapIntensity: 1.2 });
std('marble', surf(T.marble, { roughness: .32, envMapIntensity: .8 }));
std('steel', { color: 0xb8bbbd, roughness: .25, metalness: .85 });
std('black', { color: 0x141414, roughness: .3 });
std('brass', { color: 0xb48a4a, roughness: .3, metalness: 1 });
std('copper', { color: 0xa8653a, roughness: .35, metalness: 1 });
std('porcelain', { color: 0xf6f6f2, roughness: .15 });
std('leaf', { color: 0x4b6a33, roughness: .85 });
std('leaf2', { color: 0x37552a, roughness: .85 });
std('leaf3', { color: 0x6a7a3a, roughness: .85 });
std('oakleaf', { color: 0x3f5530, roughness: .85 });
std('oakleaf2', { color: 0x4c6338, roughness: .85 });
std('moss', { color: 0x9aa48f, roughness: 1, side: THREE.DoubleSide });
std('crape', { color: 0xd98ca8, roughness: .8 });
std('hydrangea', { color: 0xe9eef2, roughness: .8 });
std('mulch', { color: 0x4a3426, roughness: 1 });
std('cyp', { color: 0x5d6b3a, roughness: .9 });
std('bark', { color: 0x4a3b2e, roughness: 1 });
std('rock', { color: 0x8d8576, roughness: .95, flatShading: true });
std('limestone', surf(T.stone, { roughness: .7, color: 0xf2ece0 }));
std('carDark', { color: 0x262b2f, roughness: .25, metalness: .7 });
std('carLight', { color: 0xe7e6e2, roughness: .25, metalness: .5 });
std('grass', { color: 0x6c8a3c, roughness: 1, side: THREE.DoubleSide });
std('figure', { color: 0x6f7f8c, roughness: .8 });
std('pad', { color: 0xbab6ad, roughness: 1 });
std('fire', { color: 0xff8a2a, emissive: 0xff6a10, emissiveIntensity: 2 });
std('flame', { color: 0xffd9a0, emissive: 0xffb050, emissiveIntensity: 3 });   // gas lanterns burn day and night
std('bulb', { color: 0xfff4e0, emissive: 0xffd8a0, emissiveIntensity: .4 });
std('lily', { color: 0x4e7a34, roughness: .7 });
std('bloom', { color: 0xf1b7c4, roughness: .7 });
for (let k = 0; k < 4; k++) std('art' + k, { map: artTex[k], roughness: .9 });
M.falls = new THREE.MeshStandardMaterial({ map: fallsTex, transparent: true, opacity: .9, roughness: .2, side: THREE.DoubleSide, depthWrite: false });
waterNormal.repeat.set(1 / 26, 1 / 26);
// cut-away for the dollhouse: everything built as part of the house clips at 8.5 ft
const CLIP = new THREE.Plane(new THREE.Vector3(0, -1, 0), 8.5);
const CLIPPED = ['siding', 'trim', 'plaster', 'frame', 'bronze', 'glass', 'cypress', 'green', 'gable', 'cabinet', 'black', 'steel', 'brass', 'copper', 'bulb', 'flame', 'art0', 'art1', 'art2', 'art3', 'oak', 'walnut'];
