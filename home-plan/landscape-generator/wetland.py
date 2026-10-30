"""Wetland tie-in study: three ways to make the wetland filter part of the rec pond. Run: python3 wetland.py OUT.html"""
import sys, math, random, re
sys.path.insert(0, '.')
OUT = sys.argv[1] if len(sys.argv) > 1 else '/mnt/project-files/home-plan/pond-wetland-study.html'
_src = open('options.py').read().split('# ---------------------------------------------------------------- 0. current')[0]
sys.argv = ['options.py', OUT]
exec(_src)  # shared helpers from the shape options page: falls, wetland, stream, steps, deck, pond_water, L, rects, gal, Y, H, T, CSS

SW = Y.SW
POND_A = area(SW)
GAL0 = gal(Y.SW, Y.Z5, Y.Z8)
FLOW = GAL0                 # one turnover an hour, gph
CENT = (2000, 3000)         # gph one full Centipede module handles (Splash Supply Co.)
FALLS_GPH_FT = 1500         # residential waterfall flow per foot of spillway (Aquascape)
MOD_L, MOD_W, MOD_STEP = 2.8, 1.33, 3.6   # Centipede V2 is 33.5" x 16"; 9" gap between modules
VIEW = (36, 46, 5.8)        # sofa: plan x, y and eye height above pond water (2 ft slab + 3.8 ft seated)
TERR = (40, 2)              # standing on the terrace
BLIND = False               # True draws plain plans with no labels, sight lines or pipes


def back_chain(x0, x1, ymax, off):
    """Pond edge points on the back shore between x0 and x1 (right to left, as SW runs), pushed out by `off`."""
    o = offset(SW, off)
    return [o[i] for i, p in enumerate(SW) if x0 <= p[0] <= x1 and p[1] <= ymax]


def near(poly, ref, tol):
    """Feet of `poly`'s edge that lie within `tol` ft of `ref`'s edge."""
    out = 0
    for i in range(len(poly)):
        a, b = poly[i], poly[(i + 1) % len(poly)]
        m = ((a[0] + b[0]) / 2, (a[1] + b[1]) / 2)
        if min(math.dist(m, q) for q in ref) <= tol:
            out += math.dist(a, b)
    return out


def length(c):
    return sum(math.dist(a, b) for a, b in zip(c, c[1:]))


def perim(p):
    return length(p + p[:1])


def plants(poly, seed, dens=.5, box=None):
    pr = random.Random(seed); s = []
    xs = [p[0] for p in poly]; ys = [p[1] for p in poly]
    for _ in range(int(area(poly) * dens)):
        x, y = pr.uniform(min(xs), max(xs)), pr.uniform(min(ys), max(ys))
        if not Y.inside((x, y), poly) or (box and Y.inside((x, y), box)):
            continue
        k = pr.random()
        if k < .42: s.append(tuft(x, y, pr.uniform(.8, 1.3), "tf"))
        elif k < .68: s.append(tuft(x, y, pr.uniform(.9, 1.4), "tf2"))
        elif k < .84: s.append(f'<circle class="pk" cx="{x:.2f}" cy="{y:.2f}" r=".55"/><circle class="pkf" cx="{x:.2f}" cy="{y - .1:.2f}" r=".22"/>')
        else: s.append(f'<circle class="ir" cx="{x:.2f}" cy="{y:.2f}" r=".5"/>')
    return "".join(s)


def lip(chain, seed, cls="st3", r=(.45, .8), every=1.6):
    """Low flat stones along a wetland lip where water sheets into the pond."""
    rg = random.Random(seed); s = []; acc = 0
    for a, b in zip(chain, chain[1:]):
        acc += math.dist(a, b)
        if acc >= every:
            acc = rg.uniform(-.3, .3); s.append(rock(a[0], a[1], rg.uniform(*r), rg, flat=True, cls=cls))
    return "".join(s)


def sheet(chain, n=3):
    """Short foam ticks showing water sheeting over a lip toward the pond."""
    s = []
    for i in range(1, len(chain) - 1, n):
        (xa, ya), (xb, yb) = chain[i - 1], chain[i + 1]
        L_ = math.hypot(xb - xa, yb - ya) or 1; nx, ny = (yb - ya) / L_, -(xb - xa) / L_
        x, y = chain[i]
        s.append(f'<path class="foam2" d="M{x:.2f},{y:.2f} L{x + nx * 1.1:.2f},{y + ny * 1.1:.2f}"/>')
    return "".join(s)


def modules(strings):
    """Centipede modules laid along each string; returns (svg, count)."""
    s, n = [], 0
    for c in strings:
        c = catmull(c, False, 6)
        pts = walk(c, MOD_STEP)
        for a, b in zip(pts, pts[1:]):
            cx, cy = (a[0] + b[0]) / 2, (a[1] + b[1]) / 2
            ang = math.degrees(math.atan2(b[1] - a[1], b[0] - a[0]))
            s.append(f'<rect class="cmod" x="{cx - MOD_L / 2:.2f}" y="{cy - MOD_W / 2:.2f}" width="{MOD_L}" height="{MOD_W}" rx=".3" transform="rotate({ang:.1f} {cx:.2f} {cy:.2f})"/>')
            n += 1
    return ("" if BLIND else "".join(s)), n


def pipe(pts):
    """Return line from the pump vault, drawn dashed."""
    if BLIND: return ""
    c = catmull(pts, False, 6); (xa, ya), (xb, yb) = c[-2], c[-1]
    a = math.atan2(yb - ya, xb - xa)
    head = [(xb, yb), (xb - 1.3 * math.cos(a - .45), yb - 1.3 * math.sin(a - .45)), (xb - 1.3 * math.cos(a + .45), yb - 1.3 * math.sin(a + .45))]
    return f'<path class="pipe" d="{d(c, False)}"/><polygon class="pipeh" points="{" ".join(f"{x:.2f},{y:.2f}" for x, y in head)}"/>'


def base_pond(skip_back):
    """Swim pond, beach, steps, deck and edge boulders, minus boulders on the shore the wetland now owns."""
    return (pond_water(Y.SW, Y.Z5, Y.Z8, Y.BEACH, Y.BAY) + steps(36.4, -8.1, 8.2) +
            Y.edge_rocks(Y.SW, 2.15, .85, 1.75, .45, Y.SKIP_POND + skip_back, 51) +
            rock(26.6, -41.8, 3.3, random.Random(77), flat=True, cls="slab") + deck(46.4, -15.2, 10.8, 10.8) +
            '<rect class="vault" x="77.6" y="-15.6" width="3.4" height="2.6" rx=".3"/>')


def lilies(pts):
    return "".join(lily(x, y, r, a) for x, y, r, a in pts)


COVE_LILIES = [(64.4, -24.2, .9, 20), (66, -26.4, .75, 140), (63.2, -27.4, .7, 260), (62.6, -22.6, .65, 200)]
VAULT_RUN = [(79.3, -15.6), (80.6, -26), (79, -38), (74.6, -48)]


def sightlines(target):
    """View cone from the sofa through the back windows, and the sight axes from the sofa and the terrace to the falls."""
    if BLIND: return ""
    ex, ey, _ = VIEW
    def ray(wx, wy, y_end=-84):
        t = (y_end - ey) / (wy - ey); return ex + (wx - ex) * t, y_end
    l, r = ray(27, 34), ray(43, 34)
    return (f'<path class="vcone" d="M{ex},{ey} L{l[0]:.1f},{l[1]} L{r[0]:.1f},{r[1]} Z"/>'
            f'<line class="vaxis" x1="{ex}" y1="{ey}" x2="{target[0]}" y2="{target[1]}"/>'
            f'<line class="vaxis t" x1="{TERR[0]}" y1="{TERR[1]}" x2="{target[0]}" y2="{target[1]}"/>'
            f'<circle class="veye" cx="{TERR[0]}" cy="{TERR[1]}" r=".8"/>')


def secline(x, y0, y1, tag):
    if BLIND: return ""
    return (f'<line class="secl" x1="{x}" y1="{y0}" x2="{x}" y2="{y1}"/>'
            f'<text class="sect" x="{x + .7}" y="{y1 + 1.6}">{tag}</text>')


def numbered(items):
    return "".join(f'<g class="co"><circle cx="{x}" cy="{y}" r="1.1"/><text x="{x}" y="{y + .42}">{n}</text></g>' for n, x, y in items)


VB = (8, -78, 82, 92)
VB_BLIND = (12, -79, 74, 75)


def frame2(inner, labels, aria):
    x, y, w, h = VB_BLIND if BLIND else VB
    terr = Y.flagstones((8, -12, 84, 22), 2.5, "cTerr", 4)
    sc = (f'<g class="scale"><rect x="{x + 2}" y="{y + 2.5}" width="5" height=".5"/><rect class="o" x="{x + 7}" y="{y + 2.5}" width="5" height=".5"/>'
          f'<rect x="{x + 12}" y="{y + 2.5}" width="10" height=".5"/><text x="{x + 2}" y="{y + 4.8}">0</text><text x="{x + 7}" y="{y + 4.8}">5</text>'
          f'<text x="{x + 12}" y="{y + 4.8}">10</text><text x="{x + 20}" y="{y + 4.8}">20 ft</text></g>')
    return (f'<svg class="plan ls zoom opt{" blind" if BLIND else ""}" viewBox="{x} {y} {w} {h}" role="img" aria-label="{aria}">{Y.defs()}'
            f'<rect fill="url(#lawn)" x="{x}" y="{y}" width="{w}" height="{h}"/>'
            f'<path class="grout" d="{d(Y.TERRACE)}"/>{terr}{inner}{H["building"]("sk")}{"" if BLIND else labels + sc}</svg>')


# ---------------------------------------------------------------- 0. current (rev. B)
def opt_current():
    mods, n = modules([[(25, -57.4), (42, -56.6), (59, -58.6)], [(30, -62.4), (42, -63.6), (54, -62.4)]])
    s = [sightlines((41.2, -48)), wetland(Y.WL_REVB, 9, ((33, -60, 2.6, 1.4), (50, -58.2, 2.2, 1.2))),
         stream(Y.STREAM_C, 2.4, 3.6, 32, rects([(-99, -29.5, 999, 99), (-99, -999, 999, -60)])),
         base_pond([]), falls(41.2, -52.2, 41.2, -45.6, 5.4, 3), lilies(COVE_LILIES), mods,
         pipe(VAULT_RUN + [(66, -64.6), (52, -66.6)]),
         tree(19.6, -52, 4.4, "maple", 1) + tree(57.6, -50.4, 3, "maple", 2), secline(41.2, -74, 12, "1")]
    lab = L(41, -25, "Swim", "lt") + L(42, -69.8, "Wetland on a berm") + L(79.8, -44, "Stream")
    sh = near(Y.WL_REVB, SW, 2.0)
    m = dict(wl=Y.WL_REVB, falls_w=5.4, shared=sh, gap="4–6 ft of boulders and berm", mods=n, extra_gal=0, sec_x=41.2,
             outlets=[("Falls", 5.4), ("Stream", 2.4)], pass_gap=False)
    return frame2("".join(s), lab, "Current wetland: an oval bed on a berm behind the falls, joined to the pond only by a 5 ft falls and a looping stream."), m


# ---------------------------------------------------------------- A. headwater crescent
A_INNER = back_chain(31, 66, -31, 1.1)            # stone lip just outside the pond edge, right to left
A_OUTER = catmull([(31.2, -45.6), (30.4, -50.6), (33.6, -56.4), (40, -60.4), (47.6, -61.4), (55.4, -58.4), (61.6, -53), (66.6, -46.4),
                   (70.4, -39.4), (71.2, -33.4), (68.6, -30.4)], False, 8)
A_WL = A_OUTER + A_INNER                           # outer runs left to right, inner comes back right to left
A_UP = blob(42.2, -54.6, 8.6, 4.6, seed=4, k=9, jit=.07, rot=-4)
A_LIP = [p for p in A_INNER if p[0] > 48]           # lower tier lip: water sheets into the pond here


def opt_a():
    mods, n = modules([[(35, -55.6), (42, -56.4), (49, -55.4)], [(52.6, -56.2), (58.6, -51.6), (63.6, -45.6), (67, -38.6), (67.4, -33.8)],
                       [(51.6, -47.6), (57.6, -44.6), (61.8, -39.2), (63.8, -35.4)], [(36.6, -59.6), (46, -60.2)]])
    s = [sightlines((41.2, -48)), f'<path class="berm" d="{d(offset(A_WL, 6))}"/>',
         f'<path fill="url(#grav)" class="wlb" d="{d(A_WL)}"/>', f'<path class="tier" d="{d(A_UP)}"/>', mods,
         plants(A_WL, 5, .55, box=blob(41.2, -49.5, 3.6, 2.6, seed=1, k=7)),
         f'<path class="w1" d="{d(blob(37.4, -56.2, 2.2, 1.1, seed=2, k=7))}"/><path class="w1" d="{d(blob(60.6, -48.4, 2.0, 1.1, seed=3, k=7, rot=-35))}"/>',
         Y.edge_rocks(A_OUTER + [A_OUTER[-1]], 2.4, .9, 1.6, .55, [lambda p: p[1] > -33], 31),
         Y.edge_rocks(A_UP, 2.0, .5, .9, 0, [lambda p: p[1] > -51], 33, cls="st3"),
         base_pond([lambda p: 30 < p[0] < 66.5 and p[1] < -30.5]),
         lip(A_INNER, 7), sheet(A_LIP, 3),
         falls(41.2, -51.0, 41.2, -45.8, 7.0, 3), lilies(COVE_LILIES + [(56, -37.6, .7, 40), (52.4, -39.4, .6, 210)]),
         '<path class="w1" d="M68.4,-31.6 C67.4,-30.4 66.6,-29.6 66.0,-28.4 L64.8,-28.8 C65.4,-30 66.2,-31 67.0,-32.2 Z"/>',
         pipe(VAULT_RUN + [(70, -54), (60, -60.6), (50, -62.4)]),
         tree(22.6, -54, 4.4, "maple", 1) + tree(75, -52.6, 3.2, "maple", 2) + tree(58, -67.4, 3.6, "birch", 3),
         secline(41.2, -74, 12, "1")]
    lab = (L(41, -25, "Swim", "lt") + L(42.2, -53.2, "Upper tier +3½′") + L(62.4, -43.2, "Lower tier +1′") +
           numbered([(1, 34.4, -49.6), (2, 51.6, -43.6), (3, 71.2, -29.4), (4, 23, -45)]))
    sh = near(A_WL, SW, 2.0)
    m = dict(wl=A_WL, falls_w=7.0, shared=sh, gap="none: a 1 ft stone lip", mods=n, extra_gal=0, sec_x=41.2,
             outlets=[("Falls", 7.0), ("Lower-tier lip", length(A_LIP)), ("Rill to the lily cove", 2.0)], pass_gap=True)
    return frame2("".join(s), lab, "Option A, headwater crescent: the wetland wraps the back of the pond in two tiers, the upper tier pours over a 7 ft falls and the lower tier sheets over a stone lip and a short rill into the lily cove."), m


# ---------------------------------------------------------------- B. planted margin at pond level
B_INNER = back_chain(31, 68.5, -20, 0)              # the submerged wall follows today's pond edge
B_OUTER = catmull([(31.2, -45.4), (30.6, -50.4), (34.4, -55.6), (41, -58.6), (49, -58.6), (57, -55.4), (64.2, -50), (70, -43), (74, -35.4),
                   (75.4, -27.6), (73.6, -21.6), (68.6, -19.6)], False, 8)
B_WL = B_OUTER + B_INNER
B_SPUR = blob(41.6, -54.6, 5.6, 4.6, seed=9, k=8)


def opt_b():
    clip = '<clipPath id="cMarg"><path d="' + d(B_WL) + '"/></clipPath>'
    rail = B_OUTER[::4] + [B_OUTER[-1]]
    r6, _ = ribbon(rail, 6.5)
    r14, _ = ribbon(rail, 15)
    mods, n = modules([[(47.6, -54.2), (55, -51.6), (62, -46.6), (67.4, -40), (70.6, -32.4), (70.4, -25.2)],
                       [(48.6, -48.6), (56, -46.4), (61.6, -41.8), (65.2, -35.2)], [(32.8, -48.4), (34.8, -53.6)]])
    s = [sightlines((41.2, -48)), clip, f'<path class="w1" d="{d(B_WL)}"/>',
         f'<g clip-path="url(#cMarg)"><path class="zdeep" d="{d(B_WL)}"/><path class="zmid" d="{d(r14)}"/><path class="zsh" d="{d(r6)}"/></g>', mods,
         plants(B_WL, 8, .3, box=B_SPUR),
         Y.edge_rocks(B_OUTER + [B_OUTER[-1]], 2.6, .7, 1.3, .55, [lambda p: p[1] > -21], 35),
         base_pond([lambda p: 30 < p[0] < 69 and p[1] < -19]),
         "" if BLIND else f'<path class="wall" d="{d(B_INNER, False)}"/>',
         f'<path class="berm" d="{d(B_SPUR)}"/>',
         "".join(rock(x, y, r, random.Random(int(x * y))) for x, y, r in ((38.2, -53.4, 2.0), (45.2, -53.8, 2.2), (39.4, -57.6, 1.8), (44.2, -58.2, 1.9), (41.8, -60.6, 1.6))),
         falls(41.4, -51.6, 41.2, -46.0, 6.0, 4),
         lilies([(50, -50.4, .8, 30), (55.6, -48.6, .7, 150), (61, -45, .8, 260), (66, -40, .7, 80), (69, -33, .8, 300), (70.2, -26.4, .7, 10), (35.6, -51.4, .7, 120)] + COVE_LILIES),
         pipe(VAULT_RUN + [(70, -52), (60.6, -57.4), (50.8, -59.4)]),
         "" if BLIND else '<path class="pipe p2" d="M78.6,-15.6 C80,-30 76,-46 66,-58 C58,-64 50,-62.6 45.4,-58.4"/>',
         tree(22.6, -54, 4.4, "maple", 1) + tree(80, -48.6, 3.2, "maple", 2) + tree(58, -64.4, 3.6, "birch", 3),
         secline(55, -72, 12, "1")]
    lab = (L(41, -25, "Swim", "lt") + L(57.6, -56.6, "0–6″ deep") + L(68.6, -45.2, "6–18″") + L(59.6, -41.6, "18–30″") +
           numbered([(1, 33.8, -56.4), (2, 49.4, -43.8), (3, 72.6, -23.6), (4, 23, -45)]))
    m = dict(wl=B_WL, falls_w=6.0, shared=near(B_WL, SW, 1.0), gap="none: same water, wall 9″ under", mods=n,
             extra_gal=area(B_WL) * 1.4 * 7.48, sec_x=55, outlets=[("Over the submerged wall", length(B_INNER))], pass_gap=True)
    return frame2("".join(s), lab, "Option B, planted margin: a shallow planted lagoon wraps the back of the pond at the same water level, behind a stone wall nine inches under the surface. A rock spur carries the falls."), m


# ---------------------------------------------------------------- C. minimal fix
C_INNER = back_chain(33, 53, -38, 1.1)
C_OUTER = catmull([(32.8, -45.2), (30.6, -51.4), (33.2, -58.6), (40, -63.4), (48.6, -63.6), (56, -59.6), (59.4, -52.6), (58.4, -46), (54.4, -42.4)], False, 8)
C_WL = C_OUTER + C_INNER
C_RILL = [(58.6, -50.6), (62.6, -47.6), (65, -42.4), (65.6, -37), (64.6, -32.6)]


def opt_c():
    mods, n = modules([[(33.4, -55.2), (45, -56.6), (56.4, -54.2)], [(36.6, -60.4), (45, -61.4), (53.6, -59.4)]])
    s = [sightlines((41.2, -48)), f'<path class="berm" d="{d(offset(C_WL, 6))}"/>',
         f'<path fill="url(#grav)" class="wlb" d="{d(C_WL)}"/>', mods, plants(C_WL, 9, .55, box=blob(41.2, -49.6, 4.2, 2.8, seed=1, k=7)),
         f'<path class="w1" d="{d(blob(36.4, -56, 2.2, 1.1, seed=2, k=7))}"/>',
         stream(C_RILL, 2.2, 3.0, 36, rects([(-99, -33.6, 999, 99), (-99, -999, 59.8, -49)])),
         Y.edge_rocks(C_OUTER + [C_OUTER[-1]], 2.4, .9, 1.6, .55, [lambda p: p[1] > -44.5 and 34 < p[0] < 54], 31),
         base_pond([lambda p: 33 < p[0] < 53 and p[1] < -39]),
         lip(C_INNER, 9), falls(41.2, -51.0, 41.2, -45.8, 8.0, 3), lilies(COVE_LILIES),
         pipe(VAULT_RUN + [(66, -60), (56, -65.6)]),
         tree(22.6, -54, 4.4, "maple", 1) + tree(71.6, -50, 3.2, "maple", 2), secline(41.2, -74, 12, "1")]
    lab = L(41, -25, "Swim", "lt") + L(45, -66.2, "Wetland +3½′") + numbered([(1, 33.4, -48.4), (2, 68.8, -44), (4, 23, -45)])
    m = dict(wl=C_WL, falls_w=8.0, shared=near(C_WL, SW, 2.0), gap="none at the falls; lawn on both sides", mods=n, extra_gal=0, sec_x=41.2,
             outlets=[("Falls", 8.0), ("Rill", 2.2)], pass_gap=False)
    return frame2("".join(s), lab, "Option C, minimal fix: the same oval wetland pulled forward against the pond, a wider 8 ft falls, and the stream shortened to a rill that hugs the right shore."), m


OPTS = [("current", opt_current), ("a", opt_a), ("b", opt_b), ("c", opt_c)]
FIG, M, MINI = {}, {}, {}
for k, f in OPTS:
    FIG[k], M[k] = f()
BLIND = True
for k, f in OPTS:
    MINI[k] = f()[0]
BLIND = False


# ---------------------------------------------------------------- sections
def x_cross(poly, x):
    """y values where the vertical line at x crosses poly's edge."""
    ys = []
    for i in range(len(poly)):
        (x1, y1), (x2, y2) = poly[i], poly[(i + 1) % len(poly)]
        if (x1 - x) * (x2 - x) < 0:
            ys.append(y1 + (y2 - y1) * (x - x1) / (x2 - x1))
    return sorted(ys)


VE = 2.0   # vertical exaggeration


def section(k):
    """Cross-section from the sofa to the back of the wetland, along the plan's section line."""
    m = M[k]; x = m['sec_x']; ey = VIEW[1]; ez = VIEW[2]
    U = lambda y: ey - y
    P = lambda y, z: f"{U(y):.2f},{-z * VE:.2f}"
    yb, yf = x_cross(SW, x)[0], x_cross(SW, x)[-1]
    pond = [(yf + .5, .5), (yf, 0)]
    if k in ("current", "a", "c"):
        pond += [(yf - 2.4, -.8), (yf - 4.8, -1.6), (yf - 7.2, -2.4), (yf - 9.4, -5), (yb + 7, -5), (yb + 3.4, -2.2), (yb + 1.2, -1.2)]
    else:
        pond += [(yf - 2, -1.2), (yf - 5, -5), (yb + 6, -5), (yb + 2, -2.6), (yb + .3, -2.6)]
    s = []
    water_top = 0
    if k == "b":
        yo = x_cross(B_WL, x)[0]
        back = [(yb + .3, -.75), (yb - .4, -.75), (yb - .6, -2.4), (yb - 6, -2.4), (yo + 5, -1.4), (yo + 1.5, -.5), (yo, 0), (yo - 1.4, .4), (yo - 8, .3), (-80, 0)]
        ground = pond + back
        water = [(yf, 0)] + pond[2:] + [(yb + .3, -.75), (yb - .4, -.75), (yb - .6, -2.4), (yb - 6, -2.4), (yo + 5, -1.4), (yo + 1.5, -.5), (yo, 0)]
        grav = [(yb - .6, -2.4), (yb - 6, -2.4), (yo + 5, -1.4), (yo + 1.5, -.5), (yo + 1.5, -.1), (yo + 5, -1.0), (yb - 6, -1.6), (yb - .6, -1.6)]
        notes = [(yb - .2, -.75, 2.6, "Wall 9″ under"), ((yb + yo) / 2, -.5, 4.4, "Planted margin, same water"), (yo - 3, .5, 2.2, "Grade, no berm")]
        lip_pt = (yo, 0)
    else:
        lip_y = {"current": -52.2, "a": -51.0, "c": -51.0}[k]
        wl_back = x_cross(m['wl'], x)[0]
        berm_w = {"current": 5.5, "a": 6, "c": 6}[k]
        back = [(yb, 0), (yb - .6, 1.2), (lip_y + 1.2, 3.0), (lip_y, 3.5), (wl_back, 3.6), (wl_back - berm_w * .4, 2.6), (wl_back - berm_w, 0), (-80, 0)]
        if k == "a":   # long, low back slope instead of a ring berm
            back = back[:5] + [(wl_back - 4, 2.6), (wl_back - 14, 0), (-80, 0)]
        ground = pond + back
        water = [(yf, 0)] + pond[2:] + [(yb, 0)]
        grav = [(lip_y - .3, 3.4), (wl_back + .3, 3.4), (wl_back + .8, 1.5), (lip_y - .3, 1.5)]
        notes = [(lip_y, 3.5, 4.8, f"Falls lip +3½′"), ((lip_y + wl_back) / 2, 3.4, 8.2, "Wetland gravel, plants")]
        if k == "a": notes.append((wl_back - 9, 1.4, 4.4, "Long back slope into the meadow"))
        if k == "current": notes.append((wl_back - 2.6, 1.6, 4.6, "Ring berm"))
        lip_pt = (lip_y, 3.5)
        water_top = 3.3
    earth = [(50, .5)] + [(20, .5), (-6, .5)] + ground + [(-80, -10), (50, -10)]
    s.append(f'<polygon points="{" ".join(P(y, z) for y, z in earth)}" fill="#D2BE98"/>')
    s.append(f'<polygon points="{" ".join(P(y, z) for y, z in water)}" fill="url(#swg)"/>')
    s.append(f'<polygon points="{" ".join(P(y, z) for y, z in grav)}" fill="url(#sgr)"/>')
    if k != "b":
        s.append(f'<line x1="{U(lip_pt[0] - .3):.2f}" x2="{U(x_cross(m["wl"], x)[0] + .3):.2f}" y1="{-water_top * VE:.2f}" y2="{-water_top * VE:.2f}" stroke="#3F7F9C" stroke-width=".25" stroke-dasharray=".7 .4"/>')
        for i in range(4):   # falls
            s.append(f'<path d="M{U(lip_pt[0]) + .2:.2f},{-3.4 * VE:.2f} C{U(lip_pt[0]) - 1.4 - i * .2:.2f},{-2.8 * VE:.2f} {U(yb) - .6 - i * .2:.2f},{-1 * VE:.2f} {U(yb) - .6 - i * .25:.2f},0" fill="none" stroke="#fff" stroke-width=".3"/>')
    # liner
    lin = pond[1:] + (back[:5] if k != "b" else back[:6])
    s.append(f'<polyline points="{" ".join(P(y, z - .18) for y, z in lin)}" fill="none" stroke="#1F2328" stroke-width=".35"/>')
    # plants
    rg = random.Random(3)
    plant_span = (lip_pt[0] - .8, x_cross(m['wl'], x)[0] + .8) if k != "b" else (yb - 1, x_cross(B_WL, x)[0] + .3)
    base_z = 3.4 if k != "b" else 0
    yy = plant_span[0]
    while yy > plant_span[1]:
        h = rg.uniform(1.6, 3.2)
        s.append(f'<path d="M{U(yy):.2f},{-base_z * VE:.2f} l{-.4:.2f},{-h * VE:.2f} M{U(yy):.2f},{-base_z * VE:.2f} l.1,{-h * 1.1 * VE:.2f} M{U(yy):.2f},{-base_z * VE:.2f} l.5,{-h * .9 * VE:.2f}" stroke="#5E8A4A" stroke-width=".22" fill="none"/>')
        yy -= rg.uniform(1.0, 1.8)
    # house, porch, terrace
    s.append(f'<rect x="{U(46) - 6:.2f}" y="{-12 * VE:.2f}" width="{U(34) - U(46) + 6:.2f}" height="{10 * VE:.2f}" fill="#EFE6D4" stroke="#3A3F48" stroke-width=".3"/>')
    s.append(f'<line x1="{U(34):.2f}" x2="{U(34):.2f}" y1="{-10.5 * VE:.2f}" y2="{-3 * VE:.2f}" stroke="#7FB3C8" stroke-width=".9"/>')
    s.append(f'<polyline points="{P(34, 12.6)} {P(20, 10.6)}" fill="none" stroke="#3A3F48" stroke-width=".5"/><line x1="{U(20.5):.2f}" x2="{U(20.5):.2f}" y1="{-10.6 * VE:.2f}" y2="{-1.6 * VE:.2f}" stroke="#3A3F48" stroke-width=".3"/>')
    s.append(f'<rect x="{U(34):.2f}" y="{-1.6 * VE:.2f}" width="{U(20) - U(34):.2f}" height="{1.1 * VE:.2f}" fill="#CFC6B6"/>')
    s.append(f'<rect x="{U(20):.2f}" y="{-.5 * VE:.2f}" width="{U(yf + .5) - U(20):.2f}" height=".5" fill="#BFB29A"/>')
    # sight line from the sofa over the falls lip
    ty, tz = lip_pt if k != "b" else (x_cross(B_WL, x)[0], 0)
    far = -82; slope = (tz - ez) / (U(ty) - 0)
    s.append(f'<line x1="0" y1="{-ez * VE:.2f}" x2="{U(far):.2f}" y2="{-(ez + slope * U(far)) * VE:.2f}" stroke="#B0812A" stroke-width=".3" stroke-dasharray="1.2 .7"/>')
    s.append(f'<circle cx="0" cy="{-ez * VE:.2f}" r=".8" fill="#B0812A"/>')
    t = lambda u, z, txt, a="middle", c="sn": f'<text class="{c}" x="{u:.2f}" y="{-z * VE:.2f}" style="text-anchor:{a}">{txt}</text>'
    s.append(t(1.4, ez + 1.6, "Sofa eye, ~6 ft above the water", "start"))
    s.append(t(U(27), -2.2, "Terrace"))
    s.append(t(U((yf + yb) / 2), -3.4, "Swim zone, 5 ft", "middle"))
    for y, z, dz, txt in notes:
        s.append(f'<line x1="{U(y):.2f}" x2="{U(y):.2f}" y1="{-(z + .3) * VE:.2f}" y2="{-(z + dz - .6) * VE:.2f}" stroke="#3A3F48" stroke-width=".15"/>' + t(U(y), z + dz, txt))
    # how much of the wetland's own water the sofa can see
    a_deg = None
    if k != "b":
        wl_back = x_cross(m['wl'], x)[0]
        a_deg = math.degrees(math.atan2(ez - water_top, U(lip_pt[0])) - math.atan2(ez - water_top, U(wl_back)))
    else:
        yo = x_cross(B_WL, x)[0]
        a_deg = math.degrees(math.atan2(ez, U(yb)) - math.atan2(ez, U(yo)))
    pond_deg = math.degrees(math.atan2(ez, U(yf)) - math.atan2(ez, U(yb)))
    m['view_deg'], m['pond_deg'] = a_deg, pond_deg
    w = U(-80) + 4
    return (f'<svg class="plan ls sec" viewBox="-6 {-14 * VE} {w + 2:.1f} {24 * VE + 2}" role="img" aria-label="Section {k}: sofa to the back of the wetland">'
            f'<rect x="-6" y="{-14 * VE}" width="{w + 2:.1f}" height="{24 * VE + 2}" fill="#FBF8F1"/>'
            '<defs><pattern id="sgr" width="1.2" height="1.2" patternUnits="userSpaceOnUse"><rect width="1.2" height="1.2" fill="#D9CDB3"/><circle cx=".3" cy=".4" r=".16" fill="#A3967D"/><circle cx=".9" cy=".9" r=".14" fill="#EEE7D7"/></pattern>'
            '<linearGradient id="swg" x1="0" x2="0" y1="0" y2="1"><stop offset="0" stop-color="#9FCFDF"/><stop offset="1" stop-color="#3F7F9C"/></linearGradient></defs>'
            + "".join(s) + t(-5, -8.8, f"Section 1 at x = {x:g} ft · vertical ×{VE:g}", "start", "sd") + '</svg>')


SEC = {k: section(k) for k in M}


# ---------------------------------------------------------------- numbers
def nums(k):
    m = M[k]; w = m['wl']
    need = (math.ceil(FLOW / CENT[1]), math.ceil(FLOW / CENT[0]))
    falls_gph = m['falls_w'] * FALLS_GPH_FT
    return dict(area=area(w), pct=area(w) / POND_A, perim=perim(w), shared=m['shared'], gap=m['gap'], mods=m['mods'], need=need,
                cap=(m['mods'] * CENT[0], m['mods'] * CENT[1]), falls_gph=falls_gph, rest=FLOW - (falls_gph if k != 'b' else 0),
                extra=m['extra_gal'], view=m['view_deg'], pond_view=m['pond_deg'])


N = {k: nums(k) for k in M}

if __name__ == '__main__' and __import__('os').environ.get('STATS_ONLY'):
    for k, n in N.items():
        print(k, {a: (round(b, 2) if isinstance(b, float) else b) for a, b in n.items()})
    sys.exit()


# ---------------------------------------------------------------- page
def chip(ok, txt):
    return f'<span class="chip {"ok" if ok is True else ("bad" if ok is False else "warn")}">{txt}</span>'


def fk(v): return f"{v / 1000:,.1f}k" if v < 100000 else f"{v / 1000:,.0f}k"


n0, nA, nB, nC = N['current'], N['a'], N['b'], N['c']
LIP_A = length(A_LIP)
rows = []
for k, name in (("current", "Current (rev. B)"), ("a", "A. Headwater crescent"), ("b", "B. Planted margin"), ("c", "C. Minimal fix")):
    n = N[k]; m = M[k]
    fits = n['cap'][1] >= FLOW
    rows.append(f'<tr><td>{name}</td><td class="num">{n["area"]:,.0f} sf · {n["pct"]:.0%}</td><td class="num">{n["shared"]:,.0f} ft</td><td>{n["gap"]}</td>'
                f'<td class="num">{n["mods"]} ({fk(n["cap"][0])}–{fk(n["cap"][1])} gph)</td>'
                f'<td>{chip(n["pct"] >= .3, "Size")} {chip(m["pass_gap"], "No gap")} {chip(fits if k != "c" else False, "Flow")}</td></tr>')
TABLE = "".join(rows)

CSS2 = '''
.vcone{fill:#E8C66A;opacity:.16}.vaxis{stroke:#B0812A;stroke-width:.3;stroke-dasharray:1.2 .8;fill:none}.vaxis.t{stroke-dasharray:.4 .6}.veye{fill:#B0812A}
.secl{stroke:#7A2E2E;stroke-width:.3;stroke-dasharray:1.6 .8}.plan.ls text.sect{font-size:1.4px;font-weight:700;fill:#7A2E2E;text-anchor:start;paint-order:stroke;stroke:#FBF8F1;stroke-width:.35px}
.tier{fill:#CBBE9E;opacity:.5;stroke:#8E7F62;stroke-width:.2}.zdeep{fill:#8EC1D1}.zmid{fill:#AFD5DC}.zsh{fill:#CBE2CF}
.wall{fill:none;stroke:#2F4A58;stroke-width:.4;stroke-dasharray:.9 .5}.cmod{fill:none;stroke:#8A6A2F;stroke-width:.16;stroke-dasharray:.35 .25;opacity:.85}
.pipe{fill:none;stroke:#8A6A2F;stroke-width:.32;stroke-dasharray:1 .5}.pipe.p2{stroke:#6E5A9A}.pipeh{fill:#8A6A2F}
.w-blind{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:14px;margin:14px 0 6px}.w-blind figure{margin:0}
.w-blind figcaption{font:600 .95em/1.2 var(--f-head);margin:0 0 4px;color:var(--ink,#23272E)}
.w-key{margin:6px 0 0}.w-key summary{cursor:pointer;font-weight:600}
.w-flow{display:flex;flex-wrap:wrap;gap:6px 4px;align-items:center;margin:4px 0 12px;font-size:.92em}
.w-flow span{border:1px solid var(--rule,#d9d2c3);border-radius:4px;padding:2px 7px;background:var(--paper2,rgba(0,0,0,.025))}.w-flow i{font-style:normal;opacity:.6}
.w-two{display:grid;grid-template-columns:1fr 1fr;gap:6px 22px}.w-two h4{margin:6px 0 2px;font:600 1em/1.3 var(--f-head)}.w-two ul{margin:0;padding-left:18px}
.plan.sec{margin-top:6px}
@media (max-width:640px){.w-blind,.w-two{grid-template-columns:1fr}}
'''

FLOWS = {
 "a": ["Intake bay", "External pumps, IonGen", f"Manifold with a valve per tier",
       f"Upper tier: ~{fk(nA['falls_gph'])} gph up through gravel", f"7 ft falls", "Swim zone",
       f"Lower tier: ~{fk(nA['rest'])} gph", f"{LIP_A:.0f} ft stone lip (~{nA['rest'] * .85 / LIP_A:,.0f} gph per ft) + rill to the lily cove"],
 "b": ["Intake bay", "External pumps, IonGen", f"~{fk(FLOW)} gph up through the margin gravel", "Over the submerged wall, all along it", "Swim zone",
       f"Separate falls pump, ~{fk(nB['falls_gph'])} gph", "Header behind the rock spur", "6 ft falls"],
 "c": ["Intake bay", "External pumps", f"{nC['mods']} Centipedes, good for {fk(nC['cap'][0])}–{fk(nC['cap'][1])} gph", f"8 ft falls (~{fk(nC['falls_gph'])} gph)",
       f"Rill gets the other ~{fk(nC['rest'])} gph"],
}


def flow(steps):
    return '<div class="w-flow">' + "<i>→</i>".join(f"<span>{x}</span>" for x in steps) + '</div>'


tpl = open(T).read()
head, rest = tpl.split('<main class="doc">')
head = head.replace('<title>Ink & Brass template</title>', '<title>Pond wetland study</title>')
head = re.sub(r'<!-- House style: Ink & Brass.*?-->\n', '', head)
head = head.replace('</style>', H['CSS'] + CSS + CSS2 + '</style>')

blind_order = [("W", "b"), ("X", "current"), ("Y", "c"), ("Z", "a")]
blind = "".join(f'<figure><figcaption>{lt}</figcaption>{MINI[k]}</figure>' for lt, k in blind_order)
KEYNAME = {"current": "the current plan", "a": "option A", "b": "option B", "c": "option C"}

body = f"""<main class="doc">
  <header class="d-head">
    <div class="d-top"><span class="d-type">New home build</span><span class="d-date">Pond wetland · Oct 26, 2026</span></div>
    <h1 class="d-title">Making the wetland part of the pond</h1>
    <p class="d-lead">You're right about the wetland. As drawn, it's an oval bed on its own ring berm, set back 4 to 6 ft from the water. It touches the pond only through a 5 ft falls, and a long stream loops away from it like a teapot handle. Three fixes are below. I recommend A: wrap the wetland around the back of the pond as its upper shore, in two tiers, so water visibly spills from it into the pond along about 30 ft.</p>
  </header>

  <div class="d-stats">
    <div><div class="l">Shared edge today</div><div class="v">{n0['shared']:.0f} ft</div><div class="s">option A: {nA['shared']:.0f} ft · B: {nB['shared']:.0f} ft</div></div>
    <div><div class="l">Wetland, option A</div><div class="v">{nA['area']:,.0f} sf</div><div class="s">{nA['pct']:.0%} of the pond; 30% is the floor</div></div>
    <div><div class="l">Centipedes that fit, A</div><div class="v">{nA['mods']}</div><div class="s">{nA['need'][0]}–{nA['need'][1]} needed for one turnover an hour</div></div>
  </div>

  <div class="d-call"><b>Bottom line</b><span>Go with A. It's the standard Aquascape upflow wetland that certified contractors already build. It keeps the falls on the living room sight line and makes it wider, 7 ft instead of 5. The wetland stops being a separate island and becomes the pond's back shore. B gives you even more of a single water body, but it needs a second pump for the falls and is less familiar to Aquascape crews. C is the cheapest change, but it doesn't solve the look or the filter size.</span></div>

  <h2 class="d-h2">Try this first: which one looks like one pond?</h2>
  <p class="d-p">Before reading further, show your wife these four plans with no labels and ask which looks like one body of water and which has a piece that looks separate. They're the same pond at the same scale. Only the wetland changes.</p>
  <div class="w-blind">{blind}</div>
  <details class="w-key"><summary>Show which is which</summary><p class="d-p">{" · ".join(f"{lt} is {KEYNAME[k]}" for lt, k in blind_order)}. If anyone picks out the wetland in A or B as a separate piece, the fix didn't work.</p></details>

  <h2 class="d-h2">What's wrong with the current wetland</h2>
  <figure class="d-fig wide">{FIG['current']}</figure>
  <dl class="d-rows">
    <dt>It's an island</dt><dd>It's an oval drawn on its own, then given a ring berm and a full ring of boulders. Nothing in its shape responds to the pond. Measured on the plan, {n0['shared']:.0f} ft of its {n0['perim']:.0f} ft edge touches the pond. The only connection is the 5 ft gap the falls drops through.</dd>
    <dt>The stream pulls away</dt><dd>The stream leaves the wetland's far right end and loops 8 to 10 ft out from the pond before it comes back to the lily cove. That loop is the teapot handle.</dd>
    <dt>The flow doesn't add up</dt><dd>Aquascape sizes a residential falls at 1,500 gph per foot of width. A 5.4 ft falls carries about {fk(n0['falls_gph'])} gph. The other ~{fk(n0['rest'])} gph of the turnover would have to go down a 2½ to 3½ ft stream, which makes it a whitewater chute. The alternative is starving the falls.</dd>
    <dt>From the house it's mostly fine</dt><dd>From the sofa, about 6 ft above the water and 95 ft away, the wetland's water surface fills about {n0['view']:.1f}° of your view. The whole pond fills {n0['pond_view']:.1f}°. You see the falls and a band of plants, not the bed. The disconnect shows from the terrace edge, the loop path, any upstairs bonus room window, and on the plan. That's also where the fix has to show.</dd>
  </dl>

  <h2 class="d-h2">Two proven ways to build a wetland</h2>
  <div class="w-two">
    <div><h4>Aquascape upflow wetland (A and C)</h4><ul><li>Pumps push water into Centipede modules under about 2 ft of river rock. It rises through the gravel and plant roots and spills out the top.</li><li>The wetland sits higher than the pond, so the falls comes out of it.</li><li>A typical ecosystem pond uses a wetland of 15 to 20% of the pond's surface, up to 30%. For a swim pond the plan holds 30% or more.</li></ul></div>
    <div><h4>Planted margin (B, European natural pool style)</h4><ul><li>The planted zone is part of the same water, separated from the swim zone by a wall a few inches under the surface. Water moves through the gravel and over the wall.</li><li>European designers size this zone at least equal to the swim area, and twice as big is better. That's for ponds with no other treatment. This plan keeps the Aquascape gear (skim cove, IonGen), so a smaller margin is closer to Aquascape practice than to that standard.</li></ul></div>
  </div>

  <h2 class="d-h2">A. Headwater crescent <span class="chip ok">Recommended</span></h2>
  <p class="d-p">The wetland becomes the pond's back shore. It runs from just past the jump rock around to the lily cove, separated from the water by a 1 ft stone lip instead of a strip of lawn. The upper tier, at +3½ ft, sits behind the falls and feeds it (1). The lower tier, about 1 ft above the water, runs along the right side. Its water sheets over the low stone lip (2) and down a short rill into the lily cove (3), so you see water leaving the wetland along about 30 ft of shore. The ring berm is replaced by a long, low slope that runs back into the meadow, so the rise reads as landform, not a mound. The jump rock (4) and the dry shore on the left stay as they are. The long stream is gone. The lower tier's lip and the rill do its job right against the pond.</p>
  {flow(FLOWS['a'])}
  <figure class="d-fig wide">{FIG['a']}</figure>
  <figure class="d-fig wide">{SEC['a']}</figure>
  <p class="d-note">Gold dashes are the return line from the pump vault. Brown dashed boxes are the {nA['mods']} Centipede modules (33½″ × 16″) laid out in four strings, two per tier, with a valve per string so the falls and the lip can be balanced. The gold wedge is the view from the sofa through the back windows.</p>

  <h2 class="d-h2">B. Planted margin</h2>
  <p class="d-p">The wetland becomes water. A shallow planted lagoon wraps the back and right of the pond at the same water level. It's separated from the swim zone by a stone-capped wall 9 inches under the surface (dashed), which marks where swimmers stop. It's planted in three depth bands: 0 to 6 inches at the outer edge, 6 to 18 inches, and 18 to 30 inches along the wall. From any angle it reads as one pond with a marshy back edge, like a bayou bank. The catch is the falls. With the wetland at water level, nothing sits high enough to feed it, so a rock spur (1) carries a separate header and pump (purple line). The margin adds about {nB['extra']:,.0f} gallons of shallow water, which warms fast in a Louisiana summer and is where string algae and mosquitoes start. Plan on fish.</p>
  {flow(FLOWS['b'])}
  <figure class="d-fig wide">{FIG['b']}</figure>
  <figure class="d-fig wide">{SEC['b']}</figure>

  <h2 class="d-h2">C. Minimal fix</h2>
  <p class="d-p">Same oval, pulled forward against the pond. The falls widens to 8 ft (1) and the stream becomes a rill that hugs the right shore (2). It's the cheapest change, but it only half works. The sides still meet lawn, so it still reads as a mound with a falls in it. At {nC['area']:,.0f} sf, only {nC['mods']} Centipedes fit, good for {fk(nC['cap'][0])}–{fk(nC['cap'][1])} gph. That's short of the ~{fk(FLOW)} gph a one-hour turnover needs.</p>
  {flow(FLOWS['c'])}
  <figure class="d-fig wide">{FIG['c']}</figure>
  <figure class="d-fig wide">{SEC['c']}</figure>

  <h2 class="d-h2">Side by side</h2>
  <p class="d-note">Measured from the drawings. Shared edge is the part of the wetland's edge within 2 ft of the pond's water. Flow uses 2,000–3,000 gph per full Centipede and a target of one turnover an hour, about {fk(FLOW)} gph for this pond's ~{round(GAL0, -3):,.0f} gallons. For two turnovers an hour you'd need {math.ceil(2 * FLOW / CENT[1])}–{math.ceil(2 * FLOW / CENT[0])} modules. None of the options fits that without a bigger wetland.</p>
  <div class="d-tw"><table>
    <thead><tr><th>Option</th><th class="num">Wetland</th><th class="num">Shared edge</th><th>Between wetland and pond</th><th class="num">Centipedes that fit</th><th>Checks</th></tr></thead>
    <tbody>{TABLE}</tbody>
  </table></div>

  <h2 class="d-h2">Planting by zone</h2>
  <p class="d-note">All are native to Acadiana and zone 9a. In A and C the water sits an inch or two under the gravel surface, so most of the wetland is bog planting. Lilies stay on the pond's own shelf.</p>
  <div class="d-tw"><table>
    <thead><tr><th>Zone</th><th>Where</th><th>Plants</th></tr></thead>
    <tbody>
      <tr><td>Wet gravel, core</td><td>A and C upper tier, around the falls</td><td>Louisiana iris (I. fulva, I. giganticaerulea), pickerelweed, golden canna, swamp lily (Crinum americanum)</td></tr>
      <tr><td>Wet gravel, back edge</td><td>A and C, where the wetland meets the slope</td><td>Scarlet swamp hibiscus, cardinal flower, spider lily, soft rush</td></tr>
      <tr><td>Sheeting lip, 0–3″</td><td>A lower-tier lip and rill</td><td>American water willow, lizard's tail, bulltongue arrowhead</td></tr>
      <tr><td>0–6″ water</td><td>B outer band</td><td>Louisiana iris, lizard's tail, cardinal flower, soft rush, spider lily</td></tr>
      <tr><td>6–18″ water</td><td>B middle band</td><td>Pickerelweed, bulltongue arrowhead, golden canna, swamp lily</td></tr>
      <tr><td>18–30″ water</td><td>B inner band, and the pond shelf in every option</td><td>Fragrant water lily, spatterdock; coontail and eelgrass under water for oxygen</td></tr>
    </tbody>
  </table></div>

  <h2 class="d-h2">What an Aquascape contractor should confirm on site</h2>
  <dl class="d-rows">
    <dt>Wetland flow</dt><dd>The Centipede count and layout for the pond's real volume, and whether they'd rather have a bigger wetland than these numbers. Aquascape sizes wetlands in its own course and says to use a certified contractor.</dd>
    <dt>Pump curve</dt><dd>~{fk(FLOW)} gph at the real head: a 3½ ft lift, the pipe run around the pond, and the gravel. Pump size comes from the curve at that head, not the label.</dd>
    <dt>Liner at the lip</dt><dd>Whether the wetland and pond share one liner with a stone lip on top (A), or need a separate liner and a capillary break. Also how the lip stays level enough to sheet evenly instead of dribbling at one low spot.</dd>
    <dt>Grade and soil</dt><dd>A spot survey of the lot. I didn't pull LiDAR, because I don't have the parcel. Louisiana's statewide LiDAR is free through LSU's Atlas and USGS 3DEP if you want it. They also need to check whether the pond spoil (likely clay) can build the back slope, and how high the water table sits under the liner.</dd>
    <dt>Rain overflow</dt><dd>Where a 6-inch Louisiana rain leaves the pond, so it doesn't overtop the lip and wash wetland gravel into the swim zone.</dd>
    <dt>For B only</dt><dd>Whether they build planted-margin ponds at all, the wall height, and the second pump for the falls.</dd>
  </dl>

  <footer class="d-foot">Concept study, not a construction drawing. Measurements come from the landscape generator's plan geometry, in feet, on the same axes as the house plan. Sources: Aquascape, <a href="https://support.aquascapeinc.com/hc/en-us/articles/48506919478036-Waterfall-What-flow-rate-is-needed-for-a-waterfall">What flow rate is needed for a waterfall</a> (1,500 gph per foot, residential); Aquascape, <a href="https://support.aquascapeinc.com/hc/en-us/articles/4412607329044-Wetland-Filter-System">Wetland Filter System</a> and <a href="https://www.aquascapeinc.com/products/centipede-module">Centipede Module</a> (33½″ × 16″); Splash Supply Co., <a href="https://splashsupplyco.com/wetland-filtration-using-aquascape-snorkel-centipede/">Wetland filtration using Snorkel and Centipede</a> (15–20% typical, up to 30%; 2,000–3,000 gph per Centipede; two 8–10″ rock layers); Natural Waterscapes, <a href="https://expert.naturalwaterscapes.com/learn/construction/natural-swimming-ponds/">Natural swimming ponds</a> (regeneration zone at least 1:1, 1:2 better; 1–3 ft deep; submerged partition wall). The 30% floor for swim ponds comes from the Pond Trade Magazine articles cited in the landscape plan. I couldn't get the German FLL guideline text, so nothing here relies on it.</footer>
</main>"""
open(OUT, 'w').write(head + body + '\n</body>\n</html>\n')
print("wrote", OUT)
