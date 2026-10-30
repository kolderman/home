import json, sys, re
sys.path.insert(0, '/tmp/claude-0/work/study')
import plan_svg as P
S = json.load(open('/tmp/claude-0/work/study/pond-result.json'))['synth']
C = {c['id']: c for c in S['concepts']}
for b in C['BEDROOM-FIRST']['erase']:
    if b[1] == -2.5: b[1] = -2.8
T = open('/root/.claude/skills/synced/cc9f2c1b-608a-4e06-a091-ff5bdc1b22f3_d99a4251-bdde-4476-9656-a75eb0a5b2ff/house-styles/assets/ink-and-brass.html').read()
style = T[T.index('<style>', T.index('-->')):T.index('</style>') + 8].replace('</style>', P.CSS + '''
body{background:#fff}.card{width:1100px;padding:40px 48px;background:var(--bg);font-family:"Source Sans 3",system-ui,sans-serif}
.card h1{font:600 34px/1.15 "Source Serif 4",Georgia,serif;color:var(--ink);margin:0 0 6px}
.card .sub{color:var(--body);font-size:19px;margin:0 0 18px}
.card .kv{display:grid;grid-template-columns:repeat(4,1fr);gap:12px;margin:0 0 20px;border-top:1px solid var(--rule);border-bottom:1px solid var(--rule);padding:12px 0}
.card .kv b{display:block;color:var(--muted);font-size:13px;font-weight:600}.card .kv span{color:var(--ink);font-size:19px;font-weight:600}
.card .foot{display:flex;justify-content:space-between;color:var(--muted);font-size:14px;margin-top:12px;gap:20px}
.card .tag{color:var(--accent);font-weight:600;font-size:14px;margin-bottom:6px}
</style>''')
links = ''.join(re.findall(r'<link[^>]*>', T[T.index('-->'):]))
BASE = {'route': [[58.5, 48], [66, 37], [88.5, 36], [88.5, 31]]}
VB = (0, -42, 120, 52)
cards = [
 ('today', BASE, 'Today (draft L)', 'For comparison', 'The bedroom sits at the front of its wing and looks at the side porch. The way in is a narrow 4 ft service hall shared with the garage, laundry, stair and office.',
  [('Walk from the island', 'About 40 ft'), ('Hallway', '14½ ft'), ('Pond view from bed', 'None'), ('Added', '—')]),
 ('1-office-swap', C['OFFICE-SWAP'], 'Idea 1 · Bedroom takes the office spot', 'Recommended', 'The bedroom moves into today\'s office, right where the hall leaves the kitchen, with a 16 ft glass wall on a private garden. Melissa\'s bath and dressing room stay. The office moves into today\'s bedroom with the same couch, desk and TV.',
  [('Walk from the island', 'About 27 ft'), ('Hallway', 'About 2 ft'), ('Water from the sitting area', 'About 15 ft'), ('Added', 'None')]),
 ('2-pavilion', C['POND-PAVILION'], 'Idea 2 · Glass pavilion bedroom', 'Upgrade of idea 1', 'Like idea 1, but the bedroom pushes 7½ ft further toward the pond, with glass on two sides, entered through a dressing room. The old dressing room becomes his closet. Needs the new pond shape to keep its distance.',
  [('Walk from the island', 'About 34 ft'), ('Hallway', 'About 2 ft'), ('Water from the sitting area', 'About 13 ft'), ('Added', '135 sf')]),
 ('3-bedroom-first', C['BEDROOM-FIRST'], 'Idea 3 · Office stays: bedroom-first suite', 'If the office can\'t move', 'The bedroom becomes the first room you enter, a lounge and sleeping zone ending in a glass sitting bay on the pond. Closet and bath move to the side. The walk is today\'s, and the service hall stays.',
  [('Walk from the island', 'About 40 ft'), ('Hallway', '14½ ft (today\'s)'), ('Water from the sitting bay', 'About 17 ft'), ('Added', '346 sf')]),
 ('4-falls-view', C['FALLS-VIEW'], 'Idea 4 · Office stays: falls view from the bed', 'Best view, longest walk', 'The suite is rebuilt so the bed faces west through a glass corner to the waterfall. You enter through a skylit morning room. The only idea with the falls visible from the pillow.',
  [('Walk from the island', 'About 56 ft'), ('Hallway', '14½ ft (today\'s)'), ('Falls from the pillow', 'About 80 ft'), ('Added', '398 sf')]),
]
for slug, opt, title, tag, sub, kv in cards:
    svg = P.render(VB, opt, title, show_pond=True)
    html = f'<!doctype html><html><head><meta charset="utf-8">{links}{style}</head><body><div class="card" id="c"><div class="tag">New home · Primary bedroom on the pond · {tag}</div><h1>{title}</h1><p class="sub">{sub}</p><div class="kv">' + \
        ''.join(f'<div><b>{a}</b><span>{b}</span></div>' for a, b in kv) + f'</div>{svg}<div class="foot"><span>Pond side at the top. Dashed brass line: the walk from the kitchen island to the bedroom door. Grey water: today\'s pond, which is being reshaped. One grid square = 2 ft.</span><span>Draft L · Oct 29, 2026</span></div></div></body></html>'
    open(f'pond-{slug}.html', 'w').write(html)
print(' '.join(c[0] for c in cards))
