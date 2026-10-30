"""Pond shape options page."""
import runpy, sys, math, random, re
sys.path.insert(0, '.')
T = '/root/.claude/skills/synced/cc9f2c1b-608a-4e06-a091-ff5bdc1b22f3_d99a4251-bdde-4476-9656-a75eb0a5b2ff/house-styles/assets/ink-and-brass.html'
OUT = sys.argv[1] if len(sys.argv) > 1 else '/mnt/project-files/home-plan/pond-shape-options.html'
sys.argv = ['plan.py', '/tmp/claude-0/-home-claude/f3cf1ba0-f40f-523c-aebf-e0d5cf75208d/scratchpad/_tmp.html', T]
H = runpy.run_path('../plan.py')
import yard as Y
from geo import *
from css import CSS

def rects(rs):
    return [lambda p, r=r: r[0] < p[0] < r[2] and r[1] < p[1] < r[3] for r in rs]

def falls(x1, y1, x2, y2, w, seed):
    rg = random.Random(seed)
    dx, dy = x2 - x1, y2 - y1; L = math.hypot(dx, dy); ux, uy = dx / L, dy / L; nx, ny = -uy, ux
    a = (x1 + nx * w / 2, y1 + ny * w / 2); b = (x1 - nx * w / 2, y1 - ny * w / 2)
    c = (x2 - nx * w * .6, y2 - ny * w * .6); d_ = (x2 + nx * w * .6, y2 + ny * w * .6)
    s = [f'<polygon class="w1" points="{" ".join(f"{p[0]:.2f},{p[1]:.2f}" for p in (a, b, c, d_))}"/>']
    for i in range(int(w / .7) + 1):
        t = -w / 2 + .35 + i * .7
        if t > w / 2: break
        sx, sy = x1 + nx * t, y1 + ny * t; ex, ey = x2 + nx * t * 1.15, y2 + ny * t * 1.15
        s.append(f'<path class="foam" d="M{sx:.2f},{sy:.2f} L{ex:.2f},{ey:.2f}"/>')
    s.append(rock(x1 - ux * .9, y1 - uy * .9, w * .5, rg, flat=True, cls="slab"))
    for sg in (1, -1):
        s.append(rock(x1 + nx * sg * (w / 2 + 1.6), y1 + ny * sg * (w / 2 + 1.6), rg.uniform(1.8, 2.4), rg))
        s.append(rock(x2 + nx * sg * (w / 2 + 1.8) - ux * .6, y2 + ny * sg * (w / 2 + 1.8) - uy * .6, rg.uniform(2.0, 2.6), rg))
    ang = math.degrees(math.atan2(ny, nx))
    s.append(f'<ellipse class="foamb" cx="{x2 + ux * .4:.2f}" cy="{y2 + uy * .4:.2f}" rx="{w * .6:.2f}" ry=".9" transform="rotate({ang:.1f} {x2 + ux * .4:.2f} {y2 + uy * .4:.2f})"/>')
    return "".join(s)

def wetland(WL, seed, pockets=()):
    s = [f'<path class="berm" d="{d(offset(WL, 5))}"/>', f'<path fill="url(#grav)" class="wlb" d="{d(WL)}"/>']
    for bx, by, rx, ry in pockets:
        s.append(f'<path class="w1" d="{d(blob(bx, by, rx, ry, seed=int(bx * 3), k=7))}"/>')
    pr = random.Random(seed)
    xs = [p[0] for p in WL]; ys = [p[1] for p in WL]
    for j in range(int(area(WL) * .5)):
        x, y = pr.uniform(min(xs), max(xs)), pr.uniform(min(ys), max(ys))
        if Y.inside((x, y), WL):
            k = pr.random()
            if k < .45: s.append(tuft(x, y, pr.uniform(.8, 1.3), "tf"))
            elif k < .7: s.append(tuft(x, y, pr.uniform(.9, 1.4), "tf2"))
            elif k < .85: s.append(f'<circle class="pk" cx="{x:.2f}" cy="{y:.2f}" r=".55"/><circle class="pkf" cx="{x:.2f}" cy="{y - .1:.2f}" r=".22"/>')
            else: s.append(f'<circle class="ir" cx="{x:.2f}" cy="{y:.2f}" r=".5"/>')
    return "".join(s)

def stream(c, w0, w1, seed, skip=()):
    poly, line = ribbon(c, w0, w1)
    s = [f'<path class="w1" d="{d(poly)}"/>']
    for t in (0.3, 0.62):
        i = int(t * (len(line) - 1)); (xa, ya), (xb, yb) = line[i - 1], line[i + 1]
        L = math.hypot(xb - xa, yb - ya); nx, ny = -(yb - ya) / L, (xb - xa) / L; x, y = line[i]
        s.append(f'<path class="foam2" d="M{x - nx * 1.4:.2f},{y - ny * 1.4:.2f} L{x + nx * 1.4:.2f},{y + ny * 1.4:.2f}"/>')
    s.append(Y.edge_rocks(offset(poly, .1), 2.1, .6, 1.3, .55, list(skip), seed))
    return "".join(s)

def slab_edge(poly, seed, skip=()):
    rg = random.Random(seed); sg = 1 if signed(poly) > 0 else -1; out = []
    n = len(poly)
    for i in range(n):
        (x1, y1), (x2, y2) = poly[i], poly[(i + 1) % n]
        L = math.hypot(x2 - x1, y2 - y1); ux, uy = (x2 - x1) / L, (y2 - y1) / L; nx, ny = uy * sg, -ux * sg
        t = 0
        while t < L - .5:
            ln = min(rg.uniform(2.4, 4.2), L - t); dep = rg.uniform(1.4, 2.1)
            cx, cy = x1 + ux * (t + ln / 2), y1 + uy * (t + ln / 2)
            if not any(f((cx, cy)) for f in skip):
                ox, oy = cx + nx * (dep / 2 - .25), cy + ny * (dep / 2 - .25)
                ang = math.degrees(math.atan2(uy, ux))
                out.append(f'<g transform="rotate({ang:.1f} {ox:.2f} {oy:.2f})"><rect class="shd" x="{ox - ln / 2 + .25:.2f}" y="{oy - dep / 2 + .3:.2f}" width="{ln - .15:.2f}" height="{dep:.2f}" rx=".2"/>'
                           f'<rect class="{rg.choice(["slab", "st3", "slab"])}" x="{ox - ln / 2:.2f}" y="{oy - dep / 2:.2f}" width="{ln - .15:.2f}" height="{dep:.2f}" rx=".2"/></g>')
            t += ln
    return "".join(out)

def deck(x, y, w, h):
    return (f'<rect class="deck" x="{x}" y="{y}" width="{w}" height="{h}"/>' + "".join(f'<line class="board" x1="{x + i * .6:.2f}" x2="{x + i * .6:.2f}" y1="{y}" y2="{y + h}"/>' for i in range(1, int(w / .6))) +
            f'<rect class="fu" x="{x + 1.4}" y="{y + 1.2}" width="2.3" height="6" rx=".4"/><rect class="fu" x="{x + 4.6}" y="{y + 1.2}" width="2.3" height="6" rx=".4"/>')

def steps(x, y, w, n=3, dy=-2.3):
    s = []
    for k in range(n):
        yy = y + k * dy
        s.append(f'<rect class="slab" x="{x + k * .4}" y="{yy + dy:.2f}" width="{w - k * .8}" height="{-dy:.2f}" rx=".2"/>')
        if k: s.append(f'<rect class="w1" opacity="{.25 * k + .05}" x="{x + k * .4}" y="{yy + dy:.2f}" width="{w - k * .8}" height="{-dy:.2f}"/>')
    return "".join(s)

def pond_water(SW, Z5, Z8, beach=None, bay=None, poly=False):
    P = SW
    s = [f'<path class="w1" d="{d(P)}"/>']
    if bay: s.append(f'<path class="w1" d="{d(bay)}"/>')
    if beach: s.append(f'<path fill="url(#grav)" d="{d(beach)}"/>')
    s.append(f'<path class="tint" d="{d(P)}"/>')
    s.append(f'<path class="w2" d="{d(Z5)}"/><path fill="url(#gDeep)" d="{d(Z8)}"/>')
    rg = random.Random(len(P))
    xs = [p[0] for p in Z5]; ys = [p[1] for p in Z5]
    for i in range(24):
        x, y = rg.uniform(min(xs), max(xs)), rg.uniform(min(ys), max(ys))
        if Y.inside((x, y), Z5): s.append(f'<path class="rip" d="M{x:.2f},{y:.2f} q1.2,-.5 2.4,0"/>')
    return "".join(s)

def L(x, y, t, cls="lt2"): return f'<text class="{cls}" x="{x}" y="{y}">{t}</text>'

VB = (-18, -96, 120, 112)

def frame(inner, labels, aria):
    x, y, w, h = VB
    terr = Y.flagstones((8, -12, 84, 22), 2.5, "cTerr", 4)
    return (f'<svg class="plan ls zoom opt" viewBox="{x} {y} {w} {h}" role="img" aria-label="{aria}">{Y.defs()}'
            f'<rect fill="url(#lawn)" x="{x}" y="{y}" width="{w}" height="{h}"/>'
            f'<path class="grout" d="{d(Y.TERRACE)}"/>{terr}{inner}{H["building"]("sk")}{labels}'
            f'<g class="scale"><rect x="-16" y="-93" width="5" height=".55"/><rect class="o" x="-11" y="-93" width="5" height=".55"/><rect x="-6" y="-93" width="10" height=".55"/>'
            f'<text x="-16" y="-90.6">0</text><text x="-11" y="-90.6">5</text><text x="-6" y="-90.6">10</text><text x="2" y="-90.6">20 ft</text></g></svg>')

STATS = {}
def gal(SW, Z5, Z8, extra=0):
    return ((area(SW) - area(Z5)) * 2 + (area(Z5) - area(Z8)) * 5 + area(Z8) * 8 + extra) * 7.48

# ---------------------------------------------------------------- 0. current
def opt_current():
    s = [wetland(Y.WL_REVB, 9, ((33, -60, 2.6, 1.4), (50, -58.2, 2.2, 1.2))), stream(Y.STREAM_C, 2.4, 3.6, 32, rects([(-99, -29.5, 999, 99), (-99, -999, 999, -60)])),
         pond_water(Y.SW, Y.Z5, Y.Z8, Y.BEACH, Y.BAY), steps(36.4, -8.1, 8.2), Y.edge_rocks(Y.SW, 2.15, .85, 1.75, .45, Y.SKIP_POND, 51),
         falls(41.2, -52.2, 41.2, -45.6, 5.4, 3), rock(26.6, -41.8, 3.3, random.Random(77), flat=True, cls="slab"), deck(46.4, -15.2, 10.8, 10.8),
         tree(19.6, -52, 4.4, "maple", 1) + tree(57.6, -50.4, 3, "maple", 2)]
    STATS['current'] = (area(Y.SW), area(Y.WL_REVB), gal(Y.SW, Y.Z5, Y.Z8))
    return frame("".join(s), L(41, -25, "Swim", "lt") + L(42, -60, "Wetland"), "Current round pond for comparison.")

# ---------------------------------------------------------------- 1. island lagoon
def opt_island():
    Q = [(14, -12), (24, -8.5), (36, -9.6), (46, -9.2), (56, -8.6), (66, -10.2), (74, -14), (80, -22), (82.4, -32), (79, -41.4), (73, -47.6), (64, -51), (56, -56.4),
         (46, -59.6), (36, -63), (28, -64), (20, -61), (12.6, -55), (8.4, -45.4), (8.2, -35), (10.4, -26.6), (15.4, -21), (12.4, -16.6)]
    SW = catmull(Q, True, 10)
    Z5 = catmull([(22, -17), (36, -15), (56, -14.2), (70, -19), (75.4, -30), (71, -41.4), (59, -46.4), (45, -51.6), (31, -55.6), (19.6, -51), (14.6, -39), (15.6, -27)], True, 10)
    Z8 = blob(26, -48, 6.2, 4.4, seed=5, k=8, jit=.08, rot=-30)
    ISL = blob(53, -32, 8.4, 5.2, seed=12, k=9, jit=.12, rot=-14)
    WL = blob(36, -80, 31, 10.4, seed=21, k=10, jit=.08)
    beach = blob(17.4, -12.4, 7, 4, seed=5, k=8, jit=.08, rot=-20); bay = blob(77, -10.4, 3.6, 2.8, seed=2, k=8, jit=.08, rot=20)
    skip = rects([(-99, -16, 30, 99), (35, -14, 46, 99), (55, -16, 68, 99), (71, -16, 76, 99), (23, -70, 33, -59), (15, -63, 23, -54), (74, -46, 84, -37)])
    s = [wetland(WL, 7, ((20, -81, 3, 1.5), (46, -79, 2.8, 1.4), (34, -84, 2.2, 1.1))), stream([(64, -78), (72, -72.6), (78.6, -65), (82.4, -56), (83, -48), (80.4, -41.6)], 2.4, 3.6, 33, rects([(-99, -42, 999, 99), (-99, -999, 999, -77)])),
         pond_water(SW, Z5, Z8, beach, bay), f'<path class="berm" d="{d(ISL)}"/>', Y.edge_rocks(ISL, 1.9, .8, 1.5, .3, [], 61),
         tree(53.6, -32.6, 3.4, "maple", 8), steps(36, -9.4, 8.6), Y.edge_rocks(SW, 2.2, .85, 1.8, .45, skip, 52),
         falls(28.2, -69, 28.2, -62.4, 6, 4), rock(19.4, -58.4, 3.4, random.Random(5), flat=True, cls="slab"), deck(56, -16.4, 11, 11.6),
         "".join(lily(x, y, r, a) for x, y, r, a in ((60.6, -28, .8, 10), (61.8, -30.4, .7, 150), (45.4, -35, .7, 80), (46.4, -37.4, .65, 220))) + '<circle class="lf" cx="61" cy="-29" r=".3"/>',
         tree(9, -62, 4.2, "maple", 3) + tree(88.6, -62, 4.4, "birch", 4)]
    STATS['island'] = (area(SW) - area(ISL), area(WL), gal(SW, Z5, Z8))
    lab = L(36, -30, "Swim", "lt") + L(53, -26.4, "Island") + L(36, -80, "Wetland") + L(17.4, -6.6, "Beach") + L(28, -69.8, "Falls") + L(86.6, -51, "Stream")
    return frame("".join(s), lab, "Island lagoon option: a large irregular pond with a planted boulder island, beach, falls and stream.")

# ---------------------------------------------------------------- 2. bayou bend
def opt_bayou():
    C = [(2, -4), (1.4, -20), (8, -35), (22, -47.6), (42, -53.4), (62, -49), (77.4, -38), (84.6, -22), (85, -6)]
    SW, line = ribbon(C, 17.5)
    SW = catmull(SW[::3], True, 3)
    Z5 = ribbon(C[1:-1], 8.6)[0]
    Z8 = blob(42, -53, 7, 3.6, seed=4, k=8, jit=.06, rot=4)
    WL = blob(42, -79.4, 27.6, 9.2, seed=31, k=10, jit=.08)
    PEN = [(13.6, -6), (14, -18), (20, -30), (32, -38.6), (46, -41.6), (60, -38.4), (70, -30), (74.4, -18), (74.4, -6)]
    s = [wetland(WL, 8, ((28, -80, 2.8, 1.4), (55, -78.6, 2.6, 1.3))), pond_water(SW, Z5, Z8, blob(2.4, -6, 6.6, 3.6, seed=9, k=8, jit=.06)),
         Y.edge_rocks(SW, 2.3, .8, 1.6, .45, rects([(-8, -12, 9, 99), (76, -12, 95, 99), (36, -50, 48, -36), (-12, -30, 16, -23)]), 53),
         falls(42, -69.6, 42, -62.6, 6, 5), steps(38.6, -38.6, 7.6, 2, -2.2)]
    fx, fy = 44, -26
    s.append(f'<circle class="fg2" cx="{fx}" cy="{fy}" r="6.4"/><circle class="st2" cx="{fx}" cy="{fy}" r="1.9"/><circle class="pit" cx="{fx}" cy="{fy}" r="1.3"/><circle class="fire" cx="{fx}" cy="{fy}" r=".7"/>')
    for k in range(6):
        a = math.radians(k * 60 + 30); s.append(Y.chair_ad(fx + 4.4 * math.cos(a), fy + 4.4 * math.sin(a), math.degrees(a) - 90))
    s.append('<rect class="deck" x="-9" y="-28.6" width="24" height="3.4"/>' + "".join(f'<line class="board" x1="{-9 + i * .7:.2f}" x2="{-9 + i * .7:.2f}" y1="-28.6" y2="-25.2"/>' for i in range(1, 34)))
    s.append(deck(78.6, -16.6, 11, 11.2))
    s.append(rock(62, -59.6, 3.2, random.Random(7), flat=True, cls="slab"))
    for x, y in ((10, -54), (18, -61.4), (70, -59), (78, -52), (90, -40), (-8, -42)):
        s.append(tree(x, y, 3.2, "birch", int(x * 7)) + "".join(f'<circle class="ttr" cx="{x + 2.6 * math.cos(t):.2f}" cy="{y + 2.6 * math.sin(t):.2f}" r=".35"/>' for t in (0.4, 2.2, 3.9, 5.3)))
    s.append("".join(lily(x, y, r, a) for x, y, r, a in ((80.6, -28, .8, 10), (82, -31, .7, 150), (6, -30, .7, 80), (5.2, -33.4, .65, 220))))
    STATS['bayou'] = (area(SW), area(WL), gal(SW, Z5, Z8))
    lab = L(44, -17.4, "Fire pit peninsula") + L(22, -46.4, "Swim", "lt") + L(42, -80, "Wetland") + L(3, -30.4, "Boardwalk") + L(2.8, -1.6, "Beach") + L(84, -3, "Deck") + L(20, -64.6, "Cypress")
    return frame("".join(s), lab, "Bayou bend option: a crescent of water wraps a fire pit peninsula off the terrace, with cypress trees, a boardwalk and a waterfall at the back.")

# ---------------------------------------------------------------- 3. quarry
def opt_quarry():
    SW = [(16, -9), (50, -9), (50, -13), (66, -13), (69, -30), (67.6, -44), (56, -51.4), (30, -51.4), (19, -46), (15, -30)]
    Z5 = offset([(24, -17.6), (48, -17.6), (60, -19), (62.4, -31), (60.6, -42), (52, -45.6), (31, -45.6), (23.6, -40), (21.4, -28)], 0)
    Z8 = [(48, -36.6), (61.6, -36.4), (60.6, -44.4), (54, -47.6), (46.6, -47.6), (45.6, -41)]
    WL = blob(42, -72.6, 23.6, 8.6, seed=41, k=10, jit=.08)
    ledge = [(16.2, -9.2), (31, -9.2), (31, -17.4), (16.6, -17.4)]
    s = [wetland(WL, 6, ((30, -73, 2.6, 1.3), (54, -72, 2.4, 1.2))), f'<path class="w1" d="{d(SW)}"/>', f'<path class="slab" opacity=".55" d="{d(ledge)}"/>',
         f'<path class="tint" d="{d(SW)}"/><path class="w2" d="{d(Z5)}"/><path fill="url(#gDeep)" d="{d(Z8)}"/>']
    s.append(slab_edge(SW, 71, rects([(34, -12, 46, 99), (28, -56, 50, -48)])))
    s.append(steps(34.2, -8.2, 11, 3))
    # sheet waterfall over a stacked-stone wall
    s.append('<rect class="st2" x="27" y="-57.4" width="24" height="5.6" rx=".3"/>' + "".join(f'<line class="board" x1="27" x2="51" y1="{-57.4 + k * 1.1:.2f}" y2="{-57.4 + k * 1.1:.2f}"/>' for k in range(1, 5)))
    s.append('<rect class="w1" x="32" y="-57.6" width="14" height="6.2"/>' + "".join(f'<path class="foam" d="M{32.4 + i * .7:.2f},-57.4 L{32.4 + i * .7:.2f},-51.6"/>' for i in range(20)))
    s.append('<ellipse class="foamb" cx="39" cy="-50.6" rx="7.6" ry="1.1"/>')
    s.append('<rect class="st2" x="58" y="-56" width="12" height="7" rx=".4"/><rect class="slab" x="59" y="-55.2" width="10" height="5.6" rx=".3"/>')
    s.append(deck(50.4, -13, 15.6, 9.2) + tree(18, -58, 4.2, "maple", 2) + tree(74, -60, 3.6, "maple", 6))
    s.append("".join(lily(x, y, r, a) for x, y, r, a in ((19.4, -22, .8, 10), (18.2, -25.6, .7, 150), (19.6, -40, .7, 80))))
    STATS['quarry'] = (area(SW), area(WL), gal(SW, Z5, Z8))
    lab = L(42, -28, "Swim", "lt") + L(23.6, -12.4, "Sun ledge") + L(39, -60.6, "Sheet falls") + L(64, -57.6, "Cliff jump") + L(42, -74.4, "Wetland")
    return frame("".join(s), lab, "Quarry option: crisp stone-slab edges, a sun ledge, a sheet waterfall over a stacked stone wall and a cliff jump.")

# ---------------------------------------------------------------- 4. two-pool cascade
def opt_cascade():
    Q = [(26, -10), (40, -9.5), (54, -9), (66, -11.6), (73, -18), (71.6, -25.4), (63, -30.6), (53, -35.6), (45, -41), (37, -47), (28.6, -49.4), (21, -46), (17.6, -38), (18.6, -28), (21.2, -18)]
    SW = catmull(Q, True, 10)
    Z5 = catmull([(30, -16), (48, -14.6), (63, -16.6), (65, -21.6), (56, -27.6), (45, -33.6), (36, -40.4), (28, -42), (24.4, -35), (25.4, -24)], True, 10)
    Z8 = blob(29.6, -38.4, 5, 3.6, seed=3, k=8, jit=.06, rot=-40)
    UP = blob(15.6, -59, 7.4, 5.4, seed=17, k=9, jit=.08, rot=-10)
    WL = blob(42, -76.4, 23.4, 8, seed=51, k=10, jit=.08)
    s = [wetland(WL, 5, ((32, -77, 2.4, 1.2), (52, -76, 2.4, 1.2))), stream([(62, -73.6), (67, -67), (69.6, -57), (68, -46), (62.6, -36.4), (57.6, -33.6)], 2.2, 3.4, 34, rects([(-99, -34.4, 999, 99), (-99, -999, 999, -72.6)])),
         f'<path class="w1" d="{d(UP)}"/><path class="w2" d="{d(offset(UP, -2))}"/>', Y.edge_rocks(UP, 2.0, .8, 1.5, .45, rects([(8, -56, 26, -52), (16, -68, 26, -62)]), 62),
         pond_water(SW, Z5, Z8, None, blob(70, -10.8, 3.4, 2.6, seed=2, k=8, jit=.08)), steps(34, -9.4, 9),
         Y.edge_rocks(SW, 2.2, .85, 1.8, .45, rects([(32, -14, 44, 99), (46, -16, 58, 99), (14, -52, 26, -44), (54, -38, 61, -31)]), 54),
         falls(24, -69.4, 19.6, -62.6, 4.4, 6), falls(18.2, -53.6, 22.6, -47.4, 6.4, 7), deck(46.4, -16, 11, 11.6),
         rock(36.4, -50.4, 3.2, random.Random(9), flat=True, cls="slab"), tree(5, -50, 4.2, "maple", 3) + tree(32, -60.4, 3.2, "maple", 4) + tree(78, -50, 4.4, "birch", 5)]
    up_gal = (area(UP) * 3.5) * 7.48
    STATS['cascade'] = (area(SW) + area(UP), area(WL), gal(SW, Z5, Z8) + up_gal)
    lab = L(44, -24, "Swim", "lt") + L(15.6, -57, "Upper soaking pool") + L(44, -77, "Wetland") + L(66, -46.6, "Stream") + L(28.6, -50.8, "Rock dam falls")
    return frame("".join(s), lab, "Two-pool cascade option: an upper soaking pool spills over a rock dam into a long diagonal swim pond, with a stream on the right.")

figs = [("current", opt_current()), ("island", opt_island()), ("bayou", opt_bayou()), ("quarry", opt_quarry()), ("cascade", opt_cascade())]
F = dict(figs)
def st(k):
    a, w, g = STATS[k]; return a, w, g

INFO = {
 "island": ("A. Island lagoon", "The biggest and most natural: a wide, scalloped lagoon around a planted boulder island with a small maple. You swim laps around the island. The beach, steps and deck stay on the near shore, the falls sit back-left over the deep end, and a long stream comes down the right side."),
 "bayou": ("B. Bayou bend", "The most Louisiana: a crescent of water wraps a fire-pit peninsula off the terrace, so you sit with water on three sides. Bald cypress and a boardwalk across the left arm give it a bayou feel. Swim the whole arc; the falls and deep end are at the back of the bend."),
 "quarry": ("C. Quarry", "The least round: crisp edges of big flat stone slabs, like an old swimming hole in a quarry. A wide sheet waterfall pours off a stacked stone wall, a high flat rock at the back right is the cliff jump, and a shallow stone sun ledge sits in the front corner."),
 "cascade": ("D. Two-pool cascade", "A long, diagonal swim pond with a smaller upper soaking pool tucked at the back left. The wetland feeds the upper pool, which spills over a rock dam into the deep end. A stream comes down the right. The upper pool could be heated later as a natural hot tub."),
}

tpl = open(T).read()
head, rest = tpl.split('<main class="doc">')
head = head.replace('<title>Ink & Brass template</title>', '<title>Pond shape options</title>')
head = re.sub(r'<!-- House style: Ink & Brass.*?-->\n', '', head)
head = head.replace('</style>', H['CSS'] + CSS + '.d-opt{margin:30px 0 0}.d-opt h3{margin:0 0 6px;font:600 1.25em/1.3 var(--f-head)}.d-opt p{margin:0 0 12px}.plan.opt{margin-top:4px}.d-minis.two figure figcaption b{margin-bottom:2px}</style>')
rows = ""
for k, (name, _) in INFO.items():
    a, w, g = st(k)
    rows += f'<tr><td>{name}</td><td class="num">{a:,.0f}</td><td class="num">{w:,.0f} ({w / a:.0%})</td><td class="num">{round(g, -3):,.0f}</td></tr>'
a, w, g = st('current')
rows = f'<tr><td>Current (rev. B)</td><td class="num">{a:,.0f}</td><td class="num">{w:,.0f} ({w / a:.0%})</td><td class="num">{round(g, -3):,.0f}</td></tr>' + rows
opts = "".join(f'<section class="d-opt"><h3>{INFO[k][0]}</h3><p class="d-p">{INFO[k][1]}</p><figure class="d-fig wide">{F[k]}</figure></section>' for k in INFO)
body = f"""<main class="doc">
  <header class="d-head">
    <div class="d-top"><span class="d-type">New home build</span><span class="d-date">Pond shapes · Oct 26, 2026</span></div>
    <h1 class="d-title">Four pond shapes to compare</h1>
    <p class="d-lead">Each option keeps what works in the current plan: the terrace, the living room view, a way in for kids and adults, a wetland filter at least 30% of the water, external pumps at the near end and the falls at the far end. What changes is the shape and the mood. All are drawn at the same scale as the house.</p>
  </header>
  <h2 class="d-h2">The current shape</h2>
  <p class="d-note">For comparison: the round pond from the landscape plan.</p>
  <figure class="d-fig wide">{F['current']}</figure>
  <h2 class="d-h2">Options</h2>
  {opts}
  <h2 class="d-h2">Side by side</h2>
  <p class="d-note">Water area includes shelves and beaches. Gallons are rough, from the drawn depth zones.</p>
  <div class="d-tw"><table>
    <thead><tr><th>Shape</th><th class="num">Water, sf</th><th class="num">Wetland, sf</th><th class="num">Gallons</th></tr></thead>
    <tbody>{rows}</tbody>
  </table></div>
  <dl class="d-rows" style="margin-top:22px">
    <dt>Cost</dt><dd>Cost follows water area and stone. The quarry uses the most cut slab and costs the most per square foot. The island lagoon and bayou bend are the most water. The cascade adds a second pool and a second falls.</dd>
    <dt>Mix and match</dt><dd>The pieces trade freely. The bayou's fire-pit peninsula, the quarry's sheet falls, or the cascade's upper soaking pool can go on any of the other shapes.</dd>
  </dl>
  <footer class="d-foot">Concept sketches for choosing a direction. The chosen shape goes back into the full landscape plan with its plantings, lighting and section.</footer>
</main>"""
open(OUT, 'w').write(head + body + '\n</body>\n</html>\n')
for k in STATS: print(k, [round(v) for v in STATS[k]])
