import re, sys
sys.path.insert(0, '/tmp/claude-0/work/study'); import plan_svg as P
TPL = '/root/.claude/skills/synced/cc9f2c1b-608a-4e06-a091-ff5bdc1b22f3_d99a4251-bdde-4476-9656-a75eb0a5b2ff/house-styles/assets/ink-and-brass.html'
def wrap(title, main, extra_css=''):
    T = open(TPL).read()
    T = re.sub(r'<title>.*?</title>', f'<title>{title}</title>', T, 1)
    T = re.sub(r'<!-- House style:.*?-->\n', '', T, 1)
    T = T.replace('</style>', P.CSS + extra_css + '</style>', 1)
    a, b = T.index('<main class="doc">'), T.index('</main>')
    return T[:a] + '<main class="doc">' + main + T[b:]
