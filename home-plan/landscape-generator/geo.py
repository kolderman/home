"""Geometry and drawing helpers for the landscape plan. Units are feet, same axes as plan.py."""
import math, random

def catmull(pts, closed=True, n=8):
    out = []
    m = len(pts)
    rng = range(m) if closed else range(m - 1)
    for i in rng:
        p0 = pts[(i - 1) % m] if closed or i > 0 else pts[0]
        p1 = pts[i]; p2 = pts[(i + 1) % m]
        p3 = pts[(i + 2) % m] if closed or i + 2 < m else pts[-1]
        for k in range(n):
            t = k / n; t2 = t * t; t3 = t2 * t
            x = 0.5 * ((2 * p1[0]) + (-p0[0] + p2[0]) * t + (2 * p0[0] - 5 * p1[0] + 4 * p2[0] - p3[0]) * t2 + (-p0[0] + 3 * p1[0] - 3 * p2[0] + p3[0]) * t3)
            y = 0.5 * ((2 * p1[1]) + (-p0[1] + p2[1]) * t + (2 * p0[1] - 5 * p1[1] + 4 * p2[1] - p3[1]) * t2 + (-p0[1] + 3 * p1[1] - 3 * p2[1] + p3[1]) * t3)
            out.append((x, y))
    if not closed:
        out.append(pts[-1])
    return out

def d(pts, closed=True):
    s = "M" + " L".join(f"{x:.2f},{y:.2f}" for x, y in pts)
    return s + (" Z" if closed else "")

def area(p):
    return abs(sum(p[i][0] * p[(i + 1) % len(p)][1] - p[(i + 1) % len(p)][0] * p[i][1] for i in range(len(p)))) / 2

def signed(p):
    return sum(p[i][0] * p[(i + 1) % len(p)][1] - p[(i + 1) % len(p)][0] * p[i][1] for i in range(len(p))) / 2

def offset(p, dist):
    """Positive dist pushes outward."""
    m = len(p); sg = 1 if signed(p) > 0 else -1
    out = []
    for i in range(m):
        a = p[(i - 1) % m]; b = p[(i + 1) % m]
        tx, ty = b[0] - a[0], b[1] - a[1]; L = math.hypot(tx, ty) or 1
        nx, ny = ty / L * sg, -tx / L * sg
        out.append((p[i][0] + nx * dist, p[i][1] + ny * dist))
    return out

def normal_at(p, i):
    m = len(p); sg = 1 if signed(p) > 0 else -1
    a = p[(i - 1) % m]; b = p[(i + 1) % m]
    tx, ty = b[0] - a[0], b[1] - a[1]; L = math.hypot(tx, ty) or 1
    return ty / L * sg, -tx / L * sg

def blob(cx, cy, rx, ry, seed=1, k=9, jit=0.16, rot=0):
    r = random.Random(seed)
    pts = []
    for i in range(k):
        a = 2 * math.pi * i / k
        f = 1 + r.uniform(-jit, jit)
        x, y = rx * f * math.cos(a), ry * f * math.sin(a)
        c, s = math.cos(math.radians(rot)), math.sin(math.radians(rot))
        pts.append((cx + x * c - y * s, cy + x * s + y * c))
    return catmull(pts, True, 8)

def ribbon(center, w0, w1=None):
    """Closed polygon around an open centerline, width tapering from w0 to w1."""
    w1 = w0 if w1 is None else w1
    c = catmull(center, False, 8); n = len(c)
    left, right = [], []
    for i in range(n):
        a = c[max(i - 1, 0)]; b = c[min(i + 1, n - 1)]
        tx, ty = b[0] - a[0], b[1] - a[1]; L = math.hypot(tx, ty) or 1
        nx, ny = -ty / L, tx / L
        w = (w0 + (w1 - w0) * i / (n - 1)) / 2
        left.append((c[i][0] + nx * w, c[i][1] + ny * w)); right.append((c[i][0] - nx * w, c[i][1] - ny * w))
    return left + right[::-1], c

def walk(c, step):
    """Points every `step` ft along an open polyline."""
    out = [c[0]]; acc = 0
    for a, b in zip(c, c[1:]):
        L = math.hypot(b[0] - a[0], b[1] - a[1])
        while acc + L >= step:
            t = (step - acc) / L
            a = (a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t)
            L = math.hypot(b[0] - a[0], b[1] - a[1]); acc = 0
            out.append(a)
        acc += L
    return out

def rock(cx, cy, r, rng, flat=False, cls="st"):
    k = rng.randint(6, 8); el = rng.uniform(0.75, 1.0) if not flat else 0.6; rot = rng.uniform(0, 180)
    pts = []
    for i in range(k):
        a = 2 * math.pi * i / k + rng.uniform(-0.25, 0.25)
        rr = r * rng.uniform(0.78, 1.08)
        x, y = rr * math.cos(a), rr * el * math.sin(a)
        c, s = math.cos(math.radians(rot)), math.sin(math.radians(rot))
        pts.append((cx + x * c - y * s, cy + x * s + y * c))
    sh = [(x + r * 0.18, y + r * 0.22) for x, y in pts]
    hi = [(cx + (x - cx) * 0.55 - r * 0.15, cy + (y - cy) * 0.55 - r * 0.15) for x, y in pts]
    tone = rng.choice(["st", "st2", "st3"]) if cls == "st" else cls
    return (f'<polygon class="shd" points="{" ".join(f"{x:.2f},{y:.2f}" for x, y in sh)}"/>'
            f'<polygon class="{tone}" points="{" ".join(f"{x:.2f},{y:.2f}" for x, y in pts)}"/>'
            f'<polygon class="sth" points="{" ".join(f"{x:.2f},{y:.2f}" for x, y in hi)}"/>')

def tree(cx, cy, r, kind="dec", seed=0):
    rng = random.Random(seed)
    k = 11 if kind != "ever" else 14
    pts = []
    for i in range(k * 2):
        a = 2 * math.pi * i / (k * 2)
        rr = r * (1 if i % 2 == 0 else (0.86 if kind != "ever" else 0.72)) * rng.uniform(0.95, 1.04)
        pts.append((cx + rr * math.cos(a), cy + rr * math.sin(a)))
    sm = catmull(pts, True, 3) if kind != "ever" else pts
    sh = [(x + r * 0.22, y + r * 0.26) for x, y in sm]
    out = f'<path class="tshd" d="{d(sh)}"/><path class="t-{kind}" d="{d(sm)}"/>'
    out += f'<circle class="t-{kind}-hi" cx="{cx - r * .25:.2f}" cy="{cy - r * .25:.2f}" r="{r * .45:.2f}"/>'
    if kind != "ever":
        for i in range(5):
            a = i * 2 * math.pi / 5 + 0.3
            out += f'<line class="tbr" x1="{cx:.2f}" y1="{cy:.2f}" x2="{cx + r * .55 * math.cos(a):.2f}" y2="{cy + r * .55 * math.sin(a):.2f}"/>'
    out += f'<circle class="ttr" cx="{cx}" cy="{cy}" r="{max(r * .07, .25):.2f}"/>'
    return out

def tuft(cx, cy, s, cls="tf"):
    out = []
    for i in range(7):
        a = math.radians(-90 + (i - 3) * 22)
        out.append(f'M{cx:.2f},{cy:.2f} L{cx + s * math.cos(a):.2f},{cy + s * math.sin(a) * 1.0:.2f}')
    return f'<path class="{cls}" d="{" ".join(out)}"/>'

def lily(cx, cy, r, rot):
    a0 = math.radians(rot); a1 = a0 + math.radians(35)
    x0, y0 = cx + r * math.cos(a0), cy + r * math.sin(a0)
    x1, y1 = cx + r * math.cos(a1), cy + r * math.sin(a1)
    return f'<path class="lp" d="M{cx:.2f},{cy:.2f} L{x0:.2f},{y0:.2f} A{r},{r} 0 1 0 {x1:.2f},{y1:.2f} Z"/>'

def shrub(cx, cy, r, cls="sh", seed=0):
    rng = random.Random(seed)
    pts = []
    for i in range(16):
        a = 2 * math.pi * i / 16
        rr = r * (1 if i % 2 == 0 else .88) * rng.uniform(.95, 1.05)
        pts.append((cx + rr * math.cos(a), cy + rr * math.sin(a)))
    return f'<path class="{cls}" d="{d(catmull(pts, True, 2))}"/>'
