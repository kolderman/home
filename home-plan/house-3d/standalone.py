# Builds ../house-3d-standalone.html: one file with the scanned assets and the stills inside it (stills resized to 1600 px).
# Run after: python3 build.py --inline
import base64, io, re, subprocess
s = open('house-3d.html').read()
def still(m):
    p = m.group(1)
    jpg = subprocess.run(['convert', p, '-resize', '1600x', '-quality', '82', 'jpg:-'], capture_output=True, check=True).stdout
    return 'src="data:image/jpeg;base64,' + base64.b64encode(jpg).decode() + '"'
s = re.sub(r'src="(stills/[^"]+\.jpg)"', still, s)
open('../house-3d-standalone.html', 'w').write(s)
print(len(s) // 1024, 'KB')
