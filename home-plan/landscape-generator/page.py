import runpy, sys, math, re
sys.path.insert(0, '.')
T = '/root/.claude/skills/synced/cc9f2c1b-608a-4e06-a091-ff5bdc1b22f3_d99a4251-bdde-4476-9656-a75eb0a5b2ff/house-styles/assets/ink-and-brass.html'
OUT = sys.argv[1] if len(sys.argv) > 1 else '/mnt/project-files/home-plan/landscape-plan.html'
sys.argv = ['plan.py', '/tmp/claude-0/-home-claude/f3cf1ba0-f40f-523c-aebf-e0d5cf75208d/scratchpad/_tmp.html', T]
H = runpy.run_path('/mnt/project-files/home-plan/plan-generator.py')
import yard_d as Y
from css import CSS
from text import body, site_labels, zoom_labels, section_svg, flow_svg

def svg(vb, cls, labels, aria):
    x, y, w, h = vb
    return (f'<svg class="plan ls {cls}" viewBox="{x} {y} {w} {h}" role="img" aria-label="{aria}">{Y.defs()}'
            f'<rect fill="#C8DAA2" x="{x}" y="{y}" width="{w}" height="{h}"/>{Y.yard()}{H["building"]("sk")}{labels}</svg>')

site = svg((-34, -116, 186, 222), "site", site_labels(), "Landscape site plan: rec pond with wetland filter and waterfall behind the house, terrace, fire pit, lawn, meadow and evergreen screen at the back, front pond and planted front yard.")
zoom = svg((-16, -82, 112, 106), "zoom", zoom_labels(), "Close-up of the rec pond with numbered features and depth zones.")
tpl = open(T).read()
head, rest = tpl.split('<main class="doc">')
head = head.replace('<title>Ink & Brass template</title>', '<title>Landscape and rec pond plan</title>')
head = re.sub(r'<!-- House style: Ink & Brass.*?-->\n', '', head)
head = head.replace('</style>', H['CSS'] + CSS + '</style>')
open(OUT, 'w').write(head + body(Y, site, zoom, section_svg(), flow_svg()) + '\n</body>\n</html>\n')
print(f"pond {Y.A_SW:.0f} sf, 5ft {Y.A5:.0f}, 8ft {Y.A8:.0f}, wetland {Y.A_WL:.0f} ({Y.A_WL / Y.A_SW:.0%}), gallons {Y.GAL:,.0f}")
