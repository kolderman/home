import json, sys, re
sys.path.insert(0, '/tmp/claude-0/work/study')
import plan_svg as P
src = open('build.py').read()
exec(src.split("VB_P, VB_G")[0])          # OPT with drawing fixes
exec(src[src.index("def fig("):src.index("def rows(")])   # section drawing
CSS2 = src[src.index('CSS = """') + 9:src.index('"""', src.index('CSS = """') + 9)]
o = open('office.py').read()
exec(o[o.index("T = open("):o.index("card('office'")].replace("P.CSS + '''", "P.CSS + CSS2 + '''"))
VB = (21, 19, 71, 66)
card('great-today', VB, 'New home · Living room and kitchen · For comparison', 'Today (draft L)', 'A 44 ft open room with flat 12 ft and 11 ft ceilings. Furniture blocks the walk from the front doors to the glass wall, and a notch at the kitchen front leaves the sink window facing a dark recess.',
     [('Living ceiling', 'Flat 12\''), ('Kitchen ceiling', 'Flat 11\''), ('Kitchen', '16\' × 25\''), ('Added', '—')], None)
card('great-g1', VB, 'New home · Living room and kitchen · Budget version', 'G1 · Plan reset', 'A clear 6 ft walk from the front doors to the glass. The range, a 13\'6" island and the TV all center on one line under the ridge. The kitchen notch is filled, so the sink gets a 10 ft window onto the front water feature.',
     [('Living ceiling', 'Flat 12\' (same)'), ('Kitchen', '16\' × 28\'6"'), ('Island', '13\'6" × 5\'11"'), ('Added', '56 sf')], OPT['G1'])
card('great-g2', VB, 'New home · Living room and kitchen · Recommended', 'G2 · Cathedral living room', 'Everything in G1, plus the living room ceiling opens up into the roof: 12 ft at the walls rising to about 20\'6" at a ridge beam, with three cypress trusses and your beams still every 4 ft (dashed brass lines overhead). The kitchen stays at 11 ft behind a timber portal.',
     [('Living ceiling', '12\' to about 20\'6"'), ('Kitchen', '16\' × 28\'6"'), ('Roof outside', 'No change'), ('Added', '56 sf')], OPT['G2'])
card('great-g3', VB, 'New home · Living room and kitchen · Decide later', 'G3 · Cathedral plus a pond dormer', 'G2 plus a 16 ft glass gable dormer over the glass wall, so the view from the front doors rises from the pond to the sky. Adds two roof valleys and steel at the glass wall.',
     [('Living ceiling', 'As G2, plus dormer'), ('Dormer glass', 'About 55-60 sf'), ('Roof outside', 'Adds a dormer'), ('Added', '56 sf')], OPT['G3'])
# section card
T2 = open('pond-great-g2.html').read()
sec = f'<div class="pgrid" style="display:grid;grid-template-columns:1fr;gap:18px">{fig(section_svg("now"), "Today", "Flat 12 ft ceiling, about 9 ft of attic above it")}{fig(section_svg("g2"), "With G2", "Same roof outside; the ceiling follows it up to a ridge beam", "rec")}</div>'
a = T2.index('<div class="kv">'); b = T2.index('<div class="foot">')
T2 = T2.replace(T2[a:b], sec).replace('G2 · Cathedral living room</h1>', 'Section through the living room</h1>').replace('Recommended', 'Section').replace(T2[T2.index('<p class="sub">'):T2.index('</p>', T2.index('<p class="sub">')) + 4], '<p class="sub">Cut through the front doors, looking toward the guest wing. Back porch and pond on the left, front porch and street on the right. The figure is 6 ft tall.</p>')
T2 = T2.replace('Pond side at the top. One grid square = 2 ft.', 'Heights above the main floor. Roof pitch 8:12.')
open('pond-great-section.html', 'w').write(T2)
print('ok')
