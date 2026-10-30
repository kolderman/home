"""Roof model for the house: planar roofs, the combined roof surface, and checks.
Plan coordinates in feet: x left to right across the front, y from the back (pond) to the front (street).
Heights are above the main floor. Each roof is a rectangle with a ridge (gable or hip ends) or a shed;
the finished roof is the highest of all of them at each point, the way framed roofs that meet each other work."""
import math
from shapely.geometry import Polygon, box, Point, LineString
from shapely.ops import unary_union

LIFT = 0.35   # top of the roof deck above the wall plate at the outside face of the wall
TH = 0.55     # roof thickness (deck, shingles, and the rafter tail seen at the eave)


class Roof:
    """kind 'ridge': x1,y1,x2,y2 is the wall rectangle, ax the ridge direction ('x' or 'y'),
    ends (start, end) along the ridge are 'gable', 'hip' or 'open' (open runs on into a bigger roof and is hidden there).
    ov = overhang at (low u side, high u side) eaves, rake = overhang at the (start, end) of the ridge, hov = overhang at hip ends (default ov[0]).
    kind 'shed': hi in 'x1','x2','y1','y2' is the high side; H is the deck height at the high wall line."""

    def __init__(self, name, x1, y1, x2, y2, plate=None, pitch=10 / 12, ax='x', ends=('gable', 'gable'), ov=(1.5, 1.5),
                 rake=(1.0, 1.0), kind='ridge', hi=None, H=None, mat='roof', note='', clip=None, hov=None):
        self.name, self.kind, self.mat, self.note = name, kind, mat, note
        self.r = (x1, y1, x2, y2)
        self.plate, self.k, self.ax, self.ends, self.ov, self.rake, self.hi, self.H = plate, pitch, ax, ends, ov, rake, hi, H
        x1, y1, x2, y2 = self.r
        if kind == 'ridge':
            along = ax == 'x'
            u1, u2 = (y1, y2) if along else (x1, x2)
            a1, a2 = (x1, x2) if along else (y1, y2)
            U1, U2 = u1 - ov[0], u2 + ov[1]
            ext = [rake[i] if ends[i] == 'gable' else ((ov[0] if hov is None else hov) if ends[i] == 'hip' else 0) for i in (0, 1)]   # hov: overhang at hip ends, when it differs from the side eaves
            A1, A2 = a1 - ext[0], a2 + ext[1]
            self.u, self.a, self.U, self.A, self.along = (u1, u2), (a1, a2), (U1, U2), (A1, A2), along
            P = plate + LIFT
            # each plane as (gx, gy, c): z = gx*x + gy*y + c ; and the edge it drains to
            pl = []
            def plane(du, da, c0):  # z = c0 + du*u + da*a
                return (da, du, c0) if along else (du, da, c0)
            pl.append(('eave0', plane(pitch, 0, P - pitch * u1)))      # rises from the u1 eave
            pl.append(('eave1', plane(-pitch, 0, P + pitch * u2)))     # rises from the u2 eave
            if ends[0] == 'hip': pl.append(('hip0', plane(0, pitch, P - pitch * a1)))
            if ends[1] == 'hip': pl.append(('hip1', plane(0, -pitch, P + pitch * a2)))
            self.planes = pl
            self.rect = box(A1, U1, A2, U2) if along else box(U1, A1, U2, A2)
            self.ridge = P + pitch * (u2 - u1) / 2
        else:
            p = pitch
            if hi in ('y1', 'y2'):
                yH = y1 if hi == 'y1' else y2
                s = 1 if hi == 'y2' else -1          # z rises toward the high side
                c = (0, s * p, H - s * p * yH)
                rect = box(x1 - rake[0], y1 - (ov[0] if hi == 'y2' else 0), x2 + rake[1], y2 + (ov[0] if hi == 'y1' else 0))
            else:
                xH = x1 if hi == 'x1' else x2
                s = 1 if hi == 'x2' else -1
                c = (s * p, 0, H - s * p * xH)
                rect = box(x1 - (ov[0] if hi == 'x2' else 0), y1 - rake[0], x2 + (ov[0] if hi == 'x1' else 0), y2 + rake[1])
            self.planes = [('shed', c)]
            self.rect = rect
            self.ridge = H
        if clip is not None:   # a box (x1, y1, x2, y2) or a list of boxes the roof is cut to
            boxes = [clip] if isinstance(clip[0], (int, float)) else clip
            self.rect = self.rect.intersection(unary_union([box(*b) for b in boxes]))

    def z(self, x, y):
        b = self.rect.bounds
        if not (b[0] - 1e-9 <= x <= b[2] + 1e-9 and b[1] - 1e-9 <= y <= b[3] + 1e-9):
            return None
        if abs(self.rect.area - (b[2] - b[0]) * (b[3] - b[1])) > 1e-6:
            if not hasattr(self, '_prep'):
                from shapely.prepared import prep
                self._prep = prep(self.rect.buffer(1e-7))
            if not self._prep.covers(Point(x, y)): return None
        return min(gx * x + gy * y + c for _, (gx, gy, c) in self.planes)

    def facets(self):
        """[(key, plane, polygon)]: each plane is the roof where it is the lowest of this roof's planes."""
        out = []
        x0, y0, x1, y1 = self.rect.bounds
        for i, (k, pi) in enumerate(self.planes):
            poly = self.rect
            for j, (_, pj) in enumerate(self.planes):
                if i == j: continue
                hp = halfplane(pi, pj, (x0 - 5, y0 - 5, x1 + 5, y1 + 5))   # where pi <= pj
                poly = poly.intersection(hp)
                if poly.is_empty: break
            if not poly.is_empty and poly.area > 1e-6:
                out.append((k, pi, poly))
        return out


def halfplane(pa, pb, bb):
    """Polygon of points in the bounding box where plane pa <= plane pb (both z = gx x + gy y + c)."""
    gx, gy, c = pa[0] - pb[0], pa[1] - pb[1], pa[2] - pb[2]   # f = gx x + gy y + c <= 0
    x0, y0, x1, y1 = bb
    big = box(x0, y0, x1, y1)
    if abs(gx) < 1e-12 and abs(gy) < 1e-12:
        return big if c <= 1e-9 else Polygon()
    # clip the box polygon by the line
    pts = list(big.exterior.coords)[:-1]
    f = lambda p: gx * p[0] + gy * p[1] + c
    out = []
    for i in range(len(pts)):
        P, Q = pts[i], pts[(i + 1) % len(pts)]
        fp, fq = f(P), f(Q)
        if fp <= 0: out.append(P)
        if (fp < 0 < fq) or (fq < 0 < fp):
            t = fp / (fp - fq)
            out.append((P[0] + t * (Q[0] - P[0]), P[1] + t * (Q[1] - P[1])))
    return Polygon(out) if len(out) >= 3 else Polygon()


def height(roofs, x, y, skip=None):
    best = None
    for r in roofs:
        if r is skip: continue
        z = r.z(x, y)
        if z is not None and (best is None or z > best): best = z
    return best


def visible(roofs):
    """For each roof facet, the part that is on top: [(roof, key, plane, polygon)]."""
    out = []
    allf = [(ri, r, k, p, poly) for ri, r in enumerate(roofs) for k, p, poly in r.facets()]
    for ri, r, k, p, poly in allf:
        vis = poly
        cut = []
        for ri2, r2, k2, p2, poly2 in allf:
            if r2 is r: continue
            if not poly2.intersects(vis): continue
            same = all(abs(p[i] - p2[i]) < 1e-6 for i in range(3))
            if same and ri2 > ri: continue          # coplanar roofs: the first one keeps the shared area
            # where the other facet is higher than this one (or level with it, for coplanar roofs)
            hp = halfplane((p[0], p[1], p[2] + (0 if same else 1e-4)), p2, poly2.buffer(1).bounds)
            reg = poly2.intersection(hp)
            if not reg.is_empty: cut.append(reg)
        if cut:
            vis = vis.difference(unary_union(cut).buffer(1e-6))
        if vis.is_empty or vis.area < 0.05: continue
        polys = [vis] if vis.geom_type == 'Polygon' else [g for g in getattr(vis, 'geoms', []) if g.geom_type == 'Polygon']
        for g in polys:
            if g.area > 0.05: out.append((r, k, p, g.simplify(0.01)))
    return out


def zp(p, x, y): return p[0] * x + p[1] * y + p[2]


def drainage(roofs, res=0.25, footprint=None):
    """Steepest-descent water on a grid over the combined roof. Returns the cells where water stops
    (no lower neighbor and not at a roof edge), grouped into clusters."""
    import numpy as np
    xs = [r.rect.bounds for r in roofs]
    X0, Y0 = min(b[0] for b in xs) - 1, min(b[1] for b in xs) - 1
    X1, Y1 = max(b[2] for b in xs) + 1, max(b[3] for b in xs) + 1
    nx, ny = int((X1 - X0) / res) + 1, int((Y1 - Y0) / res) + 1
    Z = np.full((ny, nx), np.nan)
    for j in range(ny):
        y = Y0 + j * res
        for i in range(nx):
            x = X0 + i * res
            h = height(roofs, x + 1e-4, y + 1e-4)
            if h is not None: Z[j, i] = h
    sinks = []
    for j in range(1, ny - 1):
        for i in range(1, nx - 1):
            z = Z[j, i]
            if np.isnan(z): continue
            nb = Z[j - 1:j + 2, i - 1:i + 2]
            if np.isnan(nb).any(): continue   # at a roof edge: water leaves the roof here
            if (nb < z - 1e-6).any(): continue
            sinks.append((X0 + i * res, Y0 + j * res, z))
    # cluster
    cl = []
    for s in sinks:
        for c in cl:
            if any(abs(s[0] - t[0]) <= res * 1.5 and abs(s[1] - t[1]) <= res * 1.5 for t in c[-40:]):
                c.append(s); break
        else: cl.append([s])
    return Z, (X0, Y0, res), cl


def _ring_segments(poly):
    rings = [list(poly.exterior.coords)] + [list(r.coords) for r in poly.interiors]
    for rc in rings:
        for a, b in zip(rc, rc[1:]):
            yield a, b


def edges(roofs, vis, step=0.25):
    """Classify every edge of the visible roof: eave, rake, ridge, hip, valley, seam (coplanar join).
    Returns [dict(t, a=(x,y,z), b=(x,y,z), n=(nx,ny) outward from the facet, i=facet index)]."""
    out = []
    for i, (r, k, p, poly) in enumerate(vis):
        for A, B in _ring_segments(poly):
            L = math.hypot(B[0] - A[0], B[1] - A[1])
            if L < 0.05: continue
            tx, ty = (B[0] - A[0]) / L, (B[1] - A[1]) / L
            nx, ny = ty, -tx
            mx, my = (A[0] + B[0]) / 2, (A[1] + B[1]) / 2
            if poly.contains(Point(mx + nx * 0.03, my + ny * 0.03)): nx, ny = -nx, -ny
            n = max(1, int(L / step))
            runs = []
            for s in range(n):
                t0, t1 = s / n, (s + 1) / n
                tm = (t0 + t1) / 2
                x, y = A[0] + (B[0] - A[0]) * tm, A[1] + (B[1] - A[1]) * tm
                q = Point(x + nx * 0.04, y + ny * 0.04)
                j = next((jj for jj, v in enumerate(vis) if jj != i and v[3].contains(q)), None)
                zi = zp(p, x, y)
                if j is None:
                    typ = None
                else:
                    pj = vis[j][2]; zj = zp(pj, x, y)
                    if abs(zj - zi) < 0.06:
                        if j < i: typ = 'dup'
                        elif all(abs(p[c] - pj[c]) < 1e-6 for c in range(3)): typ = 'seam'
                        else:
                            qi = zp(p, q.x, q.y); qj = zp(pj, q.x, q.y)
                            convex = qi > qj + 1e-6 or vis[j][0] is r
                            d1 = math.atan2(-p[1], -p[0]); d2 = math.atan2(-pj[1], -pj[0])
                            same_dir = abs(math.remainder(d1 - d2, 2 * math.pi)) < math.radians(35) and abs(p[0]) + abs(p[1]) > 1e-9 and abs(pj[0]) + abs(pj[1]) > 1e-9
                            if same_dir: typ = 'break'
                            elif convex:
                                typ = 'ridge' if abs(zp(p, A[0], A[1]) - zp(p, B[0], B[1])) < 0.02 and abs(zp(pj, A[0], A[1]) - zp(pj, B[0], B[1])) < 0.02 else 'hip'
                            else: typ = 'valley'
                            if same_dir: typ = 'break'
                    elif zj > zi: typ = 'under'      # this facet runs under a higher roof's edge: no trim here
                    else: typ = None                 # this facet's edge stands above a lower roof
                if typ is None:
                    level = abs(zp(p, A[0], A[1]) - zp(p, B[0], B[1])) < 0.02
                    down = p[0] * nx + p[1] * ny < -1e-6
                    typ = 'eave' if level and down else ('top' if level else 'rake')
                if runs and runs[-1][0] == typ and abs(runs[-1][2] - t0) < 1e-9: runs[-1][2] = t1
                else: runs.append([typ, t0, t1])
            for typ, t0, t1 in runs:
                if typ in ('dup', 'under'): continue
                a = (A[0] + (B[0] - A[0]) * t0, A[1] + (B[1] - A[1]) * t0)
                b = (A[0] + (B[0] - A[0]) * t1, A[1] + (B[1] - A[1]) * t1)
                out.append(dict(t=typ, a=(a[0], a[1], zp(p, *a)), b=(b[0], b[1], zp(p, *b)), n=(nx, ny), i=i))
    return out


def gables(roofs, wall_top, step=0.25):
    """Vertical infill under each gable end, from the wall or lower roof up to the underside of the roof.
    wall_top(x, y) gives the top of the outside wall at a point on the wall line, or None if there is no wall there.
    Gable ends of ridge roofs and the rake ends of sheds. Returns [dict(roof, ax, a, d=outward sign, pts=[(u, bottom, top), ...])] in runs."""
    out = []
    for r in roofs:
        if r.kind == 'ridge':
            ends = [(r.a[e], r.u, r.along, 2 * e - 1) for e in (0, 1) if r.ends[e] == 'gable']
        else:   # a shed's two rake ends, at the wall lines across its slope
            X1, Y1, X2, Y2 = r.r
            ends = [(a, (Y1, Y2), True, d) for a, d in ((X1, -1), (X2, 1))] if r.hi in ('y1', 'y2') else [(a, (X1, X2), False, d) for a, d in ((Y1, -1), (Y2, 1))]
        for a, (u1, u2), along, d in ends:
            ax = 'x' if along else 'y'
            n = max(1, int((u2 - u1) / step))
            run = []
            def flush():
                if len(run) > 1: out.append(dict(roof=r.name, ax=ax, a=a, d=d, pts=list(run)))
                run.clear()
            for s in range(n + 1):
                u = u1 + (u2 - u1) * s / n
                x, y = (a, u) if along else (u, a)
                top = r.z(x, y)
                if top is None: flush(); continue
                top -= TH * 0.9
                oth = [o.z(x, y) for o in roofs if o is not r]
                oth = [z for z in oth if z is not None]
                if any(z > top + TH for z in oth): flush(); continue        # buried inside a taller roof
                w = wall_top(x, y)
                cand = ([w] if w is not None else []) + oth
                bot = max(cand) if cand else None
                if bot is None or bot >= top - 0.02: flush(); continue
                run.append((u, bot, top))
            flush()
    return out
