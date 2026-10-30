"""Landscape drawing: site plan and rec pond close-up. Feet; x left->right, y back (pond) -> front (street)."""
import math, random
from geo import *

R = random.Random(7)
# ---------------------------------------------------------------- pond geometry
Q = [(23, -10), (30, -8.5), (36, -9.5), (44, -9.5), (50, -8.6), (56, -9.8), (60, -13), (61.5, -17), (63.5, -20), (67, -22.6), (68, -27.6),
     (65, -31.2), (61.4, -31.4), (60.6, -35), (57, -39.5), (51, -41.6), (46.2, -42.2), (44.6, -45.6), (41, -47.2), (37.4, -45.8), (35.6, -42.6),
     (30, -42), (25.5, -39.5), (22, -35), (19.5, -29), (20, -23), (23.6, -19.4), (21, -16.8), (18, -14.4), (18.8, -11)]
SW = catmull(Q, True, 10)
Z5 = catmull([(28, -17), (38, -14.2), (48, -13.6), (55, -16), (57.4, -24), (55.2, -33), (48, -37.4), (38, -38.4), (29.4, -36), (24.8, -29.4), (25.6, -22)], True, 10)
Z8 = blob(32.4, -32.6, 6.2, 4.2, seed=3, k=8, jit=.08, rot=-28)
WL_REVB = blob(42, -59.6, 20.6, 8.4, seed=11, k=10, jit=.1)   # rev. B oval wetland, kept for the comparison pages
# rev. C wetland: a two-tier crescent that forms the pond's back shore (option A of the wetland study)
_o = offset(SW, 1.1)
WL_INNER = [_o[i] for i, p in enumerate(SW) if 31 <= p[0] <= 66 and p[1] <= -31]       # 1 ft stone lip, right to left
WL_OUTER = catmull([(31.2, -45.6), (30.4, -50.6), (33.6, -56.4), (40, -60.4), (47.6, -61.4), (55.4, -58.4), (61.6, -53), (66.6, -46.4),
                    (70.4, -39.4), (71.2, -33.4), (68.6, -30.4)], False, 8)
WL = WL_OUTER + WL_INNER
WL_UP = blob(42.2, -54.6, 8.6, 4.6, seed=4, k=9, jit=.07, rot=-4)                       # upper tier, +3.5 ft, feeds the falls
WL_LIP = [p for p in WL_INNER if p[0] > 48]                                             # lower tier lip, about 1 ft above the water
BERM = offset(WL, 6)
BEACH = blob(24.6, -11.2, 7.0, 4.0, seed=5, k=8, jit=.08, rot=-22)
BAY = blob(63.2, -9.0, 3.6, 2.8, seed=2, k=8, jit=.08, rot=25)
STREAM_C = [(61, -61), (67.4, -59.4), (72.4, -53.6), (74.2, -45.6), (73.6, -37.6), (70.4, -31.4), (66.2, -27.2)]
STREAM, STREAM_LINE = ribbon(STREAM_C, 2.4, 3.6)
FIRE = (6, -26)
OVER = (42, -76.4)

A_SW, A5, A8, A_WL = area(SW), area(Z5), area(Z8), area(WL)
GAL = ((A_SW - A5) * 2.0 + (A5 - A8) * 5 + A8 * 8) * 7.48

TERR_OUT = [(81.6, -0.4), (79, -2.6), (72, -4.4), (64, -5.1), (57, -4.6), (46.4, -4.6), (45, -8.0), (36, -8.0), (33.5, -6.2),
            (28.5, -5.6), (22, -5.2), (16, -2.2), (12, 3), (10.6, 8), (12, 13)]
TERRACE = [(12, 13), (24, 13), (24, 20), (46, 20), (46, 10), (68, 10), (68, 5), (81.6, 5)] + catmull(TERR_OUT, False, 6)

PATH_L = [(13.6, 6.6), (10.8, -3), (8.6, -12), (7.2, -17.6)]
PATH_LOOP = [(5, -34.4), (6.6, -43), (11, -54), (17.6, -64), (26.6, -71.4), (36.2, -75.4)]
PATH_LOOP2 = [(47.8, -75.4), (57, -72.8), (66.6, -67.4), (75.4, -59.8), (80.4, -50), (81.4, -39), (79.6, -28.4), (76.4, -19.4), (73.4, -8)]
PATH_SIDE = [(-13, 74), (-14, 56), (-13, 36), (-11.2, 19), (-5, 9.6), (4, 5.4), (10.8, 5.2)]
PATH_PRIM = [(109, 15.6), (110.4, 6), (112, -3), (109.6, -9.6), (104.6, -14.2), (99.6, -13.6)]
LOT = (-34, -116, 152, 93)


def inside(pt, poly):
    x, y = pt; c = False; n = len(poly)
    for i in range(n):
        x1, y1 = poly[i]; x2, y2 = poly[(i + 1) % n]
        if (y1 > y) != (y2 > y) and x < (x2 - x1) * (y - y1) / (y2 - y1) + x1:
            c = not c
    return c


def defs():
    rg = random.Random(3)
    grav = "".join(f'<circle cx="{rg.uniform(0, 2):.2f}" cy="{rg.uniform(0, 2):.2f}" r="{rg.uniform(.07, .16):.2f}" fill="{rg.choice(["#BBAE95", "#EEE7D7", "#A3967D", "#CFC3AA"])}"/>' for _ in range(22))
    mead = "".join(f'<circle cx="{rg.uniform(0, 6):.2f}" cy="{rg.uniform(0, 6):.2f}" r="{rg.uniform(.12, .24):.2f}" fill="{rg.choice(["#E3BE4E", "#C27FB0", "#8FB0D6", "#FFFFFF", "#9DB86B", "#9DB86B"])}"/>' for _ in range(26))
    return f'''<defs>
<pattern id="grav" width="2" height="2" patternUnits="userSpaceOnUse"><rect width="2" height="2" fill="#D9CDB3"/>{grav}</pattern>
<pattern id="mead" width="6" height="6" patternUnits="userSpaceOnUse"><rect width="6" height="6" fill="#D3DDAA"/>{mead}</pattern>
<pattern id="lawn" width="12" height="12" patternUnits="userSpaceOnUse"><rect width="12" height="12" fill="#C8DAA2"/><rect width="6" height="12" fill="#C1D59A"/></pattern>
<pattern id="moss" width="3" height="3" patternUnits="userSpaceOnUse"><rect width="3" height="3" fill="#C9D3B4"/><circle cx=".8" cy="1" r=".18" fill="#A9B98E"/><circle cx="2.2" cy="2.3" r=".14" fill="#B6C49C"/></pattern>
<clipPath id="cTerr"><path d="{d(TERRACE)}"/></clipPath>
<clipPath id="cPond"><path d="{d(SW)}"/></clipPath>
<radialGradient id="gDeep"><stop offset="0" stop-color="#2F6F8C"/><stop offset="1" stop-color="#4C8CA7"/></radialGradient>
<filter id="glow" x="-1" y="-1" width="3" height="3"><feGaussianBlur stdDeviation=".35"/></filter>
</defs>'''


def flagstones(bbox, cell, clip, seed, cls="fg"):
    rg = random.Random(seed)
    x0, y0, x1, y1 = bbox
    nx, ny = int((x1 - x0) / cell) + 2, int((y1 - y0) / cell) + 2
    G = [[(x0 + i * cell + rg.uniform(-.32, .32) * cell, y0 + j * cell + rg.uniform(-.32, .32) * cell) for j in range(ny)] for i in range(nx)]
    out = [f'<g clip-path="url(#{clip})">']
    for i in range(nx - 1):
        for j in range(ny - 1):
            q = [G[i][j], G[i + 1][j], G[i + 1][j + 1], G[i][j + 1]]
            cx = sum(p[0] for p in q) / 4; cy = sum(p[1] for p in q) / 4
            q = [(cx + (p[0] - cx) * .86, cy + (p[1] - cy) * .86) for p in q]
            out.append(f'<polygon class="{cls}{rg.randint(1, 3)}" points="{" ".join(f"{x:.2f},{y:.2f}" for x, y in q)}"/>')
    out.append('</g>')
    return "".join(out)


def stepping(center, step, seed, size=1.25):
    rg = random.Random(seed)
    c = catmull(center, False, 8)
    out = []
    for i, (x, y) in enumerate(walk(c, step)):
        out.append(rock(x + rg.uniform(-.25, .25), y + rg.uniform(-.25, .25), size * rg.uniform(.85, 1.1), rg, flat=True, cls="fg2"))
    return "".join(out)


def edge_rocks(poly, spacing, rmin, rmax, push, skip, seed, cls="st"):
    rg = random.Random(seed)
    out = []; acc = 0; n = len(poly)
    for i in range(n):
        a, b = poly[i], poly[(i + 1) % n]
        acc += math.hypot(b[0] - a[0], b[1] - a[1])
        if acc < spacing:
            continue
        acc = rg.uniform(-.4, .4)
        if any(f(a) for f in skip):
            continue
        r = rg.uniform(rmin, rmax); nx, ny = normal_at(poly, i)
        out.append(rock(a[0] + nx * r * push, a[1] + ny * r * push, r, rg, cls=cls))
    return "".join(out)


SKIP_POND = [lambda p: p[0] < 33.6 and p[1] > -15, lambda p: 35 < p[0] < 46 and p[1] > -13, lambda p: 46 < p[0] < 57.5 and p[1] > -13.5,
             lambda p: 57.5 < p[0] < 62.5 and p[1] > -16, lambda p: 65 < p[0] < 69.5 and -30.5 < p[1] < -24,
             lambda p: 36 < p[0] < 46 and p[1] < -43, lambda p: 22.5 < p[0] < 30.5 and -44 < p[1] < -37]
SKIP_POND_C = SKIP_POND + [lambda p: 30 < p[0] < 66.5 and p[1] < -30.5]   # back shore belongs to the wetland lip


def chair_ad(cx, cy, ang):
    return (f'<g transform="rotate({ang:.1f} {cx:.2f} {cy:.2f})"><path class="fu" d="M{cx - 1.1:.2f},{cy - .9:.2f} L{cx + 1.1:.2f},{cy - .9:.2f} L{cx + 1.3:.2f},{cy + 1.5:.2f} L{cx - 1.3:.2f},{cy + 1.5:.2f} Z"/>'
            f'<path class="fu2" d="M{cx - 1.35:.2f},{cy + 1.0:.2f} L{cx + 1.35:.2f},{cy + 1.0:.2f} L{cx + 1.45:.2f},{cy + 1.75:.2f} L{cx - 1.45:.2f},{cy + 1.75:.2f} Z"/></g>')


def lights(pts):
    return "".join(f'<circle class="lg" cx="{x}" cy="{y}" r=".75" filter="url(#glow)"/><circle class="lgc" cx="{x}" cy="{y}" r=".22"/>' for x, y in pts)


def yard():
    s = []
    rg = random.Random(21)
    x0, y0, x1, y1 = LOT
    # ground
    s.append(f'<rect fill="url(#lawn)" x="{x0}" y="{y0}" width="{x1 - x0}" height="{y1 - y0}"/>')
    s.append(f'<rect class="road" x="-40" y="96" width="200" height="10"/><line class="curb" x1="-40" x2="160" y1="96" y2="96"/>')
    mead = [(x0, y0)] + [(x0 + i * (x1 - x0) / 12, -86 + 3 * math.sin(i * 1.3) + rg.uniform(-1, 1)) for i in range(13)] + [(x1, y0)]
    s.append(f'<path fill="url(#mead)" d="{d(mead)}"/>')
    s.append('<path class="mow" d="M40.6,-77 C40,-84 36,-90 44,-96 C52,-102 70,-100 86,-99" fill="none"/>')
    # back yard beds and berm
    s.append(f'<path class="berm" d="{d(BERM)}"/>')
    ring = offset(SW, 5.2)
    for i in range(0, len(ring), 7):
        x, y = ring[i]
        if y > -14 or (FIRE[0] - 2 < x < 15 and -36 < y < -16) or (60 < x < 84 and -66 < y < -24):
            continue
        s.append(shrub(x, y, rg.uniform(1.6, 2.4), rg.choice(["sh", "sh2", "sh3", "sh"]), seed=i))
    # terrace
    s.append(f'<path class="grout" d="{d(TERRACE)}"/>')
    s.append(flagstones((8, -12, 84, 22), 2.5, "cTerr", 4))
    # outdoor shower
    s.append('<rect class="deck" x="81.6" y="-0.6" width="4.4" height="5.6"/>' + "".join(f'<line class="board" x1="{81.6 + i * .55:.2f}" x2="{81.6 + i * .55:.2f}" y1="-0.6" y2="5"/>' for i in range(1, 8)) +
             '<path class="fence" d="M81.6,-0.6 L86,-0.6 M81.6,-0.6 L81.6,2.6"/><circle class="fu2" cx="85" cy="4" r=".45"/>')
    # fire pit circle
    fx, fy = FIRE
    s.append(f'<circle class="dg" cx="{fx}" cy="{fy}" r="7.6"/><circle class="edge" cx="{fx}" cy="{fy}" r="7.6"/>')
    s.append(f'<circle class="st2" cx="{fx}" cy="{fy}" r="2.1"/><circle class="pit" cx="{fx}" cy="{fy}" r="1.4"/><circle class="fire" cx="{fx}" cy="{fy}" r=".75"/>')
    for k in range(6):
        a = math.radians(k * 60 + 15); cx, cy = fx + 4.9 * math.cos(a), fy + 4.9 * math.sin(a)
        s.append(chair_ad(cx, cy, math.degrees(a) - 90))
    # paths
    s.append(stepping(PATH_L, 2.3, 1) + stepping(PATH_LOOP, 2.3, 2) + stepping(PATH_LOOP2, 2.3, 3) + stepping(PATH_SIDE, 2.4, 4) + stepping(PATH_PRIM, 2.2, 5, 1.1))
    s.append(f'<circle class="fg2" cx="{OVER[0]}" cy="{OVER[1]}" r="3.7"/><path class="bench" d="M{OVER[0] - 2.9},{OVER[1] - .6} A3,3 0 0 1 {OVER[0] + 2.9},{OVER[1] - .6}"/>')
    # wetland filter: crescent on the back shore, upper tier behind the falls, lower tier sheeting over a stone lip
    s.append(f'<path fill="url(#grav)" class="wlb" d="{d(WL)}"/><path class="tier" d="{d(WL_UP)}"/>')
    for bx, by, rx, ry, rot in ((37.4, -56.2, 2.2, 1.1, 0), (60.6, -48.4, 2.0, 1.1, -35)):
        s.append(f'<path class="w1" d="{d(blob(bx, by, rx, ry, seed=int(bx), k=7, rot=rot))}"/>')
    pr = random.Random(5)
    for j in range(330):
        x, y = pr.uniform(30, 72), pr.uniform(-62, -30)
        if inside((x, y), WL) and not (37.6 < x < 44.8 and y > -52.4):
            kind = pr.random()
            if kind < .42: s.append(tuft(x, y, pr.uniform(.8, 1.3), "tf"))
            elif kind < .68: s.append(tuft(x, y, pr.uniform(.9, 1.4), "tf2"))
            elif kind < .84: s.append(f'<circle class="pk" cx="{x:.2f}" cy="{y:.2f}" r=".55"/><circle class="pkf" cx="{x:.2f}" cy="{y - .1:.2f}" r=".22"/>')
            else: s.append(f'<circle class="ir" cx="{x:.2f}" cy="{y:.2f}" r=".5"/>')
    s.append(edge_rocks(WL_OUTER + [WL_OUTER[-1]], 2.4, .9, 1.6, .55, [lambda p: p[1] > -33], 31))
    s.append(edge_rocks(WL_UP, 2.0, .5, .9, 0, [lambda p: p[1] > -51], 33, cls="st3"))
    # pond water
    s.append(f'<path class="w1" d="{d(SW)}"/><path class="w1" d="{d(BAY)}"/>')
    shelf = offset(SW, -1.4)
    s.append(edge_rocks(shelf, 2.4, .5, 1.0, 0, [lambda p: p[0] < 33 and p[1] > -18], 41, cls="st3"))
    s.append(f'<path fill="url(#grav)" d="{d(BEACH)}"/>')
    s.append(f'<path class="tint" d="{d(SW)}"/><path class="tint" d="{d(BAY)}"/>')
    s.append(f'<path class="w2" d="{d(Z5)}"/><path fill="url(#gDeep)" d="{d(Z8)}"/>')
    for i in range(14):
        x, y = rg.uniform(26, 58), rg.uniform(-38, -14)
        if inside((x, y), Z5):
            s.append(f'<path class="rip" d="M{x:.2f},{y:.2f} q1.2,-.5 2.4,0"/>')
    # lilies on the planting shelf where the stream comes in
    for x, y, r, a in ((64.4, -24.2, .9, 20), (66, -26.4, .75, 140), (63.2, -27.4, .7, 260), (65.4, -29.2, .8, 80), (62.6, -22.6, .65, 200), (66.4, -23.8, .6, 320), (56, -37.6, .7, 40), (52.4, -39.4, .6, 210)):
        s.append(lily(x, y, r, a))
    s.append('<circle class="lf" cx="64.7" cy="-25.2" r=".32"/><circle class="lf2" cx="65.8" cy="-28.4" r=".3"/><circle class="lf" cx="62.9" cy="-23.4" r=".26"/>')
    # slab steps into the swim zone
    for k, (yy, op) in enumerate(((-8.1, 0), (-10.5, .3), (-12.9, .55))):
        xa = 36.4 + k * .5; xb = 44.6 - k * .5
        s.append(f'<path class="slab" d="M{xa},{yy} L{xb},{yy - .1} L{xb - .2},{yy - 2.3} L{xa + .3},{yy - 2.2} Z"/>')
        if op:
            s.append(f'<path class="w1" opacity="{op}" d="M{xa},{yy} L{xb},{yy - .1} L{xb - .2},{yy - 2.3} L{xa + .3},{yy - 2.2} Z"/>')
    # edge boulders, jump rock and waterfall
    s.append(edge_rocks(SW, 2.15, .85, 1.75, .45, SKIP_POND_C, 51))
    s.append(edge_rocks(BAY, 1.7, .55, 1.0, .45, [lambda p: p[0] < 61.5], 52))
    s.append('<path class="w1" d="M37.7,-51.2 L44.7,-51.4 L45.4,-45.0 L37.0,-45.2 Z"/>')
    for i in range(9):
        x = 38.1 + i * .8
        s.append(f'<path class="foam" d="M{x:.2f},-50.8 C{x + .2:.2f},-48.8 {x - .25:.2f},-47.2 {x + .1:.2f},-45.5"/>')
    s.append(rock(41.2, -52.0, 3.0, random.Random(5), flat=True, cls="slab"))
    s.append('<path class="w1" opacity=".55" d="M38.2,-51.5 L44.2,-51.7 L44.2,-50.9 L38.2,-50.8 Z"/>')
    for x, y, r in ((34.8, -49.0, 2.5), (47.6, -49.2, 2.7), (33.6, -52.6, 1.8), (49.0, -52.8, 1.9)):
        s.append(rock(x, y, r, random.Random(int(x * 10))))
    s.append('<ellipse class="foamb" cx="41.1" cy="-44.9" rx="4.4" ry="1.0"/><ellipse class="foamb" cx="41.4" cy="-43.8" rx="2.6" ry=".5" opacity=".6"/>')
    s.append(rock(26.6, -41.8, 3.3, random.Random(77), flat=True, cls="slab"))
    s.append(rock(22.6, -43.8, 2.0, random.Random(78)) + rock(23.4, -19.6, 1.9, random.Random(81)) + rock(21.4, -17.4, 1.4, random.Random(82)))
    # lower-tier lip: low flat stones, water sheeting into the pond, and the rill into the lily cove
    acc, lr = 0, random.Random(7)
    for a, b in zip(WL_INNER, WL_INNER[1:]):
        acc += math.hypot(b[0] - a[0], b[1] - a[1])
        if acc >= 1.6:
            acc = lr.uniform(-.3, .3); s.append(rock(a[0], a[1], lr.uniform(.45, .8), lr, flat=True, cls="st3"))
    for i in range(1, len(WL_LIP) - 1, 3):
        (xa, ya), (xb, yb) = WL_LIP[i - 1], WL_LIP[i + 1]
        L = math.hypot(xb - xa, yb - ya) or 1; nx, ny = (yb - ya) / L, -(xb - xa) / L; x, y = WL_LIP[i]
        s.append(f'<path class="foam2" d="M{x:.2f},{y:.2f} L{x + nx * 1.1:.2f},{y + ny * 1.1:.2f}"/>')
    s.append('<path class="w1" d="M68.4,-31.6 C67.4,-30.4 66.6,-29.6 66.0,-28.4 L64.8,-28.8 C65.4,-30 66.2,-31 67.0,-32.2 Z"/>')
    # deck over the water
    s.append('<path class="deck" d="M46.4,-4.4 L57.2,-4.4 L57.2,-12.2 L54.4,-15.2 L46.4,-15.2 Z"/>' +
             "".join(f'<line class="board" x1="{46.4 + i * .6:.2f}" x2="{46.4 + i * .6:.2f}" y1="-4.4" y2="{-15.2 if 46.4 + i * .6 <= 54.4 else -15.2 + (46.4 + i * .6 - 54.4):.2f}"/>' for i in range(1, 18)))
    s.append('<rect class="fu" x="48" y="-13.4" width="2.3" height="6.2" rx=".4"/><rect class="fu2" x="48" y="-13.4" width="2.3" height="1.8" rx=".4"/>'
             '<rect class="fu" x="51.4" y="-13.4" width="2.3" height="6.2" rx=".4"/><rect class="fu2" x="51.4" y="-13.4" width="2.3" height="1.8" rx=".4"/>'
             '<circle class="fu" cx="55.4" cy="-9" r=".7"/><path class="ladder" d="M53.1,-15.2 L53.1,-16.6 M54.6,-15.2 L54.6,-16.6 M53.1,-15.9 L54.6,-15.9"/>')
    # terrace furniture
    s.append('<rect class="fu" x="26.4" y="-3" width="2.3" height="6" rx=".4"/><rect class="fu2" x="26.4" y="1.2" width="2.3" height="1.8" rx=".4"/>'
             '<rect class="fu" x="30" y="-3" width="2.3" height="6" rx=".4"/><rect class="fu2" x="30" y="1.2" width="2.3" height="1.8" rx=".4"/>'
             '<circle class="umb" cx="29.3" cy="-.4" r="3.4"/><circle class="fu2" cx="29.3" cy="-.4" r=".25"/>')
    for x, y in ((17.5, 9), (66.5, 7.5), (78.5, 2.2)):
        s.append(f'<circle class="pot" cx="{x}" cy="{y}" r="1.2"/>' + shrub(x, y, .85, "sh", seed=int(x)))
    # pump vault beside the intake bay
    s.append('<rect class="vault" x="77.6" y="-15.6" width="3.4" height="2.6" rx=".3"/><circle class="vault" cx="81.9" cy="-14.3" r=".5"/>')
    for x, y in ((76.2, -12), (82.6, -12.2), (79.4, -11.6), (76.6, -16.8), (83, -16.4)):
        s.append(shrub(x, y, 1.15, "sh", seed=int(x * y)))
    # trees around the pond
    s.append(tree(22.6, -54, 4.4, "maple", 1) + tree(75, -52.6, 3.2, "maple", 2) + tree(58, -67.4, 3.6, "birch", 32) + tree(87.4, -58, 4.6, "birch", 3) + tree(89.2, -53.2, 2.6, "birch", 31))
    s.append(tree(-15, -52, 8.6, "dec", 4) + tree(118, -68, 9.4, "dec", 5) + tree(-18, -88, 7.4, "dec", 6) + tree(130, -36, 7, "dec", 7))
    for k, x in enumerate(range(-26, 146, 9)):
        s.append(tree(x + rg.uniform(-1.5, 1.5), -105 + (k % 2) * 3.4, rg.uniform(4.4, 5.6), "ever", 40 + k))
    for k, y in enumerate(range(-90, 70, 16)):
        if -30 < y < 30: continue
        s.append(tree(-25.5 + (k % 2) * 2, y, rg.uniform(3.8, 4.8), "ever", 70 + k))
        if y > -60: s.append(tree(143.5 - (k % 2) * 2, y, rg.uniform(3.8, 4.8), "ever", 90 + k))
    # left side shade garden
    s.append(f'<path class="bed" d="{d(blob(-4.4, 33.4, 4.2, 20, seed=8, k=10, jit=.08))}"/>')
    for k in range(9):
        s.append(shrub(-4.2 + (k % 2) * 1.6, 16 + k * 4.2, rg.uniform(1.2, 1.7), rg.choice(["sh", "sh2", "fern"]), seed=200 + k))
    # primary garden behind the primary bath
    garden = [(86, -2.5)] + [(100 + 14 * math.cos(math.radians(a)), -4 + 21 * math.sin(math.radians(a))) for a in range(180, 361, 10)] + [(106, -2.5)]
    s.append(f'<path fill="url(#moss)" d="{d(garden)}"/>')
    for a in range(180, 341, 8):
        x, y = 100 + 15.2 * math.cos(math.radians(a)), -4 + 22.2 * math.sin(math.radians(a))
        s.append(shrub(x, y, 1.7, "hedge", seed=a))
    s.append(f'<circle fill="url(#grav)" cx="95" cy="-12.6" r="2.6"/><circle class="w1" cx="95" cy="-12.6" r="1.5"/>')
    for dx, dy in ((-.45, -.2), (.5, -.35), (.05, .45)):
        cx, cy = 95 + dx, -12.6 + dy
        s.append('<polygon class="basalt" points="' + " ".join(f"{cx + .48 * math.cos(math.radians(60 * i)):.2f},{cy + .48 * math.sin(math.radians(60 * i)):.2f}" for i in range(6)) + '"/>')
    s.append(tree(89.4, -17.6, 3.4, "maple", 9) + '<rect class="fu2" x="104.2" y="-21.6" width="4.6" height="1.5" rx=".3" transform="rotate(-35 106.5 -20.8)"/>')
    # kitchen garden and mower route
    s.append(f'<path class="gpath" d="{d(ribbon([(117, 45), (118.2, 30), (118.4, 14), (118, 0), (117.6, -10)], 4)[0])}"/>')
    s.append('<rect class="pav" x="113" y="44.2" width="8" height="11.6"/>')
    s.append(stepping([(112.6, 28), (115.6, 28.4)], 1.6, 9, 1))
    s.append('<rect class="gpath" x="124" y="18" width="21.6" height="26"/><rect class="fenceg" x="124" y="18" width="21.6" height="26"/>')
    for cx in (126.2, 133, 139.8):
        for cy in (20.4, 31.6):
            s.append(f'<rect class="rbed" x="{cx}" y="{cy}" width="4" height="9.6" rx=".2"/>')
            for j in range(4): s.append(shrub(cx + 1 + (j % 2) * 2, cy + 1.5 + j * 2.2, .7, "veg", seed=int(cx * cy) + j))
    # front yard: drive, walk, beds, front pond
    s.append('<path class="drive" d="M79.5,66.5 L107.5,66.5 L107.5,78 L103.4,84 L103.4,92 L106,96 L82,96 L84.6,92 L84.6,84 L79.5,78 Z"/>')
    walk_poly, _ = ribbon([(38, 72), (38.2, 76.6), (44, 79.6), (56, 80.4), (68, 79.2), (79.5, 76.6)], 4.4)
    s.append(f'<path class="grout" d="{d(walk_poly)}"/>')
    s.append('<clipPath id="cWalk"><path d="' + d(walk_poly) + '"/></clipPath>' + flagstones((30, 70, 82, 84), 2.1, "cWalk", 12))
    s.append('<path class="bed" d="M7.2,72.3 L24,72.3 L24,76.4 C18,77.6 12,77.2 7.2,75.8 Z"/><path class="bed" d="M24,72.3 L35.6,72.3 L35.6,75.6 C31,76.6 27,76.4 24,75.6 Z"/>'
             '<path class="bed" d="M40.6,72.3 L52,72.3 L52,75.2 C48,76.2 44,76 40.6,75.6 Z"/><path class="bed" d="M68,62.8 L78.4,62.8 L78.4,66 C74,67.2 70,67 68,66 Z"/>'
             '<path class="bed" d="M107.6,55.8 L112.8,55.8 L112.8,62 C112.5,65 110.4,66.2 107.6,66.2 Z"/>')
    for x in (9, 12.4, 15.8, 19.2, 22.4, 25.6, 28.8, 32.4, 43, 46.4, 49.6, 70, 73.4, 76.6, 109.6, 111.2):
        y = 74.2 if x < 60 else (64.4 if x < 100 else 59 + (x - 109.6) * 2)
        s.append(shrub(x, y, 1.25, rg.choice(["sh", "sh2", "sh3"]), seed=int(x * 10)))
    # front ecosystem pond in the courtyard by the porch
    FP = blob(60.2, 66.6, 5.4, 3.7, seed=6, k=9, jit=.1, rot=-8)
    s.append(f'<path class="w1" d="{d(FP)}"/><path class="w2" d="{d(offset(FP, -1.6))}"/>')
    s.append(lily(58.4, 67.6, .7, 30) + lily(61.6, 68.4, .6, 200) + '<circle class="lf" cx="58.6" cy="67.3" r=".26"/>')
    s.append(edge_rocks(FP, 1.6, .55, 1.0, .5, [lambda p: p[0] < 55.4 and p[1] > 65], 61))
    s.append('<path class="w1" d="M63.6,62.6 L65.6,62.2 L65.2,64.4 L63.4,64.6 Z"/><path class="foam" d="M64,62.6 L63.9,64.4 M64.8,62.4 L64.6,64.3"/>')
    s.append(rock(65.2, 61.4, 1.5, random.Random(91)) + rock(66.8, 63.4, 1.2, random.Random(92)) + rock(62.4, 61.6, 1.0, random.Random(93)))
    s.append(rock(54.4, 67.4, 1.3, random.Random(94), flat=True, cls="slab"))
    for x, y in ((54.4, 62.2), (67, 66.4), (66.2, 70.4), (55.6, 71), (61, 71.2)):
        s.append(shrub(x, y, 1.1, rg.choice(["sh", "sh2", "sh3"]), seed=int(x * y)))
    s.append(tree(12, 86, 7.4, "dec", 13) + tree(124, 82, 7.2, "dec", 14) + tree(-6.4, 75, 3.6, "orn", 15) + tree(72.4, 72.6, 3.0, "orn", 16) + tree(58, 87.4, 4.2, "orn", 17))
    s.append('<rect class="fu2" x="80" y="90.6" width="1" height="1" />')
    # optional barrier fence with gates
    s.append('<path class="bfence" d="M0,24 L-11,24 M-15,24 L-22,24 L-22,-92 L96,-92 L96,-56 M96,-51 L96,-28 L85.4,-26.4 L85.4,-3"/>')
    # lot line
    # lights: underwater, waterfall, stream, trees, paths
    s.append(lights([(39.4, -46.4), (42.8, -46.6), (30.6, -35), (50.4, -36), (36, -14.6), (58.6, -14), (56.6, -40.4), (62.6, -35.6), (60, -56), (25.4, -50.6), (74, -49.6), (64.6, -25.4),
                     (60.6, -11.4), (95, -10), (8.2, -10), (12, -55), (36.2, -73.4), (79, -40), (60.4, 63.4)]))
    return "".join(s)
