"""Export the house (draft L) + long pond yard to JSON for the 3D viewer.
Reads plan-generator.py, roofkit.py and landscape-generator/{geo,long}.py from the project folder (read only).
PLAN_DIR overrides where plan-generator.py and roofkit.py are read from."""
import sys, os, json, re, math
HP = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '')
PLAN = os.path.join(os.environ.get('PLAN_DIR', HP), '')
OUT = sys.argv[1]

# ---- house constants, roofs and furniture(): exec plan-generator.py minus its page() call
src = open(PLAN + 'plan-generator.py').read()
src = src[:src.rindex('\npage()')]
H = {'__name__': 'plan', '__file__': PLAN + 'plan-generator.py'}
sys.argv = ['x', '/dev/null', '/dev/null']
exec(compile(src, 'plan', 'exec'), H)
import roofkit
from shapely.geometry import Polygon, Point, box as sbox, MultiPolygon
from shapely.geometry.polygon import orient

# ---- pond geometry: geo.py helpers + the geometry block of long.py
G = {}
exec(open(HP + 'landscape-generator/geo.py').read(), G)
ls = open(HP + 'landscape-generator/long.py').read()
blk = ls[ls.index('LQ = '):ls.index('def lgal')]
exec(blk, G)

r2 = lambda pts: [[round(x, 2), round(y, 2)] for x, y in pts]

# ---- walls: merge axis-aligned segments
segs = []  # (orient, c, a, b, ext)
def add(p, q, ext):
    (x1, y1), (x2, y2) = p, q
    if abs(y1 - y2) < 1e-6: segs.append(('h', round(y1, 3), min(x1, x2), max(x1, x2), ext))
    elif abs(x1 - x2) < 1e-6: segs.append(('v', round(x1, 3), min(y1, y2), max(y1, y2), ext))
S = H['SHELL']
for a, b in zip(S, S[1:] + S[:1]): add(a, b, True)
for name, x1, y1, x2, y2, fl, walls, *_ in H['ROOMS']:
    if walls and name != 'Garage':
        for a, b in [((x1, y1), (x2, y1)), ((x2, y1), (x2, y2)), ((x1, y2), (x2, y2)), ((x1, y1), (x1, y2))]: add(a, b, False)
for a, b in H['PARTS']: add(a, b, False)
# garage to house wall
add((78.5, 40), (78.5, 62.5), False); add((78.5, 40), (102.4, 40), False)
UPPER_Z = H['UPPER_Z']

lines = {}
for o, c, a, b, ext in segs:
    lines.setdefault((o, c), []).append([a, b, ext])
merged = []
for (o, c), iv in lines.items():
    # split at all endpoints, mark each piece ext if any ext seg covers it
    pts = sorted(set([p for s in iv for p in s[:2]] + ([107.5] if o == 'h' and c == 46.4 else [])))
    for a, b in zip(pts, pts[1:]):
        cov = [s for s in iv if s[0] <= a + 1e-6 and s[1] >= b - 1e-6]
        if cov: merged.append([o, c, a, b, any(s[2] for s in cov)])
# join adjacent pieces with same ext
merged.sort(key=lambda m: (m[0], m[1], m[2]))
W = []
for m in merged:
    brk = m[0] == 'h' and abs(m[2] - 107.5) < 1e-6
    if W and not brk and W[-1][0] == m[0] and W[-1][1] == m[1] and abs(W[-1][3] - m[2]) < 1e-6 and W[-1][4] == m[4]: W[-1][3] = m[3]
    else: W.append(list(m))

# openings on walls: kind, orient, c, a, b
ops = []
def on(p, q, kind):
    (x1, y1), (x2, y2) = p, q
    if abs(y1 - y2) < 1e-6: ops.append([kind, 'h', y1, min(x1, x2), max(x1, x2)])
    else: ops.append([kind, 'v', x1, min(y1, y2), max(y1, y2)])
for x, y, w, ax, s, hs in H['DOORS']:
    on((x, y), (x + w, y) if ax == 'h' else (x, y + w), 'door')
for p, q in H['OPENINGS']: on(p, q, 'open')
for p, q in H['WINDOWS']: on(p, q, 'win')
for p, q in H['SLIDERS']: on(p, q, 'slider')
for p, q, n, pk in H['GLASSWALLS']: on(p, q, 'glass')
for p, q in H['GARAGE_DOORS']: on(p, q, 'gdoor')
for p, q in H['PASSDOORS']: on(p, q, 'pass')

def ceil(name):
    return {'Living': 12, 'Kitchen': 11, 'Dining': 11, 'Lounge': 11, 'Primary bedroom': 11, 'Office': 10, 'Bedroom 2': 10, 'Bedroom 3': 10,
            'Stairs': 12, 'Garage': round(UPPER_Z - 1.4, 2)}.get(name, 9)
rooms = []
for name, x1, y1, x2, y2, fl, walls, (dx, dy), show in H['ROOMS']:
    rooms.append(dict(n=name, r=[x1, y1, x2, y2], fl=fl, c=ceil(name), lab=[(x1 + x2) / 2 + dx, (y1 + y2) / 2 + dy]))

ROOFS, PLATES = H['ROOFS'], H['PLATES']
def plate_at(x, y):
    best = None
    for x1, y1, x2, y2, p in PLATES:
        if x1 - .05 <= x <= x2 + .05 and y1 - .05 <= y <= y2 + .05: best = max(best or 0, p)
    return best

def room_at(x, y):
    hit = [r for r in rooms if r['r'][0] <= x <= r['r'][2] and r['r'][1] <= y <= r['r'][3]]
    named = [r for r in hit if r['n']]
    return (named or hit or [None])[0]

walls = []
for o, c, a, b, ext in W:
    m = (a + b) / 2
    if ext:
        x, y = (m, c) if o == 'h' else (c, m)
        # garage bump walls are lower (shed roof)
        if x >= 107.4 and 46.3 <= y <= 55.6 and x > 107.6: h = 10.75   # mower bay: under the low side of its shed roof
        else: h = plate_at(x, y) or 10
    else:
        hs = []
        for e in (-.3, .3):
            x, y = (m, c + e) if o == 'h' else (c + e, m)
            r = room_at(x, y)
            if r: hs.append(r['c'])
        h = max(hs or [9])
        x, y = (m, c) if o == 'h' else (c, m)
        if 78.4 <= x <= 107.6 and 39.9 <= y <= 66.6: h = UPPER_Z   # garage/house walls run up to the bonus floor; the bonus walls above are built in the viewer
    if ext and 102.3 <= x <= 107.6 and 39.9 <= y <= 46.5:   # the trash corner sits under the bonus floor: its walls stop at the garage ceiling
        h = 11 if o == 'h' and abs(c - 40) < .05 else round(UPPER_Z - 1.4, 3)
    my = [[k, s, e] for k, oo, cc, s, e in ops if oo == o and abs(cc - c) < .05 and s >= a - .05 and e <= b + .05]
    walls.append(dict(o=o, c=c, a=a, b=b, ext=ext, h=h, ops=my))

# ---- furniture from the sketch SVG
fsvg = H['furniture']()
items = []
stack = [(0, 0, 0)]  # tx, ty, rot about point
tok = re.finditer(r'<(/?)(g|rect|circle|ellipse)([^>]*?)/?>', fsvg)
def attr(s, k):
    m = re.search(r'\b' + k + r'="([^"]*)"', s); return m.group(1) if m else None
for t in tok:
    close, tag, at = t.group(1), t.group(2), t.group(3)
    if tag == 'g':
        if close: stack.pop(); continue
        tr = attr(at, 'transform') or ''
        tx, ty, rot = stack[-1]
        m = re.match(r'translate\(([-\d.]+) ([-\d.]+)\)', tr)
        if m: stack.append((tx + float(m.group(1)), ty + float(m.group(2)), 0)); continue
        m = re.match(r'rotate\(([-\d.]+) ([-\d.]+) ([-\d.]+)\)', tr)
        if m: stack.append((tx, ty, (float(m.group(1)), float(m.group(2)), float(m.group(3))))); continue
        stack.append(stack[-1]); continue
    cls = attr(at, 'class')
    tx, ty, rot = stack[-1]
    def xf(x, y):
        if rot:
            a, cx, cy = rot; ca, sa = math.cos(math.radians(a)), math.sin(math.radians(a))
            x, y = cx + (x - cx) * ca - (y - cy) * sa, cy + (x - cx) * sa + (y - cy) * ca
        return x + tx, y + ty
    if tag == 'rect':
        x, y, w, h = (float(attr(at, k)) for k in ('x', 'y', 'width', 'height'))
        rx = float(attr(at, 'rx') or 0)
        cx, cy = xf(x + w / 2, y + h / 2)
        items.append(dict(t='box', k=cls, c=[round(cx, 2), round(cy, 2)], s=[w, h], rx=rx, a=rot[0] if rot else 0))
    elif tag in ('circle', 'ellipse'):
        cx, cy = float(attr(at, 'cx')), float(attr(at, 'cy'))
        rx = float(attr(at, 'r') or attr(at, 'rx')); ry = float(attr(at, 'r') or attr(at, 'ry'))
        X, Y = xf(cx, cy)
        items.append(dict(t='cyl', k=cls, c=[round(X, 2), round(Y, 2)], s=[rx, ry], a=rot[0] if rot else 0))

def hfor(it):
    k = it['k']; x, y = it['c']; r = room_at(x, y); n = r['n'] if r else ''
    if 52 <= x <= 68 and 10 <= y <= 22: n = 'Outdoor kitchen'
    if 24 <= x <= 52 and (20 <= y <= 34 or 62.5 <= y <= 72): n = 'Porch'
    wet = n in ('Kitchen', 'Scullery', 'Laundry', 'Bath 2', 'Bath 3', 'Powder', 'Primary bath', 'Outdoor kitchen')
    store = n in ('WIC', 'Closet', 'Dressing room', 'Server', '') or (n == 'Garage' and not (x > 102.4 and y < 44))
    if it['t'] == 'cyl':
        if k == 'pl': return ('plant', 0, 6)
        if k == 'fu':
            if it['s'][0] != it['s'][1]: return ('toilet', 0, 1.3)
            if it['s'][0] <= .95: return ('stool', 0, 2.4 if n in ('Kitchen', 'Outdoor kitchen') else 1.6)
            return ('table', 0, 2.5)
        return None
    w, h = it['s']; rx = it['rx']
    if k == 'rug': return ('rug', 0, .04)
    if k == 'car': return ('car', 0, 6.2 if h > 18 else 5.6)
    if k == 'tv': return ('tv', 3.6, 3.6 + max(w, h) * .56)
    if k == 'bk': return ('book', 0, 8)
    if k == 'wet': return ('tub', 0, 1.7)
    if k == 'oh': return ('hood', 6.5, 11) if n == 'Kitchen' else ('shelf', 5.4, 7)
    if k == 'pl2': return None
    if k == 'fu':
        if rx >= .45: return ('soft', 0, 1.5)
        if rx >= .28: return ('bed', 0, 2.1) if min(w, h) >= 4.5 else ('soft', 0, 1.6)
        if rx >= .2: return ('wood', 0, 2.2)
        if store: return ('cab', 0, 7.5)
        if n == 'Garage': return ('cab', 0, 3.4)
        return ('counter', 0, 2.5 if n in ('Office',) else 3)
    if k == 'fu2':
        if wet:
            if abs(w - 2.1) < .01 and abs(h - 3) < .01: return ('fridge', 0, 7.2)
            return ('appl', 0, 3)
        if rx >= .38: return ('soft2', 0, 2.6)
        if rx >= .28: return ('pillow', 2.1, 2.5)
        if store or n == 'Hall': return ('cab', 0, 7.5)
        if n == 'Garage': return ('appl', 7, 8)
        return ('media', 0, 2.2)
    return None
furn = []
for it in items:
    r = hfor(it)
    if r: furn.append(dict(t=it['t'], k=r[0], z0=r[1], z1=r[2], c=it['c'], s=it['s'], a=it['a']))
# kitchen island (drawn as a path in the sketch): 6 ft island with a rounded end toward the living room
furn.append(dict(t='island', k='counter', z0=0, z1=3, c=[58.45, 46.8], s=[5.9, 10.15], a=0))
for x, y, w, h in H['BUILTINS']: furn.append(dict(t='box', k='cab', z0=0, z1=7 if h < 2 else 3.4, c=[x + w / 2, y + h / 2], s=[w, h], rx=0, a=0))

def pond_d():
    D = json.load(open(HP + 'landscape-generator/pond-rev-d.json'))
    cm, bl = G['catmull'], G['blob']
    e = lambda o, seed, k=8, jit=.08: r2(bl(o['center'][0], o['center'][1], o['rx'], o['ry'], seed=seed, k=k, jit=jit, rot=o.get('rot_deg', 0)))
    def pts(v):
        return [tuple(p) for p in v]
    wl = pts(D['wetland_outline'])
    return dict(sw=r2(cm(pts(D['pond_outline']), True, 10)), z5=r2(cm(pts(D['zone_5ft']), True, 10)), z8=e(D['zone_8ft'], 3, 8, .07),
                ledge=D['sun_ledge_12in'], beach=e(D['beach'], 5), cove=e(D['intake_bay'], 2), lily=e(D['lily_cove'], 8, 8, .06),
                wl=r2(wl), up=e(D['wetland_upper_tier'], 4, 9, .07), terr=r2(pts(D['terrace_outline'])), falls=D['falls'],
                fire=D['fire_pit']['center'], jump=D['jump_rock']['center'], jump_r=D['jump_rock']['r'], overlook=D['overlook'],
                bench=D['far_bench'], vault=D['pump_vault'])

# ---- roofs: visible facets of the combined roof, classified edges, gable-end infill
SHELLP = Polygon(H['SHELL'])
TH = roofkit.TH
vis = roofkit.visible(ROOFS)
def rings(g):
    for q in (g.geoms if hasattr(g, 'geoms') else [g]):
        if q.is_empty or q.area < 1e-4: continue
        q = orient(q, sign=-1.0)          # clockwise in plan: the viewer's side walls then face outward
        yield q
facets = []
for r, k, p, g in vis:
    for q in rings(g):
        facets.append(dict(n=r.name, m=r.mat, p=[round(v, 6) for v in p], o=r2(list(q.exterior.coords)[:-1]), h=[r2(list(h.coords)[:-1]) for h in q.interiors]))
def soffit(e):
    # depth from an eave back to the wall, 0 where the eave runs over a porch (the beadboard ceiling covers it)
    mx, my = (e['a'][0] + e['b'][0]) / 2, (e['a'][1] + e['b'][1]) / 2
    for t in [i * .05 for i in range(0, 61)]:
        if SHELLP.buffer(.01).contains(Point(mx - e['n'][0] * t, my - e['n'][1] * t)): return round(t, 2)
    return 0
edges = []
for e in roofkit.edges(ROOFS, vis):
    if e['t'] in ('seam',): continue
    d = dict(t=e['t'], a=[round(v, 3) for v in e['a']], b=[round(v, 3) for v in e['b']], n=[round(v, 4) for v in e['n']], m=vis[e['i']][0].mat, r=vis[e['i']][0].name)
    if e['t'] == 'eave': d['so'] = soffit(e)
    edges.append(d)
DORM = [r for r in ROOFS if r.name == 'Dormer']
def wall_top(x, y):
    if any(r.r[0] - .05 <= x <= r.r[2] + .05 and abs(y - r.r[3]) < .05 for r in DORM): return H['DORMER_PLATE']
    return plate_at(x, y)
gab = []
for gr in roofkit.gables(ROOFS, wall_top):
    gab.append(dict(ax=gr['ax'], a=gr['a'], d=gr['d'], pts=[[round(u, 3), round(b, 3), round(t, 3)] for u, b, t in gr['pts']]))
# ridge roofs (for the gable-end window awnings) and porch sheds (beadboard ceilings and post tops)
ridges = [[*r.r, r.plate, r.ax, list(r.ends)] for r in ROOFS if r.kind == 'ridge' and r.name != 'Dormer']
sheds = []
for r in ROOFS:
    if r.kind != 'shed': continue
    p = r.planes[0][1]
    ceil_ = r.rect.difference(SHELLP.buffer(.3))
    sheds.append(dict(n=r.name, r=list(r.r), p=list(p), ceil=[r2(list(q.exterior.coords)[:-1]) for q in rings(ceil_) if q.area > 2]))
# bonus room ceiling: the garage roof's own planes over the bonus floor, below the deck
GR = next(r for r in ROOFS if r.name == 'Garage')
bonus_ceil = []
for k, p, poly in GR.facets():
    q = poly.intersection(sbox(78.8, 40.3, 107.2, 66.2))
    for qq in rings(q): bonus_ceil.append(dict(p=list(p), o=r2(list(qq.exterior.coords)[:-1])))
for D_ in DORM:
    for k, p, poly in D_.facets():
        q = poly.intersection(sbox(D_.r[0] + .3, H['DORMER_Y'], D_.r[2] - .3, 66.2))
        for qq in rings(q): bonus_ceil.append(dict(p=list(p), o=r2(list(qq.exterior.coords)[:-1])))
roof = dict(facets=facets, edges=edges, gables=gab, ridges=ridges, sheds=sheds, bonus=bonus_ceil, TH=TH, LIFT=roofkit.LIFT,
            dormers=[[r.r[0], r.r[2], H['DORMER_PLATE']] for r in DORM], dormer_y=H['DORMER_Y'], beams=H['BEAMS'], stoop=H['STOOP'],
            passdoors=H['PASSDOORS'], upper_z=UPPER_Z, risers=H['RISERS'], run1=H['RUN1'], landing=H['LANDING'], run2=H['RUN2'],
            up_windows=H['UP_WINDOWS'])

data = dict(
    shell=r2(H['SHELL']), rooms=rooms, walls=walls, roof=roof,
    porches=[dict(n=n, p=r2(p)) for n, p, _ in H['PORCHES'] if p], posts=H['POSTS'], furn=furn,
    fire=H['FIREPLACES'], gen=H['GENPAD'], upper=H['UPPER_SHELL'],
    pond=pond_d(),
    pond_c=dict(sw=r2(G['LSW']), z5=r2(G['LZ5']), z8=r2(G['LZ8']), ledge=G['LEDGE'], beach=r2(G['LBEACH']), cove=r2(G['LCOVE']),
              lily=r2(G['LILY']), wl=r2(G['L_WL']), up=r2(G['L_UP']), terr=r2(G['TERR_L']), fire=G['FIRE'], jump=G['JUMP'], vault=G['VAULT']),
)
json.dump(data, open(OUT, 'w'), separators=(',', ':'))
print('walls', len(walls), 'furn', len(furn), 'bytes', len(json.dumps(data)))
