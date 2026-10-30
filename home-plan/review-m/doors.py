exec(open('composite.py').read())
from shapely.geometry import Polygon, box, Point
import math
def sector(d):
    x, y, w, ax, s, hs = d
    if ax == 'h':
        hx = x if hs else x + w; ox = x + w if hs else x
        a0 = math.atan2(0, ox - hx); a1 = math.atan2(s * w, 0)
        c = (hx, y)
    else:
        hy = y if hs else y + w; oy = y + w if hs else y
        a0 = math.atan2(oy - hy, 0); a1 = math.atan2(0, s * w)
        c = (x, hy)
    # quarter circle between a0 and a1 (shortest)
    da = (a1 - a0 + math.pi) % (2 * math.pi) - math.pi
    pts = [c] + [(c[0] + w * math.cos(a0 + da * i / 16), c[1] + w * math.sin(a0 + da * i / 16)) for i in range(17)]
    return Polygon(pts)
names = ['Guest suite 2 door','Bedroom 3 door','Server door','Living to guest foyer','Closet 3','Front door L','Front door R','Porch door',
 'Suite foyer door','Powder door','Office door','Dressing to bath','Primary WC','Laundry from hall','Laundry exterior','Garage to hall','Closet under stair',
 'Dining French L','Dining French R','Lounge door L','Lounge door R']
S = [sector(d).buffer(-0.05) for d in DOORS]
for i, a in enumerate(S):
    for j in range(i + 1, len(S)):
        if a.intersects(S[j]): print('DOOR CLASH', names[i], '<->', names[j], round(a.intersection(S[j]).area, 2))
    for f in FX:
        b = box(f['x1'], f['y1'], f['x2'], f['y2'])
        if a.intersects(b) and a.intersection(b).area > 0.05: print('HITS FIXTURE', names[i], '->', f['label'], round(a.intersection(b).area, 2))
    for x, y, r in CIRCLES:
        if a.intersects(Point(x, y).buffer(r)): print('HITS', names[i], 'circle', x, y)
