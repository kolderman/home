import json, sys
sys.path.insert(0, '/tmp/claude-0/work/study')
exec(open('pond_png.py').read().split("BASE =")[0].replace("S = json.load(open('/tmp/claude-0/work/study/pond-result.json'))['synth']\nC = {c['id']: c for c in S['concepts']}\nfor b in C['BEDROOM-FIRST']['erase']:\n    if b[1] == -2.5: b[1] = -2.8\n", ''))
W = {o['id']: o for o in json.load(open('wing-result.json'))['synth']['options']}
VB = (-6, 11, 31, 56)
style = style.replace('.card{width:1100px', '.card{width:1000px')
cards = [
 ('today', {}, 'Today (draft L)', 'For comparison', 'A dark 3 ft dog-leg hall off the living room, a 27 sf reach-in "walk-in" for bedroom 2, single sinks, and a 26 in shower in bath 3 that is under the 30 in code minimum.',
  [('Bedroom 2', '24\'0" × 13\'10"'), ('Closet 2', '27 sf reach-in'), ('Hall', '3 ft, no daylight'), ('Added', '—')]),
 ('g1', W['G1'], 'G1 · Guest foyer, same footprint', 'Recommended', 'The dark hall becomes a daylit foyer with a sealed door to the living room. Suite 2 gets a vestibule, a real walk-in and a 60 in vanity; bath 3 gets a code-legal 36 in shower and a 60 in vanity. The server room gets a sound wall.',
  [('Bedroom 2', '24\'0" × 13\'10", 2 window walls'), ('Closet 2', '42 sf walk-in'), ('Hall', '6\'6" daylit foyer'), ('Added', 'None')]),
 ('w4', W['W4'], 'W4 · West wall out 4 ft', 'Upgrade path', 'The west wall moves out 4 ft (+164 sf). Both rooms become full suites with dressing entries, private toilet rooms and bigger baths. Roughly $35-55k, the wing ridge rises 1 ft 4 in, and the side setback must be checked on the survey.',
  [('Bedroom 2', '21\'0" × 13\'2"'), ('Closet 2', '56 sf walk-in'), ('Bedroom 3', '21\'6" × 12\'4"'), ('Added', '164 sf')]),
 ('v1', W['V1'], 'V1 · Hotel suite plus flex room', 'Alternative', 'Suite 2 becomes a hotel-style suite with its own foyer, morning bar, walk-in, double vanity and private toilet. Bedroom 3 stays a simpler secondary room. Same footprint.',
  [('Bedroom 2', '17\'6" × 13\'10"'), ('Closet 2', '55 sf walk-in'), ('Bedroom 3', 'Unchanged'), ('Added', 'None')]),
]
for slug, opt, title, tag, sub, kv in cards:
    svg = P.render(VB, opt, title, show_pond=False)
    html = f'<!doctype html><html><head><meta charset="utf-8">{links}{style}</head><body><div class="card" id="c"><div class="tag">New home · Guest wing · {tag}</div><h1>{title}</h1><p class="sub">{sub}</p><div class="kv">' + \
        ''.join(f'<div><b>{a}</b><span>{b}</span></div>' for a, b in kv) + f'</div>{svg}<div class="foot"><span>Pond side at the top, street at the bottom. Garage and server room unchanged. One grid square = 2 ft.</span><span>Draft L · Oct 29, 2026</span></div></div></body></html>'
    open(f'wing-{slug}.html', 'w').write(html)
