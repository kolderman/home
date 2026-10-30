import json, sys, re
sys.path.insert(0, '/tmp/claude-0/work/study')
import plan_svg as P
exec(open('build.py').read().split("VB_P, VB_G")[0])   # reuse OPT and label fixes
T = open('/root/.claude/skills/synced/cc9f2c1b-608a-4e06-a091-ff5bdc1b22f3_d99a4251-bdde-4476-9656-a75eb0a5b2ff/house-styles/assets/ink-and-brass.html').read()
style = T[T.index('<style>', T.index('-->')):T.index('</style>') + 8].replace('</style>', P.CSS + '''
body{background:#fff}.card{width:1100px;padding:40px 48px;background:var(--bg);font-family:"Source Sans 3",system-ui,sans-serif}
.card h1{font:600 34px/1.15 "Source Serif 4",Georgia,serif;color:var(--ink);margin:0 0 6px}
.card .sub{color:var(--body);font-size:19px;margin:0 0 18px}
.card .kv{display:grid;grid-template-columns:repeat(4,1fr);gap:12px;margin:0 0 20px;border-top:1px solid var(--rule);border-bottom:1px solid var(--rule);padding:12px 0}
.card .kv b{display:block;color:var(--muted);font-size:13px;font-weight:600}.card .kv span{color:var(--ink);font-size:19px;font-weight:600}
.card .pl{max-height:1500px}.card .foot{display:flex;justify-content:space-between;color:var(--muted);font-size:14px;margin-top:12px}
.card .tag{color:var(--accent);font-weight:600;font-size:14px;margin-bottom:6px}
.pl-fl{font-size:inherit}
</style>''')
links = ''.join(re.findall(r'<link[^>]*>', T[T.index('-->'):]))
VB = (82, -12, 114, 42)
LY = {'A': {'Primary closet': 12.5, 'Primary bedroom': 28}, 'B': {'Primary closet / dressing': 6.6, 'Primary bedroom (unchanged)': 27.5},
      'C': {'Her closet': 6.4, 'Primary bedroom (unchanged walls)': 27.5}}
for k, m in LY.items():
    for r in OPT[k]['rooms']:
        if r['name'] in m: r['ly'] = m[r['name']]
        if r['name'] == 'Primary closet / dressing': r['name'] = 'Primary closet'
cards = [
 ('draft-l', None, 'Current plan (draft L)', 'Primary suite as drawn today', 'Bath, closet and bedroom are three full-width strips. The closet is a corridor with a 3\'7" aisle.',
  [('Closet', '20\' × 8\' · 160 sf'), ('Bath', '20\' × 10\'6" · 210 sf'), ('Bedroom', '20\' × 16\''), ('Added', 'None')]),
 ('option-a', 'A', 'Option A · Same footprint', 'Closet and bath side by side', 'No added space. Better room shapes: a 5\'7" closet aisle, facing vanities, a bigger shower, a private toilet room.',
  [('Closet', '10\' × 19\'6" · 195 sf'), ('Bath', '10\' × 19\'6" · 195 sf'), ('Bedroom', '20\' × 15\''), ('Added', 'None')]),
 ('option-b', 'B', 'Option B · Push the back wall out 7 ft', 'Recommended', 'A real closet room with a drawer island and 42" aisles. A zoned bath with a freestanding tub, a 6\' × 7\' shower and a private toilet room.',
  [('Closet', '20\' × 13\'6" · 270 sf'), ('Bath', '20\' × 12\' · 240 sf'), ('Bedroom', '20\' × 16\' (same)'), ('Added', '140 sf')]),
 ('option-c', 'C', 'Option C · Full luxury, 6 ft wider', 'His and her closets', 'Separate closets, a coffee bar at the suite entrance, a 26\' × 12\' bath with an 8\' × 6\' shower. The side porch loses its open back end.',
  [('Closets', '12\' × 13\'6" + 9\' × 13\'6"'), ('Bath', '26\' × 12\' · 312 sf'), ('Bedroom', '20\' × 16\' (same)'), ('Added', '293 sf')]),
]
for slug, key, title, tag, sub, kv in cards:
    svg = P.render(VB, OPT[key] if key else None, title)
    html = f'<!doctype html><html><head><meta charset="utf-8">{links}{style}</head><body><div class="card" id="c"><div class="tag">New home · Primary suite · {tag}</div><h1>{title}</h1><p class="sub">{sub}</p><div class="kv">' + \
        ''.join(f'<div><b>{a}</b><span>{b}</span></div>' for a, b in kv) + f'</div>{svg}<div class="foot"><span>Pond side at the top, front of the house at the bottom. One grid square = 2 ft.</span><span>Draft L · Oct 29, 2026</span></div></div></body></html>'
    open(f'png-{slug}.html', 'w').write(html)
print('ok')
