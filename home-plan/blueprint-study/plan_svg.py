"""Draw a crop of the to-scale plan as inline SVG, optionally with a proposed option drawn over it.
Plan feet: x left to right across the front, y from the back (pond) to the front. SVG colors come from the page tokens."""
import json, math

H = json.load(open('/tmp/claude-0/work/home-plan/house-3d/house.json'))
EXT, INT = 0.55, 0.38


def _seg(o, c, a, b):
    return (a, c, b, c) if o == 'h' else (c, a, c, b)


def _inside(px, py, regions):
    return any(x1 - 1e-6 <= px <= x2 + 1e-6 and y1 - 1e-6 <= py <= y2 + 1e-6 for x1, y1, x2, y2 in regions)


def _clip_out(o, c, a, b, regions):
    """Pieces of a wall line [a, b] that are not inside any region (sampled every 0.25 ft)."""
    n = max(1, int(round((b - a) / .25)))
    keep, run = [], None
    for i in range(n):
        u0, u1 = a + (b - a) * i / n, a + (b - a) * (i + 1) / n
        m = (u0 + u1) / 2
        px, py = (m, c) if o == 'h' else (c, m)
        out = not any(x1 + .05 < px < x2 - .05 and y1 + .05 < py < y2 - .05 for x1, y1, x2, y2 in regions)   # walls on a region's edge stay
        if out:
            run = [u0, u1] if run is None else [run[0], u1]
        elif run: keep.append(run); run = None
    if run: keep.append(run)
    return keep


def fmt(ft):
    f = int(ft + 1e-6); i = round((ft - f) * 12)
    if i == 12: f, i = f + 1, 0
    return f"{f}'" if i == 0 else f"{f}'{i}\""


def render(vb, option=None, title='', furn=True, labels=True, regions=None, show_pond=False):
    """vb = (x1, y1, x2, y2) crop in plan feet. option = dict(rooms, fixtures, openings). regions: plan boxes where the
    existing plan is erased and replaced by the option (default: the option's rooms)."""
    x1, y1, x2, y2 = vb
    W, Hh = x2 - x1, y2 - y1
    s = []
    s.append(f'<svg class="pl" viewBox="{x1} {y1} {W} {Hh}" role="img" aria-label="{title}" preserveAspectRatio="xMidYMid meet">')
    # grid
    s.append('<g class="pl-grid">')
    for gx in range(int(math.floor(x1 / 2) * 2), int(x2) + 1, 2): s.append(f'<line x1="{gx}" x2="{gx}" y1="{y1}" y2="{y2}"/>')
    for gy in range(int(math.floor(y1 / 2) * 2), int(y2) + 1, 2): s.append(f'<line y1="{gy}" y2="{gy}" x1="{x1}" x2="{x2}"/>')
    s.append('</g>')
    rooms = (option or {}).get('rooms', [])
    reg = regions if regions is not None else [(r['x1'], r['y1'], r['x2'], r['y2']) for r in rooms if room_kind(r, option) != 'ext']
    reg = reg + [tuple(b) for b in (option or {}).get('erase', [])]
    if show_pond:
        for key in ('sw', 'wl'):   # swim water and the wetland
            wl = H['pond'].get(key)
            if wl: s.append(f'<polygon class="pl-water{" pl-wet" if key == "wl" else ""}" points="' + ' '.join(f'{a},{b}' for a, b in wl) + '"/>')
    # porches
    for p in H['porches']:
        pts = ' '.join(f'{a},{b}' for a, b in p['p'])
        s.append(f'<polygon class="pl-porch" points="{pts}"/>')
    # existing room tints
    for r in H['rooms']:
        a, b, c, d = r['r']
        if _inside((a + c) / 2, (b + d) / 2, reg): continue
        s.append(f'<rect class="pl-room" x="{a}" y="{b}" width="{c - a}" height="{d - b}"/>')
    # option room tints
    for r in rooms:
        if room_kind(r, option) == 'ext': continue
        s.append(f'<rect class="pl-room" x="{r["x1"]}" y="{r["y1"]}" width="{r["x2"] - r["x1"]}" height="{r["y2"] - r["y1"]}"/>')
        s.append(f'<rect class="pl-new" x="{r["x1"]}" y="{r["y1"]}" width="{r["x2"] - r["x1"]}" height="{r["y2"] - r["y1"]}"/>')
    # existing furniture outside the option area
    if furn:
        for f in H['furn']:
            if f.get('t') != 'box' or f.get('k') in ('rug',) or f['z1'] < .3: continue
            (cx, cy), (sw, sd), ang = f['c'], f['s'], f.get('a', 0)
            if _inside(cx, cy, reg): continue
            s.append(f'<rect class="pl-furn" x="{cx - sw / 2}" y="{cy - sd / 2}" width="{sw}" height="{sd}" transform="rotate({-math.degrees(ang)} {cx} {cy})"/>')
    # existing walls, minus the option area, with openings
    for w in H['walls']:
        o, c, a, b, ext = w['o'], w['c'], w['a'], w['b'], w['ext']
        t = EXT if ext else INT
        ops = sorted(w['ops'], key=lambda q: q[1])
        pieces, cur = [], a
        for k, s0, e0 in ops:
            if s0 > cur: pieces.append((cur, s0))
            cur = max(cur, e0)
        if b > cur: pieces.append((cur, b))
        for pa, pb in pieces:
            for qa, qb in _clip_out(o, c, pa, pb, reg):
                X1, Y1, X2, Y2 = _seg(o, c, qa, qb)
                s.append(f'<line class="pl-wall" x1="{X1}" y1="{Y1}" x2="{X2}" y2="{Y2}" stroke-width="{t}"/>')
        for k, s0, e0 in ops:
            if not _clip_out(o, c, s0, e0, reg): continue
            mm = (s0 + e0) / 2; qx, qy = (mm, c) if o == 'h' else (c, mm)
            if any(a_ - .1 <= qx <= c_ + .1 and b_ - .1 <= qy <= d_ + .1 for a_, b_, c_, d_ in (option or {}).get('close', [])):
                X1, Y1, X2, Y2 = _seg(o, c, s0, e0)
                s.append(f'<line class="pl-wall" x1="{X1}" y1="{Y1}" x2="{X2}" y2="{Y2}" stroke-width="{t}"/>'); continue
            X1, Y1, X2, Y2 = _seg(o, c, s0, e0)
            if k in ('win', 'glass', 'slider'):
                s.append(f'<line class="pl-win" x1="{X1}" y1="{Y1}" x2="{X2}" y2="{Y2}" stroke-width="{t * .45}"/>')
            elif k in ('door',):
                s.append(_door(o, c, s0, e0))
            elif k == 'gdoor':
                s.append(f'<line class="pl-gd" x1="{X1}" y1="{Y1}" x2="{X2}" y2="{Y2}"/>')
    # option: room walls (walled rooms only), extra walls, then openings cut into them
    if option:
        for r in rooms:
            k = room_kind(r, option)
            cls = {'room': 'pl-nwall', 'open': 'pl-zone', 'ext': 'pl-ext'}[k]
            s.append(f'<rect class="{cls}" x="{r["x1"]}" y="{r["y1"]}" width="{r["x2"] - r["x1"]}" height="{r["y2"] - r["y1"]}"/>')
        for a, b, c, d in option.get('walls', []):
            s.append(f'<line class="pl-wall" x1="{a}" y1="{b}" x2="{c}" y2="{d}" stroke-width="{EXT}"/>')
        for w in H['walls']:   # existing openings on the edge of the option area show through its walls
            t = EXT if w['ext'] else INT
            for k, s0, e0 in w['ops']:
                if not _clip_out(w['o'], w['c'], s0, e0, reg): continue
                m = (s0 + e0) / 2; px, py = (m, w['c']) if w['o'] == 'h' else (w['c'], m)
                if not any(x1_ - .1 <= px <= x2_ + .1 and y1_ - .1 <= py <= y2_ + .1 for x1_, y1_, x2_, y2_ in reg): continue
                if any(a_ - .1 <= px <= c_ + .1 and b_ - .1 <= py <= d_ + .1 for a_, b_, c_, d_ in option.get('close', [])): continue   # opening walled in
                X1, Y1, X2, Y2 = _seg(w['o'], w['c'], s0, e0)
                s.append(f'<line class="pl-gap" x1="{X1}" y1="{Y1}" x2="{X2}" y2="{Y2}"/>')
                if k in ('win', 'glass', 'slider'): s.append(f'<line class="pl-win" x1="{X1}" y1="{Y1}" x2="{X2}" y2="{Y2}" stroke-width="{t * .45}"/>')
                elif k == 'door': s.append(_door(w['o'], w['c'], s0, e0))
        CEIL = ('truss', 'beam', 'Beam', 'portal', 'Ridge', 'ridge')
        for f in option.get('fixtures', []):
            a, b, c, d = f['x1'], f['y1'], f['x2'], f['y2']
            a, c = min(a, c), max(a, c); b, d = min(b, d), max(b, d)
            if any(k in f['label'] for k in CEIL):   # ceiling structure: dashed overhead lines, drawn under the furniture
                f['nolabel'] = True
                s.append(f'<rect class="pl-ceil" x="{a}" y="{b}" width="{c - a}" height="{d - b}"/>'); continue
            s.append(f'<rect class="pl-fix" x="{a}" y="{b}" width="{c - a}" height="{d - b}" rx=".15"/>')
        for op in option.get('openings', []):
            a, b, c, d, k = op['x1'], op['y1'], op['x2'], op['y2'], op['kind']
            horiz = abs(b - d) < abs(a - c)
            o, cc, s0, e0 = ('h', (b + d) / 2, min(a, c), max(a, c)) if horiz else ('v', (a + c) / 2, min(b, d), max(b, d))
            X1, Y1, X2, Y2 = _seg(o, cc, s0, e0)
            s.append(f'<line class="pl-gap" x1="{X1}" y1="{Y1}" x2="{X2}" y2="{Y2}"/>')
            if k in ('window', 'glass'): s.append(f'<line class="pl-win" x1="{X1}" y1="{Y1}" x2="{X2}" y2="{Y2}" stroke-width=".25"/>')
            elif k == 'door': s.append(_door(o, cc, s0, e0))
            elif k == 'pocket': s.append(f'<line class="pl-pocket" x1="{X1}" y1="{Y1}" x2="{X2}" y2="{Y2}"/>')
        if labels:
            for f in option.get('fixtures', []):
                a, b, c, d = f['x1'], f['y1'], f['x2'], f['y2']
                w_, h_ = abs(c - a), abs(d - b)
                if max(w_, h_) < 1.2 or not f.get('label') or f.get('nolabel'): continue
                lab = f.get('short') or f['label']
                vert = h_ > w_ * 1.6 and w_ < 2.5
                long_, short_ = (h_, w_) if vert else (w_, h_)
                fs = min(.62, short_ * .55, .92 * long_ / (len(lab) * .5 + .4))
                if fs < .26: continue
                rot = ' transform="rotate(-90 {0} {1})"'.format((a + c) / 2, (b + d) / 2) if vert else ''
                s.append(f'<text class="pl-fl" x="{(a + c) / 2}" y="{(b + d) / 2 + fs * .35}" style="font-size:{fs:.2f}px"{rot}>{_esc(lab)}</text>')
            for r in rooms:
                if not r.get('name') or r.get('nolabel'): continue
                w_, h_ = r['x2'] - r['x1'], r['y2'] - r['y1']
                if min(w_, h_) < 3: continue
                fs = max(.55, min(.95, min(w_, h_) * .11))
                cx, cy = (r['x1'] + r['x2']) / 2, (r['y1'] + r['y2']) / 2
                ly = r.get('ly', cy)
                nm = r['name'].split(' (')[0]
                s.append(f'<text class="pl-rl" x="{cx}" y="{ly - .15}" style="font-size:{fs}px">{_esc(nm)}</text>')
                s.append(f'<text class="pl-rd" x="{cx}" y="{ly + fs * .95}" style="font-size:{fs * .78}px">{fmt(w_)} × {fmt(h_)}</text>')
    # existing room labels outside the option area
    if labels:
        for r in H['rooms']:
            if not r['n']: continue
            a, b, c, d = r['r']
            if _inside((a + c) / 2, (b + d) / 2, reg): continue
            lx, ly = r['lab']
            if not (x1 < lx < x2 and y1 < ly < y2): continue
            s.append(f'<text class="pl-xl" x="{lx}" y="{ly}">{_esc(r["n"])}</text>')
    rt = (option or {}).get('route')
    if rt and len(rt) > 1:
        s.append('<polyline class="pl-route" points="' + ' '.join(f'{a},{b}' for a, b in rt) + '"/>')
        (ax, ay), (bx, by) = rt[-2], rt[-1]
        L = math.hypot(bx - ax, by - ay) or 1; ux, uy = (bx - ax) / L, (by - ay) / L
        s.append(f'<polygon class="pl-arrow" points="{bx},{by} {bx - ux * 1.2 - uy * .6},{by - uy * 1.2 + ux * .6} {bx - ux * 1.2 + uy * .6},{by - uy * 1.2 - ux * .6}"/>')
        s.append(f'<circle class="pl-arrow" cx="{rt[0][0]}" cy="{rt[0][1]}" r=".5"/>')
    s.append('</svg>')
    return ''.join(s)


EXT_WORDS = ('porch', 'pond', 'outdoor', 'link', 'stoop')
def room_kind(r, option):
    if r.get('kind'): return r['kind']
    n = r['name'].lower()
    if any(w in n for w in EXT_WORDS): return 'ext'
    if r['name'] in (option or {}).get('open', []): return 'open'
    return 'room'


def _door(o, c, s0, e0):
    w = e0 - s0
    if o == 'h':
        return f'<path class="pl-door" d="M{s0},{c} L{s0},{c - w} A{w},{w} 0 0,1 {e0},{c}"/>'
    return f'<path class="pl-door" d="M{c},{s0} L{c + w},{s0} A{w},{w} 0 0,1 {c},{e0}"/>'


def _esc(t):
    return str(t).replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')


CSS = """
/* additions: plan crops */
.pl{width:100%;height:auto;display:block;background:var(--surface);border:1px solid var(--rule);border-radius:4px}
.pl-grid line{stroke:var(--rule);stroke-width:.05}
.pl-porch{fill:var(--rule);opacity:.35;stroke:var(--rule-strong);stroke-width:.08;stroke-dasharray:.4 .3}
.pl-room{fill:var(--bg)}
.pl-new{fill:var(--accent);opacity:.09}
.pl-furn{fill:none;stroke:var(--muted);stroke-width:.07;opacity:.55}
.pl-wall{stroke:var(--ink);stroke-linecap:square}
.pl-nwall{fill:none;stroke:var(--ink);stroke-width:.4}
.pl-win{stroke:var(--muted);opacity:.9}
.pl-gd{stroke:var(--muted);stroke-width:.12;stroke-dasharray:.5 .3}
.pl-gap{stroke:var(--surface);stroke-width:.62;stroke-linecap:butt}
.pl-door{fill:none;stroke:var(--muted);stroke-width:.07}
.pl-pocket{stroke:var(--muted);stroke-width:.1;stroke-dasharray:.25 .2}
.pl-zone{fill:none;stroke:var(--accent);stroke-width:.12;stroke-dasharray:.5 .35}
.pl-ext{fill:var(--rule);opacity:.6;stroke:var(--muted);stroke-width:.1;stroke-dasharray:.5 .35}
.pl-water{fill:var(--muted);opacity:.18;stroke:var(--muted);stroke-width:.12}
.pl-wet{opacity:.1}
.pl-route{fill:none;stroke:var(--accent);stroke-width:.32;stroke-dasharray:.9 .5;stroke-linecap:round;stroke-linejoin:round}
.pl-arrow{fill:var(--accent)}
.pl-ceil{fill:none;stroke:var(--accent);stroke-width:.14;stroke-dasharray:.6 .4;opacity:.8}
.pl-fix{fill:var(--surface);stroke:var(--body);stroke-width:.08}
.pl-fl{fill:var(--muted);text-anchor:middle;font-family:"Source Sans 3",system-ui,sans-serif}
.pl-rl{fill:var(--ink);text-anchor:middle;font-weight:600;font-family:"Source Sans 3",system-ui,sans-serif}
.pl-rd{fill:var(--muted);text-anchor:middle;font-family:"Source Sans 3",system-ui,sans-serif;font-variant-numeric:tabular-nums}
.pl-xl{fill:var(--muted);text-anchor:middle;font-size:.8px;font-family:"Source Sans 3",system-ui,sans-serif}
"""
