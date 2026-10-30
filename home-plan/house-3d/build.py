import sys, os, base64, json
# python3 build.py [--inline]   --inline puts the scanned assets inside the page (standalone file); otherwise they load from assets/
inline = '--inline' in sys.argv
d = open('house.json').read()
A = {}
if inline:
    for f in sorted(os.listdir('assets')):
        mime = 'model/gltf-binary' if f.endswith('.glb') else 'image/jpeg'
        A[f] = 'data:%s;base64,%s' % (mime, base64.b64encode(open(os.path.join('assets', f), 'rb').read()).decode())
s = open('src.html').read().replace('/*DATA*/', d).replace('/*ASSETS*/', json.dumps(A))
s = s.replace('<!--STILLS-->', open('stills.html').read() if os.path.exists('stills.html') else '')
open('house-3d.html', 'w').write(s)
open('local.html', 'w').write('<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover"></head><body style="margin:0">' + s + '</body></html>')
print(len(s))
