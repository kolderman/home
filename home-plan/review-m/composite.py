"""Draft M candidate = draft L + office swap (layout 3) + great room G2 + guest wing G1, for the review.
Execs plan-generator.py (read only) and swaps its geometry globals."""
import sys, json
HP = '/mnt/project-files/home-plan/'
src = open(HP + 'plan-generator.py').read()
src = src[:src.rindex('\npage()')]
H = {'__name__': 'plan', '__file__': HP + 'plan-generator.py'}
sys.argv = ['x', '/dev/null', '/dev/null']
exec(compile(src, 'plan', 'exec'), H)

R = lambda n, x1, y1, x2, y2, fl='wood', w=True, off=(0, 0), show=True: (n, x1, y1, x2, y2, fl, w, off, show)
ROOMS = [
    # guest wing G1
    R("Bedroom 2", 0, 13, 24, 26.8, off=(-2, -1.2)),
    R("Vest. 2", 17.5, 26.8, 24, 32, show=False),
    R("Walk-in 2", 12, 26.8, 17.5, 34.4, show=False),
    R("Bath 2", 0, 26.8, 12, 34.4, 'tile', off=(1.5, -0.6)),
    R("Foyer", 17.5, 32, 24, 38, w=False, show=False, off=(0.6, 0.6)),
    R("Bedroom 3", 0, 34.4, 17.5, 46.7, off=(1.5, 1.6)),
    R("Server", 17.5, 38, 24, 46.7, show=False, off=(0, 1)),
    R("Bath 3", 0, 46.7, 11.4, 54, 'tile', off=(1.2, -1.2)),
    R("", 11.4, 46.7, 15.7, 54, show=False),
    R("Closet 3", 15.7, 46.7, 24, 54, show=False),
    R("Lounge", 7, 54, 24, 72, off=(0, -4.6)),
    # great room G2
    R("Living", 24, 34, 52, 62.5, w=False, off=(0, 9.5)),
    R("Kitchen", 52, 34, 68, 62.5, w=False, off=(-3.6, 1.5)),
    R("Dining", 52, 22, 68, 34, w=False, off=(-4.6, -3.6)),
    # office swap
    R("Primary bedroom", 68, 5, 86, 27, off=(0, -4.5)),
    R("Suite foyer", 68, 27, 78, 34, show=False, off=(0.5, 0.2)),
    R("Powder", 78, 27, 86, 34, 'tile', show=False, off=(0.6, -1.5)),
    R("Hall", 68, 34, 91, 38, w=False, show=False, off=(2, 0.4)),
    R("", 78.5, 38, 91, 40, w=False, show=False),
    R("Stairs", 68, 38, 71.75, 50.6, w=False, show=False),
    R("", 71.75, 38, 78.5, 50.6, w=False, show=False),
    R("Scullery", 68, 50.6, 78.5, 62.5, 'tile', off=(0, -1.0)),
    R("Primary bath", 86, -2.5, 106, 8, 'tile', off=(4, 1.0)),
    R("Dressing room", 86, 8, 106, 16, off=(-3.5, 0)),
    R("Office", 86, 16, 112, 32, off=(-1.5, 0.8)),
    R("Laundry", 91, 32, 106, 40, 'tile', off=(-3.0, -1.6)),
    R("Garage", 78.5, 40, 113, 66.5, 'conc', w=False, off=(-2.0, 4.0)),
]
PARTS = [p for p in H['PARTS'] if p not in [((73.6, 28), (73.6, 30.5)), ((72, 30.5), (73.6, 30.5))]]
SHELL = [(0, 13), (24, 13), (24, 34), (52, 34), (52, 22), (68, 22), (68, 5), (86, 5), (86, -2.5), (106, -2.5),
         (106, 16), (112, 16), (112, 32), (106, 32),
         (106, 40), (102.4, 40), (102.4, 46.4), (113, 46.4), (113, 55.5), (107.5, 55.5), (107.5, 66.5), (78.5, 66.5), (78.5, 62.5),
         (24, 62.5), (24, 72), (7, 72), (7, 54), (0, 54)]
PORCHES = [H['PORCHES'][0], H['PORCHES'][1], H['PORCHES'][2],
           ("Stoop", [(106, 32), (112, 32), (112, 40), (106, 40)], (109, 36.6)), H['PORCHES'][4]]
POSTS = [p for p in H['POSTS'] if p != (111.5, 16.5)]
drop_w = [((70.6, 5), (74.3, 5)), ((75.4, 5), (79, 5)), ((80, 5), (83.3, 5)), ((56, 59), (64, 59)), ((26.5, 62.5), (32.5, 62.5)), ((42.5, 62.5), (48.5, 62.5))]
WINDOWS = [w for w in H['WINDOWS'] if w not in drop_w] + [
    ((26, 62.5), (33, 62.5)), ((42, 62.5), (49, 62.5)), ((55, 62.5), (65, 62.5)),     # G1/G2 front windows
    ((24, 14), (24, 19)), ((24, 32.3), (24, 33.4)),                                       # guest wing G1: bedroom 2 side window, foyer sidelight
    ((112, 18.5), (112, 24.5)), ((106.5, 16), (111, 16)),                                 # office layout 3
    ((68, 5.5), (68, 8)),                                                                 # bedroom corner glass
]
SLIDERS = []
GLASSWALLS = [H['GLASSWALLS'][0], ((69, 5), (85, 5), 4, (85, 85))]
SOUND = [((86.7, 16.7), (86.7, 31.3)), ((86.7, 16.7), (111.3, 16.7)), ((86.7, 31.3), (105.3, 31.3)),
         ((68.7, 5.7), (68.7, 26.3)), ((78.3, 27.7), (85.3, 27.7)), ((91.6, 32.7), (105.4, 32.7)), ((18.2, 38.7), (18.2, 46))]
D = H['DOORS']
keep = lambda d: d in D
DOORS = [
    (19.8, 32, 3, 'h', -1, False),        # guest suite 2 door (hinge x 22.8)
    (17.5, 34.8, 3, 'v', 1, False),       # bedroom 3 from the guest foyer (hinge y 37.8)
    (20.6, 38, 3, 'h', 1, False),         # server (hinge x 23.6)
    (24, 34.5, 3.4, 'v', -1, False),      # sealed door, living to guest foyer (hinge y 37.9)
    (15.7, 47.2, 2.4, 'v', 1, True),      # closet 3
    (34.5, 62.5, 3, 'h', -1, True), (37.5, 62.5, 3, 'h', -1, False),
    (47, 34, 3, 'h', -1, False),
    (68.5, 34, 3, 'h', -1, True),         # suite foyer
    (80.5, 34, 2.5, 'h', -1, True),       # powder
    (87, 32, 3, 'h', -1, True),           # office
    (87, 8, 2.83, 'h', -1, True), (89.2, 2.5, 2.4, 'h', 1, False),
    (91, 33, 2.75, 'v', 1, True), (106, 32.3, 3, 'v', -1, False),
    (87, 40, 3, 'h', -1, False), (75.5, 38, 2.5, 'h', 1, False),
    (57.5, 22, 2.5, 'h', 1, True), (60, 22, 2.5, 'h', 1, False),
    (24, 55.5, 3, 'v', 1, True), (24, 58.5, 3, 'v', 1, False),
]
OPENINGS = [((68.4, 38), (71.5, 38)), ((11.6, 46.7), (15.5, 46.7)), ((86.2, 2.5), (88, 2.5)), ((100.6, 2.5), (103.6, 2.5)),
            ((18.5, 26.8), (23.4, 26.8)), ((68, 53.5), (68, 56.8)), ((86, 10.5), (86, 13.5))]
POCKETS = [((17.5, 29.4), (17.5, 31.9)), ((12, 29.4), (12, 31.9)), ((11.4, 47.2), (11.4, 49.6)), ((70, 27), (73, 27)), ((86, 5.3), (86, 7.8))]
BEAMS = [b for b in H['BEAMS'] if b != ((52, 62.5), (68, 62.5))] + [((106, 16), (106, 32)), ((24, 48.25), (52, 48.25)), ((52, 34), (52, 62.5)), ((68.5, 5), (85.5, 5))]

for k, v in dict(ROOMS=ROOMS, PARTS=PARTS, SHELL=SHELL, PORCHES=PORCHES, POSTS=POSTS, WINDOWS=WINDOWS, SLIDERS=SLIDERS,
                 GLASSWALLS=GLASSWALLS, SOUND=SOUND, DOORS=DOORS, OPENINGS=OPENINGS, BEAMS=BEAMS).items():
    H[k] = v

# fixtures, from the option geometry where it exists
BS = HP + 'blueprint-study/'
res = json.load(open(BS + 'result.json'))['synth']['great']['options']
g2 = [o for o in res if o['id'] == 'G2'][0]
wing = [o for o in json.load(open(BS + 'wing-result.json'))['synth']['options'] if o['id'] == 'G1'][0]
off = json.load(open(BS + 'office-layout.json'))
FX = []
def fx(label, x1, y1, x2, y2, k='fx'): FX.append(dict(label=label, x1=x1, y1=y1, x2=x2, y2=y2, k=k))
for f in g2['fixtures']:
    l = f['label']
    if any(s in l for s in ('truss', 'rafter', 'Glulam', 'Ridge post', 'portal', 'Portal', 'Chandelier', 'moment')): continue
    fx(l, f['x1'], f['y1'], f['x2'], f['y2'])
for f in wing['fixtures']: fx(f['label'], f['x1'], f['y1'], f['x2'], f['y2'])
for f in off['fixtures']:
    if f['label'] in ('King bed', 'Nightstand', 'Sitting area', 'Dresser', 'Morning bar', 'Bench', 'Powder vanity', 'Powder WC'):
        fx(f['label'], f['x1'], f['y1'], f['x2'], f['y2'])
# office layout 3 (from office3.py)
for l, a, b, c, d in [('Media console', 89.5, 16.2, 98.5, 17.6), ('L couch', 89.5, 26, 100, 29), ('Couch return', 86.5, 21, 89.5, 29),
                      ('Lounge chair', 100.6, 20, 103.6, 23), ('Coffee table', 91.5, 21, 97.5, 23.8), ('Desk', 104.5, 29.4, 111.8, 31.8),
                      ('Desk return', 109.4, 25.4, 111.8, 29.4), ('Desk chair', 105.8, 26.6, 107.8, 28.6), ('Bookcase', 103.5, 16.2, 106, 22)]:
    fx(l, a, b, c, d)
# unchanged rooms (draft L furniture, bath and dressing shifted 2.5 ft back as drawn)
for l, a, b, w, h in [('Tub', 92.2, -2.1, 6.2, 3), ('Bench', 92.6, 3.0, 3.6, 1.1), ('Shower', 100.2, -2.1, 5.4, 4.2), ('Vanity', 90.8, 6.1, 8.8, 1.7),
                      ('Vanity', 100, 6.1, 2.6, 1.7), ('Tower', 104.1, 3.1, 1.5, 4.7), ('Wardrobes', 90.6, 8.2, 13.6, 2.0), ('Wardrobes', 90.6, 14.0, 13.6, 2.0),
                      ('Window seat', 104.3, 10.7, 1.3, 3.0), ('Mirror (draft L)', 86.3, 10.6, 0.4, 3.2), ('WC', 86.6, -2.2, 1.8, 2.4),
                      ('Laundry counter', 91.2, 37.9, 9.6, 1.9), ('Washer', 101, 37.6, 2.2, 2.1), ('Dryer', 103.4, 37.6, 2.2, 2.1),
                      ('Drop zone', 78.7, 38.3, 7.6, 1.5), ('Scullery counter', 68.4, 60.3, 9.7, 1.8), ('Scullery counter', 68.4, 50.8, 9.7, 1.8),
                      ('Scullery counter', 68.2, 57.6, 1.8, 2.7), ('Wine wall', 66, 23, 1.9, 10.5), ('Bookcase', 7.4, 54.6, 1.5, 5.5), ('Bookcase', 7.4, 65.9, 1.5, 5.7),
                      ('Closet shelving', 77.1, 40.8, 1.2, 9.4)]:
    fx(l, a, b, a + w, b + h)
CIRCLES = [(59.5, 29.6, 2.4), (16, 63.5, 1.8)]   # dining table, lounge table

def fixtures_svg():
    s = []
    for f in FX:
        cls = 'fx-m' if f['label'].startswith('Mirror') else 'fx'
        s.append(f'<rect class="{cls}" x="{f["x1"]}" y="{f["y1"]}" width="{f["x2"] - f["x1"]:.2f}" height="{f["y2"] - f["y1"]:.2f}" rx=".12"/>')
    for x, y, r in CIRCLES: s.append(f'<circle class="fx" cx="{x}" cy="{y}" r="{r}"/>')
    for (x1, y1), (x2, y2) in POCKETS:
        if x1 == x2: s.append(f'<rect class="bp-gap" x="{x1 - .45}" y="{y1}" width=".9" height="{y2 - y1}"/><line class="pk" x1="{x1}" x2="{x1}" y1="{y1}" y2="{y2}"/>')
        else: s.append(f'<rect class="bp-gap" x="{x1}" y="{y1 - .45}" width="{x2 - x1}" height=".9"/><line class="pk" x1="{x1}" x2="{x2}" y1="{y1}" y2="{y2}"/>')
    return ''.join(s)

def plan(markers='', vb=(-6, -9, 124, 86), extra='', aria='Draft M candidate floor plan'):
    body = H['building']('bp') + fixtures_svg() + H['labels']('bp-t', 'bp-d')
    return (f'<svg class="plan" viewBox="{vb[0]} {vb[1]} {vb[2]} {vb[3]}" role="img" aria-label="{aria}">'
            f'<rect class="bp-bg" x="{vb[0]}" y="{vb[1]}" width="{vb[2]}" height="{vb[3]}"/>{body}{extra}{markers}</svg>')
