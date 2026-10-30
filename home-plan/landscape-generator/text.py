def T(x, y, s, cls="lt"):
    return f'<text class="{cls}" x="{x}" y="{y}">{s}</text>'

def site_labels():
    L = [T(48, -16, "Rec pond"), T(62, -45, "Wetland filter", "lt2"), T(12.4, -55.4, "Fire pit"), T(62, 1.4, "Terrace"),
         T(42, -81.8, "Overlook", "lt2"), T(60, -90, "Cajun prairie (native meadow)", "lt2"), T(60, -110.6, "Native tree line: wax myrtle, holly, cypress", "lt2"), T(-14, -58.6, "Live oak", "lt2"), T(118, -56.6, "Live oak", "lt2"),
         T(118, -40, "Lawn"), T(100, -6.4, "Primary garden", "lt2"), T(134.8, 16.6, "Kitchen garden", "lt2"),
         T(124.6, 6, "Mower route", "lt2"), T(60, 74.6, "Front pond", "lt2"), T(93.5, 88, "Drive", "lt2"), T(60, 101.6, "Street", "lt2"),
         T(-4.4, 12.6, "Shade garden", "lt2"), T(37, -94.2, "Pool barrier, if the city requires one (dashed); the house wall closes it", "lt2"), T(120, -113.6, "Property continues on all sides", "lt2"),
         T(84, 2, "Shower", "lt2")]
    cap = ('<g class="cap"><text x="-32" y="-113.4">BACK ↑</text><text x="-32" y="102.6">FRONT: street ↓</text></g>'
           '<g class="scale"><rect x="110" y="98.6" width="10" height=".8"/><rect class="o" x="120" y="98.6" width="10" height=".8"/><rect x="130" y="98.6" width="20" height=".8"/>'
           '<text x="110" y="102.2">0</text><text x="120" y="102.2">10</text><text x="130" y="102.2">20</text><text x="146" y="102.2">40 ft</text></g>')
    return "".join(L) + cap

CALLOUTS = [(1, 62, -1.2), (2, 25.8, 2.8), (3, 42.8, -3.4), (4, 10.4, -1.2), (5, 1.4, -23.2), (6, -5.9, -21.8), (7, 60, -18.6), (8, 30.6, -25.2),
            (9, 23, -39.6), (10, 44.2, -40.4), (11, 39.1, -49.8), (12, 66, -37), (13, 77.6, -22.2), (14, 12.4, -38.4), (15, 42, -80.6), (16, 26.2, -61.8),
            (17, 83.8, -3.2), (18, 37.5, 10)]

def zoom_labels():
    co = "".join(f'<g class="co"><circle cx="{x}" cy="{y}" r="1.1"/><text x="{x}" y="{y + .42}">{n}</text></g>' for n, x, y in CALLOUTS)
    dep = T(48.6, -20.4, "5 ft", "dep") + T(21.4, -24.2, "8 ft", "dep") + T(72.4, -9.4, "2 ft", "dep") + T(11.6, -6.6, "0–18 in", "dep") + T(81.6, -15.2, "1 ft", "dep") + T(36.4, 2.4, "12 in", "dep")
    cap = ('<g class="scale"><rect x="-14" y="-80" width="5" height=".55"/><rect class="o" x="-9" y="-80" width="5" height=".55"/><rect x="-4" y="-80" width="10" height=".55"/>'
           '<text x="-14" y="-77.6">0</text><text x="-9" y="-77.6">5</text><text x="-4" y="-77.6">10</text><text x="4" y="-77.6">20 ft</text></g>')
    return co + dep + cap


def _xc(poly, x):
    ys = []
    for k in range(len(poly)):
        (x1, y1), (x2, y2) = poly[k], poly[(k + 1) % len(poly)]
        if (x1 - x) * (x2 - x) < 0:
            ys.append(y1 + (y2 - y1) * (x - x1) / (x2 - x1))
    return sorted(ys)


def section_svg():
    """Section on the axis (x = 37.5): sofa, glass wall, porch, terrace, sun ledge, lap lane, falls, wetland, back slope. Vertical x2."""
    import random, yard_d as D
    VE = 2.0; x = D.AXIS - .05; ey, ez = 46, 5.8   # just off the vertex at the falls notch          # sofa: plan y and seated eye height above the water
    U = lambda y: ey - y
    P = lambda y, z: f"{U(y):.2f},{-z * VE:.2f}"
    yb, yf = _xc(D.SW, x)[0], _xc(D.SW, x)[-1]
    led = _xc(D.LEDGE, x)
    wl_back = _xc(D.WL, x)[0]
    lip_y = -43.4
    pond = [(yf, 0), (yf, -1), (led[0], -1), (led[0] - 2.4, -2), (led[0] - 4.8, -3), (led[0] - 7.2, -4), (led[0] - 9, -5), (yb + 7, -5), (yb + 3.4, -2.2), (yb + 1, -1.2), (yb, 0)]
    back = [(yb - .6, 1.2), (lip_y + 1.2, 3.0), (lip_y, 3.5), (wl_back, 3.6), (wl_back - 4, 2.6), (wl_back - 14, 0), (-80, 0)]
    earth = [(60, .3), (20, .3)] + pond + back + [(-80, -12), (60, -12)]
    water = pond[:-1] + [(yb, 0)]
    grav = [(lip_y - .3, 3.4), (wl_back + .3, 3.4), (wl_back + .8, 1.5), (lip_y - .3, 1.5)]
    s = [f'<polygon points="{" ".join(P(y, z) for y, z in earth)}" fill="#D2BE98"/>', f'<polygon points="{" ".join(P(y, z) for y, z in water)}" fill="url(#swg)"/>',
         f'<polygon points="{" ".join(P(y, z) for y, z in grav)}" fill="url(#sgr)"/>',
         f'<polyline points="{" ".join(P(y, z - .18) for y, z in pond + back[:4])}" fill="none" stroke="#1F2328" stroke-width=".35"/>',
         f'<polyline points="{" ".join(P(y, z - .4) for y, z in pond)}" fill="none" stroke="#8E7A5C" stroke-width=".18" stroke-dasharray=".6 .35"/>']
    for k in range(4):
        s.append(f'<path d="M{U(lip_y) + .2:.2f},{-3.4 * VE:.2f} C{U(lip_y) - 1.4 - k * .2:.2f},{-2.8 * VE:.2f} {U(yb) - .6 - k * .2:.2f},{-1 * VE:.2f} {U(yb) - .6 - k * .25:.2f},0" fill="none" stroke="#fff" stroke-width=".3"/>')
    rg = random.Random(3); yy = lip_y - .8
    while yy > wl_back + .8:
        h = rg.uniform(1.6, 3.2)
        s.append(f'<path d="M{U(yy):.2f},{-3.4 * VE:.2f} l-.4,{-h * VE:.2f} M{U(yy):.2f},{-3.4 * VE:.2f} l.1,{-h * 1.1 * VE:.2f} M{U(yy):.2f},{-3.4 * VE:.2f} l.5,{-h * .9 * VE:.2f}" stroke="#5E8A4A" stroke-width=".22" fill="none"/>')
        yy -= rg.uniform(1.0, 1.8)
    # Centipede pipes under the upper tier
    s.append(f'<rect x="{U(lip_y - 1.2):.2f}" y="{-2.6 * VE:.2f}" width="{U(wl_back + 1) - U(lip_y - 1.2):.2f}" height=".7" rx=".35" fill="none" stroke="#2F3135" stroke-width=".16"/>')
    # house: living room, 10 ft glass wall, porch roof and post, terrace and coping
    s.append(f'<rect x="{U(46) - 6:.2f}" y="{-12 * VE:.2f}" width="{U(34) - U(46) + 6:.2f}" height="{10 * VE:.2f}" fill="#EFE6D4" stroke="#3A3F48" stroke-width=".3"/>')
    s.append(f'<line x1="{U(34):.2f}" x2="{U(34):.2f}" y1="{-12 * VE:.2f}" y2="{-2 * VE:.2f}" stroke="#7FB3C8" stroke-width=".9"/>')
    s.append(f'<polyline points="{P(34, 12.6)} {P(20, 10.6)}" fill="none" stroke="#3A3F48" stroke-width=".5"/>')
    s.append(f'<rect x="{U(34):.2f}" y="{-1.6 * VE:.2f}" width="{U(20) - U(34):.2f}" height="{1.3 * VE:.2f}" fill="#CFC6B6"/>')
    s.append(f'<rect x="{U(20):.2f}" y="{-.5 * VE:.2f}" width="{U(yf) - U(20):.2f}" height="{.5 * VE:.2f}" fill="#BFB29A"/><rect x="{U(yf) - .2:.2f}" y="{-.7 * VE:.2f}" width="1.6" height="{.7 * VE:.2f}" fill="#CFC6B6" stroke="#6E665A" stroke-width=".1"/>')
    for fy in (34, 20.5):
        s.append(f'<rect x="{U(fy) - .8:.2f}" y="{1.0 * VE:.2f}" width="1.6" height="{1.2 * VE:.2f}" fill="#9C9384"/>')
    s.append(f'<line x1="{U(20.5) + .8:.2f}" y1="{2.2 * VE:.2f}" x2="{U(20.5) + 9.4:.2f}" y2="{10.8 * VE:.2f}" stroke="#7A2E2E" stroke-width=".25" stroke-dasharray=".8 .5"/>')
    s.append(f'<line x1="{U(20.5):.2f}" x2="{U(20.5):.2f}" y1="{-10.6 * VE:.2f}" y2="{-1.6 * VE:.2f}" stroke="#3A3F48" stroke-width=".3"/>')
    # pump vault and return line, drawn schematically below grade
    s.append(f'<path d="M{U(yb) + 2:.2f},{9.4 * VE:.2f} L{U(lip_y - 2):.2f},{9.4 * VE:.2f} L{U(lip_y - 2):.2f},{-2.4 * VE:.2f}" fill="none" stroke="#2F6F8C" stroke-width=".28" stroke-dasharray=".8 .4"/>')
    # sight line from the sofa, through the glass, to the falls lip
    slope = (3.5 - ez) / U(lip_y); far = -80
    s.append(f'<line x1="0" y1="{-ez * VE:.2f}" x2="{U(far):.2f}" y2="{-(ez + slope * U(far)) * VE:.2f}" stroke="#B0812A" stroke-width=".3" stroke-dasharray="1.2 .7"/><circle cx="0" cy="{-ez * VE:.2f}" r=".8" fill="#B0812A"/>')
    T_ = lambda u, z, txt, a="middle", c="sn": f'<text class="{c}" x="{u:.2f}" y="{-z * VE:.2f}" style="text-anchor:{a}">{txt}</text>'
    nt = lambda y, z, dz, txt: f'<line x1="{U(y):.2f}" x2="{U(y):.2f}" y1="{-(z + .3) * VE:.2f}" y2="{-(z + dz - .6) * VE:.2f}" stroke="#3A3F48" stroke-width=".15"/>' + T_(U(y), z + dz, txt)
    s += [T_(1.4, ez + 1.6, "Sofa, looking through the glass wall", "start"), T_(U(27), -2.2, "Porch"), T_(U(12), -2.2, "Terrace and coping"),
          nt(led[0] + .8, -.8, -3.6, "Sun ledge, 12″"), nt(led[0] - 4.8, -2.8, -3.4, "Slab steps"),
          T_(U((yf + yb) / 2 - 7), -3.6, "Lap lane, 5 ft"), nt(lip_y, 3.5, 4.4, "Falls, 3½′ drop"), nt((lip_y + wl_back) / 2, 3.4, 7.8, "Wetland upper tier"),
          nt(wl_back - 9, 1.4, 4.2, "Back slope from pond spoil"), T_(U(-68), -10.6, "Return line from the pumps to the Centipede pipes under the wetland", "end"),
          T_(U(20.5) + 10, -11.4, "1:1 line from the porch footing: the dig stays outside it", "start"),
          T_(-5, -12.6, "SECTION ON THE AXIS (x = 37½ ft) · VERTICAL SCALE 2×", "start", "sn")]
    w = U(-70) + 4
    return (f'<svg class="plan ls sec" viewBox="-6 {-14 * VE} {w + 2:.1f} {27 * VE + 2}" role="img" aria-label="Section on the axis from the sofa through the glass wall, porch, terrace, sun ledge, lap lane, falls and wetland to the back slope">'
            f'<rect x="-6" y="{-14 * VE}" width="{w + 2:.1f}" height="{27 * VE + 2}" fill="#FBF8F1"/>'
            '<defs><pattern id="sgr" width="1.2" height="1.2" patternUnits="userSpaceOnUse"><rect width="1.2" height="1.2" fill="#D9CDB3"/><circle cx=".3" cy=".4" r=".16" fill="#A3967D"/><circle cx=".9" cy=".9" r=".14" fill="#EEE7D7"/></pattern>'
            '<linearGradient id="swg" x1="0" x2="0" y1="0" y2="1"><stop offset="0" stop-color="#9FCFDF"/><stop offset="1" stop-color="#3F7F9C"/></linearGradient></defs>'
            + "".join(s) + '</svg>')

def flow_svg():
    steps = [("Intake bay", "Skims leaves and debris", "off the surface"), ("External pumps", "About one turnover an hour,", "IonGen and dosing inline"),
             ("Wetland filter", "Water rises through gravel", "and plant roots"), ("Falls + lip", "Over the 7 ft falls and", "a 36 ft sheeting lip"),
             ("Swim zone", "Jets and the far-side intake", "keep it circulating")]
    s = ['<svg class="flow" viewBox="0 0 100 19" role="img" aria-label="Water loop: intake bay, external pumps, wetland filter, waterfall and wetland lip, swim zone, back to the intake bay.">']
    for i, (a, b, c) in enumerate(steps):
        x = 1 + i * 20
        s.append(f'<rect x="{x}" y="1" width="16.6" height="11" rx="1.2" fill="var(--surface,#FBF8F1)" stroke="#8A6A2F" stroke-width=".22"/>'
                 f'<text x="{x + 8.3}" y="4.6" text-anchor="middle" font-size="1.75" font-weight="700" fill="currentColor">{a}</text>'
                 f'<text x="{x + 8.3}" y="7.6" text-anchor="middle" font-size="1.3" fill="currentColor" opacity=".8">{b}</text>'
                 f'<text x="{x + 8.3}" y="9.6" text-anchor="middle" font-size="1.3" fill="currentColor" opacity=".8">{c}</text>')
        if i < 4:
            s.append(f'<path d="M{x + 17},6.5 L{x + 19.6},6.5 M{x + 18.8},5.7 L{x + 19.6},6.5 L{x + 18.8},7.3" stroke="#8A6A2F" stroke-width=".3" fill="none"/>')
    s.append('<path d="M89.3,12.2 L89.3,16.4 L9.3,16.4 L9.3,12.6 M8.5,13.4 L9.3,12.4 L10.1,13.4" stroke="#8A6A2F" stroke-width=".3" fill="none" stroke-dasharray=".9 .5"/>')
    s.append('<text x="49.3" y="18.4" text-anchor="middle" font-size="1.3" fill="currentColor" opacity=".75">across the pond, back to the intake bay</text></svg>')
    return "".join(s)


KEY = ["Flagstone terrace from the back porch to the water, ending in cut stone coping",
       "Sun ledge, 12 in deep, in front of the back porch: chaises sit in the water",
       "Slab steps: three wide stones from the ledge down into the lap lane",
       "Beach entry at the left end: pea gravel sloping to about 18 in, for kids and easy wading",
       "Intake bay (skim cove) in the far-left corner: the pumps draw from here, away from the beach and swimmers",
       "Pump vault past the bedroom wing: external pumps, IonGen and controls, screened by shrubs",
       "Lap lane, about 5 ft deep and close to 70 ft long",
       "Deep zone, about 8 ft, under the jump rock",
       "Jump rock: a flat slab set tight to the bank, with nothing sticking out below it",
       "Main waterfall, 7 ft wide with about a 3½ ft drop, on the axis from the front doors",
       "Wetland upper tier, about 3½ ft up, which feeds the falls",
       "Lower tier and lip: water sheets over low stone along the far shore, planted with iris, rush and pickerelweed",
       "Lily cove at the right end, where the rill comes in, out of the swim lane",
       "Fire pit across the water: six chairs looking back at the house, with the falls beside them",
       "Overlook bench on the back slope",
       "Stepping-stone loop behind the wetland, from the fire pit to a bench at the right end",
       "Outdoor rinse shower by the primary bath",
       "The axis: front doors, glass wall, sun ledge and falls on one line"]

def body(Y, site, zoom, sec, flow):
    from geo import area
    terr = area(Y.TERRACE)
    key = "".join(f"<li>{k}</li>" for k in KEY)
    return f"""<main class="doc">
  <header class="d-head">
    <div class="d-top"><span class="d-type">New home build</span><span class="d-date">Landscape concept, rev. D · Oct 26, 2026</span></div>
    <h1 class="d-title">Landscape plan and rec pond</h1>
    <p class="d-lead">A natural swimming pond in the style of Greg Wittstock and Aquascape is the centerpiece of the back yard. There's no chlorine: a planted wetland filters the water and spills back in over a waterfall. The pond runs along the back of the house, so the terrace ends at the water. Around it are a sun ledge, a beach, a fire pit across the water and a loop path, with gardens and a small pond out front. This revision is tuned for Youngsville, Louisiana: zone 9a plants, the water table, heavy rain, long summers and an open, flat property.</p>
  </header>

  <div class="d-stats">
    <div><div class="l">Pond surface</div><div class="v">~{Y.A_SW:,.0f} sf</div><div class="s">about 80 ft long, 0 to 8 ft deep</div></div>
    <div><div class="l">Wetland filter</div><div class="v">~{Y.A_WL:,.0f} sf</div><div class="s">{Y.A_WL / Y.A_SW:.0%} of the pond; the rule of thumb is 30% or more</div></div>
    <div><div class="l">Water</div><div class="v">~{round(Y.GAL, -3):,.0f} gal</div><div class="s">turned over about once an hour</div></div>
  </div>

  <div class="d-call"><b>New in rev. D</b><span>The long pond you picked replaces the round one. It runs across the back of the house, so the terrace ends in stone coping at the water, with a 12 in sun ledge in front of the porch and a lap lane close to 70 ft long. The deck is gone. The wetland crescent from rev. C moves to the far shore. The falls also moved 3½ ft left, so it sits on the line from the front doors through the new glass wall. See the <a href="long-pond-option.html">long pond option</a> for the comparison with rev. C.</span></div>
  <div class="d-call"><b>What changed with Youngsville</b><span>The plants are now south Louisiana natives and proven zone 9a choices. The pond gets a sub-liner drain and a raised rim for the water table and the rain. The back opens onto native Cajun prairie instead of a lot line. Costs rise a little, because every boulder has to be trucked in. North is still unknown.</span></div>

  <h2 class="d-h2">Site plan</h2>
  <p class="d-note">The yard around the house, with the draft K floor plan in place. The back of the house (pond side) is at the top. The property runs on past every edge of this drawing.</p>
  <figure class="d-fig wide">{site}</figure>

  <h2 class="d-h2">The rec pond</h2>
  <p class="d-p">The pond sits on the house's main axis. From the front doors you look through the living room and the new glass wall, across the porch and the sun ledge, down the water to the falls. The near shore is for getting in: stone coping, the sun ledge with steps into the lap lane, and a beach at the left end. The far shore is for show: the wetland garden runs along the back as its upper shore, with the falls on the axis and a stone lip sheeting water in along the right half. The intake bay hides in the far-left corner, and the lily cove sits at the right end where the rill comes in.</p>
  <figure class="d-fig wide">{zoom}</figure>
  <ol class="d-key">{key}</ol>

  <h2 class="d-h2">How the water stays clean</h2>
  <p class="d-p">This is the Aquascape recipe: an ecosystem, not a pool. Pumps pull water from the intake bay in the far-left corner and push it under the wetland along the far shore. It rises up through the gravel, where bacteria and plant roots strip out the nutrients algae feed on. Then it pours back in over the waterfall and sheets over the wetland's stone lip along the right half. Water enters across the far shore and leaves at the far-left corner, so the whole lap lane moves, right to left. Frogs and dragonflies will show up, and the water gets better with age. Expect a year or two before the wetland fills in.</p>
  {flow}

  <h2 class="d-h2">Section through the pond</h2>
  <p class="d-note">Cut on the axis, from the sofa through the glass wall to the back slope. The 8 ft deep zone is off to the left of this line, under the jump rock.</p>
  <figure class="d-fig wide">{sec}</figure>

  <h2 class="d-h2">Around the pond</h2>
  <dl class="d-rows">
    <dt>Terrace</dt><dd>About {round(terr, -2):,.0f} sf of irregular flagstone, stepping down from the back porch and the outdoor kitchen to cut stone coping at the water's edge. An umbrella table sits off the outdoor kitchen, and pots keep it from feeling like a parking lot.</dd>
    <dt>Getting in</dt><dd>Little kids wade in from the beach at the left end. Adults sit on the 12 in sun ledge in front of the porch, where the chaises stand in the water, and walk down the slab steps into the lap lane. Swimmers jump off the jump rock into the deep end. The jump rock is one big flat slab, and the boulders near it are set back so nothing sits under a jumper. The deep water stays out in the middle, well away from the house walls.</dd>
    <dt>Waterfall</dt><dd>The 7 ft wide falls drop about 3½ ft out of the wetland's upper tier into a small bay on the axis, framed by the two largest boulders on the job. Japanese maples on either side frame it from the house.</dd>
    <dt>Wetland</dt><dd>It's the pond's far shore, not a separate bed. A long crescent of planted gravel runs from just past the jump rock to the lily cove, separated from the water by a 1 ft stone lip. The upper tier, about 3½ ft up, feeds the falls. The lower tier, about 1 ft up, runs along the right half. The land behind it rises on a long, low slope built from the soil dug out of the pond and runs back into the meadow, so it reads as landform rather than a mound. It is the filter, so it stays full size: Aquascape builders say not to shrink the wetland to save money.</dd>
    <dt>Wetland lip</dt><dd>Water from the lower tier sheets over about {Y.LIP_FT:.0f} ft of low, flat stone into the pond, then runs down a short rill into the lily cove. It adds a quieter sound than the falls and keeps the right end moving. A valve on each tier's pipe balances the falls against the lip, and turns the falls down at night for bedroom 2.</dd>
    <dt>Fire pit</dt><dd>A gravel circle with a gas or wood fire pit and six chairs, across the water on the far-left shore. You sit with the falls beside you and look back at the house over the pond. You reach it by stepping stones around the beach end.</dd>
    <dt>Loop path</dt><dd>Flat stepping stones run from the terrace around the beach end to the fire pit, then behind the wetland to the overlook bench, and on to a second bench at the right end looking at the lip.</dd>
    <dt>Lighting</dt><dd>Lights sit under the falls, in the lap lane and deep zone, on the sun ledge, in the wetland and in the front pond. Uplights on the maples and low path lights finish it. The yellow dots on the plans mark them.</dd>
    <dt>Beyond the pond</dt><dd>Behind the pond the yard turns into Cajun prairie, the native tallgrass meadow of Acadiana, mowed once a year with a mown path through it. A loose tree line of wax myrtle, holly and bald cypress closes the view. Live oaks shade the fire pit side and the lawn. All the big trees stay at least 25 ft from the water to keep leaves out.</dd>
    <dt>Lawn</dt><dd>St. Augustine or zoysia. The open lawn is on the right, behind the office and primary suite, for play. The mower comes out of the garage's side roll-up door onto a paver apron, then up a gravel path to the back lawn.</dd>
    <dt>Primary garden</dt><dd>A hedged moss-and-gravel garden behind the primary bath, lined up on the tub window. It has a basalt-column bubbler, a Japanese maple and a bench. You reach it from the side porch.</dd>
    <dt>Outdoor shower</dt><dd>A cedar rinse shower sits in the corner where the office and primary bath walls meet, plumbed from the primary bath.</dd>
    <dt>Kitchen garden</dt><dd>Six raised beds inside a low fence by the garage side door, close to the kitchen and outside the pond area. It's optional.</dd>
  </dl>

  <h2 class="d-h2">Front yard</h2>
  <dl class="d-rows">
    <dt>Front pond</dt><dd>The water feature by the front porch becomes a small Aquascape ecosystem pond, about 11' × 7', with a boulder spill on the pantry side. You see it from the porch chairs and from the kitchen sink window above it. A flat stone off the end of the porch is the spot to sit and watch the fish.</dd>
    <dt>Walk</dt><dd>A flagstone walk curves from the front steps to the drive, so guests who park don't cut across the lawn.</dd>
    <dt>Beds and trees</dt><dd>Low beds run along the lounge, porch and pantry fronts. There are two shade trees in the lawn, flowering trees at the lounge corner and by the drive, and a bed on the garage's side wall.</dd>
    <dt>Left side</dt><dd>A shade garden of ferns and hostas runs along the bedroom wing, with a stepping-stone path from the front yard past the pump vault to the fire pit.</dd>
  </dl>

  <h2 class="d-h2">Building it in Youngsville</h2>
  <dl class="d-rows">
    <dt>Foundation</dt><dd>With the water this close, the porch footings set how near the deep water can come. The 5 ft zone stays outside a 45° line down from the porch footing (red dashed line in the section). A structural engineer should design the porch slab, the coping and the pond edge together, with drainage away from the slab.</dd>
    <dt>Water table</dt><dd>South Louisiana's groundwater sits high, and a pond liner with water under it can float up in "whales." Plan on a sub-liner drain with a sump and a vent, and get a soil boring before digging. The clay-heavy soil holds the shape well once it's drained.</dd>
    <dt>Rain and flooding</dt><dd>The rim sits a few inches above the surrounding grade, with a shallow swale around it, so lawn runoff and fertilizer stay out of the pond. The overflow is sized for 10 inch rain events. Check the FEMA flood zone for the pond site as well as the house.</dd>
    <dt>Heat</dt><dd>Summer water will reach the upper 80s. The 8 ft deep zone stays cooler, aeration runs all summer, and the falls and lip add oxygen. Shade from the maples and live oaks on the afternoon side helps once north is known. Tropical water lilies love it.</dd>
    <dt>Year-round</dt><dd>There's no winter shutdown, so the pumps run 12 months and the growing season, and the algae season, are long. The wetland and IonGen carry that load.</dd>
    <dt>Mosquitoes and wildlife</dt><dd>Moving water and fish keep mosquitoes out, so fish are close to a must here. Cottonmouths visit any Louisiana pond with frogs, so keep the beach and step edges clear of tall plants.</dd>
    <dt>Hurricanes</dt><dd>Put the pumps and aeration on the house generator, because stagnant warm water turns fast without power. Plan to skim storm debris and bring in the ledge and terrace furniture.</dd>
    <dt>Stone</dt><dd>South Louisiana has no native rock, so every boulder and all the gravel come in by truck, usually from Arkansas, Oklahoma or the Texas Hill Country. Pick one stone type, such as Arkansas fieldstone or Texas moss rock, so it reads as natural.</dd>
  </dl>

  <h2 class="d-h2">Planting palette</h2>
  <p class="d-note">USDA zone 9a, Lafayette Parish. Louisiana natives first, with a few proven garden plants.</p>
  <div class="d-tw"><table>
    <thead><tr><th>Where</th><th>Plants</th><th>Why</th></tr></thead>
    <tbody>
      <tr><td>Wetland filter</td><td>Louisiana iris, pickerelweed, swamp lily, golden canna, soft rush, duck potato, lizard's tail; American water willow along the lip; scarlet swamp hibiscus and cardinal flower on the back edge</td><td>Native to Acadiana's marshes; their roots do the filtering, and something blooms spring to fall</td></tr>
      <tr><td>Lily cove and shelves</td><td>Hardy and tropical water lilies, American lotus in a sunk pot, water clover, water hyssop</td><td>Shade the water against algae, kept out of the swim lanes</td></tr>
      <tr><td>Between the boulders</td><td>Gulf muhly, dwarf palmetto, Louisiana phlox, swamp milkweed, sedges, black-eyed Susan</td><td>Take the heat and wet feet; muhly turns pink in fall</td></tr>
      <tr><td>Feature trees</td><td>Weeping Japanese maple in afternoon shade, a second maple or a weeping yaupon by the falls, river birch clump behind the wetland</td><td>Color and form near the water with small leaves</td></tr>
      <tr><td>Shade trees</td><td>Live oak, swamp red maple, bald cypress kept well back from the water</td><td>Long-lived natives for shade and scale</td></tr>
      <tr><td>Shade garden</td><td>Cast iron plant, holly fern, autumn fern, oakleaf hydrangea, ginger lily</td><td>Thrive on the house's shady side in the humidity</td></tr>
      <tr><td>Cajun prairie</td><td>Little bluestem, switchgrass, Indiangrass, rattlesnake master, purple coneflower, swamp sunflower</td><td>Restores the native tallgrass prairie; pollinators and one mowing a year</td></tr>
      <tr><td>Tree line</td><td>Wax myrtle, Savannah holly, yaupon, southern magnolia</td><td>Evergreen and storm-tough</td></tr>
      <tr><td>Primary garden</td><td>Podocarpus or Japanese boxwood hedge, mondo grass instead of moss, a Japanese maple, cast iron plant</td><td>Calm and green from the tub window, and it holds up in the heat</td></tr>
    </tbody>
  </table></div>

  <h2 class="d-h2">Pond equipment</h2>
  <div class="d-tw"><table>
    <thead><tr><th>Part</th><th>What it does</th></tr></thead>
    <tbody>
      <tr><td>Intake bay</td><td>A rock-and-gravel cove where the pumps draw water. It catches leaves and keeps suction away from swimmers.</td></tr>
      <tr><td>External pumps in a vault</td><td>Recommended over submersible pumps when people swim. Sized for about one turnover an hour, around 66,000 gallons an hour across four or five pumps.</td></tr>
      <tr><td>Wetland filter with Centipede modules</td><td>Perforated pipes under the gravel spread the water so it rises evenly through the whole bed.</td></tr>
      <tr><td>IonGen G2 and Smart Pond Dosing</td><td>Algae control and automatic water treatment, both part of Aquascape's recreational pond kit.</td></tr>
      <tr><td>Jets and aeration</td><td>Keep the deep water from going stagnant.</td></tr>
      <tr><td>45 mil EPDM liner</td><td>A fish-safe rubber liner on geotextile underlayment, with rock pad under the boulders.</td></tr>
      <tr><td>Auto-fill and overflow</td><td>Tops up evaporation and sends storm water somewhere safe.</td></tr>
      <tr><td>Sub-liner drain and vent</td><td>Expected in Youngsville because of the high water table. It keeps groundwater from lifting the liner.</td></tr>
      <tr><td>Generator circuit</td><td>Keeps pumps and aeration running through hurricane outages.</td></tr>
    </tbody>
  </table></div>

  <h2 class="d-h2">Rough budget</h2>
  <p class="d-note">Rough, checked against real prices on Oct 26, 2026. A Texas builder starts a 50' × 70' swim pond with wetland at <a href="https://thenaturalswimmingpond.com/natural-swim-pond-prices">$130,000</a>, including the dig, liner and equipment. Cost guides put natural pools at <a href="https://www.angi.com/articles/natural-pool-cost.htm">$50–$100 per sq ft</a>, cheaper per foot as they get bigger. This pond plus its wetland is about 3,400 sq ft, so it lands around $130k–$210k once you add boulders, falls, coping, lights and trucking stone into south Louisiana. The pumps, vault and design don't grow with the size; mostly the dig, liner and stone do. Rev. B's $175k–$260k scaled up a small pond's starting price, which overcounted the fixed setup. Flagstone runs about <a href="https://www.homeadvisor.com/cost/outdoor-living/install-flagstone-patio/">$15–$30 per sq ft</a> installed, and landscape lights about <a href="https://www.lawnstarter.com/blog/cost/landscape-lighting-price/">$100–$150 each</a>. The planting, gardens and front pond lines haven't been checked against outside prices yet.</p>
  <div class="d-tw"><table>
    <thead><tr><th>Item</th><th class="num">Range</th></tr></thead>
    <tbody>
      <tr><td>Rec pond, sun ledge, wetland, waterfall, lip and rill, equipment, pond lights</td><td class="num">$130k–$210k</td></tr>
      <tr><td>Flagstone terrace and coping, walk, fire pit circle, stepping stones</td><td class="num">$35k–$70k</td></tr>
      <tr><td>Front ecosystem pond</td><td class="num">$10k–$18k</td></tr>
      <tr><td>Trees, beds, meadow, lawn, irrigation</td><td class="num">$40k–$75k</td></tr>
      <tr><td>Primary garden, outdoor shower, kitchen garden</td><td class="num">$15k–$30k</td></tr>
      <tr><td>Landscape lighting outside the ponds (about 30 fixtures)</td><td class="num">$4k–$10k</td></tr>
      <tr><td>Pond circuit on the house's standby generator</td><td class="num">$1k–$3k</td></tr>
      <tr><td><b>All of it</b></td><td class="num"><b>$235k–$416k</b></td></tr>
    </tbody>
  </table></div>

  <h2 class="d-h2">Open questions</h2>
  <ol class="d-q">
    <li><b>Fish.</b> Koi, native fish like bluegill and mosquitofish, or both? Some fish are close to a must here for mosquitoes.</li>
    <li><b>North.</b> It decides where afternoon shade falls and whether the fire pit should swap sides.</li>
    <li><b>Pool rules.</b> Louisiana's statewide code points to the International Swimming Pool and Spa Code, which asks for a 4 ft barrier around water over 24 in deep. Whether a natural pond counts is the City of Youngsville's call, so ask the permit office early. With the water this close to the porch, the house's back wall becomes part of the barrier, which usually means alarms or self-closing, self-latching hardware on the glass wall, porch door and dining doors. The dashed line shows the fence that closes the rest, with gates.</li>
    <li><b>Flood zone.</b> Do you know the FEMA zone for the back of the property? It affects how high the pond rim and the wetland sit.</li>
  </ol>

  <footer class="d-foot">Concept plan, not a construction drawing. Pond sizing follows published Aquascape guidance: wetland at least 30% of the pond, 4 to 8 ft swim depths, external pumps and a skim cove for swim ponds, and one to two turnovers an hour. Sources: <a href="https://www.pondtrademag.com/demystifying-recreation-ponds-for-clients/">Demystifying Recreation Ponds for Clients</a>, <a href="https://www.pondtrademag.com/overcoming-the-challenges-of-building-a-recreational-pond/">Overcoming the Challenges of Building a Recreational Pond</a>, <a href="https://www.pondtrademag.com/vegas-east-a-backyard-oasis-like-no-other/">Vegas East</a> (Pond Trade Magazine), and <a href="https://www.aquascapeinc.com/products/recreational-pond-kit-9x20">Aquascape's recreational pond kit</a>.</footer>
</main>"""
