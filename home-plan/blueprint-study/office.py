import json, sys, re, copy
sys.path.insert(0, '/tmp/claude-0/work/study')
import plan_svg as P
S = json.load(open('pond-result.json'))['synth']
base = copy.deepcopy([c for c in S['concepts'] if c['id'] == 'OFFICE-SWAP'][0])
# new office: today's primary bedroom plus the side porch beside it, 26' x 16'
base['rooms'] = [r for r in base['rooms'] if r['name'] != 'Office'] + [
    {'name': 'Office', 'x1': 86, 'y1': 16, 'x2': 112, 'y2': 32, 'kind': 'room'},
    {'name': 'Workstation', 'x1': 102.5, 'y1': 16, 'x2': 112, 'y2': 23.5, 'kind': 'open', 'nolabel': True},
    {'name': 'Laundry stoop', 'x1': 106, 'y1': 32, 'x2': 112, 'y2': 40, 'kind': 'ext'}]
base['fixtures'] = [f for f in base['fixtures'] if not f['label'].startswith('Office') and f['label'] != 'Couch return'] + [
    {'label': 'Desk', 'x1': 103.5, 'y1': 16.2, 'x2': 111.8, 'y2': 18.8},
    {'label': 'Desk return', 'short': 'Desk', 'x1': 109.3, 'y1': 18.8, 'x2': 111.8, 'y2': 21.4},
    {'label': 'Desk chair', 'short': 'Chair', 'x1': 106, 'y1': 19.3, 'x2': 108, 'y2': 21.3},
    {'label': 'L couch', 'x1': 91.5, 'y1': 20.5, 'x2': 101.5, 'y2': 23.5},
    {'label': 'Couch return', 'short': 'Couch', 'x1': 101.5, 'y1': 20.5, 'x2': 104.5, 'y2': 26},
    {'label': 'Lounge chair', 'short': 'Chair', 'x1': 87.6, 'y1': 19.8, 'x2': 90.6, 'y2': 22.8},
    {'label': 'Lounge chair', 'short': 'Chair', 'x1': 87.6, 'y1': 23.6, 'x2': 90.6, 'y2': 26.6},
    {'label': 'Coffee table', 'short': 'Table', 'x1': 93.5, 'y1': 24.4, 'x2': 99.5, 'y2': 27},
    {'label': 'Media console', 'short': 'Console', 'x1': 92.5, 'y1': 30.3, 'x2': 101.5, 'y2': 31.7},
    {'label': '83" OLED', 'x1': 93.95, 'y1': 31.5, 'x2': 100.05, 'y2': 31.8, 'nolabel': True}]
base['openings'] = [o for o in base['openings'] if not (abs(o['x1'] - 106) < .01 and abs(o['x2'] - 106) < .01)] + [
    {'kind': 'window', 'x1': 112, 'y1': 22, 'x2': 112, 'y2': 28}]
base['erase'] = base.get('erase', []) + [[105.7, 16.3, 106.3, 31.7]]   # old bedroom east wall and slider come out
base['route'] = None
base['close'] = [[86.5, 15.8, 90.5, 16.2]]   # old bedroom-to-dressing opening is walled in
json.dump(base, open('office-layout.json', 'w'), indent=1)

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
def card(slug, vb, tag, title, sub, kv, opt, pond=False, foot='Pond side at the top. One grid square = 2 ft.'):
    svg = P.render(vb, opt, title, show_pond=pond)
    html = f'<!doctype html><html><head><meta charset="utf-8">{links}{style}</head><body><div class="card" id="c"><div class="tag">{tag}</div><h1>{title}</h1><p class="sub">{sub}</p><div class="kv">' + \
        ''.join(f'<div><b>{a}</b><span>{b}</span></div>' for a, b in kv) + f'</div>{svg}<div class="foot"><span>{foot}</span><span>Draft L · Oct 29, 2026</span></div></div></body></html>'
    open(f'pond-{slug}.html', 'w').write(html)
card('office', (84, 13, 115, 42), 'New home · Office in its new spot', 'New office: workstation plus theater corner',
     'Today\'s primary bedroom plus the side porch beside it becomes a 26 × 16 office. The desk sits in the back corner with the window beside it. The L couch and two chairs face an 83" OLED on the front wall.',
     [('Size', '26\' × 16\' · 416 sf'), ('Today\'s office', '18\' × 29\''), ('Couch to screen', 'About 9\'9"'), ('Window', '6 ft, east wall')], base)
card('1-office-swap-v2', (0, -42, 120, 52), 'New home · Primary bedroom on the pond · Your pick', 'Idea 1 with the new office',
     'The bedroom takes today\'s office spot with a 16 ft glass wall on a private garden. The office moves into today\'s primary bedroom and the side porch beside it.',
     [('Walk from the island', 'About 27 ft'), ('Hallway', 'About 2 ft'), ('Primary bedroom', '18\' × 22\''), ('Office', '26\' × 16\'')],
     dict(base, route=[[58.5, 48], [66.5, 37], [70, 35.2], [70, 34], [71.5, 27]]), pond=True,
     foot='Pond side at the top. Dashed brass line: the walk from the kitchen island to the bedroom. Grey: today\'s pond, which is being reshaped. One grid square = 2 ft.')
print('ok')
