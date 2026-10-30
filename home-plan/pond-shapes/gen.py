import json, math
D = json.load(open('/tmp/claude-0/-home-claude/a0365b26-e317-5a40-a062-30aeb8882135/scratchpad/three/house.json'))
SHELL = D['shell']; PORCH = [p['p'] for p in D['porches']]; TERR = D['pond']['terr']; CUR = D['pond_c']['sw']

def spline(pts, n=14):
    out = []; m = len(pts)
    for i in range(m):
        p0, p1, p2, p3 = pts[(i-1)%m], pts[i], pts[(i+1)%m], pts[(i+2)%m]
        for k in range(n):
            t = k/n; t2=t*t; t3=t2*t
            x = .5*((2*p1[0])+(-p0[0]+p2[0])*t+(2*p0[0]-5*p1[0]+4*p2[0]-p3[0])*t2+(-p0[0]+3*p1[0]-3*p2[0]+p3[0])*t3)
            y = .5*((2*p1[1])+(-p0[1]+p2[1])*t+(2*p0[1]-5*p1[1]+4*p2[1]-p3[1])*t2+(-p0[1]+3*p1[1]-3*p2[1]+p3[1])*t3)
            out.append((x,y))
    return out
def area(poly):
    return abs(sum(poly[i][0]*poly[(i+1)%len(poly)][1]-poly[(i+1)%len(poly)][0]*poly[i][1] for i in range(len(poly))))/2
# view: plan x -> svg x, plan y -> svg y flipped. Window x -20..105, y -70..40
S = 9.0; X0, Y0 = -20, 38; HDR = 150
def P(x, y): return (round((x-X0)*S,1), round(HDR + (Y0-y)*S,1))
def path(poly, close=True):
    return 'M' + ' L'.join(f'{P(*p)[0]},{P(*p)[1]}' for p in poly) + (' Z' if close else '')
W, H = int(125*S), int(HDR + 102*S + 120)

SHAPES = []
def shape(name, blurb, water, wet=None, extras=None, bullets=()):
    SHAPES.append(dict(name=name, blurb=blurb, water=water, wet=wet, extras=extras or [], bullets=bullets))

# 1 kidney / bean: inner bend hugs the terrace, falls at the far end on the door axis
kid = spline([(8,-6),(22,-4),(38,-6),(52,-4),(66,-8),(76,-16),(74,-28),(62,-34),(48,-30),(38,-34),(26,-42),(14,-40),(6,-30),(4,-16)])
shape('Kidney', 'The classic Aquascape bean. The inner bend wraps the terrace, so the water feels close from the porch and the glass wall.',
      kid, wet=spline([(16,-42),(30,-44),(42,-50),(56,-48),(66,-40),(60,-36),(48,-33),(36,-36),(24,-44)]),
      extras=[('falls',(37.5,-35)),('beach',(10,-10)),('fire',(84,-30)),('jump',(70,-24))],
      bullets=('5 ft swim zone, 8 ft hole under the jump rock', 'Beach lagoon at the left, near the back porch', 'Wetland crescent and falls on the far shore, on the door axis'))
# 2 lagoon with island
lag = spline([(6,-4),(24,-2),(44,-4),(62,-2),(80,-8),(90,-22),(84,-38),(66,-48),(44,-50),(24,-46),(8,-36),(2,-20)])
isl = spline([(40,-22),(50,-20),(58,-26),(54,-34),(42,-34),(36,-28)])
shape('Lagoon with an island', 'One broad pool with a planted island in the middle, reached by stepping stones. Reads as a natural lake.',
      lag, wet=spline([(26,-48),(40,-54),(58,-54),(72,-50),(66,-44),(48,-46),(32,-46)]),
      extras=[('island',isl),('falls',(70,-44)),('beach',(8,-10)),('fire',(14,-50)),('stones',[(30,-8),(34,-14),(38,-20)])],
      bullets=('The biggest of the set, and the most to build', 'Island takes a specimen tree and the heron stand-off', 'Falls off-axis to the right, beach straight off the porch'))
# 3 bayou bend: crescent around a fire-pit peninsula
bay = spline([(4,-6),(20,-5),(36,-7),(52,-5),(68,-7),(82,-14),(88,-28),(80,-40),(66,-46),(56,-40),(52,-30),(44,-24),(34,-24),(26,-30),(22,-40),(12,-44),(2,-34),(0,-18)])
shape('Bayou bend', 'A crescent that wraps a peninsula with the fire pit on it, like a bend in a bayou. You cross to the fire on a stone causeway.',
      bay, wet=spline([(6,-46),(16,-52),(26,-48),(22,-42),(12,-44)]),
      extras=[('falls',(10,-42)),('beach',(70,-12)),('fire',(38,-36)),('cause',[(37.5,-8),(38,-24)]),('jump',(82,-30))],
      bullets=('The fire pit sits inside the water', 'Falls at the left end, on the lounge/bedroom side', 'Long swim run along the far arm'))
# 4 quarry: angular slabs, cliff jump, sheet falls
qua = [(6,-6),(30,-4),(48,-8),(64,-4),(80,-10),(84,-26),(72,-36),(58,-32),(46,-40),(30,-42),(14,-34),(4,-20)]
shape('Quarry', 'Straight slab edges and a stone cliff instead of soft curves. Modern, sharp, and it suits the glass wall.',
      qua, wet=[(30,-42),(46,-40),(52,-50),(26,-52),(16,-46)],
      extras=[('falls',(38,-41)),('cliff',[(58,-32),(72,-36),(74,-30)]),('fire',(88,-40)),('steps',(12,-12))],
      bullets=('Slab steps into the water straight off the terrace', 'Sheet falls off a cut-stone lip on the door axis', 'Cliff-jump rock on the right, 8 ft deep below it'))
# 5 two-pool cascade: upper soaking pool spilling into the main pond
mainp = spline([(8,-6),(24,-4),(40,-6),(56,-4),(70,-10),(76,-22),(66,-32),(50,-30),(36,-32),(22,-34),(10,-28),(4,-16)])
upper = spline([(32,-35),(44,-33),(52,-39),(46,-47),(34,-47),(28,-41)])
shape('Two-pool cascade', 'A smaller upper pool, warmer and still, spills over a wide lip into the swim pond. Two kinds of water in one view.',
      mainp, wet=spline([(54,-38),(68,-38),(76,-46),(64,-54),(52,-50),(50,-42)]),
      extras=[('pool',upper),('falls',(38,-33.5)),('beach',(10,-10)),('fire',(84,-28)),('jump',(68,-26))],
      bullets=('Plus a 400 sf upper pool that doubles as a soaking pool', 'Upper pool sits 3 ft higher: soak, read, watch the water go over', 'Wetland behind the upper pool feeds it'))
# 6 meandering creek: a river that winds across the back with a swim hole on the door axis
crk = spline([(-4,-8),(8,-6),(20,-10),(30,-8),(44,-6),(58,-10),(72,-8),(86,-14),(94,-26),(86,-34),(74,-28),(62,-30),(50,-36),(38,-38),(26,-32),(16,-30),(6,-34),(-6,-26)])
shape('Winding creek', 'A pond that reads as a slow creek. Narrow at the ends, it opens into a swim hole in front of the glass wall.',
      crk, wet=spline([(40,-42),(52,-40),(62,-46),(54,-54),(40,-54),(32,-48)]),
      extras=[('falls',(44,-39)),('fire',(0,-40)),('bridge',[(76,-6),(78,-30)]),('jump',(40,-34)),('beach',(16,-12))],
      bullets=('Less water than it looks, but 100 ft of shoreline', 'Stone bridge over the narrow right end', 'Fire pit at the far left end, across the tail'))

CSS = """<style>text{font-family:'Helvetica Neue',Arial,sans-serif;fill:#2b2a27} .h{font-size:34px;font-weight:700} .b{font-size:19px;fill:#4a4842} .l{font-size:15px;fill:#4a4842;letter-spacing:.04em;text-transform:uppercase} .t{font-size:14px;fill:#6b6862}</style>"""
def hatch(id_):
    return f'<pattern id="{id_}" width="6" height="6" patternUnits="userSpaceOnUse" patternTransform="rotate(45)"><line x1="0" y1="0" x2="0" y2="6" stroke="#6b8f5a" stroke-width="1.6"/></pattern>'

def draw(sh, i, full=True):
    g = [CSS, '<defs>', hatch('wet'), '</defs>', f'<rect width="{W}" height="{H}" fill="#fbfaf7"/>']
    # lawn grid
    for gx in range(X0, X0+126, 10): g.append(f'<line x1="{P(gx,0)[0]}" y1="0" x2="{P(gx,0)[0]}" y2="{H}" stroke="#eeece6"/>')
    for gy in range(-70, 41, 10): g.append(f'<line x1="0" y1="{P(0,gy)[1]}" x2="{W}" y2="{P(0,gy)[1]}" stroke="#eeece6"/>')
    g.append(f'<path d="{path(TERR)}" fill="#e2dfd6" stroke="#cfcbc0" stroke-width="1.5"/>')
    g.append(f'<path d="{path(SHELL)}" fill="#f1efe9" stroke="#8d897f" stroke-width="2.5"/>')
    for p in PORCH: g.append(f'<path d="{path(p)}" fill="#e8e3d6" stroke="#8d897f" stroke-width="1.2" stroke-dasharray="4 3"/>')
    # door axis + glass wall
    g.append(f'<line x1="{P(37.5,34)[0]}" y1="{P(37.5,34)[1]}" x2="{P(37.5,-70)[0]}" y2="{P(37.5,-70)[1]}" stroke="#b9b3a4" stroke-dasharray="6 5"/>')
    g.append(f'<line x1="{P(29.5,34)[0]}" y1="{P(29.5,34)[1]}" x2="{P(45.5,34)[0]}" y2="{P(45.5,34)[1]}" stroke="#2b2a27" stroke-width="4"/>')
    if sh['wet']: g.append(f'<path d="{path(sh["wet"])}" fill="url(#wet)" stroke="#6b8f5a" stroke-width="1.5"/>')
    g.append(f'<path d="{path(sh["water"])}" fill="#b9d6df" stroke="#3f7a8c" stroke-width="3"/>')
    g.append(f'<path d="{path(sh["water"])}" fill="none" stroke="#dcebf0" stroke-width="10" opacity=".6" transform="translate(0,0)"/>')
    g.append(f'<path d="{path(sh["water"])}" fill="none" stroke="#3f7a8c" stroke-width="3"/>')
    for k, v in sh['extras']:
        if k == 'island': g.append(f'<path d="{path(v)}" fill="#dfe6c8" stroke="#6b8f5a" stroke-width="2"/>'); g.append(f'<text class="t" x="{P(47,-27)[0]}" y="{P(47,-27)[1]}" text-anchor="middle">island</text>')
        elif k == 'pool': g.append(f'<path d="{path(v)}" fill="#cfe3ea" stroke="#3f7a8c" stroke-width="2.5"/>'); g.append(f'<text class="t" x="{P(40,-41)[0]}" y="{P(40,-41)[1]}" text-anchor="middle">upper pool</text>')
        elif k == 'falls': x,y=P(*v); g.append(f'<rect x="{x-24}" y="{y-4}" width="48" height="8" fill="#ffffff" stroke="#3f7a8c" stroke-width="2"/>'); g.append(f'<text class="t" x="{x}" y="{y-9}" text-anchor="middle">falls</text>')
        elif k == 'beach': x,y=P(*v); g.append(f'<circle cx="{x}" cy="{y}" r="22" fill="#efe3c6" stroke="#cdb98a"/>'); g.append(f'<text class="t" x="{x}" y="{y+5}" text-anchor="middle">beach</text>')
        elif k == 'fire': x,y=P(*v); g.append(f'<circle cx="{x}" cy="{y}" r="16" fill="#e6e2d6" stroke="#8d897f"/><circle cx="{x}" cy="{y}" r="5" fill="#d9772f"/>'); g.append(f'<text class="t" x="{x}" y="{y+30}" text-anchor="middle">fire pit</text>')
        elif k == 'jump': x,y=P(*v); g.append(f'<circle cx="{x}" cy="{y}" r="12" fill="#d4d0c6" stroke="#6b675d"/>'); g.append(f'<text class="t" x="{x+16}" y="{y+5}">jump rock</text>')
        elif k == 'cliff': g.append(f'<path d="{path(v, False)}" fill="none" stroke="#6b675d" stroke-width="7" stroke-linecap="round"/>'); x,y=P(66,-29); g.append(f'<text class="t" x="{x}" y="{y}" text-anchor="middle">cliff jump</text>')
        elif k == 'steps': x,y=P(*v); [g.append(f'<rect x="{x-14}" y="{y+j*7}" width="28" height="5" fill="#d4d0c6" stroke="#6b675d"/>') for j in range(3)]; g.append(f'<text class="t" x="{x}" y="{y-6}" text-anchor="middle">slab steps</text>')
        elif k in ('cause','bridge','stones'):
            if k == 'stones': [g.append(f'<circle cx="{P(*p)[0]}" cy="{P(*p)[1]}" r="6" fill="#d4d0c6" stroke="#6b675d"/>') for p in v]
            else: g.append(f'<path d="{path(v, False)}" fill="none" stroke="#d4d0c6" stroke-width="12" stroke-linecap="round"/><path d="{path(v, False)}" fill="none" stroke="#6b675d" stroke-width="1.5" stroke-dasharray="5 4"/>')
            x,y=P(*v[-1]); g.append(f'<text class="t" x="{x+10}" y="{y+5}">{ {"cause":"stone causeway","bridge":"stone bridge","stones":"stepping stones"}[k] }</text>')
    g.append(f'<text class="t" x="{P(37.5,36)[0]}" y="{P(37.5,36)[1]-4}" text-anchor="middle">16 ft glass wall and front-door axis</text>')
    g.append(f'<text class="t" x="{P(58,34)[0]+6}" y="{P(58,34)[1]+16}">house, draft K</text>')
    g.append(f'<text class="t" x="{P(50,14)[0]}" y="{P(50,14)[1]}" text-anchor="middle">terrace</text>')
    # scale bar 20 ft
    x,y=P(80,-62); g.append(f'<line x1="{x}" y1="{y}" x2="{x+20*S}" y2="{y}" stroke="#2b2a27" stroke-width="3"/><text class="t" x="{x}" y="{y+18}">20 ft</text>')
    g.append(f'<rect x="0" y="0" width="{W}" height="{HDR-8}" fill="#fbfaf7"/>')
    # title block
    a = area(sh['water']); g.append(f'<text class="h" x="30" y="52">{i}. {sh["name"]}</text>')
    g.append(f'<text class="l" x="30" y="80">about {int(round(a/100.0)*100):,} sf of water</text>')
    g.append(f'<line x1="30" y1="{HDR-14}" x2="{W-30}" y2="{HDR-14}" stroke="#d8d4c9"/>')
    g.append(f'<text class="b" x="30" y="108">{sh["blurb"][:95]}</text>' if len(sh['blurb'])<=95 else '')
    if len(sh['blurb'])>95:
        words=sh['blurb'].split(); l1=''; l2=''
        for w_ in words:
            if len(l1)<90 and not l2: l1+=w_+' '
            else: l2+=w_+' '
        g.append(f'<text class="b" x="30" y="108">{l1}</text><text class="b" x="30" y="132">{l2}</text>')
    yb = H-84
    for b in sh['bullets']: g.append(f'<text class="b" x="30" y="{yb}">•  {b}</text>'); yb += 26
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">' + ''.join(g) + '</svg>'

# current rev. D for reference
cur = dict(name='Current, rev. D (for comparison)', blurb='The long pond Melissa is not sold on.', water=CUR, wet=D['pond']['wl'], extras=[('falls',(37.5,-40)),('fire',(12.4,-46))], bullets=('The long pond with the falls on the door axis',))
html = ['<html><body style="margin:0;background:#fff">']
for i, sh in enumerate(SHAPES, 1):
    svg = draw(sh, i); open(f'shape-{i}.svg','w').write(svg); html.append(f'<div id="s{i}">{svg}</div>')
svg0 = draw(cur, 0); open('shape-0.svg','w').write(svg0); html.append(f'<div id="s0">{svg0}</div>')
html.append('</body></html>'); open('shapes.html','w').write(''.join(html))
print(W, H, [ (sh['name'], int(area(sh['water']))) for sh in SHAPES])
