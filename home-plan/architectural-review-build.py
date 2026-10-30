import base64, re, sys
SK = '/root/.claude/skills/synced/cc9f2c1b-608a-4e06-a091-ff5bdc1b22f3_d99a4251-bdde-4476-9656-a75eb0a5b2ff/house-styles/assets/ink-and-brass.html'
RV = '/tmp/claude-0/-home-user/79901f7b-853f-526e-8d3a-6f3e4ff70d44/scratchpad/rv/'
OUT = sys.argv[1]
t = open(SK).read()
t = re.sub(r'<title>.*?</title>', '<title>Architectural review, draft K</title>', t)
t = re.sub(r'<!-- House style.*?-->\n?', '', t)
b64 = lambda f: base64.b64encode(open(RV + f, 'rb').read()).decode()

ADD = '''
/* additions */
.rv-fig{margin:18px 0 6px}
.rv-fig svg{width:100%;height:auto;display:block}
.rv-fig img{width:100%;height:auto;display:block;border:1px solid var(--rule)}
.rv-fig figcaption{font-size:13px;color:var(--muted);margin-top:6px}
.rp-shell{fill:none;stroke:var(--rule-strong);stroke-width:.35}
.rp-wing{fill:var(--surface);stroke:var(--body);stroke-width:.3}
.rp-shed{fill:var(--rule);stroke:var(--muted);stroke-width:.2;stroke-dasharray:.8 .5}
.rp-ridge{stroke:var(--ink);stroke-width:.35;stroke-dasharray:1.4 .8}
.rp-t{font-size:2px;fill:var(--muted);text-anchor:middle;font-family:inherit}
.rp-h{font-size:2.3px;fill:var(--ink);text-anchor:middle;font-weight:600;font-family:inherit}
.rp-bad{fill:var(--bad)}.rp-warn{fill:var(--warn)}
.rp-mk{font-size:2.1px;fill:var(--surface);text-anchor:middle;font-weight:700;font-family:inherit}
.rp-line-bad{stroke:var(--bad);stroke-width:.9;fill:none;stroke-linecap:round}
.rp-line-warn{stroke:var(--warn);stroke-width:.9;fill:none;stroke-linecap:round}
.rp-area-bad{fill:var(--bad);opacity:.22}
.sx-t{font-size:12px;fill:var(--muted);font-family:inherit}
.sx-h{font-size:12px;fill:var(--ink);font-weight:600;font-family:inherit}
.sx-roof{fill:none;stroke:var(--ink);stroke-width:2.5}
.sx-roof2{fill:none;stroke:var(--body);stroke-width:1.6;stroke-dasharray:6 4}
.sx-fl{stroke:var(--body);stroke-width:2}
.sx-wall{fill:var(--rule-strong)}
.sx-ok{fill:var(--ok);opacity:.16}.sx-bad{fill:var(--bad);opacity:.2}
.sx-okl{stroke:var(--ok);stroke-width:1.4;stroke-dasharray:5 3}
.sx-dim{stroke:var(--muted);stroke-width:1}
.sx-person{fill:none;stroke:var(--bad);stroke-width:1.6}
.rp-t,.rp-h{paint-order:stroke;stroke:var(--surface);stroke-width:.7px;stroke-linejoin:round}
.sx-t,.sx-h{paint-order:stroke;stroke:var(--bg);stroke-width:4px;stroke-linejoin:round}
.d-tw td .sub{display:block;color:var(--muted);font-size:13px}
'''
t = t.replace('</style>', ADD + '</style>', 1)

# ---------------------------------------------------------------- roof plan
WINGS = [
    ("Bedroom wing", 0, 13, 24, 54, 10, 'y', 20.0),
    ("Lounge", 7, 54, 24, 72, 11, 'y', 18.1),
    ("Great room", 24, 34, 78.5, 62.5, 12, 'x', 23.9),
    ("Dining", 52, 22, 68, 34, 11, 'y', 17.7),
    ("Office", 68, 5, 86, 40, 10, 'y', 17.5),
    ("Primary", 86, -2.5, 106, 40, 11, 'y', 19.3),
    ("Garage + bonus", 78.5, 40, 107.5, 66.5, 15, 'x', 26.0),
]
SHEDS = [(24, 20, 52, 34), (46, 10, 68, 22), (24, 62.5, 52, 72), (106, 16, 112, 40), (107.5, 46.4, 113, 55.5)]
SHELL = [(0, 13), (24, 13), (24, 34), (52, 34), (52, 22), (68, 22), (68, 5), (86, 5), (86, -2.5), (106, -2.5),
         (106, 40), (102.4, 40), (102.4, 46.4), (113, 46.4), (113, 55.5), (107.5, 55.5), (107.5, 66.5), (78.5, 66.5), (78.5, 62.5),
         (68, 62.5), (68, 59), (52, 59), (52, 62.5), (24, 62.5), (24, 72), (7, 72), (7, 54), (0, 54)]
s = []
for x1, y1, x2, y2 in SHEDS:
    s.append(f'<rect class="rp-shed" x="{x1}" y="{y1}" width="{x2-x1}" height="{y2-y1}"/>')
order = [0, 1, 4, 5, 3, 2, 6]
for i in order:
    n, x1, y1, x2, y2, p, ax, r = WINGS[i]
    s.append(f'<rect class="rp-wing" x="{x1}" y="{y1}" width="{x2-x1}" height="{y2-y1}" style="fill-opacity:.82"/>')
    if ax == 'y':
        xm = (x1 + x2) / 2; s.append(f'<line class="rp-ridge" x1="{xm}" x2="{xm}" y1="{y1}" y2="{y2}"/>')
    else:
        ym = (y1 + y2) / 2; s.append(f'<line class="rp-ridge" x1="{x1}" x2="{x2}" y1="{ym}" y2="{ym}"/>')
pts = " ".join(f"{x},{y}" for x, y in SHELL)
s.append(f'<polygon class="rp-shell" points="{pts}"/>')
# problem lines and areas
s.append('<line class="rp-line-bad" x1="86" y1="5" x2="86" y2="40"/>')
s.append('<line class="rp-line-bad" x1="68" y1="22" x2="68" y2="34"/>')
s.append('<line class="rp-line-bad" x1="24" y1="34" x2="24" y2="62.5"/>')
s.append('<line class="rp-line-bad" x1="68" y1="40" x2="106" y2="40"/>')
s.append('<rect class="rp-area-bad" x="102.4" y="40" width="5.1" height="6.4"/>')
s.append('<line class="rp-line-warn" x1="46" y1="22" x2="52" y2="22"/>')
s.append('<rect class="rp-area-bad" x="52" y="59" width="16" height="3.5" style="fill:var(--warn)"/>')
s.append('<line class="rp-line-warn" x1="29.5" y1="34" x2="45.5" y2="34"/>')
# labels
LAB = {0: (12, 24), 1: (15.5, 66), 2: (40, 41.5), 3: (60, 27.5), 4: (77, 16), 5: (96, 24), 6: (93, 60)}
for i, (lx, ly) in LAB.items():
    n, x1, y1, x2, y2, p, ax, r = WINGS[i]
    s.append(f'<text class="rp-h" x="{lx}" y="{ly}">{n}</text><text class="rp-t" x="{lx}" y="{ly+2.6}">plate {p}\' · ridge {r:g}\'</text>')
MK = [(1, 86, 31, 'bad'), (2, 68, 28, 'bad'), (3, 24, 44, 'bad'), (4, 96, 40, 'bad'), (5, 105, 43.2, 'bad'),
      (6, 49, 22, 'warn'), (7, 60, 60.8, 'warn'), (8, 37.5, 34, 'warn')]
for k, x, y, c in MK:
    s.append(f'<circle class="rp-{c}" cx="{x}" cy="{y}" r="1.8"/><text class="rp-mk" x="{x}" y="{y+.75}">{k}</text>')
s.append('<text class="rp-t" x="-3" y="-5.5" style="text-anchor:start">Back (pond) ↑</text><text class="rp-t" x="113" y="76" style="text-anchor:end">↓ Front (street)</text>')
roofsvg = (f'<svg viewBox="-5 -8 123 87" role="img" aria-label="Roof plan of the placeholder roof: seven separate gables at four plate heights, with two flat valleys, a wing draining into a wall, gables butting into the garage eave and an unsupported corner over the trash area.">'
           + "".join(s) + '</svg>')

# ---------------------------------------------------------------- section through the bonus room (x about 90), y 34..68
S, Z = 15, 15        # px per ft
Y0, ZTOP = 32, 28
X = lambda y: 40 + (y - Y0) * S
Yz = lambda z: 30 + (ZTOP - z) * Z
q = []
q.append(f'<rect class="sx-ok" x="{X(45.4)}" y="{Yz(26)}" width="{X(61.1)-X(45.4)}" height="{Yz(12.5)-Yz(26)}" style="opacity:0"/>')
# headroom >= 7 ft band
poly_ok = [(45.4, 12.5), (45.4, 19.5), (53.25, 26), (61.1, 19.5), (61.1, 12.5)]
q.append('<polygon class="sx-ok" points="' + " ".join(f"{X(y)},{Yz(z)}" for y, z in poly_ok) + '"/>')
# option-2 hall and stair arrival, under 6'8"
hall = [(40, 12.5), (40, 15), (44, 18.33), (44, 12.5)]
q.append('<polygon class="sx-bad" points="' + " ".join(f"{X(y)},{Yz(z)}" for y, z in hall) + '"/>')
arr = [(38, 12.5), (38, 15.3), (40, 17.0), (40, 12.5)]
q.append('<polygon class="sx-bad" points="' + " ".join(f"{X(y)},{Yz(z)}" for y, z in arr) + '"/>')
# garage roof underside
q.append(f'<polyline class="sx-roof" points="{X(38.5)},{Yz(13.75)} {X(53.25)},{Yz(26)} {X(68)},{Yz(13.75)}"/>')
# great room / office roof at the stair landing (dashed)
q.append(f'<polyline class="sx-roof2" points="{X(34)},{Yz(12)} {X(40)},{Yz(17)}"/>')
# floors and walls
q.append(f'<line class="sx-fl" x1="{X(34)}" x2="{X(68)}" y1="{Yz(0)}" y2="{Yz(0)}"/>')
q.append(f'<line class="sx-fl" x1="{X(38)}" x2="{X(66.5)}" y1="{Yz(12.5)}" y2="{Yz(12.5)}"/>')
q.append(f'<line class="sx-fl" x1="{X(40)}" x2="{X(66.5)}" y1="{Yz(11.5)}" y2="{Yz(11.5)}" style="stroke-dasharray:4 3;stroke-width:1"/>')
for y, z0, z1 in [(40, 0, 15), (66.5, 0, 15), (38, 0, 12.5)]:
    q.append(f'<rect class="sx-wall" x="{X(y)-3}" y="{Yz(z1)}" width="6" height="{Yz(z0)-Yz(z1)}"/>')
q.append(f'<line class="sx-okl" x1="{X(45.4)}" x2="{X(61.1)}" y1="{Yz(19.5)}" y2="{Yz(19.5)}"/>')
# person 6 ft at y 42
px, pz = X(42.2), 12.5
q.append(f'<line class="sx-person" x1="{px}" x2="{px}" y1="{Yz(pz)}" y2="{Yz(pz+4.6)}"/><circle class="sx-person" cx="{px}" cy="{Yz(pz+5.4)}" r="{0.6*Z}"/>')
# labels
L = lambda y, z, txt, c="sx-t", a="start": q.append(f'<text class="{c}" x="{X(y)}" y="{Yz(z)}" text-anchor="{a}">{txt}</text>')
L(53.25, 26.6, "Garage roof ridge ~26'", "sx-h", "middle")
L(53.25, 18.1, "7 ft headroom or more", "sx-t", "middle")
L(53.25, 16.9, "about 16 ft wide", "sx-t", "middle")
L(53.25, 6.5, "Garage, ~11'6\" ceiling", "sx-h", "middle")
L(53.25, 13.1, "Bonus floor ≈ 12'6\" above the main floor", "sx-t", "middle")
L(34.2, 25.6, "Back hall (option 2):", "sx-h", "start")
L(34.2, 24.6, "2'6\" to 5'10\" of headroom", "sx-t", "start")
L(34.2, 21.6, "Stair arrives here:", "sx-h", "start")
L(34.2, 20.6, "about 3 to 5 ft of headroom", "sx-t", "start")
L(66.2, 13.2, "2'6\" knee wall", "sx-t", "end")
L(34, -1.6, "Back (stair hall, y 38)", "sx-t", "start")
L(68, -1.6, "Front (garage door, y 66.5)", "sx-t", "end")
secsvg = (f'<svg viewBox="0 0 {X(69)+10} {Yz(-2.5)}" role="img" aria-label="Section through the bonus room: the stair arrives and the option 2 hall sits under the low back eave with 2.5 to 5.8 feet of headroom; full headroom is only a 16 ft strip in the middle.">'
          + "".join(q) + '</svg>')

# ---------------------------------------------------------------- page body
def chip(c, txt): return f'<span class="chip {c}">{txt}</span>'

doors = [
    # name, width, verdict, note
    ("Front doors (pair)", "6'0\"", "ok", "Centered on the axis, matches the glass wall."),
    ("Glass wall, living to porch", "16'0\"", "ok", "Framed by the porch posts at x 29.5 and 45.5."),
    ("Porch door, living", "3'0\"", "ok", "Swings out onto the porch."),
    ("Dining French doors", "2 × 2'6\"", "neu", "Works. 2'8\" leaves feel less cramped if the wall allows."),
    ("Primary slider to side porch", "8'0\"", "ok", ""),
    ("Laundry to side porch", "2'8\"", "neu", "Make it 3'0\" for baskets and the trash run."),
    ("Garage to hall", "3'0\"", "warn", "Needs a fire-rated, self-closing door and a landing if there's a step down."),
    ("Garage overhead door", "20'9\" × 10'", "ok", "Needs a wind-rated door and a big header carrying the bonus wall."),
    ("Mower roll-up", "5'2\"", "neu", "Fine up to a 54\" deck. Check the mower's width."),
    ("Bedroom 2 (from hall)", "3'0\"", "ok", ""),
    ("Bedroom 3 (from hall)", "2'4\"", "warn", "Narrow for a bedroom. Go 2'8\" or 3'0\"."),
    ("Living to bedroom wing (cased opening)", "2'4\"", "bad", "Main route to two bedrooms. Widen to 3'0\" or more; the passage is only 3'1\" wide."),
    ("Bath 2", "2'6\"", "ok", ""),
    ("Bath 3, closet 3", "2'5\"", "ok", ""),
    ("Bed 2 walk-in, linen", "2'2\"", "ok", ""),
    ("Server room", "2'6\"", "warn", "A rack on casters barely fits. Use 3'0\"."),
    ("Lounge doors (pair)", "6'0\"", "ok", "Steel and glass, swing into the lounge."),
    ("Office hall door", "3'0\"", "ok", "Across from the stair, as decided. Solid core with seals."),
    ("Office inner door", "2'10\"", "ok", "Solid core with seals; it's on the sound line."),
    ("Powder room", "2'6\"", "ok", ""),
    ("Stair opening", "3'1\"", "ok", ""),
    ("Closet under stairs", "2'2\"", "ok", ""),
    ("Kitchen to scullery", "3'4\"", "ok", ""),
    ("Grocery hatch, garage to scullery", "2'6\"", "bad", "An opening between garage and house must be a rated door; see code items."),
    ("Primary bedroom", "3'0\"", "ok", ""),
    ("Dressing room (cased)", "3'0\"", "ok", ""),
    ("Primary bath", "2'6\"", "warn", "Go 2'10\" or 3'0\" in the primary suite for aging in place."),
    ("Primary WC", "2'5\"", "ok", ""),
    ("Primary shower (cased)", "3'0\"", "ok", ""),
    ("Laundry from hall", "2'9\"", "ok", "Fits a standard washer and dryer."),
    ("Bonus room from stair landing", "4'0\"", "bad", "Wide enough, but it sits under the low eave: about 3 to 6 ft of headroom."),
]
LBL = {"ok": "OK", "warn": "Fix", "bad": "Must fix", "neu": "Optional"}
door_rows = "".join(f'<tr><td>{n}</td><td class="num">{w}</td><td>{chip(c, LBL[c])}</td><td>{note}</td></tr>' for n, w, c, note in doors)
nbad = sum(1 for d in doors if d[2] == "bad")

roof_rows = [
    (1, "bad", "Flat valley between the office and primary wings", "Both roofs slope down toward x 86 and meet in a 35 ft gutter that runs dead level, with eaves at different heights (10' and 11'). Water has nowhere to go but sideways.", "Put the office and primary under one roof, or turn one of the ridges so it runs across the house, or hip the ends."),
    (2, "bad", "Flat valley between the dining and office wings", "Same problem on a 12 ft run at x 68, right above the wine wall and the office TV wall.", "Same fix. Often solved by letting the dining gable die into the great room roof and hipping the office's back end."),
    (3, "bad", "Bedroom wing and lounge drain into the living room wall", "The great room's gable end stands at x 24, and the bedroom wing (and the lounge behind it) slope down into it for about 28 ft. A roof that drains against a wall is the classic leak.", "Turn the great room's left end into a hip, or turn the bedroom wing's ridge, or step the great room roof down over the bedroom wing."),
    (4, "bad", "Office and primary gables butt into the garage's back eave", "Their ridges (17'6\" and 19'4\") are taller than the garage eave (15') where they meet at the y 40 line, so the gables poke through the garage roof. In the 3D model the garage gutter is buried inside the primary roof.", "Tie them into the garage roof with proper valleys, or hold them below the garage eave."),
    (5, "bad", "Garage gable has no wall under it at the trash corner", "The garage roof and bonus floor run to x 107.5, but the house below stops at x 102.4 there. The 3D model shows a hole in the garage's end wall.", "Either pull the bonus room back to x 102.4, or add a beam and post at the trash area, or enclose it."),
    (6, "warn", "Outdoor kitchen roof floats over the back porch", "Its high edge (10'5\") runs 6 ft past the dining wall over the back porch roof, which is lower there (about 8'7\"). Nothing holds that edge up.", "Add a beam and post, or join the two porch roofs into one plane."),
    (7, "warn", "Living room eave hangs 5 ft over the front courtyard", "The great room roof runs to y 62.5 while the kitchen wall sits back at y 59.", "Accept it as a deep eave with outriggers, add two posts to make it a small porch, or hip that section."),
    (8, "warn", "Back porch roof meets the wall where the glass wall's header goes", "The porch roof ties in at about 10'7\". A 10 ft glass wall plus a 16 ft header needs roughly 11'6\" to 12'.", "Raise the porch ledger to the 12 ft plate. It also gives a taller view through the glass."),
]
roof_tbl = "".join(f'<tr><td class="num">{k}</td><td>{chip(c, "Must fix" if c=="bad" else "Fix")}</td><td><b>{h}</b><span class="sub">{w}</span></td><td>{f}</td></tr>' for k, c, h, w, f in roof_rows)

body = f'''
  <header class="d-head">
    <div class="d-top"><span class="d-type">Design review</span><span class="d-date">Draft K · Oct 29, 2026</span></div>
    <h1 class="d-title">Architectural review before the 3D model</h1>
    <p class="d-lead">The floor plan holds up. Every room is closed in, nothing is missing on the main floor, and almost every door and aisle is the right size. The roof and the bonus room don't work yet. The placeholder roof has two flat valleys and a wing that drains into a wall. The stair also comes up where there's only 3 to 5 ft of headroom.</p>
  </header>

  <div class="d-stats">
    <div><div class="l">Must fix before modeling</div><div class="v">11</div><div class="s">5 roof, 4 stair and bonus room, 2 openings</div></div>
    <div><div class="l">Should fix</div><div class="v">13</div><div class="s">roof details, doors, code, layout</div></div>
    <div><div class="l">Openings checked</div><div class="v">{len(doors)}</div><div class="s">{nbad} must fix, the rest OK or minor</div></div>
  </div>

  <div class="d-call"><b>Bottom line</b><span>Everything below the ceiling line can go into the detailed model as drawn. The roof and the stair-to-bonus section need an architect's roof plan first, or the model will be built on a roof that leaks and a bonus room you can't stand up in.</span></div>

  <h2 class="d-h2">What checks out</h2>
  <dl class="d-rows">
    <dt>Walls</dt><dd>Every room on the main floor is closed where it should be and open where it should be. I traced each wall line in the plan data and found no gaps. One 5' × 2' spot at the primary bedroom door has no label. It works as a small vestibule off the hall, so just name it.</dd>
    <dt>Main axis</dt><dd>The front doors, the 16 ft glass wall and the waterfall all sit on x 37.5. The back porch posts at 29.5 and 45.5 frame the glass exactly, so nothing blocks the view.</dd>
    <dt>Kitchen</dt><dd>The island-to-range aisle is about 51 in, and the island-to-sink aisle is about 56 in. Both beat the 48 in target. The fridge and range are on the stair wall, clear of the hall opening.</dd>
    <dt>Halls</dt><dd>The main hall clears about 3'8". The bedroom hall clears about 3'0", which is the code minimum and fine for a short run.</dd>
    <dt>Bedrooms</dt><dd>Every bedroom has a window big enough for emergency escape. The primary bedroom also has the slider. Bedroom 3 is 12'4" deep now, which fixes the problem in the earlier review.</dd>
    <dt>Baths</dt><dd>The toilets have the required side and front clearances, including the tight powder room (18 in from the toilet's center to the wall).</dd>
    <dt>Pond</dt><dd>The water's closest point to the house is about 10 ft, at bedroom 2. That works with the sub-liner drain already in the pond spec.</dd>
  </dl>

  <h2 class="d-h2">Roofline</h2>
  <p class="d-p">Short answer: <b>no, it doesn't make sense yet.</b> The roof in the 3D model was always a placeholder: a separate gable over each wing. That gives seven gables at four different wall heights (10, 11, 12 and 15 ft), with ridges from 17'6" to 26'. Where those gables meet, several joints can't shed water. None of this is a floor plan problem. It's the next design step, and it should happen before anyone spends money on a detailed model.</p>
  <figure class="rv-fig">{roofsvg}
    <figcaption>The placeholder roof from the 3D model, seen from above. Dashed lines are ridges, and grey dashed areas are porch roofs. Red marks must be fixed, and amber marks should be fixed. Heights are in feet above the main floor.</figcaption></figure>
  <div class="d-tw"><table>
    <thead><tr><th class="num">#</th><th>Level</th><th>Problem</th><th>Fix</th></tr></thead>
    <tbody>{roof_tbl}</tbody></table></div>
  <figure class="rv-fig"><img alt="3D still of the garage's right end: the bonus room floor shows through a hole in the gable wall above the trash area" src="data:image/jpeg;base64,{b64('hole.jpg')}" style="max-width:420px">
    <figcaption>Problem 5 in the current 3D model: the bonus floor shows through the garage's end wall above the trash area.</figcaption></figure>
  <p class="d-p"><b>A direction for the architect.</b> Let the great room carry the main side-gabled roof, since it's the tallest and most important room. Treat the bedroom wing, the lounge and the primary suite as front-to-back gables that meet it in proper valleys or hips. Put the office and primary under one roof, or join them with a low connector so no two eaves run side by side. Make the garage either a front-facing gable or a side gable with a long shed dormer on the back. Either way, it must give the bonus room real headroom (next section). That keeps the modern farmhouse look from your wife's photos and gets rid of every flat valley.</p>

  <h2 class="d-h2">Stairs and bonus room</h2>
  <figure class="rv-fig">{secsvg}
    <figcaption>A section through the bonus room, back on the left and the street on the right. Green is where you can stand at 7 ft or more. Red is where the stair arrives and where option 2's hall would be.</figcaption></figure>
  <div class="d-panel bad"><b>Headroom</b><span>The stair arrives at the back of the house (y 38 to 40). That's the low edge of the great room, office and garage roofs, so there's only 3 to 5 ft over the top step. Code needs 6'8". The bonus room's entry opening (x 78.5, y 40.6 to 44.6) has the same problem. Option 2's whole back hall sits under the low eave too, with 2'6" to 5'10" of headroom. Fix: a shed dormer across the back of the garage roof over the stair hall, or taller garage walls, or a stair that arrives toward the front.</span></div>
  <div class="d-panel bad"><b>Riser count</b><span>The bonus floor sits about 12'6" above the main floor. The plan draws two runs of 8 treads, which makes 18 risers of about 8.3 in each. The code limit is 7¾ in. You need 20 risers: two runs of 9 treads at 10 in, plus the landing. That's still about 11'4" long, so it fits in the same 11'6" stair box. The 3D model draws 9 treads per run (19 risers, about 7.9 in), which is close but still over the limit.</span></div>
  <div class="d-panel bad"><b>Top landing</b><span>The second run ends 5 in from the hall wall, so the top step leads straight into a wall. Code needs a 36 in landing in the direction you're walking. End the run about 3 ft sooner, or turn the top onto the landing strip over the closet.</span></div>
  <div class="d-panel bad"><b>Upstairs windows</b><span>Both upstairs options draw windows that can't exist. The ones on the back wall (y 40) sit in a 2'6" knee wall with the office and primary roofs right behind it. The ones on the left wall (x 78.5, y 53 to 58) open into the great room attic. Only the gable-end window and the two front dormers get daylight. A bedroom up there needs an escape window, so this matters if option 2 is chosen.</span></div>
  <div class="d-panel warn"><b>Floor depth</b><span>The bonus floor spans about 26 to 29 ft over the garage with no posts. That takes about 16 in deep joists or trusses, plus the subfloor. The 3D model allows about 11 in. Either drop the garage slab a step or plan on a 13 ft floor-to-floor and 21 risers.</span></div>
  <p class="d-p">Your wife is redrawing the stairs anyway. The numbers to give her: about 20 risers at 7½ in, about 16 ft of total tread run, a 36 in landing at the top, and an arrival point under the middle of the garage roof, not its back edge.</p>

  <h2 class="d-h2">Doors and openings</h2>
  <p class="d-note">Leaf widths from the plan data. Interior doors lose about 2 in to the stop and hinge, so a 2'6" door gives about 28 in of clear width.</p>
  <div class="d-tw"><table>
    <thead><tr><th>Opening</th><th class="num">Width</th><th>Verdict</th><th>Note</th></tr></thead>
    <tbody>{door_rows}</tbody></table></div>

  <h2 class="d-h2">Structure to hand the engineer</h2>
  <dl class="d-rows">
    <dt>Glass wall</dt><dd>A 16 ft header, plus a pocket wall about 12 in thick to hold four stacked panels. A normal exterior wall is 6 in, so the pocket from x 25.1 to 29.5 needs to be drawn thicker.</dd>
    <dt>Kitchen–dining</dt><dd>The great room's back wall line (y 34) has no wall for 16 ft where the kitchen opens to the dining room. A beam has to carry the roof there.</dd>
    <dt>Garage front</dt><dd>A 21 ft header over the 10 ft door that also carries the bonus room's front wall and roof.</dd>
    <dt>Bonus floor</dt><dd>A 26 to 29 ft clear span with no posts (see above). It also has an unsupported corner over the trash area (roof problem 5).</dd>
    <dt>Porch posts</dt><dd>The back porch has a 16 ft span between the posts at 29.5 and 45.5 (needs a beam). The middle post was moved, as already noted in the handoff.</dd>
  </dl>

  <h2 class="d-h2">Code and safety items</h2>
  <p class="d-note">Based on the residential code (IRC) and electrical code (NEC) most Louisiana parishes use. Confirm locally with the Youngsville or Lafayette Parish building office.</p>
  <dl class="d-rows">
    <dt>Grocery hatch</dt><dd>The code allows only rated doors between a garage and the house, so an open hatch or a window there isn't allowed. Use a small 20-minute rated, self-closing pass-through door. The 3D model currently shows a glass window.</dd>
    <dt>Garage door</dt><dd>The garage-to-hall door needs to be solid or fire-rated, ideally self-closing. If the garage floor is a step down, it needs a 3 ft landing on the garage side. The truck's tailgate leaves about 3'7".</dd>
    <dt>Range hood</dt><dd>A pro range hood over 400 CFM needs a makeup-air system. The hood's duct goes up through the 11 ft ceiling and out through the roof, because the range is on an inside wall.</dd>
    <dt>Generator</dt><dd>The pad sits about 5 in from the garage wall. Generac wants at least 18 in from the house and 5 ft from any opening window or door. Slide it out about 1'6".</dd>
    <dt>Shower windows</dt><dd>The windows in bath 2's tub/shower, bath 3's shower and the primary shower need tempered glass and a waterproof sill, or they can move.</dd>
    <dt>Panels</dt><dd>The panels in the server room need a 30 in wide by 36 in deep clear space in front, so keep shelving out of it. With the panels inside, the meter needs an outdoor main or emergency disconnect, which also suits the generator transfer switch.</dd>
    <dt>Attic access</dt><dd>HVAC and the water heater in the attic need a code-sized access opening and a walkway. A knee-wall door from the upstairs stair hall into the great room attic is the easiest way.</dd>
    <dt>Wind</dt><dd>The glass wall, the 21 ft garage door and the windows need design-pressure ratings for the local hurricane wind speed (about 140 to 150 mph in Lafayette Parish). Impact glass is worth pricing for the glass wall even if it's not required.</dd>
    <dt>Pond barrier</dt><dd>If the city treats the pond as a pool, the glass wall, porch door, dining doors and primary slider become part of the barrier and need alarms or self-closing hardware. This is already an open question in the handoff.</dd>
  </dl>

  <h2 class="d-h2">Smaller catches</h2>
  <dl class="d-rows">
    <dt>Front porch posts</dt><dd>The middle pair sits at 33.7 and 42.3. That centers them on x 38, so they're 6 in off the front door axis. Move them to 33.2 and 41.8 so the door is centered between them.</dd>
    <dt>Dressing room</dt><dd>The full-length mirror on the end wall is drawn right over the window (x 106, y 10 to 13). Move the window or the mirror. The wardrobes are drawn 19 in deep, and hanging clothes need 24 in. The bench sits in the aisle, which breaks the "nothing in walkways" rule.</dd>
    <dt>Office vestibule</dt><dd>The office's sound boundary includes the corridor door, so that door and the hall door both need seals and solid cores.</dd>
    <dt>Outdoor kitchen</dt><dd>The grill sits under a covered roof, so it needs a rated vent hood and clearance from the beadboard ceiling.</dd>
  </dl>

  <h2 class="d-h2">Where the 3D model differs from the plan</h2>
  <dl class="d-rows">
    <dt>Roof</dt><dd>The roof exists only in the 3D model. The floor plan has no roof plan, so every roof issue above comes from the model's placeholder roof.</dd>
    <dt>Stairs</dt><dd>The plan has 8 treads per run, and the model has 9.</dd>
    <dt>Bonus floor</dt><dd>The model uses about 11 in of floor depth. A real floor needs about 16 to 18 in.</dd>
    <dt>Hatch</dt><dd>The plan draws a hatch, and the model shows a glass window.</dd>
    <dt>Upstairs windows</dt><dd>The bonus-room windows on the upstairs plans aren't in the model, and most of them couldn't be built (see above).</dd>
    <dt>Garage end wall</dt><dd>The model has a hole above the trash area.</dd>
  </dl>

  <h2 class="d-h2">Recommended order</h2>
  <ol class="d-time">
    <li><span class="w">1</span><span>Fix the six small plan items: the bedroom wing opening, the grocery hatch, the bedroom 3 and server doors, the porch posts, and the dressing room mirror and window. The 3D model can pick these up as is.</span></li>
    <li><span class="w">2</span><span>Have an architect or experienced designer draw a real roof plan and a section through the stair and bonus room, using the direction above. This is the one thing that should come before the detailed model.</span></li>
    <li><span class="w">3</span><span>Your wife redraws the stair with 20 risers and a top landing, arriving under the middle of the garage roof.</span></li>
    <li><span class="w">4</span><span>Then build the full 3D model and renders.</span></li>
  </ol>

  <footer class="d-foot">I checked the draft K plan data (plan-generator.py: rooms, walls, doors, windows, porches), the 3D model source (export.py and src.html: roof wings, plate heights, stair, bonus floor), its current stills, the handoff brief and the draft G design review. Heights and clearances are calculated from the plan's centerline coordinates, so expect them to move by an inch or two in construction drawings. This is a planning-level review, not an engineer's or code official's sign-off.</footer>
'''
t = re.sub(r'<main class="doc">.*</main>', lambda m: '<main class="doc">' + body + '</main>', t, flags=re.S)
open(OUT, 'w').write(t)
print(len(t))
