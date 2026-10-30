import sys, json, html, re
sys.path.insert(0, '/tmp/claude-0/work/draftM/ideas'); import render
T = open([l for l in __import__('glob').glob('/root/.claude/skills/synced/*/house-styles/assets/ink-and-brass.html')][0]).read()
style = T[T.index('<style>', T.index('-->')):T.index('</style>')]
links = ''.join(re.findall(r'<link[^>]*>', T[T.index('-->'):]))
def card(slug, opt, tag, n, total):
    s, css = render.svg(opt)
    css_extra = css + '''body{background:#fff;margin:0}.card{width:1300px;padding:40px 48px;background:var(--bg);font-family:"Source Sans 3",system-ui,sans-serif;box-sizing:border-box}
.card .tag{color:var(--accent);font-weight:600;font-size:15px;margin-bottom:6px}
.card h1{font:600 34px/1.15 "Source Serif 4",Georgia,serif;color:var(--ink);margin:0 0 18px}
.grid{display:grid;grid-template-columns:560px 1fr;gap:36px;align-items:start}
.plan{border-radius:10px;border:1px solid var(--rule)}
.txt p{margin:0 0 14px;font-size:19px;line-height:1.45;color:var(--body)}
.txt dl{margin:0;border-top:1px solid var(--rule)}.txt dt{font-weight:600;color:var(--muted);font-size:14px;margin-top:12px}.txt dd{margin:2px 0 0;font-size:17px;line-height:1.4;color:var(--ink)}
.foot{display:flex;justify-content:space-between;color:var(--muted);font-size:14px;margin-top:16px}'''
    rows = [('Getting into the bedroom', opt['how_you_enter_the_bedroom']), ('Powder room', opt['what_powder_does']), ('Trade-offs', opt['tradeoffs'])]
    h = (f'<!doctype html><html><head><meta charset="utf-8">{links}{style}{css_extra}</style></head><body><div class="card" id="c">'
         f'<div class="tag">New home · Suite foyer space · {('Open idea ' + str(n - 6) + ' of 3') if n > 6 else ('Idea ' + str(n) + ' of ' + str(total))}{" · " + tag if tag else ""}</div><h1>{html.escape(opt["name"])}</h1>'
         f'<div class="grid">{s}<div class="txt"><p>{html.escape(opt["pitch"])}</p><dl>' + ''.join(f'<dt>{a}</dt><dd>{html.escape(b)}</dd>' for a, b in rows) +
         f'</dl></div></div><div class="foot"><span>Pond side at the top. The strip is x 68-86 between the primary bedroom and the hall. One grid square = 2 ft.</span><span>Draft M · Oct 30, 2026</span></div></div></body></html>')
    open(f'foyer-{slug}.html', 'w').write(h)
