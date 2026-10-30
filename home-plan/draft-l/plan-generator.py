"""Generate the home floor plan page: a rendered sketch and a to-scale blueprint.
All geometry is in feet. x runs left to right across the front, y runs back (pond) to front (street)."""
import math, sys, os

OUT = sys.argv[1]
TEMPLATE = sys.argv[2]

def fmt(ft):
    f = int(ft); i = round((ft - f) * 12)
    if i == 12: f, i = f + 1, 0
    return f"{f}'-{i}\""

def short(ft):
    f = int(ft); i = round((ft - f) * 12)
    return f"{f}'" if i == 0 else f"{f}'{i}\""

# ---------------------------------------------------------------- rooms
# name, x1, y1, x2, y2, floor, draw walls, label offset (dx, dy), show size
ROOMS = [
    ("Bedroom 2", 0, 13, 24, 26.8, "wood", True, (4, -1.5), True),
    ("", 19.4, 26.8, 24, 31, "wood", True, (0, 0), False),
    ("Bath 2", 0, 26.8, 13, 34.4, "tile", True, (1.6, -0.4), True),
    ("WIC", 13, 26.8, 19.4, 31, "wood", True, (-0.6, 0.3), False),
    ("Hall", 13, 31, 24, 34.4, "wood", False, (0.5, 0.3), False),
    ("", 17.5, 34.4, 24, 38, "wood", False, (0, 0), False),
    ("", 17.5, 34.4, 19.5, 38, "wood", True, (0, 0), False),
    ("Bedroom 3", 0, 34.4, 17.5, 46.7, "wood", True, (2.8, 2.6), True),
    ("Bath 3", 0, 46.7, 11.4, 54, "tile", True, (0.6, -1.4), True),
    ("", 11.4, 46.7, 15.7, 54, "wood", True, (0, 0), False),
    ("Server", 17.5, 38, 24, 46.7, "wood", True, (-1, 0.2), False),
    ("Closet", 15.7, 46.7, 24, 54, "wood", True, (0.4, 0.6), False),
    ("Lounge", 7, 54, 24, 72, "wood", True, (0, -4.6), True),
    ("Living", 24, 34, 52, 62.5, "wood", False, (0, 6.8), True),
    ("Kitchen", 52, 34, 68, 59, "wood", False, (-3.5, 7.0), True),
    ("Dining", 52, 22, 68, 34, "wood", False, (-5.6, -3.4), True),
    ("Office", 68, 5, 86, 34, "wood", True, (-0.5, 5.8), True),
    ("", 68, 28, 72, 34, "wood", True, (0, 0), False),
    ("Powder", 72, 28, 79, 34, "tile", True, (0, 1.6), False),
    ("Hall", 68, 34, 91, 38, "wood", False, (0, 0.4), False),
    ("", 78.5, 38, 91, 40, "wood", False, (0, 0), False),
    ("Stairs", 68, 38, 71.75, 50.6, "wood", False, (0, 0), False),
    ("", 71.75, 38, 78.5, 50.6, "wood", False, (0, 0), False),
    ("Scullery", 68, 50.6, 78.5, 62.5, "tile", True, (0, -1.0), True),
    ("Primary bath", 86, -2.5, 106, 8, "tile", True, (4, 1.0), True),
    ("Dressing room", 86, 8, 106, 16, "wood", True, (-3.5, 0), True),
    ("Primary bedroom", 86, 16, 106, 32, "wood", True, (0, 4.6), True),
    ("Laundry", 91, 32, 106, 40, "tile", True, (-3.0, -1.6), True),
    ("Garage", 78.5, 40, 113, 66.5, "conc", False, (-2.0, 4.0), True),
]
# extra interior partitions (WC room, shower)
PARTS = [((78.5, 40), (91, 40)), ((86, 2.5), (91.8, 2.5)), ((91.8, -2.5), (91.8, 2.5)), ((100, -2.5), (100, 2.5)), ((24, 31), (24, 38)),
         ((86, 0.9), (88.2, 0.9)), ((88.2, 0.9), (88.2, 2.5)), ((99.8, 5.4), (99.8, 8)), ((100, 2.5), (106, 2.5)),
         ((73.6, 28), (73.6, 30.5)), ((72, 30.5), (73.6, 30.5)), ((71.75, 38), (71.75, 46.73)), ((68, 38), (68, 50.6)), ((68, 38), (78.5, 38)), ((78.5, 38), (78.5, 50.6))]

PORCHES = [
    ("Back porch", [(24, 20), (46, 20), (46, 10), (68, 10), (68, 22), (52, 22), (52, 34), (24, 34)], (35, 23.5)),
    ("Outdoor kitchen", None, (60.2, 19.2)),
    ("Front porch", [(24, 62.5), (52, 62.5), (52, 72), (24, 72)], (38, 69.6)),
    ("Side|porch", [(106, 16), (112, 16), (112, 40), (106, 40)], (109, 30.4)),
    ("Trash", [(102.4, 40), (113, 40), (113, 46.4), (102.4, 46.4)], (106.2, 45.5)),
]
POSTS = [(24.5, 20.5), (29.5, 20.5), (45.5, 20.5), (46.5, 10.5), (57, 10.5), (67.5, 10.5),
         (24.5, 71.5), (33.2, 71.5), (41.8, 71.5), (51.5, 71.5), (111.5, 16.5), (111.5, 39.5), (107.1, 40.4)]

# exterior envelope (house + garage)
SHELL = [(0, 13), (24, 13), (24, 34), (52, 34), (52, 22), (68, 22), (68, 5), (86, 5), (86, -2.5), (106, -2.5),
         (106, 40), (102.4, 40), (102.4, 46.4), (113, 46.4), (113, 55.5), (107.5, 55.5), (107.5, 66.5), (78.5, 66.5), (78.5, 62.5),
         (68, 62.5), (68, 59), (52, 59), (52, 62.5), (24, 62.5), (24, 72), (7, 72), (7, 54), (0, 54)]

# windows: wall segments
WINDOWS = [((10.5, 13), (19.5, 13)), ((0, 28.5), (0, 31)), ((0, 38), (0, 43)),
           ((0, 48.5), (0, 51)), ((8.5, 72), (22.5, 72)),
           ((26.5, 62.5), (32.5, 62.5)),
           ((42.5, 62.5), (48.5, 62.5)), ((52, 25), (52, 30)), ((56, 59), (64, 59)),
           ((70.6, 5), (74.3, 5)), ((75.4, 5), (79, 5)), ((80, 5), (83.3, 5)), ((92, -2.5), (98, -2.5)), ((106, -1), (106, 1.5)),
           ((106, 10.5), (106, 13.5)), ((71, 62.5), (76, 62.5))]
# sliding doors: wall segments
SLIDERS = [((106, 20), (106, 28))]
# 16 ft multi-slide glass wall centered on the front doors (x 37.5); four panels stack into a pocket on the left
GLASSWALLS = [((29.5, 34), (45.5, 34), 4, (25.1, 29.5))]
# sound-isolated walls (double or staggered studs): all four office walls and the laundry/primary wall, drawn just inside the room
SOUND = [((68.7, 5.7), (68.7, 27.3)), ((68.7, 5.7), (85.3, 5.7)), ((85.3, 5.7), (85.3, 33.3)), ((68.7, 27.3), (78.4, 27.3)),
         ((78.4, 27.3), (78.4, 33.3)), ((78.4, 33.3), (85.3, 33.3)), ((91.6, 32.7), (105.4, 32.7))]

# doors: (x, y, width, axis, swing_sign, hinge_at_start) ; axis 'h' = wall along x, 'v' = wall along y
DOORS = [
    (20.2, 31, 3, 'h', -1, False), (13.1, 34.4, 3, 'h', 1, True),
    (7, 26.8, 2.5, 'h', 1, True), (13.4, 26.8, 2.2, 'h', 1, True), 
    (20.6, 38, 3, 'h', 1, True), (19.5, 34.8, 2.2, 'v', 1, True), (11.4, 47.2, 2.4, 'v', -1, True), (15.7, 47.2, 2.4, 'v', 1, True),
    (34.5, 62.5, 3, 'h', -1, True), (37.5, 62.5, 3, 'h', -1, False),
    (47, 34, 3, 'h', -1, False), (72, 30.8, 2.5, 'v', 1, False), (68.5, 34, 3, 'h', -1, True), (68.6, 28, 2.8, 'h', -1, True),
    (87, 32, 3, 'h', -1, True), (87, 8, 2.83, 'h', -1, True), (89.2, 2.5, 2.4, 'h', 1, False),
    (91, 33, 2.75, 'v', 1, True), (106, 32.3, 3, 'v', -1, False),
    (87, 40, 3, 'h', -1, False), (75.5, 38, 2.5, 'h', 1, False),
    (57.5, 22, 2.5, 'h', 1, True), (60, 22, 2.5, 'h', 1, False),  # dining French doors to the outdoor kitchen
    (24, 55.5, 3, 'v', 1, True), (24, 58.5, 3, 'v', 1, False),  # steel-and-glass doors, living to lounge
]
OPENINGS = [((24, 34.5), (24, 37.9)), ((68.4, 38), (71.5, 38)), ((11.6, 46.7), (15.5, 46.7)), ((86.2, 2.5), (88, 2.5)), ((100.6, 2.5), (103.6, 2.5)), ((72, 28.3), (72, 30.3)), ((19.8, 26.8), (23.6, 26.8)), ((87, 16), (90, 16)),
            ((68, 53.5), (68, 56.8))]
GARAGE = [(78.5, 40), (102.4, 40), (102.4, 46.4), (113, 46.4), (113, 55.5), (107.5, 55.5), (107.5, 66.5), (78.5, 66.5)]
GARAGE_DOORS = [((80.4, 66.5), (101.2, 66.5)), ((113, 47.2), (113, 52.4))]
CARS = []
# garage built-ins traced from the sketch: deep shelving, storage closet, cabinets
FIREPLACES = [(7, 60.5, 1.4, 5.0)]  # x, y, depth into the room, width along the wall: flush gas insert on the lounge's left wall
GENPAD = (109.0, 58.4, 3.1, 5.0)  # standby generator pad 18" off the garage side wall, in the notch below the side roll-up
BUILTINS = [(102.2, 53.6, 10.4, 1.8), (102.2, 55.6, 4.9, 2.2), (105.3, 58.8, 1.8, 3.8), (102.4, 63.6, 4.7, 2.5)]
STAIR_NOTE = "UP"
# 20-minute rated, self-closing pass door from the garage to the scullery (replaces the open grocery hatch), counter height
PASSDOORS = [((78.5, 55), (78.5, 57.5))]
# beams that carry a roof over an opening with no wall: the courtyard eave in front of the kitchen, the bonus room over the trash corner
BEAMS = [((52, 62.5), (68, 62.5)), ((102.4, 40), (107.5, 40)), ((107.5, 40), (107.5, 46.4)), ((107.5, 46.4), (107.5, 55.5))]
# 3' landing on the garage side of the garage-to-hall door (the garage floor sits a step down)
STOOP = (86.5, 40, 4, 3)
# stair: 20 risers of 7.6" to the bonus floor at 12'-8"; run 1 climbs toward the front, a landing, run 2 turns right into the bonus room
RISERS, UPPER_Z = 20, 12 + 8 / 12
RUN1 = (68.4, 38.4, 71.6, 10)      # x1, y start, x2, treads (10" each), climbing toward the front
LANDING = (68.4, 46.73, 71.6, 50.23)
RUN2 = (71.75, 46.73, 50.23, 8)    # x start, y1, y2, treads, climbing to the right

# ---------------------------------------------------------------- roof
# Planes in roofkit.py. Every roof drains: hips and gables meet in sloped valleys, never in a level trough or against a wall.
try:
    _HERE = os.path.dirname(os.path.abspath(__file__))
except NameError:
    _HERE = '/mnt/project-files/home-plan'
sys.path.insert(0, _HERE)
from roofkit import Roof
K10, K8, KP = 10 / 12, 8 / 12, 1.5 / 12
DORMERS, DORMER_PLATE = [(83.3, 89.7), (96.3, 102.7)], 20.5   # plate leaves room for a header over the 19'-5" window head
DORMER_Y = 66.5 - (DORMER_PLATE - 16) / K10    # where the garage roof climbs past the dormer walls: the eave is cut from here forward
ROOFS = [
    # main gable over the great room, kitchen and stair; its left gable end stands on the bedroom wing roof at x 7
    Roof('Great room', 7, 34, 78.5, 62.5, plate=12, pitch=K8, ax='x', ends=('gable', 'gable'), ov=(0, 1.5), rake=(1.0, 0.15)),
    # bedroom wing: hipped at the back, its ridge runs into the great room roof
    Roof('Bedroom wing', 0, 13, 24, 54, plate=10, pitch=K8, ax='y', ends=('hip', 'gable'), ov=(1.5, 1.5), rake=(0, 1.0),
         clip=[(-2, 11, 26, 50), (-2, 49, 7, 55)]),   # past y 50 only the strip in front of the lounge needs it
    # lounge: steep front-facing gable toward the street, running back into the great room roof
    Roof('Lounge', 7, 50, 24, 72, plate=11, pitch=K10, ax='y', ends=('open', 'gable'), ov=(1.5, 1.5), rake=(0, 1.0)),
    # office and primary suite under one hip roof, ridge front to back, running into the garage roof
    Roof('Office and primary', 68, 5, 106, 52, plate=11, pitch=K8, ax='y', ends=('hip', 'open'), ov=(1.0, 0.5), hov=1.5),
    Roof('Primary bath', 86, -2.5, 106, 20, plate=11, pitch=K8, ax='y', ends=('hip', 'open'), ov=(1.0, 0.5)),
    # garage: side gable on 16 ft walls, so the bonus room gets 3'-4" knee walls and a full-height middle
    Roof('Garage', 78.5, 40, 107.5, 66.5, plate=16, pitch=K10, ax='x', ends=('gable', 'gable'), ov=(1.5, 1.5), rake=(1.0, 1.0),
         clip=[(77, 38, 109, DORMER_Y)] + [(a, DORMER_Y, b, 69) for a, b in zip([77] + [d[1] for d in DORMERS], [d[0] for d in DORMERS] + [109])]),
    # two wall dormers on the front of the garage roof: the bonus room's front wall runs up through the eave into a small gable
    *[Roof('Dormer', x1, 58, x2, 66.5, plate=DORMER_PLATE, pitch=K10, ax='y', ends=('open', 'gable'), ov=(0.5, 0.5), rake=(0, 0.5)) for x1, x2 in DORMERS],
    # dining bump-out: low standing-seam shed sloping to the back
    Roof('Dining', 52, 22, 80, 42, kind='shed', hi='y2', H=11.85 + 20 * 2 / 12, pitch=2 / 12, ov=(1.5,), rake=(0.6, 0), mat='seam'),
    # back porch and outdoor kitchen share one standing-seam plane, tied in under the great room's 12 ft plate
    Roof('Back porch', 21, 20, 52, 34, kind='shed', hi='y2', H=11.5, pitch=KP, ov=(1.5,), rake=(0, 0.15), mat='seam'),
    Roof('Outdoor kitchen', 46, 10, 68, 22, kind='shed', hi='y2', H=11.5 - 12 * KP, pitch=KP, ov=(1.5,), rake=(0.6, 0), mat='seam'),
    Roof('Front porch', 24, 62.5, 52, 72, kind='shed', hi='y1', H=10.9, pitch=2.6 / 12, ov=(1.5,), rake=(0.15, 0.6), mat='seam'),
    Roof('Side porch', 106, 16, 112, 40, kind='shed', hi='x1', H=10.4, pitch=3 / 12, ov=(1.5,), rake=(0.6, 0.6), mat='seam'),
    Roof('Mower bay', 107.5, 46.4, 113, 55.5, kind='shed', hi='x1', H=12.5, pitch=3 / 12, ov=(1.5,), rake=(0.6, 0.6), mat='seam'),
]
# top of the outside walls, by area (feet above the main floor)
PLATES = [(0, 13, 24, 54, 10), (7, 54, 24, 72, 11), (24, 34, 78.5, 62.5, 12), (52, 22, 68, 34, 11.5), (68, 5, 86, 40, 11), (86, -2.5, 106, 40, 11), (78.5, 40, 107.5, 66.5, 16)]


def poly(pts):
    return " ".join(f"{x:.2f},{y:.2f}" for x, y in pts)


def area(pts):
    a = 0
    for (x1, y1), (x2, y2) in zip(pts, pts[1:] + pts[:1]):
        a += x1 * y2 - x2 * y1
    return abs(a) / 2


shell_area = area(SHELL)
garage_area = (113 - 78.5) * (66.5 - 40) - (113 - 107.5) * (66.5 - 55.5) - (113 - 102.4) * 6.4
living_area = shell_area - garage_area
porch_area = area(PORCHES[0][1]) + area(PORCHES[2][1]) + area(PORCHES[3][1])  # trash pad excluded


def door_svg(d, gap_cls, line_cls, arc_cls):
    x, y, w, ax, s, hs = d
    out = []
    t = 0.9
    if ax == 'h':
        out.append(f'<rect class="{gap_cls}" x="{x}" y="{y - t / 2}" width="{w}" height="{t}"/>')
        hx = x if hs else x + w
        ox = x + w if hs else x
        ty = y + s * w
        out.append(f'<line class="{line_cls}" x1="{hx}" y1="{y}" x2="{hx}" y2="{ty}"/>')
        sweep = 1 if (hs and s > 0) or (not hs and s < 0) else 0
        out.append(f'<path class="{arc_cls}" d="M{hx},{ty} A{w},{w} 0 0 {1 - sweep} {ox},{y}"/>')
    else:
        out.append(f'<rect class="{gap_cls}" x="{x - t / 2}" y="{y}" width="{t}" height="{w}"/>')
        hy = y if hs else y + w
        oy = y + w if hs else y
        tx = x + s * w
        out.append(f'<line class="{line_cls}" x1="{x}" y1="{hy}" x2="{tx}" y2="{hy}"/>')
        sweep = 1 if (hs and s < 0) or (not hs and s > 0) else 0
        out.append(f'<path class="{arc_cls}" d="M{tx},{hy} A{w},{w} 0 0 {1 - sweep} {x},{oy}"/>')
    return "".join(out)


def window_svg(w, gap_cls, line_cls):
    (x1, y1), (x2, y2) = w
    t = 0.75
    if y1 == y2:
        r = f'<rect class="{gap_cls}" x="{x1}" y="{y1 - t / 2}" width="{x2 - x1}" height="{t}"/>'
        l = "".join(f'<line class="{line_cls}" x1="{x1}" x2="{x2}" y1="{y1 + o}" y2="{y1 + o}"/>' for o in (-t / 2, 0, t / 2))
    else:
        r = f'<rect class="{gap_cls}" x="{x1 - t / 2}" y="{y1}" width="{t}" height="{y2 - y1}"/>'
        l = "".join(f'<line class="{line_cls}" y1="{y1}" y2="{y2}" x1="{x1 + o}" x2="{x1 + o}"/>' for o in (-t / 2, 0, t / 2))
    return r + l


def opening_svg(o, gap_cls, line_cls):
    (x1, y1), (x2, y2) = o
    t = 0.9
    if y1 == y2:
        return (f'<rect class="{gap_cls}" x="{x1}" y="{y1 - t / 2}" width="{x2 - x1}" height="{t}"/>'
                f'<line class="{line_cls}" x1="{x1}" x2="{x1}" y1="{y1 - t / 2}" y2="{y1 + t / 2}"/>'
                f'<line class="{line_cls}" x1="{x2}" x2="{x2}" y1="{y1 - t / 2}" y2="{y1 + t / 2}"/>')
    return (f'<rect class="{gap_cls}" x="{x1 - t / 2}" y="{y1}" width="{t}" height="{y2 - y1}"/>'
            f'<line class="{line_cls}" y1="{y1}" y2="{y1}" x1="{x1 - t / 2}" x2="{x1 + t / 2}"/>'
            f'<line class="{line_cls}" y1="{y2}" y2="{y2}" x1="{x1 - t / 2}" x2="{x1 + t / 2}"/>')


def stairs(cls):
    s = []
    x1, y0, x2, n = RUN1
    T = 10 / 12
    s.append(f'<rect class="{cls}" x="{x1}" y="{y0}" width="{x2 - x1}" height="{n * T:.2f}"/>')
    for i in range(1, n):
        yy = y0 + i * T
        s.append(f'<line class="{cls}" x1="{x1}" x2="{x2}" y1="{yy:.2f}" y2="{yy:.2f}"/>')
    lx1, ly1, lx2, ly2 = LANDING
    s.append(f'<rect class="{cls}" x="{lx1}" y="{ly1}" width="{lx2 - lx1}" height="{ly2 - ly1}"/>')
    # run 2 passes over the closet, above the cut line: dashed
    xs, a, b, n2 = RUN2
    s.append(f'<rect class="{cls} ovh" x="{xs}" y="{a}" width="{n2 * T:.2f}" height="{b - a}"/>')
    for i in range(1, n2):
        xx = xs + i * T
        s.append(f'<line class="{cls} ovh" x1="{xx:.2f}" x2="{xx:.2f}" y1="{a}" y2="{b}"/>')
    return "".join(s)

STAIR_ARROW = "M70,39.2 L70,48.5 L77.4,48.5 M76.5,47.9 L77.4,48.5 L76.5,49.1"


# ---------------------------------------------------------------- furniture (sketch only)
def furniture():
    f = []
    R = lambda x, y, w, h, r=0.25, c="fu": f.append(f'<rect class="{c}" x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}"/>')
    C = lambda x, y, r, c="fu": f.append(f'<circle class="{c}" cx="{x}" cy="{y}" r="{r}"/>')
    P = lambda d, c="fu": f.append(f'<path class="{c}" d="{d}"/>')

    def bed(x, y, w, h, head):  # head: 'l','t'
        R(x, y, w, h, 0.3)
        if head == 'l':
            R(x + 0.4, y + 0.5, 1.4, h / 2 - 0.8, 0.3, "fu2"); R(x + 0.4, y + h / 2 + 0.3, 1.4, h / 2 - 0.8, 0.3, "fu2")
            P(f"M{x + w * .45},{y} L{x + w * .45},{y + h}", "fl")
        else:
            R(x + 0.5, y + 0.4, w / 2 - 0.8, 1.4, 0.3, "fu2"); R(x + w / 2 + 0.3, y + 0.4, w / 2 - 0.8, 1.4, 0.3, "fu2")
            P(f"M{x},{y + h * .45} L{x + w},{y + h * .45}", "fl")

    def chair(cx, cy, a=0, s=2.6):
        f.append(f'<g transform="rotate({a} {cx} {cy})"><rect class="fu" x="{cx - s / 2}" y="{cy - s / 2}" width="{s}" height="{s}" rx="0.5"/>'
                 f'<rect class="fu2" x="{cx - s / 2}" y="{cy - s / 2}" width="{s}" height="0.6" rx="0.3"/></g>')

    def sofa(x, y, w, h, back):  # back: 't','b','l','r'
        R(x, y, w, h, 0.5)
        if back == 'b': R(x, y + h - 0.8, w, 0.8, 0.4, "fu2")
        if back == 't': R(x, y, w, 0.8, 0.4, "fu2")
        if back == 'r': R(x + w - 0.8, y, 0.8, h, 0.4, "fu2")
        if back == 'l': R(x, y, 0.8, h, 0.4, "fu2")

    def toilet(x, y, rot):
        f.append(f'<g transform="rotate({rot} {x} {y})"><rect class="fu" x="{x - 0.9}" y="{y - 1.3}" width="1.8" height="0.7" rx="0.2"/>'
                 f'<ellipse class="fu" cx="{x}" cy="{y + 0.3}" rx="0.8" ry="1.0"/></g>')

    def sink(x, y): f.append(f'<ellipse class="fu2" cx="{x}" cy="{y}" rx="0.7" ry="0.5"/>')

    # rugs first
    for x, y, w, h in [(27, 36.5, 19, 19.5), (27.5, 22.5, 18, 10.5), (2.5, 15, 14, 11), (2.5, 36.2, 10.5, 9.6),
                       (89, 17.5, 14, 11), (10, 57.5, 12, 12), (71.2, 8.0, 9.0, 7.6)]:
        R(x, y, w, h, 0.4, "rug")
    # bedroom 2
    bed(0.6, 16.6, 7, 5.3, 'l'); R(0.6, 14.6, 1.7, 1.6); R(0.6, 22.3, 1.7, 1.6); R(22.9, 16, 0.7, 6, 0.1, "tv")
    chair(21.5, 15.2, 30)
    # bath 2: tub and shower on the outside wall, toilet, one sink
    R(0.4, 27.0, 3.4, 7.2, 0.1, "wet"); toilet(5.4, 32.9, 180)
    R(7.4, 32.8, 5.4, 1.4, 0.1); sink(10.1, 33.5)
    # bedroom 2 walk-in closet
    R(13.2, 27.2, 6, 1.1, 0.1); R(18, 28.5, 1.2, 2.3, 0.1)
    # bedroom 3: TV built-in on the right wall, reach-in closet on the outside wall
    bed(0.6, 38, 7, 5.3, 'l'); R(0.6, 36, 1.7, 1.6); R(0.6, 43.7, 1.7, 1.6)
    R(15.6, 38.4, 1.7, 6.1, 0.1, "fu2"); R(15.2, 39.5, 0.4, 3.9, 0.1, "tv")
    # server room and the closet below it, both lined with shelving
    R(22.2, 41.2, 1.6, 3.8, 0.1, "fu2"); R(17.7, 45.1, 6.1, 1.4, 0.1)
    R(17.8, 38.7, 0.5, 1.6, 0.05); R(17.8, 40.6, 0.5, 1.6, 0.05)
    R(17.7, 34.6, 1.6, 2.7, 0.1, "fu2"); f.append('<text class="sk-d" x="18.5" y="36.3" style="font-size:.55px">linen</text>')  # electrical and network panels
    R(15.9, 52.6, 7.9, 1.2, 0.1); R(22.6, 46.9, 1.2, 5.7, 0.1); P("M17.4,50.3 L22,50.3", "fl")
    # bath 3 and the closet open off a 4' vestibule below bedroom 3, with a cabinet at its end
    R(0.4, 46.9, 2.2, 6.7, 0.1, "wet"); P("M2.6,46.9 L2.6,53.6", "fl")
    toilet(5, 52.3, 180); R(7.2, 52.2, 4, 1.4, 0.1); sink(9.2, 52.9)
    R(11.6, 52.0, 3.9, 1.6, 0.1, "fu2")
    # living media wall with the TV
    R(24.25, 39, 1.55, 15.7, 0.1, "fu2"); R(25.75, 46, 0.45, 2.5, 0.1, "tv")
    # lounge: tub chairs around a round table; green-lacquer bookcases either side of the fireplace (bar cabinet in one)
    R(7.4, 54.6, 1.5, 5.5, 0.1, "bk"); R(7.4, 65.9, 1.5, 5.7, 0.1, "bk")
    C(16, 63.5, 1.8); chair(12.4, 59.9, -45, 3); chair(19.6, 59.9, 45, 3); chair(12.4, 67.1, -135, 3); chair(19.6, 67.1, 135, 3)
    # living
    sofa(30.5, 37.2, 10.5, 3, 't'); R(32.5, 43.6, 7, 2.6, 0.5); chair(30.2, 52.5, 30, 3.2); chair(40.8, 52.5, -30, 3.2)
    sofa(42, 41.5, 3, 9, 'r'); R(46, 42.3, 2.7, 8.3, 0.1, "fu2")
    for yy in (43.6, 46.4, 49.2): C(49.6, yy, 0.7)
    C(36.7, 52.7, 0.9)
    # tree in the entry
    C(48.2, 59, 3.2, "pl"); C(48.2, 59, 1.3, "pl2")
    # kitchen
    R(65.7, 38.2, 2.1, 14, 0.1)
    R(65.7, 38.2, 2.1, 3, 0.1, "fu2")  # refrigerator
    R(65.5, 45.3, 2.3, 2.5, 0.1, "fu2")  # range, centered behind the island
    R(65.0, 44.6, 2.8, 3.9, 0, "oh")  # tapered plaster hood to the ceiling
    for cx, cy in ((66.3, 46.0), (67.1, 46.0), (66.3, 47.1), (67.1, 47.1)): C(cx, cy, 0.3, "fl")
    R(52.4, 56.6, 15.4, 2.0, 0.1); sink(60.1, 57.6)
    for dx in (56.4, 61.9):  # dishwashers either side of the sink
        R(dx, 56.7, 1.9, 1.8, 0.05, "fu2"); P(f"M{dx},56.7 L{dx + 1.9},58.5 M{dx + 1.9},56.7 L{dx},58.5", "fl")
    P("M55.5,51.9 L55.5,41.75 A2.95,2.95 0 0 1 61.4,41.75 L61.4,51.9 Z")
    R(55.5, 50.2, 5.9, 1.7, 0.05, "fu2"); P("M58.45,43 L58.45,50.2", "fl")
    for yy in (43.2, 46, 48.8): C(54.4, yy, 0.75)
    C(58.45, 37.9, 0.75); C(54.6, 41.2, 0.75)
    # nook
    C(59.5, 29.6, 2.4); [C(59.5 + 3.3 * math.cos(a), 29.6 + 3.3 * math.sin(a), 0.75) for a in [i * math.pi / 3 for i in range(6)]]
    R(66, 23, 1.9, 10.5, 0.1, "fu2"); P("M65.95,23.2 L65.95,33.3", "wine")  # glass-front wine wall in place of the buffet
    f.append('<text class="sk-d" x="67.1" y="28.2" transform="rotate(-90 67.1 28.2)" style="font-size:.6px">wine wall</text>')
    # outdoor kitchen
    R(54.3, 10.4, 2.0, 6.4, 0.1, "fu2"); R(56.3, 10.4, 2.1, 6.4, 0.1); R(58.4, 10.4, 9.2, 2.2, 0.1)
    R(59, 10.6, 2.8, 1.7, 0.1, "fu2"); R(65.6, 12.6, 2.0, 9.4, 0.1); R(66.0, 14.6, 1.3, 2.3, 0.1, "fu2")
    for yy in (11.8, 13.6, 15.4): C(53.5, yy, 0.7)
    # back porch
    sofa(30, 30.4, 10, 3, 'b'); R(32, 25.6, 6, 2.6, 0.4); chair(27.4, 24.8, 45, 2.8); chair(27.4, 30, 135, 2.8)
    chair(42.6, 24.8, -45, 2.8); chair(42.6, 30, -135, 2.8)
    # front porch
    chair(27.5, 66.3, -20, 2.6); chair(31.5, 66.3, 20, 2.6); C(29.5, 64.6, 0.7)
    chair(44.5, 66.3, -20, 2.6); chair(48.5, 66.3, 20, 2.6); C(46.5, 64.6, 0.7)
    # office: L-shaped couch along the back wall, its return butting into the computer desk, facing the TV
    sofa(72.6, 5.4, 11.0, 3.2, 't'); sofa(80.4, 8.6, 3.2, 7.4, 'r')
    # built-ins sit on the wall faces: exterior walls 0.375 ft in from the line, interior 0.2
    R(68.4, 5.4, 1.6, 18.9, 0.1, "fu2"); R(70, 9.6, 0.35, 4.4, 0.05, "tv")
    R(83.8, 7, 2, 6, 0.1, "fu2")
    R(77.2, 16, 8.6, 2.3, 0.1); R(77.2, 18.3, 2.2, 5.1, 0.1); C(81.6, 20.4, 0.8)
    # powder
    # shelves open to the corridor; toilet and vanity on the right wall
    R(72.2, 28.2, 1.2, 2.1, 0.1, "fu2"); toilet(77.5, 29.5, 90); R(77.4, 31.3, 1.4, 2.5, 0.1); sink(78.0, 32.55)
    # office desk nook: U-shaped desk on three walls, open to the office, shelving above along the hall wall
    P("M79.2,28.2 L81.2,28.2 L81.2,31.8 L83.8,31.8 L83.8,28.2 L85.8,28.2 L85.8,33.8 L79.2,33.8 Z")
    R(79.2, 32.6, 6.6, 1.2, 0, "oh")
    # stairs
    f.append(stairs("fl"))
    f.append(f'<path class="ar" d="{STAIR_ARROW}"/>')
    # pantry: no garage door; cabinets under the stairs, on the left wall below the kitchen opening, and along the front
    R(68.4, 60.3, 6.9, 1.8, 0.1); sink(72.3, 61.2); R(75.3, 60.1, 2.8, 2, 0.1, "fu2")
    # scullery: second dishwasher beside the sink; coffee station and appliance garage on the left-wall run
    R(73.3, 60.4, 1.85, 1.7, 0.05, "fu2"); P("M73.3,60.4 L75.15,62.1 M75.15,60.4 L73.3,62.1", "fl")
    R(68.2, 57.6, 1.8, 2.7, 0.1); R(68.4, 50.8, 9.7, 1.8, 0.1)
    # walk-in closet beside and under the stairs: shelving on the garage wall and the back wall, door from the hall
    R(77.1, 40.8, 1.2, 9.4, 0.1); R(72.1, 38.3, 3.2, 1.2, 0.1)
    f.append('<text class="sk-d" x="74.6" y="43.6" style="font-size:.6px">walk-in</text><text class="sk-d" x="74.6" y="44.4" style="font-size:.6px">closet</text>')
    f.append('<text class="sk-d" x="76.4" y="54.4" style="font-size:.6px">rated</text><text class="sk-d" x="76.4" y="55.1" style="font-size:.6px">pass door</text>')
    # primary bath and closet sit 2.5 ft further back than the sketch
    f.append('<g transform="translate(0 -2.5)">')
    toilet(87.5, 1.6, -90); R(86.2, 3.5, 1.8, 1.3, 0.1, "fu2")
    R(92.2, 0.4, 6.2, 3, 0.6, "wet"); R(92.6, 5.5, 3.6, 1.1, 0.3, "fu2")
    R(100.2, 0.4, 5.4, 4.2, 0.1, "wet"); R(90.8, 8.6, 8.8, 1.7, 0.1); sink(94, 9.4); sink(97.8, 9.4)
    R(100, 8.6, 2.6, 1.7, 0.1); sink(101.3, 9.4); R(104.1, 5.6, 1.5, 4.7, 0.1)
    # dressing room: 2 ft glass-front wardrobes both sides, full-length mirror on the office end wall, window seat under the end window
    R(90.6, 10.7, 13.6, 2.0, 0.1); R(90.6, 16.5, 13.6, 2.0, 0.1)
    P("M90.8,12.75 L104.0,12.75 M90.8,16.45 L104.0,16.45", "wine"); P("M86.5,13.1 L86.5,16.3", "mirror")
    R(104.3, 13.2, 1.3, 3.0, 0.3)
    f.append('</g>')
    f.append('<text class="sk-t sm" x="102.9" y="0.3">Shower</text>')
    # primary bedroom
    f.append('<g transform="translate(0 -2.4)">')
    bed(94.1, 18.9, 7.8, 7, 't'); R(91.9, 18.9, 1.9, 1.7); R(102.2, 18.9, 1.9, 1.7); R(94.7, 26.4, 6.5, 1.4, 0.4)
    f.append('</g>')
    R(94, 31.1, 8, 0.7, 0.1, "tv"); R(86.2, 21.5, 1.6, 6, 0.1); C(103.5, 30, 1.3, "pl")
    # side porch
    chair(109.2, 21.5, 90, 2.4); chair(109.2, 28.5, 90, 2.4)
    P("M106.4,32 L111.6,32", "oh")
    # laundry
    R(91.2, 37.9, 9.6, 1.9, 0.1); R(101, 37.6, 2.2, 2.1, 0.1, "fu2"); R(103.4, 37.6, 2.2, 2.1, 0.1, "fu2")
    R(91.4, 32.4, 1.6, 0.3, 0.1)
    # garage: ductless mini-split head on the back wall, Level 2 EV charger on the truck bay wall
    R(91.6, 40.3, 3.2, 0.6, 0.15, "fu2"); R(78.75, 59.6, 0.55, 1.4, 0.1, "fu2")
    f.append('<text class="sk-d" x="93.2" y="41.9" style="font-size:.6px">mini-split</text><text class="sk-d" x="80.6" y="60.6" style="font-size:.6px">EV</text>')
    # drop zone: bench with cubbies and hooks, left of the garage door
    R(78.7, 38.3, 7.6, 1.5, 0.1, "fu2")
    for xx in (80.6, 82.5, 84.4): P(f"M{xx},38.3 L{xx},39.8", "fl")
    f.append('<text class="sk-d" x="82.5" y="37.5" style="font-size:.7px">drop zone</text>')
    # garage: lockers, cars, shelving
    for xx in (104, 107, 110): R(xx, 40.6, 2.4, 2.4, 0.3)  # trash and recycling cans
    for cx in ():
        R(cx - 3.1, 47.5, 6.2, 15, 1.4, "car"); R(cx - 2.5, 52, 5, 3.2, 0.6, "fl")
    R(81.5, 43.6, 7.2, 20, 1.6, "car"); R(82.3, 51, 5.6, 3.4, 0.6, "fl")
    R(94.5, 47, 6.6, 16.5, 1.5, "car"); R(95.3, 52.5, 5, 3.2, 0.6, "fl")
    return "".join(f)


def landscape():
    g = []
    # pond behind the bedroom wing and porch
    g.append('<path class="water" d="M-6,1 C-2,-6 8,-7 14,-3 C20,1 22,7 29,6 C36,5 37,-2 43,-3 C49,-4 52,2 50,6 '
             'C48,10 41,10 36,11 C29,12 25,12 21,11 C15,9.5 12,8 6,9.5 C0,11 -7,8 -6,1 Z"/>')
    g.append('<path class="bed" d="M-8,-1 C-6,-9 6,-10 13,-6" fill="none"/>')
    # front courtyard garden
    g.append('<path class="water" d="M54,62 C55,60.3 59,60.4 61,61.4 C63.2,62.5 66.8,61.6 67.2,64 C67.6,66.6 64.6,67 64.4,69 '
             'C64.2,71 60.8,71.6 59.6,69.6 C58.6,68 55.6,69.4 54.6,67.6 C53.6,65.8 53,63.6 54,62 Z"/>')
    g.append('<path class="bedg" d="M68.4,63.2 L78.2,63.2 L78.2,66.2 C75,67.5 71,67.4 68.4,66 Z"/>')
    g.append('<path class="bedg" d="M107.9,56 L112.8,56 L112.8,62 C112.5,65 110.4,66.2 107.9,66.2 Z"/>')
    # walks and drive
    g.append('<rect class="walk" x="35" y="72" width="5" height="8"/>')
    g.append('<rect class="drive" x="79.5" y="66.5" width="28" height="13.5"/>')
    return "".join(g)


def labels(cls_name, cls_dim, sizes=True):
    t = []
    for name, x1, y1, x2, y2, fl, walls, (dx, dy), show in ROOMS:
        if not name:
            continue
        cx, cy = (x1 + x2) / 2 + dx, (y1 + y2) / 2 + dy
        small = (x2 - x1) < 9 or (y2 - y1) < 7
        t.append(f'<text class="{cls_name}{" sm" if small else ""}" x="{cx}" y="{cy}">{name}</text>')
        if show and sizes:
            dims = "18' × 23' + 7' × 6' desk nook" if name == "Office" else f"{short(x2 - x1)} × {short(y2 - y1)}"
            t.append(f'<text class="{cls_dim}" x="{cx}" y="{cy + 1.7}">{dims}</text>')
    for name, pts, (cx, cy) in PORCHES:
        parts = name.split("|")
        spans = "".join(f'<tspan x="{cx}" dy="{0 if i == 0 else 1.4}">{w}</tspan>' for i, w in enumerate(parts))
        t.append(f'<text class="{cls_name} por" x="{cx}" y="{cy}">{spans}</text>')
    return "".join(t)


def building(theme):
    """theme: 'sk' (sketch) or 'bp' (blueprint)"""
    s = []
    p = theme
    # porches
    for name, pts, _ in PORCHES:
        if pts:
            s.append(f'<polygon class="{p}-porch" points="{poly(pts)}"/>')
    for x, y in POSTS:
        s.append(f'<rect class="{p}-post" x="{x - 0.45}" y="{y - 0.45}" width="0.9" height="0.9"/>')
    # floors
    for name, x1, y1, x2, y2, fl, walls, _, _ in ROOMS:
        if name == "Garage":
            s.append(f'<polygon class="{p}-fl {p}-conc" points="{poly(GARAGE)}"/>')
            continue
        s.append(f'<rect class="{p}-fl {p}-{fl}" x="{x1}" y="{y1}" width="{x2 - x1}" height="{y2 - y1}"/>')
    if p == 'sk':
        s.append(furniture())
    else:
        s.append(stairs("bp-thin"))
        s.append(f'<path class="bp-thin" d="{STAIR_ARROW}"/>')
        s.append(f'<text class="bp-note" x="70" y="43.3">{STAIR_NOTE}</text>')
    # walls
    for name, x1, y1, x2, y2, fl, walls, _, _ in ROOMS:
        if walls:
            s.append(f'<rect class="{p}-iw" x="{x1}" y="{y1}" width="{x2 - x1}" height="{y2 - y1}"/>')
    for a, b in PARTS:
        s.append(f'<line class="{p}-iw" x1="{a[0]}" y1="{a[1]}" x2="{b[0]}" y2="{b[1]}"/>')
    s.append(f'<polygon class="{p}-ew" points="{poly(SHELL)}"/>')
    # openings
    gap = f"{p}-gap"
    for w in WINDOWS:
        s.append(window_svg(w, gap, f"{p}-win"))
    for o in OPENINGS:
        s.append(opening_svg(o, gap, f"{p}-thin"))
    for (x, y1), (_, y2) in SLIDERS:
        m = (y1 + y2) / 2
        s.append(f'<rect class="{gap}" x="{x - 0.45}" y="{y1}" width="0.9" height="{y2 - y1}"/>'
                 f'<line class="{p}-leaf" x1="{x - 0.17}" x2="{x - 0.17}" y1="{y1}" y2="{m + 0.4}"/>'
                 f'<line class="{p}-leaf" x1="{x + 0.17}" x2="{x + 0.17}" y1="{m - 0.4}" y2="{y2}"/>')
    for (x1, y), (x2, _), n, (px1, px2) in GLASSWALLS:
        s.append(f'<rect class="{gap}" x="{x1}" y="{y - 0.45}" width="{x2 - x1}" height="0.9"/>'
                 f'<rect class="gwp" x="{px1}" y="{y - 0.4}" width="{px2 - px1}" height="0.8"/>')
        w = (x2 - x1) / n
        for i in range(n):
            yy = y - 0.27 + 0.18 * i
            s.append(f'<line class="gw" x1="{x1 + i * w:.2f}" x2="{x1 + (i + 1) * w + 0.2:.2f}" y1="{yy:.2f}" y2="{yy:.2f}"/>')
    if p == 'bp':
        for a, b in SOUND:
            s.append(f'<line class="snd" x1="{a[0]}" y1="{a[1]}" x2="{b[0]}" y2="{b[1]}"/>')
    for d in DOORS:
        s.append(door_svg(d, gap, f"{p}-leaf", f"{p}-arc"))
    for (x1, y1), (x2, y2) in GARAGE_DOORS:
        if y1 == y2:
            s.append(f'<rect class="{gap}" x="{x1}" y="{y1 - 0.45}" width="{x2 - x1}" height="0.9"/>')
        else:
            s.append(f'<rect class="{gap}" x="{x1 - 0.45}" y="{y1}" width="0.9" height="{y2 - y1}"/>')
        s.append(f'<line class="{p}-gd" x1="{x1}" x2="{x2}" y1="{y1}" y2="{y2}"/>')
    for (x1, y1), (x2, y2) in PASSDOORS:  # rated pass door: a short solid leaf in the wall at counter height
        s.append(f'<rect class="{gap}" x="{x1 - 0.45}" y="{y1}" width="0.9" height="{y2 - y1}"/>'
                 f'<line class="{p}-leaf" x1="{x1}" x2="{x1}" y1="{y1}" y2="{y2}" style="stroke-width:.3"/>')
    for (x1, y1), (x2, y2) in BEAMS:
        s.append(f'<line class="{p}-beam" x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}"/>')
    if STOOP:
        x, y, w, h = STOOP
        s.append(f'<rect class="{p}-bi" x="{x}" y="{y}" width="{w}" height="{h}"/>')
    for x, y, w, h in BUILTINS:
        s.append(f'<rect class="{p}-bi" x="{x}" y="{y}" width="{w}" height="{h}"/>')
    if GENPAD:
        x, y, w, h = GENPAD
        s.append(f'<rect class="{p}-bi" x="{x}" y="{y}" width="{w}" height="{h}"/><rect class="{p}-bi" x="{x + .6}" y="{y + .6}" width="{w - 1.2}" height="{h - 1.2}" rx=".2"/>'
                 f'<text class="{p}-d" x="{x + w / 2}" y="{y + h / 2 + .3}" style="font-size:.75px">GEN</text>')
    for x, y, d, w in FIREPLACES:  # hearth on an interior face of a left-hand wall, firebox open to the room
        s.append(f'<rect class="{p}-bi" x="{x + 0.375}" y="{y}" width="{d}" height="{w}"/>'
                 f'<rect class="{p}-bi" x="{x + 0.375 + d * 0.45}" y="{y + 1}" width="{d * 0.55}" height="{w - 2}"/>'
                 )
    for x, y, w, h in CARS:
        s.append(f'<rect class="bp-car" x="{x}" y="{y}" width="{w}" height="{h}" rx="1.3"/>')
    return "".join(s)


def dim_chain(xs, y, horizontal=True, off=0):
    """Chain of dimensions along y (horizontal) or x (vertical)."""
    s = []
    if horizontal:
        s.append(f'<line class="bp-dl" x1="{xs[0]}" x2="{xs[-1]}" y1="{y}" y2="{y}"/>')
        for x in xs:
            s.append(f'<line class="bp-dt" x1="{x - 0.6}" x2="{x + 0.6}" y1="{y + 0.6}" y2="{y - 0.6}"/>')
            s.append(f'<line class="bp-dl" x1="{x}" x2="{x}" y1="{y - 1}" y2="{y + 1}"/>')
        for a, b in zip(xs, xs[1:]):
            s.append(f'<text class="bp-dim" x="{(a + b) / 2}" y="{y - 0.7}">{fmt(b - a)}</text>')
    else:
        x = y
        s.append(f'<line class="bp-dl" y1="{xs[0]}" y2="{xs[-1]}" x1="{x}" x2="{x}"/>')
        for v in xs:
            s.append(f'<line class="bp-dt" y1="{v + 0.6}" y2="{v - 0.6}" x1="{x - 0.6}" x2="{x + 0.6}"/>')
            s.append(f'<line class="bp-dl" y1="{v}" y2="{v}" x1="{x - 1}" x2="{x + 1}"/>')
        for a, b in zip(xs, xs[1:]):
            s.append(f'<text class="bp-dim" transform="translate({x - 0.7} {(a + b) / 2}) rotate(-90)">{fmt(b - a)}</text>')
    return "".join(s)


def sketch_svg():
    return f'''<svg class="plan sk" viewBox="-12 -12 134 98" role="img" aria-label="Rendered floor plan sketch of a single-level home about 113 by 72 feet, with the bedroom wing on the left, great room in the middle, primary suite and garage on the right.">
<rect class="sk-site" x="-12" y="-12" width="134" height="98"/>
{landscape()}
{building('sk')}
{labels('sk-t', 'sk-d')}
<g class="sk-cap"><text x="-10" y="83">BACK: future pond ↑</text><text x="96" y="83">↓ FRONT: street / drive</text></g>
</svg>'''


def blueprint_svg():
    grid = "".join(f'<line class="bp-grid" x1="{x}" x2="{x}" y1="-14" y2="92"/>' for x in range(-16, 132, 2))
    grid += "".join(f'<line class="bp-grid" y1="{y}" y2="{y}" x1="-16" x2="132"/>' for y in range(-14, 92, 2))
    top = dim_chain([0, 24, 46, 68, 86, 106, 113], -6)
    top2 = dim_chain([0, 113], -10)
    bot = dim_chain([0, 7, 24, 52, 68, 78.5, 107.5, 113], 78)
    left = dim_chain([13, 26.8, 34.4, 54, 72], -6, False)
    left2 = dim_chain([-2.5, 72], -10, False)
    right = dim_chain([-2.5, 8, 16, 32, 40, 55.5, 66.5], 119, False)
    scale = ('<g class="bp-scale"><rect x="96" y="83" width="5" height="0.8"/><rect class="o" x="101" y="83" width="5" height="0.8"/>'
             '<rect x="106" y="83" width="10" height="0.8"/><text x="96" y="86.4">0</text><text x="101" y="86.4">5</text>'
             '<text x="106" y="86.4">10</text><text x="116" y="86.4">20 ft</text></g>')
    return f'''<svg class="plan bp" viewBox="-16 -14 148 106" role="img" aria-label="To-scale blueprint floor plan with dimension strings: overall 113 feet wide by 72 feet deep.">
<rect class="bp-bg" x="-16" y="-14" width="148" height="106"/>
{grid}
{building('bp')}
{labels('bp-t', 'bp-d')}
{top}{top2}{bot}{left}{left2}{right}
{scale}
<g class="bp-title"><text x="-14" y="86.4">FIRST FLOOR PLAN · DRAFT L · SCALE 1 SQ = 2 FT</text></g>
<g class="bp-north"><path d="M124,-11 L124,-4 M122.6,-6 L124,-4 L125.4,-6"/><text x="124" y="-12">FRONT</text></g>
</svg>'''


# ---------------------------------------------------------------- roof plan
def roof_svg():
    from roofkit import visible, edges, zp
    vis = visible(ROOFS)
    E = edges(ROOFS, vis)
    o = []
    grid = "".join(f'<line class="bp-grid" x1="{x}" x2="{x}" y1="-14" y2="92"/>' for x in range(-16, 132, 2))
    grid += "".join(f'<line class="bp-grid" y1="{y}" y2="{y}" x1="-16" x2="132"/>' for y in range(-14, 92, 2))
    o.append(f'<rect class="bp-bg" x="-16" y="-14" width="148" height="106"/>{grid}')
    o.append(f'<polygon class="rf-shell" points="{poly(SHELL)}"/>')
    for r, k, pl, g in vis:
        gx, gy = pl[0], pl[1]
        if abs(gx) + abs(gy) < 1e-9: tone = .5
        else:
            ang = math.atan2(-gy, -gx)
            tone = .5 + .5 * math.cos(ang - math.radians(225))
        cls = 'rf-m' if r.mat == 'seam' else 'rf-s'
        o.append(f'<polygon class="{cls}" style="fill-opacity:{.2 + .4 * tone:.2f}" points="{poly(list(g.exterior.coords)[:-1])}"/>')
    W = dict(eave=.16, rake=.16, ridge=.26, hip=.22, valley=.22, seam=0, top=.16, **{'break': .14})
    for e in E:
        if e['t'] == 'seam': continue
        o.append(f'<line class="rf-{e["t"]}" style="stroke-width:{W[e["t"]]}" x1="{e["a"][0]:.2f}" y1="{e["a"][1]:.2f}" x2="{e["b"][0]:.2f}" y2="{e["b"][1]:.2f}"/>')
    # downslope arrows with the pitch, one per facet big enough to hold one
    for r, k, pl, g in vis:
        gx, gy = pl[0], pl[1]
        m = math.hypot(gx, gy)
        if m < 1e-9 or g.area < 14 or r.name == 'Dormer': continue
        c = g.representative_point()
        L = 2.2
        dx, dy = -gx / m * L, -gy / m * L
        pitch = round(m * 12 * 2) / 2
        lab = f"{pitch:g}:12"
        o.append(f'<path class="rf-ar" d="M{c.x - dx / 2:.2f},{c.y - dy / 2:.2f} L{c.x + dx / 2:.2f},{c.y + dy / 2:.2f}"/>'
                 f'<path class="rf-ah" d="M{c.x + dx / 2:.2f},{c.y + dy / 2:.2f} l{-dx * .3 - dy * .2:.2f},{-dy * .3 + dx * .2:.2f} l{dy * .4:.2f},{-dx * .4:.2f} Z"/>'
                 f'<text class="rf-p" x="{c.x + (dy / L) * 1.2:.2f}" y="{c.y - (dx / L) * 1.2 + .35:.2f}">{lab}</text>')
    # ridge heights
    for r in ROOFS:
        if r.kind != 'ridge' or r.name in ('Primary bath', 'Dormer'): continue
        best = None
        for e in E:
            if e['t'] != 'ridge' or vis[e['i']][0] is not r: continue
            L = math.hypot(e['b'][0] - e['a'][0], e['b'][1] - e['a'][1])
            if best is None or L > best[0]: best = (L, e)
        if not best: continue
        e = best[1]
        mx, my = (e['a'][0] + e['b'][0]) / 2, (e['a'][1] + e['b'][1]) / 2
        horiz = abs(e['b'][0] - e['a'][0]) > abs(e['b'][1] - e['a'][1])
        t = f"{r.name} · ridge {fmt(e['a'][2])}"
        if horiz: o.append(f'<text class="rf-t" x="{mx:.2f}" y="{my - .7:.2f}">{t}</text>')
        else: o.append(f'<text class="rf-t" transform="translate({mx - .7:.2f} {my:.2f}) rotate(-90)">{t}</text>')
    dm = [r for r in ROOFS if r.name == 'Dormer']
    if dm: o.append(f'<text class="rf-t" x="{(dm[0].r[0] + dm[-1].r[2]) / 2:.2f}" y="70.6">Two wall dormers · ridge {fmt(dm[0].ridge)}</text>')
    leg = [("ridge", "Ridge"), ("hip", "Hip"), ("valley", "Valley"), ("break", "Pitch change"), ("eave", "Eave"), ("rake", "Gable edge (rake)")]
    lx = -13
    for k, t in leg:
        o.append(f'<line class="rf-{k}" style="stroke-width:{W[k]}" x1="{lx}" y1="86" x2="{lx + 2.4}" y2="86"/><text class="rf-l" x="{lx + 3}" y="86.35">{t}</text>')
        lx += 4.6 + len(t) * .52
    o.append('<g class="bp-title"><text x="-14" y="89.6">ROOF PLAN · DRAFT L · SHINGLES ARE THE WARM AREAS, STANDING-SEAM METAL THE COOL ONES · HEIGHTS ABOVE THE MAIN FLOOR</text></g>')
    o.append('<g class="bp-north"><path d="M124,-11 L124,-4 M122.6,-6 L124,-4 L125.4,-6"/><text x="124" y="-12">FRONT</text></g>')
    return ('<svg class="plan bp" viewBox="-16 -14 148 106" role="img" aria-label="Roof plan for draft L: ridges, hips, valleys and slope arrows over the house outline.">'
            + "".join(o) + '</svg>')


# ---------------------------------------------------------------- low voltage
LV_CAMS = [(36, 63.1, 90, "door"), (24.4, 72.2, 115), (51.6, 72.2, 65), (78.8, 66.8, 100), (107.2, 66.8, 80), (113.3, 56.2, 10), (113.2, 46.6, -40),
           (111.8, 16.2, -60), (106.2, -2.3, -40), (68.3, 4.8, -110), (46.4, 10.2, -90), (24.3, 20.2, -100), (0.3, 13.3, -135), (0.2, 54, 180),
           (7.2, 71.8, 135), (79.6, 41, 40)]
LV_WAPS = [(40, 46), (60, 28), (17.5, 32.6), (96, 24), (77, 15.4), (93, 54), (35, 27), (109, 28), (14, 63)]
LV_DATA = [(68.7, 14.8), (82.5, 33.3), (24.6, 47.2), (23.4, 19), (15.2, 41.5), (98, 31.4), (0.6, 22), (102, 40.6), (85.6, 33.3)]
LV_SPK = [(32, 42), (44, 42), (32, 53), (44, 53), (30, 27.5), (41, 27.5), (55, 15), (64, 15), (12, 60), (20, 67)]
LV_CND = [(60, 10.4, "outdoor kitchen"), (38, 20.4, "to the pond"), (111.6, 26, "side porch"), (93, 66.4, "gate + drive")]
SRV = (22.6, 43.1)


def lv_svg():
    old = swapped(furniture=lambda: "")
    base = building("sk")
    swapped(**old)
    sx, sy = SRV
    s = []
    for x, y, *_ in LV_CAMS + [(x, y) for x, y in LV_WAPS]:
        s.append(f'<path class="lv-run" d="M{sx},{sy} L{x},{y}"/>')
    for c in LV_CAMS:
        x, y, a = c[0], c[1], c[2]
        r, h = 6.5, 32
        a1, a2 = math.radians(a - h), math.radians(a + h)
        if len(c) > 3:
            s.append(f'<rect class="lv-cam" x="{x - .55}" y="{y - .55}" width="1.1" height="1.1" transform="rotate(45 {x} {y})"/>')
        else:
            s.append(f'<path class="lv-fov" d="M{x},{y} L{x + r * math.cos(a1):.2f},{y + r * math.sin(a1):.2f} A{r},{r} 0 0 1 {x + r * math.cos(a2):.2f},{y + r * math.sin(a2):.2f} Z"/>'
                     f'<circle class="lv-cam" cx="{x}" cy="{y}" r=".6"/>')
    for x, y in LV_WAPS:
        s.append(f'<circle class="lv-wap" cx="{x}" cy="{y}" r=".85"/><path class="lv-arc" d="M{x - 1.3},{y - .9} A1.6,1.6 0 0 1 {x + 1.3},{y - .9} M{x - 1.9},{y - 1.4} A2.4,2.4 0 0 1 {x + 1.9},{y - 1.4}"/>')
    for x, y in LV_DATA:
        s.append(f'<path class="lv-data" d="M{x},{y - .7} L{x + .65},{y + .5} L{x - .65},{y + .5} Z"/>')
    for x, y in LV_SPK:
        s.append(f'<circle class="lv-spk" cx="{x}" cy="{y}" r=".7"/><circle class="lv-spk2" cx="{x}" cy="{y}" r=".25"/>')
    for x, y, t in LV_CND:
        s.append(f'<rect class="lv-cnd" x="{x - .6}" y="{y - .6}" width="1.2" height="1.2"/><text class="lv-t" x="{x}" y="{y + (1.9 if y > 30 or t.startswith("gate") else -1.1)}">{t}</text>')
    s.append(f'<rect class="lv-srv" x="{sx - 1.6}" y="{sy - 2.6}" width="3.2" height="5.2" rx=".2"/><text class="lv-t w" x="{sx}" y="{sy + .25}">RACK</text>')
    s.append('<rect class="lv-cnd" x="17.9" y="45.2" width="2.6" height=".6"/><text class="lv-t" x="20.7" y="48.6">mini-split</text>')
    leg = [("cam", "Camera, PoE"), ("door", "Video doorbell"), ("wap", "Wi-Fi access point"), ("data", "Data drop, Cat6"), ("spk", "Ceiling speaker"), ("cnd", "Conduit stub"), ("run", "Home run to the rack")]
    lx = -10
    for k, t in leg:
        y = -7
        if k == "cam": sym = f'<circle class="lv-cam" cx="{lx}" cy="{y}" r=".6"/>'
        elif k == "door": sym = f'<rect class="lv-cam" x="{lx - .55}" y="{y - .55}" width="1.1" height="1.1" transform="rotate(45 {lx} {y})"/>'
        elif k == "wap": sym = f'<circle class="lv-wap" cx="{lx}" cy="{y}" r=".85"/>'
        elif k == "data": sym = f'<path class="lv-data" d="M{lx},{y - .7} L{lx + .65},{y + .5} L{lx - .65},{y + .5} Z"/>'
        elif k == "spk": sym = f'<circle class="lv-spk" cx="{lx}" cy="{y}" r=".7"/>'
        elif k == "cnd": sym = f'<rect class="lv-cnd" x="{lx - .6}" y="{y - .6}" width="1.2" height="1.2"/>'
        else: sym = f'<path class="lv-run" style="opacity:1" d="M{lx - 1},{y} L{lx + 1},{y}"/>'
        s.append(sym + f'<text class="lv-t" x="{lx + 1.4}" y="{y + .35}" style="text-anchor:start;font-size:1px">{t}</text>')
        lx += 4.2 + len(t) * .5
    return (f'<svg class="plan sk lv" viewBox="-12 -12 134 98" role="img" aria-label="Low-voltage plan: cameras, Wi-Fi access points, data drops, ceiling speakers and conduit, all home-run to the rack in the server room.">'
            f'<rect class="sk-site" x="-12" y="-12" width="134" height="98"/><g opacity=".5">{base}{labels("sk-t", "sk-d", sizes=False)}</g>{"".join(s)}</svg>')


# ---------------------------------------------------------------- variants
def swapped(**kw):
    g = globals()
    old = {k: g[k] for k in kw}
    g.update(kw)
    return old


def bp_grid(x0, y0, w, h):
    gx = "".join(f'<line class="bp-grid" x1="{x}" x2="{x}" y1="{y0}" y2="{y0 + h}"/>' for x in range(int(x0), int(x0 + w) + 1, 2))
    gy = "".join(f'<line class="bp-grid" y1="{y}" y2="{y}" x1="{x0}" x2="{x0 + w}"/>' for y in range(int(y0), int(y0 + h) + 1, 2))
    return f'<rect class="bp-bg" x="{x0}" y="{y0}" width="{w}" height="{h}"/>' + gx + gy


SHELL_SIDE = SHELL[:SHELL.index((113, 46.4)) + 1] + [(113, 66.5)] + SHELL[SHELL.index((78.5, 66.5)):]
SIDE_DOOR = (113, 47, 3, 'v', -1, True)
GARAGE_VARIANTS = [
    dict(key="A", name="As sketched, one wide door", note="One door about 20'-9\" wide, as drawn in the sketch. No post between the truck and the SUV.",
         GARAGE_DOORS=[((80.4, 66.5), (101.2, 66.5)), ((113, 46.4), (113, 51.6))],
         CARS=[(82, 43.6, 7.2, 20), (93.5, 47, 6.6, 16.5)],
         drive='<rect class="bp-drive" x="78.5" y="66.5" width="29" height="17.5"/>'),
    dict(key="B", name="Front-load, two singles", note="Two 10' doors, one for the truck and one for the SUV.",
         GARAGE_DOORS=[((80.5, 66.5), (90.5, 66.5)), ((93, 66.5), (103, 66.5)), ((113, 46.4), (113, 51.6))],
         CARS=[(81.5, 43.6, 7.2, 20), (94.5, 47, 6.6, 16.5)],
         drive='<rect class="bp-drive" x="78.5" y="66.5" width="29" height="17.5"/>'),
    dict(key="C", name="Side-load", note="One 18' door turns to the right side, so the street sees a wall with windows.",
         SHELL=SHELL_SIDE, GARAGE=[(78.5, 40), (102.4, 40), (102.4, 46.4), (113, 46.4), (113, 66.5), (78.5, 66.5)],
         GARAGE_DOORS=[((113, 47.5), (113, 65.5)), ((95, 66.5), (101, 66.5))],
         BUILTINS=[],
         CARS=[(90, 48, 20, 7.2), (93.5, 57.6, 16.5, 6.6)],
         
         WINDOWS=[w for w in WINDOWS if w != ((113, 42), (113, 45))] + [((83, 66.5), (88, 66.5)), ((91, 66.5), (96, 66.5))],
         drive='<path class="bp-drive" d="M113,40 L137,40 L137,84 L126,84 L126,66.5 L113,66.5 Z"/>'
               '', top='<text class="bp-note" x="87" y="51">WORKSHOP</text>'),
]


def garage_svg(v):
    keys = {k: v[k] for k in v if k.isupper()}
    old = swapped(**keys)
    vb = (75, 37, 62, 46)
    out = (f'<svg class="plan bp mini" viewBox="{vb[0]} {vb[1]} {vb[2]} {vb[3]}" role="img" aria-label="Garage option {v["key"]}: {v["name"]}">'
           f'{bp_grid(*vb)}{v["drive"]}{building("bp")}{labels("bp-t", "bp-d")}{v.get("top", "")}'
           f'<text class="bp-t" x="{vb[0] + 2.5}" y="{vb[1] + vb[3] - 2}" style="text-anchor:start">OPTION {v["key"]}</text></svg>')
    swapped(**old)
    return out


UPPER_SHELL = [(68, 38), (78.5, 38), (78.5, 40), (107.5, 40), (107.5, 66.5), (78.5, 66.5), (78.5, 50.6), (68, 50.6)]
# the stair arrives through the garage's left wall, under the ridge of the great room roof
UP_ENTRY = ((78.5, 46.73), (78.5, 50.23))
# windows that can exist upstairs: the two front dormers, the right gable end, and the left gable end above the great room roof
UP_WINDOWS = [((84.3, 66.5), (88.7, 66.5)), ((97.3, 66.5), (101.7, 66.5)), ((107.5, 48.5), (107.5, 51.5)), ((107.5, 54.5), (107.5, 57.5)), ((78.5, 59), (78.5, 62))]
UPPER = [
    dict(key="1", name="One bonus room", note="One big room with sloped ceilings, about 29' × 18½', with 7 ft or more of headroom across the middle 17 ft. A bath and a closet sit in the front strip under the left dormer, a window seat in the right dormer, and attic storage in the right front corner.",
         ROOMS=[("Stairs", 68, 38, 78.5, 50.6, "wood", True, (0, 3.2), False),
                ("Bonus room", 78.5, 40, 107.5, 58.5, "wood", True, (0, 0), True),
                ("Bath", 78.5, 58.5, 90, 66.5, "tile", True, (0, 0.6), True),
                ("Closet", 90, 58.5, 95.5, 66.5, "wood", True, (0, 0), False),
                ("Nook", 95.5, 58.5, 103.5, 66.5, "wood", True, (0, 0), False),
                ("Attic", 103.5, 58.5, 107.5, 66.5, "wood", True, (0, 0), False)],
         PARTS=[], DOORS=[(82, 58.5, 2.67, 'h', 1, True), (91.5, 58.5, 2.5, 'h', 1, True), (104.5, 58.5, 2.2, 'h', 1, True)],
         OPENINGS=[UP_ENTRY], WINDOWS=UP_WINDOWS),
    dict(key="2", name="Two rooms", note="Two bedrooms and a shared bath. The stair lands in a hall along the middle of the floor, where the headroom is full. The bath sits off the hall in the full-height middle too, so the shower has its full 6'-8\" and more; the low strip along the back eave is storage. Room 1 gets the left dormer and the left gable window, with a closet beside the bath; room 2 gets the right dormer and the right gable windows, so both have an escape window.",
         ROOMS=[("Stairs", 68, 38, 78.5, 50.6, "wood", True, (0, 3.2), False),
                ("Hall", 78.5, 46.5, 95, 50.5, "wood", False, (2, 0.4), False),
                ("Closet", 78.5, 40, 84, 46.5, "wood", True, (0, 0), False),
                ("Storage", 84, 40, 95, 46.5, "wood", True, (0, 0), False),
                ("Room 1", 78.5, 50.5, 90, 66.5, "wood", True, (0, -1.5), True),
                ("Bath", 90, 50.5, 95, 58, "tile", True, (0, 1.2), True),
                ("Closet", 90, 58, 95, 66.5, "wood", True, (0, -.5), False),
                ("Room 2", 95, 40, 107.5, 66.5, "wood", True, (0, -1.5), True)],
         PARTS=[((95, 50.5), (95, 46.5))],
         DOORS=[(81, 46.5, 2.5, 'h', 1, True), (88, 46.5, 2.5, 'h', 1, True), (84, 50.5, 3, 'h', 1, False), (91.2, 50.5, 2.5, 'h', 1, True),
                (90, 60, 2.5, 'v', 1, True), (95, 47.2, 3, 'v', 1, True)],
         OPENINGS=[UP_ENTRY], WINDOWS=UP_WINDOWS),
]


def upper_svg(u):
    keys = {k: u[k] for k in u if k.isupper()}
    old = swapped(SHELL=UPPER_SHELL, PORCHES=[], POSTS=[], GARAGE_DOORS=[], CARS=[], BUILTINS=[], STAIR_NOTE="DN", PASSDOORS=[], BEAMS=[], STOOP=None, GENPAD=None, FIREPLACES=[], GLASSWALLS=[], SLIDERS=[], SOUND=[], **keys)
    vb = (62, 30, 56, 42)
    ghost = f'<polygon class="bp-ghost" points="{poly(old["SHELL"] if "SHELL" in old else SHELL_FIRST)}"/>'
    out = (f'<svg class="plan bp mini" viewBox="{vb[0]} {vb[1]} {vb[2]} {vb[3]}" role="img" aria-label="Upstairs option {u["key"]}: {u["name"]}">'
           f'{bp_grid(*vb)}{ghost}{building("bp")}{labels("bp-t", "bp-d")}'
           f'{dim_chain([78.5, 107.5], 35.5)}{dim_chain([40, 66.5], 111.5, False)}'
           f'<text class="bp-t" x="{vb[0] + 2}" y="{vb[1] + vb[3] - 2}" style="text-anchor:start">UPSTAIRS {u["key"]}</text></svg>')
    swapped(**old)
    return out


SHELL_FIRST = SHELL


CSS = r'''
/* additions */
:root{--pl-paper:#FBF8F1;--pl-site:#E4EAD6;--pl-wood:#EBDDC2;--pl-tile:#DCE3E5;--pl-conc:#DEDBD4;--pl-deck:#D7BF98;--pl-wall:#2A2E35;--pl-fu:#FFFFFF;--pl-fu2:#EFE8DA;--pl-line:#6E6556;--pl-rug:#E2CFAE;--pl-wet:#BFD6E0;--pl-water:#A9CCDB;--pl-bed:#A9C08A;--pl-bed2:#7E9A5F;--pl-walk:#D9D3C6;--pl-text:#23272E;--pl-tv:#3A3F48;--bp-bg:#143563;--bp-grid:#1D4374;--bp-line:#EAF2FB;--bp-dim:#A9CBEF;--bp-fill:#173B6D}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){--pl-paper:#FBF8F1;--pl-site:#E4EAD6;--pl-wood:#EBDDC2;--pl-tile:#DCE3E5;--pl-conc:#DEDBD4;--pl-deck:#D7BF98;--pl-wall:#2A2E35;--pl-fu:#FFFFFF;--pl-fu2:#EFE8DA;--pl-line:#6E6556;--pl-rug:#E2CFAE;--pl-wet:#BFD6E0;--pl-water:#A9CCDB;--pl-bed:#A9C08A;--pl-bed2:#7E9A5F;--pl-walk:#D9D3C6;--pl-text:#23272E;--pl-tv:#3A3F48;--bp-bg:#143563;--bp-grid:#1D4374;--bp-line:#EAF2FB;--bp-dim:#A9CBEF;--bp-fill:#173B6D}}
:root[data-theme="dark"]{--pl-paper:#FBF8F1;--pl-site:#E4EAD6;--pl-wood:#EBDDC2;--pl-tile:#DCE3E5;--pl-conc:#DEDBD4;--pl-deck:#D7BF98;--pl-wall:#2A2E35;--pl-fu:#FFFFFF;--pl-fu2:#EFE8DA;--pl-line:#6E6556;--pl-rug:#E2CFAE;--pl-wet:#BFD6E0;--pl-water:#A9CCDB;--pl-bed:#A9C08A;--pl-bed2:#7E9A5F;--pl-walk:#D9D3C6;--pl-text:#23272E;--pl-tv:#3A3F48;--bp-bg:#143563;--bp-grid:#1D4374;--bp-line:#EAF2FB;--bp-dim:#A9CBEF;--bp-fill:#173B6D}
.d-fig.wide{width:min(1180px,calc(100vw - 32px));position:relative;left:50%;transform:translateX(-50%)}
.d-fig.wide figcaption{max-width:800px;margin-inline:auto}
.plan{display:block;width:100%;height:auto;border-radius:12px;border:1px solid var(--rule)}
.plan text{text-anchor:middle;font-family:var(--f-body)}
.sk-site{fill:var(--pl-site)}
.sk-fl{stroke:none}.sk-wood{fill:var(--pl-wood)}.sk-tile{fill:var(--pl-tile)}.sk-conc{fill:var(--pl-conc)}
.sk-porch{fill:var(--pl-deck);stroke:var(--pl-line);stroke-width:.15;stroke-dasharray:.6 .4}
.sk-post{fill:var(--pl-wall)}
.sk-iw{fill:none;stroke:var(--pl-wall);stroke-width:.4}
.sk-ew{fill:none;stroke:var(--pl-wall);stroke-width:.75;stroke-linejoin:miter}
.sk-gap{fill:var(--pl-wood)}
.sk-win{stroke:var(--pl-wall);stroke-width:.09}
.sk-leaf{stroke:var(--pl-wall);stroke-width:.14}
.sk-arc{fill:none;stroke:var(--pl-line);stroke-width:.08;stroke-dasharray:.3 .2}
.sk-thin{stroke:var(--pl-wall);stroke-width:.12}
.sk-gd{stroke:var(--pl-wall);stroke-width:.15;stroke-dasharray:.6 .3}
.fu{fill:var(--pl-fu);stroke:var(--pl-line);stroke-width:.1}
.fu2{fill:var(--pl-fu2);stroke:var(--pl-line);stroke-width:.08}
.fl{fill:none;stroke:var(--pl-line);stroke-width:.08}
.ar{fill:none;stroke:var(--pl-wall);stroke-width:.14}
.tv{fill:var(--pl-tv)}
.rug{fill:var(--pl-rug);opacity:.55;stroke:none}
.wet{fill:var(--pl-wet);stroke:var(--pl-line);stroke-width:.1}
.oh{fill:none;stroke:var(--pl-line);stroke-width:.08;stroke-dasharray:.35 .2}
.car{fill:none;stroke:var(--pl-line);stroke-width:.1;stroke-dasharray:.4 .25}
.pl{fill:var(--pl-bed);stroke:var(--pl-bed2);stroke-width:.12}.pl2{fill:var(--pl-bed2)}
.water{fill:var(--pl-water);stroke:var(--pl-line);stroke-width:.1}
.bed{stroke:var(--pl-bed2);stroke-width:.12}
.bedg{fill:var(--pl-bed);stroke:var(--pl-bed2);stroke-width:.12}
.walk{fill:var(--pl-walk)}.drive{fill:var(--pl-walk)}
.plan text.sk-t{font-size:1.25px;font-weight:600;fill:var(--pl-text);letter-spacing:.02px}
.plan text.sk-t.sm{font-size:.85px}.plan text.sk-t.por{font-style:italic;font-weight:400}
.plan text.sk-d{font-size:.95px;fill:var(--pl-line)}
.plan .sk-cap text{font-size:1.1px;fill:var(--pl-line);letter-spacing:.08px;text-anchor:start}
.bp-bg{fill:var(--bp-bg)}.bp-grid{stroke:var(--bp-grid);stroke-width:.06}
.bp-fl{fill:var(--bp-fill)}
.bp-porch{fill:none;stroke:var(--bp-dim);stroke-width:.12;stroke-dasharray:.7 .4}
.bp-post{fill:var(--bp-line)}
.bp-iw{fill:none;stroke:var(--bp-line);stroke-width:.38}
.bp-ew{fill:none;stroke:var(--bp-line);stroke-width:.6}
.bp-gap{fill:var(--bp-fill)}
.bp-win{stroke:var(--bp-line);stroke-width:.07}
.bp-leaf{stroke:var(--bp-line);stroke-width:.12}
.bp-arc{fill:none;stroke:var(--bp-dim);stroke-width:.07}
.bp-thin{fill:none;stroke:var(--bp-dim);stroke-width:.07}
.bp-gd{stroke:var(--bp-line);stroke-width:.12;stroke-dasharray:.6 .3}
.plan text.bp-t{font-size:1.15px;font-weight:600;fill:var(--bp-line);letter-spacing:.06px;text-transform:uppercase}
.plan text.bp-t.sm{font-size:.8px}.plan text.bp-t.por{fill:var(--bp-dim);font-weight:400}
.plan text.bp-d{font-size:.95px;fill:var(--bp-dim)}
.plan text.bp-note{font-size:.8px;fill:var(--bp-dim)}
.bp-dl{stroke:var(--bp-dim);stroke-width:.06}.bp-dt{stroke:var(--bp-line);stroke-width:.12}
.plan text.bp-dim{font-size:.95px;fill:var(--bp-line)}
.bp-scale rect{fill:var(--bp-line)}.bp-scale rect.o{fill:none;stroke:var(--bp-line);stroke-width:.1}
.plan .bp-scale text,.plan .bp-title text{font-size:.95px;fill:var(--bp-line);text-anchor:start;letter-spacing:.06px}
.bp-north path{fill:none;stroke:var(--bp-line);stroke-width:.15}.plan .bp-north text{font-size:.9px;fill:var(--bp-line)}
.lv-cam{fill:#C2412D}.lv-fov{fill:#C2412D;opacity:.14}.lv-wap{fill:#fff;stroke:#1F6FB2;stroke-width:.2}.lv-arc{fill:none;stroke:#1F6FB2;stroke-width:.14}
.lv-data{fill:#1F6FB2}.lv-spk{fill:#fff;stroke:#7A4FB0;stroke-width:.18}.lv-spk2{fill:#7A4FB0}.lv-cnd{fill:#fff;stroke:#2E8B57;stroke-width:.2}
.lv-run{fill:none;stroke:#1F6FB2;stroke-width:.07;stroke-dasharray:.4 .3;opacity:.4}.lv-srv{fill:#1F2328}
.plan text.lv-t{font-size:.75px;fill:#23272E;font-weight:600;paint-order:stroke;stroke:#FBF8F1;stroke-width:.25px}.plan text.lv-t.w{fill:#fff;stroke:none;font-size:.6px}
.plan .gw{stroke:#2F7FA3;stroke-width:.2}.plan .gwp{fill:none;stroke:#2F7FA3;stroke-width:.1;stroke-dasharray:.35 .25}
.plan .snd{stroke:#6E5A9A;stroke-width:.45;stroke-dasharray:.6 .4;opacity:.85}
.plan .wine{fill:none;stroke:#2F7FA3;stroke-width:.14}.plan .mirror{fill:none;stroke:#2F7FA3;stroke-width:.3}
.plan .bk{fill:#3F6B4E;stroke:var(--pl-line,#3a3530);stroke-width:.08}
.d-q{margin:0;padding-left:1.3em}.d-q li{margin:.5em 0}
.d-fig svg.plan{overflow:hidden}
.mini .bp-gd{stroke:var(--bp-dim);stroke-width:.35;stroke-dasharray:1 .5}
.bp-bi{fill:none;stroke:var(--bp-dim);stroke-width:.1}.sk-bi{fill:var(--pl-fu);stroke:var(--pl-line);stroke-width:.1}
.sk-beam{stroke:var(--pl-wall);stroke-width:.18;stroke-dasharray:1 .35 .25 .35}.bp-beam{stroke:var(--bp-line);stroke-width:.16;stroke-dasharray:1 .35 .25 .35}
.plan .ovh{stroke-dasharray:.35 .25}
.rf-shell{fill:none;stroke:var(--bp-dim);stroke-width:.12;stroke-dasharray:.5 .35}
.rf-s{fill:#D9A55E;stroke:none}.rf-m{fill:#8EC3EE;stroke:none}
.rf-ridge,.rf-hip{stroke:var(--bp-line)}.rf-valley{stroke:#F2B26B;stroke-dasharray:.7 .3}.rf-break{stroke:var(--bp-dim);stroke-dasharray:.2 .25}
.rf-eave,.rf-rake,.rf-top{stroke:var(--bp-line);opacity:.85}
.rf-ar{stroke:var(--bp-line);stroke-width:.1;fill:none}.rf-ah{fill:var(--bp-line)}
.plan text.rf-p{font-size:.7px;fill:var(--bp-dim);text-anchor:middle}
.plan text.rf-t{font-size:.85px;fill:var(--bp-line);font-weight:600;letter-spacing:.04px;text-anchor:middle;paint-order:stroke;stroke:var(--bp-bg);stroke-width:.3px}
.plan text.rf-l{font-size:.8px;fill:var(--bp-line);text-anchor:start}
.bp-car{fill:none;stroke:var(--bp-dim);stroke-width:.1;stroke-dasharray:.4 .25}
.bp-drive{fill:none;stroke:var(--bp-dim);stroke-width:.12;stroke-dasharray:.8 .4}
.bp-ghost{fill:none;stroke:var(--bp-dim);stroke-width:.1;stroke-dasharray:.5 .5;opacity:.6}
.d-minis{display:grid;grid-template-columns:repeat(3,1fr);gap:12px}.d-minis.two{grid-template-columns:1fr 1fr}
.d-minis figure{margin:0}.d-minis figcaption{font-size:.9em;margin-top:8px}.d-minis figcaption b{display:block}
@media (max-width:640px){.d-minis,.d-minis.two{grid-template-columns:1fr}}
'''


def page():
    tpl = open(TEMPLATE).read()
    head, rest = tpl.split("<main class=\"doc\">")
    head = head.replace("<title>Ink & Brass template</title>", "<title>Home floor plan</title>")
    head = head.replace("<!-- House style: Ink & Brass. Template: keep the <style> block, replace <title> and the content inside <main>, then delete this comment. -->\n", "")
    head = head.replace("</style>", CSS + "</style>")
    rows = []
    for name, x1, y1, x2, y2, fl, walls, _, show in ROOMS:
        if show:
            w, d = x2 - x1, y2 - y1
            a = w * d - ((113 - 107.5) * (66.5 - 55.5) + (113 - 102.4) * 6.4 if name == "Garage" else 0)
            size = f'{short(w)} × {short(d)}'
            if name == "Office":
                a, size = 18 * 23 + 7 * 6, "18' × 23' + 7' × 6' desk nook"
            rows.append(f'<tr><td>{name}</td><td class="num">{size}</td><td class="num">{a:,.0f}</td></tr>')
    for name, pts, _ in PORCHES:
        if pts:
            rows.append(f'<tr><td>{name.replace("|", " ")}</td><td class="num">—</td><td class="num">{area(pts):,.0f}</td></tr>')
    upper_area = (107.5 - 78.5) * (66.5 - 40)
    garages = "".join(f'<figure>{garage_svg(v)}<figcaption><b>{v["key"]}. {v["name"]}</b>{v["note"]}</figcaption></figure>' for v in GARAGE_VARIANTS)
    uppers = "".join(f'<figure>{upper_svg(u)}<figcaption><b>{u["key"]}. {u["name"]}</b>{u["note"]}</figcaption></figure>' for u in UPPER)
    body = f"""<main class="doc">
  <header class="d-head">
    <div class="d-top"><span class="d-type">New home build</span><span class="d-date">Draft L · Oct 29, 2026</span></div>
    <h1 class="d-title">Floor plan, draft L</h1>
    <p class="d-lead">A single-level home about 113 feet across, with a bonus floor over the garage, in Youngsville, Louisiana. Draft L takes the fixes from the architectural review: a real roof plan where every slope drains, a stair with 20 code-height risers that lands in the bonus room under full headroom, wider doors where they were tight, and a rated door in place of the grocery hatch. The rooms are the same as draft K.</p>
  </header>

  <div class="d-stats">
    <div><div class="l">Main floor, heated</div><div class="v">{living_area:,.0f} sf</div><div class="s">excludes garage and porches</div></div>
    <div><div class="l">Upstairs bonus</div><div class="v">~{upper_area:,.0f} sf</div><div class="s">over the garage, before knee walls</div></div>
    <div><div class="l">Garage</div><div class="v">{garage_area:,.0f} sf</div><div class="s">two bays plus mower space</div></div>
  </div>

  <div class="d-call"><b>Still to decide</b><span>One or two rooms upstairs, which way is north, and whether to screen the back porch. An architect should confirm the roof plan and size the beams before construction drawings.</span></div>

  <h2 class="d-h2">Rendered sketch</h2>
  <p class="d-note">Furniture follows the hand drawing. The back of the house (pond side) is at the top. Blue lines are new glass, and the dashed box over the range is the plaster hood. Garage shown as sketched, with one wide door.</p>
  <figure class="d-fig wide">{sketch_svg()}</figure>

  <h2 class="d-h2">Blueprint, main floor</h2>
  <p class="d-note">Drawn to scale in feet. Each grid square is 2 ft, the same as one dot in the sketchbook. Exterior walls 6", interior walls about 4½". The purple dashed lines mark the sound-isolated walls.</p>
  <figure class="d-fig wide">{blueprint_svg()}</figure>

  <h2 class="d-h2">Low-voltage plan</h2>
  <p class="d-note">Everything home-runs to the rack in the server room, which also holds the electrical panels and the fiber. The red wedges show roughly what each camera sees.</p>
  <figure class="d-fig wide">{lv_svg()}</figure>

  <h2 class="d-h2">Roof plan</h2>
  <p class="d-note">Seen from above, with the front of the house at the bottom. Arrows point downhill. Every slope runs to an eave: no two roofs meet in a level trough, and no roof drains against a wall. A drainage check on a 3-inch grid over the whole roof finds no spot where water can stand.</p>
  <figure class="d-fig wide">{roof_svg()}</figure>
  <dl class="d-rows">
    <dt>Great room</dt><dd>One side gable, 8:12, on 12 ft walls, from the bedroom wing to the garage. It's the main roof. Its left gable end stands on the bedroom wing roof, and its right end tucks under the garage roof.</dd>
    <dt>Bedroom wing</dt><dd>Hipped at the back. Its ridge runs into the great room roof and meets it in two sloped valleys. The back porch roof ties into its side the same way.</dd>
    <dt>Lounge</dt><dd>A steep 10:12 gable facing the street, with the 14 ft window under it. It runs back into the great room roof.</dd>
    <dt>Office and primary</dt><dd>One hip roof over both, 8:12, ridge running front to back. This replaces the two side-by-side gables that made the flat valley. The ridge runs into the garage roof, and a small hip covers the primary bath.</dd>
    <dt>Garage</dt><dd>A 10:12 side gable on 16 ft walls, with two wall dormers on the front. The taller walls give the bonus room 3'-4" knee walls, 7 ft or more of headroom across its middle 17 ft, and a vaulted ceiling that peaks about 14 ft up. A post and beams carry the corner over the trash area, so the bonus room no longer hangs over open air.</dd>
    <dt>Dining</dt><dd>A low 2:12 standing-seam shed sloping to the back. It runs up into the great room roof and meets the office roof in a sloped valley, instead of ending in an eave against the office wall.</dd>
    <dt>Porches</dt><dd>The back porch and the outdoor kitchen now share one standing-seam plane at 1½:12, so the kitchen roof no longer floats over the porch. The porch now ties in at 11'-6", high enough to clear the glass wall's header. A beam spans the 16 ft courtyard eave in front of the kitchen.</dd>
  </dl>

  <h2 class="d-h2">Changes in this draft</h2>
  <dl class="d-rows">
    <dt>Roof</dt><dd>A real roof plan (above) replaces the placeholder gable over each wing. It fixes both flat valleys, the bedroom wing draining into the great room wall, and the office and primary gables poking through the garage eave.</dd>
    <dt>Stair</dt><dd>20 risers of about 7⅝" (the code limit is 7¾") to a bonus floor 12'-8" up, which leaves room for a 16" floor over the 29 ft garage span. Run 1 climbs toward the front, a 3'-6" landing turns right, and run 2 lands straight into the bonus room, under the great room's ridge, with more than 8 ft of headroom. The space beside and under the stair becomes a walk-in closet off the hall, about 6'-9" × 12'-6". The scullery gives up about 1 ft of depth.</dd>
    <dt>Bedroom wing</dt><dd>The opening from the living room widens from 2'-4" to 3'-5", and the passage behind it to 3'-7". The server room gives up 6". Bedroom 3 and the server room get 3'-0" doors.</dd>
    <dt>Doors</dt><dd>Primary bath door 2'-10", laundry door to the side porch 3'-0". The grocery hatch becomes a 20-minute rated, self-closing pass door at counter height, since code allows only rated doors between the garage and the house. The garage-to-hall door is rated and self-closing, with a 3 ft landing on the garage side because the garage floor sits 6" lower.</dd>
    <dt>Small fixes</dt><dd>The middle front porch posts move ½ ft so the front door is centered between them. The dressing room wardrobes are 2 ft deep for hanging clothes, the mirror moves to the office-side wall, and a window seat replaces the bench under the end window. The generator pad sits 18" off the garage wall. The old garage door options are gone, since the garage is final.</dd>
  </dl>

  <h2 class="d-h2">Carried over from draft K</h2>
  <dl class="d-rows">
    <dt>Glass wall</dt><dd>A 16 ft multi-slide glass wall (steel or bronze-clad wood) replaces the living room's three back windows. It's centered on the front doors, so from the front porch the view runs straight through the house to the back porch and the pond. The four panels stack into a pocket on the left, which needs a thicker wall there. Motorized screens and solar shades drop from ceiling pockets. The porch door at the right end stays, for everyday use. The middle porch post moves 5½ ft left to line up with the glass wall's edge, so nothing sits in the view. A structural engineer sizes the header over the opening and the longer porch beam.</dd>
    <dt>Dining doors</dt><dd>A pair of French doors replaces the dining room's back window, out to the outdoor kitchen. A glass-front wine wall replaces the buffet.</dd>
    <dt>Lounge</dt><dd>Steel-and-glass double doors close the 6 ft opening to the living room. Green-lacquer bookcases sit on both sides of the fireplace, with a bar cabinet in one, so the lounge reads as a library.</dd>
    <dt>Kitchen hood</dt><dd>A tapered plaster hood runs to the ceiling over the range, with a marble slab backsplash and a pot filler. The fridge and freezer get cabinet panels.</dd>
    <dt>Powder room</dt><dd>A furniture-style sinker cypress vanity with an undermount sink in honed marble, a round brass mirror, and a sconce on each side. Calm and classic, with no vessel sink.</dd>
    <dt>Scullery</dt><dd>The pantry becomes a working scullery: a second dishwasher beside the sink, a coffee and beverage station, an appliance garage, a steam or speed oven, and open shelves. Cabinetry only; no walls move.</dd>
    <dt>Dressing room</dt><dd>The primary closet becomes a dressing room with glass-front wardrobes and built-in lighting, a full-length mirror on the office-side wall, and a window seat under the end window. Cabinetry only.</dd>
    <dt>Sound walls</dt><dd>All four office walls and the wall between the laundry and the primary bedroom get double or staggered studs, mineral wool and two layers of ⅝" drywall with damping compound. The office also gets a solid-core door with seals, an insulated ceiling on resilient channel, and lined ducts. Roughly $3–6k over a standard office (estimate, not a quote).</dd>
  </dl>

  <h2 class="d-h2">Ceiling plan</h2>
  <p class="d-note">The living room, kitchen and dining heights are your picks. The rest are suggestions from the design pass, with halls and closets kept lower so the rooms off them feel taller.</p>
  <div class="d-tw"><table>
    <thead><tr><th>Room</th><th class="num">Height</th><th>Treatment</th></tr></thead>
    <tbody>
      <tr><td>Living room</td><td class="num">12'</td><td>Exposed sinker cypress beams about every 4 ft, running right to the front doors (no lowered entry band)</td></tr>
      <tr><td>Kitchen and dining</td><td class="num">11'</td><td>Flat plaster; the hood runs to the ceiling</td></tr>
      <tr><td>Lounge</td><td class="num">11'</td><td>Shallow coffers (suggested)</td></tr>
      <tr><td>Primary bedroom</td><td class="num">11'</td><td>Tray with indirect cove light (suggested)</td></tr>
      <tr><td>Office, bedrooms 2 and 3</td><td class="num">10'</td><td>Flat; acoustic plaster in the office (suggested)</td></tr>
      <tr><td>Halls, baths, closets</td><td class="num">9'</td><td>Flat (suggested)</td></tr>
    </tbody>
  </table></div>

  <h2 class="d-h2">Building specs</h2>
  <dl class="d-rows">
    <dt>Generator</dt><dd>A standby generator on a 3' × 5' pad 18" off the garage's outside wall, tucked in the notch below the mower roll-up door. That keeps its noise and exhaust away from the bedrooms and more than 5 ft from any door or window, and a few shrubs hide it from the street. An automatic transfer switch sits at the main disconnect. Size it once the HVAC is picked; 24 to 26 kW air-cooled with load shedding is typical for a house this size. It keeps the server room, the fridges and the pond pumps running through storms.</dd>
    <dt>Garage</dt><dd>One insulated 20' × 10' door instead of a standard 8' tall one, so the truck clears. A ductless mini-split head on the back wall, and a Level 2 EV charger on the truck bay wall. A 10' door needs about 11'6" of ceiling with a high-lift or wall-mount opener, which pushes the bonus room floor up and adds about two steps to the stair.</dd>
    <dt>Low-voltage</dt><dd>Fifteen PoE cameras around the eaves for Scrypted, plus a video doorbell. Nine Wi-Fi access points, including two outdoor ones for the back and side porches. Cat6 drops at every TV and desk, ceiling speakers in the living room, lounge, back porch and outdoor kitchen, and conduit stubs to the outdoor kitchen, side porch, pond and gate. The server room gets its own mini-split so the rack stays cool around the clock.</dd>
    <dt>Conditioned attic</dt><dd>Spray foam on the underside of the roof deck instead of insulation on the attic floor. The HVAC and water heater then sit in an attic near 80° instead of 140°, and the ducts stop leaking heat. Add a whole-house dehumidifier tied into the HVAC, and a drain pan with a leak sensor under the water heater.</dd>
    <dt>Porch screens</dt><dd>Still under discussion. One option is motorized retractable screens in each back porch and outdoor kitchen opening, which roll up out of sight when you want the open view. Another is fixed screen panels on just the side porch's dashed section. Ceiling fans on every porch either way.</dd>
    <dt>Not taken</dt><dd>No safe room, no pool bath door, and no flood-elevation change, since the site sits well above flood elevation.</dd>
  </dl>

  <h2 class="d-h2">For the architect and engineer</h2>
  <dl class="d-rows">
    <dt>Beams</dt><dd>A 16 ft header over the glass wall, with a 12" pocket wall for the stacked panels. A beam where the kitchen opens to the dining room (16 ft, no wall below). A 21 ft header over the garage door that also carries the bonus room's front wall. A 16 ft beam across the courtyard eave in front of the kitchen. A beam and post at the trash corner under the bonus room, and a 9 ft header where the garage opens to the mower bay, since the bonus room wall sits above both. A 16 ft beam on the back porch between the posts that frame the glass wall. A 23 ft eave beam on the side porch between its two posts (or add a middle post).</dd>
    <dt>Bonus floor</dt><dd>About 16" deep joists or floor trusses over the 26 to 29 ft garage span, no posts in the garage.</dd>
    <dt>Overframing</dt><dd>The great room's left gable end and the office and primary roof where it runs over the garage roof are framed on top of the roofs below (valley or "California" framing).</dd>
    <dt>Code items</dt><dd>Makeup air for a range hood over 400 CFM. Fire separation under the bonus room: 5/8" Type X drywall on the garage ceiling, ½" drywall on the garage walls, and the beams and posts that carry the bonus floor (including the trash-corner post) covered to match; the garage-to-house doors self-closing and rated. Tempered glass for the windows in the tub and shower walls. A 30" × 36" clear space in front of the panels in the server room, with an outside disconnect. A code-sized attic access and walkway to the HVAC and water heater. Design-pressure ratings for the glass wall, the garage door and the windows (about 140 to 150 mph in Lafayette Parish). Check whether the pond counts as a pool for barrier rules.</dd>
  </dl>

  <h2 class="d-h2">Upstairs options</h2>
  <p class="d-note">Over the garage, 12'-8" above the main floor. The stair arrives through the left wall into the middle of the floor, where the ceiling is highest. The walls are 3'-4" knee walls front and back, and the vaulted ceiling peaks about 14 ft up. Windows only where they can exist: the two front wall dormers, the right gable end, and a small window high in the left gable above the great room roof.</p>
  <div class="d-fig wide"><div class="d-minis two">{uppers}</div></div>

  <h2 class="d-h2">Room schedule, main floor</h2>
  <p class="d-note">Inside dimensions to the wall centerline, rounded. Areas in square feet.</p>
  <div class="d-tw"><table>
    <thead><tr><th>Room</th><th class="num">Size</th><th class="num">Area</th></tr></thead>
    <tbody>{"".join(rows)}</tbody>
  </table></div>

  <h2 class="d-h2">Open questions</h2>
  <ol class="d-q">

    <li><b>Upstairs.</b> One bonus room or two rooms? Both now work with the new stair and windows.</li>
    <li><b>Ceilings.</b> Are the suggested heights for the lounge, primary bedroom, office, bedrooms and halls OK?</li>
    <li><b>Orientation.</b> Which way is north? It decides which porches get afternoon sun.</li>
    <li><b>Porch screens.</b> Motorized retractable screens on the back porch, fixed screens on the side porch, or leave them open?</li>
  </ol>

  <footer class="d-foot">Traced from five sketchbook photos (IMG_0054 to IMG_0058), measured at 2 ft per dot. The left bedroom wing is drawn full-size as requested. This is a planning sketch, not construction documents; walls are within about ±1 ft of the hand drawing.</footer>
</main>
</body>
</html>
"""
    open(OUT, "w").write(head + body)


page()
print(f"shell {shell_area:.0f} garage {garage_area:.0f} living {living_area:.0f} porch {porch_area:.0f}")
