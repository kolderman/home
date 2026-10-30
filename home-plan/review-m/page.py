import re, sys
OUT = sys.argv[1]
exec(open('/tmp/claude-0/-home-user/79901f7b-853f-526e-8d3a-6f3e4ff70d44/scratchpad/m/composite.py').read())
SK = '/root/.claude/skills/synced/cc9f2c1b-608a-4e06-a091-ff5bdc1b22f3_d99a4251-bdde-4476-9656-a75eb0a5b2ff/house-styles/assets/ink-and-brass.html'
t = open(SK).read()
t = re.sub(r'<title>.*?</title>', '<title>Floor plan review, draft M candidate</title>', t)
t = re.sub(r'<!-- House style.*?-->\n?', '', t)
# the old office dims label is hard-wired to the name "Office"
H['ROOMS'] = [(('Home office',) + r[1:]) if r[0] == 'Office' else r for r in H['ROOMS']]

ADD = '''
/* additions */
.rv-fig{margin:18px 0 6px}
.rv-fig.wide{width:min(1240px,calc(100vw - 32px));position:relative;left:50%;transform:translateX(-50%)}
.rv-fig.wide figcaption{max-width:736px;margin-left:auto;margin-right:auto}
.rv-fig svg{width:100%;height:auto;display:block;border:1px solid var(--rule);border-radius:4px}
.rv-fig figcaption{font-size:13px;color:var(--muted);margin-top:6px}
.plan .bp-bg{fill:var(--surface)}.plan .bp-fl{fill:var(--surface)}
.plan .bp-porch{fill:none;stroke:var(--muted);stroke-width:.12;stroke-dasharray:.7 .4}.plan .bp-post{fill:var(--ink)}
.plan .bp-iw{fill:none;stroke:var(--ink);stroke-width:.38}.plan .bp-ew{fill:none;stroke:var(--ink);stroke-width:.6}
.plan .bp-gap{fill:var(--surface)}.plan .bp-win{stroke:var(--ink);stroke-width:.07}
.plan .bp-leaf{stroke:var(--ink);stroke-width:.12}.plan .bp-arc{fill:none;stroke:var(--muted);stroke-width:.07}
.plan .bp-thin{fill:none;stroke:var(--muted);stroke-width:.07}.plan .bp-gd{stroke:var(--ink);stroke-width:.12;stroke-dasharray:.6 .3}
.plan text.bp-t{font-size:1.05px;font-weight:600;fill:var(--ink);text-anchor:middle;letter-spacing:.04px;text-transform:uppercase;font-family:inherit}
.plan text.bp-t.sm{font-size:.75px}.plan text.bp-t.por{fill:var(--muted);font-weight:400}
.plan text.bp-d{font-size:.85px;fill:var(--muted);text-anchor:middle;font-family:inherit}
.plan text.bp-note{font-size:.75px;fill:var(--muted);font-family:inherit}
.plan .gw{stroke:var(--accent);stroke-width:.2}.plan .gwp{fill:none;stroke:var(--accent);stroke-width:.1;stroke-dasharray:.35 .25}
.plan .snd{stroke:var(--muted);stroke-width:.4;stroke-dasharray:.6 .4;opacity:.7}
.plan .bp-bi{fill:none;stroke:var(--muted);stroke-width:.1}.plan .bp-beam{stroke:var(--ink);stroke-width:.16;stroke-dasharray:1 .35 .25 .35}
.plan .fx{fill:none;stroke:var(--muted);stroke-width:.07;opacity:.75}.plan .fx-m{fill:var(--bad)}
.plan .pk{stroke:var(--ink);stroke-width:.12;stroke-dasharray:.3 .2}
.plan .mk-bad{fill:var(--bad)}.plan .mk-warn{fill:var(--warn)}.plan .mk-neu{fill:var(--muted)}
.plan .mk-t{font-size:1.1px;font-weight:700;fill:var(--surface);text-anchor:middle;font-family:inherit}
.plan .tag{fill:var(--surface);stroke:var(--ink);stroke-width:.1}.plan .tag-bad{fill:var(--surface);stroke:var(--bad);stroke-width:.22}
.plan .tag-warn{fill:var(--surface);stroke:var(--warn);stroke-width:.22}
.plan .tag-t{font-size:.72px;font-weight:700;fill:var(--ink);text-anchor:middle;font-family:inherit}
.d-tw td .sub{display:block;color:var(--muted);font-size:13px}
.d-tw td.k{white-space:nowrap;font-weight:600;color:var(--ink)}
'''
t = t.replace('</style>', ADD + '</style>', 1)

def chip(c, s): return f'<span class="chip {c}">{s}</span>'

# ---------------------------------------------------------------- findings markers
MUST = [
    (1, 86.9, 6.5, "Bedroom-to-bath pocket door can't be built",
     "The pocket door in the bedroom's right wall (x 86, y 5.3 to 7.8) has nowhere to slide. One side is the outside corner of the house, and the other side is where the bath/dressing wall lands at y 8, with the new dressing room opening 2.7 ft beyond. A swinging door there would hit the existing dressing-room-to-bath door.",
     "Drop it. The route is bedroom → dressing room (new 3 ft opening) → bath, which is the classic suite sequence and only a few steps longer."),
    (2, 85.4, 12, "The new dressing room opening lands on the mirror",
     "Draft L moved the full-length mirror to the dressing room's left end wall (x 86, y 10.6 to 13.8). The office swap cuts the new bedroom opening in exactly that spot.",
     "Put the mirror on the inside face of the wardrobe end panel at x 90.6, or on one wardrobe door."),
    (3, 60, 64.4, "The front pond would sit 1 ft from the kitchen wall",
     "Great room G1/G2 fills the courtyard notch and moves the kitchen's front wall to y 62.5. The study then moves the front ecosystem pond to y 63.5 to 71.5. That puts standing water 12 in from a slab-on-grade foundation, in clay with a high water table.",
     "Keep the water edge at least 3 ft off the wall (start it at y 65.5 or later) with a gravel and planting strip, or build it as a raised, fully lined basin with the foundation waterproofed."),
    (4, 2, 50.2, "Bath 3's shower is under code in draft L",
     "Draft L still draws bath 3's shower 26 in wide. The code minimum is 30 in. Every guest wing option (G1, W4, V1) fixes it, so this only matters if draft M were built without one.",
     "Build draft M with a guest wing option. G1 gives bath 3 a 36 × 80 in shower."),
]
SHOULD = [
    (5, 71, 34.9, "Primary suite door", "The suite's hall door (x 68.5 to 71.5) sits in line with the pocket door into the bedroom (x 70 to 73) and faces the bottom of the stair, 4 ft from the kitchen. With both doors open, anyone in the kitchen or on the stair looks straight in at the bed.", "Shift the hall door to x 73 to 76. The two doors then don't line up, and the suite door moves away from the stair. Move the bench to the left wall."),
    (6, 82, 26.3, "Powder room behind the primary headboard", "The new powder room shares the bedroom's headboard wall (y 27) for about 4 ft, and its toilet sits on the office's sound wall. Flush and fan noise at the bed is the most common complaint about this layout.", "Keep the staggered-stud wall with mineral wool, and add a 12 to 15 in shelf or linen cabinet along the y 27 wall inside the powder room as a buffer. Hang the bed on a solid headboard panel, and use a quiet fan (under 0.5 sone) on a timer."),
    (7, 87.6, 24.5, "Theater sound into the primary suite", "Layout 3 puts the OLED on the dressing room wall (y 16) and the couch against the bedroom wall (x 86), so two of the office's four walls back onto the primary suite.", "Keep all four office walls double-stud with two layers of 5/8 in drywall and damping compound, and seal the door. Put no recessed boxes or in-wall speakers in those two walls, and keep the subwoofer off the x 86 wall on isolation feet. Layout 2 (screen on the outside wall) is quieter if this becomes a problem."),
    (8, 109, 19.6, "Enclosing the side porch strip", "The office takes in the old side porch (x 106 to 112). The house's old outside wall at x 106 comes out, so a 16 ft beam has to carry the hip roof's eave. The porch slab sits lower than the floor and must be raised and insulated. The strip keeps its porch roof, so the ceiling over the desk drops to about 8 ft at the outer wall.", "Show the beam, the slab infill and the ceiling on draft M. Decide whether an 8 ft ceiling over the desk is fine, or carry the main hip out to x 112 (a roof change)."),
    (9, 61.9, 48.2, "Kitchen work triangle", "In G2 the fridge (back), range (middle) and sink (front wall) are about 8½, 13 and 21 ft apart, around the island: about 43 ft in total. Kitchen designers aim for 26 ft or less.", "Add an 18 in prep sink in the island on the range side, about 4 ft from the range. The working triangle drops to about 22 ft, and the main sink and dishwashers stay on the front window."),
    (10, 94.4, 4.6, "Primary bath bench crowds the vanities", "The bench drawn in front of the tub leaves 24 in in front of the vanities. Thirty inches is the minimum and 36 in is comfortable.", "Drop the bench or put it at the tub's end."),
    (11, 7.5, 27.6, "Bath 2 only through the closet", "With G1, a guest in bedroom 2 walks through the vestibule, the walk-in closet and two pocket doors to reach the toilet: about 30 ft at night. The dresser drawn 19 in from the bed's side is also too tight.", "Add the direct door the study offers (x 7 to 9.5) and move the dresser to the TV wall. The walk-in stays a pass-through for dressing."),
    (12, 77, 4.0, "Bedroom glass wall", "The 16 ft wall (x 69 to 85) leaves about 1 ft of wall at each end, so there's no room for a pocket. The panels have to stack inside the opening, which leaves about 12 ft clear. It also needs an engineered header under the 11 ft plate, and north is still unknown.", "Spec a 3- or 4-panel stacker, or a lift-and-slide with one fixed panel. Confirm orientation before sizing the glass. A west-facing 16 ft glass wall in a bedroom needs low-SHGC glass and a canopy."),
    (13, 66.2, 15, "Outdoor kitchen against the bedroom wall", "The outdoor kitchen U still runs along x 68, which is now the bedroom wall. The study moves the grill to the x 46 end, but the bar and stools stay right outside the bedroom.", "Make the x 68 leg a cold bar only (no grill, no ice maker, no TV), or turn the U so it opens away from the wall. Keep the double-stud wall."),
    (14, 29, 48.2, "TV distance in the living room", "G2's TV group puts the sofa about 7 ft from the screen on the media wall. That suits about a 65 to 75 in TV, not 85 in.", "Either keep the TV at 75 in or less, or pull the sofa back toward the gallery (it can lose 1 ft and the walk still clears 5 ft)."),
    (15, 60, 21.2, "Dining French doors swing in", "The 2 × 2'6\" leaves open into the dining room. Inswing doors leak in wind-driven rain, though the outdoor kitchen roof helps.", "Use outswing doors with a rated sill, or 2'8\" leaves for a less pinched look."),
    (16, 21.6, 39.6, "Server door crosses the panel space", "The server door swings through a corner of the clear space in front of the electrical panels.", "Most inspectors accept a door swing there, but nothing may be stored in it. A 2'6\" door hinged at x 23.6 almost clears it."),
    (17, 88.5, 30.2, "Office door meets the couch", "The office door opens to within 0 in of the couch return's end. It works, but there's no slack if the couch is any deeper.", "Hold the couch return to 8 ft long, or hinge the door on the right so it opens against the wall."),
]
def markers(items, cls):
    return ''.join(f'<circle class="mk-{cls}" cx="{x}" cy="{y}" r="1.25"/><text class="mk-t" x="{x}" y="{y + .4}">{k}</text>' for k, x, y, *_ in items)
findings_svg = plan(markers(MUST, 'bad') + markers(SHOULD, 'warn'), aria='Combined floor plan with numbered review findings: red must be fixed, amber should change.')

# ---------------------------------------------------------------- door schedule
DS = [  # tag, x, y (tag position), name, from-to, width, type, verdict, note
    ('E1', 37.5, 64.2, 'Front doors', 'Porch to living', '6\'0" pair', 'Swing in', 'ok', 'On the x 37.5 axis. 9 ft tall max under the porch roof.'),
    ('E2', 37.5, 32.6, 'Living glass wall', 'Living to back porch', '16\'0"', 'Multi-slide, pocket left', 'ok', 'Needs a moment frame (very little solid wall left on y 34).'),
    ('E3', 48.5, 32.4, 'Porch door', 'Living to back porch', '3\'0"', 'Swing out', 'ok', ''),
    ('E4', 60, 20.6, 'Dining French doors', 'Dining to outdoor kitchen', '2 × 2\'6"', 'Swing in', 'warn', 'Outswing with a rated sill (finding 15).'),
    ('E5', 72, 3.4, 'Bedroom glass wall', 'Primary bedroom to garden', '16\'0"', 'Stacking slider', 'warn', 'No room for a pocket; header; orientation (finding 12).'),
    ('E6', 107.6, 33.8, 'Laundry door', 'Laundry to stoop', '3\'0"', 'Swing in', 'ok', ''),
    ('E7', 91, 68, 'Garage door', 'Garage to drive', '20\'9" × 10\'', 'Overhead', 'ok', 'Wind-rated. Final.'),
    ('E8', 114.6, 49.8, 'Mower roll-up', 'Garage to side yard', '5\'2"', 'Roll-up', 'ok', 'Final.'),
    ('E9', 79.9, 56.2, 'Pass door', 'Garage to scullery', '2\'6"', '20-min rated', 'ok', 'Counter height, self-closing.'),
    ('E10', 88.5, 41.6, 'Garage entry', 'Garage to hall', '3\'0"', 'Swing in, self-closing', 'ok', 'Fire-rated; stoop on the garage side.'),
    ('D1', 25.6, 36.2, 'Guest wing door', 'Living to guest foyer', '3\'5"', 'Swing in, sealed', 'ok', 'Leaf parks flat against the server wall.'),
    ('D2', 21.3, 30.6, 'Suite 2 door', 'Guest foyer to vestibule 2', '3\'0"', 'Swing', 'ok', 'Glazed transom for foyer light.'),
    ('D3', 21, 25.4, 'Bedroom 2', 'Vestibule 2 to bedroom 2', '4\'11"', 'Cased opening', 'ok', ''),
    ('D4', 16.3, 28.2, 'Walk-in 2', 'Vestibule 2 to walk-in', '2\'6"', 'Pocket', 'ok', ''),
    ('D5', 10.6, 30.4, 'Bath 2', 'Walk-in to bath 2', '2\'6"', 'Pocket', 'warn', 'Add a direct door from bedroom 2 (finding 11).'),
    ('D6', 19, 36.4, 'Bedroom 3', 'Guest foyer to bedroom 3', '3\'0"', 'Swing into foyer', 'ok', 'Leaf parks against the server wall.'),
    ('D7', 22.1, 39.6, 'Server', 'Guest foyer to server', '3\'0"', 'Swing in, sealed', 'neu', 'Crosses the panel space corner (finding 16).'),
    ('D8', 13.5, 45.4, 'Vestibule 3', 'Bedroom 3 to vestibule 3', '3\'11"', 'Cased opening', 'ok', ''),
    ('D9', 10.2, 48.4, 'Bath 3', 'Vestibule 3 to bath 3', '2\'5"', 'Pocket', 'ok', ''),
    ('D10', 17, 48.4, 'Closet 3', 'Vestibule 3 to closet 3', '2\'5"', 'Swing', 'ok', ''),
    ('D11', 25.6, 58.5, 'Lounge doors', 'Living to lounge', '6\'0" pair', 'Steel and glass, swing in', 'ok', ''),
    ('D12', 70, 35.6, 'Suite foyer', 'Hall to suite foyer', '3\'0"', 'Swing in', 'warn', 'Shift to x 73 to 76 (finding 5).'),
    ('D13', 71.5, 28.2, 'Primary bedroom', 'Suite foyer to bedroom', '3\'0"', 'Pocket', 'ok', ''),
    ('D14', 84.2, 12, 'Dressing room', 'Bedroom to dressing room', '3\'0"', 'Cased opening', 'bad', 'Lands on the mirror (finding 2).'),
    ('D15', 84.2, 6.6, 'Bath (direct)', 'Bedroom to primary bath', '2\'6"', 'Pocket', 'bad', 'Cannot be built; drop it (finding 1).'),
    ('D16', 88.4, 9.2, 'Primary bath', 'Dressing room to bath', '2\'10"', 'Swing into bath', 'ok', ''),
    ('D17', 90.4, 3.6, 'Primary WC', 'Bath to WC', '2\'5"', 'Swing out', 'ok', ''),
    ('D18', 102.1, 0.8, 'Shower', 'Bath to shower', '3\'0"', 'Cased, no door', 'ok', 'Make it curbless.'),
    ('D19', 81.8, 32.3, 'Powder', 'Hall to powder', '2\'6"', 'Swing in', 'ok', '2\'8" if the wall allows.'),
    ('D20', 88.5, 33.2, 'Office', 'Hall to office', '3\'0"', 'Swing in', 'neu', 'Solid core, sealed. Opens to the couch end (finding 17).'),
    ('D21', 92.8, 37.0, 'Laundry', 'Hall to laundry', '2\'9"', 'Swing in', 'ok', 'Fits a 27 in washer.'),
    ('D22', 76.8, 36.6, 'Stair closet', 'Hall to walk-in closet', '2\'6"', 'Swing in', 'ok', ''),
    ('D23', 70, 39.4, 'Stair', 'Hall to stair', '3\'1"', 'Open', 'ok', '20 risers at 7.6 in, 10 in treads.'),
    ('D24', 66.6, 55.2, 'Scullery', 'Kitchen to scullery', '3\'4"', 'Cased opening', 'ok', ''),
]
def tags():
    s = []
    for tg, x, y, *_r in DS:
        v = _r[5]
        c = 'tag-bad' if v == 'bad' else 'tag-warn' if v == 'warn' else 'tag'
        w = .55 * len(tg) + .5
        s.append(f'<rect class="{c}" x="{x - w / 2}" y="{y - .6}" width="{w}" height="1.2" rx=".6"/><text class="tag-t" x="{x}" y="{y + .26}">{tg}</text>')
    return ''.join(s)
doors_svg = plan(tags(), aria='Combined floor plan with every door and opening tagged E1 to E10 (exterior) and D1 to D24 (interior).')
LB = {'ok': 'OK', 'warn': 'Change', 'bad': 'Must fix', 'neu': 'Note'}
door_rows = ''.join(f'<tr><td class="k">{tg}</td><td>{n}<span class="sub">{ft}</span></td><td class="num">{w}</td><td>{ty}</td><td>{chip(v, LB[v])}</td><td>{note}</td></tr>'
                    for tg, x, y, n, ft, w, ty, v, note in DS)

rooms = [  # name, size, sf, verdict, note
    ('Living', "28' × 28'6\"", 798, 'ok', 'Cathedral in G2. Two seating groups either side of a clear 6 ft gallery from the front doors to the glass.'),
    ('Kitchen', "16' × 28'6\"", 456, 'warn', 'Aisles are 49 in at the range and 63 in at the sink. Add the island prep sink (finding 9).'),
    ('Dining', "16' × 12'", 192, 'ok', 'Fits a 58 to 60 in round table for 6, with 30 in behind the chairs at the wine wall.'),
    ('Scullery', "10'6\" × 11'11\"", 125, 'ok', 'Counters on three walls with a 7'+"'"+'8" aisle. Room for a small work table.'),
    ('Lounge', "17' × 18'", 306, 'ok', 'Library with the gas insert and bookcases. 17 ft width kept.'),
    ('Primary bedroom', "18' × 22'", 396, 'ok', 'King bed faces the glass, 9 ft to the sitting area, 2 ft 5 in to the dresser. Good.'),
    ('Suite foyer', "10' × 7'", 70, 'warn', 'Door alignment (finding 5).'),
    ('Dressing room', "20' × 8'", 160, 'neu', 'Now the only primary closet and also the path to the bath. Study option B (20 × 13½) would help.'),
    ('Primary bath', "20' × 10'6\"", 210, 'warn', 'Bench clearance (finding 10). Tub, 6 × 5 shower, WC room, three sinks.'),
    ('Powder', "8' × 7'", 56, 'warn', 'Generous, but on the headboard wall (finding 6). About 55 ft from the front door.'),
    ('Home office', "26' × 16'", 416, 'warn', 'Two zones work. Sound and the porch strip (findings 7 and 8).'),
    ('Laundry', "15' × 8'", 120, 'ok', '5½ ft aisle, counter, door to the stoop and trash.'),
    ('Bedroom 2', "24' × 13'10\"", 331, 'ok', 'Windows on two walls in G1. Move the dresser (finding 11).'),
    ('Walk-in 2', "5'6\" × 7'7\"", 42, 'neu', 'About 3½ ft aisle between 24 in rods. Small for a primary-size guest suite, fine for guests.'),
    ('Bath 2', "12' × 7'7\"", 91, 'ok', '38 × 86 in shower, 60 in vanity, toilet out of the door sightline.'),
    ('Bedroom 3', "17'6\" × 12'4\"", 215, 'ok', 'Option A size. One window wall. Shares a sound wall with the server.'),
    ('Bath 3', "11'5\" × 7'4\"", 83, 'ok', '36 × 80 in shower in G1 (was 26 in), 60 in vanity.'),
    ('Closet 3', "8'4\" × 7'4\"", 61, 'ok', 'True 24 in rods.'),
    ('Guest foyer', "6'6\" × 6'", 39, 'ok', 'Four doors and a linen cabinet. The swings don\'t clash: the living room and bedroom 3 leaves both park against the server wall.'),
    ('Server', "6'6\" × 8'8\"", 57, 'ok', 'Panels with 30 × 36 in clear space, rack, mini-split.'),
    ('Main hall', "23' × 4'", 92, 'neu', 'About 3\'8" clear. Eight doors and openings use it (finding 5 and circulation).'),
    ('Stair closet', "6'9\" × 12'7\"", 85, 'ok', 'Full height except under run 2.'),
    ('Garage', "34'6\" × 26'6\"", 786, 'ok', 'Final. Not reviewed for changes.'),
]
room_rows = ''.join(f'<tr><td>{n}</td><td class="num">{s}</td><td class="num">{sf}</td><td>{chip(v, LB[v])}</td><td>{note}</td></tr>' for n, s, sf, v, note in rooms)

should_rows = ''.join(f'<tr><td class="num">{k}</td><td><b>{h}</b><span class="sub">{w}</span></td><td>{f}</td></tr>' for k, x, y, h, w, f in SHOULD)
must_panels = ''.join(f'<div class="d-panel bad"><b>{k}. {h}</b><span>{w} <b>Fix:</b> {f}</span></div>' for k, x, y, h, w, f in MUST)

code = [
    ('Emergency escape windows', 'ok', 'Bedroom 2 (back and side windows), bedroom 3 (5 ft window), the primary bedroom (glass wall), and both upstairs rooms in option 2 (dormer and gable windows). Specify a 44 in max sill and 5.7 sf net opening.'),
    ('Shower sizes', 'ok', 'Bath 2 38 × 86, bath 3 36 × 80 with G1, primary 72 × 60. The 26 in shower in draft L is gone.'),
    ('Toilet clearances', 'ok', 'All toilets have 15 in or more to each side and 21 in or more in front.'),
    ('Safety glass', 'warn', 'Tempered glass is required in the three shower windows, the tub window, the guest foyer sidelight (within 24 in of a door) and both glass walls.'),
    ('Garage separation', 'ok', 'Rated self-closing entry door, rated pass door, and 5/8 in Type X ceiling under the bonus room.'),
    ('Stair', 'ok', '20 risers at about 7.6 in, 10 in treads, 3 ft+ clear width, 3½ ft landing, 6\'8" headroom. Add a 36 in guard where the bonus floor meets the open stairwell.'),
    ('Range hood makeup air', 'warn', 'Any hood over 400 CFM needs a makeup-air damper. Still open from the draft K review.'),
    ('Smoke and CO alarms', 'neu', 'In each bedroom, outside each sleeping area and on each level. CO alarms because of the gas range, gas fireplace and attached garage.'),
    ('Panel working space', 'ok', '30 in wide by 36 in deep in front of the panels in the server room.'),
    ('Pond barrier', 'warn', 'Still open. If the city treats the pond as a pool, three glass walls/doors now open toward it (living, porch door and the primary bedroom), and each needs an alarm or self-closing hardware.'),
    ('Wind design', 'neu', 'Both 16 ft glass walls, the 21 ft garage door and every window need design-pressure ratings for the Lafayette Parish wind speed.'),
    ('Front pond setback', 'bad', 'Finding 3: water 1 ft from the foundation.'),
]
code_rows = ''.join(f'<tr><td>{n}</td><td>{chip(v, {"ok":"OK","warn":"Action","bad":"Must fix","neu":"Note"}[v])}</td><td>{note}</td></tr>' for n, v, note in code)

walks = [
    ('Kitchen island to the primary bed', '27 ft', 'about 40 ft', 'ok', 'The main reason for the office swap.'),
    ('Garage door to the kitchen island', '25 ft', '25 ft', 'ok', 'Unchanged. Groceries go through the pass door.'),
    ('Garage door to the primary suite door', '18 ft', 'about 8 ft', 'neu', 'Longer, but still short.'),
    ('Laundry to the primary closet', 'about 45 ft', 'about 18 ft', 'warn', 'The swap\'s real cost. A rolling hamper or a small folding counter in the dressing room helps.'),
    ('Front door to the powder room', 'about 55 ft', 'about 50 ft', 'neu', 'Guests cross the kitchen and pass the suite door. No better spot without giving up the stair closet.'),
    ('Living room to a guest bedroom door', 'under 6 ft', 'about 10 ft', 'ok', 'G1 replaces the dark dog-leg hall.'),
    ('Office door to the desk', 'about 17 ft', 'new', 'ok', 'Along a 3 ft walk behind the couch.'),
]
walk_rows = ''.join(f'<tr><td>{n}</td><td class="num">{a}</td><td class="num">{b}</td><td>{chip(v, {"ok":"Good","warn":"Trade-off","neu":"Note"}[v])}</td><td>{note}</td></tr>' for n, a, b, v, note in walks)

picks = [
    ('Primary bedroom takes the office spot (idea 1)', 'Yes', 'ok', 'It puts the bedroom on the pond 27 ft from the island with no added square feet or roof. Fix findings 1, 2, 5, 6 and 13 as part of it.'),
    ('Office layout 3 (two rooms in one)', 'Yes, with the sound spec', 'ok', 'It gives the clearest split between work and the couch. Finding 7 covers the two shared walls. Layout 2 is the fallback if the TV is ever heard in the bedroom.'),
    ('Great room G2 (cathedral)', 'Yes', 'ok', 'The biggest jump in how the house feels, inside the roof you already have. Add the island prep sink and keep the front pond off the wall (findings 3 and 9).'),
    ('Guest wing G1', 'Yes, plus a direct bath 2 door', 'ok', 'Same footprint, fixes the under-code shower, and turns the dark hall into a lit foyer. W4 is better but costs $35 to 55k and needs the west setback checked. V1 favors one suite over the other.'),
    ('Primary suite option B (bath and closet pushed back 7 ft)', 'Recommended', 'neu', 'With the office swap, the 20 × 8 dressing room is the only primary closet and also the path to the bath. B makes it 20 × 13½. Check the 5 ft pond setback at the new corner.'),
    ('Upstairs: one room or two', 'Either works', 'neu', 'Both meet headroom and escape-window rules after draft L. Two rooms adds a 4th and 5th bedroom; one room is the better bonus space.'),
]
pick_rows = ''.join(f'<tr><td>{n}</td><td>{chip(v, p)}</td><td>{w}</td></tr>' for n, p, v, w in picks)

body = f'''
  <header class="d-head">
    <div class="d-top"><span class="d-type">Design review</span><span class="d-date">Draft L + pending picks · Oct 29, 2026</span></div>
    <h1 class="d-title">Floor plan review, as lead architect</h1>
    <p class="d-lead">This is a good plan, and the pending picks make it better. Moving the primary bedroom to the pond, the cathedral living room and the guest foyer each fix a real weakness. Four things have to be fixed before draft M is built: a pocket door that can't be built, a mirror in a new doorway, the front pond against the kitchen wall, and bath 3's under-code shower if no wing option is taken. Thirteen smaller changes would make it noticeably better.</p>
  </header>

  <div class="d-stats">
    <div><div class="l">Must fix before draft M</div><div class="v">4</div><div class="s">two in the office swap, one in G2, one in draft L</div></div>
    <div><div class="l">Should change</div><div class="v">13</div><div class="s">privacy, sound, kitchen, details</div></div>
    <div><div class="l">Doors and openings checked</div><div class="v">{len(DS)}</div><div class="s">size, place and swing; no swing clashes</div></div>
  </div>

  <div class="d-call"><b>Bottom line</b><span>Say yes to the office swap, office layout 3, great room G2 and guest wing G1, but build them into draft M with the four fixes below and the suite door, powder buffer and island prep sink changes. Then it's ready for an architect's construction set.</span></div>

  <h2 class="d-h2">The plan I reviewed</h2>
  <p class="d-p">Draft M isn't built yet, so I drew the combination you're leaning toward on one plan: <b>draft L</b>, plus the <b>primary bedroom in the office spot</b> with <b>office layout 3</b>, <b>great room G2</b> and <b>guest wing G1</b>. Everything is from the plan data, to scale. Grey outlines are furniture and fixtures, dashed lines are beams, and purple dashes are sound walls.</p>
  <figure class="rv-fig wide">{findings_svg}
    <figcaption>Draft M candidate. Red numbers must be fixed and amber numbers should change; each one is explained below. Pond side at the top, street at the bottom. The red bar at the dressing room is the draft L mirror.</figcaption></figure>

  <h2 class="d-h2">Fix before draft M</h2>
  {must_panels}

  <h2 class="d-h2">Should change</h2>
  <div class="d-tw"><table>
    <thead><tr><th class="num">#</th><th>Issue</th><th>Recommendation</th></tr></thead>
    <tbody>{should_rows}</tbody></table></div>

  <h2 class="d-h2">Every door and opening</h2>
  <p class="d-note">E tags are exterior and D tags are interior. Widths are leaf or opening widths. I ran every hinged door's swing against every other swing and against the drawn furniture: none collide. The one thing a swing reaches is the corner of the server panel space (D7).</p>
  <figure class="rv-fig wide">{doors_svg}
    <figcaption>Door tags. Red tags must be fixed, amber should change.</figcaption></figure>
  <div class="d-tw"><table>
    <thead><tr><th>Tag</th><th>Door</th><th class="num">Width</th><th>Type</th><th>Verdict</th><th>Note</th></tr></thead>
    <tbody>{door_rows}</tbody></table></div>
  <p class="d-p">Primary route doors are all 3 ft or more (suite door, bedroom pocket, dressing opening, shower), and the bath door is 2'10", so the suite works for aging in place if the shower is made curbless.</p>

  <h2 class="d-h2">Room by room</h2>
  <p class="d-note">Sizes are wall center to wall center.</p>
  <div class="d-tw"><table>
    <thead><tr><th>Room</th><th class="num">Size</th><th class="num">Sq ft</th><th>Verdict</th><th>Note</th></tr></thead>
    <tbody>{room_rows}</tbody></table></div>

  <h2 class="d-h2">Walls and structure</h2>
  <dl class="d-rows">
    <dt>Walls that come out</dt><dd>The old office corridor and powder walls, the house's outside wall at x 106 (beam), the kitchen's notched front wall (x 52 to 68 at y 59, with its two short returns), and the old guest hall partitions, linen nook and walk-in.</dd>
    <dt>New walls</dt><dd>Suite foyer and powder (y 27 and x 78), the office's new outside walls (x 112, plus short runs at y 16 and y 32), the kitchen's front wall at y 62.5 (new footing), and the guest wing's closet and vestibule walls.</dd>
    <dt>Beams and posts</dt><dd>Primary bedroom glass header, 16 ft. Office beam at x 106, 16 ft. G2 ridge beam, 28 ft, on posts at (24, 48.25), (52, 34) and (52, 62.5), with footings. The x 52 timber portal. The living glass wall's moment frame. The garage door header and the trash corner beam carry over from draft L.</dd>
    <dt>Sound walls</dt><dd>All four office walls, the primary bedroom's x 68 wall (outdoor kitchen and dining) and its y 27 wall (powder), the laundry wall, and the server wall in the guest wing.</dd>
    <dt>Plumbing</dt><dd>Stacks well. The powder vanity backs onto the suite foyer's morning bar, both guest baths sit on the outside wall, and the kitchen and scullery sinks are both on the front wall. The island prep sink is the one new run.</dd>
    <dt>HVAC</dt><dd>G2 removes the attic over the living room, so plan two systems (bedroom wing attic and kitchen/scullery attic) with low returns in the living room.</dd>
  </dl>

  <h2 class="d-h2">Circulation</h2>
  <div class="d-tw"><table>
    <thead><tr><th>Walk</th><th class="num">Draft M</th><th class="num">Draft L</th><th>Verdict</th><th>Note</th></tr></thead>
    <tbody>{walk_rows}</tbody></table></div>
  <p class="d-p">The main hall becomes the busiest 23 ft in the house. The kitchen, stair, stair closet, suite door, powder, office, laundry and garage entry all open off it. It works at 3'8" clear, but it's why the suite door should step away from the stair (finding 5).</p>

  <h2 class="d-h2">Code check</h2>
  <div class="d-tw"><table>
    <thead><tr><th>Item</th><th>Status</th><th>Note</th></tr></thead>
    <tbody>{code_rows}</tbody></table></div>

  <h2 class="d-h2">Pending picks: my calls</h2>
  <div class="d-tw"><table>
    <thead><tr><th>Choice</th><th>My call</th><th>Why</th></tr></thead>
    <tbody>{pick_rows}</tbody></table></div>

  <h2 class="d-h2">Left as decided</h2>
  <p class="d-p">I didn't reopen these: no foyer or coat closet at the front door, no living room fireplace, no wet room, no closet island, the garage as drawn, the server room where it is, the 16 ft glass wall on the door axis, the range behind the island, and the lounge's 17 ft width.</p>

  <footer class="d-foot">Reviewed from plan-generator.py (draft L) and the option geometry in home-plan/blueprint-study (office-layout.json and office3.py for layout 3, result.json for G2, wing-result.json for G1). Door swings were checked by computing each swing arc against every other arc and the drawn fixtures. Code references are the 2021 IRC as adopted in Louisiana. Confirm locally. This is a planning-level review, not construction documents.</footer>
'''
t = re.sub(r'<main class="doc">.*</main>', lambda m: '<main class="doc">' + body + '</main>', t, flags=re.S)
open(OUT, 'w').write(t)
print(len(t))
