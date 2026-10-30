import json, sys, copy
sys.path.insert(0, '/tmp/claude-0/work/study')
exec(open('office.py').read().split("def card(")[0].split("T = open(")[0])   # base geometry
import re
src = open('office.py').read()
exec(src[src.index("T = open("):src.index("card('office'")])                   # style, links, card()
keep = [f for f in base['fixtures'] if f['label'] in ('King bed', 'Nightstand', 'Sitting area', 'Dresser', 'Morning bar', 'Bench', 'Powder vanity', 'Powder WC', 'Screen wall')]
def F(label, x1, y1, x2, y2, short=None, nolabel=False):
    d = dict(label=label, x1=x1, y1=y1, x2=x2, y2=y2)
    if short: d['short'] = short
    if nolabel: d['nolabel'] = True
    return d
def W(x1, y1, x2, y2): return dict(kind='window', x1=x1, y1=y1, x2=x2, y2=y2)
other_open = [o for o in base['openings'] if not (abs(o['x1'] - 112) < .01 and abs(o['x2'] - 112) < .01)]
L = {}
L['1'] = (F'Layout 1 · Like your office today', 'Same arrangement as today', 'The L couch sits against the back wall, and its return runs into your desk in the corner. The OLED goes on the front wall, about 12 ft away, with a chair on each side of the coffee table.',
  [F('L couch', 91, 16.4, 102, 19.6), F('Couch return', 102, 16.4, 105, 22.5, 'Couch'),
   F('Desk', 105, 16.2, 111.8, 18.8), F('Desk return', 109.2, 18.8, 111.8, 23, 'Desk'), F('Desk chair', 106.4, 19.6, 108.4, 21.6, 'Chair'),
   F('Lounge chair', 87.3, 21.5, 90.3, 24.5, 'Chair'), F('Lounge chair', 103, 24.6, 106, 27.6, 'Chair'),
   F('Coffee table', 93.5, 21.8, 99.5, 24.6, 'Table'), F('Media console', 92, 30.3, 101, 31.7, 'Console'), F('OLED', 93.5, 31.5, 99.6, 31.8, nolabel=True)],
  [W(112, 24, 112, 30)], [('Couch to screen', 'About 12 ft'), ('Desk', 'Back corner'), ('Window', '6 ft beside the desk'), ('Screen wall', 'Laundry side')])
L['2'] = ('Layout 2 · Screen on the outside wall', 'Best for sound', 'The OLED goes on the east wall, the only wall that isn\'t shared with another room, so the theater sound stays out of the bedroom. Windows flank it. Your desk faces the screen from the other end, so you can see it while you work.',
  [F('Media console', 110.4, 20, 111.8, 28, 'Console'), F('OLED', 111.5, 20.95, 111.8, 27.05, nolabel=True),
   F('L couch', 99.5, 19.2, 102.5, 29, 'L couch'), F('Couch return', 102.5, 19.2, 106, 22.2, 'Couch'),
   F('Lounge chair', 103.2, 27.6, 106.2, 30.6, 'Chair'), F('Coffee table', 103.8, 23, 107.6, 26.4, 'Table'),
   F('Desk', 91, 19.5, 94, 27.5), F('Desk chair', 88.6, 22.5, 90.6, 24.5, 'Chair'), F('Credenza', 86.2, 18, 87.8, 28.6, 'Credenza'),
   F('Bookcase', 91, 16.2, 98, 17.6, 'Bookcase')],
  [W(106.5, 16, 110.5, 16), W(106.5, 32, 110.5, 32)], [('Couch to screen', 'About 9\'4"'), ('Desk', 'Faces the screen'), ('Windows', 'Two, 4 ft each'), ('Screen wall', 'Outside wall')])
L['3'] = ('Layout 3 · Two rooms in one', 'Separate zones', 'A theater lounge at the west end with the OLED on the back wall, and a workstation at the east end by two windows. The couch backs onto the walk from the door to the desk.',
  [F('Media console', 89.5, 16.2, 98.5, 17.6, 'Console'), F('OLED', 90.95, 16.2, 97.05, 16.5, nolabel=True),
   F('L couch', 89.5, 26, 100, 29), F('Couch return', 86.5, 21, 89.5, 29, 'Couch'),
   F('Lounge chair', 100.6, 20, 103.6, 23, 'Chair'), F('Coffee table', 91.5, 21, 97.5, 23.8, 'Table'),
   F('Desk', 104.5, 29.4, 111.8, 31.8), F('Desk return', 109.4, 25.4, 111.8, 29.4, 'Desk'), F('Desk chair', 105.8, 26.6, 107.8, 28.6, 'Chair'),
   F('Bookcase', 103.5, 16.2, 106, 22, 'Shelves')],
  [W(112, 18.5, 112, 24.5), W(106.5, 16, 111, 16)], [('Couch to screen', 'About 9\'9"'), ('Desk', 'Front corner'), ('Windows', 'Two, beside the desk'), ('Screen wall', 'Dressing room side')])
for k, (title, tag, sub, fx, wins, kv) in L.items():
    o = copy.deepcopy(base); o['fixtures'] = keep + fx; o['openings'] = other_open + wins; o['route'] = None
    o['rooms'] = [dict(r, nolabel=True) if r['name'] == 'Office' else r for r in o['rooms'] if r['name'] != 'Workstation']
    card(f'office-{k}', (84, 13, 115, 42), f'New home · New office · {tag}', title, sub, [('Size', '26\' × 16\' · 416 sf')] + kv[:3], o)
print('ok')
