"""Blueprint improvement study page: plan crops of draft L and the verified options, plus a great-room section."""
import json, sys
sys.path.insert(0, '/tmp/claude-0/work/study')
import plan_svg as P, page

S = json.load(open('/tmp/claude-0/work/study/result.json'))['synth']
OPT = {o['id']: o for o in S['primary']['options'] + S['great']['options'] + S['other']}

# drawing fixes per option: open zones (no walls), extra walls, short fixture labels
G_OPEN = [r['name'] for o in ('G1', 'G2', 'G3') for r in OPT[o]['rooms']]
for k in ('G1', 'G2', 'G3'):
    OPT[k]['open'] = G_OPEN
    OPT[k]['walls'] = [(52, 62.5, 68, 62.5)]
    for r in OPT[k]['rooms']:
        if r['name'].startswith('Entry gallery') or r['name'].startswith('Pond gable'): r['nolabel'] = r['name'].startswith('Entry')
for r in OPT['W5']['rooms']:
    if r['name'].startswith('Dining'): r['name'] = 'Dining'
OPT['W5']['open'] = ['Dining']
OPT['W5']['walls'] = [(52, 17, 68, 17), (52, 17, 52, 22)]
SHORT = {'Oval 54x108 for 10 (or 72in round for 8)': 'Table for 10', 'Glass-front wine wall': 'Wine wall',
         'Outdoor grill counter (faces terrace)': 'Grill counter', 'Outdoor return against office wall': 'Counter',
         'Wardrobes back wall (sliding glass, 24in)': 'Wardrobes, 24" deep', 'Wardrobes front wall (sliding glass, 24in)': 'Wardrobes, 24" deep',
         'Her vanity 6ft (x 86 wall)': 'Her vanity', 'His vanity 6.5ft': 'His vanity', 'His vanity 7ft': 'His vanity', 'His vanity 6ft': 'His vanity',
         'Her vanity 6ft': 'Her vanity', 'Freestanding tub 5.5ft': 'Tub', 'Freestanding tub 5ft': 'Tub', 'Hanging 24in (left)': 'Hanging',
         'Hanging 24in (right)': 'Hanging', 'King bed (shifted 1 ft left)': 'King bed', 'Coffee bar + fridge (no sink)': 'Coffee bar',
         'Makeup / linen tower': 'Linen', 'Lockers + bench (4 x 2\'-6")': 'Lockers and bench', 'Drop zone bench (extended)': 'Drop zone',
         'Garage mini-split head (moved)': 'Mini-split', 'Furniture vanity (option A)': 'Vanity', 'Office storage (former shelves)': 'Office storage',
         'Island 13\'-6" x 5\'-11"': 'Island 13\'6"', 'Sofa 10\'-0" (back to gallery)': 'Sofa', 'Settee 6\'-0" facing glass': 'Settee',
         'Media built-in re-centered': 'Media wall', 'Media built-in re-centered, cypress above': 'Media wall', 'TV centered y 48.25': 'TV',
         'Range centered y 48.25': 'Range', 'Sink run on new front wall': 'Sink run', 'Range-wall counter': 'Counter',
         'Glulam ridge beam y 48.25, soffit about 19\'-0"': 'Ridge beam', 'Glulam ridge beam y 48.25': 'Ridge beam',
         'Cypress collar-tie truss (glass jamb line)': 'Cypress truss', 'Cypress collar-tie truss (door axis)': 'Cypress truss',
         'Sloped cypress rafter beam': 'Beam', 'Timber girder/portal truss, chord 11\'-0"': 'Timber portal', 'Chandelier at axis crossing': 'Chandelier',
         'Chandelier hung from ridge beam': 'Chandelier', 'Cypress beam at x 52 (soffit 11\'-0")': 'Timber portal'}
for o in OPT.values():
    for f in o['fixtures']:
        if f['label'] in SHORT: f['short'] = SHORT[f['label']]
        if f['label'] in ('Ridge post in thickened x 24 wall', 'Back-wall portal/moment frame', 'Steel header/moment frame + wind girts',
                          'Valley diverters onto back porch roof', 'Stools x5', 'Swivel chair', 'Lounge chair', 'Coffee table', 'Fridge', 'Plaster hood'):
            f['nolabel'] = True

VB_P, VB_G = (82, -12, 114, 42), (21, 19, 71, 66)


def fig(svg, cap, sub='', cls=''):
    return f'<figure class="pf {cls}">{svg}<figcaption>{cap}<span>{sub}</span></figcaption></figure>'


def section_svg(kind):
    """Cross-section through the living room at the front-door axis, looking left: back (pond) on the left, street on the right."""
    y0, y1 = 14, 76
    sx = lambda y: (y - y0) * 10
    sz = lambda z: 250 - z * 10
    o = [f'<svg class="sec" viewBox="0 0 {sx(y1)} 270" role="img" aria-label="{"Today the living room has a flat 12 ft ceiling with about 9 ft of attic above it." if kind == "now" else "Option G2 opens the ceiling into the roof: 12 ft at the walls rising to about 20 ft 6 in at the ridge beam."}">']
    o.append(f'<line class="s-grade" x1="0" x2="{sx(y1)}" y1="{sz(0)}" y2="{sz(0)}"/>')
    pk = 12.35 + 14.25 * 8 / 12
    roof = [(32.5, 12.35 - 1.5 * 8 / 12), (48.25, pk), (64, 12.35 - 1.5 * 8 / 12)]
    o.append('<polyline class="s-roof" points="' + ' '.join(f'{sx(a)},{sz(b)}' for a, b in roof) + '"/>')
    # porch sheds
    o.append(f'<polyline class="s-shed" points="{sx(20)},{sz(11.5 - 14 * 1.5 / 12)} {sx(34)},{sz(11.5)}"/>')
    o.append(f'<polyline class="s-shed" points="{sx(62.5)},{sz(10.9)} {sx(73.5)},{sz(10.9 - 11 * 2.6 / 12)}"/>')
    for y, z in ((20.5, 11.5 - 13.5 * 1.5 / 12), (71.5, 10.9 - 9 * 2.6 / 12)): o.append(f'<line class="s-post" x1="{sx(y)}" x2="{sx(y)}" y1="{sz(0)}" y2="{sz(z)}"/>')
    # walls: glass wall (back) and front wall with doors
    o.append(f'<rect class="s-wall" x="{sx(33.75)}" y="{sz(12)}" width="5" height="{20}"/><rect class="s-glass" x="{sx(33.85)}" y="{sz(10)}" width="3" height="100"/>')
    o.append(f'<rect class="s-wall" x="{sx(62.25)}" y="{sz(12)}" width="5" height="{30}"/><rect class="s-glass" x="{sx(62.35)}" y="{sz(9)}" width="3" height="90"/>')
    if kind == 'now':
        o.append(f'<line class="s-ceil" x1="{sx(34)}" x2="{sx(62.5)}" y1="{sz(12)}" y2="{sz(12)}"/>')
        for y in range(36, 62, 4): o.append(f'<rect class="s-beam" x="{sx(y) - 3}" y="{sz(12)}" width="6" height="8"/>')
        o.append(f'<text class="s-lab" x="{sx(48.25)}" y="{sz(15.2)}">Attic, about 9 ft</text>')
        o.append(f'<text class="s-dim" x="{sx(48.25)}" y="{sz(6.5)}">Flat ceiling 12\'-0"</text>')
    else:
        ins = [(34.25, 12.0), (48.25, 20.5), (62.25, 12.0)]
        o.append('<polyline class="s-ceil" points="' + ' '.join(f'{sx(a)},{sz(b)}' for a, b in ins) + '"/>')
        o.append(f'<rect class="s-beam" x="{sx(48.25) - 4}" y="{sz(20.4)}" width="8" height="18"/>')
        za = 15.5; ya, yb = 48.25 - (20.5 - za) * 12 / 8, 48.25 + (20.5 - za) * 12 / 8
        o.append(f'<line class="s-tie" x1="{sx(ya)}" x2="{sx(yb)}" y1="{sz(za)}" y2="{sz(za)}"/>')
        o.append(f'<text class="s-dim" x="{sx(48.25)}" y="{sz(14.4)}">Cypress collar tie 15\'-6"</text>')
        o.append(f'<text class="s-dim" x="{sx(48.25)}" y="{sz(6.5)}">12\'-0" at the walls, about 20\'-6" at the ridge beam</text>')
    # person for scale
    px = sx(41)
    o.append(f'<circle class="s-man" cx="{px}" cy="{sz(5.45)}" r="4.5"/><line class="s-man" x1="{px}" x2="{px}" y1="{sz(5)}" y2="{sz(2.6)}"/>'
             f'<line class="s-man" x1="{px}" x2="{px - 4}" y1="{sz(2.6)}" y2="{sz(0)}"/><line class="s-man" x1="{px}" x2="{px + 4}" y1="{sz(2.6)}" y2="{sz(0)}"/>'
             f'<line class="s-man" x1="{px - 5}" x2="{px + 5}" y1="{sz(4.3)}" y2="{sz(4.3)}"/>')
    o.append(f'<text class="s-lab" x="{sx(26.5)}" y="{sz(1.2)}">Back porch</text><text class="s-lab" x="{sx(68)}" y="{sz(1.2)}">Front porch</text>')
    o.append(f'<text class="s-lab" x="{sx(48.25)}" y="{sz(0) + 14}">Living room, 28\'-6" deep</text>')
    o.append('</svg>')
    return ''.join(o)


def rows(d):
    return '<dl class="d-rows">' + ''.join(f'<dt>{k}</dt><dd>{v}</dd>' for k, v in d) + '</dl>'


M = []
M.append('''<header class="d-head">
  <div class="d-top"><span class="d-type">Blueprint study</span><span class="d-date">Draft L · Oct 29, 2026</span></div>
  <h1 class="d-title">Making the floor plan feel like a high-end house</h1>
  <p class="d-lead">You're right about the primary bath and closet. Three moves make the biggest difference: push the primary bath back 7 ft so the closet becomes a real room, open the living room ceiling up into the roof the house already has, and clear a straight walk from the front doors to the glass wall.</p>
</header>
<div class="d-stats">
  <div><div class="l">Primary closet</div><div class="v">270 sf</div><div class="s">from a 160 sf corridor with a 3'7" aisle (option B)</div></div>
  <div><div class="l">Living room ceiling</div><div class="v">20'6"</div><div class="s">at the ridge, from a flat 12 ft (option G2)</div></div>
  <div><div class="l">Added footprint</div><div class="v">196 sf</div><div class="s">140 for the primary bath, 56 to square off the kitchen</div></div>
</div>
<div class="d-call"><b>Bottom line</b><span>Pick primary option B and great room option G2. Together they add under 200 sf and change no roof shapes, and they fix the two things you named.</span></div>''')

M.append('''<h2 class="d-h2">What's already strong, and what holds it back</h2>
<p class="d-p"><b>Strong.</b> The front doors line up with the 16 ft glass wall and the pond. Living and kitchen are one open room about 44 ft by 28'6". There's a real scullery, a sound-isolated office, and a primary suite at the quiet end of the house with its own porch. None of that needs to move.</p>
<p class="d-p"><b>Holding it back.</b></p>
<ul class="d-list">
<li><b>The closet is a corridor.</b> The dressing room is 20 ft by 8 ft, and the walk-through strip uses part of it. That leaves a 3'7" aisle between two wardrobe runs, with no island and one small window.</li>
<li><b>The bath is a strip.</b> It's 210 sf, but only 10'6" deep. The toilet, tub and shower are lined up against the back wall, the sinks face them 3'7" away, and you reach it through the closet. Bath, closet and bedroom are three full-width bands stacked front to back. That layout is why it feels tight, and adding area alone wouldn't fix it.</li>
<li><b>The great room is wide but low.</b> Its ceilings are flat at 12 and 11 ft over a 28'6" span. About 9 ft of height sits unused in the attic right above it.</li>
<li><b>The walk from the front door is blocked.</b> Chairs, the coffee table and a 10'6" sofa with its back to the pond sit in the way.</li>
<li><b>The kitchen notch.</b> A 16 ft by 3'6" notch at the kitchen front leaves the sink window looking into a dark recess.</li>
</ul>''')

# ---------------------------------------------------------------- primary suite
A, B, C = OPT['A'], OPT['B'], OPT['C']
M.append('<h2 class="d-h2">Primary bath and closet</h2><p class="d-note">Draft L on the left, then the three options. The back of the house (pond side) is at the top. One grid square is 2 ft. The tinted area is what changes.</p>')
M.append('<div class="pgrid">' +
         fig(P.render(VB_P, None, 'Draft L primary suite'), 'Draft L', 'Bath 20\' × 10\'6", closet 20\' × 8\'') +
         fig(P.render(VB_P, A, 'Option A'), 'A · Same footprint', 'Closet and bath side by side, 10\' × 19\'6" each') +
         fig(P.render((82, -12, 114, 42), B, 'Option B'), 'B · Push the back wall out 7 ft', 'Closet 20\' × 13\'6", bath 20\' × 12\'', 'rec') +
         fig(P.render((82, -12, 114, 42), C, 'Option C'), 'C · Full luxury, wider by 6 ft', 'His and her closets, 26\' × 12\' bath') + '</div>')
M.append('''<div class="d-tw"><table>
<thead><tr><th>Option</th><th class="num">Closet</th><th class="num">Bath</th><th>Shower</th><th class="num">Added</th><th>Roof</th><th>Verdict</th></tr></thead>
<tbody>
<tr><td>Draft L</td><td class="num">160 sf</td><td class="num">210 sf</td><td>About 5'7" × 4'7"</td><td class="num">0 sf</td><td>As drawn</td><td><span class="chip neu">Tight</span></td></tr>
<tr><td>A · Same footprint</td><td class="num">195 sf</td><td class="num">195 sf</td><td>5'6" × 6'6"</td><td class="num">0 sf</td><td>No change</td><td><span class="chip neu">Fallback</span></td></tr>
<tr><td>B · Back 7 ft</td><td class="num">270 sf</td><td class="num">240 sf</td><td>6' × 7'</td><td class="num">140 sf</td><td>Hip end slides back</td><td><span class="chip ok">Recommended</span></td></tr>
<tr><td>C · Wider too</td><td class="num">284 sf</td><td class="num">312 sf</td><td>8' × 6'</td><td class="num">293 sf</td><td>Hip plus porch roof</td><td><span class="chip neu">If budget allows</span></td></tr>
</tbody></table></div>''')
M.append('<div class="d-cards">')
M.append('<div class="d-card"><h3>A · Same footprint</h3><div class="d-tags"><span>0 sf added</span><span>Low cost</span></div>'
         '<p>The back 19\'6" is split down the middle. The closet becomes a 10 ft wide room with 24" hanging on both walls, a 5\'7" aisle, an ottoman and a window seat. The bath gets facing 6 ft vanities, a 5\'6" × 6\'6" shower, a private toilet room and a freestanding tub. The bedroom loses 1 ft of depth.</p>'
         '<p>The catch: hanging space barely grows, the bath is still reached through the closet, and the toilet room is close to the code minimum. The rooms get a better shape, but no more space.</p></div>')
M.append('<div class="d-card"><h3>B · Push the back wall out 7 ft</h3><div class="d-tags"><span>140 sf added</span><span>Medium cost</span></div>'
         '<p>The bedroom stays exactly as it is. The closet becomes a 20 ft × 13\'6" room with 15 ft of glass-front wardrobes on both long walls, a 7 ft drawer island with 42" aisles, a shoe tower, a window seat, and a mirror and bench on the dressing side.</p>'
         '<p>The bath becomes 20 × 12: a freestanding tub centered under a 7 ft back window, split vanities, a 6 × 7 walk-in shower with a bench, and a private toilet room with its own door. The roof keeps the same hip and ridge, just 7 ft longer, with no new valleys.</p></div>')
M.append('<div class="d-card wide"><h3>C · Full luxury: widen to the side porch</h3><div class="d-tags"><span>293 sf added</span><span>High cost</span></div>'
         '<p>B, plus 6 ft of width over the back end of the side porch. That buys separate his and her closets, a morning coffee bar inside the suite entrance, and a 26 × 12 bath with an 8 × 6 shower lit from two sides.</p>'
         '<p>The cost is roughly twice B\'s added area and more roof work. The side porch loses its open back end, and the ceilings in his closet and the shower slope down to about 9 ft.</p></div>')
M.append('</div>')
M.append('<p class="d-p"><b>Two things to settle for B.</b> Melissa marked "no closet island" on draft G. The island is what makes this closet feel luxurious, but a 7 ft bench works in the same spot if she still says no. Second, the new corner sits about 4 ft from the water on the current long-pond drawing. The pond is being reshaped anyway, so keep its edge at least 5 ft off the house, or push the wall back 6 ft instead of 7.</p>')

# ---------------------------------------------------------------- great room
M.append('<h2 class="d-h2">A grander living room and kitchen</h2><p class="d-note">The front doors are at the bottom and the glass wall to the pond is at the top. The dashed band down the middle is the clear walk from the front doors to the glass.</p>')
M.append('<div class="pgrid">' + fig(P.render(VB_G, None, 'Draft L great room'), 'Draft L', 'Flat 12\' living, 11\' kitchen, notch at the kitchen front') +
         fig(P.render(VB_G, OPT['G2'], 'Option G2'), 'G2 · Cathedral living room plus the plan reset', 'Plan is the same as G1; the beams show the new ceiling', 'rec') + '</div>')
M.append('<div class="pgrid">' + fig(section_svg('now'), 'Section today', 'Through the front doors, looking toward the bedroom wing') +
         fig(section_svg('g2'), 'Section with G2', 'Same roof outside; the ceiling follows it up', 'rec') + '</div>')
M.append('''<div class="d-tw"><table>
<thead><tr><th>Option</th><th>Living ceiling</th><th>What changes</th><th class="num">Added</th><th>Roof</th><th>Verdict</th></tr></thead>
<tbody>
<tr><td>G1 · Plan reset</td><td>Flat 12' (as now)</td><td>Clear entry walk, notch filled, range, island and TV centered on one line</td><td class="num">56 sf</td><td>No change</td><td><span class="chip neu">Budget version</span></td></tr>
<tr><td>G2 · G1 plus cathedral</td><td>12' rising to about 20'6"</td><td>Ridge beam, three cypress trusses, beams still every 4 ft to the front doors</td><td class="num">56 sf</td><td>Same outside</td><td><span class="chip ok">Recommended</span></td></tr>
<tr><td>G3 · G2 plus pond dormer</td><td>As G2, plus a glass gable over the glass wall</td><td>A 16 ft dormer with clerestory glass facing the pond</td><td class="num">56 sf</td><td>Adds a dormer and two valleys</td><td><span class="chip neu">Decide later</span></td></tr>
</tbody></table></div>''')
M.append('''<h3 class="d-h3">What G2 does</h3>
<ul class="d-list">
<li><b>The ceiling goes up into the roof.</b> The living room ceiling rises from 12 ft at the walls to about 20'6" at a glulam ridge beam. Three cypress collar-tie trusses line up with the glass wall's edges and the front-door axis. Sloped cypress beams fill in between them, so your beams still come every 4 ft and still run to the front doors.</li>
<li><b>The kitchen stays at 11 ft.</b> A timber portal at its edge makes the step in height look intended rather than accidental.</li>
<li><b>A clear 6 ft walk from the front doors to the glass.</b> The furniture splits into a TV group and a view group facing the pond, on either side of that walk.</li>
<li><b>A cross line under the ridge.</b> The range, the 13'6" island and the TV all center on it, with a chandelier where it crosses the front-door axis. The range stays on the stair wall behind the island.</li>
<li><b>The notch is filled.</b> The kitchen front wall moves out 3'6", which makes the kitchen 16 × 28'6", and the sink moves to a new 10 ft window that looks at the front water feature. That feature shifts forward about 3 ft.</li>
<li><b>Wider front windows.</b> The living room's front windows go from 6 ft to 7 ft.</li>
</ul>
<p class="d-p"><b>What it costs.</b> This is a rough, unverified estimate of $45-80k more than G1, mostly for the ridge beam, the trusses and the engineering. Ducts can no longer cross the living room, so plan on two air handlers (likely needed at this size anyway). The taller room will sound livelier, so rugs and an acoustic plaster panel help. The front doors stay at 9 ft unless the porch roof is raised. G3's dormer can be added later, once north is known and you've seen the vault in 3D.</p>''')

# ---------------------------------------------------------------- other upgrades
M.append('<h2 class="d-h2">Other upgrades worth making</h2><p class="d-note">Ranked by value for the cost. Each one survived a skeptic\'s check against draft L.</p>')
M.append('<div class="pgrid three">' + fig(P.render((84, 28, 110, 46), OPT['W1'], 'Mud laundry'), '1 · Garage entry through the laundry', 'Lockers, bench, sink, washer and dryer') +
         fig(P.render((64, 24, 84, 40), OPT['W3'], 'Powder room door'), '2 · Powder door on the hall', 'Guests stop using the office vestibule') +
         fig(P.render((44, 6, 72, 36), OPT['W5'], 'Bigger dining'), '4 · Dining 5 ft deeper (optional)', '16 × 17, a table for 8 to 10') + '</div>')
M.append('''<div class="d-tw"><table>
<thead><tr><th>Upgrade</th><th>Why</th><th class="num">Added</th><th>Cost</th></tr></thead>
<tbody>
<tr><td>1 · Mud laundry entry</td><td>Today the garage door looks straight into the primary bedroom door 8 ft away. Entering through the laundry gives coats and shoes a real home, and the hall bench stays for keys and charging. The rated door moves 5 ft along the garage wall; the bays, built-ins and EV charger don't change.</td><td class="num">0 sf</td><td><span class="chip ok">Low</span></td></tr>
<tr><td>2 · Powder door on the hall</td><td>Guests reach the powder room through the office vestibule today. A 2'6" door on the hall fixes that, and the vestibule becomes the office's sound lock.</td><td class="num">0 sf</td><td><span class="chip ok">Low</span></td></tr>
<tr><td>3 · Daylight in the halls</td><td>Solar tubes or small skylights in the gallery hall and the bedroom hall, which get no daylight today.</td><td class="num">0 sf</td><td><span class="chip ok">Low</span></td></tr>
<tr><td>4 · Bigger dining room</td><td>Fits a table for 10, or a 72" round for 8. It costs about 5 ft of covered outdoor kitchen. Melissa's call.</td><td class="num">80 sf</td><td><span class="chip neu">Medium</span></td></tr>
<tr><td>5 · Guest suite targets</td><td>For Melissa's bedroom-wing redraw: a walk-in of about 50 sf per guest room, a private toilet room, a 60" or wider vanity, a hall about 42" clear, and daylight. Bedroom 2 is bigger than the primary bedroom today but has a 27 sf closet. The server room stays exactly where it is.</td><td class="num">0 sf</td><td><span class="chip neu">Targets only</span></td></tr>
</tbody></table></div>''')

M.append('''<h2 class="d-h2">Checked and ruled out</h2>
<ul class="d-list">
<li><b>Raising the great room walls to 14 ft.</b> The back slope would rise above the garage roof edge and create new valleys against the bonus room.</li>
<li><b>Moving the primary bedroom to the back for the pond view.</b> It shrinks the bath, puts the bedroom about 2 ft from the party terrace, and runs into the berm.</li>
<li><b>Everything you already decided against:</b> a living room fireplace, turning the island so the range isn't behind it, shrinking the garage, losing the server room, and a primary wet room. None of the options touch these.</li>
</ul>''')

M.append('<h2 class="d-h2">Decisions for you</h2>')
DEC = [('warn', 'Primary suite', 'A, B or C? I recommend B: 140 sf for a real closet and a zoned bath, with the simplest roof change.'),
       ('warn', 'Closet island', 'Will Melissa take a 7 × 2 ft drawer island this time? If not, a 7 ft bench goes in the same spot.'),
       ('warn', 'Living room ceiling', 'Change the flat 12 ft beamed ceiling to a cathedral of about 20\'6", keeping the beams every 4 ft? I recommend yes (G2).'),
       ('warn', 'Kitchen notch', 'Fill it and move the front water feature forward about 3 ft? I recommend yes.'),
       ('warn', 'Garage entry', 'Enter through the laundry instead of the hall? I recommend yes.'),
       ('warn', 'Dining', 'Grow it 5 ft for a table for 8 to 10? Optional, and Melissa\'s call.')]
M.append(''.join(f'<div class="d-panel {c}"><b>{a}</b><span>{b}</span></div>' for c, a, b in DEC))
M.append('<footer class="d-foot">Built on draft L (Oct 29, 2026). Five architect reviewers each looked at one area: the primary suite within the footprint, the primary suite expanded, the great room volume, the great room plan, and the whole house. A skeptic then checked each set against the drawing, the code minimums, the roof and your past decisions, and fixed or dropped what failed. Cost figures are rough and unverified. Room sizes are inside dimensions to wall centers.</footer>')

CSS = """
.pgrid{display:grid;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));gap:16px;margin:16px 0}
.pgrid.three{grid-template-columns:repeat(auto-fit,minmax(240px,1fr))}
.pf{margin:0;display:grid;gap:6px;cursor:zoom-in}
.pf figcaption{font-weight:600;color:var(--ink);font-size:15px}
.pf figcaption span{display:block;font-weight:400;color:var(--muted);font-size:14px}
.pf.rec .pl,.pf.rec .sec{outline:2px solid var(--accent);outline-offset:-1px}
.pf.big{grid-column:1/-1;cursor:zoom-out}
.d-list{margin:8px 0 16px;padding-left:20px;display:grid;gap:8px;color:var(--body)}
.d-h3{font-size:17px;margin:20px 0 6px;color:var(--ink)}
.sec{width:100%;height:auto;display:block;background:var(--surface);border:1px solid var(--rule);border-radius:4px}
.s-grade{stroke:var(--ink);stroke-width:2}
.s-roof{fill:none;stroke:var(--ink);stroke-width:4;stroke-linejoin:round}
.s-shed{fill:none;stroke:var(--muted);stroke-width:3}
.s-post{stroke:var(--muted);stroke-width:3}
.s-wall{fill:var(--ink)}
.s-glass{fill:var(--muted);opacity:.6}
.s-ceil{fill:none;stroke:var(--accent);stroke-width:2.5}
.s-beam{fill:var(--accent);opacity:.75}
.s-tie{stroke:var(--accent);stroke-width:4}
.s-man{fill:none;stroke:var(--muted);stroke-width:1.6}
.s-lab{fill:var(--muted);font-size:11px;text-anchor:middle;font-family:"Source Sans 3",system-ui,sans-serif}
.s-dim{fill:var(--ink);font-size:11.5px;text-anchor:middle;font-weight:600;font-family:"Source Sans 3",system-ui,sans-serif}
"""
JS = "<script>document.querySelectorAll('.pf').forEach(f=>f.addEventListener('click',()=>f.classList.toggle('big')));</script>"
out = page.wrap('Blueprint Study', '\n'.join(M) + JS, CSS)
open(sys.argv[1], 'w').write(out)
print(len(out))
