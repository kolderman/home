"""Rev. D landscape: the long pond (picked 2026-10-26) in place of the rev. C round pond.
Same axes as the house plan: feet, x left->right, y < 0 is the back yard. yard.py stays as rev. C for the comparison pages."""
import math, random
import yard as _Y
from yard import *          # helpers: flagstones, stepping, edge_rocks, chair_ad, lights, inside, LOT, paths that don't change
from geo import *

AXIS = 37.5                 # front doors -> glass wall -> falls

# ---------------------------------------------------------------- long pond, falls moved 3.5 ft left onto the axis
Q = [(8, -4.5), (14, .6), (20, 3.4), (27, 4.8), (36, 5.2), (44.6, 2.6), (50, -2.4), (56, -4.6), (64, -5.4), (72, -6.8), (79, -8.6), (83.4, -12.4),
     (84.6, -18), (83, -23.6), (77, -27), (68, -28.8), (59, -30.4), (51, -33), (42.7, -34.4), (41.1, -37.8), (37.5, -39.2), (33.9, -37.8),
     (32.1, -34.8), (27, -34.0), (22, -33.6), (14, -31), (8.4, -27.6), (4.6, -23), (3, -16), (3.6, -9)]
SW = catmull(Q, True, 10)
Z5 = catmull([(14, -8), (24, -5), (36, -3.4), (48, -6.6), (60, -10.4), (72, -12.6), (78, -17.6), (74, -22.6), (62, -24.2), (50, -27.4),
              (38, -30.4), (26, -29.6), (16, -27), (11, -21), (10.6, -13)], True, 10)
Z8 = blob(25.6, -24.4, 7.2, 3.8, seed=3, k=8, jit=.07, rot=-6)
LEDGE = [(28.4, 4.3), (44, 3.0), (43.2, -.6), (29, .6)]                  # 12 in sun ledge off the porch
BEACH = blob(10.4, -4.6, 6.2, 3.6, seed=5, k=8, jit=.08, rot=-30)
COVE = blob(5.2, -24.6, 3.2, 2.6, seed=2, k=8, jit=.08, rot=20)         # intake bay, far-left corner
LILYC = blob(81.6, -18.6, 3.6, 3.8, seed=8, k=8, jit=.06)               # lily cove where the rill comes in
VAULT = (-7.6, -27.2)

_o = offset(SW, 1.1)
WL_INNER = [_o[i] for i, p in enumerate(SW) if 30.5 <= p[0] <= 83.6 and p[1] <= -22.6]
WL_OUTER = catmull([(30.7, -36.4), (29.3, -43), (33.5, -50), (42, -53.6), (55.6, -52.6), (65.6, -48.6), (75.2, -44.4), (83.6, -38.6),
                    (89, -30.6), (90.2, -24.2), (86.8, -21.2)], False, 8)
WL = WL_OUTER + WL_INNER
WL_UP = blob(39.1, -44.6, 8.2, 4.2, seed=4, k=9, jit=.07, rot=-4)        # upper tier, +3.5 ft, feeds the falls
WL_LIP = [p for p in WL_INNER if p[0] > 50]                               # lower tier lip, about 1 ft above the water
BERM = offset(WL, 6)
FIRE = (12.4, -46)
JUMP = (23, -35.4)
OVER = (42, -76.4)

A_SW, A5, A8, A_WL = area(SW), area(Z5), area(Z8), area(WL)
GAL = ((A_SW - A5) * 2 + (A5 - A8) * 5 + A8 * 8 - area(LEDGE)) * 7.48
LIP_FT = sum(math.dist(a, b) for a, b in zip(WL_LIP, WL_LIP[1:]))

NEAR = [p for p in SW if p[1] > -9.5 and 12 < p[0] < 84]                   # near shore, where the coping runs
TERRACE = ([(18, 13), (24, 13), (24, 20), (46, 20), (46, 10), (68, 10), (68, 5), (86, 5), (86, -5.6)] +
           [(x + nx * .2, y + ny * .2) for (x, y), (nx, ny) in [(p, normal_at(SW, SW.index(p))) for p in sorted(NEAR, key=lambda p: -p[0])]] + [(14.6, 3.2), (14, 13)])

PATH_L = [(-1, 6), (-3.6, -8), (-4, -20), (-1, -34), (4.6, -42)]
PATH_LOOP = [(18.6, -51), (24, -60), (30.6, -68), (37.4, -74.4)]
PATH_LOOP2 = [(47.8, -75.4), (58, -72), (70, -66), (81, -58), (89.4, -48), (94, -38.6)]
SEAT = (94.2, -34.8)                                                      # bench at the end of the right path, looking at the lip


def defs():
    return _Y.defs().replace(d(_Y.TERRACE), d(TERRACE)).replace(d(_Y.SW), d(SW))


def falls(x1, y1, x2, y2, w, seed):
    """Falls from the upper tier at (x1, y1) down to the pond at (x2, y2), w ft wide."""
    rg = random.Random(seed)
    dx, dy = x2 - x1, y2 - y1; L = math.hypot(dx, dy); ux, uy = dx / L, dy / L; nx, ny = -uy, ux
    a = (x1 + nx * w / 2, y1 + ny * w / 2); b = (x1 - nx * w / 2, y1 - ny * w / 2)
    c = (x2 - nx * w * .6, y2 - ny * w * .6); d_ = (x2 + nx * w * .6, y2 + ny * w * .6)
    s = [f'<polygon class="w1" points="{" ".join(f"{p[0]:.2f},{p[1]:.2f}" for p in (a, b, c, d_))}"/>']
    for i in range(int(w / .7) + 1):
        t = -w / 2 + .35 + i * .7
        if t > w / 2: break
        s.append(f'<path class="foam" d="M{x1 + nx * t:.2f},{y1 + ny * t:.2f} L{x2 + nx * t * 1.15:.2f},{y2 + ny * t * 1.15:.2f}"/>')
    s.append(rock(x1 - ux * .9, y1 - uy * .9, w * .5, rg, flat=True, cls="slab"))
    for sg in (1, -1):
        s.append(rock(x1 + nx * sg * (w / 2 + 1.6), y1 + ny * sg * (w / 2 + 1.6), rg.uniform(1.8, 2.4), rg))
        s.append(rock(x2 + nx * sg * (w / 2 + 1.8) - ux * .6, y2 + ny * sg * (w / 2 + 1.8) - uy * .6, rg.uniform(2.0, 2.6), rg))
    s.append(f'<ellipse class="foamb" cx="{x2 + ux * .4:.2f}" cy="{y2 + uy * .4:.2f}" rx="{w * .6:.2f}" ry=".9"/>')
    return "".join(s)


def coping():
    """Cut stone coping along the near shore: the terrace ends at the water."""
    rg = random.Random(4); s = []
    pts = sorted(NEAR, key=lambda p: p[0])
    for a, b in zip(pts[::2], pts[2::2]):
        if 28 < (a[0] + b[0]) / 2 < 44.4: continue          # the sun ledge has its own edge
        n = normal_at(SW, SW.index(a)); w = 1.5
        q = [a, b, (b[0] + n[0] * w, b[1] + n[1] * w), (a[0] + n[0] * w, a[1] + n[1] * w)]
        s.append(f'<polygon class="{rg.choice(["slab", "st3", "slab"])}" points="{" ".join(f"{x:.2f},{y:.2f}" for x, y in q)}"/>')
    return "".join(s)


def yard():
    s = []
    rg = random.Random(21)
    x0, y0, x1, y1 = LOT
    # ground, meadow and mown path
    s.append(f'<rect fill="url(#lawn)" x="{x0}" y="{y0}" width="{x1 - x0}" height="{y1 - y0}"/>')
    s.append(f'<rect class="road" x="-40" y="96" width="200" height="10"/><line class="curb" x1="-40" x2="160" y1="96" y2="96"/>')
    mead = [(x0, y0)] + [(x0 + i * (x1 - x0) / 12, -86 + 3 * math.sin(i * 1.3) + rg.uniform(-1, 1)) for i in range(13)] + [(x1, y0)]
    s.append(f'<path fill="url(#mead)" d="{d(mead)}"/>')
    s.append('<path class="mow" d="M40.6,-77 C40,-84 36,-90 44,-96 C52,-102 70,-100 86,-99" fill="none"/>')
    # back slope behind the wetland, and shrubs around the pond's back side
    s.append(f'<path class="berm" d="{d(BERM)}"/>')
    ring = offset(SW, 5.2); wl_zone = offset(WL, 6.5)
    for i in range(0, len(ring), 7):
        x, y = ring[i]
        if y > -14 or x < 0 or inside((x, y), wl_zone) or math.dist((x, y), FIRE) < 11 or math.dist((x, y), JUMP) < 5:
            continue
        s.append(shrub(x, y, rg.uniform(1.6, 2.4), rg.choice(["sh", "sh2", "sh3", "sh"]), seed=i))
    # terrace: flagstone from the porch to the coping
    s.append(f'<path class="grout" d="{d(TERRACE)}"/>')
    s.append(flagstones((10, -14, 90, 22), 2.5, "cTerr", 4))
    # outdoor shower
    s.append('<rect class="deck" x="81.6" y="-0.6" width="4.4" height="5.6"/>' + "".join(f'<line class="board" x1="{81.6 + i * .55:.2f}" x2="{81.6 + i * .55:.2f}" y1="-0.6" y2="5"/>' for i in range(1, 8)) +
             '<path class="fence" d="M81.6,-0.6 L86,-0.6 M81.6,-0.6 L81.6,2.6"/><circle class="fu2" cx="85" cy="4" r=".45"/>')
    # fire pit across the water
    fx, fy = FIRE
    s.append(f'<circle class="dg" cx="{fx}" cy="{fy}" r="7"/><circle class="edge" cx="{fx}" cy="{fy}" r="7"/>')
    s.append(f'<circle class="st2" cx="{fx}" cy="{fy}" r="2"/><circle class="pit" cx="{fx}" cy="{fy}" r="1.3"/><circle class="fire" cx="{fx}" cy="{fy}" r=".7"/>')
    s.append("".join(chair_ad(fx + 4.6 * math.cos(math.radians(a)), fy + 4.6 * math.sin(math.radians(a)), a - 90) for a in (20, 70, 120, 160, 200, 340)))
    # paths, overlook and the far-shore bench
    s.append(stepping(PATH_L, 2.3, 1) + stepping(PATH_LOOP, 2.3, 2) + stepping(PATH_LOOP2, 2.3, 3) + stepping(_Y.PATH_SIDE, 2.4, 4) + stepping(_Y.PATH_PRIM, 2.2, 5, 1.1))
    s.append(f'<circle class="fg2" cx="{OVER[0]}" cy="{OVER[1]}" r="3.7"/><path class="bench" d="M{OVER[0] - 2.9},{OVER[1] - .6} A3,3 0 0 1 {OVER[0] + 2.9},{OVER[1] - .6}"/>')
    s.append(f'<circle class="fg2" cx="{SEAT[0]}" cy="{SEAT[1]}" r="2.6"/><rect class="fu2" x="{SEAT[0] - 2}" y="{SEAT[1] - 1.9}" width="4" height="1.1" rx=".3" transform="rotate(30 {SEAT[0]} {SEAT[1]})"/>')
    # wetland: the far shore, upper tier behind the falls, lower tier sheeting over a stone lip
    s.append(f'<path fill="url(#grav)" class="wlb" d="{d(WL)}"/><path class="tier" d="{d(WL_UP)}"/>')
    for bx, by, rx, ry, rot in ((32.6, -46.6, 1.8, 1.0, 20), (70.4, -38.2, 2.0, 1.0, -20)):
        s.append(f'<path class="w1" d="{d(blob(bx, by, rx, ry, seed=int(bx), k=7, rot=rot))}"/>')
    pr = random.Random(5)
    for _ in range(620):
        x, y = pr.uniform(28, 92), pr.uniform(-56, -20)
        if inside((x, y), WL) and not (33.6 < x < 41.4 and y > -45.8):
            kind = pr.random()
            if kind < .42: s.append(tuft(x, y, pr.uniform(.8, 1.3), "tf"))
            elif kind < .68: s.append(tuft(x, y, pr.uniform(.9, 1.4), "tf2"))
            elif kind < .84: s.append(f'<circle class="pk" cx="{x:.2f}" cy="{y:.2f}" r=".55"/><circle class="pkf" cx="{x:.2f}" cy="{y - .1:.2f}" r=".22"/>')
            else: s.append(f'<circle class="ir" cx="{x:.2f}" cy="{y:.2f}" r=".5"/>')
    s.append(edge_rocks(WL_OUTER + [WL_OUTER[-1]], 2.4, .9, 1.6, .55, [lambda p: p[1] > -22], 31))
    s.append(edge_rocks(WL_UP, 2.0, .5, .9, 0, [lambda p: p[1] > -41], 33, cls="st3"))
    # the pond
    s.append(f'<path class="w1" d="{d(SW)}"/><path class="w1" d="{d(COVE)}"/><path class="w1" d="{d(LILYC)}"/>')
    s.append(f'<path fill="url(#grav)" d="{d(BEACH)}"/>')
    s.append(f'<path class="tint" d="{d(SW)}"/><path class="tint" d="{d(COVE)}"/>')
    s.append(f'<path class="w2" d="{d(Z5)}"/><path fill="url(#gDeep)" d="{d(Z8)}"/>')
    for _ in range(26):
        x, y = rg.uniform(14, 76), rg.uniform(-28, -6)
        if inside((x, y), Z5):
            s.append(f'<path class="rip" d="M{x:.2f},{y:.2f} q1.2,-.5 2.4,0"/>')
    # sun ledge, with chaises in the water, and slab steps down into the lap lane
    s.append(f'<polygon class="slab" opacity=".55" points="{" ".join(f"{x},{y}" for x, y in LEDGE)}"/>')
    for k, (yy, op) in enumerate(((-.4, .25), (-2.8, .45), (-5.2, .6))):
        xa = 32.4 + k * .5; xb = 40.6 - k * .5
        s.append(f'<path class="slab" d="M{xa},{yy} L{xb},{yy - .1} L{xb - .2},{yy - 2.3} L{xa + .3},{yy - 2.2} Z"/>'
                 f'<path class="w1" opacity="{op}" d="M{xa},{yy} L{xb},{yy - .1} L{xb - .2},{yy - 2.3} L{xa + .3},{yy - 2.2} Z"/>')
    s.append("".join(f'<rect class="fu" x="{x}" y=".9" width="2.2" height="3.6" rx=".4"/><rect class="fu2" x="{x}" y="3.3" width="2.2" height="1.2" rx=".4"/>' for x in (29.6, 41.4)))
    # edge stone: coping on the near shore, boulders elsewhere, the lip on the far shore
    s.append(edge_rocks(SW, 2.15, .85, 1.75, .45, [lambda p: p[1] > -9.5 and p[0] > 12, lambda p: p[1] < -22 and p[0] > 30,
                                                   lambda p: p[0] < 16 and p[1] > -9, lambda p: 20 < p[0] < 26 and p[1] < -32], 51))
    s.append(edge_rocks(COVE, 1.6, .55, 1.0, .45, [lambda p: p[0] > 7], 52))
    s.append(coping())
    acc, lr = 0, random.Random(7)
    for a, b in zip(WL_INNER, WL_INNER[1:]):
        acc += math.hypot(b[0] - a[0], b[1] - a[1])
        if acc >= 1.6 and not (33.4 < a[0] < 41.6):
            acc = lr.uniform(-.3, .3); s.append(rock(a[0], a[1], lr.uniform(.45, .8), lr, flat=True, cls="st3"))
    for i in range(1, len(WL_LIP) - 1, 3):
        (xa, ya), (xb, yb) = WL_LIP[i - 1], WL_LIP[i + 1]
        L = math.hypot(xb - xa, yb - ya) or 1; nx, ny = (yb - ya) / L, -(xb - xa) / L; x, y = WL_LIP[i]
        s.append(f'<path class="foam2" d="M{x:.2f},{y:.2f} L{x + nx * 1.1:.2f},{y + ny * 1.1:.2f}"/>')
    s.append('<path class="w1" d="M86.4,-22.4 C85.8,-21.4 85.2,-20.8 84.6,-20.0 L83.6,-20.6 C84.2,-21.4 84.8,-22.2 85.4,-23.0 Z"/>')   # rill into the lily cove
    # falls on the axis, jump rock over the deep zone
    s.append(falls(AXIS, -43.4, AXIS, -38.4, 7.0, 3))
    s.append(rock(JUMP[0], JUMP[1], 3.3, random.Random(77), flat=True, cls="slab"))
    s.append(rock(19.2, -36.8, 1.9, random.Random(78)))
    for x, y, r, a in ((80.2, -16.8, .8, 20), (82.6, -19.6, .7, 140), (80.6, -21, .7, 260), (83, -16.4, .6, 200), (66, -27, .7, 40), (58.6, -28.8, .6, 210)):
        s.append(lily(x, y, r, a))
    # terrace furniture: table and umbrella, pots
    s.append('<circle class="umb" cx="58" cy="4" r="3.2"/><circle class="fu2" cx="58" cy="4" r=".25"/>')
    for x, y in ((17.5, 9), (66.5, 7.5), (78.5, 2.2)):
        s.append(f'<circle class="pot" cx="{x}" cy="{y}" r="1.2"/>' + shrub(x, y, .85, "sh", seed=int(x)))
    # pump vault past the bedroom wing, screened
    s.append(f'<rect class="vault" x="{VAULT[0]}" y="{VAULT[1]}" width="3.4" height="2.6" rx=".3"/>')
    for x, y in ((-9, -23.4), (-4.4, -24.2), (-9.6, -30.6), (-4.6, -31)):
        s.append(shrub(x, y, 1.15, "sh", seed=int(x * y)))
    # trees: maples framing the falls, birches behind the wetland, live oaks well back
    s.append(tree(23.4, -45.4, 4.0, "maple", 1) + tree(52.4, -46.2, 3.0, "maple", 2) + tree(91.6, -40.4, 3.2, "maple", 22) +
             tree(62, -59, 3.6, "birch", 3) + tree(80, -54.4, 3.4, "birch", 32) + tree(-14, -48, 8.4, "dec", 4))
    s.append(tree(118, -68, 9.4, "dec", 5) + tree(-18, -88, 7.4, "dec", 6) + tree(130, -36, 7, "dec", 7))
    for k, x in enumerate(range(-26, 146, 9)):
        s.append(tree(x + rg.uniform(-1.5, 1.5), -105 + (k % 2) * 3.4, rg.uniform(4.4, 5.6), "ever", 40 + k))
    for k, y in enumerate(range(-90, 70, 16)):
        if -30 < y < 30: continue
        s.append(tree(-25.5 + (k % 2) * 2, y, rg.uniform(3.8, 4.8), "ever", 70 + k))
        if y > -60: s.append(tree(143.5 - (k % 2) * 2, y, rg.uniform(3.8, 4.8), "ever", 90 + k))
    # everything from the shade garden to the front pond is unchanged from rev. C
    rest = _Y.yard()
    a = rest.index('<path class="bed" d="' + d(blob(-4.4, 33.4, 4.2, 20, seed=8, k=10, jit=.08)))
    b = rest.index('<path class="bfence"')
    s.append(rest[a:b])
    # pool barrier: the house's back wall is part of it, the fence wraps the yard and the primary garden
    s.append('<path class="bfence" d="M0,24 L-11,24 M-15,24 L-22,24 L-22,-92 L96,-92 L96,-56 M96,-51 L96,-30 L116,-30 L116,-2.5 L106,-2.5"/>')
    # the axis from the front doors through the glass wall to the falls
    s.append(f'<line class="axisl" x1="{AXIS}" y1="33.4" x2="{AXIS}" y2="-37.8"/>')
    s.append(lights([(35.6, -39.4), (39.4, -39.4), (25.6, -24.4), (20, -16), (48, -14), (66, -18), (36.4, 1.8), (55, -47.6), (72, -40), (44.6, -49),
                     (81.6, -17), (23.4, -45.4), (52.4, -46.2), (91.6, -40.4), (62, -59), (2, -30), (37.4, -73.4), (95, -10), (60.4, 63.4), (94.2, -31.6)]))
    return "".join(s)
