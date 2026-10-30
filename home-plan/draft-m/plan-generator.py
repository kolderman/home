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
    # guest wing (G1): a daylit foyer replaces the dark hall; each bedroom is a suite
    ("Bedroom 2", 0, 13, 24, 26.8, "wood", True, (-2, -1.2), True),
    ("Vest. 2", 17.5, 26.8, 24, 32, "wood", True, (0, -1.2), False),
    ("Walk-in 2", 12, 26.8, 17.5, 34.4, "wood", True, (0, 0.3), False),
    ("Bath 2", 0, 26.8, 12, 34.4, "tile", True, (-1.2, -0.7), True),
    ("Foyer", 17.5, 32, 24, 38, "wood", False, (1.2, 1.0), False),
    ("Bedroom 3", 0, 34.4, 17.5, 46.7, "wood", True, (2.6, 1.6), True),
    ("Server", 17.5, 38, 24, 46.7, "wood", True, (-0.6, 1.4), False),
    ("Bath 3", 0, 46.7, 11.4, 54, "tile", True, (1.2, -0.4), True),
    ("", 11.4, 46.7, 15.7, 54, "wood", True, (0, 0), False),
    ("Closet 3", 15.7, 46.7, 24, 54, "wood", True, (0.2, -1.0), False),
    ("Lounge", 7, 54, 24, 72, "wood", True, (0, -6.4), True),
    # great room (G2 plan): the courtyard notch is filled, so the kitchen runs to the front wall
    ("Living", 24, 34, 52, 62.5, "wood", False, (0, 9.5), True),
    ("Kitchen", 52, 34, 68, 62.5, "wood", False, (-1.5, 8.9), True),
    ("Dining", 52, 22, 68, 34, "wood", False, (-5.6, -3.4), True),
    # primary suite in the old office spot, entered from a small foyer off the hall
    ("Primary bedroom", 68, 5, 86, 27, "wood", True, (0, -1.6), True),
    ("Suite foyer", 68, 27, 78, 34, "wood", True, (-0.4, 1.2), False),
    ("Powder", 78, 27, 86, 34, "tile", True, (-0.2, -0.3), False),
    ("Hall", 68, 34, 91, 38, "wood", False, (6, 0.4), False),
    ("", 78.5, 38, 91, 40, "wood", False, (0, 0), False),
    ("", 86, 32, 91, 34, "wood", False, (0, 0), False),
    ("Stairs", 68, 38, 71.75, 50.6, "wood", False, (0, 0), False),
    ("", 71.75, 38, 78.5, 50.6, "wood", False, (0, 0), False),
    ("Scullery", 68, 50.6, 78.5, 62.5, "tile", True, (0, -1.0), True),
    # primary bath and closet: the back wall moves out 3.5 ft (a trimmed study option B)
    ("Primary bath", 86, -6, 106, 3, "tile", True, (-3.6, 0.2), True),
    ("Shower", 100, -6, 106, -1, "tile", True, (0, 0), False),
    ("WC", 100, -1, 106, 3, "tile", True, (-0.6, -0.6), False),
    ("Primary closet", 86, 3, 106, 16, "wood", True, (0.6, -3.3), True),
    # the office moves into the old primary bedroom and takes in the side porch strip
    ("Office", 86, 16, 112, 32, "wood", True, (-1.6, 4.6), True),
    ("Laundry", 91, 32, 106, 40, "tile", True, (-3.0, -1.6), True),
    ("Garage", 78.5, 40, 113, 66.5, "conc", False, (-2.0, 4.0), True),
]
# extra interior partitions (wall between the guest foyer and the living room, stair walls, garage wall)
PARTS = [((78.5, 40), (91, 40)), ((24, 31), (24, 38)),
         ((71.75, 38), (71.75, 46.73)), ((68, 38), (68, 50.6)), ((68, 38), (78.5, 38)), ((78.5, 38), (78.5, 50.6))]

PORCHES = [
    ("Back porch", [(24, 20), (46, 20), (46, 10), (68, 10), (68, 22), (52, 22), (52, 34), (24, 34)], (35, 32.6)),
    ("Outdoor kitchen", None, (60.2, 19.2)),
    ("Front porch", [(24, 62.5), (52, 62.5), (52, 72), (24, 72)], (38, 69.6)),
    ("Stoop", [(106, 32), (112, 32), (112, 40), (106, 40)], (109, 37.2)),
    ("Trash", [(102.4, 40), (113, 40), (113, 46.4), (102.4, 46.4)], (106.2, 45.5)),
]
POSTS = [(24.5, 20.5), (29.5, 20.5), (45.5, 20.5), (46.5, 10.5), (57, 10.5), (67.5, 10.5),
         (24.5, 71.5), (33.2, 71.5), (41.8, 71.5), (51.5, 71.5), (111.5, 39.5), (107.1, 40.4)]

# exterior envelope (house + garage)
SHELL = [(0, 13), (24, 13), (24, 34), (52, 34), (52, 22), (68, 22), (68, 5), (86, 5), (86, -6), (106, -6),
         (106, 16), (112, 16), (112, 32), (106, 32),
         (106, 40), (102.4, 40), (102.4, 46.4), (113, 46.4), (113, 55.5), (107.5, 55.5), (107.5, 66.5), (78.5, 66.5), (78.5, 62.5),
         (24, 62.5), (24, 72), (7, 72), (7, 54), (0, 54)]

# windows: wall segments
WINDOWS = [((10.5, 13), (19.5, 13)), ((0, 28.5), (0, 31)), ((0, 35), (0, 37.3)), ((0, 43.9), (0, 46.2)),   # bedroom 3: casements beside the bed, one egress-sized
           ((0, 48.5), (0, 51)), ((8.5, 72), (22.5, 72)),
           ((24, 14), (24, 19)), ((24, 32.3), (24, 33.4)),              # bedroom 2 terrace window, tempered foyer sidelight
           ((26, 62.5), (33, 62.5)), ((42, 62.5), (49, 62.5)), ((55, 62.5), (65, 62.5)),   # front windows, kitchen on the new front wall
           ((52, 25), (52, 30)),
           ((68, 5.5), (68, 8)),                                         # bedroom corner glass toward the falls
           ((90.5, -6), (97.5, -6)), ((101.5, -6), (104.5, -6)), ((86, -5), (86, -1)),   # bath: tub, shower, clerestory over her vanity
           ((106, -0.3), (106, 2.2)), ((106, 10.5), (106, 13.5)),
           ((112, 18.5), (112, 24.5)), ((106.5, 16), (111, 16)),         # office workstation windows
           ((71, 62.5), (76, 62.5))]
# sliding doors: wall segments
SLIDERS = []
# multi-slide glass walls: (start, end, panels, pocket span). Living: 16 ft centered on the front doors, stacking into a pocket on the left.
# Bedroom: 16 ft four-panel stacker with one fixed panel; there's no room for a pocket, so the panels stack inside the opening.
GLASSWALLS = [((29.5, 34), (45.5, 34), 4, (25.1, 29.5)), ((69, 5), (85, 5), 4, (85, 85))]
# sound-isolated walls (double or staggered studs), drawn just inside the room: all four office walls, the bedroom's dining and
# outdoor-kitchen wall, the powder room's headboard wall, the laundry wall and the server room's bedroom 3 wall
SOUND = [((86.7, 16.7), (86.7, 31.3)), ((86.7, 16.7), (111.3, 16.7)), ((86.7, 31.3), (105.3, 31.3)), ((111.3, 16.7), (111.3, 31.3)),
         ((68.7, 5.7), (68.7, 26.3)), ((78.3, 27.7), (85.3, 27.7)), ((91.6, 32.7), (105.4, 32.7)), ((18.2, 38.7), (18.2, 46))]

# doors: (x, y, width, axis, swing_sign, hinge_at_start) ; axis 'h' = wall along x, 'v' = wall along y
DOORS = [
    (19.8, 32, 3, 'h', -1, False),        # guest suite 2, from the foyer (hinge x 22.8, glazed transom)
    (7, 26.8, 2.5, 'h', 1, False),        # bath 2 straight from bedroom 2 (hinge x 9.5)
    (17.5, 34.85, 2.83, 'v', -1, False),  # bedroom 3, from the foyer, swinging into the bedroom (hinge y 37.68)
    (21.1, 38, 2.5, 'h', 1, False),       # server, sealed (hinge x 23.6, clear of the panel space)
    (24, 34.6, 3.0, 'v', -1, False),      # sealed door, living room to the guest foyer (hinge y 37.6, clear of the server wall)
    (15.7, 47.2, 2.4, 'v', 1, True),      # closet 3
    (34.5, 62.5, 3, 'h', -1, True), (37.5, 62.5, 3, 'h', -1, False),   # front doors
    (47, 34, 3, 'h', -1, False),          # porch door
    (73, 34, 3, 'h', -1, True),           # suite foyer, off line from the bedroom pocket door and the stair
    (80.5, 34, 2.5, 'h', -1, True),       # powder
    (87, 32, 3, 'h', -1, True),           # office, solid core and sealed
    (87, 3, 2.83, 'h', -1, True),         # closet to primary bath
    (100, -0.4, 2.5, 'v', -1, True),      # WC, swings out into the bath
    (91, 33, 2.75, 'v', 1, True), (106, 33.0, 3, 'v', -1, False),   # laundry from the hall, laundry to the stoop
    (87, 40, 3, 'h', -1, False), (75.5, 38, 2.5, 'h', 1, False),    # garage to hall, stair closet
    (56.83, 22, 2.67, 'h', -1, True), (59.5, 22, 2.67, 'h', -1, False),   # dining French doors, outswing with a rated sill
    (24, 55.5, 3, 'v', 1, True), (24, 58.5, 3, 'v', 1, False),  # steel-and-glass doors, living to lounge
]
OPENINGS = [((68.4, 38), (71.5, 38)), ((11.6, 46.7), (15.5, 46.7)), ((18.5, 26.8), (23.4, 26.8)), ((68, 53.5), (68, 56.8)),
            ((17.5, 29.4), (17.5, 31.9)),  # vestibule 2 to walk-in 2, cased
            ((86, 10.5), (86, 13.5)),     # bedroom to the closet
            ((100, -3.9), (100, -1.3))]   # curbless shower entry
# pocket doors: walk-in 2 to bath 2 (2'-4"), bath 3, bedroom from the suite foyer
POCKETS = [((12, 29.3), (12, 31.63)), ((11.4, 47.2), (11.4, 49.6)), ((70, 27), (73, 27))]
GARAGE = [(78.5, 40), (102.4, 40), (102.4, 46.4), (113, 46.4), (113, 55.5), (107.5, 55.5), (107.5, 66.5), (78.5, 66.5)]
GARAGE_DOORS = [((80.4, 66.5), (101.2, 66.5)), ((113, 47.2), (113, 52.4))]
CARS = []
FIREPLACES = [(7, 60.5, 1.4, 5.0)]  # x, y, depth into the room, width along the wall: flush gas insert on the lounge's left wall
GENPAD = (109.0, 58.4, 3.1, 5.0)  # standby generator pad 18" off the garage side wall, in the notch below the side roll-up
BUILTINS = [(102.2, 53.6, 10.4, 1.8), (102.2, 55.6, 4.9, 2.2), (105.3, 58.8, 1.8, 3.8), (102.4, 63.6, 4.7, 2.5)]
STAIR_NOTE = "UP"
# 20-minute rated, self-closing pass door from the garage to the scullery, counter height
PASSDOORS = [((78.5, 55), (78.5, 57.5))]
# beams over openings with no wall below: kitchen to living (cypress, 11 ft soffit), the office where the old outside wall comes out,
# and the bonus room over the trash corner
BEAMS = [((52, 34), (52, 62.5)), ((106, 16), (106, 32)),
         ((102.4, 40), (107.5, 40)), ((107.5, 40), (107.5, 46.4)), ((107.5, 46.4), (107.5, 55.5))]
# the old side porch strip inside the office: slab raised and insulated to floor level, ceiling drops to about 8 ft under the porch roof
INFILL = (106, 16, 112, 32)
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
    Roof('Primary bath', 86, -6, 106, 20, plate=11, pitch=K8, ax='y', ends=('hip', 'open'), ov=(1.0, 0.5)),
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
    # the side porch roof stays; the office takes in its back 16 ft, with a beam at x 106 and an 8 ft ceiling at the outer wall
    Roof('Side porch', 106, 16, 112, 40, kind='shed', hi='x1', H=10.4, pitch=3 / 12, ov=(1.5,), rake=(0.6, 0.6), mat='seam'),
    Roof('Mower bay', 107.5, 46.4, 113, 55.5, kind='shed', hi='x1', H=12.5, pitch=3 / 12, ov=(1.5,), rake=(0.6, 0.6), mat='seam'),
]
# top of the outside walls, by area (feet above the main floor)
PLATES = [(0, 13, 24, 54, 10), (7, 54, 24, 72, 11), (24, 34, 78.5, 62.5, 12), (52, 22, 68, 34, 11.5), (68, 5, 86, 40, 11), (86, -6, 106, 40, 11), (78.5, 40, 107.5, 66.5, 16)]


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
    for x, y, w, h in [(26.6, 40, 7.4, 16.5), (41.1, 37.4, 8.8, 13), (27.5, 20.3, 18, 9.8), (2.5, 15, 14, 11), (2.5, 36.2, 10.5, 9.6),
                       (72.4, 17.4, 12, 9.4), (69.4, 6.2, 8, 5.2), (10, 57.5, 12, 12), (90, 19.2, 10, 8.4)]:
        R(x, y, w, h, 0.4, "rug")
    # ---- guest wing (G1)
    # bedroom 2: king bed on the outside wall, reading chair by the terrace window, dresser under the TV
    bed(0.4, 16.8, 6.7, 6.6, 'l'); R(0.4, 14.8, 1.8, 1.8); R(0.4, 23.6, 1.8, 1.8)
    chair(21.4, 15.8, 30); R(22, 19, 1.6, 5.4, 0.1); R(23.35, 19.4, 0.35, 4.6, 0.1, "tv")
    # bath 2: full-length shower on the outside wall, 60" vanity, toilet on the bedroom 3 wall out of the door sightline
    R(0.4, 27, 3.2, 7.2, 0.1, "wet"); R(4.2, 32.6, 5, 1.6, 0.1); sink(6.7, 33.4); toilet(10.55, 32.9, 180)
    # walk-in 2: 24" hanging on both long walls, pocket doors at each end
    R(12.2, 27, 5.1, 2, 0.1); R(12.2, 32.2, 5.1, 2, 0.1)
    # guest foyer: 22" linen cabinet
    R(17.7, 32.2, 1.8, 2.1, 0.1, "fu2")
    f.append('<text class="sk-d" x="18.6" y="33.5" style="font-size:.5px">linen</text>')
    # bedroom 3: TV built-in on the server wall (sound wall behind)
    bed(0.4, 37.4, 6.7, 6.6, 'l'); R(0.4, 35.4, 1.8, 1.8); R(0.4, 44.2, 1.8, 1.8)
    R(15.6, 38.4, 1.7, 6.1, 0.1, "fu2"); R(15.2, 39.5, 0.4, 3.9, 0.1, "tv")
    # server: rack, surface-mounted panels with their 30" x 36" clear space
    R(22.2, 41.2, 1.6, 3.8, 0.1, "fu2"); R(17.7, 38.7, 0.6, 3.5, 0.05); R(18.3, 38.7, 3, 3.5, 0, "oh")
    # bath 3: 36 x 80 shower on the outside wall, 60" vanity, toilet on the door wall; vestibule cabinet; closet 3 with 24" rods
    R(0.4, 46.9, 3, 6.7, 0.1, "wet"); R(4, 46.9, 5, 1.8, 0.1); sink(6.5, 47.8); toilet(9.9, 52.55, 90)
    R(11.6, 52, 3.9, 1.6, 0.1, "fu2")
    R(15.9, 51.8, 7.9, 2, 0.1); R(21.8, 46.9, 2, 4.9, 0.1)
    # ---- lounge: tub chairs around a round table; green-lacquer bookcases either side of the fireplace (bar cabinet in one)
    R(7.4, 54.6, 1.5, 5.5, 0.1, "bk"); R(7.4, 65.9, 1.5, 5.7, 0.1, "bk")
    C(16, 63.5, 1.8); chair(12.4, 59.9, -45, 3); chair(19.6, 59.9, 45, 3); chair(12.4, 67.1, -135, 3); chair(19.6, 67.1, 135, 3)
    # ---- living (G2 plan): media wall centered on the room, a TV group and a glass-facing group either side of a clear 6 ft gallery
    R(24.25, 41.25, 1.35, 14, 0.1, "fu2"); R(25.6, 45.55, 0.4, 5.4, 0.1, "tv")
    sofa(32.5, 43.25, 3, 10, 'r'); R(29.4, 45.25, 2, 6, 0.4)
    chair(29.2, 40.2, 150, 3); chair(29.2, 56.3, 30, 3)
    sofa(41.5, 46, 6, 3, 'b'); R(42.7, 42.6, 3.6, 2.4, 0.4); chair(42.9, 40, 0, 2.8); chair(45.9, 40, 0, 2.8)
    C(48.2, 59, 3.2, "pl"); C(48.2, 59, 1.3, "pl2")
    # ---- kitchen (G2): range centered on the island, island prep sink on the range side, main sink on the new front wall
    R(65.7, 38.2, 2.1, 15, 0.1)
    R(65.7, 38.2, 2.1, 3, 0.1, "fu2")  # refrigerator
    R(65.5, 47, 2.3, 2.5, 0.1, "fu2")  # range
    R(65.0, 46.3, 2.8, 3.9, 0, "oh")  # tapered plaster hood to the ceiling
    for cx, cy in ((66.3, 47.6), (67.1, 47.6), (66.3, 48.9), (67.1, 48.9)): C(cx, cy, 0.3, "fl")
    R(52.4, 60.25, 15.4, 2.0, 0.1); sink(60.0, 61.25)
    for dx in (56.3, 61.8):  # dishwashers either side of the sink
        R(dx, 60.35, 1.9, 1.8, 0.05, "fu2"); P(f"M{dx},60.35 L{dx + 1.9},62.15 M{dx + 1.9},60.35 L{dx},62.15", "fl")
    P("M55.5,55 L55.5,44.45 A2.95,2.95 0 0 1 61.4,44.45 L61.4,55 Z")
    R(55.5, 53.3, 5.9, 1.7, 0.05, "fu2"); P("M58.45,45.6 L58.45,53.3", "fl")
    f.append('<ellipse class="fu2" cx="60.55" cy="48.25" rx=".55" ry=".75"/>')  # 18" prep sink, about 4 ft from the range
    for yy in (43.5, 45.8, 48.1, 50.4, 52.7): C(54.4, yy, 0.75)
    # ---- dining
    C(59.5, 29.6, 2.4); [C(59.5 + 3.3 * math.cos(a), 29.6 + 3.3 * math.sin(a), 0.75) for a in [i * math.pi / 3 for i in range(6)]]
    R(66, 23, 1.9, 10.5, 0.1, "fu2"); P("M65.95,23.2 L65.95,33.3", "wine")  # glass-front wine wall
    f.append('<text class="sk-d" x="67.1" y="28.2" transform="rotate(-90 67.1 28.2)" style="font-size:.6px">wine wall</text>')
    # ---- outdoor kitchen: grill on the west leg, sink on the back leg, the leg on the bedroom wall a cold bar only
    R(54.3, 10.4, 2.0, 6.4, 0.1); R(56.3, 10.4, 2.1, 6.4, 0.1, "fu2"); R(58.4, 10.4, 9.2, 2.2, 0.1); sink(61.4, 11.5)
    R(65.6, 12.6, 2.0, 9.4, 0.1)
    for yy in (11.8, 13.6, 15.4): C(53.5, yy, 0.7)
    f.append('<text class="sk-d" x="57.35" y="13.8" transform="rotate(-90 57.35 13.8)" style="font-size:.55px">grill</text>'
             '<text class="sk-d" x="66.6" y="17.3" transform="rotate(-90 66.6 17.3)" style="font-size:.55px">cold bar</text>')
    # ---- back porch
    sofa(30, 27.2, 10, 3, 'b'); R(32, 22.6, 6, 2.6, 0.4); chair(27.4, 21.9, 45, 2.8); chair(27.4, 27.1, 135, 2.8)
    chair(42.6, 21.9, -45, 2.8); chair(42.6, 27.1, -135, 2.8)
    # ---- front porch
    chair(27.5, 66.3, -20, 2.6); chair(31.5, 66.3, 20, 2.6); C(29.5, 64.6, 0.7)
    chair(44.5, 66.3, -20, 2.6); chair(48.5, 66.3, 20, 2.6); C(46.5, 64.6, 0.7)
    # ---- primary bedroom: king bed on a solid headboard panel on the foyer wall, facing the 16 ft glass; sitting chairs at the glass
    R(75, 20, 6.8, 7, 0.3); R(75.5, 25.2, 2.6, 1.4, 0.3, "fu2"); R(78.7, 25.2, 2.6, 1.4, 0.3, "fu2"); P("M75,23.6 L81.8,23.6", "fl")
    R(74.8, 26.55, 7.2, 0.35, 0.05, "fu2"); R(73.1, 25.2, 1.8, 1.8); R(81.9, 25.2, 1.8, 1.8)
    R(75.6, 18.2, 5.6, 1.3, 0.4, "fu2")
    chair(71.2, 8.4, 180, 2.8); chair(75.4, 8.4, 180, 2.8); C(73.3, 8.6, 0.6)
    R(84.2, 13.8, 1.6, 5.5, 0.1)
    # suite foyer: bench on the left wall, morning bar (coffee, fridge drawers) on the powder wall
    R(68.2, 28, 1.4, 2.8, 0.3); R(76.2, 28, 1.6, 5.5, 0.1, "fu2")
    f.append('<text class="sk-d" x="77" y="30.8" transform="rotate(-90 77 30.8)" style="font-size:.5px">morning bar</text>')
    # powder: 14" shelf cabinet on the headboard wall as a sound buffer, furniture vanity, WC on the far wall
    R(80, 27.2, 5.6, 1.2, 0.1, "fu2"); R(78.2, 28.6, 1.6, 3.4, 0.1); sink(79, 30.3); toilet(84.5, 32, 90)
    # ---- stairs and the closet under them
    f.append(stairs("fl"))
    f.append(f'<path class="ar" d="{STAIR_ARROW}"/>')
    R(77.1, 40.8, 1.2, 9.4, 0.1); R(72.1, 38.3, 3.2, 1.2, 0.1)
    f.append('<text class="sk-d" x="74.6" y="43.6" style="font-size:.6px">walk-in</text><text class="sk-d" x="74.6" y="44.4" style="font-size:.6px">closet</text>')
    # ---- scullery
    R(68.4, 60.3, 6.9, 1.8, 0.1); sink(72.3, 61.2); R(75.3, 60.1, 2.8, 2, 0.1, "fu2")
    R(73.3, 60.4, 1.85, 1.7, 0.05, "fu2"); P("M73.3,60.4 L75.15,62.1 M75.15,60.4 L73.3,62.1", "fl")
    R(68.2, 57.6, 1.8, 2.7, 0.1); R(68.4, 50.8, 9.7, 1.8, 0.1)
    f.append('<text class="sk-d" x="76.4" y="58.6" style="font-size:.6px">rated</text><text class="sk-d" x="76.4" y="59.3" style="font-size:.6px">pass door</text>')
    # ---- primary closet (option B): glass-front wardrobes on both long walls, a 7 ft bench (no island), shoe tower, window seat,
    # full-length mirror on the end panel of the front wardrobe, facing the way in from the bedroom
    R(90.75, 3.25, 15, 2, 0.1); R(90.75, 13.75, 15, 2, 0.1)
    P("M90.9,5.3 L105.6,5.3 M90.9,13.7 L105.6,13.7", "wine"); P("M90.6,13.9 L90.6,15.6", "mirror")
    R(94, 8.5, 7, 2, 0.5, "fu2"); R(104.25, 5.5, 1.5, 4.7, 0.1); R(104.5, 10.5, 1.25, 3, 0.3)
    f.append('<text class="sk-d" x="97.5" y="9.75" style="font-size:.6px">bench</text>')
    # ---- primary bath (option B): tub on the back wall, her vanity on the garden wall, his on the closet wall,
    # curbless 6 x 7 shower with a bench, private WC
    R(91.25, -5.1, 5.5, 2.7, 0.6, "wet"); R(97.75, -5.75, 2, 1.75, 0.1, "fu2")
    R(86.25, -5.5, 1.8, 5, 0.1); sink(87.15, -4.1); sink(87.15, -1.9)
    R(91, 1.2, 6.5, 1.8, 0.1); sink(92.9, 2.1); sink(95.6, 2.1)
    R(100.2, -5.8, 5.6, 4.6, 0.1, "wet"); R(104.5, -5.7, 1.25, 4.4, 0.1, "fu2")
    toilet(104.3, 1, 90)
    # ---- office (layout 3, two rooms in one): theater lounge facing the OLED on the closet wall, workstation by the east windows
    R(89.5, 16.2, 9, 1.4, 0.1, "fu2"); R(90.95, 16.25, 6.1, 0.3, 0.05, "tv")
    sofa(89.5, 25, 10.5, 3, 'b'); sofa(86.5, 20, 3, 8, 'l'); R(91.5, 20.6, 6, 2.6, 0.4)
    chair(101.9, 21.5, 90, 3)
    R(103.5, 16.2, 2.5, 5.8, 0.1, "fu2")
    R(104.5, 29.2, 7.1, 2.3, 0.1); R(109.3, 25.4, 2.3, 3.8, 0.1); chair(106.8, 27.6, 0, 2.2)
    f.append('<text class="sk-d" x="108.6" y="21.4" style="font-size:.55px">8\' ceiling</text>')
    # ---- laundry
    R(91.2, 37.9, 9.6, 1.9, 0.1); R(101, 37.6, 2.2, 2.1, 0.1, "fu2"); R(103.4, 37.6, 2.2, 2.1, 0.1, "fu2")
    R(103.6, 32.4, 1.6, 0.3, 0.1)
    # garage: ductless mini-split head on the back wall, Level 2 EV charger on the truck bay wall
    R(91.6, 40.3, 3.2, 0.6, 0.15, "fu2"); R(78.75, 59.6, 0.55, 1.4, 0.1, "fu2")
    f.append('<text class="sk-d" x="93.2" y="41.9" style="font-size:.6px">mini-split</text><text class="sk-d" x="80.6" y="60.6" style="font-size:.6px">EV</text>')
    # drop zone: bench with cubbies and hooks, left of the garage door
    R(78.7, 38.3, 7.6, 1.5, 0.1, "fu2")
    for xx in (80.6, 82.5, 84.4): P(f"M{xx},38.3 L{xx},39.8", "fl")
    f.append('<text class="sk-d" x="82.5" y="37.5" style="font-size:.7px">drop zone</text>')
    for xx in (104, 107, 110): R(xx, 40.6, 2.4, 2.4, 0.3)  # trash and recycling cans
    R(81.5, 43.6, 7.2, 20, 1.6, "car"); R(82.3, 51, 5.6, 3.4, 0.6, "fl")
    R(94.5, 47, 6.6, 16.5, 1.5, "car"); R(95.3, 52.5, 5, 3.2, 0.6, "fl")
    return "".join(f)


def landscape():
    g = []
    # pond behind the bedroom wing and porch
    g.append('<g transform="translate(0 -4)">')
    g.append('<path class="water" d="M-6,1 C-2,-6 8,-7 14,-3 C20,1 22,7 29,6 C36,5 37,-2 43,-3 C49,-4 52,2 50,6 '
             'C48,10 41,10 36,11 C29,12 25,12 21,11 C15,9.5 12,8 6,9.5 C0,11 -7,8 -6,1 Z"/>')
    g.append('<path class="bed" d="M-8,-1 C-6,-9 6,-10 13,-6" fill="none"/>')
    g.append('</g>')
    # front water garden, held 3 ft off the kitchen wall behind a gravel and planting strip
    g.append('<path class="bedg" d="M52.6,62.9 L78.2,62.9 L78.2,65.3 L52.6,65.3 Z"/>')
    g.append('<path class="water" d="M54,67.4 C55.2,65.9 59,66 61,66.6 C63.2,67.2 66.6,66.5 67,68.6 C67.4,70.8 64.8,71.2 63.6,72.2 '
             'C62.2,73.4 59.6,73.2 58.6,72.2 C57.4,71 55.4,71.8 54.4,70.4 C53.4,69.2 53.2,68.4 54,67.4 Z"/>')
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
            dims = f"{short(x2 - x1)} × {short(y2 - y1)}"
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
    for (x1, y1), (x2, y2) in POCKETS:  # pocket door: a leaf half drawn out of its pocket, the pocket dashed in the wall
        if x1 == x2:
            s.append(f'<rect class="{gap}" x="{x1 - 0.45}" y="{y1}" width="0.9" height="{y2 - y1}"/>'
                     f'<line class="{p}-leaf" x1="{x1}" x2="{x1}" y1="{y1}" y2="{y1 + (y2 - y1) * .55:.2f}"/>'
                     f'<line class="{p}-arc" x1="{x1}" x2="{x1}" y1="{y2}" y2="{y2 + (y2 - y1) * .6:.2f}"/>')
        else:
            s.append(f'<rect class="{gap}" x="{x1}" y="{y1 - 0.45}" width="{x2 - x1}" height="0.9"/>'
                     f'<line class="{p}-leaf" x1="{x1}" x2="{x1 + (x2 - x1) * .55:.2f}" y1="{y1}" y2="{y1}"/>'
                     f'<line class="{p}-arc" x1="{x2}" x2="{x2 + (x2 - x1) * .6:.2f}" y1="{y1}" y2="{y1}"/>')
    if p == 'bp':
        if INFILL:
            x1, y1, x2, y2 = INFILL
            s.append(f'<rect class="bp-infill" x="{x1 + .3}" y="{y1 + .3}" width="{x2 - x1 - .6}" height="{y2 - y1 - .6}"/>'
                     f'<text class="bp-note" transform="translate({x2 - 1.2} {(y1 + y2) / 2}) rotate(-90)">SLAB INFILL · 8\' CLG</text>')
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
    return f'''<svg class="plan sk" viewBox="-12 -16 134 102" role="img" aria-label="Rendered floor plan sketch of a single-level home about 113 by 72 feet, with the bedroom wing on the left, great room in the middle, primary suite and garage on the right.">
<rect class="sk-site" x="-12" y="-16" width="134" height="102"/>
{landscape()}
{building('sk')}
{labels('sk-t', 'sk-d')}
<g class="sk-cap"><text x="-10" y="83">BACK: future pond ↑</text><text x="96" y="83">↓ FRONT: street / drive</text></g>
</svg>'''


def blueprint_svg():
    grid = "".join(f'<line class="bp-grid" x1="{x}" x2="{x}" y1="-20" y2="92"/>' for x in range(-16, 132, 2))
    grid += "".join(f'<line class="bp-grid" y1="{y}" y2="{y}" x1="-16" x2="132"/>' for y in range(-20, 92, 2))
    top = dim_chain([0, 24, 46, 68, 86, 106, 112, 113], -13)
    top2 = dim_chain([0, 113], -17)
    bot = dim_chain([0, 7, 24, 52, 68, 78.5, 107.5, 113], 78)
    left = dim_chain([13, 26.8, 34.4, 54, 72], -6, False)
    left2 = dim_chain([-6, 72], -10, False)
    right = dim_chain([-6, 3, 16, 32, 40, 55.5, 66.5], 119, False)
    scale = ('<g class="bp-scale"><rect x="96" y="83" width="5" height="0.8"/><rect class="o" x="101" y="83" width="5" height="0.8"/>'
             '<rect x="106" y="83" width="10" height="0.8"/><text x="96" y="86.4">0</text><text x="101" y="86.4">5</text>'
             '<text x="106" y="86.4">10</text><text x="116" y="86.4">20 ft</text></g>')
    return f'''<svg class="plan bp" viewBox="-16 -20 148 112" role="img" aria-label="To-scale blueprint floor plan with dimension strings: overall 113 feet wide by 72 feet deep.">
<rect class="bp-bg" x="-16" y="-20" width="148" height="112"/>
{grid}
{building('bp')}
{labels('bp-t', 'bp-d')}
{top}{top2}{bot}{left}{left2}{right}
{scale}
<g class="bp-title"><text x="-14" y="86.4">FIRST FLOOR PLAN · DRAFT M · SCALE 1 SQ = 2 FT</text></g>
<g class="bp-north"><path d="M124,-17 L124,-10 M122.6,-12 L124,-10 L125.4,-12"/><text x="124" y="-18">FRONT</text></g>
</svg>'''


# ---------------------------------------------------------------- roof plan
def roof_svg():
    from roofkit import visible, edges, zp
    vis = visible(ROOFS)
    E = edges(ROOFS, vis)
    o = []
    grid = "".join(f'<line class="bp-grid" x1="{x}" x2="{x}" y1="-20" y2="92"/>' for x in range(-16, 132, 2))
    grid += "".join(f'<line class="bp-grid" y1="{y}" y2="{y}" x1="-16" x2="132"/>' for y in range(-20, 92, 2))
    o.append(f'<rect class="bp-bg" x="-16" y="-20" width="148" height="112"/>{grid}')
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
    o.append('<g class="bp-title"><text x="-14" y="89.6">ROOF PLAN · DRAFT M · SHINGLES ARE THE WARM AREAS, STANDING-SEAM METAL THE COOL ONES · HEIGHTS ABOVE THE MAIN FLOOR</text></g>')
    o.append('<g class="bp-north"><path d="M124,-17 L124,-10 M122.6,-12 L124,-10 L125.4,-12"/><text x="124" y="-18">FRONT</text></g>')
    return ('<svg class="plan bp" viewBox="-16 -20 148 112" role="img" aria-label="Roof plan for draft M: ridges, hips, valleys and slope arrows over the house outline.">'
            + "".join(o) + '</svg>')


# ---------------------------------------------------------------- low voltage
LV_CAMS = [(36, 63.1, 90, "door"), (24.4, 72.2, 115), (51.6, 72.2, 65), (78.8, 66.8, 100), (107.2, 66.8, 80), (113.3, 56.2, 10), (113.2, 46.6, -40),
           (111.8, 16.2, -60), (106.2, -5.8, -40), (85.8, -5.8, -140), (68.3, 4.8, -110), (46.4, 10.2, -90), (24.3, 20.2, -58), (0.3, 13.3, -135), (0.2, 54, 180),
           (7.2, 71.8, 135), (79.6, 41, 40)]
LV_WAPS = [(40, 46), (60, 28), (17.5, 32.6), (96, 24), (77, 18), (93, 54), (35, 27), (110.5, 34), (14, 63)]
LV_DATA = [(68.7, 14.8), (111.4, 29), (94, 16.6), (24.6, 48.25), (23.6, 21.7), (15.2, 41.5), (0.6, 22), (102, 40.6)]
LV_SPK = [(32, 42), (44, 42), (32, 53), (44, 53), (30, 27.5), (41, 27.5), (55, 15), (64, 15), (12, 60), (20, 67)]
LV_CND = [(60, 10.4, "outdoor kitchen"), (38, 20.4, "to the pond"), (111.6, 38.6, "stoop"), (93, 66.4, "gate + drive")]
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
    return (f'<svg class="plan sk lv" viewBox="-12 -16 134 102" role="img" aria-label="Low-voltage plan: cameras, Wi-Fi access points, data drops, ceiling speakers and conduit, all home-run to the rack in the server room.">'
            f'<rect class="sk-site" x="-12" y="-16" width="134" height="102"/><g opacity=".5">{base}{labels("sk-t", "sk-d", sizes=False)}</g>{"".join(s)}</svg>')


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
.bp-infill{fill:none;stroke:var(--bp-dim);stroke-width:.08;stroke-dasharray:.25 .35}
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
            rows.append(f'<tr><td>{name}</td><td class="num">{size}</td><td class="num">{a:,.0f}</td></tr>')
    for name, pts, _ in PORCHES:
        if pts:
            rows.append(f'<tr><td>{name.replace("|", " ")}</td><td class="num">—</td><td class="num">{area(pts):,.0f}</td></tr>')
    upper_area = (107.5 - 78.5) * (66.5 - 40)
    garages = "".join(f'<figure>{garage_svg(v)}<figcaption><b>{v["key"]}. {v["name"]}</b>{v["note"]}</figcaption></figure>' for v in GARAGE_VARIANTS)
    uppers = "".join(f'<figure>{upper_svg(u)}<figcaption><b>{u["key"]}. {u["name"]}</b>{u["note"]}</figcaption></figure>' for u in UPPER)
    body = f"""<main class="doc">
  <header class="d-head">
    <div class="d-top"><span class="d-type">New home build</span><span class="d-date">Draft M · Oct 30, 2026</span></div>
    <h1 class="d-title">Floor plan, draft M</h1>
    <p class="d-lead">A single-level home about 113 feet across, with a bonus floor over the garage, in Youngsville, Louisiana. Draft M builds in your blueprint picks and the lead-architect review. The primary bedroom moves onto the pond, 27 ft from the kitchen island with no long hallway. The office moves into the old primary bedroom. The kitchen runs to the front wall, and a clear gallery crosses the living room from the front doors to the glass. The guest wing gets a daylit foyer and two real suites, and the primary bath and closet grow by pushing the back wall out 3½ ft. The garage and the server room are unchanged, and the living room keeps its flat 12 ft beamed ceiling.</p>
  </header>

  <div class="d-stats">
    <div><div class="l">Main floor, heated</div><div class="v">{living_area:,.0f} sf</div><div class="s">excludes garage and porches</div></div>
    <div><div class="l">Upstairs bonus</div><div class="v">~{upper_area:,.0f} sf</div><div class="s">over the garage, before knee walls</div></div>
    <div><div class="l">Garage</div><div class="v">{garage_area:,.0f} sf</div><div class="s">two bays plus mower space</div></div>
  </div>

  <div class="d-call"><b>Still to decide</b><span>Melissa's markup of this draft, one or two rooms upstairs, which way is north (it sets the glass on the new bedroom wall), whether an 8 ft ceiling over the desk is fine, and whether to screen the back porch. An architect should confirm the roof plan and size the beams before construction drawings.</span></div>

  <h2 class="d-h2">Rendered sketch</h2>
  <p class="d-note">The back of the house (pond side) is at the top. Blue lines are new glass (and the glass fronts of the wardrobes and wine wall), and the dashed box over the range is the plaster hood. Pocket doors are drawn half out of their pockets.</p>
  <figure class="d-fig wide">{sketch_svg()}</figure>

  <h2 class="d-h2">Blueprint, main floor</h2>
  <p class="d-note">Drawn to scale in feet. Each grid square is 2 ft, the same as one dot in the sketchbook. Exterior walls 6", interior walls about 4½". The purple dashed lines mark the sound-isolated walls, and the dotted box at the office's east end is the old side porch strip.</p>
  <figure class="d-fig wide">{blueprint_svg()}</figure>

  <h2 class="d-h2">Low-voltage plan</h2>
  <p class="d-note">Everything home-runs to the rack in the server room, which also holds the electrical panels and the fiber. The red wedges show roughly what each camera sees. No camera looks into the bedroom glass.</p>
  <figure class="d-fig wide">{lv_svg()}</figure>

  <h2 class="d-h2">Roof plan</h2>
  <p class="d-note">Seen from above, with the front of the house at the bottom. Arrows point downhill. Every slope runs to an eave: no two roofs meet in a level trough, and no roof drains against a wall. A drainage check on a 3-inch grid over the whole roof finds no spot where water can stand.</p>
  <figure class="d-fig wide">{roof_svg()}</figure>
  <dl class="d-rows">
    <dt>Great room</dt><dd>One side gable, 8:12, on 12 ft walls, from the bedroom wing to the garage. It's the main roof. Its left gable end stands on the bedroom wing roof, and its right end tucks under the garage roof. The kitchen's front wall now sits under its front eave, so the courtyard beam from draft L goes away.</dd>
    <dt>Bedroom wing</dt><dd>Hipped at the back. Its ridge runs into the great room roof and meets it in two sloped valleys. The back porch roof ties into its side the same way.</dd>
    <dt>Lounge</dt><dd>A steep 10:12 gable facing the street, with the 14 ft window under it. It runs back into the great room roof.</dd>
    <dt>Primary and office</dt><dd>One hip roof over both, 8:12, ridge running front to back into the garage roof. The primary bath's small hip now starts 3½ ft further back, at the new bath wall; it keeps the same pitch and drains the same way.</dd>
    <dt>Office strip</dt><dd>The old side porch roof stays. The office takes in its back 16 ft, so the ceiling there slopes down to about 8 ft at the outer wall. A 16 ft beam at x 106 carries the main roof's eave where the old outside wall comes out.</dd>
    <dt>Garage</dt><dd>A 10:12 side gable on 16 ft walls, with two wall dormers on the front. The taller walls give the bonus room 3'-4" knee walls, 7 ft or more of headroom across its middle 17 ft, and a vaulted ceiling that peaks about 14 ft up.</dd>
    <dt>Dining and porches</dt><dd>A low 2:12 standing-seam shed over the dining room, and one 1½:12 standing-seam plane over the back porch and the outdoor kitchen, tied in at 11'-6" to clear the glass wall's header.</dd>
  </dl>

  <h2 class="d-h2">Changes in this draft</h2>
  <dl class="d-rows">
    <dt>Primary bedroom</dt><dd>Moves to the pond, into the old office spot. You reach it through a small suite foyer right where the hall leaves the kitchen: about 27 ft from the island, with no long hallway. The bedroom is 18' × 22', with a 16 ft glass wall onto a private garden and a small corner window toward the falls. The king bed sits on a solid headboard panel on the foyer wall and faces the glass. The foyer has a bench and a morning bar, and its door now sits off line from the bedroom's pocket door and away from the stair, so no one in the kitchen sees into the bedroom.</dd>
    <dt>Primary bath and closet</dt><dd>A trimmed study option B: the back wall moves out 3½ ft. The closet becomes 20' × 13' (260 sf), with glass-front wardrobes on both long walls, a 7 ft bench in place of an island, a shoe tower, a window seat and a full-length mirror on the end of the front wardrobe. The bath is 20' × 9': a tub under a back window, her vanity on the garden wall under a high clerestory, his vanity on the closet wall, a curbless 6' × 5' shower with a bench, and a private WC. The pocket door from the bedroom straight into the bath is dropped, since it had nowhere to slide; the way in is bedroom, closet, bath.</dd>
    <dt>Office</dt><dd>Moves into the old primary bedroom and takes in the side porch strip: 26' × 16'. Layout 3: a theater lounge at the west end with the OLED on the closet wall, an L couch and a chair, and a workstation at the east end by two windows. All four walls are sound walls. The couch sits about 6" off the door's swing, measured from the face of the double-stud wall.</dd>
    <dt>Kitchen</dt><dd>The courtyard notch is filled, so the kitchen runs to the front wall. The main sink and both dishwashers move to a 15 ft run under a 10 ft window on the front. The range is centered behind a 13'-6" island, and an 18" prep sink in the island's range side cuts the work triangle from about 43 ft to about 24 ft.</dd>
    <dt>Living room</dt><dd>The media wall is centered on the room. A TV group and a group facing the glass sit either side of a clear 6 ft gallery from the front doors to the glass wall. The sofa sits about 8 ft from the screen, which suits a TV of 75" or less. The ceiling stays flat at 12 ft with the cypress beams, as Melissa asked (no cathedral).</dd>
    <dt>Guest wing</dt><dd>The dark 3 ft hall becomes a daylit foyer with a tempered sidelight and a sealed door to the living room. Bedroom 2 gets a vestibule, a 42 sf walk-in, a terrace window, and its own door straight into bath 2. Both baths get 60" vanities. Bath 3's shower grows from 26" (under code) to 36" × 80". The server room gets a sound wall on the bedroom 3 side, surface-mounted panels and a 2'-6" sealed door. The door's swing just touches a corner of the panel clear space, so nothing may be stored there. Bedroom 3's door now swings into the bedroom, so it never meets the living room door in the foyer.</dd>
    <dt>Outdoor kitchen</dt><dd>The leg on the bedroom wall becomes a cold bar only: no grill, ice maker or TV. The grill moves to the west leg.</dd>
    <dt>Doors</dt><dd>The dining French doors swing out, with 2'-8" leaves and a rated sill against wind-driven rain. The powder room gets its own hall door, a 14" shelf cabinet on the bedroom side as a sound buffer, and a quiet exhaust fan (under 0.5 sone) on a timer.</dd>
    <dt>Front water garden</dt><dd>Held at least 3 ft off the new kitchen wall behind a gravel and planting strip, so no water sits against the slab.</dd>
  </dl>

  <h2 class="d-h2">Carried over</h2>
  <dl class="d-rows">
    <dt>Glass wall</dt><dd>A 16 ft multi-slide glass wall centered on the front doors, so from the front porch the view runs straight through the house to the pond. Its four panels stack into a pocket on the left. Motorized screens and solar shades drop from ceiling pockets, and the porch door at the right end stays for everyday use.</dd>
    <dt>Lounge</dt><dd>Steel-and-glass double doors to the living room, a flush gas insert on the left wall, and green-lacquer bookcases with a bar cabinet, so it reads as a library.</dd>
    <dt>Kitchen hood</dt><dd>A tapered plaster hood to the ceiling, a marble slab backsplash and a pot filler. Paneled fridge and freezer.</dd>
    <dt>Powder room</dt><dd>A furniture-style sinker cypress vanity with an undermount sink in honed marble, a round brass mirror and a sconce on each side.</dd>
    <dt>Scullery</dt><dd>A third dishwasher, a coffee and beverage station, an appliance garage, a steam or speed oven and open shelves.</dd>
    <dt>Sound walls</dt><dd>Double or staggered studs, mineral wool and two layers of ⅝" drywall with damping compound on all four office walls, the bedroom's dining and outdoor-kitchen wall, the powder room's bedroom wall, the laundry wall and the server room's bedroom 3 wall. The office also gets a sealed solid-core door, a ceiling on resilient channel and lined ducts. No recessed boxes or in-wall speakers in the office walls shared with the suite, and the subwoofer stays off the bedroom wall on isolation feet.</dd>
  </dl>

  <h2 class="d-h2">Ceiling plan</h2>
  <p class="d-note">The living room, kitchen and dining heights are your picks. The rest are suggestions, with halls and closets kept lower so the rooms off them feel taller.</p>
  <div class="d-tw"><table>
    <thead><tr><th>Room</th><th class="num">Height</th><th>Treatment</th></tr></thead>
    <tbody>
      <tr><td>Living room</td><td class="num">12'</td><td>Flat, with exposed sinker cypress beams about every 4 ft, running right to the front doors (no lowered entry band, no cathedral)</td></tr>
      <tr><td>Kitchen and dining</td><td class="num">11'</td><td>Flat plaster; a cypress beam at 11 ft marks the opening to the living room, and the hood runs to the ceiling</td></tr>
      <tr><td>Lounge</td><td class="num">11'</td><td>Shallow coffers (suggested)</td></tr>
      <tr><td>Primary bedroom</td><td class="num">11'</td><td>Tray with indirect cove light (suggested)</td></tr>
      <tr><td>Office</td><td class="num">10'</td><td>Flat with acoustic plaster; slopes to about 8 ft over the desk end, under the old porch roof</td></tr>
      <tr><td>Bedrooms 2 and 3</td><td class="num">10'</td><td>Flat (suggested)</td></tr>
      <tr><td>Foyers, halls, baths, closets</td><td class="num">9'</td><td>Flat (suggested)</td></tr>
    </tbody>
  </table></div>

  <h2 class="d-h2">Building specs</h2>
  <dl class="d-rows">
    <dt>Generator</dt><dd>A standby generator on a 3' × 5' pad 18" off the garage's outside wall, in the notch below the mower roll-up door, away from the bedrooms and more than 5 ft from any door or window. An automatic transfer switch at the main disconnect. Size it once the HVAC is picked; 24 to 26 kW air-cooled with load shedding is typical for a house this size.</dd>
    <dt>Garage</dt><dd>One insulated 20' × 10' door so the truck clears, a ductless mini-split head on the back wall, and a Level 2 EV charger on the truck bay wall.</dd>
    <dt>Low-voltage</dt><dd>Sixteen PoE cameras around the eaves for Scrypted, plus a video doorbell. Nine Wi-Fi access points, including two outdoor ones for the back porch and the stoop. Cat6 drops at every TV and desk, ceiling speakers in the living room, lounge, back porch and outdoor kitchen, and conduit stubs to the outdoor kitchen, stoop, pond and gate. The server room gets its own quiet mini-split so the rack stays cool around the clock.</dd>
    <dt>Conditioned attic</dt><dd>Spray foam on the underside of the roof deck. The HVAC and water heater sit in an attic near 80° instead of 140°. Add a whole-house dehumidifier tied into the HVAC, and a drain pan with a leak sensor under the water heater.</dd>
    <dt>Porch screens</dt><dd>Still under discussion: motorized retractable screens in the back porch and outdoor kitchen openings, which roll up out of sight. Ceiling fans on every porch either way.</dd>
    <dt>Not taken</dt><dd>No safe room, no pool bath door, no closet island, and no flood-elevation change, since the site sits well above flood elevation.</dd>
  </dl>

  <h2 class="d-h2">For the architect and engineer</h2>
  <dl class="d-rows">
    <dt>Beams</dt><dd>A 16 ft header over the living room glass wall, with a 12" pocket wall for the stacked panels and a steel portal or moment frame, since little solid wall is left on that side. A 16 ft header over the bedroom glass wall under the 11 ft plate. A cypress-clad beam at 11 ft where the kitchen opens to the living room, and a beam where the kitchen opens to the dining room. A 16 ft beam at x 106 in the office where the old outside wall comes out. A 21 ft header over the garage door that also carries the bonus room's front wall, a beam and post at the trash corner under the bonus room, and a 9 ft header at the mower bay. A 16 ft beam on the back porch between the posts that frame the glass wall.</dd>
    <dt>Slab</dt><dd>The office's porch strip is raised and insulated to floor level. The primary bath's 3½ ft extension and the filled kitchen notch are new slab. Hold the front water garden at least 3 ft off the kitchen wall behind the gravel strip, and the reshaped back pond at least 5 ft from the house, with waterproofing where they come close.</dd>
    <dt>Bedroom glass</dt><dd>16 ft wide with about 1 ft of wall at each end, so there's no room for a pocket. Spec a three- or four-panel stacker, or a lift-and-slide with one fixed panel. If the wall faces west, use low-SHGC glass and add a canopy. Confirm the orientation before sizing it.</dd>
    <dt>Bonus floor</dt><dd>About 16" deep joists or floor trusses over the 26 to 29 ft garage span, no posts in the garage.</dd>
    <dt>Code items</dt><dd>Makeup air for a range hood over 400 CFM. Fire separation under the bonus room and rated, self-closing garage-to-house doors. Tempered glass in the tub and shower windows, the bedroom glass and the guest foyer sidelight. Egress casements in bedrooms 2 and 3 (bedroom 3's window moves beside the bed, so the headboard doesn't block it). A 36 in guard where the bonus floor meets the open stairwell, and a handrail on both stair runs. A curbless primary shower. A 30" × 36" clear space in front of the server room panels, with nothing stored in it, and an outside disconnect. A code-sized attic access and walkway to the HVAC and water heater. Design-pressure ratings for the glass walls, the garage door and the windows (about 140 to 150 mph in Lafayette Parish). Check whether the pond counts as a pool for barrier rules.</dd>
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
    <li><b>Melissa's markup.</b> Bath 2 now has its own door from the bedroom as well as the way through the walk-in; bedroom 3's door opens off the new foyer; bath 3's toilet moves to the door wall; the primary closet has a bench, not an island. Do these work for her?</li>
    <li><b>Upstairs.</b> One bonus room or two rooms?</li>
    <li><b>Office ceiling.</b> Is about 8 ft over the desk end fine, or should the main roof be carried out over the strip (a roof change)?</li>
    <li><b>Orientation.</b> Which way is north? It decides the glass on the new bedroom wall and which porches get afternoon sun.</li>
    <li><b>Porch screens.</b> Motorized retractable screens on the back porch, or leave it open?</li>
  </ol>

  <footer class="d-foot">Traced from five sketchbook photos (IMG_0054 to IMG_0058), measured at 2 ft per dot. The left bedroom wing is drawn full-size as requested. This is a planning sketch, not construction documents; walls are within about ±1 ft of the hand drawing.</footer>
</main>
</body>
</html>
"""
    open(OUT, "w").write(head + body)


page()
print(f"shell {shell_area:.0f} garage {garage_area:.0f} living {living_area:.0f} porch {porch_area:.0f}")
