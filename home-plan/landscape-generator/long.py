"""Long pond study: a lap pond that runs across the back of the house, compared with rev. C. Run: python3 long.py OUT.html"""
import sys, math, random, re
sys.path.insert(0, '.')
OUT = sys.argv[1] if len(sys.argv) > 1 else '/mnt/project-files/home-plan/long-pond-option.html'
_w = open('wetland.py').read().split('# ---------------------------------------------------------------- 0. current (rev. B)')[0]
sys.argv = ['wetland.py', OUT]
exec(_w)  # options.py helpers plus near, length, perim, plants, lip, sheet, modules, pipe, lilies, sightlines, numbered, CENT, FALLS_GPH_FT, VIEW

# ---------------------------------------------------------------- long pond geometry (feet, house plan axes; y < 0 is the back yard)
LQ = [(8, -4.5), (14, .6), (20, 3.4), (27, 4.8), (36, 5.2), (44.6, 2.6), (50, -2.4), (56, -4.6), (64, -5.4), (72, -6.8), (79, -8.6), (83.4, -12.4),
      (84.6, -18), (83, -23.6), (77, -27), (68, -28.8), (59, -30.4), (51, -33), (46.2, -34.4), (44.6, -37.8), (41, -39.2), (37.4, -37.8),
      (35.6, -34.8), (30, -34.2), (22, -33.6), (14, -31), (8.4, -27.6), (4.6, -23), (3, -16), (3.6, -9)]
LSW = catmull(LQ, True, 10)
LZ5 = catmull([(14, -8), (24, -5), (36, -3.4), (48, -6.6), (60, -10.4), (72, -12.6), (78, -17.6), (74, -22.6), (62, -24.2), (50, -27.4),
               (38, -30.4), (26, -29.6), (16, -27), (11, -21), (10.6, -13)], True, 10)
LZ8 = blob(25.6, -24.4, 7.2, 3.8, seed=3, k=8, jit=.07, rot=-6)
LEDGE = [(28.4, 4.3), (44, 3.0), (43.2, -.6), (29, .6)]                  # 12 in sun ledge off the porch, chaises in the water
LBEACH = blob(10.4, -4.6, 6.2, 3.6, seed=5, k=8, jit=.08, rot=-30)
LCOVE = blob(5.2, -24.6, 3.2, 2.6, seed=2, k=8, jit=.08, rot=20)      # intake bay at the far-left corner, away from the beach
LILY = blob(81.6, -18.6, 3.6, 3.8, seed=8, k=8, jit=.06)             # lily cove at the right end, where the rill comes in
VAULT = (-7.6, -27.2)

_o = offset(LSW, 1.1)
L_INNER = [_o[i] for i, p in enumerate(LSW) if 34 <= p[0] <= 83.6 and p[1] <= -22.6]
L_OUTER = catmull([(34.2, -36.4), (32.8, -43), (37, -50), (45.6, -53.6), (55.6, -52.6), (65.6, -48.6), (75.2, -44.4), (83.6, -38.6),
                   (89, -30.6), (90.2, -24.2), (86.8, -21.2)], False, 8)
L_WL = L_OUTER + L_INNER
L_UP = blob(42.6, -44.6, 8.2, 4.2, seed=4, k=9, jit=.07, rot=-4)
L_LIP = [p for p in L_INNER if p[0] > 50]
FIRE = (12.4, -46)
JUMP = (24.4, -36.2)

NEAR = [p for p in LSW if p[1] > -9.5 and 12 < p[0] < 84]                 # near shore the coping runs along
TERR_L = ([(18, 13), (24, 13), (24, 20), (46, 20), (46, 10), (68, 10), (68, 5), (86, 5), (86, -5.6)] +
          [(x + nx * .2, y + ny * .2) for (x, y), (nx, ny) in [(p, normal_at(LSW, LSW.index(p))) for p in sorted(NEAR, key=lambda p: -p[0])]] + [(14.6, 3.2), (14, 13)])


def lgal():
    return ((area(LSW) - area(LZ5)) * 2 + (area(LZ5) - area(LZ8)) * 5 + area(LZ8) * 8 - area(LEDGE) * 1) * 7.48


def coping():
    """Cut stone coping along the near shore: the terrace ends at the water."""
    rg = random.Random(4); s = []
    pts = sorted(NEAR, key=lambda p: p[0])
    for a, b in zip(pts[::2], pts[2::2]):
        if 28 < (a[0] + b[0]) / 2 < 44.4: continue          # the sun ledge has its own edge
        L_ = math.dist(a, b) or 1; ux, uy = (b[0] - a[0]) / L_, (b[1] - a[1]) / L_
        n = normal_at(LSW, LSW.index(a)); w = 1.5
        q = [(a[0], a[1]), (b[0], b[1]), (b[0] + n[0] * w, b[1] + n[1] * w), (a[0] + n[0] * w, a[1] + n[1] * w)]
        s.append(f'<polygon class="{rg.choice(["slab", "st3", "slab"])}" points="{" ".join(f"{x:.2f},{y:.2f}" for x, y in q)}"/>')
    return "".join(s)


def long_plan(blind=False):
    global BLIND
    BLIND = blind
    mods, n = modules([[(36, -45.4), (42.6, -46.2), (49.4, -45.4)], [(37.4, -48.4), (46, -49)],
                       [(53, -46.8), (61, -43.6), (69, -40.2), (77, -36.8), (83.4, -31.6), (85.4, -25.6)],
                       [(52, -38.4), (60.6, -35), (69.4, -32.6), (77.6, -29.8), (82.6, -25.8)], [(54.6, -42.6), (64, -39), (73, -35.6)], [(55.4, -49.4), (65, -45.6), (75, -41.4), (83.4, -36), (87.4, -29)], [(38.6, -51), (47, -51.6)]])
    clipT = f'<clipPath id="cTerrL"><path d="{d(TERR_L)}"/></clipPath>'
    s = [clipT, sightlines((41, -38)),
         f'<path class="grout" d="{d(TERR_L)}"/>', Y.flagstones((10, -14, 90, 22), 2.5, "cTerrL", 4),
         f'<path class="berm" d="{d(offset(L_WL, 6))}"/>',
         f'<path fill="url(#grav)" class="wlb" d="{d(L_WL)}"/>', f'<path class="tier" d="{d(L_UP)}"/>', mods,
         plants(L_WL, 6, .5, box=blob(41, -39.6, 3.8, 2.6, seed=1, k=7)),
         f'<path class="w1" d="{d(blob(37.4, -45.6, 2.0, 1.0, seed=2, k=7))}"/><path class="w1" d="{d(blob(70.4, -38.2, 2.0, 1.0, seed=3, k=7, rot=-20))}"/>',
         Y.edge_rocks(L_OUTER + [L_OUTER[-1]], 2.4, .9, 1.6, .55, [lambda p: p[1] > -22], 31),
         Y.edge_rocks(L_UP, 2.0, .5, .9, 0, [lambda p: p[1] > -41], 33, cls="st3"),
         f'<path class="w1" d="{d(LSW)}"/><path class="w1" d="{d(LCOVE)}"/><path class="w1" d="{d(LILY)}"/>',
         f'<path fill="url(#grav)" d="{d(LBEACH)}"/>', f'<path class="tint" d="{d(LSW)}"/>',
         f'<path class="w2" d="{d(LZ5)}"/><path fill="url(#gDeep)" d="{d(LZ8)}"/>',
         f'<polygon class="slab" opacity=".55" points="{" ".join(f"{x},{y}" for x, y in LEDGE)}"/>',
         Y.edge_rocks(LSW, 2.15, .85, 1.75, .45, [lambda p: p[1] > -9.5 and p[0] > 12, lambda p: p[1] < -22 and p[0] > 33.6, lambda p: p[0] < 16 and p[1] > -9,
                                                   lambda p: 21 < p[0] < 28 and p[1] < -32], 51),
         Y.edge_rocks(LCOVE, 1.6, .55, 1.0, .45, [lambda p: p[0] > 7], 52),
         coping(), lip(L_INNER, 7), sheet(L_LIP, 3),
         falls(41, -41.2, 41, -36.4, 7.0, 3),
         rock(JUMP[0], JUMP[1], 3.3, random.Random(77), flat=True, cls="slab"),
         steps(33.6, .4, 7.4, 3, -2.0),
         lilies([(80.2, -16.8, .8, 20), (82.6, -19.6, .7, 140), (80.6, -21, .7, 260), (83, -16.4, .6, 200), (66, -27, .7, 40), (58.6, -28.8, .6, 210)]),
         '<path class="w1" d="M86.4,-22.4 C85.8,-21.4 85.2,-20.8 84.6,-20.0 L83.6,-20.6 C84.2,-21.4 84.8,-22.2 85.4,-23.0 Z"/>',
         # chaises on the sun ledge and the terrace table
         "".join(f'<rect class="fu" x="{x}" y="0.9" width="2.2" height="3.6" rx=".4"/>' for x in (31, 34.4, 37.8, 41.2)),
         '<circle class="umb" cx="58" cy="4" r="3.2"/><circle class="fu2" cx="58" cy="4" r=".25"/>',
         # fire pit across the water
         f'<circle class="dg" cx="{FIRE[0]}" cy="{FIRE[1]}" r="7"/><circle class="edge" cx="{FIRE[0]}" cy="{FIRE[1]}" r="7"/>'
         f'<circle class="st2" cx="{FIRE[0]}" cy="{FIRE[1]}" r="2"/><circle class="pit" cx="{FIRE[0]}" cy="{FIRE[1]}" r="1.3"/><circle class="fire" cx="{FIRE[0]}" cy="{FIRE[1]}" r=".7"/>',
         "".join(Y.chair_ad(FIRE[0] + 4.6 * math.cos(math.radians(a)), FIRE[1] + 4.6 * math.sin(math.radians(a)), a - 90) for a in (20, 70, 120, 160, 200, 340)),
         Y.stepping([(-1, 6), (-3.6, -8), (-4, -20), (-1, -34), (4.6, -42)], 2.3, 2) + Y.stepping([(20.6, -48), (28, -54.6), (36, -59)], 2.3, 3),
         f'<rect class="vault" x="{VAULT[0]}" y="{VAULT[1]}" width="3.4" height="2.6" rx=".3"/>',
         "".join(shrub(x, y, 1.15, "sh", seed=int(x * y)) for x, y in ((-9, -23.4), (-4.4, -24.2), (-9.6, -30.6), (-4.6, -31))),
         tree(23.4, -44.6, 4.2, "maple", 1) + tree(91.6, -36.4, 3.2, "maple", 2) + tree(62, -59, 3.6, "birch", 3) + tree(-14, -46, 8.4, "dec", 4),
         pipe([(VAULT[0] + 1.7, VAULT[1]), (-2, -44), (12, -58), (30, -58.6), (40, -53.6)]),
         "" if blind else secline(40, -64, 30, "1")]
    BLIND = False
    lab = (L(52, -16, "Lap lane, 5 ft deep", "lt") + L(25.6, -24.8, "8 ft") + L(36.4, 6.6, "Sun ledge, 12″") + L(10.4, -3.4, "Beach") +
           L(42.6, -45.6, "Upper tier +3½′") + L(70, -33.6, "Lower tier +1′") + L(5.2, -21.4, "Intake") + L(81.4, -13.8, "Lilies") +
           L(12.4, -54.6, "Fire pit across the water") + L(64, -1.2, "Terrace"))
    m = dict(sw=LSW, z5=LZ5, z8=LZ8, wl=L_WL, falls_w=7.0, mods=n)
    return frame_long("".join(s), "" if blind else lab, blind,
                      "Long pond option: a lap pond running across the back of the house, with a stone edge and sun ledge off the porch, the wetland and falls on the far shore, and a fire pit across the water."), m


def frame_long(inner, labels, blind, aria):
    x, y, w, h = (-16, -66, 112, 104) if not blind else (-12, -64, 106, 82)
    sc = (f'<g class="scale"><rect x="{x + 2}" y="{y + 2.5}" width="5" height=".5"/><rect class="o" x="{x + 7}" y="{y + 2.5}" width="5" height=".5"/>'
          f'<rect x="{x + 12}" y="{y + 2.5}" width="10" height=".5"/><text x="{x + 2}" y="{y + 4.8}">0</text><text x="{x + 7}" y="{y + 4.8}">5</text>'
          f'<text x="{x + 12}" y="{y + 4.8}">10</text><text x="{x + 20}" y="{y + 4.8}">20 ft</text></g>')
    return (f'<svg class="plan ls zoom opt" viewBox="{x} {y} {w} {h}" role="img" aria-label="{aria}">{Y.defs()}'
            f'<rect fill="url(#lawn)" x="{x}" y="{y}" width="{w}" height="{h}"/>{inner}{H["building"]("sk")}{labels}{"" if blind else sc}</svg>')


def revc_plan():
    """Rev. C as built in the landscape plan, same frame for comparison."""
    x, y, w, h = (-16, -82, 110, 120)
    return (f'<svg class="plan ls zoom opt" viewBox="{x} {y} {w} {h}" role="img" aria-label="Rev. C: the round pond behind the terrace with the wetland crescent on its back shore.">{Y.defs()}'
            f'<rect fill="#C8DAA2" x="{x}" y="{y}" width="{w}" height="{h}"/>{Y.yard()}{H["building"]("sk")}{L(41, -25, "Rev. C pond", "lt")}</svg>')


LONG, LM = long_plan()
LONG_MINI, _ = long_plan(True)
REVC = revc_plan()


# ---------------------------------------------------------------- numbers
def x_cross(poly, x):
    """y values where the vertical line at x crosses poly's edge, back to front."""
    ys = []
    for i in range(len(poly)):
        (x1, y1), (x2, y2) = poly[i], poly[(i + 1) % len(poly)]
        if (x1 - x) * (x2 - x) < 0:
            ys.append(y1 + (y2 - y1) * (x - x1) / (x2 - x1))
    return sorted(ys)


def view_deg(near_y, far_y, ez=VIEW[2], ey=VIEW[1]):
    return math.degrees(math.atan2(ez, ey - near_y) - math.atan2(ez, ey - far_y))


def lane(z5):
    """Longest straight swim inside the 5 ft zone (any direction), in feet."""
    best = 0
    for i in range(0, len(z5), 2):
        for j in range(i + 1, len(z5), 2):
            a, b = z5[i], z5[j]; L_ = math.dist(a, b)
            if L_ <= best: continue
            if all(Y.inside((a[0] + (b[0] - a[0]) * t / 20, a[1] + (b[1] - a[1]) * t / 20), offset(z5, .3)) for t in range(1, 20)):
                best = L_
    return best


def wall_gap(poly, z, walls):
    """Closest distance from a pond zone to the house walls."""
    return min(math.dist(p, q) for p in poly for q in walls)


SHELL_PTS = []
for a, b in zip(H['SHELL'], H['SHELL'][1:] + H['SHELL'][:1]):
    n_ = max(int(math.dist(a, b)), 1)
    SHELL_PTS += [(a[0] + (b[0] - a[0]) * t / n_, a[1] + (b[1] - a[1]) * t / n_) for t in range(n_)]
PORCH_PTS = [(x, 20) for x in range(24, 47)] + [(x, 10) for x in range(46, 69)]
BED2 = (15, 13); PBATH = (95, -2.5)


def stats(sw, z5, z8, wl, falls_xy, mods, gal_):
    cross = x_cross(sw, 36.3)
    return dict(area=area(sw), wl=area(wl), pct=area(wl) / area(sw), gal=gal_, need=(math.ceil(gal_ / CENT[1]), math.ceil(gal_ / CENT[0])), mods=mods,
                lane=lane(z5), porch=min(math.dist(p, q) for p in sw for q in PORCH_PTS + SHELL_PTS),
                deep5=min(math.dist(p, q) for p in z5 for q in SHELL_PTS), deep8=min(math.dist(p, q) for p in z8 for q in SHELL_PTS),
                view=view_deg(cross[-1], cross[0]), sofa_falls=math.dist(VIEW[:2], falls_xy),
                bed2=math.dist(BED2, falls_xy), pbath=math.dist(PBATH, falls_xy))


SC = stats(Y.SW, Y.Z5, Y.Z8, Y.WL, (41.2, -46), 16, Y.GAL)
SL = stats(LSW, LZ5, LZ8, L_WL, (41, -37), LM['mods'], lgal())
SC['terr'] = area(Y.TERRACE); SL['terr'] = area(TERR_L)



# ---------------------------------------------------------------- section at x = 40, sofa to the back slope
def long_section():
    VE = 2.0; x = 40; ey, ez = VIEW[1], VIEW[2]
    U = lambda y: ey - y
    P = lambda y, z: f"{U(y):.2f},{-z * VE:.2f}"
    yb, yf = x_cross(LSW, x)[0], x_cross(LSW, x)[-1]
    led = x_cross([(28.4, 4.3), (44, 3.0), (43.2, -.6), (29, .6)], x)
    wl_back = x_cross(L_WL, x)[0]
    lip_y = -41.2
    pond = [(yf, 0), (yf, -1), (led[0], -1), (led[0] - 1.2, -2.2), (led[0] - 2.4, -3.4), (led[0] - 3.6, -5), (yb + 7, -5), (yb + 3.4, -2.2), (yb + 1, -1.2), (yb, 0)]
    back = [(yb - .6, 1.2), (lip_y + 1.2, 3.0), (lip_y, 3.5), (wl_back, 3.6), (wl_back - 4, 2.6), (wl_back - 14, 0), (-80, 0)]
    earth = [(60, .3), (20, .3)] + pond + back + [(-80, -12), (60, -12)]
    water = pond[:-1] + [(yb, 0)]
    grav = [(lip_y - .3, 3.4), (wl_back + .3, 3.4), (wl_back + .8, 1.5), (lip_y - .3, 1.5)]
    s = [f'<polygon points="{" ".join(P(y, z) for y, z in earth)}" fill="#D2BE98"/>', f'<polygon points="{" ".join(P(y, z) for y, z in water)}" fill="url(#swg)"/>',
         f'<polygon points="{" ".join(P(y, z) for y, z in grav)}" fill="url(#sgr)"/>',
         f'<polyline points="{" ".join(P(y, z - .18) for y, z in pond + back[:4])}" fill="none" stroke="#1F2328" stroke-width=".35"/>']
    for i in range(4):
        s.append(f'<path d="M{U(lip_y) + .2:.2f},{-3.4 * VE:.2f} C{U(lip_y) - 1.4 - i * .2:.2f},{-2.8 * VE:.2f} {U(yb) - .6 - i * .2:.2f},{-1 * VE:.2f} {U(yb) - .6 - i * .25:.2f},0" fill="none" stroke="#fff" stroke-width=".3"/>')
    rg = random.Random(3); yy = lip_y - .8
    while yy > wl_back + .8:
        h = rg.uniform(1.6, 3.2)
        s.append(f'<path d="M{U(yy):.2f},{-3.4 * VE:.2f} l-.4,{-h * VE:.2f} M{U(yy):.2f},{-3.4 * VE:.2f} l.1,{-h * 1.1 * VE:.2f} M{U(yy):.2f},{-3.4 * VE:.2f} l.5,{-h * .9 * VE:.2f}" stroke="#5E8A4A" stroke-width=".22" fill="none"/>')
        yy -= rg.uniform(1.0, 1.8)
    # house, porch roof, terrace and coping
    s.append(f'<rect x="{U(46) - 6:.2f}" y="{-12 * VE:.2f}" width="{U(34) - U(46) + 6:.2f}" height="{10 * VE:.2f}" fill="#EFE6D4" stroke="#3A3F48" stroke-width=".3"/>')
    s.append(f'<line x1="{U(34):.2f}" x2="{U(34):.2f}" y1="{-10.5 * VE:.2f}" y2="{-3 * VE:.2f}" stroke="#7FB3C8" stroke-width=".9"/>')
    s.append(f'<polyline points="{P(34, 12.6)} {P(20, 10.6)}" fill="none" stroke="#3A3F48" stroke-width=".5"/><line x1="{U(20.5):.2f}" x2="{U(20.5):.2f}" y1="{-10.6 * VE:.2f}" y2="{-1.6 * VE:.2f}" stroke="#3A3F48" stroke-width=".3"/>')
    s.append(f'<rect x="{U(34):.2f}" y="{-1.6 * VE:.2f}" width="{U(20) - U(34):.2f}" height="{1.3 * VE:.2f}" fill="#CFC6B6"/>')
    s.append(f'<rect x="{U(20):.2f}" y="{-.5 * VE:.2f}" width="{U(yf) - U(20):.2f}" height="{.5 * VE:.2f}" fill="#BFB29A"/><rect x="{U(yf) - .2:.2f}" y="{-.7 * VE:.2f}" width="1.6" height="{.7 * VE:.2f}" fill="#CFC6B6" stroke="#6E665A" stroke-width=".1"/>')
    # footings and the 1:1 line the excavation stays outside of
    for fy in (34, 20.5):
        s.append(f'<rect x="{U(fy) - .8:.2f}" y="{1.0 * VE:.2f}" width="1.6" height="{1.2 * VE:.2f}" fill="#9C9384"/>')
    s.append(f'<line x1="{U(20.5) + .8:.2f}" y1="{2.2 * VE:.2f}" x2="{U(20.5) + 9.4:.2f}" y2="{(2.2 + 8.6) * VE:.2f}" stroke="#7A2E2E" stroke-width=".25" stroke-dasharray=".8 .5"/>')
    # sight line over the falls lip
    slope = (3.5 - ez) / U(lip_y); far = -80
    s.append(f'<line x1="0" y1="{-ez * VE:.2f}" x2="{U(far):.2f}" y2="{-(ez + slope * U(far)) * VE:.2f}" stroke="#B0812A" stroke-width=".3" stroke-dasharray="1.2 .7"/><circle cx="0" cy="{-ez * VE:.2f}" r=".8" fill="#B0812A"/>')
    T_ = lambda u, z, txt, a="middle", c="sn": f'<text class="{c}" x="{u:.2f}" y="{-z * VE:.2f}" style="text-anchor:{a}">{txt}</text>'
    nt = lambda y, z, dz, txt: f'<line x1="{U(y):.2f}" x2="{U(y):.2f}" y1="{-(z + .3) * VE:.2f}" y2="{-(z + dz - .6) * VE:.2f}" stroke="#3A3F48" stroke-width=".15"/>' + T_(U(y), z + dz, txt)
    s += [T_(1.4, ez + 1.6, "Sofa eye, ~6 ft above the water", "start"), T_(U(12), -1.8, "Terrace and coping"), nt(led[0] + .6, -.8, -3.4, "Sun ledge, 12″"),
          T_(U((yf + yb) / 2 - 4), -3.4, "Lap lane, 5 ft"), nt(lip_y, 3.5, 4.4, "Falls lip +3½′"), nt((lip_y + wl_back) / 2, 3.4, 7.8, "Wetland upper tier"),
          nt(wl_back - 9, 1.4, 4.2, "Back slope"), T_(U(20.5) + 10.2, -10.4, "1:1 line from the porch footing: dig stays outside it", "start"),
          T_(-5, -9.4, "Section 1 at x = 40 ft · vertical ×2", "start", "sd")]
    w = U(-70) + 4
    return (f'<svg class="plan ls sec" viewBox="-6 {-14 * VE} {w + 2:.1f} {27 * VE + 2}" role="img" aria-label="Section through the long pond from the sofa to the back slope">'
            f'<rect x="-6" y="{-14 * VE}" width="{w + 2:.1f}" height="{27 * VE + 2}" fill="#FBF8F1"/>'
            '<defs><pattern id="sgr" width="1.2" height="1.2" patternUnits="userSpaceOnUse"><rect width="1.2" height="1.2" fill="#D9CDB3"/><circle cx=".3" cy=".4" r=".16" fill="#A3967D"/><circle cx=".9" cy=".9" r=".14" fill="#EEE7D7"/></pattern>'
            '<linearGradient id="swg" x1="0" x2="0" y1="0" y2="1"><stop offset="0" stop-color="#9FCFDF"/><stop offset="1" stop-color="#3F7F9C"/></linearGradient></defs>'
            + "".join(s) + '</svg>')


SECL = long_section()

if __import__('os').environ.get('STATS_ONLY'):
    for k, v in (("revC", SC), ("long", SL)):
        print(k, {a: (round(b, 1) if isinstance(b, float) else b) for a, b in v.items()})
    sys.exit()


# ---------------------------------------------------------------- page
def row(label, a, b, fmt):
    return f'<tr><td>{label}</td><td class="num">{fmt(a)}</td><td class="num">{fmt(b)}</td></tr>'


ft = lambda v: f"{v:,.0f} ft"
sf = lambda v: f"{v:,.0f} sf"
rows = "".join([
    row("Water surface", SC['area'], SL['area'], sf),
    row("Gallons, rough", SC['gal'], SL['gal'], lambda v: f"{round(v, -3):,.0f}"),
    row("Longest straight swim, 5 ft zone", SC['lane'], SL['lane'], ft),
    row("Wetland (share of pond)", (SC['wl'], SC['pct']), (SL['wl'], SL['pct']), lambda v: f"{v[0]:,.0f} sf ({v[1]:.0%})"),
    row("Centipedes that fit / needed for 1 turnover an hour", (SC['mods'], SC['need']), (SL['mods'], SL['need']), lambda v: f"{v[0]} / {v[1][0]}–{v[1][1]}"),
    row("Water seen from the sofa", SC['view'], SL['view'], lambda v: f"{v:.1f}°"),
    row("Closest water to the porch or house", SC['porch'], SL['porch'], ft),
    row("Closest 5 ft water to a house wall", SC['deep5'], SL['deep5'], ft),
    row("Sofa to the falls", SC['sofa_falls'], SL['sofa_falls'], ft),
    row("Falls to bedroom 2's back window", SC['bed2'], SL['bed2'], ft),
    row("Falls to the primary bath window", SC['pbath'], SL['pbath'], ft),
    row("Terrace", SC['terr'], SL['terr'], sf)])

CSS3 = ('.cmod{fill:none;stroke:#8A6A2F;stroke-width:.16;stroke-dasharray:.35 .25;opacity:.85}.pipe{fill:none;stroke:#8A6A2F;stroke-width:.32;stroke-dasharray:1 .5}.pipeh{fill:#8A6A2F}'
        '.vcone{fill:#E8C66A;opacity:.16}.vaxis{stroke:#B0812A;stroke-width:.3;stroke-dasharray:1.2 .8;fill:none}.vaxis.t{stroke-dasharray:.4 .6}.veye{fill:#B0812A}'
        '.secl{stroke:#7A2E2E;stroke-width:.3;stroke-dasharray:1.6 .8}.plan.ls text.sect{font-size:1.4px;font-weight:700;fill:#7A2E2E;text-anchor:start;paint-order:stroke;stroke:#FBF8F1;stroke-width:.35px}'
        '.l-two{display:grid;grid-template-columns:1fr 1fr;gap:14px}.l-two figure{margin:0}.l-two figcaption{font:600 .95em/1.2 var(--f-head);margin:0 0 4px}'
        '@media (max-width:640px){.l-two{grid-template-columns:1fr}}')

tpl = open(T).read()
head, rest = tpl.split('<main class="doc">')
head = head.replace('<title>Ink & Brass template</title>', '<title>Long pond option</title>')
head = re.sub(r'<!-- House style: Ink & Brass.*?-->\n', '', head)
head = head.replace('</style>', H['CSS'] + CSS + CSS3 + '</style>')
ratio = SL['area'] / SC['area']
body = f"""<main class="doc">
  <header class="d-head">
    <div class="d-top"><span class="d-type">New home build</span><span class="d-date">Long pond option · Oct 26, 2026</span></div>
    <h1 class="d-title">A long pond across the back</h1>
    <p class="d-lead">Nothing requires the pond to be round. The round shape came from the first placeholder sketch, not from any Aquascape rule. This option stretches the pond along the back of the house so the terrace ends at the water. The swim is a {SL['lane']:.0f} ft lap lane instead of {SC['lane']:.0f} ft. From the sofa you see about {SL['view'] / SC['view']:.1f} times as much water. The wetland and falls move to the far shore, using the same crescent design you picked.</p>
  </header>

  <div class="d-stats">
    <div><div class="l">Longest swim</div><div class="v">{SL['lane']:.0f} ft</div><div class="s">rev. C: {SC['lane']:.0f} ft</div></div>
    <div><div class="l">Water from the sofa</div><div class="v">{SL['view']:.1f}°</div><div class="s">rev. C: {SC['view']:.1f}°</div></div>
    <div><div class="l">Pond size</div><div class="v">{SL['area']:,.0f} sf</div><div class="s">{ratio:.1f}× rev. C; about $25k–$40k more overall</div></div>
  </div>

  <div class="d-call"><b>My take</b><span>I'd take it. The pond becomes the reason you're on the terrace instead of something past it, and you get real laps. The trade is modest on cost, about $25k–$40k more overall, because the pumps and setup don't grow with the pond and the deck goes away. The bigger trade is that the pool-barrier rules come up against the back doors.</span></div>

  <h2 class="d-h2">The plan</h2>
  <figure class="d-fig wide">{LONG}</figure>
  <dl class="d-rows">
    <dt>Near shore</dt><dd>Cut stone coping runs along the water's edge, so the terrace ends at the pond. A 12-inch-deep sun ledge in front of the back porch takes chaises in the water. Three slab steps go down from it into the lap lane. The deep water stays out in the middle, at least {SL['deep5']:.0f} ft from any house wall.</dd>
    <dt>Lap lane</dt><dd>A 5 ft swim zone runs nearly the full length. The 8 ft deep zone sits at the far-left side, under the jump rock.</dd>
    <dt>Far shore</dt><dd>It's the same crescent wetland as rev. C, stretched along the back. The upper tier feeds a 7 ft falls on the living room sight line. The lower tier sheets over a stone lip into the right half of the pond and down a short rill into the lily cove at the right end. The far shore is at least {SL['pct']:.0%} wetland, and {SL['mods']} Centipedes fit, against {SL['need'][0]}–{SL['need'][1]} needed for this volume.</dd>
    <dt>Circulation</dt><dd>The intake bay is in the far-left corner, away from the beach. The pumps sit in a buried vault past the bedroom wing. Water returns at the falls and lip, so it flows across the whole pond, right to left.</dd>
    <dt>Fire pit</dt><dd>It moves across the water to the far-left shore, reached by stepping stones around the beach end. You sit with the falls on one side and look back at the house over the pond.</dd>
    <dt>Beach</dt><dd>It's at the left end, next to the bedroom wing. It's shallow, so it can sit closer to the house.</dd>
  </dl>

  <h2 class="d-h2">From the sofa</h2>
  <figure class="d-fig wide">{SECL}</figure>
  <p class="d-note">The dashed red line runs down at 45° from the porch footing. The dig stays outside it everywhere. A structural engineer should confirm that for our clay before the porch and the pond are designed together.</p>

  <h2 class="d-h2">Long pond vs. rev. C</h2>
  <div class="l-two"><figure><figcaption>Rev. C (round)</figcaption>{REVC}</figure><figure><figcaption>Long pond</figcaption>{LONG_MINI}</figure></div>
  <div class="d-tw"><table>
    <thead><tr><th></th><th class="num">Rev. C</th><th class="num">Long pond</th></tr></thead>
    <tbody>{rows}</tbody>
  </table></div>
  <p class="d-note">Measured from the drawings. "Water seen from the sofa" is how tall the pond's surface looks from a seated eye about 6 ft above the water, looking out the living room's back windows. It's measured in degrees of your view.</p>

  <h2 class="d-h2">What it takes</h2>
  <dl class="d-rows">
    <dt>Foundation</dt><dd>The house and porch footings set how close the deep water can come. The plan keeps the 5 ft zone at least {SL['deep5']:.0f} ft from the walls and outside a 45° line from the footings. With the pond this close, the engineer should design the porch slab and the pond edge together, including drainage away from the slab.</dd>
    <dt>Pool barrier</dt><dd>The water ends up about {SL['porch']:.0f} ft from the porch, so a fence between the house and the pond no longer works. The house wall becomes part of the barrier. Under the pool code the city points to, that usually means alarms or self-closing, self-latching hardware on the doors that open toward the pond. The fence then wraps the rest of the back yard and ties into the house at both ends. Youngsville's ruling is still open.</dd>
    <dt>Noise</dt><dd>The falls ends up {SL['bed2']:.0f} ft from bedroom 2's back window, versus {SC['bed2']:.0f} ft today. A valve can turn it down at night, and the lip makes a quieter sound than the falls.</dd>
    <dt>Bugs and humidity</dt><dd>The near shore is hard stone and moving water, and the planted edges sit on the far shore. That keeps mosquitoes and damp away from the doors. Fish are still the main mosquito control.</dd>
    <dt>Cost</dt><dd>The pond line goes from about $100k–$160k to $130k–$210k. That's checked against a Texas builder's <a href="https://thenaturalswimmingpond.com/natural-swim-pond-prices">$130,000 starting price for a 50' × 70' swim pond with wetland</a> and cost guides at <a href="https://www.angi.com/articles/natural-pool-cost.htm">$50–$100 per sq ft</a>. The pumps, vault and design don't grow with the size; mostly the dig, liner and stone do. Dropping the deck saves $10k–$20k, and the coping adds a little. The net is about $25k–$40k more than rev. C: about $235k–$416k for the whole landscape, against $210k–$376k.</dd>
    <dt>Sun</dt><dd>North is still unknown. A long east–west pond gets full sun on the water, which is good for swimming. Shade then has to come from trees on the far shore.</dd>
  </dl>
  <footer class="d-foot">Concept option, not a construction drawing. Generated by landscape-generator/long.py on the same axes as the house plan. Wetland sizing uses the same rules as the wetland study: at least 30% of the pond, 2,000–3,000 gph per Centipede and 1,500 gph per foot of falls.</footer>
</main>"""
open(OUT, 'w').write(head + body + '\n</body>\n</html>\n')
print("wrote", OUT)
