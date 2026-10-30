import sys, json, html
sys.path.insert(0, '/tmp/claude-0/work/draftM')
BASE = '/tmp/claude-0/work/draftM/plan-generator-M2-foyer.py'
import re
def load(dx=0):
    src = open(BASE).read(); src = src[:src.rindex('\npage()')]
    if dx:
        a = src.index('    R(75, 20, 6.8, 7, 0.3)'); b = src.index('    chair(71.2, 8.4')
        blk = re.sub(r'(?<![\d.])(7[2-9](?:\.\d+)?|8[0-3](?:\.\d+)?)(?=[,"]| L)', lambda m: f'{float(m.group(1)) + dx:g}' , src[a:b])
        src = src[:a] + blk + src[b:]
    H = {'__name__': 'plan'}; sys.argv = ['x', '/dev/null', '/dev/null']; exec(src, H); return H
def inside(x, y, box=(67.9, 26.9, 86.1, 34.1)):
    return box[0] <= x <= box[2] and box[1] <= y <= box[3]
def svg(opt, vb=(62, 2, 34, 39)):
    H = load(opt.get('bed_dx', 0))
    H['ROOMS'] = [r for r in H['ROOMS'] if r[0] not in ('Suite foyer', 'Powder')]
    H['DOORS'] = [d for d in H['DOORS'] if not (d[1] in (27, 34) and 68 <= d[0] < 86 and d[0] != 87)]
    H['POCKETS'] = [p for p in H['POCKETS'] if p != ((70, 27), (73, 27))]
    H['SOUND'] = [s for s in H['SOUND'] if s != ((78.3, 27.7), (85.3, 27.7))]
    for r in opt.get('rooms', []):
        H['ROOMS'].append((re.sub(r'\s*\(.*?\)', '', r['name']), r['x1'], r['y1'], r['x2'], r['y2'], 'tile' if any(k in r['name'].lower() for k in ('powder', 'bath', 'laundry', 'wet', 'steam', 'sauna', 'wc', 'wash')) else 'wood', not r.get('open'), tuple(r.get('lab', (0, 0))), False))
    H['PARTS'] += [tuple(map(tuple, p)) for p in opt.get('parts', [])]
    H['DOORS'] += [tuple(d) for d in opt.get('doors', [])]
    H['POCKETS'] += [tuple(map(tuple, p)) for p in opt.get('pockets', [])]
    H['OPENINGS'] += [tuple(map(tuple, p)) for p in opt.get('openings', [])]
    base_f = H['furniture']
    def furn():
        s = base_f()
        s += '<rect x="68.2" y="27.2" width="17.6" height="6.6" style="fill:var(--pl-wood)"/>'
        for f in opt.get('fixtures', []):
            w, h = f['x2'] - f['x1'], f['y2'] - f['y1']
            s += f'<rect class="fu" x="{f["x1"]}" y="{f["y1"]}" width="{w:.2f}" height="{h:.2f}" rx=".12"/>'
            vert = h > w * 1.6
            cx, cy = f['x1'] + w / 2, f['y1'] + h / 2
            fs = min(.5, max(.32, (max(w, h) - .3) / max(1, len(f['label'])) * 1.7))
            tr = f' transform="rotate(-90 {cx:.2f} {cy:.2f})"' if vert else ''
            s += f'<text class="sk-d" x="{cx:.2f}" y="{cy + .15:.2f}" style="font-size:{fs:.2f}px"{tr}>{html.escape(f["label"])}</text>'
        return s
    H['furniture'] = furn
    body = H['landscape']() + H['building']('sk')
    # room labels: everything outside the strip as usual, strip rooms small
    lab = H['labels']('sk-t', 'sk-d')
    return (f'<svg class="plan sk" viewBox="{vb[0]} {vb[1]} {vb[2]} {vb[3]}" role="img"><rect class="sk-site" x="{vb[0]}" y="{vb[1]}" width="{vb[2]}" height="{vb[3]}"/>{body}{lab}</svg>'), H['CSS']
