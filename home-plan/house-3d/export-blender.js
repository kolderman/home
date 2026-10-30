// Exports the model as a GLB for Blender: node export-blender.js out.glb
// Drops what Blender rebuilds itself (mirror water, sky, clouds, mist sprites, labels, lights) and expands instanced meshes.
const { chromium } = require('playwright'); const path = require('path'); const fs = require('fs');
(async () => {
  const out = process.argv[2];
  const b = await chromium.launch({ args: ['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'] });
  const p = await b.newPage({ viewport: { width: 640, height: 360 } });
  p.on('pageerror', e => console.log('pageerror:', e.message));
  p.on('console', m => { if (m.type() === 'error') console.log('console:', m.text().slice(0, 300)); });
  await p.route('https://cdn.jsdelivr.net/npm/three@0.160.0/**', r => { const f = r.request().url().split('three@0.160.0/')[1]; r.fulfill({ path: path.join(__dirname, 'node_modules/three', f), contentType: 'text/javascript' }); });
  await p.route('https://fonts.googleapis.com/**', r => r.fulfill({ body: '', contentType: 'text/css' }));
  await p.goto('file://' + path.join(__dirname, 'local.html') + '?still=out:back:16.5');
  await p.waitForFunction(() => window.__ready, null, { timeout: 300000 });
  const n = await p.evaluate(async () => {
    const { THREE, scene, water, sky, cloudsMesh, P, wz } = window.__X;
    const { GLTFExporter } = await import('three/addons/exporters/GLTFExporter.js');
    const root = new THREE.Group(); root.name = 'HOUSE';
    const skip = o => o === water || o === sky || o === cloudsMesh || o.isSprite || o.isLight || o.isPoints || !o.visible;
    const mats = new Map();
    const exportMat = m => { // plain standard material copy, named so Blender can find and upgrade it
      if (mats.has(m)) return mats.get(m);
      const c = new THREE.MeshStandardMaterial({ color: m.color, map: m.map || null, normalMap: m.normalMap || null, roughnessMap: m.roughnessMap || null,
        roughness: m.roughness ?? .8, metalness: m.metalness ?? 0, emissive: m.emissive || new THREE.Color(0), emissiveMap: m.emissiveMap || null, emissiveIntensity: m.emissiveIntensity ?? 1,
        transparent: !!m.transparent, opacity: m.opacity ?? 1, side: m.side, alphaTest: m.alphaTest || 0 });
      c.name = m.name || ''; mats.set(m, c); return c; };
    // name materials by their key in M
    for (const [k, m] of Object.entries(window.__X.M)) if (m && m.isMaterial && !m.name) m.name = k;
    let count = 0;
    scene.updateMatrixWorld(true);
    scene.traverse(o => {
      if (!o.isMesh || skip(o)) return; let a = o; while (a) { if (skip(a)) return; a = a.parent; }
      const mm = Array.isArray(o.material) ? o.material[0] : o.material; if (!mm || mm.isShaderMaterial) return;
      const mat = exportMat(mm);
      if (o.isInstancedMesh) { const m4 = new THREE.Matrix4(), col = new THREE.Color();
        for (let i = 0; i < o.count; i++) { o.getMatrixAt(i, m4); const g = o.geometry.clone().applyMatrix4(m4).applyMatrix4(o.matrixWorld);
          let mt = mat; if (o.instanceColor) { o.getColorAt(i, col); mt = mat.clone(); mt.color.copy(col); mt.name = mat.name + '_i'; }
          const x = new THREE.Mesh(g, mt); x.name = (mm.name || 'inst') + '_' + i; root.add(x); count++; } return; }
      const g = o.geometry.clone().applyMatrix4(o.matrixWorld); const x = new THREE.Mesh(g, mat); x.name = mm.name || o.name || 'mesh'; root.add(x); count++; });
    // the pond surface as a plain named plane; Blender gives it real water
    const shape = new THREE.Shape(P.sw.map(([x, y]) => new THREE.Vector2(x, -y)));
    const wg = new THREE.ShapeGeometry(shape, 4); wg.rotateX(-Math.PI / 2); wg.translate(0, wz, 0);
    const wm = new THREE.MeshStandardMaterial({ color: 0x0f2b2c, roughness: .02 }); wm.name = 'POND_WATER'; const w = new THREE.Mesh(wg, wm); w.name = 'POND_WATER'; root.add(w);
    const ex = new GLTFExporter();
    const buf = await ex.parseAsync(root, { binary: true, maxTextureSize: 4096 });
    const u8 = new Uint8Array(buf); let s = ''; const CH = 0x8000; const parts = [];
    for (let i = 0; i < u8.length; i += CH) parts.push(String.fromCharCode.apply(null, u8.subarray(i, i + CH)));
    window.__glb = btoa(parts.join('')); return count; });
  const len = await p.evaluate(() => window.__glb.length); const chunks = [];
  for (let i = 0; i < len; i += 8e6) chunks.push(await p.evaluate(([a, b]) => window.__glb.slice(a, b), [i, i + 8e6]));
  fs.writeFileSync(out, Buffer.from(chunks.join(''), 'base64'));
  console.log('meshes', n, 'bytes', fs.statSync(out).size);
  await b.close();
})();
